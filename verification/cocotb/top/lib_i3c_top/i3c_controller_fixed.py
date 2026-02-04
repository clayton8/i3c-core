# SPDX-License-Identifier: Apache-2.0
"""
Fixed I3C Controller

This module provides extensions to the I3cController from cocotbext-i3c that add
missing parameters needed for recovery interface testing.

Additional Features:
    - Extended i3c_write with send_rsvd parameter for chaining transactions
    - Extended i3c_ccc_read/write for chaining support (future)

Usage:
    Instead of:
        from cocotbext_i3c.i3c_controller import I3cController

    Use:
        from i3c_controller_fixed import I3cControllerFixed as I3cController
"""

from typing import Iterable

from cocotbext_i3c.i3c_controller import I3cController, I3cXferMode
from cocotbext_i3c.common import I3C_RSVD_BYTE, I3cPWResp


class I3cControllerFixed(I3cController):
    """
    Extended I3cController with additional parameters for chaining and testing.
    """

    async def i3c_write(
        self,
        addr: int,
        data: Iterable[int],
        stop: bool = True,
        mode: I3cXferMode = I3cXferMode.PRIVATE,
        inject_tbit_err: bool = False,
        send_rsvd: bool = True,
    ) -> I3cPWResp:
        """
        I3C Private Write transfer with optional reserved byte skipping.

        Extended from the base class to add send_rsvd parameter for chaining
        transactions without sending the 0x7E reserved byte header each time.

        Args:
            addr: Target I3C address
            data: Data bytes to write
            stop: If True (default), send STOP at end; if False, leave bus active
            mode: Transfer mode (PRIVATE or LEGACY_I2C)
            inject_tbit_err: If True, inject T-bit (parity) error
            send_rsvd: If True (default), send S + 0x7E + Sr before address;
                       if False, just send S + address (for chaining after another transfer)

        Returns:
            I3cPWResp with nack status and sent count
        """
        await self.take_bus_control()
        self.log_info(f"I3C: Write data ({mode.name}) {data} @ {hex(addr)}")

        if send_rsvd:
            await self.send_start()
            await self.write_addr_header(I3C_RSVD_BYTE)
            await self.send_start()
        else:
            await self.send_start()

        ack = await self.write_addr_header(addr)
        if ack:
            for i, d in enumerate(data):
                match mode:
                    case I3cXferMode.PRIVATE:
                        await self.send_byte_tbit(d, inject_tbit_err)
                    case I3cXferMode.LEGACY_I2C:
                        await self.send_byte(d)
                self.log_info(f"I3C: wrote byte {hex(d)}, idx={i}")

        if stop:
            await self.send_stop()

        self.give_bus_control()
        return I3cPWResp(not ack, len(data))

    async def i3c_write_chained(
        self,
        addr: int,
        data: Iterable[int],
        stop: bool = True,
        start: bool = True,
        mode: I3cXferMode = I3cXferMode.PRIVATE,
        inject_tbit_err: bool = False,
    ) -> I3cPWResp:
        """
        I3C Private Write with full chaining control.

        This method provides complete control over START and STOP for chaining
        multiple transactions together.

        Args:
            addr: Target I3C address
            data: Data bytes to write
            stop: If True (default), send STOP at end; if False, leave bus active
            start: If True (default), take bus control and send START;
                   if False, assume we already have bus control
            mode: Transfer mode (PRIVATE or LEGACY_I2C)
            inject_tbit_err: If True, inject T-bit (parity) error

        Returns:
            I3cPWResp with nack status and sent count
        """
        if start:
            await self.take_bus_control()
            self.log_info(f"I3C: Write data ({mode.name}) {data} @ {hex(addr)}")
            await self.send_start()
            await self.write_addr_header(I3C_RSVD_BYTE)

        await self.send_start()
        ack = await self.write_addr_header(addr)
        if ack:
            for i, d in enumerate(data):
                match mode:
                    case I3cXferMode.PRIVATE:
                        await self.send_byte_tbit(d, inject_tbit_err)
                    case I3cXferMode.LEGACY_I2C:
                        await self.send_byte(d)
                self.log_info(f"I3C: wrote byte {hex(d)}, idx={i}")

        if stop:
            await self.send_stop()
            self.give_bus_control()

        return I3cPWResp(not ack, len(data))

    async def i3c_stop(self):
        """
        Convenience method to send a STOP condition and release bus control.

        This is useful for cleaning up after a transaction that was left
        without a STOP (e.g., after a NACK or for testing purposes).
        """
        await self.send_stop()
        self.give_bus_control()
