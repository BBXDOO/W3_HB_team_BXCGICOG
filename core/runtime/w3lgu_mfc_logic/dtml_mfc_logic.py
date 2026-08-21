from __future__ import annotations

from typing import Any, Dict, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, STOP, WAIT, make_result, normalize_text

REVIEW_MARKERS = {"risk", "conflict", "review", "governance", "law"}
CONTINUE_MARKERS = {"ready", "ok", "accepted", "trace", "route", "handoff", "checkpoint"}
REVIEW_SCOPES = {"cross_series", "external", "mixed", "unknown"}
RED_RISK_MARKERS = {"delete", "overwrite", "secret", "credential", "token"}
YELLOW_RISK_MARKERS = {"mutate", "execute", "deploy", "merge", "public"}


def _as_payload(decision_input: Any) -> Dict[str, Any]:
    if isinstance(decision_input, Mapping):
        return dict(decision_input)
    return {"text": normalize_text(decision_input)}


def _risk_level(payload: Dict[str, Any], text: str) -> str:
    declared = str(payload.get("risk") or "").lower()
    if declared in {"red", "yellow", "green"}:
        return declared
    if any(marker in text for marker in RED_RISK_MARKERS):
        return "red"
    if any(marker in text for marker in YELLOW_RISK_MARKERS):
        return "yellow"
    return "green"


def _review_state(payload: Dict[str, Any], text: str, risk: str) -> str:
    details = payload.get("details") if isinstance(payload.get("details"), Mapping) else {}
    route_scope = payload.get("route_scope") or details.get("route_scope")
    unknown_routes = payload.get("unknown_routes") or details.get("unknown_routes") or []
    cross_routes = payload.get("cross_routes") or details.get("cross_routes") or []
    bridge_contract = bool(payload.get("bridge_contract") or details.get("bridge_contract"))
    inspection = payload.get("inspection") if isinstance(payload.get("inspection"), Mapping) else {}

    if payload.get("stop_required") or payload.get("status") == STOP or risk == "red":
        return "stop"
    if risk == "yellow":
        return "review_required"
    if route_scope in REVIEW_SCOPES:
        return "review_required"
    if unknown_routes:
        return "review_required"
    if cross_routes and not bridge_contract:
        return "review_required"
    if payload.get("review_required"):
        return "review_required"
    if payload.get("status") == REVIEW_REQUIRED:
        return "review_required"
    if any(marker in text for marker in REVIEW_MARKERS):
        return "review_required"
    if any(marker in text for marker in CONTINUE_MARKERS):
        return "continue"
    if inspection.get("matrix_layer") and not inspection.get("chaos_area"):
        return "continue"
    return "unclear"


def trace_decision(decision_input: Any) -> object:
    """Build the authoritative DTML decision trace for every runtime entry."""

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
            details={"payload": payload, "review_state": "none", "risk": "green"},
        )

    risk = _risk_level(payload, text)
    markers = sorted(marker for marker in REVIEW_MARKERS if marker in text)
    review_state = _review_state(payload, text, risk)
    details = payload.get("details") if isinstance(payload.get("details"), Mapping) else {}
    route_scope = payload.get("route_scope") or details.get("route_scope", "local_w3lgu")
    unknown_routes = payload.get("unknown_routes") or details.get("unknown_routes") or []
    cross_routes = payload.get("cross_routes") or details.get("cross_routes") or []
    inspection = payload.get("inspection") if isinstance(payload.get("inspection"), Mapping) else {}
    trace = [
        "input_received",
        "context_checked",
        "risk_classified",
        "markers_scanned",
        f"route_scope:{route_scope}",
        f"risk:{risk}",
        f"review_state:{review_state}",
    ]
    common = {
        "trace": trace,
        "markers": markers,
        "risk": risk,
        "review_state": review_state,
        "route_scope": route_scope,
        "unknown_routes": list(unknown_routes),
        "cross_routes": list(cross_routes),
        "inspection": dict(inspection),
        "payload": payload,
    }

    if review_state == "stop":
        trace.append("stop_and_route_to_lrc2_checkpoint")
        return make_result(
            module="DTML",
            status=STOP,
            confidence=0.95,
            input_type="decision:risk_stop",
            decision="stop_suspicious_activity",
            reason="red-risk decision input must stop before downstream execution",
            next_modules=["LRC2"],
            standby=["REDR", "PSP2"],
            review=True,
            details=common,
        )

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
            review=True,
            details=common,
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
            details=common,
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
        review=True,
        details=common,
    )
