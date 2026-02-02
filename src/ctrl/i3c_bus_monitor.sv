// Copyright lowRISC contributors (OpenTitan project).
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0
//

/*
I3C bus monitor. Detects HDR exit pattern and reset pattern

HDR Exit Pattern (per I3C spec 5.2.1.1.1):
  - SCL held low continuously
  - 4 SDA falling edges while SCL is low
  - Then STOP condition (SCL high, SDA rising)

The spec reference implementation uses SDA negedge as clock and SCL high as reset.
This is the equivalent oversampled implementation.
*/
module i3c_bus_monitor
  import i3c_pkg::*;
(
    input logic clk_i,
    input logic rst_ni,

    input logic enable_i,

    // Bus state
    bus_state_t bus_i,

    input logic is_in_hdr_mode_i,  // Module is in HDR mode
    output logic hdr_exit_detect_o,     // Detected HDR exit condition (see: 5.2.1.1.1 of the base spec)
    output logic target_reset_detect_o  // Detected Target Reset condtition
);
  // HDR exit pattern detection
  // Equivalent to spec: SCL high resets counter, SDA negedge increments
  // After 4 SDA negedges while SCL stays low, pattern is complete
  logic [3:0] hdr_exit_stp_cnt;

  // Oversampled equivalent of spec logic:
  // - Reset when: not in HDR mode, SCL goes stable high, or disabled
  // - Shift in 1 on each SDA negedge while SCL is low
  always_ff @(posedge clk_i or negedge rst_ni) begin:w
    
    if (!rst_ni) begin
      hdr_exit_stp_cnt <= '0;
    end else if (!enable_i || !is_in_hdr_mode_i || bus_i.scl.stable_high) begin
      // Equivalent to scl_rst_n = ~iSCL & iIsInHDR
      // SCL stable high (or not in HDR mode) resets the counter
      hdr_exit_stp_cnt <= '0;
    end else if (bus_i.sda.neg_edge) begin
      // Equivalent to posedge SDA_clk_n (SDA falling edge)
      // Shift chain counter: shift in 1 from LSB
      hdr_exit_stp_cnt <= {hdr_exit_stp_cnt[2:0], 1'b1};
    end
  end

  // HDR exit detected when counter reaches 4 (stp_cnt[3] = 1)
  // This indicates 4 SDA negedges occurred while SCL was continuously low
  assign hdr_exit_detect_o = hdr_exit_stp_cnt[3] ;

  target_reset_detector target_reset_detector (
      .clk_i,
      .rst_ni,
      .enable_i,
      .bus_i,
      .target_reset_detect_o
  );

endmodule
