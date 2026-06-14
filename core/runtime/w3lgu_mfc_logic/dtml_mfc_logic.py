from __future__ import annotations

from typing import Any, Dict, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text

REVIEW_MARKERS = {"risk", "conflict", "review", "governance", "law"}
CONTINUE_MARKERS = {"ready", "ok", "accepted", "trace", "route", "handoff", "checkpoint"}


def _as_payload(decision_input: Any) -> Dict[str, Any]:
    if isinstance(decision_input, Mapping):
        return dict(decision_input)
    return {"text": normalize_text(decision_input)}


def _review_state(payload: Dict[str, Any], text: str) -> str:
    if payload.get("review_required"):
        return "review_required"
    if payload.get("status") == REVIEW_REQUIRED:
        return "review_required"
    if any(marker in text for marker in REVIEW_MARKERS):
        return "review_required"
    if any(marker in text for marker in CONTINUE_MARKERS):
        return "continue"
    return "unclear"


def trace_decision(decision_input: Any) -> object:
    """Build a standard minimum decision trace map for W3Lgu flow review."""

    payload = _as_payload(decision_input)
    text = normalize_text(payload).lower()

    if not text:
        return make_result(
            module="DTML",
            status=WAIT,
            confidence=0.0,
            input_type="empty",
            decision="wait_for_decision_input",
            reason="no decision input was provided",
            next_modules=[],
            standby=["REDR", "PSP2", "LRC2"],
            details={"payload": payload, "review_state": "none"},
        )

    markers = sorted(marker for marker in REVIEW_MARKERS if marker in text)
    review_state = _review_state(payload, text)
    trace = [
        "input_received",
        "context_checked",
        "markers_scanned",
        f"review_state:{review_state}",
    ]

    if review_state == "review_required":
        trace.append("route_to_lrc2_review_checkpoint")
        return make_result(
            module="DTML",
            status=REVIEW_REQUIRED,
            confidence=0.85,
            input_type="decision:trace",
            decision="review_trace_required",
            reason="decision input requires review before continuing",
            next_modules=["LRC2"],
            standby=["REDR", "PSP2"],
            details={"trace": trace, "markers": markers, "review_state": review_state, "payload": payload},
        )

    if review_state == "continue":
        trace.append("trace_ready")
        return make_result(
            module="DTML",
            status=ACTIVE,
            confidence=0.75,
            input_type="decision:trace",
            decision="decision_trace_ready",
            reason="decision input is traceable and can continue",
            next_modules=["PSP2", "LRC2"],
            standby=["REDR"],
            details={"trace": trace, "markers": markers, "review_state": review_state, "payload": payload},
        )

    trace.append("clarify_before_route")
    return make_result(
        module="DTML",
        status=WAIT,
        confidence=0.5,
        input_type="decision:unclear",
        decision="wait_for_clearer_decision_context",
        reason="decision input is traceable but route intent is unclear",
        next_modules=[],
        standby=["REDR", "PSP2", "LRC2"],
        details={"trace": trace, "markers": markers, "review_state": review_state, "payload": payload},
    )
