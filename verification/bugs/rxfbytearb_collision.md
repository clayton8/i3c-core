# Bug: RxFByteArb processes collision-garbled address on simultaneous arb loss + byte done

## Summary
In `RxFByteArb` (i3c_target_fsm.sv:573-601), when `arbitration_lost_i` and
`bus_rx_rsp_i.done` fire on the same cycle (arbitration loss detected at bit 0),
the `bus_rx_rsp_i.done` assignment (`state_d = CheckFByte`) overrides the
`arbitration_lost_i` assignment (`state_d = RxFByte`). The DUT then processes
the collision-garbled address byte as a valid transaction.

When the DUT's IBI address collides with the controller's reserved byte (0x7E/W),
the open-drain AND produces a byte that may coincidentally match the DUT's own
dynamic address, causing a phantom write and subsequent TE2 parity error.

## Root Cause
The two `state_d` assignments in `RxFByteArb` are in separate `if` blocks with
no priority guard:

```verilog
// i3c_target_fsm.sv:584-587 — arb loss handler
if (arbitration_lost_i) begin
    ibi_status_we_o = 1'b1;
    ibi_status_o    = IbiFailureAddressArb;
    state_d = RxFByte;                    // (A) intent: continue receiving passively
end

// i3c_target_fsm.sv:591-600 — byte receive handler
if (bus_tx_rsp_i.done && !arbitration_lost_i) begin
    state_d = IbiReadAck;
end else if (bus_rx_rsp_i.done) begin     // (C) NO !arbitration_lost_i guard
    bus_addr_valid = 1'b1;
    bus_addr_d     = bus_rx_rsp_i.data[7:1];
    bus_rnw_d      = bus_rx_rsp_i.data[0];
    state_d = CheckFByte;                 // overrides (A) when both fire
end
```

When arb loss occurs at bit 0 (the last bit), `bus_rx_rsp_i.done` fires
simultaneously and (C) overwrites (A).

### Collision example (TARGET_ADDRESS = 0x5A):
- DUT IBI byte:       0xB5 = {0x5A, 1}
- Controller 0x7E/W:  0xFC = {0x7E, 0}
- Open-drain bus:      0xB4 = 0xFC & 0xB5 = {0x5A, 0}

The collision byte 0xB4 has addr=0x5A (matching the DUT) and RnW=0 (Write).
The DUT proceeds to ACK and enters `RxPWriteData` for a transaction that does
not actually exist, while the controller handles the IBI inline and retries.

## Suggested Fix
Add `!arbitration_lost_i` guard to the `bus_rx_rsp_i.done` path:

```verilog
if (bus_tx_rsp_i.done && !arbitration_lost_i) begin
    state_d = IbiReadAck;
end else if (bus_rx_rsp_i.done && !arbitration_lost_i) begin
    bus_addr_valid = 1'b1;
    bus_addr_d     = bus_rx_rsp_i.data[7:1];
    bus_rnw_d      = bus_rx_rsp_i.data[0];
    state_d = CheckFByte;
end
```

**Note:** This fix would also affect `test_ibi_arb_loss_rnw_bit` (Test 14),
which currently relies on the DUT processing the collision byte when the
DUT and controller target the same 7-bit address with different RnW bits.
That test's expectation may need to be re-evaluated against the I3C spec
§5.1.6.2: "If the Target's address is not seen on the Bus (arbitration was
lost), the Target shall wait for the Controller to issue the next START
condition."

## Reproduction
The RTL bug is confirmed by code inspection: `i3c_target_fsm.sv` RxFByteArb
state still lacks the `!arbitration_lost_i` guard on the `bus_rx_rsp_i.done`
path (lines ~591-600).

The original reproducing test (`test_ibi_refuse_no_retry_on_rstart`) now
**PASSES** because a testbench workaround was added: IBI is disabled via CSR
before the private write to prevent the collision, then re-enabled after the
write completes. This avoids triggering the bug but does NOT fix it.

```
I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs \
  make -C verification/cocotb/top/i3c_axi MODULE=test_ibi TESTCASE=test_ibi_refuse_no_retry_on_rstart all
```

A direct reproduction requires the IBI workaround to be removed, allowing
the DUT to re-arbitrate IBI during the controller's START + 0x7E/W phase.

## Workaround
Testbench disables IBI in the DUT via CSR before the private write to prevent
the collision, then re-enables after the write completes. This is applied in
`test_ibi_refuse_no_retry_on_rstart`.
