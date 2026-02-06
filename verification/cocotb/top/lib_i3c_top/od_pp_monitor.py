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
"""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Edge, Timer, First


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
