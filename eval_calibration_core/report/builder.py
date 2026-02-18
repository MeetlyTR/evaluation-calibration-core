# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Build Report from PacketV2 list (metrics + invariants + contract check)."""

from decision_schema import __version__ as schema_version

from eval_calibration_core.contracts import check_expected_minor_range
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report.model import Report
from eval_calibration_core.suites.invariants import check_invariants


def build_report(
    packets: list,
    suite_name: str = "default",
    expected_schema_minor: int = 2,
) -> Report:
    """
    Build a Report from packets: compute metrics, check invariants, check schema compat.

    Args:
        packets: List of PacketV2 instances
        suite_name: Suite identifier
        expected_schema_minor: Expected decision-schema minor (default 2 for 0.2.x)

    Returns:
        Report instance (use write_report(report, output_dir) to write files)
    """
    metrics = compute_metrics(packets)
    invariant_results = check_invariants(packets)
    contract_ok, contract_details = check_expected_minor_range(
        expected_major=0, min_minor=expected_schema_minor, max_minor=expected_schema_minor
    )
    return Report(
        report_version="0.1.0",
        schema_version=schema_version,
        suite_name=suite_name,
        input_stats={"total_packets": len(packets)},
        metrics=metrics,
        invariant_results=invariant_results,
        contract_matrix_check=contract_details,
        contract_ok=contract_ok,
    )
