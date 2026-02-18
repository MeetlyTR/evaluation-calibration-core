# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Tests for invariant checks."""

from decision_schema.packet_v2 import PacketV2
from decision_schema.types import Action

from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.suites.invariants import check_invariants

# INVARIANT 5: canonical metric output keys (must match docs and compute.py)
EXPECTED_METRIC_KEYS = frozenset({
    "action_distribution",
    "guard_trigger_rates",
    "safety_invariant_pass_rate",
    "latency_percentiles",
    "total_steps",
})


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


def test_invariant_fail_closed_exception_path() -> None:
    """F8: Verify exception path invariant (allowed=False, mismatch=None => fail_closed marker)."""
    # Valid: Exception path with harness.fail_closed marker
    valid_exception = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={"harness.fail_closed": True, "now_ms": 1700000000000},
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD", "allowed": False},
        latency_ms=1,
        mismatch=None,  # Exception path: no mismatch
    )
    results = check_invariants([valid_exception])
    assert results["fail_closed"] is True

    # Valid: Exception path with other fail_closed marker (ops.fail_closed, etc.)
    valid_ops_exception = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={"ops.fail_closed": True},
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD", "allowed": False},
        latency_ms=1,
        mismatch=None,
    )
    results = check_invariants([valid_ops_exception])
    assert results["fail_closed"] is True

    # Invalid: Exception path without fail_closed marker
    invalid_exception = PacketV2(
        run_id="test",
        step=0,
        input={},
        external={},  # Missing fail_closed marker
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD", "allowed": False},
        latency_ms=1,
        mismatch=None,  # No mismatch but no marker
    )
    results = check_invariants([invalid_exception])
    assert results["fail_closed"] is False


def test_invariant_5_metric_key_set() -> None:
    """INVARIANT 5: metric output key set is fixed and matches docs."""
    empty_metrics = compute_metrics([])
    assert set(empty_metrics.keys()) == EXPECTED_METRIC_KEYS

    from eval_calibration_core.io.fixtures import load_fixture_suite
    packets = load_fixture_suite("smoke")
    non_empty_metrics = compute_metrics(packets)
    assert set(non_empty_metrics.keys()) == EXPECTED_METRIC_KEYS
