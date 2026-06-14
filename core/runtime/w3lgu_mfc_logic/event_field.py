from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Mapping
from uuid import uuid4

from .contracts import clamp_confidence, normalize_text

LOCAL_OWNER_SCOPE = "W3LGU_MFC_REFERENCE_ONLY"


@dataclass(frozen=True)
class EventField:
    """Local event-field object for W3Lgu MFC experiments.

    This object keeps chain and event identity visible while the local MFC logic
    selects a route. It is a local reference shape, not an authority model for
    other systems.
    """

    chain_id: str
    event_id: str
    sequence: int
    source: str
    intent: str
    context: Mapping[str, Any] = field(default_factory=dict)
    signals: Mapping[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    mutated: bool = False
    traceable: bool = True
    owner_scope: str = LOCAL_OWNER_SCOPE
    borrowed_from: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not normalize_text(self.chain_id):
            raise ValueError("chain_id is required for EventField")
        if not normalize_text(self.event_id):
            raise ValueError("event_id is required for EventField")
        if self.sequence < 1:
            raise ValueError("sequence must be >= 1")
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))
        object.__setattr__(self, "context", dict(self.context))
        object.__setattr__(self, "signals", dict(self.signals))
        object.__setattr__(self, "borrowed_from", tuple(self.borrowed_from))

    def to_dict(self) -> dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "event_id": self.event_id,
            "sequence": self.sequence,
            "source": self.source,
            "intent": self.intent,
            "context": dict(self.context),
            "signals": dict(self.signals),
            "confidence": self.confidence,
            "mutated": self.mutated,
            "traceable": self.traceable,
            "owner_scope": self.owner_scope,
            "borrowed_from": list(self.borrowed_from),
        }

    def with_borrowed_field(self, system_name: str) -> "EventField":
        borrowed = tuple(dict.fromkeys((*self.borrowed_from, system_name)))
        return replace(self, borrowed_from=borrowed)


def build_event_field(
    *,
    chain_id: str | None = None,
    event_id: str | None = None,
    sequence: int = 1,
    source: str = "W3Lgu-MFC",
    intent: str = "observe",
    context: Mapping[str, Any] | None = None,
    signals: Mapping[str, Any] | None = None,
    confidence: float = 0.5,
    owner_scope: str = LOCAL_OWNER_SCOPE,
) -> EventField:
    """Create a local EventField.

    Missing ids are generated only for this local reference layer. System owners
    should pass their own chain_id and event_id when integrating.
    """

    return EventField(
        chain_id=chain_id or f"local-chain-{uuid4()}",
        event_id=event_id or f"local-event-{uuid4()}",
        sequence=sequence,
        source=source,
        intent=intent,
        context=dict(context or {}),
        signals=dict(signals or {}),
        confidence=confidence,
        owner_scope=owner_scope,
    )


def event_field_from_mapping(data: Mapping[str, Any]) -> EventField:
    return build_event_field(
        chain_id=data.get("chain_id"),
        event_id=data.get("event_id"),
        sequence=int(data.get("sequence", 1)),
        source=str(data.get("source", "W3Lgu-MFC")),
        intent=str(data.get("intent", "observe")),
        context=data.get("context") if isinstance(data.get("context"), Mapping) else {},
        signals=data.get("signals") if isinstance(data.get("signals"), Mapping) else {},
        confidence=float(data.get("confidence", 0.5)),
        owner_scope=str(data.get("owner_scope", LOCAL_OWNER_SCOPE)),
    )
