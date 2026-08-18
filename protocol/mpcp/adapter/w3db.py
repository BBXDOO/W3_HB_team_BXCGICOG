"""MPCP to W3DB append-candidate bridge."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def build_w3db_evidence_candidate(
    *,
    chain_id: str,
    event_id: str,
    result: Mapping[str, Any],
) -> dict:
    """Use W3DB's real append contract without performing a write."""
    from src.w3db.append_flow import build_append_envelope

    envelope = build_append_envelope(
        kind="mpcp-result",
        source="MPCP",
        subject=event_id,
        payload={
            "chain_id": chain_id,
            "event_id": event_id,
            "state": result.get("state"),
            "reason": result.get("reason"),
            "mutated": bool(result.get("mutated", False)),
            "source_truth_mutated": bool(result.get("source_truth_mutated", False)),
            "review": bool(result.get("review", False)),
        },
        references=(f"chain:{chain_id}", f"event:{event_id}"),
    )
    return {
        "operation": "append_candidate",
        "approved_for_append": False,
        "envelope": envelope.to_dict(),
        "mutated": False,
    }
