from __future__ import annotations

from hashlib import sha1
from typing import Any, Dict, Iterable, List, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text

KNOWN_MODULES = ["REDR", "PSP2", "DTML", "LRC2"]
ROUTE_MARKERS = {
    "DTML": {"dtml", "decision", "trace", "review", "law", "governance"},
    "LRC2": {"lrc2", "memory", "checkpoint", "record", "history", "lifecycle", "continuity"},
    "REDR": {"redr", "risk", "event", "classify", "triage"},
}


def _as_payload(package: Any) -> Dict[str, Any]:
    if isinstance(package, Mapping):
        return dict(package)
    return {"text": normalize_text(package)}


def _stable_stamp(payload: Dict[str, Any]) -> str:
    raw = normalize_text(payload)
    return sha1(raw.encode("utf-8")).hexdigest()[:12]


def _normalize_modules(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        values: Iterable[Any] = [value]
    else:
        try:
            values = list(value)
        except TypeError:
            values = [value]

    modules = []
    for item in values:
        name = str(item).upper().strip()
        if name in KNOWN_MODULES and name not in modules:
            modules.append(name)
    return modules


def validate_routing_path(route_plan: Any) -> bool:
    """Validate the explicit handoff path used by :class:`PSP2Agent`.

    PSP2 may stamp a package but must not hand it to itself, repeat a hop, or
    route toward an unknown module.  An empty path is rejected because it does
    not identify a next handoff target.
    """
    if isinstance(route_plan, (str, bytes)):
        return False

    try:
        steps = list(route_plan)
    except TypeError:
        return False

    if not steps:
        return False

    normalized = []
    for step in steps:
        if not isinstance(step, str):
            return False
        name = step.upper().strip()
        if not name or name not in KNOWN_MODULES or name == "PSP2" or name in normalized:
            return False
        normalized.append(name)

    return True


def _detect_route(payload: Dict[str, Any], text: str) -> List[str]:
    route_path: List[str] = []

    requested = _normalize_modules(payload.get("next") or payload.get("next_modules"))
    for module in requested:
        if module != "PSP2" and module not in route_path:
            route_path.append(module)

    for module, markers in ROUTE_MARKERS.items():
        if module == "PSP2":
            continue
        if any(marker in text for marker in markers) and module not in route_path:
            route_path.append(module)

    if not route_path:
        route_path.append("DTML")
    return route_path


def route_package(package: Any) -> object:
    """Create a route stamp and handoff preview for a W3Lgu package.

    PSP2's standard MFC role is:
    package in -> route stamp -> next module list -> standby list.
    It does not execute the target module.
    """

    payload = _as_payload(package)
    text = normalize_text(payload).lower()

    if not text:
        return make_result(
            module="PSP2",
            status=WAIT,
            confidence=0.0,
            input_type="empty",
            decision="wait_for_package",
            reason="no package data was provided",
            next_modules=[],
            standby=["REDR", "DTML", "LRC2"],
            details={"payload": payload, "route_quality": "none"},
        )

    route_path = _detect_route(payload, text)
    route_quality = "explicit" if payload.get("next") or payload.get("next_modules") else "inferred"
    status = REVIEW_REQUIRED if payload.get("status") == REVIEW_REQUIRED and "LRC2" in route_path else ACTIVE
    confidence = 0.9 if route_quality == "explicit" else 0.7
    stamp = _stable_stamp(payload)
    standby = [name for name in KNOWN_MODULES if name not in route_path and name != "PSP2"]

    return make_result(
        module="PSP2",
        status=status,
        confidence=confidence,
        input_type="package:route",
        decision="handoff_path_prepared",
        reason="package was stamped and assigned to a preview route",
        next_modules=route_path,
        standby=standby,
        details={
            "route_stamp": f"PSP2-{stamp}",
            "route_path": route_path,
            "route_quality": route_quality,
            "payload": payload,
        },
    )
