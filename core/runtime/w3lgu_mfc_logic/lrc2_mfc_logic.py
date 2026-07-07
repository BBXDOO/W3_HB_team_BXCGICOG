from __future__ import annotations

from hashlib import sha1
import json
from typing import Any, Dict, Mapping

from .contracts import ACTIVE, WAIT, make_result, normalize_text

PHASE_MARKERS = {
    "review": {"review", "risk", "conflict", "governance", "law"},
    "route": {"route", "handoff", "stamp", "package", "transfer"},
    "memory": {"memory", "checkpoint", "record", "history", "continuity"},
    "trace": {"trace", "decision", "timeline", "verify"},
}


def _as_payload(record: Any) -> Dict[str, Any]:
    if isinstance(record, Mapping):
        return dict(record)
    return {"text": normalize_text(record)}


def _stable_key(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return sha1(raw.encode("utf-8")).hexdigest()[:16]


def _record_phase(text: str) -> str:
    lowered = text.lower()
    for phase, markers in PHASE_MARKERS.items():
        if any(marker in lowered for marker in markers):
            return phase
    return "general"


def _extract_identity(payload: Mapping[str, Any]) -> Dict[str, Any]:
    details = payload.get("details") if isinstance(payload.get("details"), Mapping) else {}
    identity = details.get("identity") if isinstance(details.get("identity"), Mapping) else {}
    package = details.get("package") if isinstance(details.get("package"), Mapping) else payload.get("package", {})
    package_identity = package.get("identity") if isinstance(package, Mapping) and isinstance(package.get("identity"), Mapping) else {}

    merged: Dict[str, Any] = {}
    for source in (package_identity, identity, payload):
        if isinstance(source, Mapping):
            for key in ("chain_id", "event_id", "package_id", "route_stamp", "route_scope", "source", "target"):
                if key in source and source[key] not in (None, ""):
                    merged[key] = source[key]
    merged["mutated"] = False
    merged["traceable"] = True
    return merged


def checkpoint_lifecycle(record: Any) -> object:
    """Create a lifecycle checkpoint preview for W3Lgu module flow.

    LRC2 already has richer runtime behavior. This function gives the MFC layer
    a shared contract-shaped checkpoint result.
    """

    payload = _as_payload(record)
    text = normalize_text(payload)

    if not text:
        return make_result(
            module="LRC2",
            status=WAIT,
            confidence=0.0,
            input_type="empty",
            decision="wait_for_record",
            reason="no record was provided for checkpoint preview",
            next_modules=[],
            standby=["REDR", "PSP2", "DTML"],
            details={"payload": payload, "record_phase": "none"},
        )

    checkpoint_key = f"LRC2-{_stable_key(payload)}"
    record_phase = _record_phase(text)
    confidence = 0.85 if record_phase != "general" else 0.65
    identity = _extract_identity(payload)
    details = payload.get("details") if isinstance(payload.get("details"), Mapping) else {}

    return make_result(
        module="LRC2",
        status=ACTIVE,
        confidence=confidence,
        input_type="record:checkpoint_preview",
        decision="checkpoint_preview_ready",
        reason="record can be represented as a lifecycle checkpoint preview",
        next_modules=[],
        standby=["REDR", "PSP2", "DTML"],
        details={
            "checkpoint_key": checkpoint_key,
            "record_length": len(text),
            "record_phase": record_phase,
            "identity": identity,
            "route_stamp": identity.get("route_stamp") or details.get("route_stamp"),
            "prior_stage_summary": payload.get("reason") or payload.get("summary"),
            "payload": payload,
        },
    )
