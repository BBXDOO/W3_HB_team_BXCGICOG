from __future__ import annotations

from typing import Any, Dict, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text


REVIEW_MARKERS = {"risk", "conflict", "review", "parser", "runtime", "governance"}


def _as_payload(decision_input: Any) -> Dict[str, Any]:
    if isinstance(decision_input, Mapping):
        return dict(decision_input)
    return {"text": normalize_text(decision_input)}


def trace_decision(decision_input: Any) -> object:
    """Build a minimum decision trace map for W3Lgu flow review."""

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
            details={"payload": payload},
        )

    markers = sorted(marker for marker in REVIEW_MARKERS if marker in text)
    needs_review = bool(markers or payload.get("review_required"))
    trace = ["input_received", "boundary_checked", "markers_scanned"]

    if needs_review:
        trace.append("review_required")
        return make_result(
            module="DTML",
            status=REVIEW_REQUIRED,
            confidence=0.85,
            input_type="decision:trace",
            decision="review_trace_required",
            reason="decision input requires review before continuing",
            next_modules=["LRC2"],
            standby=["REDR", "PSP2"],
            details={"trace": trace, "markers": markers, "payload": payload},
        )

    trace.append("trace_ready")
    return make_result(
        module="DTML",
        status=ACTIVE,
        confidence=0.7,
        input_type="decision:trace",
        decision="decision_trace_ready",
        reason="decision input is traceable",
        next_modules=["PSP2", "LRC2"],
        standby=["REDR"],
        details={"trace": trace, "markers": markers, "payload": payload},
    )
