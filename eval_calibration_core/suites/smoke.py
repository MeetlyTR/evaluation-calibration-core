# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Smoke test suite."""

from typing import Any

from decision_schema.packet_v2 import PacketV2


class SmokeSuite:
    """Minimal smoke test suite."""

    @staticmethod
    def generate(seed: int = 42) -> list[PacketV2]:
        """
        Generate smoke test packets.
        
        Args:
            seed: Random seed (for determinism)
        
        Returns:
            List of PacketV2 packets
        """
        packets = []
        for step in range(10):
            packets.append(
                PacketV2(
                    run_id="smoke-run",
                    step=step,
                    input={"ts": 1000 + step * 100, "seed": seed},
                    external={"mid": 0.5},
                    mdm={"action": "HOLD", "confidence": 0.5},
                    final_action={"action": "HOLD"},
                    latency_ms=2,
                    mismatch=None,
                )
            )
        return packets
