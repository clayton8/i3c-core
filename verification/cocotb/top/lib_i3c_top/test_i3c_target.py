# SPDX-License-Identifier: Apache-2.0

import logging
import random
from math import ceil

from boot import boot_init
from bus2csr import dword2int, int2dword
from ccc import CCC
from i3c_controller_fixed import I3cControllerFixed as I3cController
from i3c_recovery_interface_fixed import I3cRecoveryInterfaceFixed as I3cRecoveryInterface
from cocotbext_i3c.i3c_target import I3CTarget
from interface import I3CTopTestInterface
from utils import format_ibi_data, get_interrupt_status

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge, Timer

VALID_I3C_ADDRESSES = (
    [i for i in range(0x03, 0x3E)]
    + [i for i in range(0x3F, 0x5B)]
    + [i for i in range(0x5C, 0x5E)]
    + [i for i in range(0x5F, 0x6E)]
    + [i for i in range(0x5F, 0x6E)]
    + [i for i in range(0x6F, 0x76)]
    + [i for i in range(0x77, 0x7A)]
    + [0x7B, 0x7D]
)
TARGET_ADDRESS = 0x5A


async def timeout_task(timeout_us=5):
    """
    A generic task for handling test timeout. Waits a fixed amount of
    simulation time and then throws an exception.
    """
    await Timer(timeout_us, "us")
    raise TimeoutError("Timeout!")


async def test_setup(dut, fclk=333.0, fbus=12.5,
                     static_addr=0x5A, virtual_static_addr=0x5B,
                     dynamic_addr=None, virtual_dynamic_addr=None):
    """
    Sets up controller, target models and top-level core interface
    """

    cocotb.log.setLevel(logging.INFO)
    cocotb.start_soon(timeout_task(500000))

    dut._log.info(f"fclk = {fclk:.3f} MHz")
    dut._log.info(f"fbus = {fbus:.3f} MHz")

    i3c_controller = I3cController(
        sda_i=dut.bus_sda,
        sda_o=dut.sda_sim_ctrl_i,
        scl_i=dut.bus_scl,
        scl_o=dut.scl_sim_ctrl_i,
        debug_state_o=None,
        speed=fbus * 1e6,
    )

    i3c_target = I3CTarget(  # noqa
        sda_i=dut.bus_sda,
        sda_o=dut.sda_sim_target_i,
        scl_i=dut.bus_scl,
        scl_o=dut.scl_sim_target_i,
        debug_state_o=None,
        speed=fbus * 1e6,
    )

    tb = I3CTopTestInterface(dut)
    await tb.setup(fclk)

    # Configure the top level

    # TODO: For now test with all timings set to 0.
    timings = {
        "T_R": 0,
        "T_F": 0,
        "T_HD_DAT": 0,
        "T_SU_DAT": 0,
    }

    for k, v in timings.items():
        dut._log.info(f"{k} = {v}")

    await boot_init(tb, timings,
                    static_addr=static_addr, virtual_static_addr=virtual_static_addr,
                    dynamic_addr=dynamic_addr, virtual_dynamic_addr=virtual_dynamic_addr)

    # Set TTI queues thresholds
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.TTI.QUEUE_THLD_CTRL.base_addr,
        tb.reg_map.I3C_EC.TTI.QUEUE_THLD_CTRL.RX_DESC_THLD,
        1,
    )

    await tb.write_csr_field(
        tb.reg_map.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.base_addr,
        tb.reg_map.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.RX_DATA_THLD,
        0,  # threshold = 2 ^ (x + 1) = 2
    )

    return i3c_controller, i3c_target, tb


@cocotb.test()
async def test_i3c_target_write(dut):
    """
    Sends multiple private writes from the controller and verifies the
    target receives correct data via interrupt-driven RX descriptor
    handling.
    """
    test_data = [[0xAA, 0x00, 0xBB, 0xCC, 0xDD], [0xDE, 0xAD, 0xBA, 0xBE]]
    recv_data = []

    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    # Receiver agent (firmware side)
    async def rx_agent():
        nonlocal recv_data

        # Enable RX descriptor interrupt
        await tb.write_csr_field(
            tb.reg_map.I3C_EC.TTI.INTERRUPT_ENABLE.base_addr,
            tb.reg_map.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_STAT_EN,
            1,
        )

        for i, tx_data in enumerate(test_data):

            # Wait for the interrupt signal to go high
            irq = dut.xi3c_wrapper.i3c.irq_o
            while irq.value == 0:
                await RisingEdge(tb.clk)

            # Read & check interrupt status
            intrs = await get_interrupt_status(tb)
            assert intrs["RX_DESC_STAT"] == 1

            # Read RX descriptor, the interrupt should go low
            data = dword2int(
                await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DESC_QUEUE_PORT.base_addr, 4)
            )
            desc_len = data & 0xFFFF

            # Examine the descriptor
            assert len(tx_data) == desc_len, "Incorrect number of bytes in RX descriptor"
            remainder = desc_len % 4

            err_stat = data >> 28
            assert err_stat == 0, "Unexpected error detected"

            # Wait for the interrupt signal to go low
            irq = dut.xi3c_wrapper.i3c.irq_o
            while irq.value != 0:
                await RisingEdge(tb.clk)

            # Read & check interrupt status
            intrs = await get_interrupt_status(tb)
            assert intrs["RX_DESC_STAT"] == 0

            # Read RX data
            data_len = ceil(desc_len / 4)
            rx_data = []
            for _ in range(data_len):
                data = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DATA_PORT.base_addr, 4))
                for k in range(4):
                    rx_data.append((data >> (k * 8)) & 0xFF)

            # Remove entries that are outside of the data length
            if remainder:
                for k in range(4 - remainder):
                    rx_data.pop()

            recv_data.append(rx_data)

    # Start the device firmware agent
    cocotb.start_soon(rx_agent())

    # Send Private Writes on I3C. The agent will handle them as their come
    for test_vec in test_data:
        await i3c_controller.i3c_write(TARGET_ADDRESS, test_vec)
        await ClockCycles(tb.clk, 10)

    # Wait
    await ClockCycles(tb.clk, 100)

    # Compare
    dut._log.info(
        "Comparing input [{}] and RX data [{}]".format(
            " ".join(["[ " + " ".join([f"0x{d:02X}" for d in s]) + " ]" for s in test_data]),
            " ".join(["[ " + " ".join([f"0x{d:02X}" for d in s]) + " ]" for s in recv_data]),
        )
    )
    assert test_data == recv_data


@cocotb.test()
async def test_i3c_target_read(dut):
    """
    Tests private reads with varying queue depths: single, batched, and
    short reads (fewer bytes than queued). Verifies data correctness
    across all patterns.
    """
    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    # Generates a randomized transfer and puts it into the TTI TX queue
    async def make_transfer(min_len=1, max_len=16):

        length = random.randint(min_len, max_len)
        data = [random.randint(0, 255) for _ in range(length)]

        dut._log.info(f"Enqueueing transfer of length {length}")

        # Write data to TTI TX FIFO
        for i in range((length + 3) // 4):
            word = data[4 * i]
            if 4 * i + 1 < length:
                word |= data[4 * i + 1] << 8
            if 4 * i + 2 < length:
                word |= data[4 * i + 2] << 16
            if 4 * i + 3 < length:
                word |= data[4 * i + 3] << 24

            await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr, int2dword(word), 4)

        # Write the TX descriptor
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr, int2dword(length), 4)

        return data

    def compare(expected, received, lnt=None):
        if lnt is None or lnt == len(expected):
            sfx = ""
        else:
            sfx = " ([" + " ".join([f"{d:02X}" for d in expected[lnt:]]) + "] skipped)"
            expected = expected[:lnt]

        dut._log.info("Expected: [" + " ".join([f"{d:02X}" for d in expected]) + "]" + sfx)
        dut._log.info("Received: [" + " ".join([f"{d:02X}" for d in received]) + "]")
        assert expected == received

    # .............

    # Test N consecutive transfers. Do not queue new transfers before completion
    dut._log.info("N consecutive transfers, one at a time")
    for i in range(2):
        tx_data = await make_transfer()
        rx_data = await i3c_controller.i3c_read(TARGET_ADDRESS, len(tx_data))
        rx_data = list(rx_data.data)
        compare(tx_data, rx_data)


    # Test N consecutive transfers. First enqueue, then service
    dut._log.info("N consecutive transfers, enqueued then serviced")
    tx_data = []
    for i in range(3):
        tx_data.append(await make_transfer())

    for i in range(3):
        rx_data = await i3c_controller.i3c_read(TARGET_ADDRESS, len(tx_data[i]))
        rx_data = list(rx_data.data)
        compare(tx_data[i], rx_data)


    # Test N consecutive transfers. First enqueue, then service. Occasionally
    # read less data.
    short = random.sample([i for i in range(5)], 2)
    dut._log.info(f"N consecutive transfers, short read for {short}")

    tx_data = []
    for i in range(5):
        tx_data.append(await make_transfer(min_len=4))

    for i in range(5):
        lnt = len(tx_data[i])
        if i in short:
            lnt -= random.randint(1, 3)

        rx_data = await i3c_controller.i3c_read(TARGET_ADDRESS, lnt)
        rx_data = list(rx_data.data)
        compare(tx_data[i], rx_data, lnt)


    # Test N consecutive transfers. Do not queue new transfers before completion
    dut._log.info("N consecutive transfers, one at a time (again)")
    for i in range(2):
        tx_data = await make_transfer()
        rx_data = await i3c_controller.i3c_read(TARGET_ADDRESS, len(tx_data))
        rx_data = list(rx_data.data)
        compare(tx_data, rx_data)

    # Dummy wait


@cocotb.test()
async def test_i3c_target_read_empty(dut):
    """
    Randomly populates or leaves TX FIFO empty before each read.
    Verifies ACK + correct data when populated, NACK when empty.
    """
    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)
    # Generates a randomized transfer and puts it into the TTI TX queue
    async def make_transfer(min_len=1, max_len=16):

        length = random.randint(min_len, max_len)
        data = [random.randint(0, 255) for _ in range(length)]

        dut._log.info(f"Enqueueing transfer of length {length}")

        # Write data to TTI TX FIFO
        for i in range((length + 3) // 4):
            word = data[4 * i]
            if 4 * i + 1 < length:
                word |= data[4 * i + 1] << 8
            if 4 * i + 2 < length:
                word |= data[4 * i + 2] << 16
            if 4 * i + 3 < length:
                word |= data[4 * i + 3] << 24

            await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr, int2dword(word), 4)

        # Write the TX descriptor
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr, int2dword(length), 4)

        return data

    def compare(expected, received, lnt=None):
        if lnt is None or lnt == len(expected):
            sfx = ""
        else:
            sfx = " ([" + " ".join([f"{d:02X}" for d in expected[lnt:]]) + "] skipped)"
            expected = expected[:lnt]

        dut._log.info("Expected: [" + " ".join([f"{d:02X}" for d in expected]) + "]" + sfx)
        dut._log.info("Received: [" + " ".join([f"{d:02X}" for d in received]) + "]")
        assert expected == received

    # issue 20 random read transactions
    # randomly choose to inicialize the FIFO or not
    # if FIFO is not initialized the transation should be NACKed
    for i in range(20):
        transfer_data = random.choice([True, False])
        if transfer_data:
            tx_data = await make_transfer()
            response = await i3c_controller.i3c_read(TARGET_ADDRESS, len(tx_data), send_rsvd = random.choice([True, False]))
            assert not response.nack
            rx_data = list(response.data)
            compare(tx_data, rx_data)
        else:
            response = await i3c_controller.i3c_read(TARGET_ADDRESS, random.randint(1, 16), send_rsvd = random.choice([True, False]))
            assert response.nack


@cocotb.test()
async def test_i3c_target_read_to_multiple_targets(dut):
    """
    Issues multi-target read sequences mixing the DUT address with
    random other addresses. Verifies the target ACKs only its own
    address and NACKs all others.
    """
    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut, fclk=100)

    # Generates a randomized transfer and puts it into the TTI TX queue
    async def make_transfer(min_len=1, max_len=16):

        length = random.randint(min_len, max_len)
        data = [random.randint(0, 255) for _ in range(length)]

        dut._log.info(f"Enqueueing transfer of length {length}")

        # Write data to TTI TX FIFO
        for i in range((length + 3) // 4):
            word = data[4 * i]
            if 4 * i + 1 < length:
                word |= data[4 * i + 1] << 8
            if 4 * i + 2 < length:
                word |= data[4 * i + 2] << 16
            if 4 * i + 3 < length:
                word |= data[4 * i + 3] << 24

            await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr, int2dword(word), 4)

        # Write the TX descriptor
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr, int2dword(length), 4)

        return data

    def compare(expected, received, lnt=None):
        if lnt is None or lnt == len(expected):
            sfx = ""
        else:
            sfx = " ([" + " ".join([f"{d:02X}" for d in expected[lnt:]]) + "] skipped)"
            expected = expected[:lnt]

        dut._log.info("Expected: [" + " ".join([f"{d:02X}" for d in expected]) + "]" + sfx)
        dut._log.info("Received: [" + " ".join([f"{d:02X}" for d in received]) + "]")
        assert expected == received

    # issue 40 random read transactions
    # randomly choose to inicialize the FIFO or not
    # if FIFO is not initialized the transation should be NACKed
    for _ in range(40):
        num_transfers = random.randint(3, 10)
        addresses = []
        num_transfers_to_our_target = random.randint(1, num_transfers - 1)
        for _ in range(num_transfers_to_our_target):
            addresses.append(TARGET_ADDRESS)
        while len(addresses) < num_transfers:
            addresses.append(random.choice(VALID_I3C_ADDRESSES))
        random.shuffle(addresses)
        data_len_rsvd_stop_nack = []
        for i, addr in enumerate(addresses):
            send_rsvd = random.choice([True, False]) if i == 0 else False
            stop = i == num_transfers - 1
            if addr == TARGET_ADDRESS:
                tx_data = await make_transfer()
                data_len_rsvd_stop_nack.append((tx_data, len(tx_data), send_rsvd, stop, False))
            else:
                data_len_rsvd_stop_nack.append((None, random.randint(1, 16), send_rsvd, stop, True))

        for address, (tx_data, length, rsvd, stop, nack) in zip(addresses, data_len_rsvd_stop_nack):
            response = await i3c_controller.i3c_read(address, length, send_rsvd=rsvd, stop=stop)
            assert nack == response.nack
            if not nack:
                rx_data = list(response.data)
                compare(tx_data, rx_data)


@cocotb.test()
async def test_i3c_target_ibi(dut):
    """
    IBI test. Sends an IBI with no data and then subsequently IBIs with
    different data lengths. Expects the controller to ACK all of them and
    return correctly received data.
    """

    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    target = i3c_controller.add_target(TARGET_ADDRESS)
    target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)

    result = True

    # Enable IBI ACK-ing
    i3c_controller.enable_ibi(True)

    # Send a broadcast CCC to initialize bus timers (need STOP to start counting)
    await i3c_controller.i3c_ccc_write(ccc=CCC.BCAST.RSTDAA)

    # Write descriptor to the TTI IBI queue. No IBI data
    mdb = 0xAA
    data = []
    ibi_data = format_ibi_data(mdb, data)
    dut._log.info(" ".join([f"0x{d:08X}" for d in ibi_data]))
    for word in ibi_data:
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.IBI_PORT.base_addr, int2dword(word), 4)

    # Wait for the IBI to be serviced, check data
    response = await i3c_controller.wait_for_ibi()
    expected = bytearray([TARGET_ADDRESS, mdb] + data)
    if response != expected:
        dut._log.critical(
            "IBI MDB/data mismatch! tgt: [ {}] ctl: [ {}]".format(
                "".join("".join(f"0x{d:02X}") + " " for d in expected),
                "".join("".join(f"0x{d:02X}") + " " for d in response),
            )
        )
        result = False

    # Check LAST_IBI_STATUS
    status = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.STATUS.base_addr, 4))
    last_ibi_status = (status & (3 << 14)) >> 14
    expected_status = 0
    if last_ibi_status != expected_status:
        dut._log.critical(
            f"Incorrect IBI status, expected {expected_status}, got {last_ibi_status}"
        )
        result = False

    await ClockCycles(tb.clk, 50)

    # Write descriptor to the TTI IBI queue with some data. Check different
    # data lengths to exercise 32-bit to 8-bit conversion that happens inside
    # IBI module
    payload = [0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE, 0xBA, 0xCA]

    for lnt in [4, 5, 6, 7, 8]:

        mdb = 0xAA
        data = payload[: lnt + 1]
        ibi_data = format_ibi_data(mdb, data)
        dut._log.info(" ".join([f"0x{d:08X}" for d in ibi_data]))
        for word in ibi_data:
            await tb.write_csr(tb.reg_map.I3C_EC.TTI.IBI_PORT.base_addr, int2dword(word), 4)

        # Wait for the IBI to be serviced, check data
        response = await i3c_controller.wait_for_ibi()
        expected = bytearray([TARGET_ADDRESS, mdb] + data)
        if response != expected:
            dut._log.critical(
                "IBI MDB/data mismatch! tgt: [ {}] ctl: [ {}]".format(
                    "".join("".join(f"0x{d:02X}") + " " for d in expected),
                    "".join("".join(f"0x{d:02X}") + " " for d in response),
                )
            )
            result = False

        # Check LAST_IBI_STATUS
        status = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.STATUS.base_addr, 4))
        last_ibi_status = (status & (3 << 14)) >> 14
        expected_status = 0
        if last_ibi_status != expected_status:
            dut._log.critical(
                f"Incorrect IBI status, expected {expected_status}, got {last_ibi_status}"
            )
            result = False

        await ClockCycles(tb.clk, 50)

    # Report the test result
    assert result


@cocotb.test()
async def test_i3c_target_ibi_retry(dut):
    """
    Disables IBI ACK-ing in controller, sends an IBI, waits some time for the
    target to retry IBI transmission, re-enables IBI-acking, waits until the
    IBI gets serviced, check if IBI data was received correctly.
    """

    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    # Enable indefinite IBI retries
    #  TTI.CONTROL.IBI_EN        = 1
    #  TTI.CONTROL.IBI_RETRY_NUM = 7 (means indefinite)
    await tb.write_csr(tb.reg_map.I3C_EC.TTI.CONTROL.base_addr, int2dword(0x0000F000), 4)

    target = i3c_controller.add_target(TARGET_ADDRESS)
    target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)

    result = True

    # Send a broadcast CCC to initialize bus timers (need STOP to start counting)
    await i3c_controller.i3c_ccc_write(ccc=CCC.BCAST.RSTDAA)

    # Disable IBI ACK-ing
    i3c_controller.enable_ibi(False)

    # Write descriptor to the TTI IBI queue
    mdb = 0xAA
    data = [0xBE, 0xEF]
    ibi_data = format_ibi_data(mdb, data)
    dut._log.info(" ".join([f"0x{d:08X}" for d in ibi_data]))
    for word in ibi_data:
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.IBI_PORT.base_addr, int2dword(word), 4)

    # Wait for some time so that the target gets a change to retry IBI
    # transmission
    await Timer(10, "us")

    # Check LAST_IBI_STATUS
    status = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.STATUS.base_addr, 4))
    last_ibi_status = (status & (3 << 14)) >> 14
    expected_status = 3
    if last_ibi_status != expected_status:
        dut._log.critical(
            f"Incorrect IBI status, expected {expected_status}, got {last_ibi_status}"
        )
        result = False

    # Re-enable IBI ACK-ing
    i3c_controller.enable_ibi(True)

    # Wait for the IBI to be serviced, check data
    response = await i3c_controller.wait_for_ibi()
    expected = bytearray([TARGET_ADDRESS, mdb] + data)
    if response != expected:
        dut._log.critical(
            "IBI MDB/data mismatch! tgt: [ {}] ctl: [ {}]".format(
                "".join("".join(f"0x{d:02X}") + " " for d in expected),
                "".join("".join(f"0x{d:02X}") + " " for d in response),
            )
        )
        result = False

    # Check LAST_IBI_STATUS
    status = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.STATUS.base_addr, 4))
    last_ibi_status = (status & (3 << 14)) >> 14
    expected_status = 0
    if last_ibi_status != expected_status:
        dut._log.critical(
            f"Incorrect IBI status, expected {expected_status}, got {last_ibi_status}"
        )
        result = False

    # Dummy wait
    await ClockCycles(tb.clk, 10)

    # Report the test result
    assert result


@cocotb.test()
async def test_i3c_target_ibi_data(dut):
    """
    Set a limit on how many IBI data bytes the controller may accept. Issue
    an IBI with more data and check if it gets serviced correctly. Finally
    issue yet another IBI to check if target logic flushed the remaining data
    correctly.
    """

    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    target = i3c_controller.add_target(TARGET_ADDRESS)
    target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)

    result = True

    # Send a broadcast CCC to initialize bus timers (need STOP to start counting)
    await i3c_controller.i3c_ccc_write(ccc=CCC.BCAST.RSTDAA)

    # Limit IBI data count that the controller can accept
    i3c_controller.set_max_ibi_data_len(6)

    # Write descriptor to the TTI IBI queue
    mdb = 0xAA
    data = [0xCA, 0xFE, 0xBA, 0xCA, 0xAA, 0xBB, 0xCC, 0xDD]
    ibi_data = format_ibi_data(mdb, data)
    dut._log.info(" ".join([f"0x{d:08X}" for d in ibi_data]))
    for word in ibi_data:
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.IBI_PORT.base_addr, int2dword(word), 4)

    # Wait for the IBI to be serviced, check data
    response = await i3c_controller.wait_for_ibi()
    expected = bytearray([TARGET_ADDRESS, mdb] + data[:6])
    if response != expected:
        dut._log.critical(
            "IBI MDB/data mismatch! tgt: [ {}] ctl: [ {}]".format(
                "".join("".join(f"0x{d:02X}") + " " for d in expected),
                "".join("".join(f"0x{d:02X}") + " " for d in response),
            )
        )
        result = False

    # Wait
    await ClockCycles(tb.clk, 50)

    # Do another IBI to check if remaining data from the TTI IBI queue got
    # flushed correctly.
    mdb = 0xAA
    data = [0x11, 0x22, 0x33]
    ibi_data = format_ibi_data(mdb, data)
    dut._log.info(" ".join([f"0x{d:08X}" for d in ibi_data]))
    for word in ibi_data:
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.IBI_PORT.base_addr, int2dword(word), 4)

    # Wait for the IBI to be serviced, check data
    response = await i3c_controller.wait_for_ibi()
    expected = bytearray([TARGET_ADDRESS, mdb] + data)
    if response != expected:
        dut._log.critical(
            "IBI MDB/data mismatch! tgt: [ {}] ctl: [ {}]".format(
                "".join("".join(f"0x{d:02X}") + " " for d in expected),
                "".join("".join(f"0x{d:02X}") + " " for d in response),
            )
        )
        result = False

    # Dummy wait
    await ClockCycles(tb.clk, 10)

    # Report the test result
    assert result


@cocotb.test()
async def test_i3c_target_writes_and_reads(dut):
    """
    Interleaves private writes and reads in a single test: sends two
    writes, drains them from the RX FIFO, then reads back pre-queued
    TX data.
    """
    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    tx_data_len = 16
    tx_test_data = [random.randint(0, 255) for _ in range(tx_data_len)]

    # Write data to TTI TX FIFO
    for i in range(0, len(tx_test_data), 4):
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr, tx_test_data[i : i + 4], 4)

    # Write the TX descriptor
    await tb.write_csr(
        tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr, int2dword(tx_data_len), 4
    )

    # Send Private Write on I3C
    test_data = [[0xAA, 0x00, 0xBB, 0xCC, 0xDD], [0xDE, 0xAD, 0xBA, 0xBE]]
    for test_vec in test_data:
        await i3c_controller.i3c_write(TARGET_ADDRESS, test_vec)
        await ClockCycles(tb.clk, 10)

    # Wait for an interrupt
    wait_irq = True
    timeout = 0
    # Number of clock cycles after which we should observe an interrupt
    TIMEOUT_THRESHOLD = 50
    while wait_irq:
        timeout += 1
        await ClockCycles(tb.clk, 10)
        irq = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.base_addr, 4))
        if irq:
            wait_irq = False
            dut._log.debug(":::Interrupt was raised:::")
        if timeout > TIMEOUT_THRESHOLD:
            wait_irq = False
            dut._log.debug(":::Timeout cancelled polling:::")

    # Read data
    recv_data = []
    for test_vec in test_data:
        recv_xfer = []
        # Read RX descriptor
        r_data = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DESC_QUEUE_PORT.base_addr, 4))
        desc_len = r_data & 0xFFFF
        assert len(test_vec) == desc_len, "Incorrect number of bytes in RX descriptor"
        remainder = desc_len % 4
        err_stat = r_data >> 28
        assert err_stat == 0, "Unexpected error detected"

        # Read RX data
        data_len = ceil(desc_len / 4)
        for _ in range(data_len):
            r_data = dword2int(await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DATA_PORT.base_addr, 4))
            for k in range(4):
                recv_xfer.append((r_data >> (k * 8)) & 0xFF)

        # Remove entries that are outside of the data length
        if remainder:
            for k in range(4 - remainder):
                recv_xfer.pop()
        recv_data.append(recv_xfer)

    # Compare
    dut._log.info(
        "Comparing input [{}] and RX data [{}]".format(
            " ".join(["[ " + " ".join([f"0x{d:02X}" for d in s]) + " ]" for s in test_data]),
            " ".join(["[ " + " ".join([f"0x{d:02X}" for d in s]) + " ]" for s in recv_data]),
        )
    )
    assert test_data == recv_data

    # Issue a private read
    recv_data = await i3c_controller.i3c_read(TARGET_ADDRESS, 16)
    recv_data = list(recv_data.data)

    assert tx_test_data == recv_data

    # Dummy wait
    await ClockCycles(tb.clk, 10)


@cocotb.test()
async def test_i3c_target_pwrite_err_detection(dut):
    """
    Injects T-bit parity errors on private writes and verifies the
    target sets PROTOCOL_ERROR, drops all received bytes (desc_len=0),
    and recovers for subsequent transfers.
    """
    I3C_DIRECT_GETSTATUS = 0x90
    PROTOCOL_ERR_LOW = 5

    # Setup
    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(VALID_I3C_ADDRESSES, 4)
    # Initialize
    i3c_controller, _, tb = await test_setup(dut,
        static_addr=STATIC_ADDR, virtual_static_addr=VIRT_STATIC_ADDR,
        dynamic_addr=DYNAMIC_ADDR, virtual_dynamic_addr=VIRT_DYNAMIC_ADDR)

    for i in range(random.randint(5, 10)):
        target_addr = DYNAMIC_ADDR
        # Check error status
        err_status = await tb.read_csr_field(
            tb.reg_map.I3C_EC.TTI.STATUS.base_addr, tb.reg_map.I3C_EC.TTI.STATUS.PROTOCOL_ERROR
        )
        assert err_status == 0, "Unexpected error detected"

        # Read target status to ensure there's no error
        result = await i3c_controller.i3c_ccc_read(
            ccc=I3C_DIRECT_GETSTATUS, addr=target_addr, count=2
        )
        status = result[0][1]
        status = int.from_bytes(status, byteorder="big", signed=False)
        assert (
            (status >> PROTOCOL_ERR_LOW) & 1
        ) == 0, "GETSTATUS reported unexpected Protocol Error"

        # Test corner case with data length 1
        TRANSFER_LENGTH = random.randint(1, 256) if i != 0 else 1

        # Send Private Write on I3C
        test_data = [random.randint(0, 255) for _ in range(TRANSFER_LENGTH)]
        await i3c_controller.i3c_write(target_addr, test_data, inject_tbit_err=True)
        await ClockCycles(tb.clk, 10)

        # Check error status
        err_status = await tb.read_csr_field(
            tb.reg_map.I3C_EC.TTI.STATUS.base_addr, tb.reg_map.I3C_EC.TTI.STATUS.PROTOCOL_ERROR
        )
        assert err_status == 1, "Expected error was not detected"
        # Read RX descriptor
        data = dword2int(
            await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DESC_QUEUE_PORT.base_addr, 4)
        )
        err_stat = data >> 28
        assert err_stat == 1, "Expected error detection"

        desc_len = data & 0xFFFF
        assert desc_len == 1

        # Clear RX data FIFO
        await tb.write_csr_field(
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.base_addr,
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.RX_DATA_RST,
            1,
        )
        await tb.write_csr_field(
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.base_addr,
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.RX_DATA_RST,
            0,
        )

        # Read target status to clear error
        result = await i3c_controller.i3c_ccc_read(
            ccc=I3C_DIRECT_GETSTATUS, addr=target_addr, count=2
        )
        status = result[0][1]
        status = int.from_bytes(status, byteorder="big", signed=False)
        assert ((status >> PROTOCOL_ERR_LOW) & 1) == 1, "GETSTATUS did not report Protocol Error"

        # Check error status
        err_status = await tb.read_csr_field(
            tb.reg_map.I3C_EC.TTI.STATUS.base_addr, tb.reg_map.I3C_EC.TTI.STATUS.PROTOCOL_ERROR
        )
        assert err_status == 0, "Unexpected error detected"
        await ClockCycles(tb.clk, 100)

    await ClockCycles(tb.clk, 100)


@cocotb.test()
async def test_i3c_target_pwrite_overflow_detection(dut):
    """
    Sends private writes exceeding the RX FIFO capacity (261-512 bytes).
    Verifies the target captures exactly 260 bytes (256 FIFO + 4 pipeline),
    flags err_stat in the RX descriptor, but does NOT set PROTOCOL_ERROR.
    """
    I3C_DIRECT_GETSTATUS = 0x90
    PROTOCOL_ERR_LOW = 5

    # Setup
    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(VALID_I3C_ADDRESSES, 4)
    # Initialize
    i3c_controller, _, tb = await test_setup(dut,
        static_addr=STATIC_ADDR, virtual_static_addr=VIRT_STATIC_ADDR,
        dynamic_addr=DYNAMIC_ADDR, virtual_dynamic_addr=VIRT_DYNAMIC_ADDR)

    for _ in range(random.randint(5, 10)):
        target_addr = DYNAMIC_ADDR
        # Check error status
        err_status = await tb.read_csr_field(
            tb.reg_map.I3C_EC.TTI.STATUS.base_addr, tb.reg_map.I3C_EC.TTI.STATUS.PROTOCOL_ERROR
        )
        assert err_status == 0, "Unexpected error detected"

        # Read target status to ensure there's no error
        result = await i3c_controller.i3c_ccc_read(
            ccc=I3C_DIRECT_GETSTATUS, addr=target_addr, count=2
        )
        status = result[0][1]
        status = int.from_bytes(status, byteorder="big", signed=False)
        assert (
            (status >> PROTOCOL_ERR_LOW) & 1
        ) == 0, "GETSTATUS reported unexpected Protocol Error"
        # FIFO size is 256 bytes + 4 bytes in the width conversion stage
        TRANSFER_LENGTH = random.randint(261, 512)

        # Send Private Write on I3C
        test_data = [random.randint(0, 255) for _ in range(TRANSFER_LENGTH)]
        await i3c_controller.i3c_write(target_addr, test_data)
        await ClockCycles(tb.clk, 10)

        # Check error status
        err_status = await tb.read_csr_field(
            tb.reg_map.I3C_EC.TTI.STATUS.base_addr, tb.reg_map.I3C_EC.TTI.STATUS.PROTOCOL_ERROR
        )
        assert err_status == 0, "Overflow is not a Protocol Error"
        # Read RX descriptor
        data = dword2int(
            await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DESC_QUEUE_PORT.base_addr, 4)
        )
        err_stat = data >> 28
        assert err_stat == 1, "Expected error detection"

        desc_len = data & 0xFFFF
        assert desc_len == 260

        # Clear RX data FIFO
        await tb.write_csr_field(
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.base_addr,
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.RX_DATA_RST,
            1,
        )
        await tb.write_csr_field(
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.base_addr,
            tb.reg_map.I3C_EC.TTI.RESET_CONTROL.RX_DATA_RST,
            0,
        )

        await ClockCycles(tb.clk, 100)

    await ClockCycles(tb.clk, 100)


@cocotb.test()
async def test_i3c_target_private_read_sizes_and_abort(dut):
    """
    Test private read transfers with specific sizes and controller-initiated aborts.

    1. Private read of exactly 256 bytes
    2. Private read of exactly 8 bytes
    3. Private read of exactly 11 bytes (non-word-aligned)
    4. Private read: target has 64 bytes, controller aborts after 4 bytes,
       then recovery read verifies target is still functional
    5. Private read: target has 64 bytes, controller aborts after 5 bytes
       (non-word-aligned), then recovery read verifies target is still
       functional
    """

    # Setup
    i3c_controller, i3c_target, tb = await test_setup(dut)

    async def enqueue_tx_data(data):
        """Write data to TTI TX FIFO and TX descriptor."""
        length = len(data)

        # Write data to TTI TX FIFO
        for i in range((length + 3) // 4):
            word = data[4 * i]
            if 4 * i + 1 < length:
                word |= data[4 * i + 1] << 8
            if 4 * i + 2 < length:
                word |= data[4 * i + 2] << 16
            if 4 * i + 3 < length:
                word |= data[4 * i + 3] << 24

            await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr, int2dword(word), 4)

        # Write the TX descriptor
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr, int2dword(length), 4)

    def compare(expected, received):
        dut._log.info("Expected: [" + " ".join([f"{d:02X}" for d in expected]) + "]")
        dut._log.info("Received: [" + " ".join([f"{d:02X}" for d in received]) + "]")
        assert expected == received

    # ---- Test 1: Private read of exactly 256 bytes ----
    dut._log.info("Test 1: Private read of 256 bytes")
    tx_data_256 = [random.randint(0, 255) for _ in range(256)]
    await enqueue_tx_data(tx_data_256)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 256)
    assert not rx_resp.nack, "Unexpected NACK on 256-byte read"
    compare(tx_data_256, list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    # ---- Test 2: Private read of exactly 8 bytes ----
    dut._log.info("Test 2: Private read of 8 bytes")
    tx_data_8 = [random.randint(0, 255) for _ in range(8)]
    await enqueue_tx_data(tx_data_8)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 8)
    assert not rx_resp.nack, "Unexpected NACK on 8-byte read"
    compare(tx_data_8, list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    # ---- Test 3: Private read of exactly 11 bytes (non-word-aligned) ----
    dut._log.info("Test 3: Private read of 11 bytes")
    tx_data_11 = [random.randint(0, 255) for _ in range(11)]
    await enqueue_tx_data(tx_data_11)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 11)
    assert not rx_resp.nack, "Unexpected NACK on 11-byte read"
    compare(tx_data_11, list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    # ---- Test 4: Controller aborts after 4 bytes (target has 64) ----
    dut._log.info("Test 4: Controller abort after 4 bytes (word-aligned)")
    tx_data_64a = [random.randint(0, 255) for _ in range(64)]
    await enqueue_tx_data(tx_data_64a)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 4)
    assert not rx_resp.nack, "Unexpected NACK on abort read"
    compare(tx_data_64a[:4], list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    # After abort, do a normal transfer to verify the target recovered
    dut._log.info("Test 4 recovery: Normal 8-byte read after abort")
    tx_data_recover = [random.randint(0, 255) for _ in range(8)]
    await enqueue_tx_data(tx_data_recover)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 8)
    assert not rx_resp.nack, "Unexpected NACK on recovery read"
    compare(tx_data_recover, list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    # ---- Test 5: Controller aborts after 5 bytes (non-word-aligned) ----
    dut._log.info("Test 5: Controller abort after 5 bytes (non-word-aligned)")
    tx_data_64b = [random.randint(0, 255) for _ in range(64)]
    await enqueue_tx_data(tx_data_64b)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 5)
    assert not rx_resp.nack, "Unexpected NACK on abort read"
    compare(tx_data_64b[:5], list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    # After abort, do a normal transfer to verify the target recovered
    dut._log.info("Test 5 recovery: Normal 8-byte read after abort")
    tx_data_recover2 = [random.randint(0, 255) for _ in range(8)]
    await enqueue_tx_data(tx_data_recover2)
    rx_resp = await i3c_controller.i3c_read(TARGET_ADDRESS, 8)
    assert not rx_resp.nack, "Unexpected NACK on recovery read"
    compare(tx_data_recover2, list(rx_resp.data))
    await ClockCycles(tb.clk, 10)

    await ClockCycles(tb.clk, 100)


@cocotb.test()
async def test_i3c_target_private_read_tbit_abort_and_chain(dut):
    """
    Verifies the I3C T-bit abort mechanism during a private read (16-byte
    TTI TX response), followed by chained transactions without releasing
    the bus.

    Preloads 16 bytes into TTI TX FIFO. Abort points: byte 1 (first),
    byte 10 (mid-transfer), byte 15 (second-to-last).

    Parts 1-3:   Private read abort → RI read (DEVICE_ID)
    Parts 4-6:   Private read abort → CCC GETSTATUS read
    Parts 7-9:   Private read abort → Private read
    Parts 10-12: Private read abort → RI write (RECOVERY_CTRL)
    Parts 13-15: Private read abort → CCC SETMWL write
    Parts 16-18: Private read abort → Private write
    """

    STATIC_ADDR = 0x5A
    VIRT_STATIC_ADDR = 0x5B
    DYNAMIC_ADDR = 0x52
    VIRT_DYNAMIC_ADDR = 0x53

    i3c_controller, i3c_target, tb = await test_setup(dut)
    recovery = I3cRecoveryInterface(i3c_controller)

    await tb.enable_target_err_intr()

    # Enable recovery mode so RI commands are accepted
    await tb.write_csr(
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_STATUS_0.base_addr,
        int2dword(0x3), 4,
    )

    # Assign dynamic addresses
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(STATIC_ADDR, [DYNAMIC_ADDR << 1])]
    )
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(VIRT_STATIC_ADDR, [VIRT_DYNAMIC_ADDR << 1])]
    )

    def make_word(bs):
        return (bs[3] << 24) | (bs[2] << 16) | (bs[1] << 8) | bs[0]

    # Pre-load DEVICE_ID for chained RI reads
    device_id_bytes = [random.randint(1, 255) for _ in range(24)]
    for i, reg in enumerate([
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_ID_0,
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_ID_1,
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_ID_2,
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_ID_3,
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_ID_4,
        tb.reg_map.I3C_EC.SECFWRECOVERYIF.DEVICE_ID_5,
    ]):
        await tb.write_csr(reg.base_addr, int2dword(make_word(device_id_bytes[i*4:(i+1)*4])), 4)

    # Baseline DEVICE_ID read
    expected_dev_id, pec_ok = await recovery.command_read(
        VIRT_DYNAMIC_ADDR, I3cRecoveryInterface.Command.DEVICE_ID
    )
    assert pec_ok, "Baseline DEVICE_ID read failed"
    dut._log.info(f"Baseline DEVICE_ID: {len(expected_dev_id)} bytes")

    # 16-byte TX payload for private reads
    tx_payload = [random.randint(0, 255) for _ in range(16)]
    dut._log.info(f"TX payload: {[f'0x{b:02X}' for b in tx_payload]}")

    abort_configs = [
        (1,  "byte 1 (first)"),
        (10, "byte 10 (mid-transfer)"),
        (15, "byte 15 (second-to-last)"),
    ]

    async def queue_tx_data(data):
        """Load TX FIFO in 4-byte words, then write the descriptor."""
        for i in range(0, len(data), 4):
            await tb.write_csr(
                tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr, data[i:i+4], 4,
            )
        await tb.write_csr(
            tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr,
            int2dword(len(data)), 4,
        )

    # =========================================================================
    # Parts 1-3: Private read abort → RI read (DEVICE_ID)
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=1):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort private read after {desc}, chain into RI DEVICE_ID read")

        await queue_tx_data(tx_payload)

        abort_bytes = await i3c_controller.i3c_read_abort(
            addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        for idx in range(abort_count):
            assert abort_bytes[idx] == tx_payload[idx], (
                f"Part {part_num}: Byte {idx} mismatch: got 0x{abort_bytes[idx]:02X}, "
                f"expected 0x{tx_payload[idx]:02X}"
            )
        dut._log.info(f"  Aborted {abort_count} byte(s), data correct")

        chain_data, chain_pec_ok = await recovery.command_read(
            VIRT_DYNAMIC_ADDR,
            I3cRecoveryInterface.Command.DEVICE_ID,
            start=False,
        )

        assert chain_data is not None, f"Part {part_num}: Chained DEVICE_ID read returned None"
        assert chain_pec_ok, f"Part {part_num}: Chained DEVICE_ID PEC failed"
        assert chain_data == expected_dev_id, f"Part {part_num}: DEVICE_ID data mismatch"
        dut._log.info(f"  Chained DEVICE_ID read OK: {len(chain_data)} bytes, PEC valid")

    # =========================================================================
    # Parts 4-6: Private read abort → CCC GETSTATUS read
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=4):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort private read after {desc}, chain into CCC GETSTATUS")

        await queue_tx_data(tx_payload)

        abort_bytes = await i3c_controller.i3c_read_abort(
            addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        dut._log.info(f"  Aborted {abort_count} byte(s)")

        responses = await i3c_controller.i3c_ccc_read_chained(
            ccc=CCC.DIRECT.GETSTATUS, addr=DYNAMIC_ADDR, count=2
        )

        assert len(responses) == 1, f"Part {part_num}: Expected 1 response"
        ack, status_data = responses[0]
        assert ack, f"Part {part_num}: CCC GETSTATUS got NACK"
        assert len(status_data) == 2, f"Part {part_num}: GETSTATUS unexpected length"
        dut._log.info(f"  Chained CCC GETSTATUS OK: 0x{status_data[0]:02X} 0x{status_data[1]:02X}")

    # =========================================================================
    # Parts 7-9: Private read abort → Private read (fresh TX data)
    # =========================================================================
    chain_read_data = [random.randint(0, 255) for _ in range(4)]

    for part_num, (abort_count, desc) in enumerate(abort_configs, start=7):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort private read after {desc}, chain into private read")

        # Queue the abort source (16 bytes)
        await queue_tx_data(tx_payload)

        abort_bytes = await i3c_controller.i3c_read_abort(
            addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        dut._log.info(f"  Aborted {abort_count} byte(s)")

        # Queue fresh data for the chained read
        await queue_tx_data(chain_read_data)

        readback = await i3c_controller.i3c_read_chained(DYNAMIC_ADDR, len(chain_read_data))

        assert list(readback.data) == chain_read_data, (
            f"Part {part_num}: Private read mismatch:\n"
            f"  got:      {[f'0x{b:02X}' for b in readback.data]}\n"
            f"  expected: {[f'0x{b:02X}' for b in chain_read_data]}"
        )
        dut._log.info(f"  Chained private read OK: {[f'0x{b:02X}' for b in readback.data]}")

    # =========================================================================
    # Parts 10-12: Private read abort → RI write (RECOVERY_CTRL)
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=10):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort private read after {desc}, chain into RI write")

        write_val = (part_num & 0xFF)
        ri_write_data = [write_val, write_val ^ 0xFF, write_val + 1]

        await queue_tx_data(tx_payload)

        abort_bytes = await i3c_controller.i3c_read_abort(
            addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        dut._log.info(f"  Aborted {abort_count} byte(s)")

        await recovery.command_write(
            VIRT_DYNAMIC_ADDR,
            I3cRecoveryInterface.Command.RECOVERY_CTRL,
            ri_write_data, start=False,
        )

        csr_val = dword2int(
            await tb.read_csr(tb.reg_map.I3C_EC.SECFWRECOVERYIF.RECOVERY_CTRL.base_addr, 4)
        )
        written_word = ri_write_data[0] | (ri_write_data[1] << 8) | (ri_write_data[2] << 16)
        assert (csr_val & 0xFFFFFF) == written_word, (
            f"Part {part_num}: RECOVERY_CTRL mismatch: got 0x{csr_val:08X}, "
            f"expected 0x{written_word:06X}"
        )
        dut._log.info(f"  RI write verified: RECOVERY_CTRL = 0x{csr_val:08X}")

    # =========================================================================
    # Parts 13-15: Private read abort → CCC SETMWL write
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=13):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort private read after {desc}, chain into CCC SETMWL")

        mwl_val = 64 + part_num
        mwl_bytes = [mwl_val & 0xFF, (mwl_val >> 8) & 0xFF]

        await queue_tx_data(tx_payload)

        abort_bytes = await i3c_controller.i3c_read_abort(
            addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        dut._log.info(f"  Aborted {abort_count} byte(s)")

        acks = await i3c_controller.i3c_ccc_write_chained(
            ccc=CCC.DIRECT.SETMWL,
            directed_data=[(DYNAMIC_ADDR, mwl_bytes)],
        )
        assert len(acks) == 1 and acks[0], f"Part {part_num}: CCC SETMWL got NACK"

        responses = await i3c_controller.i3c_ccc_read(
            ccc=CCC.DIRECT.GETMWL, addr=DYNAMIC_ADDR, count=2
        )
        ack, mwl_readback = responses[0]
        assert ack and list(mwl_readback) == mwl_bytes, (
            f"Part {part_num}: MWL readback mismatch"
        )
        dut._log.info(f"  CCC SETMWL verified: MWL = {mwl_val}")

    # =========================================================================
    # Parts 16-18: Private read abort → Private write
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=16):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort private read after {desc}, chain into private write")

        priv_write_data = [part_num & 0xFF, 0xCA, 0xFE, 0x00 | part_num]

        await queue_tx_data(tx_payload)

        abort_bytes = await i3c_controller.i3c_read_abort(
            addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        dut._log.info(f"  Aborted {abort_count} byte(s)")

        await i3c_controller.i3c_write_after_abort(DYNAMIC_ADDR, priv_write_data)

        rx_desc = dword2int(
            await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DESC_QUEUE_PORT.base_addr, 4)
        )
        rx_len = rx_desc & 0xFFFF
        assert rx_len == len(priv_write_data), (
            f"Part {part_num}: RX length mismatch: got {rx_len}, expected {len(priv_write_data)}"
        )

        rx_data = []
        for _ in range((rx_len + 3) // 4):
            word = dword2int(
                await tb.read_csr(tb.reg_map.I3C_EC.TTI.RX_DATA_PORT.base_addr, 4)
            )
            for i in range(4):
                if len(rx_data) < rx_len:
                    rx_data.append((word >> (8 * i)) & 0xFF)

        assert rx_data == priv_write_data, (
            f"Part {part_num}: Private write mismatch:\n"
            f"  got:      {[f'0x{b:02X}' for b in rx_data]}\n"
            f"  expected: {[f'0x{b:02X}' for b in priv_write_data]}"
        )
        dut._log.info(f"  Private write verified: {[f'0x{b:02X}' for b in rx_data]}")

    await tb.assert_no_target_errors()
