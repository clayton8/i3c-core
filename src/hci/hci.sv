// SPDX-License-Identifier: Apache-2.0

// I3C Host Controller Interface
module hci
  import i3c_pkg::*;
#(
    parameter int unsigned DatAw = 7,
    parameter int unsigned DctAw = 7,

    parameter int unsigned CsrDataWidth = 32,
    parameter int unsigned CsrAddrWidth = 12,

    parameter int unsigned HciRespFifoDepth = 64,
    parameter int unsigned HciCmdFifoDepth  = 64,
    parameter int unsigned HciRxFifoDepth   = 64,
    parameter int unsigned HciTxFifoDepth   = 64,
    parameter int unsigned HciIbiFifoDepth  = 64,

    localparam int unsigned HciRespFifoDepthWidth = $clog2(HciRespFifoDepth + 1),
    localparam int unsigned HciCmdFifoDepthWidth  = $clog2(HciCmdFifoDepth + 1),
    localparam int unsigned HciTxFifoDepthWidth   = $clog2(HciTxFifoDepth + 1),
    localparam int unsigned HciRxFifoDepthWidth   = $clog2(HciRxFifoDepth + 1),
    localparam int unsigned HciIbiFifoDepthWidth  = $clog2(HciIbiFifoDepth + 1),

    parameter int unsigned HciRespDataWidth = 32,
    parameter int unsigned HciCmdDataWidth  = 64,
    parameter int unsigned HciRxDataWidth   = 32,
    parameter int unsigned HciTxDataWidth   = 32,
    parameter int unsigned HciIbiDataWidth  = 32,

    parameter int unsigned HciRespThldWidth = 8,
    parameter int unsigned HciCmdThldWidth  = 8,
    parameter int unsigned HciRxThldWidth   = 3,
    parameter int unsigned HciTxThldWidth   = 3,
    parameter int unsigned HciIbiThldWidth  = 8
) (
    input clk_i,  // clock
    input rst_ni, // active low reset

    // I3C SW CSR access interface
    input  logic                    s_cpuif_req,
    input  logic                    s_cpuif_req_is_wr,
    input  logic [CsrAddrWidth-1:0] s_cpuif_addr,
    input  logic [CsrDataWidth-1:0] s_cpuif_wr_data,
    input  logic [CsrDataWidth-1:0] s_cpuif_wr_biten,
    output logic                    s_cpuif_req_stall_wr,
    output logic                    s_cpuif_req_stall_rd,
    output logic                    s_cpuif_rd_ack,
    output logic                    s_cpuif_rd_err,
    output logic [CsrDataWidth-1:0] s_cpuif_rd_data,
    output logic                    s_cpuif_wr_ack,
    output logic                    s_cpuif_wr_err,

    // DAT <-> Controller interface
    input  logic             dat_read_valid_hw_i,
    input  logic [DatAw-1:0] dat_index_hw_i,
    output logic [     63:0] dat_rdata_hw_o,

    // DCT <-> Controller interface
    input  logic             dct_write_valid_hw_i,
    input  logic             dct_read_valid_hw_i,
    input  logic [DctAw-1:0] dct_index_hw_i,
    input  logic [    127:0] dct_wdata_hw_i,
    output logic [    127:0] dct_rdata_hw_o,

    // DAT memory export interface
    input  dat_mem_src_t  dat_mem_src_i,
    output dat_mem_sink_t dat_mem_sink_o,

    // DCT memory export interface
    input  dct_mem_src_t  dct_mem_src_i,
    output dct_mem_sink_t dct_mem_sink_o,

    // Response queue
    output logic hci_resp_full_o,
    output logic [HciRespFifoDepthWidth-1:0] hci_resp_depth_o,
    output logic [HciRespThldWidth-1:0] hci_resp_ready_thld_o,
    output logic hci_resp_ready_thld_trig_o,
    output logic hci_resp_empty_o,
    input logic hci_resp_wvalid_i,
    output logic hci_resp_wready_o,
    input logic [CsrDataWidth-1:0] hci_resp_wdata_i,

    // Command queue
    output logic hci_cmd_full_o,
    output logic [HciCmdFifoDepthWidth-1:0] hci_cmd_depth_o,
    output logic [HciCmdThldWidth-1:0] hci_cmd_ready_thld_o,
    output logic hci_cmd_ready_thld_trig_o,
    output logic hci_cmd_empty_o,
    output logic hci_cmd_rvalid_o,
    input logic hci_cmd_rready_i,
    output logic [HciCmdDataWidth-1:0] hci_cmd_rdata_o,

    // RX queue
    output logic hci_rx_full_o,
    output logic [HciRxFifoDepthWidth-1:0] hci_rx_depth_o,
    output logic [HciRxThldWidth-1:0] hci_rx_start_thld_o,
    output logic [HciRxThldWidth-1:0] hci_rx_ready_thld_o,
    output logic hci_rx_start_thld_trig_o,
    output logic hci_rx_ready_thld_trig_o,
    output logic hci_rx_empty_o,
    input logic hci_rx_wvalid_i,
    output logic hci_rx_wready_o,
    input logic [CsrDataWidth-1:0] hci_rx_wdata_i,

    // TX queue
    output logic hci_tx_full_o,
    output logic [HciTxFifoDepthWidth-1:0] hci_tx_depth_o,
    output logic [HciTxThldWidth-1:0] hci_tx_start_thld_o,
    output logic [HciTxThldWidth-1:0] hci_tx_ready_thld_o,
    output logic hci_tx_start_thld_trig_o,
    output logic hci_tx_ready_thld_trig_o,
    output logic hci_tx_empty_o,
    output logic hci_tx_rvalid_o,
    input logic hci_tx_rready_i,
    output logic [HciTxDataWidth-1:0] hci_tx_rdata_o,

    // In-band Interrupt queue
    output logic hci_ibi_full_o,
    output logic [HciIbiFifoDepthWidth-1:0] hci_ibi_depth_o,
    output logic [HciIbiThldWidth-1:0] hci_ibi_ready_thld_o,
    output logic hci_ibi_ready_thld_trig_o,
    output logic hci_ibi_empty_o,
    input logic hci_ibi_wvalid_i,
    output logic hci_ibi_wready_o,
    input logic [HciIbiDataWidth-1:0] hci_ibi_wdata_i,

    // Target Transaction Interface CSRs
    output I3CCSR_pkg::I3CCSR__I3C_EC__TTI__out_t hwif_tti_o,
    input  I3CCSR_pkg::I3CCSR__I3C_EC__TTI__in_t  hwif_tti_i,
    // SoC Managment CSR interface
    output I3CCSR_pkg::I3CCSR__I3C_EC__SoCMgmtIf__out_t hwif_socmgmt_o,
    input  I3CCSR_pkg::I3CCSR__I3C_EC__SoCMgmtIf__in_t  hwif_socmgmt_i,

    // Recovery interface CSRs
    output I3CCSR_pkg::I3CCSR__I3C_EC__SecFwRecoveryIf__out_t hwif_rec_o,
    input  I3CCSR_pkg::I3CCSR__I3C_EC__SecFwRecoveryIf__in_t  hwif_rec_i,

    // Controller configuration
    output I3CCSR_pkg::I3CCSR__out_t hwif_out_o,

    input logic [6:0] set_dasa_i,
    input logic       set_dasa_valid_i,
    input logic       set_dasa_virtual_device_i,
    input logic       set_aasa_i,
    input logic       set_aasa_virt_i,
    input logic       rstdaa_i,
    input logic [6:0] newda_i,
    input logic       set_newda_i,
    input logic       set_newda_virtual_device_i,

    input logic [7:0] rst_action_i,
    input logic rst_action_valid_i
);

  I3CCSR_pkg::I3CCSR__in_t hwif_in;

  // Propagate reset to CSRs
  assign hwif_in.rst_ni = rst_ni;

  // DAT CSR interface
  I3CCSR_pkg::I3CCSR__DAT__out_t dat_o;
  I3CCSR_pkg::I3CCSR__DAT__in_t  dat_i;

  // DCT CSR interface
  I3CCSR_pkg::I3CCSR__DCT__out_t dct_o;
  I3CCSR_pkg::I3CCSR__DCT__in_t  dct_i;


  // TTI CSR interface
  assign hwif_tti_o = hwif_out_o.I3C_EC.TTI;
  assign hwif_in.I3C_EC.TTI = hwif_tti_i;

  // SoC Managment CSR interface
  assign hwif_socmgmt_o = hwif_out_o.I3C_EC.SoCMgmtIf;
  assign hwif_in.I3C_EC.SoCMgmtIf = hwif_socmgmt_i;

  // Recovery CSR interface
  assign hwif_rec_o = hwif_out_o.I3C_EC.SecFwRecoveryIf;

  // TODO: Use this if
  assign hwif_in.I3C_EC.SecFwRecoveryIf = hwif_rec_i;

  // Reset control
  logic cmd_reset_ctrl_we;
  logic cmd_reset_ctrl_next;

  logic rx_reset_ctrl_we;
  logic rx_reset_ctrl_next;

  logic tx_reset_ctrl_we;
  logic tx_reset_ctrl_next;

  logic resp_reset_ctrl_we;
  logic resp_reset_ctrl_next;

  // HCI queues' threshold
  logic [HciCmdThldWidth-1:0] cmd_ready_thld;
  logic [HciRxThldWidth-1:0] rx_ready_thld;
  logic [HciTxThldWidth-1:0] tx_ready_thld;
  logic [HciRespThldWidth-1:0] resp_ready_thld;

  // HCI queue port control
  logic cmd_req;  // Read DWORD from the COMMAND_PORT request
  logic cmd_wr_ack;  // Feedback to the COMMAND_PORT; command has been fetched
  logic [CsrDataWidth-1:0] cmd_wr_data;  // DWORD collected from the COMMAND_PORT

  logic xfer_req;  // RX / TX data write / read request
  logic xfer_req_is_wr;  // TX iff true, otherwise RX

  logic rx_req;  // Write RX data to the RX_PORT request
  logic rx_rd_ack;  // RX_DATA_PORT drives valid RX data
  logic [HciRxDataWidth-1:0] rx_rd_data;  // RX data read from the rx_fifo to be put to RX port

  logic tx_req;  // Read TX data from the TX_PORT request
  logic tx_wr_ack;  // Feedback to the TX_DATA_PORT; data has been read from TX port
  logic [CsrDataWidth-1:0] tx_wr_data;  // TX data to be put in tx_fifo

  logic resp_req;  // Write response to the RESPONSE_PORT request
  logic resp_rd_ack;  // resp_req is fulfilled; RESPONSE_PORT drives valid data
  logic [HciRespDataWidth-1:0] resp_rd_data;  // Response read from resp_fifo
                                              // placed in RESPONSE_PORT

  logic cmdrst, txrst, resprst, rxrst;

  logic cmd_ready_thld_swmod_q, cmd_ready_thld_we;
  logic resp_ready_thld_swmod_q, resp_ready_thld_we;

  always_ff @(posedge clk_i or negedge rst_ni) begin : blockName
    if (!rst_ni) begin
      cmd_ready_thld_we  <= '0;
      resp_ready_thld_we <= '0;
      cmd_ready_thld_swmod_q <= '0;
      resp_ready_thld_swmod_q <= '0;
    end else begin
      cmd_ready_thld_swmod_q <= hwif_out_o.PIOControl.QUEUE_THLD_CTRL.CMD_EMPTY_BUF_THLD.swmod;
      cmd_ready_thld_we <= cmd_ready_thld_swmod_q;
      resp_ready_thld_swmod_q <= hwif_out_o.PIOControl.QUEUE_THLD_CTRL.RESP_BUF_THLD.swmod;
      resp_ready_thld_we <= resp_ready_thld_swmod_q;
    end
  end

  always_comb begin : wire_hwif
    // Reset control
    cmdrst = hwif_out_o.I3CBase.RESET_CONTROL.CMD_QUEUE_RST.value;
    rxrst = hwif_out_o.I3CBase.RESET_CONTROL.RX_FIFO_RST.value;
    txrst = hwif_out_o.I3CBase.RESET_CONTROL.TX_FIFO_RST.value;
    resprst = hwif_out_o.I3CBase.RESET_CONTROL.RESP_QUEUE_RST.value;

    hwif_in.I3CBase.RESET_CONTROL.CMD_QUEUE_RST.we = cmd_reset_ctrl_we;
    hwif_in.I3CBase.RESET_CONTROL.CMD_QUEUE_RST.next = cmd_reset_ctrl_next;

    hwif_in.I3CBase.RESET_CONTROL.RX_FIFO_RST.we = rx_reset_ctrl_we;
    hwif_in.I3CBase.RESET_CONTROL.RX_FIFO_RST.next = rx_reset_ctrl_next;

    hwif_in.I3CBase.RESET_CONTROL.TX_FIFO_RST.we = tx_reset_ctrl_we;
    hwif_in.I3CBase.RESET_CONTROL.TX_FIFO_RST.next = tx_reset_ctrl_next;

    hwif_in.I3CBase.RESET_CONTROL.RESP_QUEUE_RST.we = resp_reset_ctrl_we;
    hwif_in.I3CBase.RESET_CONTROL.RESP_QUEUE_RST.next = resp_reset_ctrl_next;

    // Threshold
    hwif_in.PIOControl.QUEUE_THLD_CTRL.CMD_EMPTY_BUF_THLD.we = cmd_ready_thld_we;
    hwif_in.PIOControl.QUEUE_THLD_CTRL.RESP_BUF_THLD.we = resp_ready_thld_we;
    hwif_in.PIOControl.QUEUE_THLD_CTRL.CMD_EMPTY_BUF_THLD.next = hci_cmd_ready_thld_o;
    hwif_in.PIOControl.QUEUE_THLD_CTRL.RESP_BUF_THLD.next = hci_resp_ready_thld_o;
    cmd_ready_thld = hwif_out_o.PIOControl.QUEUE_THLD_CTRL.CMD_EMPTY_BUF_THLD.value;
    hci_rx_start_thld_o = hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.RX_START_THLD.value;
    rx_ready_thld = hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.RX_BUF_THLD.value;
    hci_tx_start_thld_o = hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.TX_START_THLD.value;
    tx_ready_thld = hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.TX_BUF_THLD.value;
    resp_ready_thld = hwif_out_o.PIOControl.QUEUE_THLD_CTRL.RESP_BUF_THLD.value;

    // HCI queue port handling

    // HCI PIOControl ports requests
    xfer_req = hwif_out_o.PIOControl.RX_DATA_PORT.req | hwif_out_o.PIOControl.TX_DATA_PORT.req;
    xfer_req_is_wr = hwif_out_o.PIOControl.RX_DATA_PORT.req_is_wr
      | hwif_out_o.PIOControl.TX_DATA_PORT.req_is_wr;

    cmd_req = hwif_out_o.PIOControl.COMMAND_PORT.req & hwif_out_o.PIOControl.COMMAND_PORT.req_is_wr;
    rx_req = xfer_req && !xfer_req_is_wr;
    tx_req = xfer_req && xfer_req_is_wr;
    resp_req = hwif_out_o.PIOControl.RESPONSE_PORT.req;

    // Reading commands from the command port
    hwif_in.PIOControl.COMMAND_PORT.wr_ack = cmd_wr_ack;
    cmd_wr_data = hwif_out_o.PIOControl.COMMAND_PORT.wr_data;

    // Writing data to the rx port
    hwif_in.PIOControl.RX_DATA_PORT.rd_ack = rx_rd_ack;
    hwif_in.PIOControl.RX_DATA_PORT.rd_data = rx_rd_data;

    // Reading data from the tx port
    hwif_in.PIOControl.TX_DATA_PORT.wr_ack = tx_wr_ack;
    tx_wr_data = hwif_out_o.PIOControl.TX_DATA_PORT.wr_data;

    // Writing response to the resp port
    hwif_in.PIOControl.RESPONSE_PORT.rd_ack = resp_rd_ack;
    hwif_in.PIOControl.RESPONSE_PORT.rd_data = resp_rd_data;

    // DXT
    hwif_in.DAT = dat_i;
    hwif_in.DCT = dct_i;
    dat_o = hwif_out_o.DAT;
    dct_o = hwif_out_o.DCT;
  end : wire_hwif

  always_comb begin : wire_hwif_rstact
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RST_ACTION.next = rst_action_valid_i ? rst_action_i : '0;
  end

  always_comb begin : wire_address_setting
    // Target address
    if (set_dasa_valid_i | rstdaa_i) begin
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.we = rstdaa_i ? '1 : set_dasa_valid_i && ~set_dasa_virtual_device_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.next = rstdaa_i ? '0 : ~set_dasa_virtual_device_i ? set_dasa_valid_i : '0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.we = rstdaa_i ? '1 : set_dasa_valid_i && ~set_dasa_virtual_device_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.next = rstdaa_i ? '0 : ~set_dasa_virtual_device_i ? set_dasa_i : '0;
      // Virtual device address
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.we = rstdaa_i ? '1 : set_dasa_valid_i && set_dasa_virtual_device_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.next = rstdaa_i ? '0 : set_dasa_virtual_device_i ? set_dasa_valid_i : '0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.we = rstdaa_i ? '1 : set_dasa_valid_i && set_dasa_virtual_device_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.next = rstdaa_i ? '0 : set_dasa_virtual_device_i ? set_dasa_i : '0;
    end else if (set_newda_i | set_newda_virtual_device_i) begin
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.we = set_newda_i && ~(set_newda_virtual_device_i);
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.next = 1'b1;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.we = set_newda_i && ~(set_newda_virtual_device_i);
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.next = newda_i;
      // Virtual device address
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.we = set_newda_i && set_newda_virtual_device_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.next = 1'b1;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.we = set_newda_i && set_newda_virtual_device_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.next = newda_i;
    end else if (set_aasa_i | set_aasa_virt_i) begin
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.we = set_aasa_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.next = 1'b1;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.we = set_aasa_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.next = hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR.value;
      // Virtual device address
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.we = set_aasa_virt_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.next = 1'b1;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.we = set_aasa_virt_i;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.next = hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR.value;
    end else begin
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.we = 1'b0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.next = '0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.we = 1'b0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.next = '0;
      // Virtual device address
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.we = 1'b0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.next = '0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.we = 1'b0;
      hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.next = '0;
    end
  end

  I3CCSR i3c_csr (
      .clk(clk_i),
      .rst('0),  // Unused, CSRs are reset through hwif_in.rst_ni

      .s_cpuif_req(s_cpuif_req),
      .s_cpuif_req_is_wr(s_cpuif_req_is_wr),
      .s_cpuif_addr(s_cpuif_addr),
      .s_cpuif_wr_data(s_cpuif_wr_data),
      .s_cpuif_wr_biten(s_cpuif_wr_biten),  // Write strobes not handled by AHB-Lite interface
      .s_cpuif_req_stall_wr(s_cpuif_req_stall_wr),
      .s_cpuif_req_stall_rd(s_cpuif_req_stall_rd),
      .s_cpuif_rd_ack(s_cpuif_rd_ack),  // Ignored by AHB component
      .s_cpuif_rd_err(s_cpuif_rd_err),
      .s_cpuif_rd_data(s_cpuif_rd_data),
      .s_cpuif_wr_ack(s_cpuif_wr_ack),  // Ignored by AHB component
      .s_cpuif_wr_err(s_cpuif_wr_err),

      .hwif_in (hwif_in),
      .hwif_out(hwif_out_o)
  );

  dxt #(
      .DatAw(DatAw),
      .DctAw(DctAw)
  ) dxt (
      .clk_i,  // clock
      .rst_ni,  // active low reset

      .dat_read_valid_hw_i,
      .dat_index_hw_i,
      .dat_rdata_hw_o,

      .dct_write_valid_hw_i,
      .dct_read_valid_hw_i,
      .dct_index_hw_i,
      .dct_wdata_hw_i,
      .dct_rdata_hw_o,

      .csr_dat_hwif_i(dat_o),
      .csr_dat_hwif_o(dat_i),

      .csr_dct_hwif_i(dct_o),
      .csr_dct_hwif_o(dct_i),

      .dat_mem_src_i,
      .dat_mem_sink_o,

      .dct_mem_src_i,
      .dct_mem_sink_o
  );

  logic unused_rx_desc_start_thld_trig, unused_tx_desc_start_thld_trig;

  queues #(
      .TxDescFifoDepth(HciCmdFifoDepth),
      .RxDescFifoDepth(HciRespFifoDepth),
      .TxFifoDepth(HciTxFifoDepth),
      .RxFifoDepth(HciRxFifoDepth),

      .TxDescFifoDataWidth(HciCmdDataWidth),
      .RxDescFifoDataWidth(HciRespDataWidth),
      .TxFifoDataWidth(HciTxDataWidth),
      .RxFifoDataWidth(HciRxDataWidth),

      .TxDescFifoThldWidth(HciCmdThldWidth),
      .RxDescFifoThldWidth(HciRespThldWidth),
      .TxFifoThldWidth(HciTxThldWidth),
      .RxFifoThldWidth(HciRxThldWidth)
  ) hci_queues (
      .clk_i,
      .rst_ni,

      .rx_desc_full_o(hci_resp_full_o),
      .rx_desc_depth_o(hci_resp_depth_o),
      .rx_desc_start_thld_trig_o(unused_rx_desc_start_thld_trig),  // Intentionally left hanging, unsupported by Response Queue
      .rx_desc_ready_thld_trig_o(hci_resp_ready_thld_trig_o),
      .rx_desc_empty_o(hci_resp_empty_o),
      .rx_desc_wvalid_i(hci_resp_wvalid_i),
      .rx_desc_wready_o(hci_resp_wready_o),
      .rx_desc_wdata_i(hci_resp_wdata_i),
      .rx_desc_req_i(resp_req),
      .rx_desc_ack_o(resp_rd_ack),
      .rx_desc_data_o(resp_rd_data),
      .rx_desc_start_thld_i('0),
      .rx_desc_ready_thld_i(resp_ready_thld),
      .rx_desc_ready_thld_o(hci_resp_ready_thld_o),
      .rx_desc_reg_rst_i(resprst),
      .rx_desc_reg_rst_we_o(resp_reset_ctrl_we),
      .rx_desc_reg_rst_data_o(resp_reset_ctrl_next),

      .tx_desc_full_o(hci_cmd_full_o),
      .tx_desc_depth_o(hci_cmd_depth_o),
      .tx_desc_start_thld_trig_o(unused_tx_desc_start_thld_trig),  // Intentionally left hanging, unsupported by Command Queue
      .tx_desc_ready_thld_trig_o(hci_cmd_ready_thld_trig_o),
      .tx_desc_empty_o(hci_cmd_empty_o),
      .tx_desc_rvalid_o(hci_cmd_rvalid_o),
      .tx_desc_rready_i(hci_cmd_rready_i),
      .tx_desc_rdata_o(hci_cmd_rdata_o),
      .tx_desc_req_i(cmd_req),
      .tx_desc_ack_o(cmd_wr_ack),
      .tx_desc_data_i(cmd_wr_data),
      .tx_desc_start_thld_i('0),
      .tx_desc_ready_thld_i(cmd_ready_thld),
      .tx_desc_ready_thld_o(hci_cmd_ready_thld_o),
      .tx_desc_reg_rst_i(cmdrst),
      .tx_desc_reg_rst_we_o(cmd_reset_ctrl_we),
      .tx_desc_reg_rst_data_o(cmd_reset_ctrl_next),

      .rx_full_o(hci_rx_full_o),
      .rx_depth_o(hci_rx_depth_o),
      .rx_start_thld_trig_o(hci_rx_start_thld_trig_o),
      .rx_ready_thld_trig_o(hci_rx_ready_thld_trig_o),
      .rx_empty_o(hci_rx_empty_o),
      .rx_wvalid_i(hci_rx_wvalid_i),
      .rx_wready_o(hci_rx_wready_o),
      .rx_wdata_i(hci_rx_wdata_i),
      .rx_req_i(rx_req),
      .rx_ack_o(rx_rd_ack),
      .rx_data_o(rx_rd_data),
      .rx_start_thld_i(hci_rx_start_thld_o),
      .rx_ready_thld_i(rx_ready_thld),
      .rx_ready_thld_o(hci_rx_ready_thld_o),
      .rx_reg_rst_i(rxrst),
      .rx_reg_rst_we_o(rx_reset_ctrl_we),
      .rx_reg_rst_data_o(rx_reset_ctrl_next),

      .tx_full_o(hci_tx_full_o),
      .tx_depth_o(hci_tx_depth_o),
      .tx_start_thld_trig_o(hci_tx_start_thld_trig_o),
      .tx_ready_thld_trig_o(hci_tx_ready_thld_trig_o),
      .tx_empty_o(hci_tx_empty_o),
      .tx_rvalid_o(hci_tx_rvalid_o),
      .tx_rready_i(hci_tx_rready_i),
      .tx_rdata_o(hci_tx_rdata_o),
      .tx_req_i(tx_req),
      .tx_ack_o(tx_wr_ack),
      .tx_data_i(tx_wr_data),
      .tx_start_thld_i(hci_tx_start_thld_o),
      .tx_ready_thld_i(tx_ready_thld),
      .tx_ready_thld_o(hci_tx_ready_thld_o),
      .tx_reg_rst_i(txrst),
      .tx_reg_rst_we_o(tx_reset_ctrl_we),
      .tx_reg_rst_data_o(tx_reset_ctrl_next)
  );



  // In-band Interrupt queue
  logic hci_ibi_rst;
  logic hci_ibi_rst_we;
  logic hci_ibi_rst_next;
  logic hci_ibi_req;
  logic hci_ibi_rd_ack;
  logic unused_ibi_queue_start_thld_trig;
  logic [HciIbiThldWidth-1:0] hci_ibi_thld;
  logic [HciIbiDataWidth-1:0] hci_ibi_rd_data;

  always_comb begin
    hci_ibi_rst = hwif_out_o.I3CBase.RESET_CONTROL.IBI_QUEUE_RST.value;
    hwif_in.I3CBase.RESET_CONTROL.IBI_QUEUE_RST.we = hci_ibi_rst_we;
    hwif_in.I3CBase.RESET_CONTROL.IBI_QUEUE_RST.next = hci_ibi_rst_next;

    hci_ibi_thld = hwif_out_o.PIOControl.QUEUE_THLD_CTRL.IBI_STATUS_THLD.value;

    hci_ibi_req = hwif_out_o.PIOControl.IBI_PORT.req;
    hwif_in.PIOControl.IBI_PORT.rd_ack = hci_ibi_rd_ack;
    hwif_in.PIOControl.IBI_PORT.rd_data = hci_ibi_rd_data;
  end

  read_queue #(
      .Depth(HciIbiFifoDepth),
      .DataWidth(HciIbiDataWidth),
      .ThldWidth(HciIbiThldWidth),
      .LimitReadyThld(0),
      .ThldIsPow(0)
  ) hci_ibi_queue (
      .clk_i,
      .rst_ni,

      .full_o(hci_ibi_full_o),
      .depth_o(hci_ibi_depth_o),
      .start_thld_trig_o(unused_ibi_queue_start_thld_trig),
      .ready_thld_trig_o(hci_ibi_ready_thld_trig_o),
      .empty_o(hci_ibi_empty_o),
      .wvalid_i(hci_ibi_wvalid_i),
      .wready_o(hci_ibi_wready_o),
      .wdata_i(hci_ibi_wdata_i),

      .req_i (hci_ibi_req),
      .ack_o (hci_ibi_rd_ack),
      .data_o(hci_ibi_rd_data),

      .start_thld_i('0),
      .ready_thld_i(hci_ibi_thld),
      .ready_thld_o(hci_ibi_ready_thld_o),

      .reg_rst_i(hci_ibi_rst),
      .reg_rst_we_o(hci_ibi_rst_we),
      .reg_rst_data_o(hci_ibi_rst_next)
  );

  always_comb begin : wire_unconnected_regs
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR_VALID.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.__rsvd_3.__rsvd.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RST_ACTION.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_OP_RSTACT_SIGNAL_EN.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR.next = '0;
    hwif_in.I3C_EC.CtrlCfg.CONTROLLER_CONFIG.OPERATION_MODE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_OP_RSTACT_STAT.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_OP_RSTACT_FORCE.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_ENTDAA_ENABLE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DEEP_SLEEP.hwclr = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR_VALID.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR.next= '0;

    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR_VALID.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR_VALID.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.PENDING_RX_NACK.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DELAY_NACK.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.ACR_FSM_OP_SELECT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.PRIME_ACCEPT_GETACCCR.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DEEP_SLEEP.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DEEP_SLEEP.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.TARGET_XACT_ENABLE.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.TARGET_XACT_ENABLE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETAASA_ENABLE.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETAASA_ENABLE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETDASA_ENABLE.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETDASA_ENABLE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_ENTDAA_ENABLE.we = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.AC_CURRENT_OWN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.SIMPLE_CRR_STATUS.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.HJ_REQ_STATUS.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_OK_REMAIN_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_OK_PRIMED_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_ERR_FAIL_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_ERR_M3_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CRR_RESPONSE_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_DYN_ADDR_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_NACKED_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_OK_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_ERR_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_OP_RSTACT_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_PARAM_MODIFIED_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_UNHANDLED_NACK_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_FATAL_RSTDAA_ERR_STAT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_OK_REMAIN_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_OK_PRIMED_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_ERR_FAIL_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_ERR_M3_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CRR_RESPONSE_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_DYN_ADDR_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_NACKED_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_OK_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_ERR_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_OP_RSTACT_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_PARAM_MODIFIED_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_UNHANDLED_NACK_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_FATAL_RSTDAA_ERR_SIGNAL_EN.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CRR_RESPONSE_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_DYN_ADDR_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_NACKED_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_OK_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_ERR_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_OP_RSTACT_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_PARAM_MODIFIED_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_UNHANDLED_NACK_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_FATAL_RSTDAA_ERR_FORCE.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_GETCAPS.F2_CRCAP1_BUS_CONFIG.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_GETCAPS.F2_CRCAP2_DEV_INTERACT.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_TIME_PERIPHERAL.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_TIME_TARGET.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_DYNAMIC_ADDR.next = '0;
    hwif_in.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_DYNAMIC_ADDR.we = '0;

    hwif_in.I3C_EC.CtrlCfg.CONTROLLER_CONFIG.OPERATION_MODE.we = '0;

    hwif_in.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR_VALID.we = '0;
    hwif_in.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR.we = '0;
    hwif_in.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR_VALID.next = '0;
    hwif_in.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR.next = '0;
    hwif_in.I3CBase.HC_CONTROL.RESUME.we = '0;
    hwif_in.I3CBase.HC_CONTROL.RESUME.next = '0;
    hwif_in.I3CBase.HC_CONTROL.BUS_ENABLE.we = '0;
    hwif_in.I3CBase.HC_CONTROL.BUS_ENABLE.next = '0;
    hwif_in.I3CBase.RESET_CONTROL.SOFT_RST.we = '0;
    hwif_in.I3CBase.RESET_CONTROL.SOFT_RST.next = '0;
    hwif_in.I3CBase.PRESENT_STATE.AC_CURRENT_OWN.next = '0;
    hwif_in.I3CBase.INTR_STATUS.HC_INTERNAL_ERR_STAT.next = '0;
    hwif_in.I3CBase.INTR_STATUS.HC_SEQ_CANCEL_STAT.next = '0;
    hwif_in.I3CBase.INTR_STATUS.HC_WARN_CMD_SEQ_STALL_STAT.next = '0;
    hwif_in.I3CBase.INTR_STATUS.HC_ERR_CMD_SEQ_TIMEOUT_STAT.next = '0;
    hwif_in.I3CBase.INTR_STATUS.SCHED_CMD_MISSED_TICK_STAT.next = '0;
    hwif_in.I3CBase.DCT_SECTION_OFFSET.TABLE_INDEX.we = '0;
    hwif_in.I3CBase.DCT_SECTION_OFFSET.TABLE_INDEX.next = '0;
    hwif_in.I3CBase.IBI_DATA_ABORT_CTRL.IBI_DATA_ABORT_MON.we = '0;
    hwif_in.I3CBase.IBI_DATA_ABORT_CTRL.IBI_DATA_ABORT_MON.next = '0;

    hwif_in.PIOControl.PIO_INTR_STATUS.TX_THLD_STAT.next = '0;
    hwif_in.PIOControl.PIO_INTR_STATUS.RX_THLD_STAT.next = '0;
    hwif_in.PIOControl.PIO_INTR_STATUS.IBI_STATUS_THLD_STAT.next = '0;
    hwif_in.PIOControl.PIO_INTR_STATUS.CMD_QUEUE_READY_STAT.next = '0;
    hwif_in.PIOControl.PIO_INTR_STATUS.RESP_READY_STAT.next = '0;
    hwif_in.PIOControl.PIO_INTR_STATUS.TRANSFER_ABORT_STAT.next = '0;
    hwif_in.PIOControl.PIO_INTR_STATUS.TRANSFER_ERR_STAT.next = '0;
  end

  // ===========================================================================
  // Assertions to detect X values on register .value fields after reset
  // Auto-generated from I3CCSR_pkg.sv
  // ===========================================================================
  // synthesis translate_off
  // verilator lint_off SYNCASYNCNET

  assert_no_x_1: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.IBA_INCLUDE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.IBA_INCLUDE.value");

  assert_no_x_2: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.I2C_DEV_PRESENT.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.I2C_DEV_PRESENT.value");

  assert_no_x_3: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.HOT_JOIN_CTRL.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.HOT_JOIN_CTRL.value");

  assert_no_x_4: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.HALT_ON_CMD_SEQ_TIMEOUT.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.HALT_ON_CMD_SEQ_TIMEOUT.value");

  assert_no_x_5: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.ABORT.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.ABORT.value");

  assert_no_x_6: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.RESUME.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.RESUME.value");

  assert_no_x_7: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.HC_CONTROL.BUS_ENABLE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.HC_CONTROL.BUS_ENABLE.value");

  assert_no_x_8: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR.value)
  ) else $error("X detected: hwif_out_o.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR.value");

  assert_no_x_9: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR_VALID.value)
  ) else $error("X detected: hwif_out_o.I3CBase.CONTROLLER_DEVICE_ADDR.DYNAMIC_ADDR_VALID.value");

  assert_no_x_10: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.RESET_CONTROL.SOFT_RST.value)
  ) else $error("X detected: hwif_out_o.I3CBase.RESET_CONTROL.SOFT_RST.value");

  assert_no_x_11: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.RESET_CONTROL.CMD_QUEUE_RST.value)
  ) else $error("X detected: hwif_out_o.I3CBase.RESET_CONTROL.CMD_QUEUE_RST.value");

  assert_no_x_12: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.RESET_CONTROL.RESP_QUEUE_RST.value)
  ) else $error("X detected: hwif_out_o.I3CBase.RESET_CONTROL.RESP_QUEUE_RST.value");

  assert_no_x_13: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.RESET_CONTROL.TX_FIFO_RST.value)
  ) else $error("X detected: hwif_out_o.I3CBase.RESET_CONTROL.TX_FIFO_RST.value");

  assert_no_x_14: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.RESET_CONTROL.RX_FIFO_RST.value)
  ) else $error("X detected: hwif_out_o.I3CBase.RESET_CONTROL.RX_FIFO_RST.value");

  assert_no_x_15: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.RESET_CONTROL.IBI_QUEUE_RST.value)
  ) else $error("X detected: hwif_out_o.I3CBase.RESET_CONTROL.IBI_QUEUE_RST.value");

  assert_no_x_16: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_INTERNAL_ERR_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_INTERNAL_ERR_STAT_EN.value");

  assert_no_x_17: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_SEQ_CANCEL_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_SEQ_CANCEL_STAT_EN.value");

  assert_no_x_18: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_WARN_CMD_SEQ_STALL_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_WARN_CMD_SEQ_STALL_STAT_EN.value");

  assert_no_x_19: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_ERR_CMD_SEQ_TIMEOUT_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_STATUS_ENABLE.HC_ERR_CMD_SEQ_TIMEOUT_STAT_EN.value");

  assert_no_x_20: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_STATUS_ENABLE.SCHED_CMD_MISSED_TICK_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_STATUS_ENABLE.SCHED_CMD_MISSED_TICK_STAT_EN.value");

  assert_no_x_21: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_INTERNAL_ERR_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_INTERNAL_ERR_SIGNAL_EN.value");

  assert_no_x_22: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_SEQ_CANCEL_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_SEQ_CANCEL_SIGNAL_EN.value");

  assert_no_x_23: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_WARN_CMD_SEQ_STALL_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_WARN_CMD_SEQ_STALL_SIGNAL_EN.value");

  assert_no_x_24: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_ERR_CMD_SEQ_TIMEOUT_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.HC_ERR_CMD_SEQ_TIMEOUT_SIGNAL_EN.value");

  assert_no_x_25: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.SCHED_CMD_MISSED_TICK_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_SIGNAL_ENABLE.SCHED_CMD_MISSED_TICK_SIGNAL_EN.value");

  assert_no_x_26: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_FORCE.HC_INTERNAL_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_FORCE.HC_INTERNAL_ERR_FORCE.value");

  assert_no_x_27: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_FORCE.HC_SEQ_CANCEL_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_FORCE.HC_SEQ_CANCEL_FORCE.value");

  assert_no_x_28: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_FORCE.HC_WARN_CMD_SEQ_STALL_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_FORCE.HC_WARN_CMD_SEQ_STALL_FORCE.value");

  assert_no_x_29: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_FORCE.HC_ERR_CMD_SEQ_TIMEOUT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_FORCE.HC_ERR_CMD_SEQ_TIMEOUT_FORCE.value");

  assert_no_x_30: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.INTR_FORCE.SCHED_CMD_MISSED_TICK_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.INTR_FORCE.SCHED_CMD_MISSED_TICK_FORCE.value");

  assert_no_x_31: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.DCT_SECTION_OFFSET.TABLE_INDEX.value)
  ) else $error("X detected: hwif_out_o.I3CBase.DCT_SECTION_OFFSET.TABLE_INDEX.value");

  assert_no_x_32: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_NOTIFY_CTRL.NOTIFY_HJ_REJECTED.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_NOTIFY_CTRL.NOTIFY_HJ_REJECTED.value");

  assert_no_x_33: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_NOTIFY_CTRL.NOTIFY_CRR_REJECTED.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_NOTIFY_CTRL.NOTIFY_CRR_REJECTED.value");

  assert_no_x_34: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_NOTIFY_CTRL.NOTIFY_IBI_REJECTED.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_NOTIFY_CTRL.NOTIFY_IBI_REJECTED.value");

  assert_no_x_35: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.MATCH_IBI_ID.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.MATCH_IBI_ID.value");

  assert_no_x_36: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.AFTER_N_CHUNKS.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.AFTER_N_CHUNKS.value");

  assert_no_x_37: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.MATCH_STATUS_TYPE.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.MATCH_STATUS_TYPE.value");

  assert_no_x_38: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.IBI_DATA_ABORT_MON.value)
  ) else $error("X detected: hwif_out_o.I3CBase.IBI_DATA_ABORT_CTRL.IBI_DATA_ABORT_MON.value");

  assert_no_x_39: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.DEV_CTX_BASE_LO.BASE_LO.value)
  ) else $error("X detected: hwif_out_o.I3CBase.DEV_CTX_BASE_LO.BASE_LO.value");

  assert_no_x_40: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3CBase.DEV_CTX_BASE_HI.BASE_HI.value)
  ) else $error("X detected: hwif_out_o.I3CBase.DEV_CTX_BASE_HI.BASE_HI.value");

  assert_no_x_41: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.QUEUE_THLD_CTRL.IBI_DATA_SEGMENT_SIZE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.QUEUE_THLD_CTRL.IBI_DATA_SEGMENT_SIZE.value");

  assert_no_x_42: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.QUEUE_THLD_CTRL.IBI_STATUS_THLD.value)
  ) else $error("X detected: hwif_out_o.PIOControl.QUEUE_THLD_CTRL.IBI_STATUS_THLD.value");

  assert_no_x_43: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.TX_BUF_THLD.value)
  ) else $error("X detected: hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.TX_BUF_THLD.value");

  assert_no_x_44: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.RX_BUF_THLD.value)
  ) else $error("X detected: hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.RX_BUF_THLD.value");

  assert_no_x_45: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.TX_START_THLD.value)
  ) else $error("X detected: hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.TX_START_THLD.value");

  assert_no_x_46: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.RX_START_THLD.value)
  ) else $error("X detected: hwif_out_o.PIOControl.DATA_BUFFER_THLD_CTRL.RX_START_THLD.value");

  assert_no_x_47: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.TX_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.TX_THLD_FORCE.value");

  assert_no_x_48: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.RX_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.RX_THLD_FORCE.value");

  assert_no_x_49: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.IBI_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.IBI_THLD_FORCE.value");

  assert_no_x_50: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.CMD_QUEUE_READY_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.CMD_QUEUE_READY_FORCE.value");

  assert_no_x_51: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.RESP_READY_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.RESP_READY_FORCE.value");

  assert_no_x_52: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.TRANSFER_ABORT_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.TRANSFER_ABORT_FORCE.value");

  assert_no_x_53: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_INTR_FORCE.TRANSFER_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_INTR_FORCE.TRANSFER_ERR_FORCE.value");

  assert_no_x_54: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_CONTROL.ENABLE.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_CONTROL.ENABLE.value");

  assert_no_x_55: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_CONTROL.RS.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_CONTROL.RS.value");

  assert_no_x_56: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.PIOControl.PIO_CONTROL.ABORT.value)
  ) else $error("X detected: hwif_out_o.PIOControl.PIO_CONTROL.ABORT.value");

  assert_no_x_57: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.EXTCAP_HEADER.CAP_ID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.EXTCAP_HEADER.CAP_ID.value");

  assert_no_x_58: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.EXTCAP_HEADER.CAP_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.EXTCAP_HEADER.CAP_LENGTH.value");

  assert_no_x_59: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_0.REC_MAGIC_STRING_0.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_0.REC_MAGIC_STRING_0.value");

  assert_no_x_60: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_1.REC_MAGIC_STRING_1.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_1.REC_MAGIC_STRING_1.value");

  assert_no_x_61: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_2.REC_PROT_VERSION.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_2.REC_PROT_VERSION.value");

  assert_no_x_62: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_2.AGENT_CAPS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_2.AGENT_CAPS.value");

  assert_no_x_63: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_3.NUM_OF_CMS_REGIONS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_3.NUM_OF_CMS_REGIONS.value");

  assert_no_x_64: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_3.MAX_RESP_TIME.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_3.MAX_RESP_TIME.value");

  assert_no_x_65: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_3.HEARTBEAT_PERIOD.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.PROT_CAP_3.HEARTBEAT_PERIOD.value");

  assert_no_x_66: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_0.DESC_TYPE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_0.DESC_TYPE.value");

  assert_no_x_67: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_0.VENDOR_SPECIFIC_STR_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_0.VENDOR_SPECIFIC_STR_LENGTH.value");

  assert_no_x_68: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_0.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_0.DATA.value");

  assert_no_x_69: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_1.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_1.DATA.value");

  assert_no_x_70: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_2.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_2.DATA.value");

  assert_no_x_71: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_3.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_3.DATA.value");

  assert_no_x_72: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_4.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_4.DATA.value");

  assert_no_x_73: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_5.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_5.DATA.value");

  assert_no_x_74: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_RESERVED.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_ID_RESERVED.DATA.value");

  assert_no_x_75: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_0.DEV_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_0.DEV_STATUS.value");

  assert_no_x_76: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_0.PROT_ERROR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_0.PROT_ERROR.value");

  assert_no_x_77: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_0.REC_REASON_CODE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_0.REC_REASON_CODE.value");

  assert_no_x_78: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_1.HEARTBEAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_1.HEARTBEAT.value");

  assert_no_x_79: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_1.VENDOR_STATUS_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_1.VENDOR_STATUS_LENGTH.value");

  assert_no_x_80: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_1.VENDOR_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_STATUS_1.VENDOR_STATUS.value");

  assert_no_x_81: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_RESET.RESET_CTRL.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_RESET.RESET_CTRL.value");

  assert_no_x_82: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_RESET.FORCED_RECOVERY.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_RESET.FORCED_RECOVERY.value");

  assert_no_x_83: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_RESET.IF_CTRL.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.DEVICE_RESET.IF_CTRL.value");

  assert_no_x_84: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.RECOVERY_STATUS.DEV_REC_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.RECOVERY_STATUS.DEV_REC_STATUS.value");

  assert_no_x_85: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.RECOVERY_STATUS.REC_IMG_INDEX.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.RECOVERY_STATUS.REC_IMG_INDEX.value");

  assert_no_x_86: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.RECOVERY_STATUS.VENDOR_SPECIFIC_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.RECOVERY_STATUS.VENDOR_SPECIFIC_STATUS.value");

  assert_no_x_87: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.TEMP_CRITICAL.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.TEMP_CRITICAL.value");

  assert_no_x_88: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.SOFT_ERR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.SOFT_ERR.value");

  assert_no_x_89: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.FATAL_ERR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.FATAL_ERR.value");

  assert_no_x_90: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.RESERVED_7_3.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.RESERVED_7_3.value");

  assert_no_x_91: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.VENDOR_HW_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.VENDOR_HW_STATUS.value");

  assert_no_x_92: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.CTEMP.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.CTEMP.value");

  assert_no_x_93: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.VENDOR_HW_STATUS_LEN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.HW_STATUS.VENDOR_HW_STATUS_LEN.value");

  assert_no_x_94: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_CTRL_0.CMS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_CTRL_0.CMS.value");

  assert_no_x_95: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_CTRL_0.RESET.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_CTRL_0.RESET.value");

  assert_no_x_96: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_CTRL_1.IMAGE_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_CTRL_1.IMAGE_SIZE.value");

  assert_no_x_97: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_0.EMPTY.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_0.EMPTY.value");

  assert_no_x_98: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_0.FULL.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_0.FULL.value");

  assert_no_x_99: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_0.REGION_TYPE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_0.REGION_TYPE.value");

  assert_no_x_100: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_1.WRITE_INDEX.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_1.WRITE_INDEX.value");

  assert_no_x_101: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_2.READ_INDEX.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_2.READ_INDEX.value");

  assert_no_x_102: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_3.FIFO_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_3.FIFO_SIZE.value");

  assert_no_x_103: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_4.MAX_TRANSFER_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_STATUS_4.MAX_TRANSFER_SIZE.value");

  assert_no_x_104: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_RESERVED.DATA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SecFwRecoveryIf.INDIRECT_FIFO_RESERVED.DATA.value");

  assert_no_x_105: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.EXTCAP_HEADER.CAP_ID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.EXTCAP_HEADER.CAP_ID.value");

  assert_no_x_106: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.EXTCAP_HEADER.CAP_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.EXTCAP_HEADER.CAP_LENGTH.value");

  assert_no_x_107: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.PENDING_RX_NACK.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.PENDING_RX_NACK.value");

  assert_no_x_108: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DELAY_NACK.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DELAY_NACK.value");

  assert_no_x_109: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.ACR_FSM_OP_SELECT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.ACR_FSM_OP_SELECT.value");

  assert_no_x_110: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.PRIME_ACCEPT_GETACCCR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.PRIME_ACCEPT_GETACCCR.value");

  assert_no_x_111: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DEEP_SLEEP.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.HANDOFF_DEEP_SLEEP.value");

  assert_no_x_112: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.CR_REQUEST_SEND.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.CR_REQUEST_SEND.value");

  assert_no_x_113: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.BAST_CCC_IBI_RING.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.BAST_CCC_IBI_RING.value");

  assert_no_x_114: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.TARGET_XACT_ENABLE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.TARGET_XACT_ENABLE.value");

  assert_no_x_115: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETAASA_ENABLE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETAASA_ENABLE.value");

  assert_no_x_116: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETDASA_ENABLE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_SETDASA_ENABLE.value");

  assert_no_x_117: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_ENTDAA_ENABLE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.DAA_ENTDAA_ENABLE.value");

  assert_no_x_118: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.RSTACT_DEFBYTE_02.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.RSTACT_DEFBYTE_02.value");

  assert_no_x_119: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.STBY_CR_ENABLE_INIT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CONTROL.STBY_CR_ENABLE_INIT.value");

  assert_no_x_120: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR.value");

  assert_no_x_121: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR_VALID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.STATIC_ADDR_VALID.value");

  assert_no_x_122: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR.value");

  assert_no_x_123: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_ADDR.DYNAMIC_ADDR_VALID.value");

  assert_no_x_124: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.SIMPLE_CRR_SUPPORT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.SIMPLE_CRR_SUPPORT.value");

  assert_no_x_125: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.TARGET_XACT_SUPPORT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.TARGET_XACT_SUPPORT.value");

  assert_no_x_126: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.DAA_SETAASA_SUPPORT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.DAA_SETAASA_SUPPORT.value");

  assert_no_x_127: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.DAA_SETDASA_SUPPORT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.DAA_SETDASA_SUPPORT.value");

  assert_no_x_128: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.DAA_ENTDAA_SUPPORT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CAPABILITIES.DAA_ENTDAA_SUPPORT.value");

  assert_no_x_129: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.PID_HI.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.PID_HI.value");

  assert_no_x_130: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.DCR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.DCR.value");

  assert_no_x_131: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.BCR_VAR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.BCR_VAR.value");

  assert_no_x_132: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.BCR_FIXED.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_CHAR.BCR_FIXED.value");

  assert_no_x_133: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.AC_CURRENT_OWN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.AC_CURRENT_OWN.value");

  assert_no_x_134: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.SIMPLE_CRR_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.SIMPLE_CRR_STATUS.value");

  assert_no_x_135: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.HJ_REQ_STATUS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_STATUS.HJ_REQ_STATUS.value");

  assert_no_x_136: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.PID_HI.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.PID_HI.value");

  assert_no_x_137: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.DCR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.DCR.value");

  assert_no_x_138: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.BCR_VAR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.BCR_VAR.value");

  assert_no_x_139: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.BCR_FIXED.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_CHAR.BCR_FIXED.value");

  assert_no_x_140: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_PID_LO.PID_LO.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_DEVICE_PID_LO.PID_LO.value");

  assert_no_x_141: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_OK_REMAIN_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_OK_REMAIN_STAT.value");

  assert_no_x_142: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_OK_PRIMED_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_OK_PRIMED_STAT.value");

  assert_no_x_143: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_ERR_FAIL_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_ERR_FAIL_STAT.value");

  assert_no_x_144: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_ERR_M3_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.ACR_HANDOFF_ERR_M3_STAT.value");

  assert_no_x_145: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CRR_RESPONSE_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CRR_RESPONSE_STAT.value");

  assert_no_x_146: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_DYN_ADDR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_DYN_ADDR_STAT.value");

  assert_no_x_147: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_NACKED_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_NACKED_STAT.value");

  assert_no_x_148: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_OK_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_OK_STAT.value");

  assert_no_x_149: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_ACCEPT_ERR_STAT.value");

  assert_no_x_150: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_OP_RSTACT_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.STBY_CR_OP_RSTACT_STAT.value");

  assert_no_x_151: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_PARAM_MODIFIED_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_PARAM_MODIFIED_STAT.value");

  assert_no_x_152: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_UNHANDLED_NACK_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_UNHANDLED_NACK_STAT.value");

  assert_no_x_153: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_FATAL_RSTDAA_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_STATUS.CCC_FATAL_RSTDAA_ERR_STAT.value");

  assert_no_x_154: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_PID_LO.PID_LO.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRTUAL_DEVICE_PID_LO.PID_LO.value");

  assert_no_x_155: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_OK_REMAIN_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_OK_REMAIN_SIGNAL_EN.value");

  assert_no_x_156: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_OK_PRIMED_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_OK_PRIMED_SIGNAL_EN.value");

  assert_no_x_157: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_ERR_FAIL_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_ERR_FAIL_SIGNAL_EN.value");

  assert_no_x_158: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_ERR_M3_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.ACR_HANDOFF_ERR_M3_SIGNAL_EN.value");

  assert_no_x_159: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CRR_RESPONSE_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CRR_RESPONSE_SIGNAL_EN.value");

  assert_no_x_160: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_DYN_ADDR_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_DYN_ADDR_SIGNAL_EN.value");

  assert_no_x_161: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_NACKED_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_NACKED_SIGNAL_EN.value");

  assert_no_x_162: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_OK_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_OK_SIGNAL_EN.value");

  assert_no_x_163: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_ERR_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_ACCEPT_ERR_SIGNAL_EN.value");

  assert_no_x_164: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_OP_RSTACT_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.STBY_CR_OP_RSTACT_SIGNAL_EN.value");

  assert_no_x_165: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_PARAM_MODIFIED_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_PARAM_MODIFIED_SIGNAL_EN.value");

  assert_no_x_166: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_UNHANDLED_NACK_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_UNHANDLED_NACK_SIGNAL_EN.value");

  assert_no_x_167: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_FATAL_RSTDAA_ERR_SIGNAL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_SIGNAL_ENABLE.CCC_FATAL_RSTDAA_ERR_SIGNAL_EN.value");

  assert_no_x_168: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CRR_RESPONSE_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CRR_RESPONSE_FORCE.value");

  assert_no_x_169: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_DYN_ADDR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_DYN_ADDR_FORCE.value");

  assert_no_x_170: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_NACKED_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_NACKED_FORCE.value");

  assert_no_x_171: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_OK_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_OK_FORCE.value");

  assert_no_x_172: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_ACCEPT_ERR_FORCE.value");

  assert_no_x_173: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_OP_RSTACT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.STBY_CR_OP_RSTACT_FORCE.value");

  assert_no_x_174: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_PARAM_MODIFIED_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_PARAM_MODIFIED_FORCE.value");

  assert_no_x_175: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_UNHANDLED_NACK_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_UNHANDLED_NACK_FORCE.value");

  assert_no_x_176: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_FATAL_RSTDAA_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_INTR_FORCE.CCC_FATAL_RSTDAA_ERR_FORCE.value");

  assert_no_x_177: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_GETCAPS.F2_CRCAP1_BUS_CONFIG.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_GETCAPS.F2_CRCAP1_BUS_CONFIG.value");

  assert_no_x_178: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_GETCAPS.F2_CRCAP2_DEV_INTERACT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_GETCAPS.F2_CRCAP2_DEV_INTERACT.value");

  assert_no_x_179: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RST_ACTION.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RST_ACTION.value");

  assert_no_x_180: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_TIME_PERIPHERAL.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_TIME_PERIPHERAL.value");

  assert_no_x_181: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_TIME_TARGET.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_TIME_TARGET.value");

  assert_no_x_182: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_DYNAMIC_ADDR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_CCC_CONFIG_RSTACT_PARAMS.RESET_DYNAMIC_ADDR.value");

  assert_no_x_183: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR.value");

  assert_no_x_184: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR_VALID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_STATIC_ADDR_VALID.value");

  assert_no_x_185: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR.value");

  assert_no_x_186: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.STBY_CR_VIRT_DEVICE_ADDR.VIRT_DYNAMIC_ADDR_VALID.value");

  assert_no_x_187: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.StdbyCtrlMode.__rsvd_3.__rsvd.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.StdbyCtrlMode.__rsvd_3.__rsvd.value");

  assert_no_x_188: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.EXTCAP_HEADER.CAP_ID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.EXTCAP_HEADER.CAP_ID.value");

  assert_no_x_189: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.EXTCAP_HEADER.CAP_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.EXTCAP_HEADER.CAP_LENGTH.value");

  assert_no_x_190: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.CONTROL.HJ_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.CONTROL.HJ_EN.value");

  assert_no_x_191: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.CONTROL.CRR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.CONTROL.CRR_EN.value");

  assert_no_x_192: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.CONTROL.IBI_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.CONTROL.IBI_EN.value");

  assert_no_x_193: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.CONTROL.IBI_RETRY_NUM.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.CONTROL.IBI_RETRY_NUM.value");

  assert_no_x_194: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.STATUS.PROTOCOL_ERROR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.STATUS.PROTOCOL_ERROR.value");

  assert_no_x_195: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.RESET_CONTROL.SOFT_RST.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.RESET_CONTROL.SOFT_RST.value");

  assert_no_x_196: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.RESET_CONTROL.TX_DESC_RST.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.RESET_CONTROL.TX_DESC_RST.value");

  assert_no_x_197: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.RESET_CONTROL.RX_DESC_RST.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.RESET_CONTROL.RX_DESC_RST.value");

  assert_no_x_198: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.RESET_CONTROL.TX_DATA_RST.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.RESET_CONTROL.TX_DATA_RST.value");

  assert_no_x_199: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.RESET_CONTROL.RX_DATA_RST.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.RESET_CONTROL.RX_DATA_RST.value");

  assert_no_x_200: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.RESET_CONTROL.IBI_QUEUE_RST.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.RESET_CONTROL.IBI_QUEUE_RST.value");

  assert_no_x_201: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DESC_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DESC_STAT.value");

  assert_no_x_202: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_STAT.value");

  assert_no_x_203: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DESC_TIMEOUT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DESC_TIMEOUT.value");

  assert_no_x_204: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_TIMEOUT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_TIMEOUT.value");

  assert_no_x_205: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DATA_THLD_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DATA_THLD_STAT.value");

  assert_no_x_206: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DATA_THLD_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DATA_THLD_STAT.value");

  assert_no_x_207: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_THLD_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_THLD_STAT.value");

  assert_no_x_208: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DESC_THLD_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.RX_DESC_THLD_STAT.value");

  assert_no_x_209: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.IBI_THLD_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.IBI_THLD_STAT.value");

  assert_no_x_210: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.IBI_DONE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.IBI_DONE.value");

  assert_no_x_211: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.PENDING_INTERRUPT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.PENDING_INTERRUPT.value");

  assert_no_x_212: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TRANSFER_ABORT_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TRANSFER_ABORT_STAT.value");

  assert_no_x_213: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_COMPLETE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TX_DESC_COMPLETE.value");

  assert_no_x_214: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TRANSFER_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_STATUS.TRANSFER_ERR_STAT.value");

  assert_no_x_215: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_STAT_EN.value");

  assert_no_x_216: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_STAT_EN.value");

  assert_no_x_217: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_TIMEOUT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_TIMEOUT_EN.value");

  assert_no_x_218: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_TIMEOUT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_TIMEOUT_EN.value");

  assert_no_x_219: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DATA_THLD_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DATA_THLD_STAT_EN.value");

  assert_no_x_220: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DATA_THLD_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DATA_THLD_STAT_EN.value");

  assert_no_x_221: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_THLD_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_THLD_STAT_EN.value");

  assert_no_x_222: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_THLD_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.RX_DESC_THLD_STAT_EN.value");

  assert_no_x_223: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.IBI_THLD_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.IBI_THLD_STAT_EN.value");

  assert_no_x_224: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.IBI_DONE_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.IBI_DONE_EN.value");

  assert_no_x_225: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TRANSFER_ABORT_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TRANSFER_ABORT_STAT_EN.value");

  assert_no_x_226: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_COMPLETE_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TX_DESC_COMPLETE_EN.value");

  assert_no_x_227: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TRANSFER_ERR_STAT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_ENABLE.TRANSFER_ERR_STAT_EN.value");

  assert_no_x_228: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DESC_STAT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DESC_STAT_FORCE.value");

  assert_no_x_229: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_STAT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_STAT_FORCE.value");

  assert_no_x_230: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DESC_TIMEOUT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DESC_TIMEOUT_FORCE.value");

  assert_no_x_231: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_TIMEOUT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_TIMEOUT_FORCE.value");

  assert_no_x_232: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DATA_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DATA_THLD_FORCE.value");

  assert_no_x_233: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DATA_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DATA_THLD_FORCE.value");

  assert_no_x_234: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_THLD_FORCE.value");

  assert_no_x_235: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DESC_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.RX_DESC_THLD_FORCE.value");

  assert_no_x_236: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.IBI_THLD_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.IBI_THLD_FORCE.value");

  assert_no_x_237: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.IBI_DONE_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.IBI_DONE_FORCE.value");

  assert_no_x_238: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TRANSFER_ABORT_STAT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TRANSFER_ABORT_STAT_FORCE.value");

  assert_no_x_239: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_COMPLETE_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TX_DESC_COMPLETE_FORCE.value");

  assert_no_x_240: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TRANSFER_ERR_STAT_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.INTERRUPT_FORCE.TRANSFER_ERR_STAT_FORCE.value");

  assert_no_x_241: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE0_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE0_ERR_DET_EN.value");

  assert_no_x_242: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE1_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE1_ERR_DET_EN.value");

  assert_no_x_243: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE2_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE2_ERR_DET_EN.value");

  assert_no_x_244: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE3_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE3_ERR_DET_EN.value");

  assert_no_x_245: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE4_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE4_ERR_DET_EN.value");

  assert_no_x_246: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE5_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.TE5_ERR_DET_EN.value");

  assert_no_x_247: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.FRAMING_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.FRAMING_ERR_DET_EN.value");

  assert_no_x_248: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_PEC_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_PEC_ERR_DET_EN.value");

  assert_no_x_249: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_LENGTH_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_LENGTH_ERR_DET_EN.value");

  assert_no_x_250: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_READONLY_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_READONLY_ERR_DET_EN.value");

  assert_no_x_251: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_UNSUPPORTED_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_UNSUPPORTED_ERR_DET_EN.value");

  assert_no_x_252: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_RX_FIFO_OVERFLOW_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_RX_FIFO_OVERFLOW_ERR_DET_EN.value");

  assert_no_x_253: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_INDIRECT_FIFO_OVERFLOW_ERR_DET_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CTRL.RI_INDIRECT_FIFO_OVERFLOW_ERR_DET_EN.value");

  assert_no_x_254: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE0_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE0_ERR_STAT.value");

  assert_no_x_255: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE1_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE1_ERR_STAT.value");

  assert_no_x_256: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE2_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE2_ERR_STAT.value");

  assert_no_x_257: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE3_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE3_ERR_STAT.value");

  assert_no_x_258: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE4_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE4_ERR_STAT.value");

  assert_no_x_259: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE5_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.TE5_ERR_STAT.value");

  assert_no_x_260: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.FRAMING_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.FRAMING_ERR_STAT.value");

  assert_no_x_261: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_PEC_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_PEC_ERR_STAT.value");

  assert_no_x_262: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_LENGTH_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_LENGTH_ERR_STAT.value");

  assert_no_x_263: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_READONLY_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_READONLY_ERR_STAT.value");

  assert_no_x_264: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_UNSUPPORTED_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_UNSUPPORTED_ERR_STAT.value");

  assert_no_x_265: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_RX_FIFO_OVERFLOW_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_RX_FIFO_OVERFLOW_ERR_STAT.value");

  assert_no_x_266: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_INDIRECT_FIFO_OVERFLOW_ERR_STAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_STATUS.RI_INDIRECT_FIFO_OVERFLOW_ERR_STAT.value");

  assert_no_x_267: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE0_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE0_ERR_EN.value");

  assert_no_x_268: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE1_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE1_ERR_EN.value");

  assert_no_x_269: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE2_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE2_ERR_EN.value");

  assert_no_x_270: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE3_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE3_ERR_EN.value");

  assert_no_x_271: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE4_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE4_ERR_EN.value");

  assert_no_x_272: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE5_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.TE5_ERR_EN.value");

  assert_no_x_273: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.FRAMING_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.FRAMING_ERR_EN.value");

  assert_no_x_274: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_PEC_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_PEC_ERR_EN.value");

  assert_no_x_275: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_LENGTH_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_LENGTH_ERR_EN.value");

  assert_no_x_276: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_READONLY_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_READONLY_ERR_EN.value");

  assert_no_x_277: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_UNSUPPORTED_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_UNSUPPORTED_ERR_EN.value");

  assert_no_x_278: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_RX_FIFO_OVERFLOW_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_RX_FIFO_OVERFLOW_ERR_EN.value");

  assert_no_x_279: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_INDIRECT_FIFO_OVERFLOW_ERR_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_ENABLE.RI_INDIRECT_FIFO_OVERFLOW_ERR_EN.value");

  assert_no_x_280: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE0_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE0_ERR_FORCE.value");

  assert_no_x_281: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE1_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE1_ERR_FORCE.value");

  assert_no_x_282: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE2_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE2_ERR_FORCE.value");

  assert_no_x_283: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE3_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE3_ERR_FORCE.value");

  assert_no_x_284: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE4_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE4_ERR_FORCE.value");

  assert_no_x_285: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE5_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.TE5_ERR_FORCE.value");

  assert_no_x_286: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.FRAMING_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.FRAMING_ERR_FORCE.value");

  assert_no_x_287: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_PEC_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_PEC_ERR_FORCE.value");

  assert_no_x_288: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_LENGTH_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_LENGTH_ERR_FORCE.value");

  assert_no_x_289: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_READONLY_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_READONLY_ERR_FORCE.value");

  assert_no_x_290: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_UNSUPPORTED_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_UNSUPPORTED_ERR_FORCE.value");

  assert_no_x_291: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_RX_FIFO_OVERFLOW_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_RX_FIFO_OVERFLOW_ERR_FORCE.value");

  assert_no_x_292: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_INDIRECT_FIFO_OVERFLOW_ERR_FORCE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_INTR_FORCE.RI_INDIRECT_FIFO_OVERFLOW_ERR_FORCE.value");

  assert_no_x_293: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE0.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE0.CNT.value");

  assert_no_x_294: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE1.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE1.CNT.value");

  assert_no_x_295: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE2.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE2.CNT.value");

  assert_no_x_296: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE3.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE3.CNT.value");

  assert_no_x_297: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE4.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE4.CNT.value");

  assert_no_x_298: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE5.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_TE5.CNT.value");

  assert_no_x_299: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_FRAMING.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_FRAMING.CNT.value");

  assert_no_x_300: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_PEC.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_PEC.CNT.value");

  assert_no_x_301: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_LENGTH.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_LENGTH.CNT.value");

  assert_no_x_302: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_READONLY.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_READONLY.CNT.value");

  assert_no_x_303: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_UNSUPPORTED.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_UNSUPPORTED.CNT.value");

  assert_no_x_304: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_RX_FIFO_OVERFLOW.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_RX_FIFO_OVERFLOW.CNT.value");

  assert_no_x_305: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_INDIRECT_FIFO_OVERFLOW.CNT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.TARGET_ERR_CNT_RI_INDIRECT_FIFO_OVERFLOW.CNT.value");

  assert_no_x_306: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.RX_DESC_BUFFER_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.RX_DESC_BUFFER_SIZE.value");

  assert_no_x_307: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.TX_DESC_BUFFER_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.TX_DESC_BUFFER_SIZE.value");

  assert_no_x_308: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.RX_DATA_BUFFER_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.RX_DATA_BUFFER_SIZE.value");

  assert_no_x_309: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.TX_DATA_BUFFER_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.QUEUE_SIZE.TX_DATA_BUFFER_SIZE.value");

  assert_no_x_310: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.IBI_QUEUE_SIZE.IBI_QUEUE_SIZE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.IBI_QUEUE_SIZE.IBI_QUEUE_SIZE.value");

  assert_no_x_311: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.TX_DATA_THLD.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.TX_DATA_THLD.value");

  assert_no_x_312: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.RX_DATA_THLD.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.RX_DATA_THLD.value");

  assert_no_x_313: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.TX_START_THLD.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.TX_START_THLD.value");

  assert_no_x_314: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.RX_START_THLD.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TTI.DATA_BUFFER_THLD_CTRL.RX_START_THLD.value");

  assert_no_x_315: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.EXTCAP_HEADER.CAP_ID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.EXTCAP_HEADER.CAP_ID.value");

  assert_no_x_316: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.EXTCAP_HEADER.CAP_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.EXTCAP_HEADER.CAP_LENGTH.value");

  assert_no_x_317: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_CONTROL.PLACEHOLDER.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_CONTROL.PLACEHOLDER.value");

  assert_no_x_318: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_STATUS.PLACEHOLDER.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_STATUS.PLACEHOLDER.value");

  assert_no_x_319: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.REC_INTF_CFG.REC_INTF_BYPASS.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.REC_INTF_CFG.REC_INTF_BYPASS.value");

  assert_no_x_320: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.REC_INTF_CFG.REC_PAYLOAD_DONE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.REC_INTF_CFG.REC_PAYLOAD_DONE.value");

  assert_no_x_321: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_RSVD_2.PLACEHOLDER.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_RSVD_2.PLACEHOLDER.value");

  assert_no_x_322: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_RSVD_3.PLACEHOLDER.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_RSVD_3.PLACEHOLDER.value");

  assert_no_x_323: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.INPUT_ENABLE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.INPUT_ENABLE.value");

  assert_no_x_324: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.SCHMITT_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.SCHMITT_EN.value");

  assert_no_x_325: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.KEEPER_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.KEEPER_EN.value");

  assert_no_x_326: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.PULL_DIR.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.PULL_DIR.value");

  assert_no_x_327: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.PULL_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.PULL_EN.value");

  assert_no_x_328: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.IO_INVERSION.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.IO_INVERSION.value");

  assert_no_x_329: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.OD_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.OD_EN.value");

  assert_no_x_330: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.VIRTUAL_OD_EN.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.VIRTUAL_OD_EN.value");

  assert_no_x_331: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.PAD_TYPE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_CONF.PAD_TYPE.value");

  assert_no_x_332: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_ATTR.DRIVE_SLEW_RATE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_ATTR.DRIVE_SLEW_RATE.value");

  assert_no_x_333: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_ATTR.DRIVE_STRENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_PAD_ATTR.DRIVE_STRENGTH.value");

  assert_no_x_334: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_FEATURE_2.PLACEHOLDER.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_FEATURE_2.PLACEHOLDER.value");

  assert_no_x_335: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_FEATURE_3.PLACEHOLDER.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.SOC_MGMT_FEATURE_3.PLACEHOLDER.value");

  assert_no_x_336: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_R_REG.T_R.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_R_REG.T_R.value");

  assert_no_x_337: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_F_REG.T_F.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_F_REG.T_F.value");

  assert_no_x_338: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_SU_DAT_REG.T_SU_DAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_SU_DAT_REG.T_SU_DAT.value");

  assert_no_x_339: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_HD_DAT_REG.T_HD_DAT.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_HD_DAT_REG.T_HD_DAT.value");

  assert_no_x_340: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_HIGH_REG.T_HIGH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_HIGH_REG.T_HIGH.value");

  assert_no_x_341: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_LOW_REG.T_LOW.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_LOW_REG.T_LOW.value");

  assert_no_x_342: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_HD_STA_REG.T_HD_STA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_HD_STA_REG.T_HD_STA.value");

  assert_no_x_343: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_SU_STA_REG.T_SU_STA.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_SU_STA_REG.T_SU_STA.value");

  assert_no_x_344: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_SU_STO_REG.T_SU_STO.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_SU_STO_REG.T_SU_STO.value");

  assert_no_x_345: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_FREE_REG.T_FREE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_FREE_REG.T_FREE.value");

  assert_no_x_346: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_AVAL_REG.T_AVAL.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_AVAL_REG.T_AVAL.value");

  assert_no_x_347: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.SoCMgmtIf.T_IDLE_REG.T_IDLE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.SoCMgmtIf.T_IDLE_REG.T_IDLE.value");

  assert_no_x_348: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.CtrlCfg.EXTCAP_HEADER.CAP_ID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.CtrlCfg.EXTCAP_HEADER.CAP_ID.value");

  assert_no_x_349: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.CtrlCfg.EXTCAP_HEADER.CAP_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.CtrlCfg.EXTCAP_HEADER.CAP_LENGTH.value");

  assert_no_x_350: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.CtrlCfg.CONTROLLER_CONFIG.OPERATION_MODE.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.CtrlCfg.CONTROLLER_CONFIG.OPERATION_MODE.value");

  assert_no_x_351: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TERMINATION_EXTCAP_HEADER.CAP_ID.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TERMINATION_EXTCAP_HEADER.CAP_ID.value");

  assert_no_x_352: assert property (
    @(posedge clk_i) disable iff (!rst_ni)
    !$isunknown(hwif_out_o.I3C_EC.TERMINATION_EXTCAP_HEADER.CAP_LENGTH.value)
  ) else $error("X detected: hwif_out_o.I3C_EC.TERMINATION_EXTCAP_HEADER.CAP_LENGTH.value");

  // verilator lint_on SYNCASYNCNET
  // synthesis translate_on

endmodule : hci
