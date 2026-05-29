"""Codex W3 implementation-agent contracts.

This module keeps Codex behavior explicit and testable. It is an adapter/helper
layer for planning implementation work; it does not write to W3DB, MPCP,
EP_SIGNAL, or governance ledgers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

CODEX_VERSION = "0.1.0"
MANIFEST_PATH = Path(__file__).resolve().parent / "modules.json"
_REQUIRED_BOUNDARIES = (
    "human_review_required",
    "governance_gate_required",
    "no_truth_mutation",
    "no_self_merge",
)


@dataclass(frozen=True)
class CodexExecutionPacket:
    """Traceable, immutable execution packet for Codex work intake."""

    id: str
    timestamp: str
    source: str
    intent: str
    target: str
    mode: str
    status: str
    w3lgu: str
    governance: Mapping[str, bool]
    handoffs: tuple[str, ...] = field(default_factory=tuple)
    references: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "source": self.source,
            "intent": self.intent,
            "target": self.target,
            "mode": self.mode,
            "status": self.status,
            "w3lgu": self.w3lgu,
            "governance": dict(self.governance),
            "handoffs": list(self.handoffs),
            "references": list(self.references),
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_manifest(path: str | Path = MANIFEST_PATH) -> dict[str, Any]:
    """Load the Codex module manifest without side effects."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_manifest(manifest: Mapping[str, Any]) -> list[str]:
    """Return deterministic manifest validation errors.

    The checks focus on W3 boundaries: Codex must remain an implementation
    executor and must not claim authority to approve, merge, or mutate truth.
    """

    errors: list[str] = []
    if manifest.get("name") != "Codex":
        errors.append("manifest.name must be Codex")
    if manifest.get("class") != "implementation_executor":
        errors.append("manifest.class must be implementation_executor")

    boundaries = manifest.get("boundaries", {})
    if not isinstance(boundaries, Mapping):
        errors.append("manifest.boundaries must be an object")
    else:
        for key in _REQUIRED_BOUNDARIES:
            if boundaries.get(key) is not True:
                errors.append(f"boundaries.{key} must be true")

    forbidden = set(manifest.get("forbidden_authority", []))
    for action in ("approve_truth", "merge_pr", "bypass_governance"):
        if action not in forbidden:
            errors.append(f"forbidden_authority must include {action}")

    handoffs = manifest.get("handoffs", {})
    if not isinstance(handoffs, Mapping):
        errors.append("manifest.handoffs must be an object")
    else:
        for required in ("governance", "verification", "final_authority"):
            if required not in handoffs:
                errors.append(f"handoffs.{required} is required")

    return sorted(errors)


def build_execution_packet(
    intent: str,
    *,
    source: str = "BBX19",
    target: str = "repository",
    mode: str = "implementation",
    timestamp: str | None = None,
    event_id: str | None = None,
) -> CodexExecutionPacket:
    """Build a non-mutating Codex execution packet.

    The generated W3Lgu packet is intentionally five lines and mirrors the W3Lgu
    law style used elsewhere in the repo. It is a trace artifact, not an
    execution approval.
    """

    manifest = load_manifest()
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("Invalid Codex manifest: " + "; ".join(errors))

    packet_id = event_id or str(uuid4())
    now = timestamp or _utc_now()
    safe_target = target or "repository"
    safe_mode = mode or "implementation"
    w3lgu = "\n".join(
        (
            f"MEM:source={source};agent=Codex",
            f"PATCH:mode={safe_mode};mutation=proposal_or_branch_only",
            f"LAW:target={safe_target};review=required",
            f"EVENT:intent={intent}",
            "SIGNAL:status=implementation_ready;truth_mutation=false",
        )
    )

    return CodexExecutionPacket(
        id=packet_id,
        timestamp=now,
        source=source,
        intent=intent,
        target=safe_target,
        mode=safe_mode,
        status="ready_for_human_review",
        w3lgu=w3lgu,
        governance={
            "human_review_required": True,
            "governance_gate_required": True,
            "truth_mutation_allowed": False,
            "self_merge_allowed": False,
        },
        handoffs=tuple(manifest["handoffs"].values()),
        references=tuple(manifest.get("references", [])),
    )
