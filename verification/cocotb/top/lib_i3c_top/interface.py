# SPDX-License-Identifier: Apache-2.0

from bus2csr import dword2int, get_frontend_bus_if, int2dword
from cocotb_helpers import reset_n
from reg_map import reg_map

import cocotb
from cocotb.handle import SimHandleBase
from cocotb.triggers import ClockCycles


class I3CTopTestInterface:

    def __init__(self, dut: SimHandleBase) -> None:
        self.dut = dut
        self.bus_if_cls = get_frontend_bus_if()
        self.reg_map = reg_map

        self.busIf = self.bus_if_cls(dut)
        self.clk = self.busIf.clk
        self.rst_n = self.busIf.rst_n
        self.read_csr = self.busIf.read_csr
        self.write_csr = self.busIf.write_csr
        self.read_csr_field = self.busIf.read_csr_field
        self.write_csr_field = self.busIf.write_csr_field

    async def setup(self, fclk=500.0):

        # Limit the requested clock frequency if a limit is set via cocotb
        # plusargs
        fmin = cocotb.plusargs.get("MinSystemClockFrequency", None)
        if fmin is not None:
            fmin = float(fmin)
            if fclk < fmin:
                self.dut._log.warning(f"Enforcing min. system clock frequency of {fmin:.3f} MHz")
                fclk = fmin

        if hasattr(self.dut, "disable_id_filtering_i"):
            self.dut.disable_id_filtering_i.value = 1

        await self.busIf.register_test_interfaces(fclk)
        await ClockCycles(self.clk, 20)
        await reset_n(self.clk, self.rst_n, cycles=5)

    async def enable_target_err_intr(self):
        """Enable all TARGET_ERR_INTR_ENABLE bits so errors are captured."""
        # Bits [13:1]: all TE0-TE5, FRAMING, RI_PEC, RI_LENGTH,
        # RI_READONLY, RI_UNSUPPORTED, RI_RX_FIFO_OVERFLOW,
        # RI_INDIRECT_FIFO_OVERFLOW
        await self.write_csr(
            self.reg_map.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.base_addr,
            int2dword(0x3FFE), 4,
        )

    async def assert_no_target_errors(self):
        """Assert PROTOCOL_ERROR, TRANSFER_ERR_STAT, and all
        TARGET_ERR_INTR_STATUS fields are zero."""
        protocol_err = await self.read_csr_field(
            self.reg_map.I3C_EC.TTI.STATUS.base_addr,
            self.reg_map.I3C_EC.TTI.STATUS.PROTOCOL_ERROR,
        )
        assert protocol_err == 0, (
            f"PROTOCOL_ERROR is set (STATUS = 0x{protocol_err:X})"
        )

        xfer_err = await self.read_csr_field(
            self.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.base_addr,
            self.reg_map.I3C_EC.TTI.INTERRUPT_STATUS.TRANSFER_ERR_STAT,
        )
        assert xfer_err == 0, "TRANSFER_ERR_STAT is set"

        tgt_err = dword2int(
            await self.read_csr(
                self.reg_map.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.base_addr, 4
            )
        )
        assert tgt_err == 0, (
            f"TARGET_ERR_INTR_STATUS is non-zero: 0x{tgt_err:04X}"
        )
