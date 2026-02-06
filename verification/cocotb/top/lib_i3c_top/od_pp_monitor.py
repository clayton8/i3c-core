# SPDX-License-Identifier: Apache-2.0
"""
OD/PP (Open Drain / Push Pull) Mode Monitor for I3C Core

This module provides continuous monitoring of the I3C Core's SDA output enable
(sda_oe) and drive mode (sel_od_pp) signals to ensure they are correctly driven
according to the I3C specification.

I3C Protocol Rules for OD/PP:
- Open Drain (OD) mode: Used during address phases, ACK/NACK, and by targets
- Push-Pull (PP) mode: Used by targets during data transmission to controller

Truth table for sda_oe:
    sel_od_pp | sda_o  || sda_oe | IO state
    ----------+--------++--------+-----------
         0    |   0    ||   1    |    0      (OD driving low)
         0    |   1    ||   0    |   hi-z    (OD releasing to high)
         1    |   0    ||   1    |    0      (PP driving low)
         1    |   1    ||   1    |    1      (PP driving high)

Write ACK Handoff Protocol (I3C Spec Section 5.1.2.1):
When Address Header results in ACK and Message is SDR Write from Controller,
the SDA line transitions from Open Drain to Push-Pull as follows:

1. I3C Target holds SDA Low during ACK (while SCL is Low) - Open Drain
2. After Target sees rising edge of SCL, it releases SDA to High-Z
   - Target releases using normal (Push-Pull) timing (release as soon as SCL rises)
3. After rising edge of SCL, I3C Controller drives SDA Low
   - Both Controller and Target drive SDA Low briefly (safe overlap)
4. On falling edge of SCL, Controller begins driving data on SDA using Push-Pull
"""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Edge, Timer, First
from enum import Enum, auto


class OdPpMonitor:
    """
    Monitor for I3C Core's OD/PP mode signals.
    
    Continuously monitors sel_od_pp_o and sda_oe signals to verify correct
    behavior according to the I3C specification.
    """
    
    def __init__(self, dut, log=None):
        """
        Initialize the OD/PP monitor.
        
        Args:
            dut: The DUT handle (i3c_test_wrapper)
            log: Optional logger. If None, uses dut._log
        """
        self.dut = dut
        self.log = log or dut._log
        self._running = False
        self._task = None
        
        # Statistics
        self.stats = {
            'od_mode_samples': 0,
            'pp_mode_samples': 0,
            'sda_oe_high_samples': 0,
            'sda_oe_low_samples': 0,
            'violations': [],
        }
        
        # Try to get the signals - they may be at different hierarchy levels
        self._resolve_signals()
        
    def _resolve_signals(self):
        """Resolve the signal paths in the DUT hierarchy."""
        # The signals in i3c_test_wrapper are:
        # - i3c_sel_od_pp (from xi3c_wrapper.sel_od_pp_o)
        # - i3c_sda_oe (from xi3c_wrapper.sda_oe)
        # - i3c_sda_o (from xi3c_wrapper.sda_o)
        # - bus_sda, bus_scl (the resolved bus values)
        
        try:
            # Try the test wrapper's internal signals first
            self.sel_od_pp = self.dut.i3c_sel_od_pp
            self.sda_oe = self.dut.i3c_sda_oe
            self.sda_o = self.dut.i3c_sda_o
            self.bus_sda = self.dut.bus_sda
            self.bus_scl = self.dut.bus_scl
            
            # Get clock
            if hasattr(self.dut, 'aclk'):
                self.clk = self.dut.aclk
            elif hasattr(self.dut, 'hclk'):
                self.clk = self.dut.hclk
            else:
                self.clk = None
                
            self.log.info("OdPpMonitor: Successfully resolved signals at test wrapper level")
            
        except AttributeError as e:
            self.log.warning(f"OdPpMonitor: Could not resolve signals: {e}")
            self.log.warning("OdPpMonitor: Monitoring will be disabled")
            self.sel_od_pp = None
            self.sda_oe = None
            self.sda_o = None
            
    def is_available(self):
        """Check if the monitor signals are available."""
        return self.sel_od_pp is not None and self.sda_oe is not None
        
    async def start(self):
        """Start the background monitoring task."""
        if not self.is_available():
            self.log.warning("OdPpMonitor: Cannot start - signals not available")
            return
            
        if self._running:
            self.log.warning("OdPpMonitor: Already running")
            return
            
        self._running = True
        self._task = cocotb.start_soon(self._monitor_loop())
        self.log.info("OdPpMonitor: Started monitoring sel_od_pp and sda_oe signals")
        
    def stop(self):
        """Stop the background monitoring task."""
        self._running = False
        if self._task:
            self._task.kill()
            self._task = None
        self.log.info("OdPpMonitor: Stopped monitoring")
        
    def get_stats(self):
        """Get monitoring statistics."""
        return self.stats.copy()
        
    def get_violations(self):
        """Get list of detected violations."""
        return self.stats['violations'].copy()
        
    def clear_violations(self):
        """Clear the violation list."""
        self.stats['violations'] = []
        
    def report(self):
        """Print a summary report of the monitoring statistics."""
        self.log.info("=" * 70)
        self.log.info("OD/PP Monitor Report")
        self.log.info("=" * 70)
        self.log.info(f"  OD mode samples:     {self.stats['od_mode_samples']}")
        self.log.info(f"  PP mode samples:     {self.stats['pp_mode_samples']}")
        self.log.info(f"  SDA OE high samples: {self.stats['sda_oe_high_samples']}")
        self.log.info(f"  SDA OE low samples:  {self.stats['sda_oe_low_samples']}")
        self.log.info(f"  Violations:          {len(self.stats['violations'])}")
        
        if self.stats['violations']:
            self.log.error("  Violation Details:")
            for v in self.stats['violations'][:10]:  # Show first 10
                self.log.error(f"    - {v}")
            if len(self.stats['violations']) > 10:
                self.log.error(f"    ... and {len(self.stats['violations']) - 10} more")
        self.log.info("=" * 70)
        
    async def _monitor_loop(self):
        """Main monitoring loop - runs in background."""
        while self._running:
            if self.clk:
                await RisingEdge(self.clk)
            else:
                await Timer(10, 'ns')  # Fallback if no clock
                
            try:
                sel_od_pp = int(self.sel_od_pp.value)
                sda_oe = int(self.sda_oe.value)
                sda_o = int(self.sda_o.value)
                
                # Update statistics
                if sel_od_pp == 0:
                    self.stats['od_mode_samples'] += 1
                else:
                    self.stats['pp_mode_samples'] += 1
                    
                if sda_oe == 1:
                    self.stats['sda_oe_high_samples'] += 1
                else:
                    self.stats['sda_oe_low_samples'] += 1
                    
                # Check for violations based on truth table:
                # OD mode (sel_od_pp=0): sda_oe should be !sda_o
                #   - sda_o=0 -> sda_oe=1 (driving low)
                #   - sda_o=1 -> sda_oe=0 (hi-z)
                # PP mode (sel_od_pp=1): sda_oe should always be 1
                #   - Always driving (either 0 or 1)
                
                if sel_od_pp == 0:  # Open Drain mode
                    expected_oe = 1 if sda_o == 0 else 0
                    if sda_oe != expected_oe:
                        violation = (
                            f"OD mode violation: sel_od_pp={sel_od_pp}, "
                            f"sda_o={sda_o}, sda_oe={sda_oe} "
                            f"(expected sda_oe={expected_oe})"
                        )
                        self.stats['violations'].append(violation)
                        self.log.error(f"OdPpMonitor: {violation}")
                        
                else:  # Push-Pull mode
                    if sda_oe != 1:
                        violation = (
                            f"PP mode violation: sel_od_pp={sel_od_pp}, "
                            f"sda_o={sda_o}, sda_oe={sda_oe} "
                            f"(expected sda_oe=1 in PP mode)"
                        )
                        self.stats['violations'].append(violation)
                        self.log.error(f"OdPpMonitor: {violation}")
                        
            except ValueError:
                # Signal might be X or Z during reset
                pass


class OdPpModeTracker:
    """
    Tracks OD/PP mode transitions and provides assertions about when
    certain modes should be active.
    
    This is useful for verifying that:
    - Target uses PP mode when transmitting data
    - Target uses OD mode for ACK/NACK
    - Mode transitions happen at correct times
    """
    
    def __init__(self, dut, log=None):
        """
        Initialize the mode tracker.
        
        Args:
            dut: The DUT handle
            log: Optional logger
        """
        self.dut = dut
        self.log = log or dut._log
        self._transitions = []
        
        # Resolve signals
        try:
            self.sel_od_pp = dut.i3c_sel_od_pp
            self.bus_scl = dut.bus_scl
            if hasattr(dut, 'aclk'):
                self.clk = dut.aclk
            elif hasattr(dut, 'hclk'):
                self.clk = dut.hclk
            else:
                self.clk = None
            self._available = True
        except AttributeError:
            self._available = False
            
    def is_available(self):
        """Check if tracking is available."""
        return self._available
        
    async def expect_od_mode(self, timeout_ns=1000, description=""):
        """
        Assert that the core should be in OD mode.
        
        Args:
            timeout_ns: How long to wait for OD mode
            description: Description of why OD mode is expected
        """
        if not self._available:
            return True
            
        start_time = cocotb.utils.get_sim_time('ns')
        deadline = start_time + timeout_ns
        
        while cocotb.utils.get_sim_time('ns') < deadline:
            try:
                if int(self.sel_od_pp.value) == 0:
                    return True
            except ValueError:
                pass
            await Timer(10, 'ns')
            
        self.log.error(f"OdPpModeTracker: Expected OD mode but got PP. {description}")
        return False
        
    async def expect_pp_mode(self, timeout_ns=1000, description=""):
        """
        Assert that the core should be in PP mode.
        
        Args:
            timeout_ns: How long to wait for PP mode
            description: Description of why PP mode is expected
        """
        if not self._available:
            return True
            
        start_time = cocotb.utils.get_sim_time('ns')
        deadline = start_time + timeout_ns
        
        while cocotb.utils.get_sim_time('ns') < deadline:
            try:
                if int(self.sel_od_pp.value) == 1:
                    return True
            except ValueError:
                pass
            await Timer(10, 'ns')
            
        self.log.error(f"OdPpModeTracker: Expected PP mode but got OD. {description}")
        return False
        
    def get_current_mode(self):
        """Get the current drive mode."""
        if not self._available:
            return None
        try:
            return "PP" if int(self.sel_od_pp.value) == 1 else "OD"
        except ValueError:
            return "X"
            
    async def wait_for_mode_change(self, timeout_ns=10000):
        """Wait for a mode change to occur."""
        if not self._available:
            return None
            
        try:
            current = int(self.sel_od_pp.value)
        except ValueError:
            current = -1
            
        start_time = cocotb.utils.get_sim_time('ns')
        deadline = start_time + timeout_ns
        
        while cocotb.utils.get_sim_time('ns') < deadline:
            try:
                new_val = int(self.sel_od_pp.value)
                if new_val != current:
                    new_mode = "PP" if new_val == 1 else "OD"
                    old_mode = "PP" if current == 1 else "OD"
                    self._transitions.append({
                        'time': cocotb.utils.get_sim_time('ns'),
                        'from': old_mode,
                        'to': new_mode
                    })
                    return new_mode
            except ValueError:
                pass
            await Timer(10, 'ns')
            
        return None  # Timeout
        
    def get_transitions(self):
        """Get list of all recorded mode transitions."""
        return self._transitions.copy()


class I3cBusState(Enum):
    """States for tracking I3C bus protocol."""
    IDLE = auto()
    START = auto()
    ADDRESS = auto()
    ADDRESS_ACK = auto()
    WRITE_DATA = auto()
    WRITE_ACK = auto()
    READ_DATA = auto()
    READ_ACK = auto()
    STOP = auto()


class WriteAckHandoffMonitor:
    """
    Monitor for I3C Write ACK OD→PP Handoff Protocol (I3C Spec Section 5.1.2.1)
    
    This monitor verifies that during a write ACK, the target correctly:
    1. Holds SDA Low during ACK (while SCL is Low) in Open Drain mode
    2. Releases SDA to High-Z after seeing SCL rise
    3. Releases using normal timing (as soon as SCL rises)
    
    The monitor runs continuously and tracks:
    - SCL edges to detect ACK periods (9th bit after each byte)
    - Target's sel_od_pp and sda_oe signals
    - Violations of the handoff protocol
    """
    
    def __init__(self, dut, log=None):
        """
        Initialize the Write ACK Handoff Monitor.
        
        Args:
            dut: The DUT handle (i3c_test_wrapper)
            log: Optional logger. If None, uses dut._log
        """
        self.dut = dut
        self.log = log or dut._log
        self._running = False
        self._task = None
        
        # Protocol tracking state
        self._bit_count = 0
        self._is_write = False  # True if current transfer is a write to target
        self._in_ack_phase = False
        self._saw_start = False
        
        # Statistics
        self.stats = {
            'write_acks_checked': 0,
            'read_acks_checked': 0,
            'handoff_violations': [],
            'timing_violations': [],
            'od_during_write_ack': 0,
            'pp_transitions': 0,
        }
        
        # Try to resolve signals
        self._resolve_signals()
        
    def _resolve_signals(self):
        """Resolve the signal paths in the DUT hierarchy."""
        try:
            # Target signals
            self.sel_od_pp = self.dut.i3c_sel_od_pp
            self.sda_oe = self.dut.i3c_sda_oe
            self.sda_o = self.dut.i3c_sda_o
            
            # Bus signals
            self.bus_sda = self.dut.bus_sda
            self.bus_scl = self.dut.bus_scl
            
            # Clock
            if hasattr(self.dut, 'aclk'):
                self.clk = self.dut.aclk
            elif hasattr(self.dut, 'hclk'):
                self.clk = self.dut.hclk
            else:
                self.clk = None
                
            self._available = True
            self.log.info("WriteAckHandoffMonitor: Successfully resolved signals")
            
        except AttributeError as e:
            self.log.warning(f"WriteAckHandoffMonitor: Could not resolve signals: {e}")
            self._available = False
            
    def is_available(self):
        """Check if the monitor signals are available."""
        return self._available
        
    async def start(self):
        """Start the background monitoring task."""
        if not self._available:
            self.log.warning("WriteAckHandoffMonitor: Cannot start - signals not available")
            return
            
        if self._running:
            self.log.warning("WriteAckHandoffMonitor: Already running")
            return
            
        self._running = True
        self._task = cocotb.start_soon(self._monitor_loop())
        self.log.info("WriteAckHandoffMonitor: Started monitoring Write ACK handoff protocol")
        
    def stop(self):
        """Stop the background monitoring task."""
        self._running = False
        if self._task:
            self._task.kill()
            self._task = None
        self.log.info("WriteAckHandoffMonitor: Stopped monitoring")
        
    def get_violations(self):
        """Get all detected violations."""
        return {
            'handoff': self.stats['handoff_violations'].copy(),
            'timing': self.stats['timing_violations'].copy(),
        }
        
    def clear_violations(self):
        """Clear all violations."""
        self.stats['handoff_violations'] = []
        self.stats['timing_violations'] = []
        
    def report(self):
        """Print a summary report."""
        self.log.info("=" * 70)
        self.log.info("Write ACK Handoff Monitor Report")
        self.log.info("=" * 70)
        self.log.info(f"  Write ACKs checked:      {self.stats['write_acks_checked']}")
        self.log.info(f"  Read ACKs checked:       {self.stats['read_acks_checked']}")
        self.log.info(f"  OD samples during ACK:   {self.stats['od_during_write_ack']}")
        self.log.info(f"  PP transitions:          {self.stats['pp_transitions']}")
        self.log.info(f"  Handoff violations:      {len(self.stats['handoff_violations'])}")
        self.log.info(f"  Timing violations:       {len(self.stats['timing_violations'])}")
        
        if self.stats['handoff_violations']:
            self.log.error("  Handoff Violations:")
            for v in self.stats['handoff_violations'][:5]:
                self.log.error(f"    - {v}")
                
        if self.stats['timing_violations']:
            self.log.error("  Timing Violations:")
            for v in self.stats['timing_violations'][:5]:
                self.log.error(f"    - {v}")
        self.log.info("=" * 70)
        
    async def _monitor_loop(self):
        """
        Main monitoring loop - tracks SCL edges and verifies ACK handoff.
        
        Protocol state machine:
        - Detect START condition (SDA falls while SCL high)
        - Count bits on each SCL falling edge
        - Track R/W bit from address phase
        - On bit 9 (ACK/NACK), check the handoff protocol for writes only
        - Detect STOP condition (SDA rises while SCL high)
        
        Note: We only check write ACK handoff. For reads, the controller ACKs
        (not the target), so we don't check the target's OD/PP mode.
        """
        last_scl = 1
        last_sda = 1
        address_byte = 0  # Accumulates address bits
        
        while self._running:
            # Sample at clock rate
            if self.clk:
                await RisingEdge(self.clk)
            else:
                await Timer(10, 'ns')
                
            try:
                scl = int(self.bus_scl.value)
                sda = int(self.bus_sda.value)
                sel_od_pp = int(self.sel_od_pp.value)
                sda_oe = int(self.sda_oe.value)
                sda_o = int(self.sda_o.value)
            except ValueError:
                # Signals might be X or Z
                last_scl = 1
                last_sda = 1
                continue
                
            # Detect START condition: SDA falls while SCL is high
            if last_sda == 1 and sda == 0 and scl == 1:
                self._saw_start = True
                self._bit_count = 0
                self._is_write = False
                self._in_ack_phase = False
                address_byte = 0
                
            # Detect STOP condition: SDA rises while SCL is high
            if last_sda == 0 and sda == 1 and scl == 1:
                self._saw_start = False
                self._bit_count = 0
                self._in_ack_phase = False
                
            # SCL rising edge - sample data bits during address phase
            if last_scl == 0 and scl == 1 and self._saw_start:
                # During address phase (bits 1-8), sample the address+R/W
                if self._bit_count < 8:
                    address_byte = (address_byte << 1) | sda
                    
                if self._in_ack_phase and self._is_write:
                    # We're in ACK phase for a WRITE, SCL just went high
                    # Per spec: Target should be in OD mode when ACKing a write
                    self.stats['write_acks_checked'] += 1
                    
                    # Target should be in OD mode during write ACK
                    if sel_od_pp != 0:
                        violation = (
                            f"Write ACK handoff: Target not in OD mode at SCL rise. "
                            f"sel_od_pp={sel_od_pp}, expected 0 (OD). "
                            f"time={cocotb.utils.get_sim_time('ns')}ns"
                        )
                        self.stats['handoff_violations'].append(violation)
                        self.log.error(f"WriteAckHandoffMonitor: {violation}")
                    else:
                        self.stats['od_during_write_ack'] += 1
                elif self._in_ack_phase and not self._is_write:
                    self.stats['read_acks_checked'] += 1
                        
            # SCL falling edge - count bits, detect ACK phase
            if last_scl == 1 and scl == 0 and self._saw_start:
                self._bit_count += 1
                
                # At bit 9 (after 8 address/data bits), this is ACK phase
                if self._bit_count == 9:
                    # This is the ACK bit period after address
                    self._in_ack_phase = True
                    # R/W bit is LSB of address byte (bit 0): 0=write, 1=read
                    self._is_write = (address_byte & 0x01) == 0
                    
                elif self._bit_count > 9 and (self._bit_count - 9) % 9 == 0:
                    # Subsequent ACK bits (every 9 bits after the first)
                    self._in_ack_phase = True
                    # Keep the same R/W direction for data ACKs
                    
                elif self._in_ack_phase:
                    # We were in ACK phase, now starting next data byte
                    self._in_ack_phase = False
                
            # Check for PP transition tracking
            if sel_od_pp == 1:
                self.stats['pp_transitions'] += 1
                
            last_scl = scl
            last_sda = sda


class I3cProtocolMonitor:
    """
    Comprehensive I3C Protocol Monitor that runs continuously during tests.
    
    Combines multiple monitoring capabilities:
    - OD/PP signal consistency (OdPpMonitor)
    - Write ACK handoff protocol (WriteAckHandoffMonitor)
    - OD/PP mode transitions (OdPpModeTracker)
    
    This is intended to be instantiated once and run for all I3C tests to
    catch protocol violations early.
    """
    
    def __init__(self, dut, log=None):
        """
        Initialize the comprehensive protocol monitor.
        
        Args:
            dut: The DUT handle
            log: Optional logger
        """
        self.dut = dut
        self.log = log or dut._log
        
        # Create sub-monitors
        self.od_pp_monitor = OdPpMonitor(dut, log)
        self.handoff_monitor = WriteAckHandoffMonitor(dut, log)
        self.mode_tracker = OdPpModeTracker(dut, log)
        
        self._running = False
        
    def is_available(self):
        """Check if monitoring is available."""
        return (self.od_pp_monitor.is_available() or 
                self.handoff_monitor.is_available())
        
    async def start(self):
        """Start all monitors."""
        if self._running:
            return
            
        self._running = True
        
        if self.od_pp_monitor.is_available():
            await self.od_pp_monitor.start()
            
        if self.handoff_monitor.is_available():
            await self.handoff_monitor.start()
            
        self.log.info("I3cProtocolMonitor: All monitors started")
        
    def stop(self):
        """Stop all monitors."""
        self._running = False
        self.od_pp_monitor.stop()
        self.handoff_monitor.stop()
        self.log.info("I3cProtocolMonitor: All monitors stopped")
        
    def get_all_violations(self):
        """Get all violations from all monitors."""
        violations = {
            'od_pp': self.od_pp_monitor.get_violations(),
            'handoff': self.handoff_monitor.get_violations(),
        }
        total = (len(violations['od_pp']) + 
                 len(violations['handoff'].get('handoff', [])) +
                 len(violations['handoff'].get('timing', [])))
        return violations, total
        
    def report(self):
        """Print reports from all monitors."""
        self.od_pp_monitor.report()
        self.handoff_monitor.report()
        
    def assert_no_violations(self):
        """
        Assert that no violations were detected.
        Raises AssertionError if any violations found.
        """
        violations, total = self.get_all_violations()
        if total > 0:
            self.report()
            raise AssertionError(
                f"I3C Protocol Monitor detected {total} violations. "
                f"See report above for details."
            )


async def create_od_pp_monitor(dut, auto_start=True):
    """
    Factory function to create and optionally start an OD/PP monitor.
    
    Args:
        dut: The DUT handle
        auto_start: If True, automatically start monitoring
        
    Returns:
        OdPpMonitor instance (or None if signals unavailable)
    """
    monitor = OdPpMonitor(dut)
    
    if not monitor.is_available():
        dut._log.warning("OD/PP monitoring not available - signals not found")
        return None
        
    if auto_start:
        await monitor.start()
        
    return monitor


async def create_protocol_monitor(dut, auto_start=True):
    """
    Factory function to create and optionally start the comprehensive
    I3C protocol monitor.
    
    This is the recommended entry point for monitoring all I3C protocol
    compliance in tests. It includes:
    - OD/PP signal consistency checking
    - Write ACK OD→PP handoff protocol verification (I3C Spec 5.1.2.1)
    - Mode transition tracking
    
    Usage in tests:
        from od_pp_monitor import create_protocol_monitor
        
        async def test_my_i3c_test(dut):
            # Start comprehensive monitoring
            protocol_monitor = await create_protocol_monitor(dut)
            
            # ... run test ...
            
            # Check for violations at end
            if protocol_monitor:
                protocol_monitor.report()
                protocol_monitor.assert_no_violations()  # Fails test if violations
    
    Args:
        dut: The DUT handle
        auto_start: If True, automatically start all monitors
        
    Returns:
        I3cProtocolMonitor instance (or None if signals unavailable)
    """
    monitor = I3cProtocolMonitor(dut)
    
    if not monitor.is_available():
        dut._log.warning("I3C Protocol monitoring not available - signals not found")
        return None
        
    if auto_start:
        await monitor.start()
        
    return monitor

