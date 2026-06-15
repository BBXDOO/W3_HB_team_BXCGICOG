from __future__ import annotations

from typing import Any, Dict, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text


RISK_WORDS = {
    "risk",
    "error",
    "fail",
    "failed",
    "failure",
    "conflict",
    "reject",
    "rejected",
    "blocked",
    "unsafe",
    "mutation",
    "mutate",
    "runtime",
    "parser",
    "source-truth",
    "source_truth",
}

ROUTE_WORDS = {"route", "handoff", "dispatch", "transfer", "package", "stamp"}
MEMORY_WORDS = {"memory", "checkpoint", "lifecycle", "record", "history", "continuity"}
TRACE_WORDS = {"decision", "trace", "law", "verify", "review", "governance"}


def _as_payload(event: Any) -> Dict[str, Any]:
    if isinstance(event, Mapping):
        return dict(event)
    return {"text": normalize_text(event)}


def classify_event(event: Any) -> object:
    """Classify an incoming W3Lgu event into the next safe module path.

    REDR's minimum functional concept is not execution. It reads an event,
    detects risk/route/memory/trace intent, and returns a non-mutating routing
    decision.
    """

    payload = _as_payload(event)
    text = normalize_text(payload).lower()

    if not text:
        return make_result(
            module="REDR",
            status=WAIT,
            confidence=0.0,
            input_type="empty",
            decision="wait_for_event",
            reason="no event text or payload was provided",
            next_modules=[],
            standby=["PSP2", "DTML", "LRC2"],
            details={"payload": payload},
        )

    found_risk = sorted(word for word in RISK_WORDS if word in text)
    found_route = sorted(word for word in ROUTE_WORDS if word in text)
    found_memory = sorted(word for word in MEMORY_WORDS if word in text)
    found_trace = sorted(word for word in TRACE_WORDS if word in text)

    if found_risk:
        return make_result(
            module="REDR",
            status=REVIEW_REQUIRED,
            confidence=0.9,
            input_type="event:risk",
            decision="route_to_dtml_review",
            reason="risk markers detected before routing",
            next_modules=["DTML"],
            standby=["PSP2", "LRC2"],
            details={"markers": found_risk, "payload": payload},
        )

    if found_trace:
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.75,
            input_type="event:trace",
            decision="route_to_dtml_trace",
            reason="decision or trace markers detected",
            next_modules=["DTML", "PSP2"],
            standby=["LRC2"],
            details={"markers": found_trace, "payload": payload},
        )

    if found_route:
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.75,
            input_type="event:route",
            decision="route_to_psp2_handoff",
            reason="route or handoff markers detected",
            next_modules=["PSP2"],
            standby=["DTML", "LRC2"],
            details={"markers": found_route, "payload": payload},
        )

    if found_memory:
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.7,
            input_type="event:memory",
            decision="route_to_lrc2_checkpoint",
            reason="memory or lifecycle markers detected",
            next_modules=["LRC2"],
            standby=["PSP2", "DTML"],
            details={"markers": found_memory, "payload": payload},
        )

    return make_result(
        module="REDR",
        status=ACTIVE,
        confidence=0.5,
        input_type="event:general",
        decision="package_event_for_route_selection",
        reason="event accepted but no strong module marker detected",
        next_modules=["PSP2"],
        standby=["DTML", "LRC2"],
        details={"payload": payload},
    )
