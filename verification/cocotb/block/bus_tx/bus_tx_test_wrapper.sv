// SPDX-License-Identifier: Apache-2.0
module bus_tx_test_wrapper
  import i3c_pkg::*;
(
    input logic clk_i,
    input logic rst_ni,

    input scl_i,  // Additional signal for SCL bus mock

    // I3C bus timings
    input i3c_timeparam_t t_r_i,      // rise time of both SDA and SCL in clock units
    input logic [12:0] t_f_i,         // fall time (unused by bus_tx)
    input i3c_timeparam_t t_su_dat_i, // data setup time in clock units
    input i3c_timeparam_t t_hd_dat_i, // data hold time in clock units

    input logic drive_i,  // Driving the bus, it should never come later than (t_low-t_hd_dat) after
    // SCL falling edge if SCL is in stable LOW state
    input logic drive_value_i,  // Requested value to drive

    // Input I3C Bus events
    input logic scl_posedge_i,
    input logic scl_negedge_i,
    input logic scl_stable_high_i,
    input logic scl_stable_low_i,

    // Open Drain / Push Pull
    input logic sel_od_pp_i,

    output logic tx_idle_o,
    output logic tx_done_o,  // Indicate finished bit write

    output logic sel_od_pp_o,
    output logic sda_o  // Output I3C SDA bus line
);

  // sel_od_pp_o is unused by bus_tx but exposed for the testbench
  assign sel_od_pp_o = sel_od_pp_i;

  bus_tx xbus_tx (
    .clk_i,
    .rst_ni,
    .t_r_i,
    .t_su_dat_i,
    .t_hd_dat_i,
    .drive_i,
    .drive_value_i,
    .scl_negedge_i,
    .scl_posedge_i,
    .scl_stable_low_i,
    .tx_idle_o,
    .tx_done_o,
    .sda_o
  );
endmodule
