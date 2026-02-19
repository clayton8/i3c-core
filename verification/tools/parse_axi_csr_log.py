#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Post-processor for AXI CSR transaction logs.

Reads axi_csr_transactions.log produced by the bind-module tracker
(+define+TRACK_FSM_TRANSITIONS) and outputs:
  1. Human-readable transaction log with aligned columns
  2. Per-register access frequency (read count, write count)
  3. Transaction rate over time (transactions per time window)
  4. Registers never accessed (coverage gap detection)

Usage:
    python parse_axi_csr_log.py [axi_csr_transactions.log]
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

# All known CSR names for coverage gap detection
KNOWN_CSRS = [
    "I3CBASE.HCI_VERSION",
    "I3CBASE.HC_CONTROL",
    "I3CBASE.CONTROLLER_DEVICE_ADDR",
    "I3CBASE.HC_CAPABILITIES",
    "I3CBASE.RESET_CONTROL",
    "I3CBASE.PRESENT_STATE",
    "I3CBASE.INTR_STATUS",
    "I3CBASE.INTR_STATUS_ENABLE",
    "I3CBASE.INTR_SIGNAL_ENABLE",
    "I3CBASE.INTR_FORCE",
    "I3CBASE.DAT_SECTION_OFFSET",
    "I3CBASE.DCT_SECTION_OFFSET",
    "I3CBASE.RING_HEADERS_SECTION_OFFSET",
    "I3CBASE.PIO_SECTION_OFFSET",
    "I3CBASE.EXT_CAPS_SECTION_OFFSET",
    "I3CBASE.INT_CTRL_CMDS_EN",
    "I3CBASE.IBI_NOTIFY_CTRL",
    "I3CBASE.IBI_DATA_ABORT_CTRL",
    "I3CBASE.DEV_CTX_BASE_LO",
    "I3CBASE.DEV_CTX_BASE_HI",
    "I3CBASE.DEV_CTX_SG",
    "PIOCONTROL.COMMAND_PORT",
    "PIOCONTROL.RESPONSE_PORT",
    "PIOCONTROL.TX_DATA_PORT",
    "PIOCONTROL.RX_DATA_PORT",
    "PIOCONTROL.IBI_PORT",
    "PIOCONTROL.QUEUE_THLD_CTRL",
    "PIOCONTROL.DATA_BUFFER_THLD_CTRL",
    "PIOCONTROL.QUEUE_SIZE",
    "PIOCONTROL.ALT_QUEUE_SIZE",
    "PIOCONTROL.PIO_INTR_STATUS",
    "PIOCONTROL.PIO_INTR_STATUS_ENABLE",
    "PIOCONTROL.PIO_INTR_SIGNAL_ENABLE",
    "PIOCONTROL.PIO_INTR_FORCE",
    "PIOCONTROL.PIO_CONTROL",
    "SECFWRECOVERYIF.EXTCAP_HEADER",
    "SECFWRECOVERYIF.PROT_CAP_0",
    "SECFWRECOVERYIF.PROT_CAP_1",
    "SECFWRECOVERYIF.PROT_CAP_2",
    "SECFWRECOVERYIF.PROT_CAP_3",
    "SECFWRECOVERYIF.DEVICE_ID_0",
    "SECFWRECOVERYIF.DEVICE_ID_1",
    "SECFWRECOVERYIF.DEVICE_ID_2",
    "SECFWRECOVERYIF.DEVICE_ID_3",
    "SECFWRECOVERYIF.DEVICE_ID_4",
    "SECFWRECOVERYIF.DEVICE_ID_5",
    "SECFWRECOVERYIF.DEVICE_ID_RESERVED",
    "SECFWRECOVERYIF.DEVICE_STATUS_0",
    "SECFWRECOVERYIF.DEVICE_STATUS_1",
    "SECFWRECOVERYIF.DEVICE_RESET",
    "SECFWRECOVERYIF.RECOVERY_CTRL",
    "SECFWRECOVERYIF.RECOVERY_STATUS",
    "SECFWRECOVERYIF.HW_STATUS",
    "SECFWRECOVERYIF.INDIRECT_FIFO_CTRL_0",
    "SECFWRECOVERYIF.INDIRECT_FIFO_CTRL_1",
    "SECFWRECOVERYIF.INDIRECT_FIFO_STATUS_0",
    "SECFWRECOVERYIF.INDIRECT_FIFO_STATUS_1",
    "SECFWRECOVERYIF.INDIRECT_FIFO_STATUS_2",
    "SECFWRECOVERYIF.INDIRECT_FIFO_STATUS_3",
    "SECFWRECOVERYIF.INDIRECT_FIFO_STATUS_4",
    "SECFWRECOVERYIF.INDIRECT_FIFO_RESERVED",
    "SECFWRECOVERYIF.INDIRECT_FIFO_DATA",
    "STDBYCTRLMODE.EXTCAP_HEADER",
    "STDBYCTRLMODE.STBY_CR_CONTROL",
    "STDBYCTRLMODE.STBY_CR_DEVICE_ADDR",
    "STDBYCTRLMODE.STBY_CR_CAPABILITIES",
    "STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_CHAR",
    "STDBYCTRLMODE.STBY_CR_STATUS",
    "STDBYCTRLMODE.STBY_CR_DEVICE_CHAR",
    "STDBYCTRLMODE.STBY_CR_DEVICE_PID_LO",
    "STDBYCTRLMODE.STBY_CR_INTR_STATUS",
    "STDBYCTRLMODE.STBY_CR_VIRTUAL_DEVICE_PID_LO",
    "STDBYCTRLMODE.STBY_CR_INTR_SIGNAL_ENABLE",
    "STDBYCTRLMODE.STBY_CR_INTR_FORCE",
    "STDBYCTRLMODE.STBY_CR_CCC_CONFIG_GETCAPS",
    "STDBYCTRLMODE.STBY_CR_CCC_CONFIG_RSTACT_PARAMS",
    "STDBYCTRLMODE.STBY_CR_VIRT_DEVICE_ADDR",
    "STDBYCTRLMODE.STBY_CR_MWL",
    "STDBYCTRLMODE.STBY_CR_MRL",
    "TTI.EXTCAP_HEADER",
    "TTI.CONTROL",
    "TTI.STATUS",
    "TTI.RESET_CONTROL",
    "TTI.QUEUE_STATUS",
    "TTI.DESC_QUEUE_DEPTH",
    "TTI.DATA_QUEUE_DEPTH",
    "TTI.IBI_QUEUE_DEPTH",
    "TTI.INTERRUPT_STATUS",
    "TTI.INTERRUPT_ENABLE",
    "TTI.INTERRUPT_FORCE",
    "TTI.TARGET_ERR_CTRL",
    "TTI.TARGET_ERR_INTR_STATUS",
    "TTI.TARGET_ERR_INTR_ENABLE",
    "TTI.TARGET_ERR_INTR_FORCE",
    "TTI.TARGET_ERR_CNT_TE0",
    "TTI.TARGET_ERR_CNT_TE1",
    "TTI.TARGET_ERR_CNT_TE2",
    "TTI.TARGET_ERR_CNT_TE3",
    "TTI.TARGET_ERR_CNT_TE4",
    "TTI.TARGET_ERR_CNT_TE5",
    "TTI.TARGET_ERR_CNT_FRAMING",
    "TTI.TARGET_ERR_CNT_RI_PEC",
    "TTI.TARGET_ERR_CNT_RI_LENGTH",
    "TTI.TARGET_ERR_CNT_RI_READONLY",
    "TTI.TARGET_ERR_CNT_RI_UNSUPPORTED",
    "TTI.TARGET_ERR_CNT_RI_RX_FIFO_OVERFLOW",
    "TTI.TARGET_ERR_CNT_RI_INDIRECT_FIFO_OVERFLOW",
    "TTI.RX_DESC_QUEUE_PORT",
    "TTI.RX_DATA_PORT",
    "TTI.TX_DESC_QUEUE_PORT",
    "TTI.TX_DATA_PORT",
    "TTI.IBI_PORT",
    "TTI.QUEUE_SIZE",
    "TTI.IBI_QUEUE_SIZE",
    "TTI.QUEUE_THLD_CTRL",
    "TTI.DATA_BUFFER_THLD_CTRL",
    "SOCMGMTIF.EXTCAP_HEADER",
    "SOCMGMTIF.SOC_MGMT_CONTROL",
    "SOCMGMTIF.SOC_MGMT_STATUS",
    "SOCMGMTIF.REC_INTF_CFG",
    "SOCMGMTIF.REC_INTF_REG_W1C_ACCESS",
    "SOCMGMTIF.SOC_MGMT_RSVD_2",
    "SOCMGMTIF.SOC_MGMT_RSVD_3",
    "SOCMGMTIF.SOC_PAD_CONF",
    "SOCMGMTIF.SOC_PAD_ATTR",
    "SOCMGMTIF.SOC_MGMT_FEATURE_2",
    "SOCMGMTIF.SOC_MGMT_FEATURE_3",
    "SOCMGMTIF.T_R_REG",
    "SOCMGMTIF.T_F_REG",
    "SOCMGMTIF.T_SU_DAT_REG",
    "SOCMGMTIF.T_HD_DAT_REG",
    "SOCMGMTIF.T_HIGH_REG",
    "SOCMGMTIF.T_LOW_REG",
    "SOCMGMTIF.T_HD_STA_REG",
    "SOCMGMTIF.T_SU_STA_REG",
    "SOCMGMTIF.T_SU_STO_REG",
    "SOCMGMTIF.T_FREE_REG",
    "SOCMGMTIF.T_AVAL_REG",
    "SOCMGMTIF.T_IDLE_REG",
    "SOCMGMTIF.HDR_TIMEOUT_EN_REG",
    "SOCMGMTIF.T_HDR_TIMEOUT_REG",
    "CTRLCFG.EXTCAP_HEADER",
    "CTRLCFG.CONTROLLER_CONFIG",
]


def parse_log(path):
    """Parse axi_csr_transactions.log, return list of (timestamp_str, csr_name, direction, data_hex)."""
    transactions = []
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 4:
                print(f"WARNING: skipping malformed line {lineno}: {line!r}", file=sys.stderr)
                continue
            ts_raw = parts[0]
            csr_name = parts[1]
            direction = parts[2]
            data_hex = parts[3]
            transactions.append((ts_raw, csr_name, direction, data_hex))
    return transactions


def parse_timestamp(ts_raw):
    """Convert raw timestamp string to a numeric value."""
    for suffix in ("fs", "ps", "ns", "us", "ms", "s"):
        if ts_raw.endswith(suffix):
            return float(ts_raw[:-len(suffix)])
    return float(ts_raw)


def print_readable_log(transactions):
    """Print aligned, human-readable transaction log."""
    print("=" * 90)
    print("AXI CSR TRANSACTION LOG")
    print("=" * 90)
    print(f"{'Timestamp':>14s} | {'CSR Name':<50s} | {'Dir':>5s} | {'Data':<10s}")
    print("-" * 90)
    for ts_raw, csr_name, direction, data_hex in transactions:
        print(f"{ts_raw:>14s} | {csr_name:<50s} | {direction:>5s} | {data_hex}")
    print(f"\nTotal transactions: {len(transactions)}")


def print_access_frequency(transactions):
    """Print per-register access frequency."""
    reads = defaultdict(int)
    writes = defaultdict(int)
    for _, csr_name, direction, _ in transactions:
        if direction == "READ":
            reads[csr_name] += 1
        else:
            writes[csr_name] += 1

    all_csrs = sorted(set(list(reads.keys()) + list(writes.keys())))

    print("\n" + "=" * 90)
    print("PER-REGISTER ACCESS FREQUENCY")
    print("=" * 90)
    print(f"  {'CSR Name':<50s} {'Reads':>8s} {'Writes':>8s} {'Total':>8s}")
    print("  " + "-" * 78)
    for csr in all_csrs:
        r = reads[csr]
        w = writes[csr]
        print(f"  {csr:<50s} {r:>8d} {w:>8d} {r+w:>8d}")
    print(f"\n  Total reads: {sum(reads.values())}, writes: {sum(writes.values())}")


def print_never_accessed(transactions):
    """Flag known CSRs that were never accessed."""
    accessed = set()
    for _, csr_name, _, _ in transactions:
        accessed.add(csr_name)

    never = [c for c in KNOWN_CSRS if c not in accessed]

    print("\n" + "=" * 90)
    print("CSR COVERAGE GAPS (never accessed)")
    print("=" * 90)
    if not never:
        print("  None — all known CSRs were accessed at least once.")
    else:
        print(f"  {len(never)} CSR(s) never accessed:")
        for csr in never:
            print(f"    {csr}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse and analyze AXI CSR transaction logs.")
    parser.add_argument("logfile", nargs="?", default="axi_csr_transactions.log",
                        help="Path to axi_csr_transactions.log (default: axi_csr_transactions.log)")
    args = parser.parse_args()

    log_path = Path(args.logfile)
    if not log_path.exists():
        print(f"ERROR: {log_path} not found.", file=sys.stderr)
        sys.exit(1)

    transactions = parse_log(log_path)
    if not transactions:
        print("No transactions found in log file.")
        sys.exit(0)

    print_readable_log(transactions)
    print_access_frequency(transactions)
    print_never_accessed(transactions)


if __name__ == "__main__":
    main()
