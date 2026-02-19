# Bug Report: Sr during T-bit pushes unchecked byte, no RX descriptor

## Classification
**Design Bug** — RTL behavior violates the specification.

## Spec Reference
I3C Basic Spec §5.1.2.3.3: Same as stop_during_tbit.md — T-bit parity must be
verified before accepting a byte. A Repeated Start during the T-bit phase means
parity was never checked.

## RTL Location
- **File**: src/ctrl/i3c_target_fsm.sv
- **Line(s)**: 341 (rx_fifo_wvalid_raw), 387 (rx_last_byte_o), 686-688 (RxPWriteTbit Sr handling)
- **Module**: i3c_target_fsm

## Description
### Expected Behavior (per spec)
When Sr fires during the T-bit phase: same as STOP — byte not pushed, descriptor generated.

### Actual Behavior (what RTL does)
Same as stop_during_tbit.md. In RxPWriteTbit (line 686-688), `bus_rstart_det_i` sets
`state_d = RxFByte`. This causes `rx_fifo_wvalid_raw` to fire (state_d != RxPWriteTbit)
and `rx_last_byte_o` to not fire (state_q != RxPWriteData).

### Root Cause Analysis
Same root cause as stop_during_tbit.md. See that bug report for full analysis.

## Suggested RTL Fix
Same fix as stop_during_tbit.md.

## Reproduction
- **Test**: `test_priv_write_sr_during_tbit` in test_i3c_target.py
- **Command**: `I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs make -C verification/cocotb/top/i3c_axi MODULE=test_i3c_target TESTCASE=test_priv_write_sr_during_tbit all`
- **Expected Result**: Test FAILS against current RTL. Test will PASS once the RTL fix is applied.

## Evidence
Same signal-level behavior as stop_during_tbit.md with Sr instead of STOP.
