# Bug Report: TE2/TE3 error counters increment multiple times per event

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
A single error event shall increment the corresponding TARGET_ERR_CNT
register by exactly 1.

### Actual Behavior (what RTL does)
All counter write-enables in tti.sv are level-sensitive — they use the raw
error signal directly as the write-enable:

```verilog
assign hwif_tti_o.TARGET_ERR_CNT_TE2.CNT.we = te2_err_i && (value != 8'hFF);
assign hwif_tti_o.TARGET_ERR_CNT_TE3.CNT.we = te3_err_i && (value != 8'hFF);
// ... same pattern for all counter types
```

When an error signal stays high for N cycles, the counter increments N times
per event instead of 1.

### Root Cause Analysis
The counter WE architecture assumes single-cycle pulse error inputs, but some
error sources produce multi-cycle signals:

- **TE2 (private write parity)**: `te2_err` stays high for the duration of the
  FSM state that detected the parity error (observed 24 cycles in test).
- **TE3 (ENTDAA parity)**: `te3_err` stays high for 2 cycles.

### Partially Fixed (commit a7123668)
**TE0** was fixed by changing the error source from `last_addr_valid_o`
(registered, multi-cycle) to `bus_addr_valid` (single-cycle combinational
pulse). After this fix, TE0 and TE1 counters now increment correctly (== 1).

### Still Affected
TE2 (private write path) and TE3 (ENTDAA path) error signals are still
multi-cycle. The CCC-path TE2, TE4, FRAMING, and TE5 errors already produce
single-cycle pulses and are not affected.

## Suggested RTL Fix
Option A — Edge-detect affected error inputs in tti.sv:

```verilog
// BEFORE (level-sensitive, multi-cycle):
assign hwif_tti_o.TARGET_ERR_CNT_TE2.CNT.we = te2_err_i && (value != 8'hFF);

// AFTER (edge-detected, single increment per event):
logic te2_err_q;
always_ff @(posedge clk_i or negedge rst_ni)
  if (!rst_ni) te2_err_q <= 1'b0;
  else         te2_err_q <= te2_err_i;
assign hwif_tti_o.TARGET_ERR_CNT_TE2.CNT.we =
    te2_err_i && !te2_err_q && (value != 8'hFF);
```

Option B — Fix the TE2/TE3 error sources to be single-cycle pulses, matching
the pattern used for the TE0 fix (commit a7123668).

## Reproduction
```
I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs \
  make -C verification/cocotb/top/i3c_axi MODULE=test_te_errors TESTCASE=test_te2_private_write_parity all
```

Tests that assert `count == 1` and are **still blocked** by this bug:
- `test_te2_private_write_parity` (test_te_errors.py) — TE2 counter
- `test_te_error_sequence_mixing` (test_te_errors.py) — TE2 counter
- `test_ccc_entdaa_te3_te4` (test_ccc.py) — TE3 counter

Tests that now **PASS** (error source fixed or already single-cycle):
- `test_te_counter_per_event` (test_te_errors.py) — TE0, TE1 counters
- `test_ccc_setdasa_padding_err` (test_ccc.py) — FRAMING counter
- `test_ccc_te2_parity` (test_ccc.py) — CCC-path TE2 counter
- `test_ccc_entdaa_te3_te4` (test_ccc.py) — TE4 counter

## Evidence
Confirmed failing tests and counter values (single error event → expected 1):
- `test_te2_private_write_parity`: TE2 counter = 24 (FAIL)
- `test_te_error_sequence_mixing`: TE2 counter = 13 (FAIL)
- `test_ccc_entdaa_te3_te4`: TE3 counter = 2 (FAIL)

Confirmed passing (error signal is already a single-cycle pulse):
- `test_te_counter_per_event`: TE0 counter = 1, TE1 counter = 1 (PASS)
- `test_ccc_setdasa_padding_err`: FRAMING counter = 1 (PASS)
- `test_ccc_te2_parity`: CCC-TE2 counter = 1 (PASS)
- `test_ccc_entdaa_te3_te4`: TE4 counter = 1 (PASS)
