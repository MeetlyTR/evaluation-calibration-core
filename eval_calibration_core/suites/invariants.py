"""Invariant checks."""

from typing import Any

from decision_schema.packet_v2 import PacketV2
from decision_schema.types import Action


def check_invariants(packets: list[PacketV2]) -> dict[str, bool]:
    """
    Check mathematical invariants on packets.
    
    Returns:
        Dict mapping invariant name -> pass (True) or fail (False)
    """
    results = {
        "contract_closure": _check_contract_closure(packets),
        "confidence_clamp": _check_confidence_clamp(packets),
        "fail_closed": _check_fail_closed(packets),
        "packet_version": _check_packet_version(packets),
    }
    return results


def _check_contract_closure(packets: list[PacketV2]) -> bool:
    """Check: Proposal.action and FinalDecision.action must be in Action enum."""
    valid_actions = {a.value for a in Action}
    for packet in packets:
        mdm_action = packet.mdm.get("action")
        final_action = packet.final_action.get("action")
        if mdm_action not in valid_actions or final_action not in valid_actions:
            return False
    return True


def _check_confidence_clamp(packets: list[PacketV2]) -> bool:
    """Check: Proposal.confidence must be within [0,1]."""
    for packet in packets:
        confidence = packet.mdm.get("confidence")
        if confidence is not None:
            if not 0.0 <= confidence <= 1.0:
                return False
    return True


def _check_fail_closed(packets: list[PacketV2]) -> bool:
    """Check: If mismatch contains deny flags => allowed must be False."""
    for packet in packets:
        final_action = packet.final_action
        mismatch = packet.mismatch

        allowed = final_action.get("allowed", True)
        has_deny_flags = mismatch is not None and mismatch.get("flags", [])

        # Fail-closed: if deny flags exist, action must not be allowed
        if has_deny_flags and allowed:
            return False
    return True


def _check_packet_version(packets: list[PacketV2]) -> bool:
    """Check: PacketV2 has schema_version present."""
    for packet in packets:
        if not packet.schema_version:
            return False
    return True
