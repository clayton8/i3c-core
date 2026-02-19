# Bug Report: STOP during T-bit pushes unchecked byte, no RX descriptor

## Classification
**Design Bug** — RTL behavior violates the specification.

## Spec Reference
I3C Basic Spec §5.1.2.3.3: The Target shall verify T-bit parity before accepting
a data byte. If a bus condition (STOP/Sr) occurs before the T-bit completes,
the byte has not been verified and shall not be pushed to the receive queue.

## RTL Location
- **File**: src/ctrl/i3c_target_fsm.sv
- **Line(s)**: 341 (rx_fifo_wvalid_raw), 387 (rx_last_byte_o)
- **Module**: i3c_target_fsm

## Description
### Expected Behavior (per spec)
When STOP fires during the T-bit phase (state_q == RxPWriteTbit):
1. The incomplete byte shall NOT be pushed to the RX queue (T-bit parity not verified)
2. An RX descriptor shall be generated with byte_count = number of previously completed bytes
3. The byte_counter in descriptor_rx shall be reset for the next transfer

### Actual Behavior (what RTL does)
1. `rx_fifo_wvalid_raw` fires: `(state_q == RxPWriteTbit) && (state_d != RxPWriteTbit)` is TRUE
   because the STOP override sets `state_d = Idle`, which != RxPWriteTbit. The te2_err_priv_wr
   check passes (stays 0) because bus_rx_rsp_i.done never fired to perform parity verification.
   → **Byte is pushed without parity check.**
2. `rx_last_byte_o` does NOT fire: `(state_q == RxPWriteData)` is FALSE because state_q is
   RxPWriteTbit. → **No descriptor generated. No queue flush.**
3. `byte_counter` in descriptor_rx is not reset → **stale counter corrupts next transfer.**

### Root Cause Analysis
`rx_fifo_wvalid_raw` (line 341) treats any exit from RxPWriteTbit as a successful byte
completion. It should also check that the exit was caused by bus_rx_rsp_i.done (T-bit
actually received) rather than a STOP/Sr override.

`rx_last_byte_o` (line 387) only checks `state_q == RxPWriteData`. It should also fire
when leaving RxPWriteTbit due to STOP/Sr, to generate the descriptor for completed bytes.

## Suggested RTL Fix
```verilog
// BEFORE (buggy):
assign rx_fifo_wvalid_raw = (state_q == RxPWriteTbit) && (state_d != RxPWriteTbit) &&
                            !(te2_err_priv_wr || parity_err);

assign rx_last_byte_o = (state_q == RxPWriteData) && (state_d inside {RxFByte, Idle});

// AFTER (fixed):
// Only push byte when T-bit was actually received (bus_rx_rsp_i.done fired)
assign rx_fifo_wvalid_raw = (state_q == RxPWriteTbit) && bus_rx_rsp_i.done &&
                            !(te2_err_priv_wr || parity_err);

// Also generate descriptor when leaving RxPWriteTbit due to STOP/Sr
assign rx_last_byte_o = ((state_q == RxPWriteData) || (state_q == RxPWriteTbit)) &&
                        (state_d inside {RxFByte, Idle});
```

## Reproduction
- **Test**: `test_priv_write_stop_during_tbit` in test_i3c_target.py
- **Command**: `I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs make -C verification/cocotb/top/i3c_axi MODULE=test_i3c_target TESTCASE=test_priv_write_stop_during_tbit all`
- **Expected Result**: Test FAILS against current RTL. Test will PASS once the RTL fix is applied.

## Evidence
- rx_fifo_wvalid_raw fires when state_q=RxPWriteTbit and STOP override sets state_d=Idle
- rx_last_byte_o remains 0 because state_q != RxPWriteData
- No RX descriptor is generated; byte_counter carries stale value to next transfer
