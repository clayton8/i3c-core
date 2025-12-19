/*
SPDX-License-Identifier: Apache-2.0

This module is supposed to control the data flow on the I3C bus. External modules can
assert following requests to drive the bus:
- send data byte,
- send tbit/ACK/NACK.

In order to request a transfer, assert `req_byte_i` or `req_bit_i` and set the requested value
`req_value_i`. If request is single bit, the LSB of `req_value_i` will be transferred. Request
signals should be asserted until `bus_tx_done_o` is not asserted. Then request should be either
deasserted or immediately configured for new transfer.

Notes:
* The `bus_tx_done_o` is single pulse indicator for finished transfers.
* Asserting both `req_byte_i` and `req_bit_i` will cause an error assertion on `req_error_o`
* The `abort_i` cancels request and releases the bus immediately
* Before asserting a request, ensure `bus_tx_idle_o` is HIGH

*/

module bus_tx_flow import i3c_pkg::*; (
  input  logic clk_i,
  input  logic rst_ni,

  // I3C bus timings
  input  i3c_timeparam_t t_r_i,      // rise time of both SDA and SCL in clock units
  input  i3c_timeparam_t t_su_dat_i, // data setup time in clock units
  input  i3c_timeparam_t t_hd_dat_i, // data hold time in clock units

  // Input I3C Bus events
  input  logic scl_negedge_i,
  input  logic scl_posedge_i,
  input  logic scl_stable_low_i,

  // Tx request and data
  input  logic      req_byte_i,
  input  logic      req_bit_i,
  input  i3c_byte_t req_value_i,

  // Bus flow control and errors
  output logic bus_tx_done_o,
  output logic bus_tx_idle_o,
  output logic req_error_o,
  output logic bus_error_o,

  // Open Drain / Push Pull
  input  logic sel_od_pp_i,
  output logic sel_od_pp_o,

  // Output I3C SDA bus line
  output logic sda_o
);

  // Signals
  logic       drive_bit_en;
  logic       drive_bit_value;
  logic       bit_counter_en;
  logic [3:0] bit_counter_q, bit_counter_d;

  logic [1:0] reqs;
  logic       req_any;
  i3c_byte_t  req_value_q, req_value_d; // TODO rename req_data ?

  logic tx_idle;
  logic tx_done; // Indicates finished bit write
  logic req_error, bus_error, errorPany;

  typedef enum logic [2:0] {
    Idle,
    DriveByte,
    DriveBit,
    NextTaskDecision
  } tx_state_e;

  tx_state_e state_d, state_q;


  assign reqs    = {req_byte_i, req_bit_i};
  assign req_any = |reqs;
  // Clever way to ensure that only one bit is HIGH
  // Source: https://stackoverflow.com/a/11235598
  // It might be optimized if we're sure there are only 2 requests at most
  assign req_error = ~(~|(reqs & (reqs - 1)));

  // TODO: Connect to bus_tx module error output signal
  assign bus_error = '0;
  assign error = req_error | bus_error;

  always_comb begin
    bit_counter_d = bit_counter_q;
    req_value_d   = req_value_q;

    if (bit_counter_en) begin
      if (tx_done) begin
        bit_counter_d = (bit_counter_q == 4'd0) ? 4'd7 : bit_counter_q - 1;
        req_value_d   = {req_value_q[6:0], 1'b0}; // shift left
      end
    end else begin
      bit_counter_d = 4'd7;
      req_value_d   = (bit_counter_q == 4'd7) ? req_value_i : '0;
    end
  end

  always_comb begin : tx_fsm
    bus_tx_idle_o = '0;
    bus_tx_done_o = '0;
    drive_bit_en = '0;
    drive_bit_value = 1'b1; // Pullup by default
    bit_counter_en = '0;

    state_d = state_q;
    unique case (state_q)
      Idle: begin
        bus_tx_idle_o = tx_idle;
        drive_bit_en  = tx_idle ? req_any : 1'b0;
        drive_bit_value = req_byte_i ? req_value_i[7] : req_value_i[0];

        if (tx_idle && req_byte_i) begin
          state_d = DriveByte;
        end else if (tx_idle && req_bit_i) begin
          state_d = DriveBit;
        end
      end
      DriveByte: begin
        bit_counter_en = 1'b1;
        drive_bit_en = req_any;
        drive_bit_value = req_value_q[7];
        if ((bit_counter_q == 4'd0) && tx_done) begin
          bus_tx_done_o = 1'b1;
          state_d = NextTaskDecision;
        end
      end
      DriveBit: begin
        drive_bit_value = req_value_q[0];
        drive_bit_en = req_any;
        if (tx_done) begin
          bus_tx_done_o = 1'b1;
          state_d = NextTaskDecision;
        end
      end
      NextTaskDecision: begin
        drive_bit_en = req_any;
        drive_bit_value = req_value_i[0];

        if (req_byte_i) begin
          state_d = DriveByte;
        end else if (req_bit_i) begin
          state_d = DriveBit;
        end else begin
          state_d = Idle;
        end
      end
      default: ;
    endcase

    // Allow to abort and go back to Idle if needed
    if (~req_any | error) begin
      state_d = Idle;
    end
  end

  bus_tx xbus_tx (
    .clk_i,
    .rst_ni,
    .t_r_i,
    .t_su_dat_i,
    .t_hd_dat_i,
    .drive_i(drive_bit_en),
    .drive_value_i(drive_bit_value),
    .scl_negedge_i,
    .scl_posedge_i,
    .scl_stable_low_i,
    .tx_idle_o(tx_idle),
    .tx_done_o(tx_done),
    .sda_o
  );

  assign req_error_o = req_error;
  assign bus_error_o = bus_error;
  assign sel_od_pp_o = sel_od_pp_i; // Feedthrough for now

  // Sequential process for all flops
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (~rst_ni) begin
      bit_counter_q <= '0;
      req_value_q   <= '0;
      state_q       <= Idle;
    end else begin
      bit_counter_q <= bit_counter_d;
      req_value_q   <= req_value_d;
      state_q       <= state_d;
    end
  end

endmodule
