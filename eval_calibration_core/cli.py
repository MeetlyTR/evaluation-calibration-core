# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""CLI for evaluation-calibration-core."""

import argparse
from pathlib import Path

from eval_calibration_core.contracts import check_schema_compatibility, check_expected_minor_range, get_schema_version
from eval_calibration_core.io.fixtures import load_fixture_suite
from eval_calibration_core.io.packet_reader import PacketReader
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report.model import Report
from eval_calibration_core.report.writer import write_report
from eval_calibration_core.suites.invariants import check_invariants


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Evaluation & Calibration Core")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run evaluation suite")
    run_parser.add_argument("--suite", choices=["smoke", "determinism", "guard_pressure"], default="smoke")
    run_parser.add_argument("--in", type=Path, help="Input JSONL file (optional, uses fixture if not provided)")
    run_parser.add_argument("--out", type=Path, default=Path("reports/latest"), help="Output directory")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report from existing data")
    report_parser.add_argument("--out", type=Path, default=Path("reports/latest"), help="Output directory")

    args = parser.parse_args()

    # Check schema compatibility
    try:
        check_schema_compatibility()
    except RuntimeError as e:
        print(f"❌ Schema compatibility check failed: {e}")
        return

    if args.command == "run":
        _run_evaluation(args)
    elif args.command == "report":
        print("Report generation from existing data not yet implemented")
    else:
        parser.print_help()


def _run_evaluation(args: argparse.Namespace) -> None:
    """Run evaluation suite."""
    # Load packets
    if args.in:
        reader = PacketReader(args.in)
        packets = reader.read_all()
        suite_name = args.in.stem
    else:
        packets = load_fixture_suite(args.suite)
        suite_name = args.suite

    # Compute metrics
    metrics = compute_metrics(packets)

    # Check invariants
    invariant_results = check_invariants(packets)

    # Check contract matrix compatibility
    contract_ok, contract_details = check_expected_minor_range(expected_major=0, min_minor=2, max_minor=2)

    # Create report
    report = Report(
        schema_version=get_schema_version(),
        suite_name=suite_name,
        input_stats={"total_packets": len(packets)},
        metrics=metrics,
        invariant_results=invariant_results,
        contract_matrix_check=contract_details,
        contract_ok=contract_ok,
    )

    # Write report
    write_report(report, args.out)
    print(f"✅ Report written to {args.out}/report.json and {args.out}/report.md")


if __name__ == "__main__":
    main()
