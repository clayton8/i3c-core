# Bug Report: GETSTATUS Sr abort prematurely clears Protocol Error

## Classification
**Design Bug** — RTL behavior violates the specification.

## Spec Reference
I3C Basic Spec §5.1.9.2.1: The Target shall only clear its Protocol Error status
after a successful GETSTATUS where the Controller reads all status bytes. If the
Controller aborts after reading only byte 0, the Target has no confirmation that
the error was delivered — the error must remain set.

## RTL Location
- **File**: src/ctrl/ccc.sv
- **Line(s)**: 1150-1153 (TxDataTbit Sr abort), 1271-1272 (get_status_done_o)
- **File**: src/ctrl/controller_standby.sv
- **Line(s)**: 286 (err_o clearing)
- **Module**: ccc, controller_standby

## Description
### Expected Behavior (per spec)
When Controller sends GETSTATUS and aborts after byte 0 with Sr, then STOP:
1. `get_status_done_o` shall NOT fire (GETSTATUS was not completed)
2. `err_o` shall remain 1 (Protocol Error not cleared)

### Actual Behavior (what RTL does)
1. In TxDataTbit (line 1150-1153): `bus_rstart_det_i` fires → `set_tx_data_complete = 1'b1`,
   `state_d = RxTargetAddr`
2. `tx_data_complete` gets set to 1 on next clock
3. CCC FSM goes to RxTargetAddr. If STOP fires before reaching TxTargetAddrAck
   (which would clear tx_data_complete via clear_tx_byte_num):
   - STOP override: state_d = DoneCCC
   - Next cycle: done_fsm_o = 1
   - `get_status_done_o = done_fsm_o && command_code_valid && GETSTATUS && tx_data_complete`
     = 1 && 1 && 1 && 1 = **1**
4. In controller_standby.sv:286: `if (get_status_done) err_o <= 1'b0` → **err_o cleared!**

### Root Cause Analysis
`set_tx_data_complete` on line 1153 fires on ANY Sr abort in TxDataTbit, regardless
of how many bytes were actually sent. It should only fire when `tx_data_last_byte`
is true (all bytes sent), which is already the condition on line 1157 for the
normal completion path.

## Suggested RTL Fix
```verilog
// BEFORE (buggy):
if (bus_rstart_det_i) begin
  // Controller abort: Target sent T=1 but Controller issued Sr
  state_d = RxTargetAddr;
  set_tx_data_complete = 1'b1;

// AFTER (fixed):
if (bus_rstart_det_i) begin
  // Controller abort: Target sent T=1 but Controller issued Sr
  state_d = RxTargetAddr;
  // Only mark complete if all bytes were sent (Controller read everything)
  set_tx_data_complete = tx_data_last_byte;
```

## Reproduction
- **Test**: `test_ccc_getstatus_sr_abort_clears_protocol_err` in test_ccc.py
- **Command**: `I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs make -C verification/cocotb/top/i3c_axi MODULE=test_ccc TESTCASE=test_ccc_getstatus_sr_abort_clears_protocol_err all`
- **Expected Result**: Test FAILS against current RTL. Test will PASS once the RTL fix is applied.

## Evidence
- set_tx_data_complete fires unconditionally on Sr abort (line 1153)
- tx_data_complete persists through RxTargetAddr → DoneCCC if STOP fires quickly
- get_status_done_o fires with tx_data_complete=1 even though only 1 of 2 bytes was sent
- err_o transitions from 1 to 0 despite Controller never receiving the Protocol Error byte
