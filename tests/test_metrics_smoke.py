"""Smoke tests for metrics computation."""

from eval_calibration_core.io.fixtures import load_fixture_suite
from eval_calibration_core.metrics.compute import compute_metrics


def test_compute_metrics_smoke() -> None:
    """Verify metrics computation works."""
    packets = load_fixture_suite("smoke")
    metrics = compute_metrics(packets)

    assert "action_distribution" in metrics
    assert "guard_trigger_rates" in metrics
    assert "safety_invariant_pass_rate" in metrics
    assert "latency_percentiles" in metrics
    assert "total_steps" in metrics
    assert metrics["total_steps"] == 10


def test_compute_metrics_empty() -> None:
    """Verify metrics computation handles empty list."""
    metrics = compute_metrics([])
    assert metrics["total_steps"] == 0
    assert metrics["safety_invariant_pass_rate"] == 1.0


def test_compute_metrics_guard_pressure() -> None:
    """Verify metrics computation on guard pressure suite."""
    packets = load_fixture_suite("guard_pressure")
    metrics = compute_metrics(packets)

    # Should have guard triggers
    assert len(metrics["guard_trigger_rates"]) > 0
    assert "max_exposure_exceeded" in metrics["guard_trigger_rates"]
