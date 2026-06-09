"""PX — W3Lgu position exchange anchors.

PX is a pointer/position layer for cross-system alignment. It records where a
meaning came from, where it is being routed, and which W3Lgu packet/report it
references. PX does not execute, diagnose, or overwrite truth; it can only be
appended as an observation through W3DB append flow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from protocol.w3lgu.core import W3LguFiveLineProgram
from src.w3db.append_flow import AppendEnvelope, AppendFlowResult, build_append_envelope, append_envelope_to_w3db
from src.w3db.store import W3DBStore

PX_REFERENCES = (
    "protocol/w3lgu/RML01.md",
    "docs/standards/referencing_standard.md",
)


@dataclass(frozen=True)
class PXAnchor:
    """Immutable pointer between W3 systems.

    PX answers: source → relation → target, with references. It is a map marker,
    not the territory and not execution authority.
    """

    px_id: str
    source: str
    target: str
    subject: str
    relation: str = "references"
    mode: str = "observe"
    payload: Mapping[str, Any] = field(default_factory=dict)
    references: tuple[str, ...] = PX_REFERENCES

    def to_dict(self) -> dict[str, Any]:
        return {
            "px_id": self.px_id,
            "source": self.source,
            "target": self.target,
            "subject": self.subject,
            "relation": self.relation,
            "mode": self.mode,
            "payload": dict(self.payload),
            "references": list(self.references),
        }


def px_from_five_line(
    program: W3LguFiveLineProgram,
    *,
    relation: str = "w3lgu.cross_reference",
    mode: str = "observe",
    extra_payload: Mapping[str, Any] | None = None,
) -> PXAnchor:
    """Create a PX anchor from a W3Lgu five-line program."""

    source = program.memory.get("SOURCE") or program.event.get("SOURCE") or "W3Lgu"
    target = program.law.get("TARGET") or program.event.get("TARGET") or "W3DB"
    subject = program.event.get("INTENT") or program.event.get("TASK") or program.event.to_text()
    payload = {
        "memory": program.memory.to_dict(),
        "patch": program.patch.to_dict(),
        "law": program.law.to_dict(),
        "event": program.event.to_dict(),
        "signal": program.signal.to_dict(),
    }
    if extra_payload:
        payload["extra"] = dict(extra_payload)
    envelope = build_append_envelope(
        kind="PX",
        source=source,
        target=target,
        subject=subject,
        payload=payload,
        references=PX_REFERENCES + tuple(program.references),
    )
    return PXAnchor(
        px_id=envelope.append_id.replace("APP-PX-", "PX-"),
        source=source,
        target=target,
        subject=subject,
        relation=relation,
        mode=mode,
        payload=payload,
        references=envelope.references,
    )


def px_to_append_envelope(px: PXAnchor, *, confidence: float = 0.5) -> AppendEnvelope:
    """Convert PX to an append-only W3DB envelope."""

    return build_append_envelope(
        kind="PX",
        source=px.source,
        target=px.target,
        subject=px.subject,
        payload=px.to_dict(),
        confidence=confidence,
        references=px.references,
    )


def append_px_to_w3db(
    px: PXAnchor,
    *,
    store: W3DBStore | None = None,
    confidence: float = 0.5,
    idempotent: bool = True,
) -> AppendFlowResult:
    """Append a PX anchor to W3DB without mutating the PX source."""

    envelope = px_to_append_envelope(px, confidence=confidence)
    return append_envelope_to_w3db(envelope, store=store, cix_id="PX", idempotent=idempotent)
