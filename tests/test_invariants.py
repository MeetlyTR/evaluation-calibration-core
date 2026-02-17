"""Tests for invariant checks."""

from decision_schema.packet_v2 import PacketV2
from decision_schema.types import Action

from eval_calibration_core.suites.invariants import check_invariants


def test_invariant_contract_closure() -> None:
    """Verify contract closure invariant."""
    # Valid packet
    valid_packet = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD"},
        latency_ms=1,
    )
    results = check_invariants([valid_packet])
    assert results["contract_closure"] is True

    # Invalid packet (action not in enum)
    invalid_packet = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "INVALID_ACTION"},
        final_action={"action": "INVALID_ACTION"},
        latency_ms=1,
    )
    results = check_invariants([invalid_packet])
    assert results["contract_closure"] is False


def test_invariant_confidence_clamp() -> None:
    """Verify confidence clamp invariant."""
    # Valid confidence
    valid_packet = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "HOLD", "confidence": 0.5},
        final_action={"action": "HOLD"},
        latency_ms=1,
    )
    results = check_invariants([valid_packet])
    assert results["confidence_clamp"] is True

    # Invalid confidence (> 1.0)
    invalid_packet = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "HOLD", "confidence": 1.5},
        final_action={"action": "HOLD"},
        latency_ms=1,
    )
    results = check_invariants([invalid_packet])
    assert results["confidence_clamp"] is False


def test_invariant_fail_closed() -> None:
    """Verify fail-closed invariant."""
    # Allowed with no mismatch (valid)
    valid_packet = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "ACT"},
        final_action={"action": "ACT", "allowed": True},
        latency_ms=1,
        mismatch=None,
    )
    results = check_invariants([valid_packet])
    assert results["fail_closed"] is True

    # Denied with mismatch (valid)
    valid_denied = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "ACT"},
        final_action={"action": "HOLD", "allowed": False},
        latency_ms=1,
        mismatch={"flags": ["exposure_limit"]},
    )
    results = check_invariants([valid_denied])
    assert results["fail_closed"] is True

    # Allowed with mismatch (invalid - fail-open)
    invalid_packet = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},
        mdm={"action": "ACT"},
        final_action={"action": "ACT", "allowed": True},
        latency_ms=1,
        mismatch={"flags": ["exposure_limit"]},  # Should not be allowed
    )
    results = check_invariants([invalid_packet])
    assert results["fail_closed"] is False
