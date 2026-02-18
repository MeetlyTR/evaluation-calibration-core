# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Metric definitions and mathematical formulas."""

from dataclasses import dataclass
from typing import Any


@dataclass
class MetricDefinitions:
    """
    Mathematical definitions for metrics.
    
    All metrics are computed from PacketV2 traces.
    """

    @staticmethod
    def action_distribution(packets: list[Any]) -> dict[str, int]:
        """
        Compute action distribution.
        
        Formula:
            count(action) = number of packets with final_action.action == action
            rate(action) = count(action) / total_steps
        
        Args:
            packets: List of PacketV2 packets
        
        Returns:
            Dict mapping action -> count
        """
        from collections import Counter

        actions = [p.final_action.get("action", "UNKNOWN") for p in packets]
        return dict(Counter(actions))

    @staticmethod
    def guard_trigger_rate(packets: list[Any]) -> dict[str, float]:
        """
        Compute guard trigger rate per reason code.
        
        Formula:
            trigger_rate(code) = triggers(code) / total_steps
        
        Args:
            packets: List of PacketV2 packets
        
        Returns:
            Dict mapping reason_code -> trigger_rate
        """
        from collections import Counter

        total_steps = len(packets)
        if total_steps == 0:
            return {}

        trigger_counts: Counter[str] = Counter()
        for packet in packets:
            if packet.mismatch:
                reason_codes = packet.mismatch.get("reason_codes", [])
                for code in reason_codes:
                    trigger_counts[code] += 1

        return {code: count / total_steps for code, count in trigger_counts.items()}

    @staticmethod
    def safety_invariant_pass_rate(packets: list[Any]) -> float:
        """
        Compute safety invariant pass rate.
        
        Formula:
            inv_pass = passed_checks / total_checks
        
        Invariant: If FinalDecision.allowed == True => mismatch is None and no deny flags
        
        Args:
            packets: List of PacketV2 packets
        
        Returns:
            Pass rate [0.0, 1.0]
        """
        if not packets:
            return 1.0

        passed = 0
        total = len(packets)

        for packet in packets:
            final_action = packet.final_action
            mismatch = packet.mismatch

            # Check: allowed implies no mismatch
            allowed = final_action.get("allowed", True)
            if allowed:
                if mismatch is None or not mismatch.get("flags", []):
                    passed += 1
            else:
                # Denied actions should have mismatch
                if mismatch is not None:
                    passed += 1

        return passed / total if total > 0 else 1.0

    @staticmethod
    def latency_percentiles(packets: list[Any]) -> dict[str, float]:
        """
        Compute latency percentiles using nearest-rank method.
        
        Formula (nearest-rank):
            p_k = value at index = floor((k/100) * n)
            For k=95, n=100: index = 95 (0-indexed: 94)
        
        Method: Nearest-rank (deterministic, simple)
        - Alternative: Linear interpolation (smoother but more complex)
        - For small n, p95 and p99 may equal max value (expected behavior)
        
        Args:
            packets: List of PacketV2 packets
        
        Returns:
            Dict with p50, p95, p99 keys (milliseconds)
        """
        latencies = [p.latency_ms for p in packets if hasattr(p, "latency_ms")]
        if not latencies:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0}

        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)

        def percentile(p: float) -> float:
            """Nearest-rank percentile: index = floor((p/100) * n)."""
            idx = int((p / 100.0) * n)
            return sorted_latencies[min(idx, n - 1)]

        return {
            "p50": percentile(50),
            "p95": percentile(95),
            "p99": percentile(99),
        }
