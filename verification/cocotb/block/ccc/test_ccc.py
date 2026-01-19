# SPDX-License-Identifier: Apache-2.0

import random

from ccc import CCC
from cocotb_helpers import cycle, reset_n

import cocotb
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.triggers import ClockCycles, RisingEdge, with_timeout

_STATUS = 0xC64B


def initialize_inputs(dut):
    dut.ccc_data_i.value = 0
    dut.ccc_valid_i.value = 0
    dut.bus_start_det_i.value = 0
    dut.bus_rstart_det_i.value = 0
    dut.bus_stop_det_i.value = 0
    dut.arbitration_lost_i.value = 0
    dut.te0_err_i.value = 0
    
    # Bus TX response (struct: {error, idle, done})
    dut.bus_tx_rsp_i.error.value = 0
    dut.bus_tx_rsp_i.idle.value = 0
    dut.bus_tx_rsp_i.done.value = 0
    
    # Bus RX response (struct: {idle, done, data[7:0]})
    dut.bus_rx_rsp_i.idle.value = 0
    dut.bus_rx_rsp_i.done.value = 0
    dut.bus_rx_rsp_i.data.value = 0
    
    dut.target_sta_address_i.value = 0
    dut.target_sta_address_valid_i.value = 0
    dut.target_dyn_address_i.value = 0
    dut.target_dyn_address_valid_i.value = 0
    dut.virtual_target_sta_address_i.value = 0
    dut.virtual_target_sta_address_valid_i.value = 0
    dut.virtual_target_dyn_address_i.value = 0
    dut.virtual_target_dyn_address_valid_i.value = 0
    dut.get_mwl_i.value = 0
    dut.get_mrl_i.value = 0
    dut.get_ibil_i.value = 0
    dut.get_pid_i.value = 0
    dut.get_bcr_i.value = 0
    dut.get_dcr_i.value = 0
    dut.virtual_get_pid_i.value = 0
    dut.virtual_get_bcr_i.value = 0
    dut.virtual_get_dcr_i.value = 0
    dut.get_status_fmt1_i.value = 0
    dut.get_acccr_i.value = 0
    dut.get_mxds_i.value = 0
    dut.target_reset_detect_i.value = 0
    dut.peripheral_reset_done_i.value = 0
    dut.exit_hdr_i.value = 0


async def setup(dut):
    """
    Initialize inputs of the DUT
    """
    dut.get_mwl_i.value = random.randint(0, 2**16 - 1)
    dut.get_mrl_i.value = random.randint(0, 2**16 - 1)
    dut.get_pid_i.value = random.randint(0, 2**48 - 1)
    dut.get_bcr_i.value = random.randint(0, 2**8 - 1)
    dut.get_dcr_i.value = random.randint(0, 2**8 - 1)
    dut.get_status_fmt1_i.value = _STATUS

    dut.target_sta_address_i.value = 0x2D
    dut.target_sta_address_valid_i.value = 1
    dut.target_dyn_address_i.value = 0x2D  # Use same as static for matching
    dut.target_dyn_address_valid_i.value = 1

    await ClockCycles(dut.clk_i, 10)


async def rx_bit(dut, value):
    """
    Send bit on the RX interface
    bus_rx_rsp_t = {idle, done, data[7:0]}
    """
    # Wait for req_bit to go high
    while not dut.bus_rx_req_o.req_bit.value:
        await RisingEdge(dut.clk_i)
    await ClockCycles(dut.clk_i, 3)
    dut.bus_rx_rsp_i.data.value = value & 0xFF
    dut.bus_rx_rsp_i.done.value = 1
    await ClockCycles(dut.clk_i, 1)
    dut.bus_rx_rsp_i.done.value = 0


async def rx_byte(dut, value):
    """
    Send byte on the RX interface
    bus_rx_rsp_t = {idle, done, data[7:0]}
    """
    # Wait for req_byte to go high
    while not dut.bus_rx_req_o.req_byte.value:
        await RisingEdge(dut.clk_i)
    await ClockCycles(dut.clk_i, 3)
    dut.bus_rx_rsp_i.data.value = value & 0xFF
    dut.bus_rx_rsp_i.done.value = 1
    await ClockCycles(dut.clk_i, 1)
    dut.bus_rx_rsp_i.done.value = 0


async def tx_bit(dut):
    """
    bus_tx_rsp_t = {error, idle, done}
    bus_tx_req_t = {drive_type, req_byte, req_bit, data[7:0]}
    """
    # Wait for req_bit to go high
    while not dut.bus_tx_req_o.req_bit.value:
        await RisingEdge(dut.clk_i)
    val = int(dut.bus_tx_req_o.data.value)  # Get the data from the request
    await ClockCycles(dut.clk_i, 3)
    dut.bus_tx_rsp_i.done.value = 1
    await ClockCycles(dut.clk_i, 1)
    dut.bus_tx_rsp_i.done.value = 0
    return val & 0xFF


async def tx_byte(dut):
    """
    bus_tx_rsp_t = {error, idle, done}
    bus_tx_req_t = {drive_type, req_byte, req_bit, data[7:0]}
    """
    # Wait for req_byte to go high
    while not dut.bus_tx_req_o.req_byte.value:
        await RisingEdge(dut.clk_i)
    val = int(dut.bus_tx_req_o.data.value)  # Get the data from the request
    await ClockCycles(dut.clk_i, 10)
    dut.bus_tx_rsp_i.done.value = 1
    await ClockCycles(dut.clk_i, 1)
    dut.bus_tx_rsp_i.done.value = 0
    return val & 0xFF


async def get_status(dut):
    # CCC - set command code and valid
    await ClockCycles(dut.clk_i, 7)
    dut.ccc_data_i.value = CCC.DIRECT.GETSTATUS
    await cycle(dut.clk_i, dut.ccc_valid_i)

    # T-bit (odd parity of command code)
    cmd_parity = bin(CCC.DIRECT.GETSTATUS).count('1') % 2
    tbit_value = 1 - cmd_parity  # Odd parity: if odd 1s, T=0; if even 1s, T=1
    await rx_bit(dut, tbit_value)

    # RS
    await ClockCycles(dut.clk_i, 5)
    await cycle(dut.clk_i, dut.bus_rstart_det_i)

    # Target Address (0x2D with R bit = 0x5B for read)
    await rx_byte(dut, 0x5B)

    # ACK
    await tx_bit(dut)

    # TX Bytes (GETSTATUS returns 2 bytes)
    status = []
    for i in range(2):
        byte_val = await tx_byte(dut)
        status.append(byte_val)
        # T-bit
        await tx_bit(dut)

    # Stop the frame
    await cycle(dut.clk_i, dut.bus_stop_det_i)
    await ClockCycles(dut.clk_i, 5)

    return status


@cocotb.test()
async def test_ccc(dut: SimHandleBase):
    """
    Test CCC
    """
    cocotb.log.setLevel("INFO")
    clk = dut.clk_i
    rst_n = dut.rst_ni

    clock = Clock(clk, 2, units="ns")
    cocotb.start_soon(clock.start())

    initialize_inputs(dut)
    await setup(dut)
    await reset_n(clk, rst_n, cycles=5)

    status = await with_timeout(get_status(dut), 200, "ns")
    _status = (int(status[0]) << 8) | int(status[1])
    print(f"Test returned {hex(_status)}, expected {hex(_STATUS)}")
    assert _status == _STATUS
