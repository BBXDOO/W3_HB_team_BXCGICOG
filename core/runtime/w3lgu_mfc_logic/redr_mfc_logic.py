from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text


RISK_WORDS = {
    "risk", "error", "fail", "failed", "failure", "conflict",
    "reject", "rejected", "blocked", "unsafe", "mutation", "mutate",
    "runtime", "parser", "source-truth", "source_truth",
}

ROUTE_WORDS = {"route", "handoff", "dispatch", "transfer", "package", "stamp"}
MEMORY_WORDS = {"memory", "checkpoint", "lifecycle", "record", "history", "continuity"}
TRACE_WORDS = {"decision", "trace", "law", "verify", "review", "governance"}
STRUCTURE_WORDS = {"module", "file", "folder", "path", "structure", "tree", "schema"}
SIGNAL_WORDS = {"signal", "state", "color", "sym", "rytm", "rhythm"}
IDENTITY_FIELDS = (
    "chain_id",
    "process_id",
    "event_id",
    "package_id",
    "sequence",
    "source",
    "target",
    "route_scope",
    "predecessor",
    "successor",
    "owner_scope",
)


def _as_payload(event: Any) -> Dict[str, Any]:
    if isinstance(event, Mapping):
        return dict(event)
    return {"text": normalize_text(event)}


def _payload_text(payload: Mapping[str, Any]) -> str:
    text_value = payload.get("text")
    if isinstance(text_value, str):
        return normalize_text(text_value)
    return normalize_text(payload)


def _stable_package_id(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"REDR-PKG-{digest}"


def _identity_map(payload: Mapping[str, Any]) -> Dict[str, Any]:
    identity: Dict[str, Any] = {}
    unknown = []
    for field in IDENTITY_FIELDS:
        value = payload.get(field)
        if value in (None, ""):
            unknown.append(field)
        else:
            identity[field] = value

    identity.setdefault("package_id", payload.get("package_id") or _stable_package_id(payload))
    identity["mutated"] = False
    identity["traceable"] = True
    if unknown:
        identity["unknown"] = {
            "fields": unknown,
            "reason": "missing_from_input",
            "review": True,
        }
    return identity


def _find_markers(text: str, words: Iterable[str]) -> list[str]:
    lowered = text.lower()
    return sorted(word for word in words if word in lowered)


def _read_tags(payload: Mapping[str, Any]) -> Dict[str, list[str]]:
    text = _payload_text(payload)
    return {
        "risk": _find_markers(text, RISK_WORDS),
        "trace": _find_markers(text, TRACE_WORDS),
        "route": _find_markers(text, ROUTE_WORDS),
        "memory": _find_markers(text, MEMORY_WORDS),
        "structure": _find_markers(text, STRUCTURE_WORDS),
        "signal": _find_markers(text, SIGNAL_WORDS),
    }


def _compact_tags(tags: Mapping[str, list[str]]) -> list[str]:
    return [name for name, values in tags.items() if values]


def build_package(event: Any) -> Dict[str, Any]:
    payload = _as_payload(event)
    text = _payload_text(payload)
    tags = _read_tags(payload)

    return {
        "schema": "w3.redr.package.v2",
        "package_id": _identity_map(payload)["package_id"],
        "reader": "REDR",
        "identity": _identity_map(payload),
        "source_payload": payload,
        "normalized_text": text,
        "tags": tags,
        "tag_summary": _compact_tags(tags),
        "copies": {
            "psp2": {"enabled": True, "purpose": "route_or_handoff"},
            "lrc2": {"enabled": True, "purpose": "record_and_future_pointer"},
        },
        "mutation": {
            "source_payload": False,
            "package_only": True,
        },
    }


def classify_event(event: Any) -> object:
    payload = _as_payload(event)
    package = build_package(payload)
    text = package["normalized_text"]

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
            details={"payload": payload, "package": package},
        )

    tags = package["tags"]

    if tags["risk"]:
        package["redr_note"] = "risk markers found; REDR asks DTML to review before handoff"
        return make_result(
            module="REDR",
            status=REVIEW_REQUIRED,
            confidence=0.88,
            input_type="package:risk",
            decision="package_and_request_dtml_review",
            reason="risk markers detected; REDR will not decide safety itself",
            next_modules=["DTML", "LRC2"],
            standby=["PSP2"],
            details={"markers": tags["risk"], "payload": payload, "package": package},
        )

    if tags["trace"]:
        package["redr_note"] = "trace/governance markers found; send package to DTML and PSP2, copy to LRC2"
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.76,
            input_type="package:trace",
            decision="package_for_trace_review_and_route",
            reason="decision or trace markers detected",
            next_modules=["DTML", "PSP2", "LRC2"],
            standby=[],
            details={"markers": tags["trace"], "payload": payload, "package": package},
        )

    if tags["route"]:
        package["redr_note"] = "route markers found; send package to PSP2 and copy to LRC2"
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.74,
            input_type="package:route",
            decision="package_for_psp2_handoff",
            reason="route or handoff markers detected",
            next_modules=["PSP2", "LRC2"],
            standby=["DTML"],
            details={"markers": tags["route"], "payload": payload, "package": package},
        )

    if tags["memory"]:
        package["redr_note"] = "memory markers found; LRC2 receives priority copy"
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.72,
            input_type="event:memory",
            decision="package_for_lrc2_checkpoint",
            reason="memory or lifecycle markers detected",
            next_modules=["LRC2"],
            standby=["PSP2", "DTML"],
            details={"markers": tags["memory"], "payload": payload, "package": package},
        )

    if tags["structure"]:
        package["redr_note"] = "structure markers found; REDR keeps this as a structure-reading package"
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.68,
            input_type="package:structure",
            decision="package_structure_map_for_route_selection",
            reason="structure or file/path markers detected",
            next_modules=["PSP2", "LRC2"],
            standby=["DTML"],
            details={"markers": tags["structure"], "payload": payload, "package": package},
        )

    if tags["signal"]:
        package["redr_note"] = "signal markers found; package should preserve signal rhythm/state hints"
        return make_result(
            module="REDR",
            status=ACTIVE,
            confidence=0.66,
            input_type="package:signal",
            decision="package_signal_for_route_selection",
            reason="signal/state/rhythm markers detected",
            next_modules=["PSP2", "LRC2"],
            standby=["DTML"],
            details={"markers": tags["signal"], "payload": payload, "package": package},
        )

    package["redr_note"] = "general event accepted; REDR wraps package without forcing interpretation"
    return make_result(
        module="REDR",
        status=ACTIVE,
        confidence=0.55,
        input_type="package:general",
        decision="package_event_for_route_selection",
        reason="event accepted but no strong module marker detected",
        next_modules=["PSP2", "LRC2"],
        standby=["DTML"],
        details={"payload": payload, "package": package},
    )


__all__ = ["build_package", "classify_event"]
