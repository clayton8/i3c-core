# SPDX-License-Identifier: Apache-2.0

import logging
import random

from boot import boot_init
from bus2csr import bytes2int, dword2int, int2dword
from ccc import CCC
from cocotbext_i3c.common import I3cTargetResetAction
from i3c_controller_fixed import I3cControllerFixed as I3cController
from i3c_recovery_interface_fixed import I3cRecoveryInterfaceFixed as I3cRecoveryInterface
from interface import I3CTopTestInterface

import cocotb
from cocotb.triggers import ClockCycles
from cocotb.regression import TestFactory

TGT_ADR = 0x5A

VALID_I3C_ADDRESSES = (
    [i for i in range(0x03, 0x3E)]
    + [i for i in range(0x3F, 0x5E)]
    + [i for i in range(0x5F, 0x6E)]
    + [i for i in range(0x6F, 0x76)]
    + [i for i in range(0x77, 0x7A)]
    + [0x7B, 0x7D]
)

async def test_setup(dut, static_addr=0x5A, virtual_static_addr=0x5B, dynamic_addr=None, virtual_dynamic_addr=None):
    """
    Sets up controller, target models and top-level core interface
    """
    cocotb.log.setLevel(logging.DEBUG)

    i3c_controller = I3cController(
        sda_i=dut.bus_sda,
        sda_o=dut.sda_sim_ctrl_i,
        scl_i=dut.bus_scl,
        scl_o=dut.scl_sim_ctrl_i,
        debug_state_o=None,
        speed=12.5e6,
    )

    # We don't need target BFM in this test
    dut.sda_sim_target_i = 1
    dut.scl_sim_target_i = 1
    i3c_target = None

    dut.peripheral_reset_done_i.value = 0

    tb = I3CTopTestInterface(dut)
    await tb.setup()
    await ClockCycles(tb.clk, 50)
    await boot_init(tb, static_addr=static_addr, virtual_static_addr=virtual_static_addr,
                    dynamic_addr=dynamic_addr, virtual_dynamic_addr=virtual_dynamic_addr)
    return i3c_controller, i3c_target, tb


@cocotb.test()
async def test_ccc_getstatus(dut):
    """
    Verifies directed GETSTATUS CCC returns correct PENDING_INTERRUPT
    field for the main target and fixed activity-mode status for the
    virtual target, using randomized addresses.
    """
    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(VALID_I3C_ADDRESSES, 4)
    # Once dynamic address is assigned, static address can no longer be used
    ADDRs = [DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR]

    i3c_controller, i3c_target, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR,
        dynamic_addr=DYNAMIC_ADDR, virtual_dynamic_addr=VIRT_DYNAMIC_ADDR)
    await ClockCycles(tb.clk, 50)

    for _ in range(random.randint(10, 30)):
        PENDING_INTERRUPT = random.randint(0, 15)
        PENDING_INTERRUPT_MASK = 0b1111

        interrupt_status_reg_addr = tb.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.base_addr
        pending_interrupt_field = tb.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.PENDING_INTERRUPT

        await tb.write_csr_field(interrupt_status_reg_addr, pending_interrupt_field, PENDING_INTERRUPT)
        pending_interrupt = await tb.read_csr_field(interrupt_status_reg_addr, pending_interrupt_field)
        assert (
            pending_interrupt == PENDING_INTERRUPT
        ), "Unexpected pending interrupt value read from CSR"

        addr = random.choice([DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR])
        responses = await i3c_controller.i3c_ccc_read(ccc=CCC.DIRECT.GETSTATUS, addr=addr, count=2)
        status = int.from_bytes(responses[0][1], byteorder="big", signed=False)
        print("status", status)
        if addr == DYNAMIC_ADDR:
            # Main target: check pending interrupt field
            pending_interrupt = status & PENDING_INTERRUPT_MASK
            assert (
                pending_interrupt == PENDING_INTERRUPT
            ), f"Unexpected pending interrupt value received from GETSTATUS CCC, expected: {PENDING_INTERRUPT} got: {pending_interrupt}"
        else:
            # Virtual target: Activity Mode=3, no pending interrupts
            assert (status == 0x00C0), f"Unexpected value received from GETSTATUS CCC, expected: 0xC0 got: {status}"
        cocotb.log.info(f"GET STATUS = {status}")


@cocotb.test()
async def test_ccc_setdasa(dut):
    """
    Assigns dynamic addresses to main and virtual targets via directed
    SETDASA, interleaving commands to unrelated addresses, then verifies
    the addresses and valid flags are set in CSRs.
    """
    list_of_values = VALID_I3C_ADDRESSES.copy()

    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(list_of_values, 4)

    # remove our addresses from list of allowed addresses
    list_of_values.remove(STATIC_ADDR)
    list_of_values.remove(VIRT_STATIC_ADDR)
    list_of_values.remove(DYNAMIC_ADDR)
    list_of_values.remove(VIRT_DYNAMIC_ADDR)

    i3c_controller, i3c_target, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR)
    await ClockCycles(tb.clk, 50)
    # send number of transaction to address other than our
    for _ in range(random.randint(1, 3)):
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(random.choice(list_of_values), [random.choice(list_of_values) << 1])], stop=False
        )
    if random.choice([True, False]):
        # send regular device dynamic address along with addresses for other random devices (those should be ignored)
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(random.choice(list_of_values), [random.choice(list_of_values) << 1]), (STATIC_ADDR, [DYNAMIC_ADDR << 1]), (random.choice(list_of_values), [random.choice(list_of_values) << 1])], stop=False
        )
    else:
        # send regular device dynamic address
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(STATIC_ADDR, [DYNAMIC_ADDR << 1])], stop=False
        )
    # send number of transaction to address other than our
    for _ in range(random.randint(1, 3)):
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(random.choice(list_of_values), [random.choice(list_of_values) << 1])], stop=False
        )
    if random.choice([True, False]):
        # send virtual device dynamic address along with addresses for other random devices (those should be ignored)
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(random.choice(list_of_values), [random.choice(list_of_values) << 1]), (VIRT_STATIC_ADDR, [VIRT_DYNAMIC_ADDR << 1]), (random.choice(list_of_values), [random.choice(list_of_values) << 1])], stop=False
        )
    else:
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(VIRT_STATIC_ADDR, [VIRT_DYNAMIC_ADDR << 1])]
        )
    # send number of transaction to address other than our
    for _ in range(random.randint(1, 3)):
        await i3c_controller.i3c_ccc_write(
            ccc=CCC.DIRECT.SETDASA, directed_data=[(random.choice(list_of_values), [random.choice(list_of_values) << 1])], stop=False
        )
    dynamic_address_reg_addr = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.base_addr
    dynamic_address_reg_value = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR
    virtual_dynamic_address_reg_addr = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.base_addr
    )
    virtual_dynamic_address_reg_value = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR
    )
    dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID
    )
    virtual_dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID
    )
    dynamic_address = await tb.read_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value)
    dynamic_address_valid = await tb.read_csr_field(
        dynamic_address_reg_addr, dynamic_address_reg_valid
    )
    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )
    assert dynamic_address == DYNAMIC_ADDR, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert dynamic_address_valid == 1, "New DYNAMIC ADDRESS is not set as valid"

    assert (
        virt_dynamic_address == VIRT_DYNAMIC_ADDR
    ), "Unexpected VIRT DYNAMIC ADDRESS read from the CSR"
    assert virt_dynamic_address_valid == 1, "New VIRT DYNAMIC ADDRESS is not set as valid"


@cocotb.test()
async def test_ccc_setdasa_nack(dut):
    """
    Verifies a second SETDASA to a target that already has a dynamic
    address is NACKed.
    """
    list_of_values = VALID_I3C_ADDRESSES.copy()

    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(list_of_values, 4)

    # remove our addresses from list of allowed addresses
    list_of_values.remove(STATIC_ADDR)
    list_of_values.remove(VIRT_STATIC_ADDR)
    list_of_values.remove(DYNAMIC_ADDR)
    list_of_values.remove(VIRT_DYNAMIC_ADDR)

    i3c_controller, i3c_target, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR)
    # set regular device dynamic address
    ack = await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(STATIC_ADDR, [DYNAMIC_ADDR << 1])], stop=False
    )
    # check ACK
    assert ack[0] == True

    # try to send SETDASA again (should be NACKed)
    ack = await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(STATIC_ADDR, [DYNAMIC_ADDR << 1])], stop=False
    )
    assert ack[0] == False

    # set virtual device dynamic address
    ack = await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(VIRT_STATIC_ADDR, [VIRT_DYNAMIC_ADDR << 1])]
    )
    # check ACK
    assert ack[0] == True

    # try to send SETDASA again (should be NACKed)
    ack = await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(VIRT_STATIC_ADDR, [VIRT_DYNAMIC_ADDR << 1])]
    )
    assert ack[0] == False


@cocotb.test()
async def test_ccc_setnewda(dut):
    """
    Pre-assigns dynamic addresses via CSR, then changes them with
    directed SETNEWDA and verifies the new values in CSRs.
    """
    list_of_values = VALID_I3C_ADDRESSES.copy()

    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR, NEW_DYNAMIC_ADDR, NEW_VIRT_DYNAMIC_ADDR) = random.sample(list_of_values, 6)

    # remove our addresses from list of allowed addresses
    list_of_values.remove(STATIC_ADDR)
    list_of_values.remove(VIRT_STATIC_ADDR)
    list_of_values.remove(DYNAMIC_ADDR)
    list_of_values.remove(VIRT_DYNAMIC_ADDR)
    list_of_values.remove(NEW_DYNAMIC_ADDR)
    list_of_values.remove(NEW_VIRT_DYNAMIC_ADDR)

    i3c_controller, i3c_target, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR)
    await ClockCycles(tb.clk, 50)

    dynamic_address_reg_addr = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.base_addr
    dynamic_address_reg_value = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR
    virtual_dynamic_address_reg_addr = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.base_addr
    )
    virtual_dynamic_address_reg_value = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR
    )
    dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID
    )
    virtual_dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID
    )

    # set dynamic addresses
    await tb.write_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value, DYNAMIC_ADDR)
    await tb.write_csr_field(dynamic_address_reg_addr, dynamic_address_reg_valid, 1)
    await tb.write_csr_field(virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value, VIRT_DYNAMIC_ADDR)
    await tb.write_csr_field(virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid, 1)

    # change regular device dynamic address
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETNEWDA, directed_data=[(DYNAMIC_ADDR, [NEW_DYNAMIC_ADDR << 1])], stop=False
    )
    # change virtual device dynamic address
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETNEWDA, directed_data=[(VIRT_DYNAMIC_ADDR, [NEW_VIRT_DYNAMIC_ADDR << 1])]
    )

    # read addresses
    dynamic_address = await tb.read_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value)
    dynamic_address_valid = await tb.read_csr_field(
        dynamic_address_reg_addr, dynamic_address_reg_valid
    )
    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )

    assert dynamic_address == NEW_DYNAMIC_ADDR, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert dynamic_address_valid == 1, "New DYNAMIC ADDRESS is not set as valid"

    assert (
        virt_dynamic_address == NEW_VIRT_DYNAMIC_ADDR
    ), "Unexpected VIRT DYNAMIC ADDRESS read from the CSR"
    assert virt_dynamic_address_valid == 1, "New VIRT DYNAMIC ADDRESS is not set as valid"

@cocotb.test()
async def test_ccc_rstdaa(dut):
    """
    Pre-assigns dynamic addresses via CSR, sends broadcast RSTDAA, and
    verifies addresses and valid flags are cleared.
    """
    DYNAMIC_ADDR = 0x52
    VIRT_DYNAMIC_ADDR = 0x53
    i3c_controller, i3c_target, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)
    dynamic_address_reg_addr = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.base_addr
    dynamic_address_reg_value = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR
    dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID
    )
    virtual_dynamic_address_reg_addr = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.base_addr
    )
    virtual_dynamic_address_reg_value = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR
    )
    virtual_dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID
    )

    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )

    # set dynamic address CSR
    await tb.write_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value, DYNAMIC_ADDR)
    await tb.write_csr_field(dynamic_address_reg_addr, dynamic_address_reg_valid, 1)
    # set virt dynamic address CSR
    await tb.write_csr_field(virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value, VIRT_DYNAMIC_ADDR)
    await tb.write_csr_field(virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid, 1)

    # check if write was successful
    dynamic_address = await tb.read_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value)
    dynamic_address_valid = await tb.read_csr_field(
        dynamic_address_reg_addr, dynamic_address_reg_valid
    )

    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )

    assert dynamic_address == DYNAMIC_ADDR, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert dynamic_address_valid == 1, "New DYNAMIC ADDRESS is not set as valid"

    assert (
        virt_dynamic_address == VIRT_DYNAMIC_ADDR
    ), "Unexpected VIRT DYNAMIC ADDRESS read from the CSR"
    assert virt_dynamic_address_valid == 1, "New VIRT DYNAMIC ADDRESS is not set as valid"

    # reset Dynamic Address
    await i3c_controller.i3c_ccc_write(ccc=CCC.BCAST.RSTDAA)

    # check if the address was reset
    dynamic_address = await tb.read_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value)
    dynamic_address_valid = await tb.read_csr_field(
        dynamic_address_reg_addr, dynamic_address_reg_valid
    )

    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )

    assert dynamic_address == 0, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert dynamic_address_valid == 0, "New DYNAMIC ADDRESS is not set as valid"
    assert virt_dynamic_address == 0, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert virt_dynamic_address_valid == 0, "New DYNAMIC ADDRESS is not set as valid"

@cocotb.test()
async def test_ccc_getbcr(dut):
    """
    Sets random BCR variable bits in CSRs and verifies directed GETBCR
    returns the correct combined (fixed | variable) value.
    """
    _BCR_FIXED = 0b001  # CSR reset value
    _BCR_VARs = [random.randint(0, 31), random.randint(0, 31)]
    command = CCC.DIRECT.GETBCR

    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(VALID_I3C_ADDRESSES, 4)
    ADDRs = [random.choice([STATIC_ADDR, DYNAMIC_ADDR]), random.choice([VIRT_STATIC_ADDR, VIRT_DYNAMIC_ADDR])]

    i3c_controller, _, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR,
        dynamic_addr=ADDRs[0] if ADDRs[0] == DYNAMIC_ADDR else None,
        virtual_dynamic_addr=ADDRs[1] if ADDRs[1] == VIRT_DYNAMIC_ADDR else None)
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.BCR_VAR,
        _BCR_VARs[0],
    )
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR.BCR_VAR,
        _BCR_VARs[1],
    )
    await ClockCycles(tb.clk, 50)

    for _tgt_adr, _bcr_var in zip(ADDRs, _BCR_VARs):
        responses = await i3c_controller.i3c_ccc_read(ccc=command, addr=_tgt_adr, count=1)
        bcr = responses[0][1]
        bcr_value = int.from_bytes(bcr, byteorder="big", signed=False)
        _BCR_VALUE = (_BCR_FIXED << 5) | _bcr_var
        assert _BCR_VALUE == bcr_value


@cocotb.test()
async def test_ccc_getdcr(dut):
    """
    Sets random DCR values in CSRs and verifies directed GETDCR returns
    the correct values for both targets.
    """
    _DCR_VARs = [random.randint(0, 255), random.randint(0, 255)]
    command = CCC.DIRECT.GETDCR

    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(VALID_I3C_ADDRESSES, 4)
    ADDRs = [random.choice([STATIC_ADDR, DYNAMIC_ADDR]), random.choice([VIRT_STATIC_ADDR, VIRT_DYNAMIC_ADDR])]

    i3c_controller, _, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR,
        dynamic_addr=ADDRs[0] if ADDRs[0] == DYNAMIC_ADDR else None,
        virtual_dynamic_addr=ADDRs[1] if ADDRs[1] == VIRT_DYNAMIC_ADDR else None)
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.DCR,
        _DCR_VARs[0],
    )
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR.DCR,
        _DCR_VARs[1],
    )
    await ClockCycles(tb.clk, 50)

    for _tgt_adr, _dcr_value in zip(ADDRs, _DCR_VARs):
        responses = await i3c_controller.i3c_ccc_read(ccc=command, addr=_tgt_adr, count=1)
        dcr = responses[0][1]
        dcr_value = int.from_bytes(dcr, byteorder="big", signed=False)
        assert _dcr_value == dcr_value


@cocotb.test()
async def test_ccc_getmwl(dut):
    """
    Verifies directed GETMWL returns the expected Max Write Length
    derived from the TX/RX queue size.
    """
    _TXRX_QUEUE_SIZE = 2 ** (5 + 1)  # Dwords
    _MWL_VALUE = 4 * _TXRX_QUEUE_SIZE  # Bytes

    command = CCC.DIRECT.GETMWL

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    responses = await i3c_controller.i3c_ccc_read(ccc=command, addr=TGT_ADR, count=2)
    [mwl_msb, mwl_lsb] = responses[0][1]

    mwl = (mwl_msb << 8) | mwl_lsb
    assert mwl == _MWL_VALUE


@cocotb.test()
async def test_ccc_getmrl(dut):
    """
    Verifies directed GETMRL returns the expected Max Read Length and
    IBI payload size.
    """
    _TXRX_QUEUE_SIZE = 2 ** (5 + 1)  # Dwords
    _MRL_VALUE = 4 * _TXRX_QUEUE_SIZE  # Bytes
    _IBI_PAYLOAD_SIZE = 255  # Bytes
    command = CCC.DIRECT.GETMRL

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    responses = await i3c_controller.i3c_ccc_read(ccc=command, addr=TGT_ADR, count=3)
    [mrl_msb, mrl_lsb, ibi_payload_size] = responses[0][1]

    mrl = (mrl_msb << 8) | mrl_lsb
    assert mrl == _MRL_VALUE
    assert ibi_payload_size == _IBI_PAYLOAD_SIZE


@cocotb.test()
async def test_ccc_setaasa(dut):
    """
    Sends broadcast SETAASA and verifies both targets' dynamic addresses
    are set to their static addresses.
    """
    STATIC_ADDR = 0x5A
    VIRT_STATIC_ADDR = 0x5B
    I3C_BCAST_SETAASA = 0x29
    i3c_controller, i3c_target, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)
    dynamic_address_reg_addr = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.base_addr
    dynamic_address_reg_value = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR
    dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID
    )
    virtual_dynamic_address_reg_addr = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.base_addr
    )
    virtual_dynamic_address_reg_value = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR
    )
    virtual_dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID
    )


    # reset Dynamic Address
    await i3c_controller.i3c_ccc_write(ccc=I3C_BCAST_SETAASA)

    # check if the address was reset
    dynamic_address = await tb.read_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value)
    dynamic_address_valid = await tb.read_csr_field(
        dynamic_address_reg_addr, dynamic_address_reg_valid
    )
    assert dynamic_address == STATIC_ADDR, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert dynamic_address_valid == 1, "New DYNAMIC ADDRESS is not set as valid"
    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )
    assert virt_dynamic_address == VIRT_STATIC_ADDR, "Unexpected VIRT DYNAMIC ADDRESS read from the CSR"
    assert virt_dynamic_address_valid == 1, "New VIRT DYNAMIC ADDRESS is not set as valid"


@cocotb.test()
async def test_ccc_setaasa_ignore(dut):
    """
    Verifies broadcast SETAASA is ignored when targets already have
    dynamic addresses assigned via SETDASA.
    """
    STATIC_ADDR = 0x5A
    VIRT_STATIC_ADDR = 0x5B
    DYNAMIC_ADDR = 0x3A
    VIRT_DYNAMIC_ADDR = 0x3B
    I3C_BCAST_SETAASA = 0x29

    i3c_controller, i3c_target, tb = await test_setup(dut)
    dynamic_address_reg_addr = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.base_addr
    dynamic_address_reg_value = tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR
    dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID
    )
    virtual_dynamic_address_reg_addr = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.base_addr
    )
    virtual_dynamic_address_reg_value = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR
    )
    virtual_dynamic_address_reg_valid = (
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID
    )
    # set dynamic address CSRs
    await tb.write_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value, DYNAMIC_ADDR)
    await tb.write_csr_field(dynamic_address_reg_addr, dynamic_address_reg_valid, 1)
    await tb.write_csr_field(virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value, VIRT_DYNAMIC_ADDR)
    await tb.write_csr_field(virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid, 1)

    # Send SETAASA
    await i3c_controller.i3c_ccc_write(ccc=I3C_BCAST_SETAASA)

    # check if the address was not changed
    dynamic_address = await tb.read_csr_field(dynamic_address_reg_addr, dynamic_address_reg_value)
    dynamic_address_valid = await tb.read_csr_field(
        dynamic_address_reg_addr, dynamic_address_reg_valid
    )
    assert dynamic_address == DYNAMIC_ADDR, "Unexpected DYNAMIC ADDRESS read from the CSR"
    assert dynamic_address_valid == 1, "New DYNAMIC ADDRESS is not set as valid"

    virt_dynamic_address = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_value
    )
    virt_dynamic_address_valid = await tb.read_csr_field(
        virtual_dynamic_address_reg_addr, virtual_dynamic_address_reg_valid
    )
    assert virt_dynamic_address == VIRT_DYNAMIC_ADDR, "Unexpected VIRT DYNAMIC ADDRESS read from the CSR"
    assert virt_dynamic_address_valid == 1, "New VIRT DYNAMIC ADDRESS is not set as valid"


@cocotb.test()
async def test_ccc_getpid(dut):
    """
    Configures PID_HI/PID_LO in CSRs and verifies directed GETPID
    returns the correct 6-byte PID for both targets.
    """
    _PID_HIs = [random.randint(0, 32767), random.randint(0, 32767)]
    _PID_LOs = [random.randint(0, (2**32)-1), random.randint(0, (2**32)-1)]
    command = CCC.DIRECT.GETPID

    (STATIC_ADDR, VIRT_STATIC_ADDR, DYNAMIC_ADDR, VIRT_DYNAMIC_ADDR) = random.sample(VALID_I3C_ADDRESSES, 4)
    ADDRs = [random.choice([STATIC_ADDR, DYNAMIC_ADDR]), random.choice([VIRT_STATIC_ADDR, VIRT_DYNAMIC_ADDR])]

    i3c_controller, _, tb = await test_setup(dut, STATIC_ADDR, VIRT_STATIC_ADDR,
        dynamic_addr=ADDRs[0] if ADDRs[0] == DYNAMIC_ADDR else None,
        virtual_dynamic_addr=ADDRs[1] if ADDRs[1] == VIRT_DYNAMIC_ADDR else None)
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.PID_HI,
        _PID_HIs[0],
    )
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_PID_LO.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_PID_LO.PID_LO,
        _PID_LOs[0],
    )
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR.PID_HI,
        _PID_HIs[1],
    )
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_PID_LO.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_PID_LO.PID_LO,
        _PID_LOs[1],
    )
    await ClockCycles(tb.clk, 50)

    for _tgt_adr, _pid_lo, _pid_hi in zip(ADDRs, _PID_LOs, _PID_HIs):
        responses = await i3c_controller.i3c_ccc_read(ccc=command, addr=_tgt_adr, count=6)
        pid = responses[0][1]
        pid_hi = int.from_bytes(pid[0:2], byteorder="big", signed=False)
        pid_lo = int.from_bytes(pid[2:6], byteorder="big", signed=False)

        # PID_HI has bit 0 always stuck at 0
        # Test can only setup 15 upper bits
        assert pid_hi == _pid_hi * 2
        assert pid_lo == _pid_lo


async def read_target_events(tb):

    reg = tb.reg_map.I3C_EC.TTI.CONTROL.base_addr
    ibi_en_field = tb.reg_map.I3C_EC.TTI.CONTROL.IBI_EN
    crr_en_field = tb.reg_map.I3C_EC.TTI.CONTROL.CRR_EN
    hj_en_field = tb.reg_map.I3C_EC.TTI.CONTROL.HJ_EN

    ibi_en = await tb.read_csr_field(reg, ibi_en_field)
    crr_en = await tb.read_csr_field(reg, crr_en_field)
    hj_en = await tb.read_csr_field(reg, hj_en_field)

    return (ibi_en, crr_en, hj_en)


@cocotb.test()
async def test_ccc_enec_disec_direct(dut):
    """
    Verifies directed DISEC clears and directed ENEC restores IBI, CRR,
    and HJ event enable bits.
    """
    command_enec = CCC.DIRECT.ENEC
    command_disec = CCC.DIRECT.DISEC

    _EVENT_TOGGLE_BYTE = 0b00001011

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Read default values
    event_en = await read_target_events(tb)
    assert event_en == (1, 0, 1)

    # Disable all target events
    await i3c_controller.i3c_ccc_write(
        ccc=command_disec, directed_data=[(TGT_ADR, [_EVENT_TOGGLE_BYTE])]
    )

    # Read disabled values
    event_en = await read_target_events(tb)
    assert event_en == (0, 0, 0)

    # Enable all target events
    await i3c_controller.i3c_ccc_write(
        ccc=command_enec, directed_data=[(TGT_ADR, [_EVENT_TOGGLE_BYTE])]
    )

    # Read enabled values
    event_en = await read_target_events(tb)
    assert event_en == (1, 1, 1)


@cocotb.test()
async def test_ccc_enec_disec_bcast(dut):
    """
    Verifies broadcast DISEC clears and broadcast ENEC restores IBI,
    CRR, and HJ event enable bits.
    """
    command_enec = CCC.BCAST.ENEC
    command_disec = CCC.BCAST.DISEC

    _EVENT_TOGGLE_BYTE = 0b00001011

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Read default values
    event_en = await read_target_events(tb)
    assert event_en == (1, 0, 1)

    # Disable all target events
    await i3c_controller.i3c_ccc_write(ccc=command_disec, broadcast_data=[_EVENT_TOGGLE_BYTE])

    # Read disabled values
    event_en = await read_target_events(tb)
    assert event_en == (0, 0, 0)

    # Enable all target events
    await i3c_controller.i3c_ccc_write(ccc=command_enec, broadcast_data=[_EVENT_TOGGLE_BYTE])

    # Read enabled values
    event_en = await read_target_events(tb)
    assert event_en == (1, 1, 1)


@cocotb.test()
async def test_ccc_setmwl_direct(dut):
    """
    Sends directed SETMWL and verifies the MWL output signal matches.
    """
    command = CCC.DIRECT.SETMWL

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Send direct SETMWL
    mwl_msb = 0xAB
    mwl_lsb = 0xCD
    await i3c_controller.i3c_ccc_write(ccc=command, directed_data=[(TGT_ADR, [mwl_msb, mwl_lsb])])

    # Check if MWL got written
    sig = dut.xi3c_wrapper.i3c.xcontroller.xconfiguration.get_mwl_o.value
    mwl = (mwl_msb << 8) | mwl_lsb
    assert mwl == int(sig)


@cocotb.test()
async def test_ccc_setmrl_direct(dut):
    """
    Sends directed SETMRL and verifies the MRL output signal matches.
    """
    command = CCC.DIRECT.SETMRL

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Send direct SETMRL
    mrl_msb = 0xAB
    mrl_lsb = 0xCD
    await i3c_controller.i3c_ccc_write(ccc=command, directed_data=[(TGT_ADR, [mrl_msb, mrl_lsb])])

    # Check if MRL got written
    sig = dut.xi3c_wrapper.i3c.xcontroller.xconfiguration.get_mrl_o.value
    mrl = (mrl_msb << 8) | mrl_lsb
    assert mrl == int(sig)


@cocotb.test()
async def test_ccc_setmwl_bcast(dut):
    """
    Sends broadcast SETMWL and verifies the MWL output signal matches.
    """

    command = CCC.BCAST.SETMWL

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Send broadcast SETMWL
    mwl_msb = 0xAB
    mwl_lsb = 0xCD
    await i3c_controller.i3c_ccc_write(ccc=command, broadcast_data=[mwl_msb, mwl_lsb])

    # Check if MWL got written
    sig = dut.xi3c_wrapper.i3c.xcontroller.xconfiguration.get_mwl_o.value
    mwl = (mwl_msb << 8) | mwl_lsb
    assert mwl == int(sig)


@cocotb.test()
async def test_ccc_setmrl_bcast(dut):
    """
    Sends broadcast SETMRL and verifies the MRL output signal matches.
    """

    command = CCC.BCAST.SETMRL

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Send broadcast SETMRL
    mrl_msb = 0xAB
    mrl_lsb = 0xCD
    await i3c_controller.i3c_ccc_write(ccc=command, broadcast_data=[mrl_msb, mrl_lsb])

    # Check if MRL got written
    sig = dut.xi3c_wrapper.i3c.xcontroller.xconfiguration.get_mrl_o.value
    mrl = (mrl_msb << 8) | mrl_lsb
    assert mrl == int(sig)


SUPPORTED_RESET_ACTIONS = [
    I3cTargetResetAction.NO_RESET,
    I3cTargetResetAction.RESET_PERIPHERAL_ONLY,
    I3cTargetResetAction.RESET_WHOLE_TARGET,
]
async def test_ccc_rstact(dut, type, rstact):
    """
    Verifies RSTACT CCC (broadcast and directed) stores the correct
    reset action and triggers the target reset pattern output.
    """
    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    if type == "broadcast":
        command = CCC.BCAST.RSTACT
        directed_data = None
        reset_actions = rstact
    elif type == "direct":
        command = CCC.DIRECT.RSTACT
        directed_data = [(TGT_ADR, [])]
        reset_actions = [(TGT_ADR, rstact)]
    else:
        assert False, "Unsupported RSTACT type, must be 'broadcast' or 'direct'"

    # Send RSTACT with the reset action as defining byte (0x00-0x02 are valid action values)
    rst_action = int(rstact)
    await i3c_controller.i3c_ccc_write(
        ccc=command,
        defining_byte=rst_action,
        directed_data=directed_data,
        stop=False,
    )

    # Check if reset action got stored correctly in the logic after Target Reset Pattern
    sig = dut.xi3c_wrapper.i3c.xcontroller.xcontroller_standby.xcontroller_standby_i3c.rst_action_o
    assert int(sig) == 0
    await i3c_controller.send_target_reset_pattern()
    assert rst_action == int(sig), f"Expected rst_action_o={rst_action}, got {int(sig)}"
    await i3c_controller.send_stop()

    # Start new frame and reset target with reset action set to peripheral reset
    await i3c_controller.target_reset(reset_actions)
    if rstact == I3cTargetResetAction.NO_RESET:
        assert dut.peripheral_reset_o == 0
        assert dut.escalated_reset_o == 0
    elif rstact == I3cTargetResetAction.RESET_PERIPHERAL_ONLY:
        assert dut.peripheral_reset_o == 1
        assert dut.escalated_reset_o == 0
    elif rstact == I3cTargetResetAction.RESET_WHOLE_TARGET:
        assert dut.peripheral_reset_o == 0
        assert dut.escalated_reset_o == 1
    else:
        assert False, f"Unsupported reset action ({rstact}), must be one of {SUPPORTED_RESET_ACTIONS}"
    await ClockCycles(tb.clk, 50)

rstact_tf = TestFactory(test_function=test_ccc_rstact)
rstact_tf.add_option(name="rstact", optionlist=SUPPORTED_RESET_ACTIONS)
rstact_tf.add_option(name="type", optionlist=["broadcast", "direct"])
rstact_tf.generate_tests()


@cocotb.test()
async def test_ccc_direct_multiple_wr(dut):
    """
    Send a sequence of multiple directed SETMWL CCCs. The first and last have
    non-matching address. The two middle ones set MWL to different values.
    Verify that the target responded to correct addresses and executed both
    CCCs.
    """

    command = CCC.DIRECT.SETMWL
    result = True

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    cccs = [
        (TGT_ADR - 1, (0x00, 0xA0)),
        (TGT_ADR, (0x00, 0xA1)),
        (TGT_ADR, (0x00, 0xA2)),
        (TGT_ADR + 2, (0x00, 0xA3)),  # TGT_ADR + 1 is set as virtual target static address
    ]

    # Send CCCs
    acks = await i3c_controller.i3c_ccc_write(ccc=command, directed_data=cccs)

    # Check if correct address was ACK-ed
    if acks != [False, True, True, False]:
        dut._log.error(f"Incorrect multiple directed CCC ACKs: {acks}")
        result = False

    # Check if MWL got written
    sig = dut.xi3c_wrapper.i3c.xcontroller.xconfiguration.get_mwl_o.value
    mwl = 0xA2
    if mwl != int(sig):
        dut._log.error(f"Written MWL mismatch ({mwl} vs. {int(sig)})")
        result = False

    assert result


@cocotb.test()
async def test_ccc_direct_multiple_rd(dut):
    """
    Send SETMWL CCC. Then send multiple directed GETMWL CCCs to three different
    addresses. Only the one for the target should contain ACK with correct
    MWL content.
    """

    result = True

    i3c_controller, _, tb = await test_setup(dut)
    await ClockCycles(tb.clk, 50)

    # Set MWL in the target
    acks = await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETMWL, directed_data=[(TGT_ADR, (0x00, 0x55))]
    )
    if acks != [True]:
        dut._log.error("Initial SETMWL failed")
        assert False

    await ClockCycles(tb.clk, 50)

    # Issue multiple directed GETMWL
    addrs = [TGT_ADR - 1, TGT_ADR, TGT_ADR, TGT_ADR + 2]
    responses = await i3c_controller.i3c_ccc_read(ccc=CCC.DIRECT.GETMWL, addr=addrs, count=2)

    # Check ACKs
    acks = [r[0] for r in responses]
    if acks != [False, True, True, False]:
        dut._log.error(f"Incorrect multiple directed CCC ACKs: {acks}")
        result = False

    # Check received MWL data
    for i, ack in enumerate(acks):
        if ack:
            data = responses[i][1]
            mwl = data[1] | (data[0] << 8)
            if mwl != 0x55:
                dut._log.error(f"Written and received MWL mismatch ({mwl} vs. 0x55) for CCC #{i}")
                result = False

    assert result


@cocotb.test()
async def test_ccc_read_tbit_abort_and_chain(dut):
    """
    Verifies the I3C T-bit abort mechanism during a directed CCC read
    (GETPID, 6-byte response), followed by chained transactions without
    releasing the bus.

    Uses GETPID as the aborted CCC since it returns 6 bytes, providing
    meaningful abort points at bytes 1 (first), 3 (middle), and 5
    (second-to-last).

    Parts 1-3:   CCC GETPID abort → RI read (DEVICE_ID)
    Parts 4-6:   CCC GETPID abort → CCC GETSTATUS read
    Parts 7-9:   CCC GETPID abort → Private read
    Parts 10-12: CCC GETPID abort → RI write (RECOVERY_CTRL)
    Parts 13-15: CCC GETPID abort → CCC SETMWL write
    Parts 16-18: CCC GETPID abort → Private write
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

    await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(STATIC_ADDR, [DYNAMIC_ADDR << 1])]
    )
    await i3c_controller.i3c_ccc_write(
        ccc=CCC.DIRECT.SETDASA, directed_data=[(VIRT_STATIC_ADDR, [VIRT_DYNAMIC_ADDR << 1])]
    )

    def make_word(bs):
        return (bs[3] << 24) | (bs[2] << 16) | (bs[1] << 8) | bs[0]

    # Configure PID with known non-zero values
    pid_hi = random.randint(1, 32767)
    pid_lo = random.randint(1, (2**32) - 1)

    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_CHAR.PID_HI,
        pid_hi,
    )
    await tb.write_csr_field(
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_PID_LO.base_addr,
        tb.reg_map.I3C_EC.STDBYCTRLMODE.STBY_CR_DEVICE_PID_LO.PID_LO,
        pid_lo,
    )
    await ClockCycles(tb.clk, 50)

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

    # Baseline GETPID read to get expected data
    responses = await i3c_controller.i3c_ccc_read(
        ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR, count=6
    )
    expected_pid = list(responses[0][1])
    assert len(expected_pid) == 6, f"Unexpected GETPID length: {len(expected_pid)}"
    assert any(b != 0 for b in expected_pid), "GETPID returned all zeros"
    dut._log.info(f"Baseline GETPID: {[f'0x{b:02X}' for b in expected_pid]}")

    # Baseline DEVICE_ID read
    expected_dev_id, pec_ok = await recovery.command_read(
        VIRT_DYNAMIC_ADDR, I3cRecoveryInterface.Command.DEVICE_ID
    )
    assert pec_ok, "Baseline DEVICE_ID read failed"
    dut._log.info(f"Baseline DEVICE_ID: {len(expected_dev_id)} bytes")

    # Abort at first, middle, and second-to-last PID bytes
    abort_configs = [
        (1, "PID byte 1 (first)"),
        (3, "PID byte 3 (middle)"),
        (5, "PID byte 5 (second-to-last)"),
    ]

    # =========================================================================
    # Parts 1-3: CCC GETPID abort → RI read (DEVICE_ID)
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=1):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort CCC GETPID after {desc}, chain into RI DEVICE_ID read")

        abort_bytes = await i3c_controller.i3c_ccc_read_abort(
            ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        for idx in range(abort_count):
            assert abort_bytes[idx] == expected_pid[idx], (
                f"Part {part_num}: PID byte {idx} mismatch: got 0x{abort_bytes[idx]:02X}, "
                f"expected 0x{expected_pid[idx]:02X}"
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
    # Parts 4-6: CCC GETPID abort → CCC GETSTATUS read
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=4):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort CCC GETPID after {desc}, chain into CCC GETSTATUS")

        abort_bytes = await i3c_controller.i3c_ccc_read_abort(
            ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        for idx in range(abort_count):
            assert abort_bytes[idx] == expected_pid[idx], (
                f"Part {part_num}: PID byte {idx} mismatch"
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
    # Parts 7-9: CCC GETPID abort → Private read
    # =========================================================================
    priv_read_data = [random.randint(0, 255) for _ in range(4)]

    for part_num, (abort_count, desc) in enumerate(abort_configs, start=7):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort CCC GETPID after {desc}, chain into private read")

        # Queue TX data for private read
        await tb.write_csr(
            tb.reg_map.I3C_EC.TTI.TX_DATA_PORT.base_addr,
            int2dword(int.from_bytes(priv_read_data, byteorder="little")), 4,
        )
        await tb.write_csr(
            tb.reg_map.I3C_EC.TTI.TX_DESC_QUEUE_PORT.base_addr,
            int2dword(len(priv_read_data)), 4,
        )

        abort_bytes = await i3c_controller.i3c_ccc_read_abort(
            ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR,
            abort_after_bytes=abort_count, stop=False,
        )

        assert len(abort_bytes) == abort_count, (
            f"Part {part_num}: Expected {abort_count} bytes, got {len(abort_bytes)}"
        )
        dut._log.info(f"  Aborted {abort_count} byte(s)")

        readback = await i3c_controller.i3c_read_chained(DYNAMIC_ADDR, len(priv_read_data))

        assert list(readback.data) == priv_read_data, (
            f"Part {part_num}: Private read mismatch:\n"
            f"  got:      {[f'0x{b:02X}' for b in readback.data]}\n"
            f"  expected: {[f'0x{b:02X}' for b in priv_read_data]}"
        )
        dut._log.info(f"  Private read OK: {[f'0x{b:02X}' for b in readback.data]}")

    # =========================================================================
    # Parts 10-12: CCC GETPID abort → RI write (RECOVERY_CTRL)
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=10):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort CCC GETPID after {desc}, chain into RI write")

        write_val = (part_num & 0xFF)
        ri_write_data = [write_val, write_val ^ 0xFF, write_val + 1]

        abort_bytes = await i3c_controller.i3c_ccc_read_abort(
            ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR,
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
    # Parts 13-15: CCC GETPID abort → CCC SETMWL write
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=13):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort CCC GETPID after {desc}, chain into CCC SETMWL")

        mwl_val = 64 + part_num
        mwl_bytes = [mwl_val & 0xFF, (mwl_val >> 8) & 0xFF]

        abort_bytes = await i3c_controller.i3c_ccc_read_abort(
            ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR,
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
    # Parts 16-18: CCC GETPID abort → Private write
    # =========================================================================
    for part_num, (abort_count, desc) in enumerate(abort_configs, start=16):
        dut._log.info("")
        dut._log.info(f"Part {part_num}: Abort CCC GETPID after {desc}, chain into private write")

        priv_write_data = [part_num & 0xFF, 0xCA, 0xFE, 0x00 | part_num]

        abort_bytes = await i3c_controller.i3c_ccc_read_abort(
            ccc=CCC.DIRECT.GETPID, addr=DYNAMIC_ADDR,
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
