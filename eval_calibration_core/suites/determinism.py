# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Determinism test suite."""

from decision_schema.packet_v2 import PacketV2


class DeterminismSuite:
    """Suite for testing determinism."""

    @staticmethod
    def generate(seed: int = 42) -> list[PacketV2]:
        """
        Generate determinism test packets.
        
        Args:
            seed: Random seed
        
        Returns:
            List of PacketV2 packets
        """
        packets = []
        for step in range(20):
            action = "ACT" if step % 3 == 0 else "HOLD"
            packets.append(
                PacketV2(
                    run_id="determinism-run",
                    step=step,
                    input={"ts": 1000 + step * 100, "seed": seed},
                    external={"mid": 0.5 + (step % 10) * 0.01},
                    mdm={"action": action, "confidence": 0.6},
                    final_action={"action": action},
                    latency_ms=1 + (step % 5),
                    mismatch=None,
                )
            )
        return packets
