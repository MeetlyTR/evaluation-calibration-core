"""Synthetic fixture suites for testing."""

from typing import Any

from decision_schema.packet_v2 import PacketV2


def load_fixture_suite(name: str) -> list[PacketV2]:
    """
    Load a synthetic fixture suite.
    
    Args:
        name: Suite name (e.g., "smoke", "determinism", "guard_pressure")
    
    Returns:
        List of PacketV2 packets
    
    Raises:
        ValueError: If suite name is unknown
    """
    suites = {
        "smoke": _smoke_suite(),
        "determinism": _determinism_suite(),
        "guard_pressure": _guard_pressure_suite(),
    }
    if name not in suites:
        raise ValueError(f"Unknown fixture suite: {name}. Available: {list(suites.keys())}")
    return suites[name]


def _smoke_suite() -> list[PacketV2]:
    """Minimal smoke test suite."""
    packets = []
    for step in range(10):
        packets.append(
            PacketV2(
                run_id="smoke-run",
                step=step,
                input={"ts": 1000 + step * 100},
                external={"mid": 0.5},
                mdm={"action": "HOLD", "confidence": 0.5},
                final_action={"action": "HOLD"},
                latency_ms=2,
                mismatch=None,
            )
        )
    return packets


def _determinism_suite() -> list[PacketV2]:
    """Suite for testing determinism."""
    packets = []
    for step in range(20):
        action = "ACT" if step % 3 == 0 else "HOLD"
        packets.append(
            PacketV2(
                run_id="determinism-run",
                step=step,
                input={"ts": 1000 + step * 100, "seed": 42},
                external={"mid": 0.5 + (step % 10) * 0.01},
                mdm={"action": action, "confidence": 0.6},
                final_action={"action": action},
                latency_ms=1 + (step % 5),
                mismatch=None,
            )
        )
    return packets


def _guard_pressure_suite() -> list[PacketV2]:
    """Suite with guard triggers."""
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
                input={"ts": 1000 + step * 100},
                external={"mid": 0.5},
                mdm={"action": "ACT", "confidence": 0.8},
                final_action={"action": "HOLD" if has_mismatch else "ACT"},
                latency_ms=3,
                mismatch=mismatch,
            )
        )
    return packets
