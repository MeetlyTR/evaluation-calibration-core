# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Smoke test: build_report produces report with INVARIANT 5 metric key set."""

from eval_calibration_core.io.fixtures import load_fixture_suite
from eval_calibration_core.report import build_report

EXPECTED_METRIC_KEYS = frozenset({
    "action_distribution",
    "guard_trigger_rates",
    "safety_invariant_pass_rate",
    "latency_percentiles",
    "total_steps",
})


def test_build_report_smoke() -> None:
    """build_report(packets) yields Report with metrics key set == EXPECTED_METRIC_KEYS."""
    packets = load_fixture_suite("smoke")
    report = build_report(packets, suite_name="smoke")
    assert set(report.metrics.keys()) == EXPECTED_METRIC_KEYS
    assert report.contract_matrix_check is not None
    assert "compatible" in report.contract_matrix_check
    assert report.invariant_results
