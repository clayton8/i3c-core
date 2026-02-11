// SPDX-License-Identifier: Apache-2.0

/*
  This module is responsible for handling the IBI descriptors.

  The descriptor is written to the TTI IBI queue by software. Optional IBI
  data follows immediately the descriptor in the same queue.

  The module watches the TTI IBI queue for descriptor write. Once a descriptor
  is in the module peeks it and waits until the defined count of data words is
  written to the queue. Finally, the module outputs MDB and the data as 8-bit
  words.

  TODO: The TTI IBI queue must be EMPTY each time a descriptor is written.
  This is because the module relies on absolute count of data words stored in
  it, not the distance between two consecutive descriptors.
*/
module descriptor_ibi #(
  parameter int unsigned TtiIbiDataWidth = 32,
  parameter int unsigned TtiIbiDataDepth = 32,
  parameter int unsigned IbiFifoWidth = 8
) (
  input  logic clk_i,
  input  logic rst_ni,

  // TTI: In-band-interrupt queue
  input  logic                       ibi_queue_rvalid_i,
  output logic                       ibi_queue_rready_o,
  input  logic [TtiIbiDataWidth-1:0] ibi_queue_rdata_i,
  input  logic [TtiIbiDataDepth-1:0] ibi_queue_depth_i,

  // Interface to/from target FSM
  output logic                    ibi_byte_valid_o,
  input  logic                    ibi_byte_ready_i,
  output logic [IbiFifoWidth-1:0] ibi_byte_o,
  output logic                    ibi_byte_last_o
);

  logic [7:0] data_mdb;
  logic [7:0] data_len;
  logic [7:0] data_words;
  logic [7:0] data_cnt;
  logic [7:0] data_byte;
  logic       queue_data_pop;
  logic       latch_descriptor;

  typedef enum logic [2:0] {
    Idle,
    DescLatch,
    DescPop,
    WriteMdb,
    WriteData
  } state_e;

  state_e state_q, state_d;

  // FSM
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q <= Idle;
    end else begin
      state_q <= state_d;
    end
  end


  // Capture IBI descriptor
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      data_mdb   <= '0;
      data_len   <= '0;
      data_words <= '0;
    end else if (latch_descriptor) begin
      data_mdb   <= ibi_queue_rdata_i[31:24];
      // -1 to compensate for comparison with data_cnt
      data_len   <= ibi_queue_rdata_i[7:0] - 1;
      // Divide by 4 and round up
      data_words <= 8'(ibi_queue_rdata_i[7:2] + |ibi_queue_rdata_i[1:0]);
    end
  end

  // Data counter
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      data_cnt <= '0;
    end else if (state_q == Idle) begin
      data_cnt <= '0;
    end else if (state_q == WriteData) begin
      if (ibi_queue_rvalid_i && ibi_byte_ready_i) data_cnt <= data_cnt + 1;
    end
  end

  always_comb begin
    ibi_byte_o       = '0;
    ibi_byte_valid_o = 1'b0;
    ibi_byte_last_o  = 1'b0;

    ibi_queue_rready_o = 1'b0;

    latch_descriptor = 1'b0;

    state_d = state_q;
    case (state_q)
      Idle: begin
        if (ibi_queue_rvalid_i) begin
          latch_descriptor = 1'b1;
          state_d = DescLatch;
        end
      end

      DescLatch: begin
        // Only proceed if enough data has been pushed to queue, including the descriptor
        if (ibi_queue_depth_i >= (data_words + 1)) begin
          state_d = DescPop;
        end
      end

      DescPop: begin
        ibi_queue_rready_o = 1'b1;
        state_d = WriteMdb;
      end

      WriteMdb: begin
        ibi_byte_o       = data_mdb;
        ibi_byte_valid_o = 1'b1;
        ibi_byte_last_o  = (data_len == 8'hFF); // No payload data

        if (ibi_byte_ready_i) begin
          // Back to Idle on no payload data
          state_d = (data_len == 8'hFF) ? Idle : WriteData;
        end
      end

      WriteData: begin
        ibi_byte_o       = data_byte;
        ibi_byte_valid_o = ibi_queue_rvalid_i;
        ibi_byte_last_o  = (data_len == data_cnt); // Last payload byte

        ibi_queue_rready_o = ibi_byte_ready_i && queue_data_pop;
        // Back to Idle when last byte read by target FSM
        if (ibi_byte_ready_i && (data_cnt == data_len)) begin
          state_d = Idle;
        end
      end
    endcase
  end

  // 32-bit to 8-bit conversion
  assign data_byte = ibi_queue_rdata_i[data_cnt[1:0]*8 +: 8];

  // Pop every 4 bytes and on the last byte
  assign queue_data_pop = (data_cnt[1:0] == 2'b11) || (data_cnt == data_len);

endmodule
