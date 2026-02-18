# SPDX-License-Identifier: Apache-2.0

"""
IBI (In-Band Interrupt) verification tests for I3C SDR Target.

Covers spec Sec 5.1.6: accept/refuse/retry/disable flows, arbitration,
Repeated-Start suppression, CCC interleaving, and Pending Read Notification.
"""

import logging
import random

from boot import boot_init
from bus2csr import int2dword
from ccc import CCC
from i3c_controller_fixed import I3cControllerFixed as I3cController
from cocotbext_i3c.i3c_target import I3CTarget
from interface import I3CTopTestInterface
from utils import format_ibi_data, get_interrupt_status

import cocotb
from cocotb.regression import TestFactory
from cocotb.result import SimTimeoutError
from cocotb.triggers import ClockCycles, Timer, with_timeout

# =============================================================================
# Constants
# =============================================================================

TARGET_ADDRESS = 0x5A


# =============================================================================
# Shared Helpers
# =============================================================================

async def timeout_task(timeout_us):
    await Timer(timeout_us, "us")
    raise TimeoutError("Timeout!")


async def test_setup(dut, fclk=333.0, fbus=12.5,
                     static_addr=TARGET_ADDRESS, timeout_us=500000):
    """Standard setup: controller + VIP target + DUT boot."""

    cocotb.log.setLevel(logging.INFO)
    cocotb.start_soon(timeout_task(timeout_us))

    i3c_controller = I3cController(
        sda_i=dut.bus_sda,
        sda_o=dut.sda_sim_ctrl_i,
        scl_i=dut.bus_scl,
        scl_o=dut.scl_sim_ctrl_i,
        debug_state_o=None,
        speed=fbus * 1e6,
    )

    i3c_target = I3CTarget(
        sda_i=dut.bus_sda,
        sda_o=dut.sda_sim_target_i,
        scl_i=dut.bus_scl,
        scl_o=dut.scl_sim_target_i,
        debug_state_o=None,
        speed=fbus * 1e6,
    )

    tb = I3CTopTestInterface(dut)
    await tb.setup(fclk)
    await boot_init(tb, fclk=fclk, static_addr=static_addr)

    return i3c_controller, i3c_target, tb


async def init_ibi(i3c_controller, tb, addr=TARGET_ADDRESS, retry_num=7):
    """Common IBI initialization: add target to controller, set retry, init timers."""
    target = i3c_controller.add_target(addr)
    target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)
    i3c_controller.enable_ibi(True)

    # Set IBI_RETRY_NUM and IBI_EN via CSR
    await set_ibi_retry_num(tb, retry_num)
    await set_ibi_enable(tb, True)

    # Broadcast CCC to initialize bus timers (STOP starts bus-available counting)
    await i3c_controller.i3c_ccc_write(ccc=CCC.BCAST.RSTDAA)

    return target


async def send_ibi(tb, mdb, data=None):
    """Queue an IBI descriptor + payload into TTI IBI_PORT."""
    if data is None:
        data = []
    ibi_words = format_ibi_data(mdb, data)
    for word in ibi_words:
        await tb.write_csr(tb.reg_map.I3C_EC.TTI.IBI_PORT.base_addr, int2dword(word), 4)


async def check_ibi_status(tb, expected, msg=""):
    """Read and assert LAST_IBI_STATUS from TTI.STATUS register."""
    status = await tb.read_csr_field(
        tb.reg_map.I3C_EC.TTI.STATUS.base_addr,
        tb.reg_map.I3C_EC.TTI.STATUS.LAST_IBI_STATUS,
    )
    assert status == expected, (
        f"LAST_IBI_STATUS mismatch{' (' + msg + ')' if msg else ''}: "
        f"expected {expected}, got {status}"
    )


async def set_ibi_retry_num(tb, value):
    """Write TTI.CONTROL.IBI_RETRY_NUM field (bits [15:13])."""
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.TTI.CONTROL.base_addr,
        tb.reg_map.I3C_EC.TTI.CONTROL.IBI_RETRY_NUM,
        value,
    )


async def set_ibi_enable(tb, enable):
    """Write TTI.CONTROL.IBI_EN field (bit 12)."""
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.TTI.CONTROL.base_addr,
        tb.reg_map.I3C_EC.TTI.CONTROL.IBI_EN,
        1 if enable else 0,
    )


async def check_ibi_done(tb, expected):
    """Assert IBI_DONE interrupt status matches expected value."""
    intrs = await get_interrupt_status(tb)
    assert intrs["IBI_DONE"] == expected, (
        f"IBI_DONE mismatch: expected {expected}, got {intrs['IBI_DONE']}"
    )


async def check_pending_interrupt(tb, expected):
    """Assert PENDING_INTERRUPT[0] (ibi_pending) matches expected value."""
    pending = await tb.read_csr_field(
        tb.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.base_addr,
        tb.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.PENDING_INTERRUPT,
    )
    actual = pending & 0x1
    assert actual == expected, (
        f"PENDING_INTERRUPT[0] mismatch: expected {expected}, got {actual}"
    )


async def verify_ibi_response(dut, response, addr, mdb, data):
    """Verify IBI response from controller matches expected addr+mdb+data."""
    expected = bytearray([addr, mdb] + (data or []))
    assert response == expected, (
        f"IBI data mismatch: "
        f"expected [{' '.join(f'0x{b:02X}' for b in expected)}], "
        f"got [{' '.join(f'0x{b:02X}' for b in response)}]"
    )


async def expect_no_ibi(i3c_controller, timeout, units="us"):
    """Assert no IBI fires within the given timeout. Deterministic cleanup
    via with_timeout — no orphaned background tasks."""
    try:
        await with_timeout(i3c_controller.wait_for_ibi(), timeout, units)
        raise AssertionError(f"Unexpected IBI observed within {timeout}{units}")
    except SimTimeoutError:
        pass


# =============================================================================
# Test 1: Accept IBI — read all data
# =============================================================================

@cocotb.test()
async def test_ibi_accept_read_all_data(dut):
    """
    Sec 5.1.6.2 item 1: Accept IBI, read all data bytes.
    Exercises MDB-only and various payload lengths.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # Sub-cases: MDB-only, 1 byte, 4 bytes, random length
    test_vectors = [
        (random.randint(0x00, 0xFF), []),
        (random.randint(0x00, 0xFF), [random.randint(0, 255)]),
        (random.randint(0x00, 0xFF), [random.randint(0, 255) for _ in range(4)]),
        (random.randint(0x00, 0xFF), [random.randint(0, 255) for _ in range(random.randint(2, 8))]),
    ]

    for mdb, data in test_vectors:
        dut._log.info(f"IBI: MDB=0x{mdb:02X}, len={len(data)}")

        # PENDING_INTERRUPT should be 0 before queueing
        await check_pending_interrupt(tb, 0)

        await send_ibi(tb, mdb, data)

        # PENDING_INTERRUPT should assert while IBI is in-flight
        await ClockCycles(tb.clk, 5)
        await check_pending_interrupt(tb, 1)

        response = await i3c_controller.wait_for_ibi()
        await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
        await check_ibi_status(tb, 0, f"MDB=0x{mdb:02X}")

        # PENDING_INTERRUPT should clear after IBI completes
        await ClockCycles(tb.clk, 10)
        await check_pending_interrupt(tb, 0)
        await check_ibi_done(tb, 0)

        await ClockCycles(tb.clk, 50)


# =============================================================================
# Test 2: Accept partial — target must NOT repeat
# =============================================================================

@cocotb.test()
async def test_ibi_accept_partial_no_repeat(dut):
    """
    Sec 5.1.6.2 item 1.a: Controller truncates additional bytes.
    Target shall NOT repeat the unserviced IBI.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # Controller accepts only MDB + 2 data bytes
    i3c_controller.set_max_ibi_data_len(2)

    mdb = 0xAA
    # 20 bytes (5 words) to exercise descriptor_ibi multi-word Flush state (CP18)
    full_data = [0xCA, 0xFE, 0xBA, 0xCA, 0xAA, 0xBB, 0xCC, 0xDD,
                 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
                 0x99, 0xAB, 0xCD, 0xEF]
    await send_ibi(tb, mdb, full_data)

    response = await i3c_controller.wait_for_ibi()
    # Controller should have received only MDB + first 2 data bytes
    expected_truncated = bytearray([TARGET_ADDRESS, mdb] + full_data[:2])
    assert response == expected_truncated, (
        f"Truncated IBI mismatch: expected {expected_truncated.hex()}, got {response.hex()}"
    )

    # RTL reports IbiFailurePartialData (0b10) on controller-initiated abort
    await ClockCycles(tb.clk, 50)
    await check_ibi_status(tb, 2, "partial data")

    # Verify target does NOT repeat the unserviced IBI
    await expect_no_ibi(i3c_controller, 10)

    # Spec L27: "Controller will service it at a later time" — verify the target
    # can serve data via Private Read after IBI abort. RTL flushes IBI data on
    # abort, so Host must re-provide remaining data via TX path.
    remaining_data = full_data[2:]  # Data that was truncated
    for i in range(0, len(remaining_data), 4):
        chunk = remaining_data[i:i + 4]
        word = 0
        for j, b in enumerate(chunk):
            word |= b << (8 * j)
        await tb.write_csr(
            tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr,
            int2dword(word), 4,
        )
    await tb.write_csr(
        tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr,
        int2dword(len(remaining_data)), 4,
    )

    read_response = await i3c_controller.i3c_read(TARGET_ADDRESS, len(remaining_data))
    assert not read_response.nack, "Private Read after partial abort was NACKed"
    assert list(read_response.data[:len(remaining_data)]) == remaining_data, (
        f"Private Read data mismatch: expected {remaining_data}, "
        f"got {list(read_response.data[:len(remaining_data)])}"
    )

    await ClockCycles(tb.clk, 50)

    # Reset max length and verify a fresh IBI works (queue flushed correctly)
    i3c_controller.set_max_ibi_data_len(65536)
    fresh_data = [0x11, 0x22, 0x33]
    await send_ibi(tb, 0xBB, fresh_data)
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, 0xBB, fresh_data)
    await check_ibi_status(tb, 0, "fresh after partial")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 3: Refuse IBI — retry sweep (0..7)
# =============================================================================

async def _test_ibi_refuse_retry(dut, retry_num):
    """
    Sec 5.1.6.2 item 2: Refuse IBI sweep over all retry_num values.
    Counts exact bus-level attempts via handle_ibi_manual.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb, retry_num=retry_num)

    mdb = 0xAA
    data = [0xBE, 0xEF]
    await send_ibi(tb, mdb, data)

    attempts = 0

    if retry_num == 7:
        # Infinite retries: NACK >8 times to prove unbounded, then ACK
        for _ in range(9):
            result = await with_timeout(
                i3c_controller.handle_ibi_manual(ack=False), 20, "us",
            )
            attempts += 1
            assert result["ack"] is False
            assert result["addr"] == TARGET_ADDRESS

        # Accept the IBI to finish cleanly
        result = await with_timeout(
            i3c_controller.handle_ibi_manual(ack=True), 20, "us",
        )
        assert result["ack"] is True
        await verify_ibi_response(
            dut, bytearray([result["addr"]]) + result["data"],
            TARGET_ADDRESS, mdb, data,
        )
        await check_ibi_status(tb, 0, "infinite retry success")

        dut._log.info(f"retry_num=7: >8 NACKs confirmed ({attempts}), then ACK")

        # CP7: Verify retry counter auto-reset on success — queue 2nd IBI
        # and confirm full retry budget is available again
        mdb2 = 0xBB
        data2 = [0xCA, 0xFE]
        await send_ibi(tb, mdb2, data2)
        for _ in range(5):
            result = await with_timeout(
                i3c_controller.handle_ibi_manual(ack=False), 20, "us",
            )
            assert result["ack"] is False
        result = await with_timeout(
            i3c_controller.handle_ibi_manual(ack=True), 20, "us",
        )
        assert result["ack"] is True
        await check_ibi_status(tb, 0, "2nd IBI success after counter reset")
    else:
        # Finite retries: expect exactly retry_num + 1 attempts
        while True:
            try:
                result = await with_timeout(
                    i3c_controller.handle_ibi_manual(ack=False),
                    20 if attempts == 0 else 3, "us",
                )
                attempts += 1
                assert result["ack"] is False
                assert result["addr"] == TARGET_ADDRESS
            except SimTimeoutError:
                # handle_ibi_manual called take_bus_control before timeout;
                # release it so the monitor can resume.
                i3c_controller.give_bus_control()
                break

        expected = retry_num + 1
        assert attempts == expected, (
            f"retry_num={retry_num}: expected {expected} bus attempts, got {attempts}"
        )
        await check_ibi_status(tb, 3, f"retry exhausted (retry_num={retry_num})")

        dut._log.info(f"retry_num={retry_num}: {attempts} attempts confirmed")

    await ClockCycles(tb.clk, 10)


# Use TestFactory to parameterize over all retry values
tf_retry = TestFactory(_test_ibi_refuse_retry)
tf_retry.add_option("retry_num", list(range(8)))
tf_retry.generate_tests(prefix="test_ibi_refuse_retry_sweep_")


# =============================================================================
# Test 4: Refuse — no retry on Repeated Start
# =============================================================================

@cocotb.test()
async def test_ibi_refuse_no_retry_on_rstart(dut):
    """
    Sec 5.1.6.2: After NACK, target retries on Bus Available/Start but NOT
    on Repeated Start. Verify WaitRestart->RxFByte (not RxFByteArb).
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # NACK the first IBI attempt
    i3c_controller.enable_ibi(False)

    mdb = 0xAA
    data = [0x11, 0x22]
    await send_ibi(tb, mdb, data)

    # Wait for NACK
    await Timer(3, "us")
    await check_ibi_status(tb, 1, "initial NACK")

    # Controller issues Sr->Private Write->P — target must NOT arbitrate IBI here
    # The Private Write uses Sr (repeated start), not a fresh Start
    await i3c_controller.i3c_write(TARGET_ADDRESS, [0xDE, 0xAD])
    await ClockCycles(tb.clk, 50)

    # Re-enable IBI ACK and wait for bus available retry
    i3c_controller.enable_ibi(True)

    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "retry after bus available")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 5: Refuse and disable interrupts (DISEC)
# =============================================================================

@cocotb.test()
async def test_ibi_refuse_and_disable(dut):
    """
    Sec 5.1.6.2 item 3: Refuse IBI, then disable interrupts via DISEC CCC.
    Target must NOT retry until ENEC re-enables.
    Uses handle_ibi_manual to NACK + Sr->broadcast DISEC in one frame,
    preventing the DUT from re-arbitrating IBI on a separate Start.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    mdb = 0xAA
    data = [0xCA, 0xFE]
    await send_ibi(tb, mdb, data)

    # NACK the IBI and immediately issue Sr->broadcast DISEC in the same frame.
    # Broadcast DISEC (0x07) sends: Sr->7E+W->CCC->data->STOP
    result = await i3c_controller.handle_ibi_manual(
        ack=False,
        ccc=CCC.BCAST.DISEC,
        ccc_data=[0x01],
        ccc_addr=None,
    )
    assert result["ack"] is False

    await ClockCycles(tb.clk, 50)

    # Verify IBI_EN is now 0
    ibi_en = await tb.read_csr_field(
        tb.reg_map.I3C_EC.TTI.CONTROL.base_addr,
        tb.reg_map.I3C_EC.TTI.CONTROL.IBI_EN,
    )
    assert ibi_en == 0, f"IBI_EN should be 0 after DISEC, got {ibi_en}"

    # Wait — target should NOT retry
    await expect_no_ibi(i3c_controller, 10)

    # Re-enable via broadcast ENEC CCC and allow controller to ACK
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.BCAST.ENEC,
        broadcast_data=[0x01],
    )
    i3c_controller.enable_ibi(True)

    # Target should now retry
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "success after ENEC")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 6: Accept IBI, then Sr->CCC
# =============================================================================

@cocotb.test()
async def test_ibi_accept_then_ccc(dut):
    """
    Sec 5.1.6.2 item 1: After accepting IBI and reading data, controller
    issues Sr->CCC. Verify CCC executes correctly.
    Also CP22: Verify PENDING_INTERRUPT reflects ibi_pending_o.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # CP22: PENDING_INTERRUPT should be 0 before queueing IBI
    await check_pending_interrupt(tb, 0)

    mdb = 0xAA
    data = [0x11, 0x22]
    await send_ibi(tb, mdb, data)

    # CP22: PENDING_INTERRUPT should be set while IBI is pending
    await ClockCycles(tb.clk, 5)
    await check_pending_interrupt(tb, 1)

    # Manual IBI handling: ACK + read data + Sr->CCC(GETSTATUS)
    result = await i3c_controller.handle_ibi_manual(
        ack=True,
        ccc=CCC.DIRECT.GETSTATUS,
        ccc_data=[0x00, 0x00],
        ccc_addr=TARGET_ADDRESS,
    )

    # Verify IBI data received correctly
    expected_data = bytearray([mdb] + data)
    assert result["data"] == expected_data, (
        f"IBI data mismatch: expected {expected_data.hex()}, got {result['data'].hex()}"
    )
    assert result["addr"] == TARGET_ADDRESS

    # CCC response should exist (GETSTATUS returns 2 bytes)
    assert result["ccc_response"] is not None, "CCC response missing after Sr->CCC"
    dut._log.info(f"GETSTATUS response: {result['ccc_response'].hex()}")

    # CP22: Parse GETSTATUS response — PENDING_INTERRUPT should have cleared
    getstatus = int.from_bytes(result["ccc_response"], byteorder="big", signed=False)
    pending_from_getstatus = getstatus & 0xF
    dut._log.info(f"GETSTATUS PENDING_INTERRUPT={pending_from_getstatus}")

    await check_ibi_status(tb, 0, "accept then CCC")

    # CP22: CSR PENDING_INTERRUPT should also be 0 after IBI completes
    await ClockCycles(tb.clk, 10)
    await check_pending_interrupt(tb, 0)


# =============================================================================
# Test 7: Refuse IBI, then Sr->CCC
# =============================================================================

@cocotb.test()
async def test_ibi_refuse_then_ccc(dut):
    """
    Sec 5.1.6.2 item 2: After NACKing IBI, controller issues Sr->CCC.
    Target must NOT attempt IBI during the Sr->CCC frame.
    After STOP + bus available, target retries IBI.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    mdb = 0xAA
    data = [0x33, 0x44]
    await send_ibi(tb, mdb, data)

    # NACK the IBI + issue Sr->CCC(GETSTATUS)
    result = await i3c_controller.handle_ibi_manual(
        ack=False,
        ccc=CCC.DIRECT.GETSTATUS,
        ccc_data=[0x00, 0x00],
        ccc_addr=TARGET_ADDRESS,
    )

    assert result["ack"] is False

    # CCC should still work after NACK'd IBI
    assert result["ccc_response"] is not None, "CCC failed after NACK'd IBI"
    dut._log.info(f"GETSTATUS response after NACK: {result['ccc_response'].hex()}")

    # After STOP + bus available, target retries IBI
    i3c_controller.enable_ibi(True)
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "retry after NACK+CCC")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 8: IBI initiation — Bus Available vs Bus Start
# =============================================================================

@cocotb.test()
async def test_ibi_initiation_bus_available_vs_start(dut):
    """
    Sec 5.1.6.2: Target initiates IBI via Bus Available Condition (1us)
    or during Bus Start within Bus Free (38.4ns).
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # --- Subtest A: Bus Available initiation ---
    # Queue IBI and let bus sit idle for >1us
    mdb_a = 0xA1
    data_a = [0x01]
    await send_ibi(tb, mdb_a, data_a)

    # Target should initiate IBI via bus available condition
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb_a, data_a)
    await check_ibi_status(tb, 0, "bus available initiation")

    await ClockCycles(tb.clk, 50)

    # --- Subtest B: Bus Start initiation ---
    # Queue IBI, then immediately issue a controller Start (before Bus Available).
    # DUT enters RxFByteArb on this Start and drives its IBI address.
    # It loses arbitration on the RnW bit (DUT=1 vs controller=0) but
    # exercises the Bus Start initiation path (Idle → RxFByteArb).
    # After the write's STOP + Bus Available, DUT retries via IbiDriveAddr.
    mdb_b = 0xB2
    data_b = [0x02]
    await send_ibi(tb, mdb_b, data_b)

    # Bare Start → TARGET_ADDRESS+W: DUT arbitrates, loses on RnW bit
    await i3c_controller.i3c_write(TARGET_ADDRESS, [0x00], send_rsvd=False)

    # DUT retries after Bus Available (ibi_inhibit clears)
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb_b, data_b)
    await check_ibi_status(tb, 0, "bus start initiation")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 9: Pending Read Notification (MDB IGI=3'b101)
# =============================================================================

async def _test_ibi_pending_read_notification(dut, read_len, ibi_extra_bytes=0):
    """
    Sec 5.1.6.2.2: IBI with Pending Read Notification MDB (IGI=101),
    followed by Private Read to consume data.
    Spec L83: Target may include additional IBI payload bytes beyond MDB.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # MDB with IGI=3'b101 (bits [7:5]) — Pending Read Notification
    mdb = 0b10100000 | random.randint(0, 0x1F)
    # Spec L83: additional payload bytes provide context for the pending read
    extra_data = [random.randint(0, 255) for _ in range(ibi_extra_bytes)]
    await send_ibi(tb, mdb, extra_data)

    response = await i3c_controller.wait_for_ibi()
    # Verify MDB received
    assert response[1] == mdb, f"MDB mismatch: expected 0x{mdb:02X}, got 0x{response[1]:02X}"
    # Verify additional IBI payload bytes if present
    if ibi_extra_bytes > 0:
        assert list(response[2:]) == extra_data, (
            f"IBI extra bytes mismatch: expected {extra_data}, got {list(response[2:])}"
        )
    await check_ibi_status(tb, 0, "PRN IBI success")

    await ClockCycles(tb.clk, 50)

    if read_len > 0:
        # Prepare TX data for the Private Read
        tx_data = [random.randint(0, 255) for _ in range(read_len)]
        for i in range(0, len(tx_data), 4):
            chunk = tx_data[i:i + 4]
            word = 0
            for j, b in enumerate(chunk):
                word |= b << (8 * j)
            await tb.write_csr(
                tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr,
                int2dword(word), 4,
            )
        await tb.write_csr(
            tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr,
            int2dword(read_len), 4,
        )

    # Controller reads the pending data
    read_response = await i3c_controller.i3c_read(TARGET_ADDRESS, max(read_len, 1))

    if read_len > 0:
        assert not read_response.nack, "Private Read was NACKed"
        assert list(read_response.data[:read_len]) == tx_data, (
            f"Private Read data mismatch: expected {tx_data}, got {list(read_response.data[:read_len])}"
        )
    else:
        # With 0 bytes prepared, target should NACK
        assert read_response.nack, "Expected NACK for 0-byte Private Read"

    await ClockCycles(tb.clk, 10)


tf_prn = TestFactory(_test_ibi_pending_read_notification)
tf_prn.add_option("read_len", [0, 1, 4])
tf_prn.add_option("ibi_extra_bytes", [0, 3])
tf_prn.generate_tests(prefix="test_ibi_pending_read_notification_")


# =============================================================================
# Test 10: Arbitration — DUT wins (lower address)
# =============================================================================

@cocotb.test()
async def test_ibi_arbitration_dut_wins(dut):
    """
    Sec 5.1.6.1: Lower address = higher priority. Verify DUT can send IBI
    when configured with a lower address. Since the VIP target doesn't
    support arbitration backoff, we verify sequential behavior:
    DUT IBI succeeds, then VIP IBI succeeds.
    """
    DUT_ADDR = 0x10
    VIP_ADDR = 0x50

    i3c_controller, i3c_target_vip, tb = await test_setup(
        dut, static_addr=DUT_ADDR,
    )
    i3c_target_vip.address = VIP_ADDR

    await init_ibi(i3c_controller, tb, addr=DUT_ADDR)

    vip_target = i3c_controller.add_target(VIP_ADDR)
    vip_target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)

    mdb_dut = 0xAA
    dut_data = [0x11]

    # DUT sends IBI first (lower address = higher priority)
    await send_ibi(tb, mdb_dut, dut_data)
    response = await i3c_controller.wait_for_ibi()
    assert response[0] == DUT_ADDR, (
        f"Expected IBI from DUT (0x{DUT_ADDR:02X}), got 0x{response[0]:02X}"
    )
    await verify_ibi_response(dut, response, DUT_ADDR, mdb_dut, dut_data)
    await check_ibi_status(tb, 0, "DUT IBI success")

    await ClockCycles(tb.clk, 50)

    # VIP sends IBI after DUT completes
    mdb_vip = 0xBB
    cocotb.start_soon(i3c_target_vip.send_ibi(mdb=mdb_vip))
    response = await i3c_controller.wait_for_ibi()
    assert response[0] == VIP_ADDR, (
        f"Expected IBI from VIP (0x{VIP_ADDR:02X}), got 0x{response[0]:02X}"
    )

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 11: Arbitration — DUT loses, waits for Bus Available
# =============================================================================

@cocotb.test()
async def test_ibi_arbitration_dut_loses_bus_available_wait(dut):
    """
    Sec 5.1.6.2: After losing arbitration (simulated via NACK), DUT sets
    ibi_inhibit and must wait for Bus Available (1us) before retrying.
    Controller issues frame within Bus Free (38.4ns) to verify DUT
    does NOT attempt IBI prematurely.

    Note: True arbitration loss requires VIP arbitration support.
    We simulate the inhibit behavior using NACK + immediate frame.
    """
    DUT_ADDR = 0x50

    i3c_controller, _, tb = await test_setup(dut, static_addr=DUT_ADDR)
    await init_ibi(i3c_controller, tb, addr=DUT_ADDR)

    mdb_dut = 0xAA
    dut_data = [0x11]

    # NACK the DUT's IBI to simulate it being refused (as in arbitration loss)
    i3c_controller.enable_ibi(False)
    await send_ibi(tb, mdb_dut, dut_data)

    # Wait for NACK
    await Timer(3, "us")
    await check_ibi_status(tb, 1, "initial NACK")

    # Immediately issue another frame — DUT should NOT attempt IBI during this
    # frame since it needs to wait for Bus Available (ibi_inhibit equivalent)
    i3c_controller.enable_ibi(True)
    await i3c_controller.i3c_write(DUT_ADDR, [0xDE, 0xAD])
    await ClockCycles(tb.clk, 10)

    # Now wait for Bus Available (>1us) — DUT should retry
    response = await i3c_controller.wait_for_ibi()
    assert response[0] == DUT_ADDR, (
        f"DUT should retry after Bus Available, got IBI from 0x{response[0]:02X}"
    )
    await verify_ibi_response(dut, response, DUT_ADDR, mdb_dut, dut_data)
    await check_ibi_status(tb, 0, "DUT retries after bus available")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 12: Back-to-back IBIs
# =============================================================================

@cocotb.test()
async def test_ibi_back_to_back(dut):
    """
    Multiple IBIs issued sequentially. Verify each is received correctly
    with proper status and interrupt behavior.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    num_ibis = random.randint(3, 5)
    dut._log.info(f"Sending {num_ibis} back-to-back IBIs")

    for i in range(num_ibis):
        mdb = random.randint(0x00, 0xFF)
        data = [random.randint(0, 255) for _ in range(random.randint(0, 4))]

        dut._log.info(f"  IBI {i}: MDB=0x{mdb:02X}, len={len(data)}")
        await send_ibi(tb, mdb, data)
        response = await i3c_controller.wait_for_ibi()
        await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
        await check_ibi_status(tb, 0, f"back-to-back IBI {i}")

        # Verify IBI_DONE fires — reading LAST_IBI_STATUS clears it
        await ClockCycles(tb.clk, 10)
        await check_ibi_done(tb, 0)

        await ClockCycles(tb.clk, 50)

    dut._log.info(f"All {num_ibis} back-to-back IBIs passed")
    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 13: Arbitration loss on address bits (Flow 1)
# =============================================================================

@cocotb.test()
async def test_ibi_arb_loss_address(dut):
    """
    Flow 1: DUT loses IBI arbitration to a lower-address peer during the
    address phase. RTL sets ibi_inhibit — DUT must NOT retry on the next
    Start, only after Bus Available condition.
    """
    DUT_ADDR = 0x60   # Higher address → lower priority
    VIP_ADDR = 0x20   # Lower address → wins arbitration

    i3c_controller, i3c_target_vip, tb = await test_setup(
        dut, static_addr=DUT_ADDR,
    )
    i3c_target_vip.address = VIP_ADDR

    await init_ibi(i3c_controller, tb, addr=DUT_ADDR)
    vip_target = i3c_controller.add_target(VIP_ADDR)
    vip_target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)

    # Both targets initiate IBI — VIP wins (lower address on open-drain bus)
    await send_ibi(tb, 0xC1, [0x99])
    peer_task = cocotb.start_soon(
        i3c_target_vip.send_ibi(mdb=0xD1, data=bytearray([0x88]))
    )
    response = await i3c_controller.wait_for_ibi()
    await peer_task
    assert response[0] == VIP_ADDR, (
        f"Expected VIP ({VIP_ADDR:#x}) to win arbitration, got {response[0]:#x}"
    )

    # CP5: Verify intermediate IbiFailureAddressArb (4) status immediately after arb loss
    await check_ibi_status(tb, 4, "arb loss intermediate (IbiFailureAddressArb)")

    # DUT has ibi_inhibit=1 — immediate Start must NOT trigger DUT IBI
    await i3c_controller.i3c_write(VIP_ADDR, [0x5A], send_rsvd=False)

    # Verify no DUT IBI within 800ns (Bus Available = 1us)
    await expect_no_ibi(i3c_controller, 800, "ns")

    # After Bus Available the DUT retries
    response = await i3c_controller.wait_for_ibi()
    assert response[0] == DUT_ADDR
    await check_ibi_status(tb, 0, "DUT IBI success after arb loss recovery")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 14: Arbitration loss on RnW bit (Flow 2)
# =============================================================================

@cocotb.test()
async def test_ibi_arb_loss_rnw_bit(dut):
    """
    Flow 2: DUT tries IBI (addr+RnW=1) during a controller-initiated write
    to the same 7-bit address (addr+RnW=0). Address bits match on the bus;
    arbitration_lost_i fires only on bit 0 (RnW) because 0 is dominant in
    open-drain. DUT sets ibi_inhibit and falls through to process the write
    normally.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    mdb = 0xAA
    data = [0x11]
    await send_ibi(tb, mdb, data)

    # Controller writes to DUT's own address without 0x7E header.
    # DUT enters RxFByteArb and drives (TARGET_ADDRESS<<1|1);
    # controller drives (TARGET_ADDRESS<<1|0). Bits 7-1 match,
    # bit 0 differs → DUT loses on RnW.
    write_data = [0xDE, 0xAD]
    resp = await i3c_controller.i3c_write(
        TARGET_ADDRESS, write_data, send_rsvd=False,
    )
    assert not resp.nack, "DUT should ACK the write after losing RnW arbitration"

    # ibi_inhibit prevents retry on immediate Start — verify via bus_available retry
    response = await i3c_controller.wait_for_ibi()
    assert response[0] == TARGET_ADDRESS
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "IBI success after RnW arb loss recovery")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 15: NACK → Sr → Private Write (Flow 4)
# =============================================================================

@cocotb.test()
async def test_ibi_nack_sr_private_write(dut):
    """
    Flow 4: Controller NACKs IBI then chains Sr → Private Write to the
    target within the same bus frame. Target must NOT attempt IBI on
    the chained Repeated Start (WaitRestart→RxFByte, not RxFByteArb).
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    mdb = 0xAA
    data = [0x55, 0x66]
    await send_ibi(tb, mdb, data)

    # NACK IBI, then Sr → Private Write to target
    write_payload = [0xDE, 0xAD]
    result = await i3c_controller.handle_ibi_manual(
        ack=False,
        chain_write_addr=TARGET_ADDRESS,
        chain_write_data=write_payload,
    )
    assert result["ack"] is False
    assert result["chain_write_ack"], "Target should ACK the chained Private Write"

    # After STOP + bus_available, DUT retries IBI
    i3c_controller.enable_ibi(True)
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "IBI success after NACK+write chain")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 16: NACK → Sr → Directed DISEC (Flow 6)
# =============================================================================

@cocotb.test()
async def test_ibi_nack_sr_directed_disec(dut):
    """
    Flow 6: Controller NACKs IBI then chains Sr → Directed DISEC with
    DISINT to the target. Uses CCC 0x81 (directed SET) with addr+W
    direction. Verifies IBI_EN clears and target stops retrying.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    mdb = 0xAA
    data = [0xCA, 0xFE]
    await send_ibi(tb, mdb, data)

    # NACK IBI, then Sr → Directed DISEC (CCC 0x81, SET → addr+W)
    result = await i3c_controller.handle_ibi_manual(
        ack=False,
        ccc=CCC.DIRECT.DISEC,
        ccc_data=[0x01],                # DISINT byte
        ccc_addr=TARGET_ADDRESS,
    )
    assert result["ack"] is False

    await ClockCycles(tb.clk, 50)

    # Verify IBI_EN cleared by directed DISEC
    ibi_en = await tb.read_csr_field(
        tb.reg_map.I3C_EC.TTI.CONTROL.base_addr,
        tb.reg_map.I3C_EC.TTI.CONTROL.IBI_EN,
    )
    assert ibi_en == 0, f"IBI_EN should be 0 after directed DISEC, got {ibi_en}"

    # Target must NOT retry while disabled
    await expect_no_ibi(i3c_controller, 5)

    # Re-enable via broadcast ENEC and verify IBI fires
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.BCAST.ENEC, broadcast_data=[0x01],
    )
    i3c_controller.enable_ibi(True)
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "IBI success after directed ENEC re-enable")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 17: BCR[2]=0 not supported — STOP without reading MDB (Flow 7)
# =============================================================================

@cocotb.test(expect_fail=True)
async def test_ibi_accept_no_mdb_stop(dut):
    """
    Flow 7: Our target always sends MDB (BCR[2]=1). Controller ACKs but
    sends STOP without reading MDB. Target should report a non-success
    IBI status since the MDB was never consumed.

    expect_fail: RTL has no BCR[2] gating in IbiSendData — STOP during
    push-pull goes to Idle via global override without writing
    ibi_status_we. Status retains stale reset value (0=success) instead
    of reporting failure. This is a known RTL gap.
    """
    i3c_controller, _, tb = await test_setup(dut)
    target = await init_ibi(i3c_controller, tb)

    mdb = 0xBB
    data = [0x11]
    await send_ibi(tb, mdb, data)

    # ACK but refuse to read MDB — violates BCR[2]=1 contract
    result = await i3c_controller.handle_ibi_manual(
        ack=True,
        skip_ibi_data=True,
    )
    assert result["ack"] is True
    assert result["addr"] == TARGET_ADDRESS

    await ClockCycles(tb.clk, 50)

    # Target should report failure — MDB was never read
    status = await tb.read_csr_field(
        tb.reg_map.I3C_EC.TTI.STATUS.base_addr,
        tb.reg_map.I3C_EC.TTI.STATUS.LAST_IBI_STATUS,
    )
    assert status != 0, (
        f"LAST_IBI_STATUS=0 (success) but MDB was never read — "
        f"target should report a non-zero error status"
    )


# =============================================================================
# Test 18: BCR[2]=0 not supported — Sr without reading MDB (Flow 8)
# =============================================================================

@cocotb.test(expect_fail=True)
async def test_ibi_accept_no_mdb_sr_ccc(dut):
    """
    Flow 8: Our target always sends MDB (BCR[2]=1). Controller ACKs but
    sends Sr → CCC without reading MDB. Target should report a non-success
    IBI status since the MDB was never consumed.

    expect_fail: Same RTL gap as Test 17 — IbiSendData has no status
    write on early Sr termination. The orphaned IBI re-fires instead of
    reporting failure.
    """
    i3c_controller, _, tb = await test_setup(dut)
    target = await init_ibi(i3c_controller, tb)

    mdb = 0xCC
    data = [0x22]
    await send_ibi(tb, mdb, data)

    # ACK but refuse to read MDB, chain Sr → CCC instead
    result = await i3c_controller.handle_ibi_manual(
        ack=True,
        skip_ibi_data=True,
        ccc=CCC.BCAST.ENEC,
        ccc_data=[0x0B],
    )
    assert result["ack"] is True

    await ClockCycles(tb.clk, 50)

    # Target should report failure — MDB was never read
    status = await tb.read_csr_field(
        tb.reg_map.I3C_EC.TTI.STATUS.base_addr,
        tb.reg_map.I3C_EC.TTI.STATUS.LAST_IBI_STATUS,
    )
    assert status != 0, (
        f"LAST_IBI_STATUS=0 (success) but MDB was never read — "
        f"target should report a non-zero error status"
    )


# =============================================================================
# Test 19: ACK, tbit abort, Sr → CCC (Flow 12)
# =============================================================================

@cocotb.test()
async def test_ibi_tbit_abort_sr_ccc(dut):
    """
    Flow 12: Controller ACKs IBI, reads partial data (T-bit abort by
    stopping early), then chains Sr → CCC. The target should report
    IbiPartialData status and the CCC should execute correctly.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    mdb = 0xAA
    full_data = [0xCA, 0xFE, 0xBA, 0xBE, 0xDD, 0xEE]
    await send_ibi(tb, mdb, full_data)

    # ACK and read only MDB + 2 data bytes, then Sr → GETSTATUS
    result = await i3c_controller.handle_ibi_manual(
        ack=True,
        max_data_len=2,
        ccc=CCC.DIRECT.GETSTATUS,
        ccc_data=[0x00, 0x00],
        ccc_addr=TARGET_ADDRESS,
    )
    assert result["ack"] is True
    assert result["addr"] == TARGET_ADDRESS
    # Should have received MDB + 2 data bytes (truncated)
    expected_truncated = bytearray([mdb] + full_data[:2])
    assert result["data"] == expected_truncated, (
        f"Truncated IBI data mismatch: expected {expected_truncated.hex()}, "
        f"got {result['data'].hex()}"
    )

    # CCC should have executed after the truncated IBI
    assert result["ccc_response"] is not None, "GETSTATUS response missing after tbit abort + Sr"
    dut._log.info(f"GETSTATUS after tbit abort: {result['ccc_response'].hex()}")

    await ClockCycles(tb.clk, 50)
    await check_ibi_status(tb, 2, "partial data from tbit abort")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 20: IBI queued while disabled, then enabled (CP6)
# =============================================================================

@cocotb.test()
async def test_ibi_queue_while_disabled_then_enable(dut):
    """
    RTL gate: ibi_pending = ibi_byte_valid_i && ibi_enable_i (line 273).
    IBI data queued while IBI_EN=0 sits dormant in the descriptor pipeline
    until IBI_EN is set via CSR — distinct from the DISEC/ENEC CCC path
    tested in test_ibi_refuse_and_disable.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # Disable IBI via CSR before queueing
    await set_ibi_enable(tb, False)

    mdb = 0xBB
    data = [0x10, 0x20]
    await send_ibi(tb, mdb, data)

    # descriptor_ibi.sv reports pending = (state != Idle) regardless of IBI_EN;
    # data IS in the pipeline, the FSM just won't act on it until enabled.
    await ClockCycles(tb.clk, 10)
    await check_pending_interrupt(tb, 1)

    # No IBI should fire while disabled
    await expect_no_ibi(i3c_controller, 3)

    # Flip the gate — queued IBI should fire immediately
    await set_ibi_enable(tb, True)
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "IBI success after enable")

    # Pending should clear after IBI completes
    await ClockCycles(tb.clk, 10)
    await check_pending_interrupt(tb, 0)

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 21: FW-initiated IBI retry counter reset (CP6)
# =============================================================================

@cocotb.test()
async def test_ibi_retry_ctr_fw_reset(dut):
    """
    CP6: Verify IBI_RETRY_CTR_RST singlepulse resets the retry counter
    mid-sequence. Without the FW reset, 2 NACKs would exhaust retry_num=1.
    """
    i3c_controller, _, tb = await test_setup(dut)
    # retry_num=1 allows 2 attempts (cnt 0 and cnt 1)
    await init_ibi(i3c_controller, tb, retry_num=1)

    mdb = 0xDD
    data = [0xAA, 0xBB]
    await send_ibi(tb, mdb, data)

    # NACK attempt 1 → counter becomes 1
    result = await i3c_controller.handle_ibi_manual(ack=False)
    assert result["ack"] is False
    await check_ibi_status(tb, 1, "NACK #1")

    # FW resets retry counter before DUT retries
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.TTI.RESET_CONTROL.base_addr,
        tb.reg_map.I3C_EC.TTI.RESET_CONTROL.IBI_RETRY_CTR_RST,
        1,
    )

    # NACK attempt 2 → counter becomes 1 again (was reset to 0)
    result = await i3c_controller.handle_ibi_manual(ack=False)
    assert result["ack"] is False

    # Without FW reset, this would have been attempt 3 (cnt=2 > retry_num=1)
    # and DUT would have flushed. Instead DUT retries (cnt=1 ≤ 1).
    result = await i3c_controller.handle_ibi_manual(ack=True)
    assert result["ack"] is True
    await verify_ibi_response(
        dut, bytearray([result["addr"]]) + result["data"],
        TARGET_ADDRESS, mdb, data,
    )
    await check_ibi_status(tb, 0, "success after FW counter reset")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 24: Multiple consecutive arbitration losses (CP25, CP4, CP10)
# =============================================================================

@cocotb.test()
async def test_ibi_multiple_arb_losses(dut):
    """
    CP25/CP4/CP10: Force multiple consecutive arb losses to exhaust the
    retry counter via the IbiFailureAddressArb path. retry_num=2 allows
    3 attempts; 3 VIP wins should exhaust retries.
    """
    DUT_ADDR = 0x60
    VIP_ADDR = 0x20

    i3c_controller, i3c_target_vip, tb = await test_setup(
        dut, static_addr=DUT_ADDR,
    )
    i3c_target_vip.address = VIP_ADDR

    await init_ibi(i3c_controller, tb, addr=DUT_ADDR, retry_num=2)
    vip_target = i3c_controller.add_target(VIP_ADDR)
    vip_target.set_bcr_fields(ibi_req_capable=True, ibi_payload=True)

    mdb_dut = 0xEE
    dut_data = [0x77]
    await send_ibi(tb, mdb_dut, dut_data)

    # Force 3 arb losses: VIP wins each time with lower address
    for i in range(3):
        peer_task = cocotb.start_soon(
            i3c_target_vip.send_ibi(mdb=0xD0 + i, data=bytearray([0x80 + i]))
        )
        response = await i3c_controller.wait_for_ibi()
        await peer_task
        assert response[0] == VIP_ADDR, (
            f"Arb loss {i}: Expected VIP ({VIP_ADDR:#x}), got {response[0]:#x}"
        )
        # After arb loss, ibi_inhibit prevents retry until Bus Available
        # Wait for Bus Available so DUT can attempt again (or exhaust)
        await Timer(2, "us")

    # After 3 arb losses with retry_num=2, counter (3) > retry_num (2)
    # → IbiFailureRetry + flush
    await ClockCycles(tb.clk, 50)
    await check_ibi_status(tb, 3, "retry exhausted via arb losses")

    # Verify IBI data was flushed — a fresh IBI should work cleanly
    mdb_fresh = 0xFF
    fresh_data = [0x11, 0x22]
    await send_ibi(tb, mdb_fresh, fresh_data)
    response = await i3c_controller.wait_for_ibi()
    assert response[0] == DUT_ADDR
    await verify_ibi_response(dut, response, DUT_ADDR, mdb_fresh, fresh_data)
    await check_ibi_status(tb, 0, "fresh IBI after arb loss exhaustion")

    await ClockCycles(tb.clk, 10)


# =============================================================================
# Test 30: IBI queued during HDR mode fires after exit (CP24)
# =============================================================================

@cocotb.test()
async def test_ibi_queued_during_hdr_fires_after_exit(dut):
    """
    CP24: Verify IBI queued while DUT is in HDR mode fires correctly
    after the HDR exit pattern is detected and Bus Available occurs.
    """
    ENTHDR0 = 0x20

    i3c_controller, _, tb = await test_setup(dut)
    await init_ibi(i3c_controller, tb)

    # Enter HDR mode via ENTHDR0 CCC
    await i3c_controller.i3c_ccc_write(
        ccc=ENTHDR0, broadcast_data=[], stop=False, pull_scl_low=True,
    )
    await ClockCycles(tb.clk, 50)

    # Queue IBI while in HDR mode — DUT is in InHDRMode state
    mdb = 0xCC
    data = [0x33, 0x44]
    await send_ibi(tb, mdb, data)
    await ClockCycles(tb.clk, 10)

    # IBI should NOT fire while in HDR mode
    await expect_no_ibi(i3c_controller, 2)

    # Exit HDR mode
    await i3c_controller.send_hdr_exit()
    await ClockCycles(tb.clk, 50)

    # After HDR exit + Bus Available, DUT should initiate IBI
    response = await i3c_controller.wait_for_ibi()
    await verify_ibi_response(dut, response, TARGET_ADDRESS, mdb, data)
    await check_ibi_status(tb, 0, "IBI success after HDR exit")

    await ClockCycles(tb.clk, 10)
