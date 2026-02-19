# Bug Report: Late ibi_pending in RxFByteArb causes shifted IBI address

## Classification
**Design Bug** — RTL behavior violates the specification.

## Spec Reference
**I3C Spec §5.1.2.2.1 (I3C Address Arbitration):**

> An Address Header following a START (but not a Repeated START) is subject to Arbitration, meaning both the Controller and one or more Targets may attempt to drive an Address onto the Bus, using SDA.

Arbitration is defined bit-by-bit starting at bit 7 of the Address Header. All participating Devices start driving on the falling edge of SCL after START. A Device that joins arbitration mid-byte (after some bits have already been clocked) violates the protocol because the bus has already committed those earlier bit positions — re-driving them from a different starting offset produces garbled data.

**I3C Spec §5.1.6.2 (I3C Target Interrupt Request):**

> In order to request an interrupt, an I3C Target shall emit its Address into the arbitrated Address header following a START.

The IBI address must be emitted *from the beginning* of the arbitrated Address Header, not from an arbitrary mid-byte position.

## RTL Location
- **File**: `src/ctrl/i3c_target_fsm.sv`
- **Line(s)**: 573-589
- **Module**: `i3c_target_fsm`

Also involves:
- **File**: `src/ctrl/descriptor_ibi.sv`
- **Line(s)**: 97-99 (`ibi_byte_valid_o` asserted in `WriteMdb`)
- **Module**: `descriptor_ibi`

## Description

### Expected Behavior (per spec)

When the target FSM enters `RxFByteArb` after a START condition, the `ibi_pending` signal should be sampled at the beginning of the byte (when arbitration begins). If `ibi_pending` is low at that point, the DUT should receive the address byte passively — it should NOT begin driving an IBI address partway through the byte even if `ibi_pending` rises later during the byte reception.

An IBI queued via CSR while the address byte is already in progress should be deferred until the next Bus Available condition.

### Actual Behavior (what RTL does)

The `ibi_pending` signal is purely combinational:

```verilog
assign ibi_pending = ibi_byte_valid_i && ibi_enable_i && target_ibi_addr_valid_i;
```

In `RxFByteArb`, the IBI address drive is gated by `ibi_pending` on every cycle:

```verilog
RxFByteArb: begin
    bus_rx_req_byte = !bus_rstart_det_i;
    if (ibi_pending && ibi_can_retry) begin
        bus_tx_req_o.req_valid  = 1'b1;
        bus_tx_req_o.req_type   = RawByte;
        bus_tx_req_o.drive_type = OpenDrain;
        bus_tx_req_o.data       = {target_ibi_addr_i, 1'b1};
    end
    ...
end
```

If firmware writes an IBI descriptor to the TTI IBI queue while the target FSM is already in `RxFByteArb` and some address bits have been clocked, `descriptor_ibi` processes the descriptor (Idle → DescLatch → DescPop → WriteMdb in ~3 system clocks). In `WriteMdb`, `ibi_byte_valid_o` goes high, causing `ibi_pending` to rise mid-byte.

The FSM then asserts `bus_tx_req_o` with the IBI address. `bus_tx_flow` starts transmitting the IBI byte from bit 7, but SCL has already advanced past bit 7. The IBI address bits are driven at the wrong positions on SDA ("shifted"), producing garbled data on the bus.

The DUT proceeds through `IbiReadAck` → `IbiSendData` based on shifted/garbled arbitration results. The DUT then gets stuck in `IbiSendData` (driving push-pull on SDA) and cannot detect the controller's STOP condition.

### Root Cause Analysis

`RxFByteArb` re-evaluates `ibi_pending` on every combinational cycle. There is no latch or guard to ensure `ibi_pending` was true at the *start* of the byte (when arbitration begins at bit 7). If `ibi_pending` rises after bit N has been clocked (where N < 7), the DUT starts driving its IBI address from bit 7 while the bus is at bit N-1, producing a bit-position mismatch.

At 333 MHz system clock / 12.5 MHz bus clock, each bus bit period is ~27 system clocks. The `descriptor_ibi` pipeline (Idle → WriteMdb) takes ~3 system clocks. This means a CSR write during bit 4 can cause `ibi_pending` to rise before bit 3 is clocked — well within the same byte.

## Suggested RTL Fix

Latch `ibi_pending` at byte-boundary entry to `RxFByteArb`, so mid-byte changes are ignored:

```verilog
// BEFORE (buggy):
// In RxFByteArb, ibi_pending is checked combinationally every cycle:
RxFByteArb: begin
    bus_rx_req_byte = !bus_rstart_det_i;
    if (ibi_pending && ibi_can_retry) begin
        bus_tx_req_o.req_valid  = 1'b1;
        ...
    end
end

// AFTER (fixed):
// Add a registered signal that latches ibi_pending on entry to RxFByteArb:
// (in the sequential always_ff block)
logic ibi_pending_at_arb_start;
always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
        ibi_pending_at_arb_start <= 1'b0;
    end else if (state_d == RxFByteArb && state_q != RxFByteArb) begin
        // Latch on entry to RxFByteArb
        ibi_pending_at_arb_start <= ibi_pending;
    end
end

// In the combinational block, use the latched value:
RxFByteArb: begin
    bus_rx_req_byte = !bus_rstart_det_i;
    if (ibi_pending_at_arb_start && ibi_can_retry) begin
        bus_tx_req_o.req_valid  = 1'b1;
        bus_tx_req_o.req_type   = RawByte;
        bus_tx_req_o.drive_type = OpenDrain;
        bus_tx_req_o.data       = {target_ibi_addr_i, 1'b1};
    end
    ...
end
```

## Reproduction
- **Test**: `test_ibi_late_pending_rxfbytearb_shifted_addr` in `test_ibi.py`
- **Command**:
  ```
  I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs \
    make -C verification/cocotb/top/i3c_axi MODULE=test_ibi \
    TESTCASE=test_ibi_late_pending_rxfbytearb_shifted_addr all
  ```
- **Expected Result**: Test FAILS against current RTL. Test will PASS once the RTL fix is applied.

## Evidence
- Target FSM state after STOP: **22 (IbiSendData)** — should be 0 (Idle)
- DUT entered IBI flow (`IbiReadAck` → `IbiSendData`) during the shifted address byte
- Controller's VIP logged garbled address `0x7C` instead of expected `0xFC` (0x7E/W), confirming collision from shifted IBI bits
- DUT gets stuck in `IbiSendData` driving push-pull on SDA, preventing STOP detection
