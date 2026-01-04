module ccc_entdaa
  import controller_pkg::*;
  import i3c_pkg::*;
(
  input  logic clk_i,  // Clock
  input  logic rst_ni, // Async reset, active low

  input  logic [47:0] id_i,
  input  logic  [7:0] dcr_i,
  input  logic  [7:0] bcr_i,

  input  logic [47:0] virtual_id_i,
  input  logic  [7:0] virtual_dcr_i,
  input  logic  [7:0] virtual_bcr_i,

  input  logic start_daa_i,
  output logic done_daa_o,

  input  logic process_virtual_i,

  // Bus Rx interface
  output bus_rx_req_t bus_rx_req_o,
  input  bus_rx_rsp_t bus_rx_rsp_i,

  // Bus Tx interface
  output bus_tx_req_t bus_tx_req_o,
  input  bus_tx_rsp_t bus_tx_rsp_i,

  // Bus Monitor interface
  input  logic bus_rstart_det_i,
  input  logic bus_stop_det_i,

  // bus access
  input  logic arbitration_lost_i,

  // addr
  output logic [6:0] address_o,
  output logic       address_valid_o
);


  typedef enum logic [7:0] {
    Idle = 'h0,
    WaitStart = 'h1,
    ReceiveRsvdByte = 'h2,
    AckRsvdByte = 'h3,
    SendNack = 'h4,
    SendID = 'h5,
    PrepareIDBit = 'h6,
    SendIDBit = 'h7,
    LostArbitration = 'h8,
    ReceiveAddr = 'h9,
    AckAddr = 'ha,
    Done = 'hb,
    Error = 'hc
  } state_e;

  state_e state_q, state_d;

  logic [6:0] id_bit_count;
  logic       load_id_counter, tick_id_counter;

  logic reserved_word_det;
  logic parity_ok;

  logic [63:0] device_id;

  assign reserved_word_det = (bus_rx_rsp_i.data == {`I3C_RSVD_ADDR, 1'b1});

  assign device_id = process_virtual_i ? {virtual_id_i, virtual_bcr_i, virtual_dcr_i} :
                                         {id_i, bcr_i, dcr_i};

  assign parity_ok = (~^bus_rx_rsp_i.data[7:1] == bus_rx_rsp_i.data[0]);

  assign address_o = bus_rx_rsp_i.data[7:1];

  always_ff @(posedge clk_i or negedge rst_ni) begin: id_bit_counter
    if (!rst_ni) begin
      id_bit_count <= '0;
    end else begin
      if (load_id_counter) begin
        id_bit_count <= 7'd64;
      end else if (tick_id_counter) begin
        id_bit_count <= id_bit_count - 1'b1;
      end else begin
        id_bit_count <= id_bit_count;
      end
    end
  end

  i3c_byte_t bus_tx_data;

  assign bus_rx_req_o = '{
    req_bit:  1'b0,
    req_byte: (state_q inside {ReceiveRsvdByte, ReceiveAddr})
  };

  assign bus_tx_req_o = '{
    drive_type: OpenDrain,
    req_byte:   1'b0,
    req_bit:    (state_q inside {AckRsvdByte, SendNack, SendIDBit, AckAddr}),
    data:       bus_tx_data
  };

  always_comb begin: fsm_ccc_entdaa
    bus_tx_data = '0;
    address_valid_o = 1'b0;
    done_daa_o = 1'b0;

    load_id_counter = 1'b0;
    tick_id_counter = 1'b0;

    state_d = state_q;
    unique case (state_q)
      Idle: begin
        if (start_daa_i) begin
          state_d = WaitStart;
        end
      end
      WaitStart: begin
        if (bus_rstart_det_i) begin
          state_d = ReceiveRsvdByte;
        end
      end
      ReceiveRsvdByte: begin
        if (bus_rx_rsp_i.done) begin
          if (reserved_word_det) state_d = AckRsvdByte;
          else state_d = SendNack;
        end
      end
      AckRsvdByte: begin
        if (bus_tx_rsp_i.done) begin
    	  state_d = SendID;
    	end
      end
      SendNack: begin
        bus_tx_data = '1; // TODO only one bit required

        if (bus_tx_rsp_i.done) begin
          state_d = Error;
    	  end
      end
      SendID: begin
        // load ID counter
        load_id_counter = 1'b1;
        state_d = PrepareIDBit;
      end
      PrepareIDBit: begin
        tick_id_counter = 1'b1;
        state_d = SendIDBit;
      end
      SendIDBit: begin
        bus_tx_data = {7'h0, device_id[id_bit_count[5:0]]};

        // our Id was overwritten by some other device
        if (arbitration_lost_i) begin
          state_d = LostArbitration;
        end else begin
          if (bus_tx_rsp_i.done) begin
            if (id_bit_count == '0) begin
              state_d = ReceiveAddr;
            end else begin
              state_d = PrepareIDBit;
            end
          end
        end
      end
      LostArbitration: begin
        state_d = Error;
      end
      ReceiveAddr: begin
        if (bus_rx_rsp_i.done) begin
          // TODO This must be as well gated by parity_ok??
          address_valid_o = 1'b1;
          if (parity_ok) begin
            state_d = AckAddr;
          end else begin 
            state_d = SendNack;
          end
        end
      end
      AckAddr: begin
        // TODO Repeat default value as bit must be explicitly zero
        bus_tx_data = '0;
        if (bus_tx_rsp_i.done) begin
          state_d = Done;
        end
      end
      Done: begin
        done_daa_o = 1'b1;
        state_d = Idle;
      end
      Error: begin
        // go back to idle and wait for next addressing round
        state_d = Idle;
      end
      default: begin
      end
    endcase

    // Overwrite decision on bus stop
    if (bus_stop_det_i) begin
      state_d = Done;
    end
  end

  // Synchronous state transition
  always_ff @(posedge clk_i or negedge rst_ni) begin : state_transition
    if (!rst_ni) begin
      state_q <= Idle;
    end else begin
      state_q <= state_d;
    end
  end

endmodule
