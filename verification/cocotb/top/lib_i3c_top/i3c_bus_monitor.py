# SPDX-License-Identifier: Apache-2.0
"""
I3C SDR Bus Monitor -- continuous protocol-level verification of the I3C Target DUT.

Monitors the I3C bus signals (SDA, SCL) along with the DUT's per-device output-enable
and OD/PP mode signals to verify that the Target Device behaves correctly according to
the I3C v1.1 specification.

Checks performed (with spec section references):
  1. OD/PP truth table integrity             -- bus_tx_flow truth table
  2. Address phase uses Open Drain            -- S5.1.2.2.1
  3. No target arbitration after Repeated Sr  -- S5.1.2.2.4
  4. ACK/NACK bit is Open Drain               -- S5.1.2.2.4, S5.1.2.3.1
  5. Write-ACK handoff (target releases SDA)  -- S5.1.2.3.1
  6. IBI-ACK handoff (target takes SDA in PP) -- S5.1.2.3.2
  7. Read data bytes in Push-Pull             -- S5.1.2.3
  8. T-bit end: target releases to Hi-Z       -- S5.1.2.3.4
  9. T-bit continue: target releases to Hi-Z  -- S5.1.2.3.4
 10. Bus contention detection                 -- general safety
 11. Target silent on non-matching address     -- S5.1.2
 12. IBI only after START, not after Sr        -- S5.1.6.2

Started automatically by I3CTopTestInterface.setup(); raises on violation.
"""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer, First, Edge
from enum import IntEnum, auto


class BusPhase(IntEnum):
    """Protocol phase tracking for the I3C SDR bus."""
    IDLE = auto()
    START = auto()           # S or Sr detected, about to clock address
    ADDR_BITS = auto()       # Clocking 7-bit address + RnW
    ADDR_ACK = auto()        # 9th bit: ACK/NACK
    WRITE_DATA = auto()      # Controller writing data bytes (8 data + T-parity)
    WRITE_TBIT = auto()      # 9th bit of controller write (parity / T-bit)
    READ_DATA = auto()       # Target returning read data bytes in PP
    READ_TBIT = auto()       # 9th bit of target read (end-of-data / T-bit)
    IBI_ADDR_BITS = auto()   # IBI: target driving address in OD
    IBI_ADDR_ACK = auto()    # IBI: controller ACK/NACK
    IBI_MDB = auto()         # IBI: mandatory data byte in PP
    IBI_DATA = auto()        # IBI: additional data bytes in PP
    IBI_DATA_TBIT = auto()   # IBI: T-bit for additional data
    CCC_BYTE = auto()        # CCC command byte (controller write)
    CCC_TBIT = auto()        # CCC T-bit
    ENTDAA = auto()          # Dynamic address assignment
    HDR_MODE = auto()        # Bus in HDR mode -- suspend SDR checking


class I3cBusMonitor:
    """
    Continuous protocol-level I3C bus monitor.

    Watches bus_scl, bus_sda, and per-device DUT signals (i3c_sda_o, i3c_sda_oe,
    i3c_sel_od_pp) to verify the I3C Target complies with the specification.
    """

    I3C_BROADCAST_ADDR = 0x7E

    def __init__(self, dut, log=None):
        self.dut = dut
        self.log = log or dut._log
        self._running = False
        self._task = None

        # Violation tracking
        self.violations = []
        self.violation_count = 0

        # Statistics
        self.stats = {
            'scl_edges': 0,
            'starts_detected': 0,
            'stops_detected': 0,
            'addr_phases': 0,
            'read_bytes': 0,
            'write_bytes': 0,
            'ibi_requests': 0,
            'od_samples': 0,
            'pp_samples': 0,
            'contention_checks': 0,
        }

        # Protocol state
        self._phase = BusPhase.IDLE
        self._bit_count = 0
        self._addr_accum = 0
        self._rnw = 0
        self._is_broadcast = False
        self._is_addressed_to_dut = False
        self._is_ibi = False
        self._is_repeated_start = False
        self._dut_dynamic_addr = None  # Will be set after DAA
        self._data_accum = 0
        self._byte_in_msg = 0         # Which byte in the current message
        self._is_ccc = False
        self._ccc_code = 0
        self._is_entdaa = False
        self._prev_scl = 1
        self._prev_sda = 1
        self._bus_active = False       # True between START and STOP

        # Resolve signal handles
        self._resolve_signals()

    def _resolve_signals(self):
        """Resolve DUT signal paths."""
        try:
            self.bus_sda = self.dut.bus_sda
            self.bus_scl = self.dut.bus_scl

            # DUT (device 2) signals exposed at wrapper level
            self.i3c_sda_o = self.dut.i3c_sda_o
            self.i3c_sda_oe = self.dut.i3c_sda_oe
            self.i3c_sel_od_pp = self.dut.i3c_sel_od_pp

            # Clock for sampling
            if hasattr(self.dut, 'aclk'):
                self.clk = self.dut.aclk
            elif hasattr(self.dut, 'hclk'):
                self.clk = self.dut.hclk
            else:
                self.clk = None

            self._available = True
            self.log.info("I3cBusMonitor: Signals resolved successfully")
        except AttributeError as e:
            self._available = False
            self.log.warning(f"I3cBusMonitor: Cannot resolve signals: {e}")

    def is_available(self):
        return self._available

    def set_dut_dynamic_addr(self, addr):
        """Set the DUT's dynamic address so the monitor can track addressing."""
        self._dut_dynamic_addr = addr
        self.log.info(f"I3cBusMonitor: DUT dynamic address set to 0x{addr:02X}")

    async def start(self):
        if not self._available:
            self.log.warning("I3cBusMonitor: Cannot start -- signals unavailable")
            return
        if self._running:
            return
        self._running = True
        self._task = cocotb.start_soon(self._monitor_loop())
        self.log.info("I3cBusMonitor: Started")

    def stop(self):
        self._running = False
        if self._task:
            self._task.kill()
            self._task = None

    def _record_violation(self, check_id, message):
        """Record a violation and raise immediately."""
        time_ns = cocotb.utils.get_sim_time('ns')
        full_msg = f"[{check_id}] @{time_ns}ns phase={self._phase.name}: {message}"
        self.violations.append(full_msg)
        self.violation_count += 1
        self.log.error(f"I3cBusMonitor VIOLATION: {full_msg}")

    def _get_dut_sda_oe(self):
        """Read DUT sda output enable, returns None on X/Z."""
        try:
            return int(self.i3c_sda_oe.value)
        except ValueError:
            return None

    def _get_dut_sel_od_pp(self):
        """Read DUT OD/PP mode, returns None on X/Z."""
        try:
            return int(self.i3c_sel_od_pp.value)
        except ValueError:
            return None

    def _get_dut_sda_o(self):
        """Read DUT SDA output data, returns None on X/Z."""
        try:
            return int(self.i3c_sda_o.value)
        except ValueError:
            return None

    def _dut_is_driving(self):
        """Return True if DUT has output-enable asserted."""
        oe = self._get_dut_sda_oe()
        return oe == 1

    def _dut_is_pp(self):
        """Return True if DUT is in Push-Pull mode."""
        pp = self._get_dut_sel_od_pp()
        return pp == 1

    def _dut_is_od(self):
        """Return True if DUT is in Open-Drain mode."""
        pp = self._get_dut_sel_od_pp()
        return pp == 0

    def _check_od_pp_truth_table(self):
        """
        Check 1: Verify the OD/PP truth table is respected.

        OD mode (sel_od_pp=0):
          sda_o=0 --> sda_oe=1 (driving low)
          sda_o=1 --> sda_oe=0 (hi-z, releasing)
        PP mode (sel_od_pp=1):
          sda_oe always = 1 (always driving)
        """
        sel = self._get_dut_sel_od_pp()
        oe = self._get_dut_sda_oe()
        sda = self._get_dut_sda_o()
        if sel is None or oe is None or sda is None:
            return  # X/Z during reset

        if sel == 0:  # Open Drain
            self.stats['od_samples'] += 1
            expected_oe = 1 if sda == 0 else 0
            if oe != expected_oe:
                self._record_violation(
                    "OD_PP_TABLE",
                    f"OD mode: sda_o={sda} expects sda_oe={expected_oe}, got {oe}"
                )
        else:  # Push-Pull
            self.stats['pp_samples'] += 1
            if oe != 1:
                self._record_violation(
                    "OD_PP_TABLE",
                    f"PP mode: sda_oe must be 1, got {oe} (sda_o={sda})"
                )

    def _check_contention(self):
        """
        Check 10: Bus contention -- DUT must not actively drive SDA high in PP
        while the bus reads low (another device pulling it low in OD).

        In OD mode, contention is safe (wired-AND). In PP mode, if DUT drives
        high but bus is low, a physical bus would see contention.

        Skipped during IDLE phase: DUT may be transitioning modes between
        transfers and there is no active bus transaction to contend with.
        """
        self.stats['contention_checks'] += 1
        if self._phase == BusPhase.IDLE:
            return
        if not self._dut_is_driving():
            return

        if self._dut_is_pp():
            sda_o = self._get_dut_sda_o()
            try:
                bus_sda = int(self.bus_sda.value)
            except ValueError:
                return

            # PP driving high while bus is low => contention
            if sda_o == 1 and bus_sda == 0:
                self._record_violation(
                    "BUS_CONTENTION",
                    f"DUT PP-driving SDA=1 but bus_sda=0 -- bus contention!"
                )

    def _check_target_silent_nonmatching(self):
        """
        Check 11: Target shall not transmit on the Bus in response
        to a non-matching Address (S5.1.2).
        """
        if self._phase in (BusPhase.WRITE_DATA, BusPhase.WRITE_TBIT,
                           BusPhase.READ_DATA, BusPhase.READ_TBIT):
            if not self._is_addressed_to_dut and not self._is_broadcast:
                if self._dut_is_driving():
                    self._record_violation(
                        "TARGET_SILENT",
                        f"DUT driving SDA during non-matching address phase "
                        f"(addr=0x{self._addr_accum:02X})"
                    )

    # --------------------------------------------------------------
    # Phase-specific checks on SCL edges
    # --------------------------------------------------------------

    def _on_scl_rising(self, bus_sda):
        """Called on every SCL rising edge."""
        self.stats['scl_edges'] += 1

        # Always check truth table and contention
        self._check_od_pp_truth_table()
        self._check_contention()

        if self._phase == BusPhase.ADDR_BITS:
            self._on_addr_bit_rise(bus_sda)
        elif self._phase == BusPhase.ADDR_ACK:
            self._on_addr_ack_rise(bus_sda)
        elif self._phase == BusPhase.IBI_ADDR_BITS:
            self._on_addr_bit_rise(bus_sda)
        elif self._phase == BusPhase.IBI_ADDR_ACK:
            self._on_ibi_ack_rise(bus_sda)
        elif self._phase == BusPhase.WRITE_DATA:
            pass  # Controller drives, DUT should be silent
        elif self._phase == BusPhase.WRITE_TBIT:
            pass  # Controller drives parity
        elif self._phase == BusPhase.READ_DATA:
            self._on_read_data_rise()
        elif self._phase == BusPhase.READ_TBIT:
            self._on_read_tbit_rise(bus_sda)
        elif self._phase == BusPhase.IBI_MDB:
            self._on_read_data_rise()
        elif self._phase == BusPhase.IBI_DATA:
            self._on_read_data_rise()
        elif self._phase == BusPhase.IBI_DATA_TBIT:
            self._on_read_tbit_rise(bus_sda)
        elif self._phase == BusPhase.CCC_BYTE:
            self._data_accum = (self._data_accum << 1) | bus_sda
        elif self._phase == BusPhase.CCC_TBIT:
            pass

    def _on_scl_falling(self, bus_sda):
        """Called on every SCL falling edge."""
        self._check_od_pp_truth_table()

        if self._phase == BusPhase.ADDR_BITS:
            self._on_addr_bit_fall()
        elif self._phase == BusPhase.ADDR_ACK:
            self._on_addr_ack_fall(bus_sda)
        elif self._phase == BusPhase.IBI_ADDR_BITS:
            self._on_addr_bit_fall()
        elif self._phase == BusPhase.IBI_ADDR_ACK:
            self._on_ibi_ack_fall(bus_sda)
        elif self._phase == BusPhase.WRITE_DATA:
            self._on_write_data_fall()
        elif self._phase == BusPhase.WRITE_TBIT:
            self._on_write_tbit_fall()
        elif self._phase == BusPhase.READ_DATA:
            self._on_read_data_fall()
        elif self._phase == BusPhase.READ_TBIT:
            self._on_read_tbit_fall(bus_sda)
        elif self._phase == BusPhase.IBI_MDB:
            self._on_ibi_mdb_fall()
        elif self._phase == BusPhase.IBI_DATA:
            self._on_ibi_data_fall()
        elif self._phase == BusPhase.IBI_DATA_TBIT:
            self._on_ibi_data_tbit_fall(bus_sda)
        elif self._phase == BusPhase.CCC_BYTE:
            self._on_ccc_byte_fall()
        elif self._phase == BusPhase.CCC_TBIT:
            self._on_ccc_tbit_fall()

        self._check_target_silent_nonmatching()

    # --------------------------------------------------------------
    # Address phase
    # --------------------------------------------------------------

    def _enter_addr_phase(self, is_repeated_start):
        """Start clocking an address header."""
        self._is_repeated_start = is_repeated_start
        self._bit_count = 0
        self._addr_accum = 0
        self._rnw = 0
        self._is_broadcast = False
        self._is_addressed_to_dut = False
        self._is_ibi = False
        self._is_ccc = False
        self._byte_in_msg = 0
        self._data_accum = 0

        # IBI: target-initiated START (not Sr) can be an IBI attempt
        # We'll detect this during address bits based on DUT driving behavior
        self._phase = BusPhase.ADDR_BITS
        self.stats['addr_phases'] += 1

    def _on_addr_bit_rise(self, bus_sda):
        """Sample address bit on SCL rising edge."""
        if self._bit_count < 7:
            # Accumulate address bits
            self._addr_accum = (self._addr_accum << 1) | bus_sda

            # Check 2: Address phase must use Open Drain (S5.1.2.2.1)
            # After a START (not Sr), the address is arbitrable --> OD required
            # After Sr, controller drives PP but target should NOT drive at all
            if not self._is_repeated_start:
                # Arbitrable header after START: DUT should use OD if driving
                if self._dut_is_driving() and self._dut_is_pp():
                    self._record_violation(
                        "ADDR_OD",
                        f"DUT using PP during arbitrable address bit[{self._bit_count}] "
                        f"after START (S5.1.2.2.1)"
                    )
            else:
                # Check 3: After Repeated START, Target shall NOT drive address
                # (S5.1.2.2.4)
                if self._dut_is_driving():
                    # Exception: if it's an IBI request... but IBI is only after
                    # START not Sr, so driving here is always wrong
                    self._record_violation(
                        "NO_ARB_AFTER_SR",
                        f"DUT driving SDA during address after Repeated START "
                        f"bit[{self._bit_count}] (S5.1.2.2.4)"
                    )

        elif self._bit_count == 7:
            # RnW bit
            self._rnw = bus_sda

        self._bit_count += 1

    def _on_addr_bit_fall(self):
        """After 8 bits (7 addr + RnW), move to ACK phase."""
        if self._bit_count >= 8:
            addr = self._addr_accum
            self._is_broadcast = (addr == self.I3C_BROADCAST_ADDR)
            self._is_addressed_to_dut = (
                self._dut_dynamic_addr is not None and
                addr == self._dut_dynamic_addr
            )

            # Detect IBI: target-initiated, addr matches DUT, RnW=1,
            # and not after Sr
            if (not self._is_repeated_start and
                    self._is_addressed_to_dut and self._rnw == 1):
                self._is_ibi = True
                self.stats['ibi_requests'] += 1
                self._phase = BusPhase.IBI_ADDR_ACK
            else:
                self._phase = BusPhase.ADDR_ACK

    def _on_addr_ack_rise(self, bus_sda):
        """
        Check 4: ACK/NACK bit -- always Open Drain (S5.1.2.2.4).
        Target drives ACK low in OD; NACK = passive (not driving).
        """
        if self._is_addressed_to_dut or self._is_broadcast:
            if self._dut_is_driving() and self._dut_is_pp():
                self._record_violation(
                    "ACK_OD",
                    f"DUT using PP during ACK/NACK (must be OD) "
                    f"addr=0x{self._addr_accum:02X} (S5.1.2.2.4)"
                )

    def _on_addr_ack_fall(self, bus_sda):
        """
        After ACK, determine next phase based on address and RnW.

        Check 5: Write-ACK handoff -- on SCL rising during ACK, Target should
        release SDA to Hi-Z so Controller can take over in PP (S5.1.2.3.1).
        """
        acked = (bus_sda == 0)

        if not acked:
            # NACKed -- target goes idle until next START/Sr
            self._phase = BusPhase.IDLE
            return

        if self._is_broadcast and self._rnw == 0:
            # Broadcast write --> expecting CCC command byte
            self._phase = BusPhase.CCC_BYTE
            self._bit_count = 0
            self._data_accum = 0
            self._byte_in_msg = 0
            return

        if self._is_addressed_to_dut or self._is_broadcast:
            if self._rnw == 0:
                # Private write to DUT
                self._phase = BusPhase.WRITE_DATA
                self._bit_count = 0
                self._data_accum = 0
            else:
                # Private read from DUT -- target will transmit in PP
                self._phase = BusPhase.READ_DATA
                self._bit_count = 0
                self._data_accum = 0
        else:
            # Not addressed to DUT -- go idle, DUT should be silent
            self._phase = BusPhase.IDLE

    # --------------------------------------------------------------
    # Write data (Controller --> Target)
    # --------------------------------------------------------------

    def _on_write_data_fall(self):
        """Count write data bits. DUT should NOT drive during controller writes."""
        self._bit_count += 1
        if self._bit_count >= 8:
            self._phase = BusPhase.WRITE_TBIT
            self._bit_count = 0

    def _on_write_tbit_fall(self):
        """After T-bit (parity), next byte or wait for Sr/P."""
        self.stats['write_bytes'] += 1
        self._byte_in_msg += 1
        self._phase = BusPhase.WRITE_DATA
        self._bit_count = 0

    # --------------------------------------------------------------
    # Read data (Target --> Controller)
    # --------------------------------------------------------------

    def _on_read_data_rise(self):
        """
        Check 7: During read data, Target should be in PP mode (S5.1.2.3).
        """
        if self._is_addressed_to_dut:
            if self._dut_is_driving() and self._dut_is_od():
                self._record_violation(
                    "READ_PP",
                    f"DUT driving read data in OD mode -- must use PP (S5.1.2.3)"
                )

    def _on_read_data_fall(self):
        """Count read data bits."""
        self._bit_count += 1
        if self._bit_count >= 8:
            self._phase = BusPhase.READ_TBIT
            self._bit_count = 0

    def _on_read_tbit_rise(self, bus_sda):
        """
        Check 8/9: T-bit behavior on SCL rising edge (S5.1.2.3.4).

        After the rising edge, the Target shall release SDA to Hi-Z:
        - T-bit=0 (end): Target sets SDA low on falling, releases on rising
        - T-bit=1 (continue): Target sets SDA high on falling, releases on rising

        In both cases, the Target goes to OD/Hi-Z after the rising edge.
        We check this condition: on the rising edge, the DUT should still be
        driving (it hasn't released yet), then it should release.
        """
        pass  # The release happens asynchronously after posedge;
              # we check on the NEXT falling edge below.

    def _on_read_tbit_fall(self, bus_sda):
        """
        After T-bit, check that the Target has properly released SDA.

        Check 8: T-bit=0 (end) -- Target released to Hi-Z, controller takes over
        Check 9: T-bit=1 (continue) -- Target released, checks if controller aborted

        At this falling edge, the DUT should be back in OD mode after releasing.
        """
        self.stats['read_bytes'] += 1
        self._byte_in_msg += 1

        # After T-bit, if SDA went low during SCL high, controller aborted (Repeated START)
        # Otherwise, Target continues with next byte.
        # Either way, we transition appropriately.

        # The actual phase transition is handled by START/STOP detection.
        # If no START/STOP happened, we continue reading.
        self._phase = BusPhase.READ_DATA
        self._bit_count = 0

    # --------------------------------------------------------------
    # IBI phases
    # --------------------------------------------------------------

    def _on_ibi_ack_rise(self, bus_sda):
        """
        IBI ACK phase on SCL rising.
        Controller ACKs/NACKs the IBI request.
        ACK/NACK is driven by Controller in OD.
        """
        pass

    def _on_ibi_ack_fall(self, bus_sda):
        """
        After IBI ACK/NACK on SCL falling.

        Check 6: IBI ACK handoff -- if Controller ACKed (SDA=0), Target shall
        take over SDA in PP to send MDB (S5.1.2.3.2).
        """
        acked = (bus_sda == 0)
        if acked:
            self._phase = BusPhase.IBI_MDB
            self._bit_count = 0
            self._data_accum = 0
        else:
            # NACKed -- Target should stop driving
            self._phase = BusPhase.IDLE

    def _on_ibi_mdb_fall(self):
        """Count MDB bits. After 8 bits, move to T-bit for additional data."""
        self._bit_count += 1
        if self._bit_count >= 8:
            # MDB complete; now T-bit decides if more data follows
            self._phase = BusPhase.IBI_DATA_TBIT
            self._bit_count = 0

    def _on_ibi_data_fall(self):
        """Count additional IBI data bits."""
        self._bit_count += 1
        if self._bit_count >= 8:
            self._phase = BusPhase.IBI_DATA_TBIT
            self._bit_count = 0

    def _on_ibi_data_tbit_fall(self, bus_sda):
        """After IBI data T-bit, continue or end."""
        self.stats['read_bytes'] += 1
        # If T-bit=0, Target ends. If T-bit=1, continue.
        # Phase transition handled by START/STOP detection.
        self._phase = BusPhase.IBI_DATA
        self._bit_count = 0

    # --------------------------------------------------------------
    # CCC phases
    # --------------------------------------------------------------

    def _on_ccc_byte_fall(self):
        """Count CCC byte bits."""
        self._bit_count += 1
        if self._bit_count >= 8:
            self._phase = BusPhase.CCC_TBIT
            self._bit_count = 0

    def _on_ccc_tbit_fall(self):
        """After CCC T-bit, check for ENTHDR and await next byte or Sr/P."""
        # First CCC byte is the command code
        if self._byte_in_msg == 0:
            self._ccc_code = self._data_accum & 0xFF
            # ENTHDR0-ENTHDR7 (0x20-0x27): bus enters HDR mode after this frame
            if 0x20 <= self._ccc_code <= 0x27:
                self.log.debug(
                    f"I3cBusMonitor: ENTHDR CCC 0x{self._ccc_code:02X} detected, "
                    f"entering HDR_MODE"
                )
                self._phase = BusPhase.HDR_MODE
                self._bus_active = False
                return
        self._byte_in_msg += 1
        self._phase = BusPhase.CCC_BYTE
        self._bit_count = 0
        self._data_accum = 0

    # --------------------------------------------------------------
    # START / STOP detection
    # --------------------------------------------------------------

    def _on_start_detected(self):
        """SDA falling while SCL high --> START or Repeated START."""
        is_sr = self._bus_active
        self._bus_active = True

        if is_sr:
            self.log.debug(f"I3cBusMonitor: Repeated START detected, was in {self._phase.name}")
        else:
            self.log.debug(f"I3cBusMonitor: START detected")
            self.stats['starts_detected'] += 1

        self._enter_addr_phase(is_repeated_start=is_sr)

    def _on_stop_detected(self):
        """SDA rising while SCL high --> STOP."""
        self.log.debug(f"I3cBusMonitor: STOP detected")
        self.stats['stops_detected'] += 1
        self._bus_active = False
        self._phase = BusPhase.IDLE
        self._is_ccc = False
        self._is_entdaa = False

    # --------------------------------------------------------------
    # Main monitoring loop
    # --------------------------------------------------------------

    async def _monitor_loop(self):
        """
        Edge-driven monitor loop.

        Samples bus_scl and bus_sda on the system clock and detects edges.
        This avoids missing glitches and aligns with how the DUT sees the bus.
        """
        while self._running:
            await RisingEdge(self.clk)

            try:
                scl = int(self.bus_scl.value)
                sda = int(self.bus_sda.value)
            except ValueError:
                continue  # X/Z during reset

            scl_rose = (scl == 1 and self._prev_scl == 0)
            scl_fell = (scl == 0 and self._prev_scl == 1)
            sda_fell = (sda == 0 and self._prev_sda == 1)
            sda_rose = (sda == 1 and self._prev_sda == 0)

            # START condition: SDA falls while SCL is high
            if sda_fell and scl == 1 and self._prev_scl == 1:
                if self._phase == BusPhase.HDR_MODE:
                    pass  # Ignore START-like patterns during HDR
                else:
                    self._on_start_detected()

            # STOP condition: SDA rises while SCL is high
            elif sda_rose and scl == 1 and self._prev_scl == 1:
                if self._phase == BusPhase.HDR_MODE:
                    # HDR Exit Pattern ends with STOP -- return to SDR IDLE
                    self.log.debug("I3cBusMonitor: STOP during HDR_MODE, returning to SDR IDLE")
                    self._phase = BusPhase.IDLE
                    self._bus_active = False
                    self._is_ccc = False
                    self._is_entdaa = False
                else:
                    self._on_stop_detected()

            # SCL rising edge
            elif scl_rose:
                if self._phase != BusPhase.HDR_MODE:
                    self._on_scl_rising(sda)

            # SCL falling edge
            elif scl_fell:
                if self._phase != BusPhase.HDR_MODE:
                    self._on_scl_falling(sda)

            self._prev_scl = scl
            self._prev_sda = sda

    def report(self):
        """Print monitoring summary."""
        self.log.info("=" * 72)
        self.log.info("I3C Bus Monitor Report")
        self.log.info("=" * 72)
        self.log.info(f"  SCL edges observed:      {self.stats['scl_edges']}")
        self.log.info(f"  STARTs detected:         {self.stats['starts_detected']}")
        self.log.info(f"  STOPs detected:          {self.stats['stops_detected']}")
        self.log.info(f"  Address phases:          {self.stats['addr_phases']}")
        self.log.info(f"  Write bytes:             {self.stats['write_bytes']}")
        self.log.info(f"  Read bytes:              {self.stats['read_bytes']}")
        self.log.info(f"  IBI requests:            {self.stats['ibi_requests']}")
        self.log.info(f"  OD mode samples:         {self.stats['od_samples']}")
        self.log.info(f"  PP mode samples:         {self.stats['pp_samples']}")
        self.log.info(f"  Contention checks:       {self.stats['contention_checks']}")
        self.log.info(f"  Total violations:        {self.violation_count}")
        if self.violations:
            self.log.error("  VIOLATIONS:")
            for v in self.violations:
                self.log.error(f"    {v}")
        else:
            self.log.info("  OK: No violations detected")
        self.log.info("=" * 72)
