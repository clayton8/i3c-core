# Bug: TE0 error counter increments 2x per event

## Summary
`te0_err_o` in `i3c_target_fsm.sv` is level-sensitive — it stays high for 2+ cycles during HDR error-mode entry, causing the TE0 counter in `tti.sv` to increment by 2+ per single error event instead of 1.

## Root Cause
`te0_err_o` uses `last_addr_valid_o` (a registered signal that remains high until cleared by `in_hdr_mode` or bus events). The `in_hdr_mode` flop is set one cycle *after* `te0_err` fires, so `te0_err_o` stays asserted for at least 2 cycles.

```verilog
// BEFORE (level-sensitive, multi-cycle):
assign te0_err_o = te0_enable_i && last_addr_valid_o && is_te0_rsvd_addr_err(bus_addr_q, bus_rnw_q);
```

## Suggested Fix
Use `bus_addr_valid` (single-cycle pulse from the `always_comb` FSM) with the combinational `_d` signals instead of the registered `_q` signals:

```verilog
// AFTER (single-cycle pulse, consistent with all other TE errors):
assign te0_err_o = te0_enable_i && bus_addr_valid && is_te0_rsvd_addr_err(bus_addr_d, bus_rnw_d);
```

## Reproduction
```
I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs \
  make -C verification/cocotb/top/i3c_axi MODULE=test_te_errors TESTCASE=test_te_counter_per_event all
```
Test reads TE0 counter after a single error event and asserts `count == 1`. Fails against current RTL (reads 2+), passes with the fix.
