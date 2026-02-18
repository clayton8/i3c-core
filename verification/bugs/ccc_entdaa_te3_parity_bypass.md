# Bug Report: TE3 parity error detection always bypassed when enabled

## Classification
**Design Bug** — RTL behavior violates the specification.

## Spec Reference
I3C Spec §5.1.10.1.4 (Error Type TE3):

> If the Target detects a parity error in the PAR Bit of the Assigned Address during a Dynamic Address Arbitration procedure, then the Target shall generate NACK (after PAR) and then wait for another Repeated START and 7E/R to re-transmit the Provisioned ID.

## RTL Location
- **File**: `src/ctrl/ccc_entdaa.sv`
- **Line(s)**: 166
- **Module**: `ccc_entdaa`

## Description
### Expected Behavior (per spec)
When `te3_err_det_en_i = 1` (TE3 error detection enabled) and the controller sends an ENTDAA address byte with incorrect parity, the target shall detect the parity error and NACK the address.

### Actual Behavior (what RTL does)
When `te3_err_det_en_i = 1`, the `parity_ok` signal is unconditionally `True` regardless of whether the actual parity matches. The target ACKs the address even when the parity bit is wrong. TE3 error detection is completely non-functional when enabled.

### Root Cause Analysis
Line 166 uses `|| te3_err_det_en_i` as the bypass term:

```verilog
assign parity_ok = (~^bus_rx_rsp_i.data[7:1] == bus_rx_rsp_i.data[0]) || te3_err_det_en_i;
```

The `_en_i` suffix means "detection **enabled**". When enabled (`= 1`), the `||` operator short-circuits `parity_ok` to `True`, bypassing the actual parity check. The polarity is inverted — the bypass should activate when detection is **disabled** (`!te3_err_det_en_i`).

This is confirmed by comparing against the TE4 pattern at line 229, which is implemented correctly:
```verilog
if (reserved_word_det || !te4_err_det_en_i) begin
```
Here `!te4_err_det_en_i` correctly bypasses the check when detection is **disabled**.

## Suggested RTL Fix
```verilog
// BEFORE (buggy):
assign parity_ok = (~^bus_rx_rsp_i.data[7:1] == bus_rx_rsp_i.data[0]) || te3_err_det_en_i;

// AFTER (fixed):
assign parity_ok = (~^bus_rx_rsp_i.data[7:1] == bus_rx_rsp_i.data[0]) || !te3_err_det_en_i;
```

Single character change: add `!` before `te3_err_det_en_i`.

## Reproduction
- **Test**: `test_ccc_entdaa_te3_te4` in `verification/cocotb/top/lib_i3c_top/test_ccc.py`
- **Command**: `I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs make -C verification/cocotb/top/i3c_axi MODULE=test_ccc TESTCASE=test_ccc_entdaa_te3_te4 all`
- **Expected Result**: Test FAILS against current RTL. Test will PASS once the RTL fix is applied.

## Evidence
Test sends ENTDAA with `inject_te3_parity=True` (inverts the parity bit on the assigned address). With `te3_err_det_en_i=1`:

- **Expected**: Target NACKs the address (`results[0]["ack"] == False`)
- **Actual**: Target ACKs the address (`results[0]["ack"] == True`)

The assertion failure message:
```
TE3: Target should NACK address with bad parity, but ACKed.
DESIGN BUG: ccc_entdaa.sv:166 — parity_ok bypass polarity is inverted
(`|| te3_err_det_en_i` should be `|| !te3_err_det_en_i`).
```

TE3 error counter (`TARGET_ERR_CNT_TE3.CNT`) does not increment and `TE3_ERR_STAT` is not set, confirming the parity error is never detected.
