"""Guard pressure test suite."""

from decision_schema.packet_v2 import PacketV2


class GuardPressureSuite:
    """Suite with guard triggers."""

    @staticmethod
    def generate(seed: int = 42) -> list[PacketV2]:
        """
        Generate guard pressure test packets.
        
        Args:
            seed: Random seed
        
        Returns:
            List of PacketV2 packets
        """
        packets = []
        for step in range(20):
            # Every 5th step triggers a guard
            has_mismatch = step % 5 == 0
            mismatch = (
                {
                    "flags": ["exposure_limit"],
                    "reason_codes": ["max_exposure_exceeded"],
                }
                if has_mismatch
                else None
            )
            packets.append(
                PacketV2(
                    run_id="guard-pressure-run",
                    step=step,
                    input={"ts": 1000 + step * 100, "seed": seed},
                    external={"mid": 0.5},
                    mdm={"action": "ACT", "confidence": 0.8},
                    final_action={"action": "HOLD" if has_mismatch else "ACT"},
                    latency_ms=3,
                    mismatch=mismatch,
                )
            )
        return packets
