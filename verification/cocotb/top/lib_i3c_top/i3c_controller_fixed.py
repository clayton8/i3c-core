# SPDX-License-Identifier: Apache-2.0
"""
Fixed I3C Controller

This module provides extensions to the I3cController from cocotbext-i3c that add
missing parameters needed for recovery interface testing.

Additional Features:
    - Extended i3c_write with send_rsvd parameter for chaining transactions
    - Extended i3c_ccc_read/write for chaining support (future)
    - Target reset pattern stress testing methods

Usage:
    Instead of:
        from cocotbext_i3c.i3c_controller import I3cController

    Use:
        from i3c_controller_fixed import I3cControllerFixed as I3cController
"""

from typing import Iterable, Optional

from cocotbext_i3c.i3c_controller import I3cController, I3cXferMode
from cocotbext_i3c.common import I3C_RSVD_BYTE, I3cPWResp, I3cState
from cocotb.triggers import Timer



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

    # =========================================================================
    # TARGET RESET PATTERN STRESS TEST METHODS
    # =========================================================================

    async def send_target_reset_pattern_stress(
        self,
        num_transitions: int = 14,
        tdig_h_ns: Optional[float] = None,
        t_start_hold_ns: Optional[float] = None,
        t_stop_hold_ns: Optional[float] = None,
    ) -> None:
        """
        Send a target reset pattern with configurable parameters for stress testing.

        Per I3C spec (5.1.11.3):
        1. 14 SDA transitions while SCL is kept Low
        2. Repeated START
        3. STOP

        Args:
            num_transitions: Number of SDA transitions (14 for valid pattern)
            tdig_h_ns: Override timing for SDA transitions in nanoseconds.
                       If None, uses the controller's default tdig_h.
            t_start_hold_ns: Override hold time for START condition in nanoseconds.
                             If None, uses tdig_h_ns or controller default.
            t_stop_hold_ns: Override hold time for STOP condition in nanoseconds.
                            If None, uses tdig_h_ns or controller default.
        """
        await self.take_bus_control()
        self._state = I3cState.TARGET_RESET

        # Use custom timing or fall back to controller's tdig_h
        if tdig_h_ns is not None:
            wait_time = Timer(tdig_h_ns, "ns")
        else:
            wait_time = self.tdig_h

        t_start = Timer(t_start_hold_ns, "ns") if t_start_hold_ns else wait_time
        t_stop = Timer(t_stop_hold_ns, "ns") if t_stop_hold_ns else wait_time

        self.log_info(f"Sending target reset pattern with {num_transitions} SDA transitions")

        # Start with SDA high, SCL low
        sda = 1
        self.sda = sda
        self.scl = 0
        await wait_time

        # Generate SDA transitions while SCL is low
        for _ in range(num_transitions):
            sda = 0 if sda else 1
            self.sda = sda
            await wait_time

        # Raise SCL and keep it high through START and STOP
        await wait_time
        self.scl = 1
        await wait_time

        # Send Repeated START (SDA falling while SCL high)
        self.sda = 0
        await t_start

        # Send STOP (SDA rising while SCL high)
        self.sda = 1
        await t_stop

        self.log_info("Target reset pattern complete")
        self.give_bus_control()

    async def send_target_reset_pattern_with_scl_glitch(
        self,
        glitch_at_transition: int = 7,
        tdig_h_ns: Optional[float] = None,
    ) -> None:
        """
        Send target reset pattern with SCL glitch during SDA transitions.
        
        This should reset the transition counter and prevent reset detection.

        Args:
            glitch_at_transition: Which SDA transition to glitch SCL at (0-indexed)
            tdig_h_ns: Override timing in nanoseconds. If None, uses controller default.
        """
        await self.take_bus_control()
        self._state = I3cState.TARGET_RESET

        if tdig_h_ns is not None:
            wait_time = Timer(tdig_h_ns, "ns")
            half_wait = Timer(tdig_h_ns / 2, "ns")
        else:
            wait_time = self.tdig_h
            half_wait = Timer(self.timings.tdig_h / 2, "ns")

        self.log_info(f"Sending pattern with SCL glitch at transition {glitch_at_transition}")

        sda = 1
        self.sda = sda
        self.scl = 0
        await wait_time

        for i in range(14):
            sda = 0 if sda else 1
            self.sda = sda
            await wait_time

            # Inject SCL glitch
            if i == glitch_at_transition:
                self.scl = 1
                await half_wait
                self.scl = 0
                await half_wait

        # Complete pattern normally
        await wait_time
        self.scl = 1
        await wait_time

        self.sda = 0
        await wait_time

        self.sda = 1
        await wait_time

        self.give_bus_control()

    async def send_target_reset_pattern_with_sda_stable_low(
        self,
        tdig_h_ns: Optional[float] = None,
    ) -> None:
        """
        Send 14 SDA transitions, but then SDA goes stable low before SCL rises.
        
        This should cause FSM to return to AwaitPattern (abort).

        Args:
            tdig_h_ns: Override timing in nanoseconds. If None, uses controller default.
        """
        await self.take_bus_control()
        self._state = I3cState.TARGET_RESET

        if tdig_h_ns is not None:
            wait_time = Timer(tdig_h_ns, "ns")
        else:
            wait_time = self.tdig_h

        self.log_info("Sending pattern with SDA stable low during AwaitSCL")

        sda = 1
        self.sda = sda
        self.scl = 0
        await wait_time

        for _ in range(14):
            sda = 0 if sda else 1
            self.sda = sda
            await wait_time

        # SDA should be high after 14 toggles, but force it low
        self.sda = 0
        await wait_time
        await wait_time

        # Now raise SCL - but FSM should have aborted
        self.scl = 1
        await wait_time

        # Try to complete pattern anyway
        self.sda = 0
        await wait_time
        self.sda = 1
        await wait_time

        self.give_bus_control()

    async def send_target_reset_pattern_with_scl_drop_await_sr(
        self,
        tdig_h_ns: Optional[float] = None,
    ) -> None:
        """
        Send valid 14 transitions, SCL rises, but then drops before START.
        
        This tests the AwaitSr abort condition when SCL goes stable low.

        Args:
            tdig_h_ns: Override timing in nanoseconds. If None, uses controller default.
        """
        await self.take_bus_control()
        self._state = I3cState.TARGET_RESET

        if tdig_h_ns is not None:
            wait_time = Timer(tdig_h_ns, "ns")
            half_wait = Timer(tdig_h_ns / 2, "ns")
        else:
            wait_time = self.tdig_h
            half_wait = Timer(self.timings.tdig_h / 2, "ns")

        self.log_info("Sending pattern with SCL drop during AwaitSr")

        sda = 1
        self.sda = sda
        self.scl = 0
        await wait_time

        for _ in range(14):
            sda = 0 if sda else 1
            self.sda = sda
            await wait_time

        await wait_time
        self.scl = 1
        await half_wait

        # Drop SCL before START - this should abort AwaitSr
        self.scl = 0
        await wait_time

        # FSM should have aborted, attempt to complete anyway
        self.scl = 1
        await wait_time
        self.sda = 0
        await wait_time
        self.sda = 1
        await wait_time

        self.give_bus_control()

    async def send_target_reset_pattern_with_scl_drop_await_p(
        self,
        tdig_h_ns: Optional[float] = None,
        t_start_hold_ns: Optional[float] = None,
    ) -> None:
        """
        Complete valid pattern through START, but SCL drops before STOP.
        
        This tests the AwaitP abort condition when SCL goes stable low.
        NOTE: SCL must drop BEFORE SDA rises, because STOP is detected on SDA rising edge.

        Args:
            tdig_h_ns: Override timing in nanoseconds. If None, uses controller default.
            t_start_hold_ns: Override START hold time. If None, uses tdig_h_ns or default.
        """
        await self.take_bus_control()
        self._state = I3cState.TARGET_RESET

        if tdig_h_ns is not None:
            wait_time = Timer(tdig_h_ns, "ns")
        else:
            wait_time = self.tdig_h

        t_start = Timer(t_start_hold_ns, "ns") if t_start_hold_ns else wait_time

        self.log_info("Sending pattern with SCL drop during AwaitP")

        sda = 1
        self.sda = sda
        self.scl = 0
        await wait_time

        for _ in range(14):
            sda = 0 if sda else 1
            self.sda = sda
            await wait_time

        await wait_time
        self.scl = 1
        await wait_time

        # Valid START - SDA falls while SCL high
        self.sda = 0
        await t_start

        # Now in AwaitP, drop SCL BEFORE raising SDA
        self.scl = 0
        await wait_time

        # Now raise SDA (but SCL is low, so no STOP detected)
        self.sda = 1
        await wait_time

        # Return to idle
        self.scl = 1
        await wait_time

        self.give_bus_control()

    async def set_bus_idle(self) -> None:
        """
        Set bus to idle state (both SDA and SCL high).
        
        Useful for initializing bus state before stress tests.
        """
        self.sda = 1
        self.scl = 1
        await self.tdig_h

    async def recv_addr_ack(self) -> bool:
        self.scl = 0
        self.sda = 1
        # We don't hold the data here, because it's on the target to pull it down
        # after the required amount of time
        await self.tdig_l
        if self.sda_i is None:
            b = False
        else:
            b = bool(self.sda)
        
        # Take over driving in case of an ACK by target
        if b == False:
            self.sda = 0
        self.scl = 1
        await self.tdig_h
        self.hold_data = False

        return b

    async def send_byte(self, b: int, addr: bool = False) -> bool:
        self._state = I3cState.ADDR if addr else I3cState.DATA_WR
        for i in range(8):
            await self.send_bit(b & (1 << 7 - i))
        self._state = I3cState.ACK
        if addr and not(b & 1):
            return await self.recv_addr_ack()
        else:
            return await self.recv_bit_od()
