"""Compute metrics from PacketV2 traces."""

from typing import Any

from decision_schema.packet_v2 import PacketV2

from eval_calibration_core.metrics.definitions import MetricDefinitions


def compute_metrics(packets: list[PacketV2]) -> dict[str, Any]:
    """
    Compute all metrics from packets.
    
    Args:
        packets: List of PacketV2 packets
    
    Returns:
        Dict containing all computed metrics
    """
    if not packets:
        return {
            "action_distribution": {},
            "guard_trigger_rates": {},
            "safety_invariant_pass_rate": 1.0,
            "latency_percentiles": {"p50": 0.0, "p95": 0.0, "p99": 0.0},
            "total_steps": 0,
        }

    return {
        "action_distribution": MetricDefinitions.action_distribution(packets),
        "guard_trigger_rates": MetricDefinitions.guard_trigger_rate(packets),
        "safety_invariant_pass_rate": MetricDefinitions.safety_invariant_pass_rate(packets),
        "latency_percentiles": MetricDefinitions.latency_percentiles(packets),
        "total_steps": len(packets),
    }
