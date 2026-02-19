// SPDX-License-Identifier: Apache-2.0
//
// FSM state transition tracker for ccc.
//
// Logs every state_q transition with a timestamp to ccc_fsm_transitions.log.
// Enable with +define+TRACK_FSM_TRANSITIONS at compile time.
// Usage: make ... TRACK_FSM=1
//
// Output format (one line per transition):
//   <timestamp> <old_state_id> <new_state_id>
// Run verification/tools/parse_ccc_fsm_log.py to convert IDs to state names.

`ifndef SYNTHESIS
`ifndef VERILATOR

module ccc_fsm_tracker
  import i3c_pkg::*;
(
    input logic clk_i,
    input logic rst_ni
);

  // The bind statement places this module inside ccc's scope,
  // so state_q resolves to the parent's local signal via upward name reference.

`ifdef TRACK_FSM_TRANSITIONS
  logic [7:0] prev_state_trk;
  integer fsm_log_fd;

  initial begin
    fsm_log_fd = $fopen("ccc_fsm_transitions.log", "w");
    if (fsm_log_fd == 0) begin
      $display("ERROR [ccc_fsm_tracker] $fopen failed");
    end else begin
      $display("INFO [ccc_fsm_tracker] Opened ccc_fsm_transitions.log (fd=%0d)", fsm_log_fd);
    end
    $fwrite(fsm_log_fd, "# ccc state transition log\n");
    $fwrite(fsm_log_fd, "# timestamp old_state new_state\n");
  end

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      prev_state_trk <= 8'd0;
    end else if (state_q !== prev_state_trk) begin
      $fwrite(fsm_log_fd, "%0t %0d %0d\n", $time, prev_state_trk, state_q);
      prev_state_trk <= state_q;
    end
  end

  final begin
    $fclose(fsm_log_fd);
  end
`endif

endmodule : ccc_fsm_tracker

bind ccc ccc_fsm_tracker u_ccc_fsm_tracker (
    .clk_i  (clk_i),
    .rst_ni (rst_ni)
);

`endif // VERILATOR
`endif // SYNTHESIS
