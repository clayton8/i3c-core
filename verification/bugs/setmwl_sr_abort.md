# Bug Report: SET CCC (SETMWL) Sr abort — CCC FSM misinterprets post-Sr data

## Classification
**NOT A BUG** — RTL handles partial SETMWL correctly. CSR data commit is gated by
byte completion, so partial data does not corrupt MWL.

## Original Analysis (DISPROVEN by testing)
The original concern was that the CCC FSM has no `bus_rstart_det_i` handling in
RxData/RxDataTbit states, and post-Sr address bytes might be interpreted as CCC data,
corrupting the MWL CSR.

## Test Result
`test_ccc_setmwl_sr_abort_during_data` **PASSED**:
- MWL was NOT corrupted after aborted SETMWL (sent byte 0, aborted byte 1 with Sr+STOP)
- Recovery SETMWL correctly updated MWL to the new value
- Target still responded to GETBCR after recovery

## Explanation
While the CCC FSM does stay in RxData after Sr (the FSM logic lacks Sr handling),
the SETMWL data commit (`set_mwl`) is gated by the completion of ALL required
data bytes. Since byte 1 never completes (STOP fires before bus_rx_flow delivers it),
the commit doesn't happen and MWL is not corrupted. The STOP override at ccc.sv:1207
eventually sends the FSM to DoneCCC, which cleans up state.
