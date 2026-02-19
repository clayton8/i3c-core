# TB Bug: test_rxfbytearb_collision_blind_drive uses non-conforming controller

## Status: RESOLVED — Testbench bug fixed; test rewritten with arb-aware driving

## Summary
The test `test_rxfbytearb_collision_blind_drive` reports that the DUT
processes a collision-garbled address byte after IBI arbitration loss.
However, the garbled byte is an artifact of the test's non-conforming
**blind-driving** controller BFM, not a defect in the RTL. In a conforming
I3C system, the byte on the bus after DUT arbitration loss is always the
controller's (or winning target's) valid byte, and the DUT's
`RxFByte → CheckFByte → TxAckFByte` flow correctly processes it.

## Why the RTL is correct

In I3C open-drain arbitration, exactly one device loses at the first
bit where it drove 1 (released SDA) while the other drove 0 (pulled low).
After the DUT loses arbitration at bit N:

1. **Bits 7..N+1 (before arb loss):** Both devices agreed on every bit
   value (otherwise one would have lost earlier). Bus = controller's value.
2. **Bit N (arb-loss bit):** DUT drove 1 (high-Z), controller drove 0.
   Bus = 0 = controller's value.
3. **Bits N-1..0 (after arb loss):** DUT backs off (bus_tx_flow releases
   SDA within the same SCL period when req_valid drops). Bus = controller's
   value.

**Therefore, the bus byte after DUT arb loss IS the controller's valid byte**
in any conforming I3C system. The `RxFByte → CheckFByte` path correctly
checks this byte against the DUT's address and ACKs only if it matches.

### Proof with test addresses

The test uses DUT IBI byte 0xB5 ({0x5A, 1}) vs controller 0xFC ({0x7E, 0}):

```
Bit 7: DUT=1 CTRL=1 bus=1 → match
Bit 6: DUT=0 CTRL=1 bus=0 → CONTROLLER loses arb at bit 6
```

A conforming controller detects arb loss at bit 6, backs off, and handles
the DUT's IBI inline. The DUT **never** sees `arbitration_lost_i` in this
scenario — it wins arbitration because 0x5A < 0x7E.

The test's blind-driving BFM ignores its own arb loss at bit 6 and keeps
driving all 8 bits, creating the artificial garbled byte 0xB4 on the bus.

## Root cause: testbench non-conformance

`test_rxfbytearb_collision_blind_drive` uses `send_bit()` in a loop to
force all 8 bits of 0x7E/W onto the bus without checking for arbitration.
A conforming I3C controller uses arb-aware driving (`send_byte_arb` /
`send_bit_arb`) and backs off on the first mismatch, per I3C spec
§5.1.2.2.1: "If another Device has driven the SDA Low, then the Device
has 'lost' the Arbitration and shall not further participate in this
Address Header."

## Suggested fix

The test has been rewritten to use arb-aware driving via
`i3c_write(TARGET_ADDRESS, write_data, send_rsvd=False)`.  The controller
now detects its own arb loss at the RnW bit and handles the DUT's IBI
inline, matching the pattern in `test_ibi_arb_loss_rnw_bit`.  The DUT
genuinely loses arbitration on the RnW bit (drives 1, reads 0) and
correctly processes the controller's valid write.

## FSM transition log (from sim)

```
10207ns  Idle → RxFByteArb       ← START detected, DUT tries IBI
10805ns  RxFByteArb → RxFByte    ← arbitration_lost_i (from blind drive)
10808ns  RxFByte → CheckFByte    ← bus_rx_rsp.done: garbled byte processed
10811ns  CheckFByte → TxAckFByte ← garbled addr 0x5A matches DUT → ACK
10877ns  TxAckFByte → RxPWriteData ← phantom write begins
10889ns  RxPWriteData → Idle     ← STOP override
```

In a conforming system, the DUT would win arb (0x5A < 0x7E) and the
sequence would be: `Idle → RxFByteArb → IbiReadAck → ...`

## Reproduction
```
I3C_ROOT_DIR=$(pwd) CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl SIM=vcs TRACK_FSM= \
  make -C verification/cocotb/top/i3c_axi MODULE=test_ibi TESTCASE=test_rxfbytearb_collision_blind_drive all
```
