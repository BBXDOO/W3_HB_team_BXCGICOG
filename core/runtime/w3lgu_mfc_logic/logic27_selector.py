from __future__ import annotations

from typing import Any

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text
from .event_field import EventField, event_field_from_mapping
from .logic27_registry import Logic27Slot, get_logic_slot

RISK_MARKERS = {"risk", "conflict", "review", "law", "governance"}
ROUTE_MARKERS = {"route", "handoff", "next", "transfer", "psp2"}
MEMORY_MARKERS = {"memory", "checkpoint", "record", "history", "lrc2", "continuity"}
BORROW_MARKERS = {"borrow", "external_field", "field_missing", "insufficient_field"}
SHADOW_MARKERS = {"shadow", "unclear", "fuzzy", "unknown"}


def _as_field(value: EventField | dict[str, Any]) -> EventField:
    if isinstance(value, EventField):
        return value
    return event_field_from_mapping(value)


def _field_text(field: EventField) -> str:
    return normalize_text(
        {
            "intent": field.intent,
            "context": dict(field.context),
            "signals": dict(field.signals),
        }
    ).lower()


def _choose_slot(field: EventField) -> Logic27Slot:
    text = _field_text(field)
    context = dict(field.context)

    if field.confidence < 0.35 or any(marker in text for marker in SHADOW_MARKERS):
        return get_logic_slot("L3-C2")
    if context.get("borrow_field") or any(marker in text for marker in BORROW_MARKERS):
        return get_logic_slot("L2-C8")
    if any(marker in text for marker in RISK_MARKERS):
        return get_logic_slot("L2-C3")
    if any(marker in text for marker in MEMORY_MARKERS):
        return get_logic_slot("L3-C5")
    if any(marker in text for marker in ROUTE_MARKERS):
        return get_logic_slot("L2-C1")
    return get_logic_slot("L1-C1")


def select_logic27(value: EventField | dict[str, Any]) -> object:
    """Select a local Logic27 slot for an EventField.

    This selector is a W3Lgu MFC reference proof. It keeps cross/event identity
    in the return details and does not claim authority over other systems.
    """

    field = _as_field(value)
    slot = _choose_slot(field)
    event_identity = {
        "chain_id": field.chain_id,
        "event_id": field.event_id,
        "sequence": field.sequence,
        "owner_scope": field.owner_scope,
    }

    status = slot.default_status
    if status == "REVIEW_REQUIRED":
        status_value = REVIEW_REQUIRED
    elif status == "WAIT":
        status_value = WAIT
    else:
        status_value = ACTIVE if status != "STOP" else "STOP"

    decision = f"logic27:{slot.name}"
    reason = f"selected {slot.slot_id} for local event-field reading"

    return make_result(
        module="LOGIC27",
        status=status_value,
        confidence=field.confidence,
        input_type="event_field:logic27",
        decision=decision,
        reason=reason,
        next_modules=slot.next_modules,
        standby=slot.standby_modules,
        details={
            "logic_slot": slot.to_dict(),
            "event_identity": event_identity,
            "event_field": field.to_dict(),
            "proposal_only": slot.proposal_only,
            "reference_only": True,
        },
    )
