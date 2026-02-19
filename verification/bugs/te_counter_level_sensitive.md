# Bug Report: All TE/FRAMING error counters increment multiple times per event

## Classification
**Design Bug** — RTL behavior violates the specification.

## Spec Reference
HCI TTI §4.12.3: Each TARGET_ERR_CNT register shall increment by exactly 1
per error event, saturating at 0xFF.

## RTL Location
- **File**: src/hci/tti.sv
- **Line(s)**: 655–703
- **Module**: tti

## Description
### Expected Behavior (per spec)
A single error event (one TE0, TE1, TE2, TE3, TE4, TE5, or FRAMING error)
shall increment the corresponding TARGET_ERR_CNT register by exactly 1.

### Actual Behavior (what RTL does)
All counter write-enables in tti.sv are level-sensitive — they use the raw
error signal directly as the write-enable:

```verilog
assign hwif_tti_o.TARGET_ERR_CNT_TE0.CNT.we = te0_err_i && (value != 8'hFF);
assign hwif_tti_o.TARGET_ERR_CNT_TE1.CNT.we = te1_err_i && (value != 8'hFF);
assign hwif_tti_o.TARGET_ERR_CNT_TE2.CNT.we = te2_err_i && (value != 8'hFF);
// ... same pattern for TE3, TE4, TE5, FRAMING, RI_PEC, RI_LENGTH, etc.
```

When any `te_err` signal stays high for N cycles, the counter increments N
times per event instead of 1. This affects ALL counter types.

### Root Cause Analysis
**TE0 specifically**: `te0_err_o` uses `last_addr_valid_o` (registered signal
that remains high until `in_hdr_mode` is set one cycle later), so `te0_err_o`
stays asserted for at least 2 cycles.

**All other TE types**: The error signals are combinational and may stay high
for 1+ cycles depending on FSM state duration and downstream settling. The
counter WE architecture assumes pulse-mode errors, but the error sources are
level-mode.

## Suggested RTL Fix
Option A — Edge-detect each error input in tti.sv:

```verilog
// BEFORE (level-sensitive, multi-cycle):
assign hwif_tti_o.TARGET_ERR_CNT_TE0.CNT.we = te0_err_i && (value != 8'hFF);

// AFTER (edge-detected, single increment per event):
logic te0_err_q;
always_ff @(posedge clk_i or negedge rst_ni)
  if (!rst_ni) te0_err_q <= 1'b0;
  else         te0_err_q <= te0_err_i;
assign hwif_tti_o.TARGET_ERR_CNT_TE0.CNT.we =
    te0_err_i && !te0_err_q && (value != 8'hFF);
```

Option B — Fix the error sources to be single-cycle pulses (e.g., for TE0,
use `bus_addr_valid` instead of `last_addr_valid_o`).

## Reproduction
```
I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$CALIPTRA_ROOT SIM=vcs \
  make -C verification/cocotb/top/i3c_axi MODULE=test_te_errors TESTCASE=test_te_counter_per_event all
```
Test asserts `count == 1` after one TE0/TE1 event. Fails against current RTL
(reads 2+). Will PASS once the RTL fix is applied.

Additional tests that assert `count == 1` and are blocked by this bug:
- `test_te2_private_write_parity` (test_te_errors.py)
- `test_te_error_sequence_mixing` (test_te_errors.py)
- `test_ccc_setdasa_padding_err` (test_ccc.py — FRAMING counter)
- `test_ccc_te2_parity` (test_ccc.py — TE2 counter)
- `test_ccc_entdaa_te3_te4` (test_ccc.py — TE3, TE4 counters)

## Evidence
Confirmed failing tests and counter values (single error event → expected 1):
- `test_te2_private_write_parity`: TE2 counter = 13 (FAIL)
- `test_te_error_sequence_mixing`: TE2 counter = 18 (FAIL)
- `test_ccc_entdaa_te3_te4`: TE3 counter = 2 (FAIL)
- `test_te_counter_per_event`: TE0 counter = 2+ (FAIL)

Confirmed passing (error signal is already single-cycle pulse):
- `test_ccc_setdasa_padding_err`: FRAMING counter = 1 (PASS)
- `test_ccc_te2_parity`: CCC-TE2 counter = 1 (PASS)
- `test_ccc_entdaa_te3_te4`: TE4 counter = 1 (PASS)

Multi-cycle error signals confirmed: TE0 (te0_err_o), TE2 (te2_err for
private write path), TE3 (te3_err). The CCC-path TE2 and TE4 errors produce
single-cycle pulses and are not affected.
