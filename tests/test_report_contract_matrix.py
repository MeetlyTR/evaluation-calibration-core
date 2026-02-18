# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Test contract matrix check in reports."""

from pathlib import Path

from eval_calibration_core.contracts import check_expected_minor_range
from eval_calibration_core.io.fixtures import load_fixture_suite
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report.model import Report
from eval_calibration_core.report.writer import write_report
from eval_calibration_core.suites.invariants import check_invariants


def test_report_includes_contract_matrix_check(tmp_path: Path) -> None:
    """Test that report includes contract_matrix_check."""
    # Load minimal fixture
    packets = load_fixture_suite("smoke")
    
    # Compute metrics
    metrics = compute_metrics(packets)
    
    # Check invariants
    invariant_results = check_invariants(packets)
    
    # Check contract compatibility
    contract_ok, contract_details = check_expected_minor_range(expected_major=0, min_minor=2, max_minor=2)
    
    # Create report
    report = Report(
        schema_version="0.2.0",
        suite_name="smoke",
        input_stats={"total_packets": len(packets)},
        metrics=metrics,
        invariant_results=invariant_results,
        contract_matrix_check=contract_details,
    )
    
    # Write report
    write_report(report, tmp_path)
    
    # Read JSON report
    json_path = tmp_path / "report.json"
    import json
    with open(json_path, "r", encoding="utf-8") as f:
        report_dict = json.load(f)
    
    # Verify contract_matrix_check exists
    assert "contract_matrix_check" in report_dict
    check = report_dict["contract_matrix_check"]
    assert "schema_version" in check
    assert "compatible" in check
    assert check["compatible"] is True  # Should be compatible with 0.2.x
    
    # Verify Markdown includes contract check
    md_path = tmp_path / "report.md"
    md_content = md_path.read_text(encoding="utf-8")
    assert "Contract Matrix Check" in md_content
    assert "✅ PASS" in md_content or "❌ FAIL" in md_content
