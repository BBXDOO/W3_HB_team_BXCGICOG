from __future__ import annotations

from hashlib import sha1
from typing import Any, Dict, Mapping

from .contracts import ACTIVE, WAIT, make_result, normalize_text


def _as_payload(package: Any) -> Dict[str, Any]:
    if isinstance(package, Mapping):
        return dict(package)
    return {"text": normalize_text(package)}


def _stable_stamp(payload: Dict[str, Any]) -> str:
    raw = normalize_text(payload)
    return sha1(raw.encode("utf-8")).hexdigest()[:12]


def route_package(package: Any) -> object:
    """Create a minimal route stamp and handoff path for a W3Lgu package.

    PSP2's minimum functional concept is route selection and handoff preview.
    It does not execute the target module and does not mutate package state.
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
            details={"payload": payload},
        )

    requested_next = payload.get("next") or payload.get("next_modules") or []
    if isinstance(requested_next, str):
        requested_next = [requested_next]

    route_path = []
    if "DTML" in requested_next or "dtml" in text or "review" in text or "trace" in text:
        route_path.append("DTML")
    if "LRC2" in requested_next or "lrc2" in text or "memory" in text or "checkpoint" in text:
        route_path.append("LRC2")
    if not route_path:
        route_path.append("DTML")

    stamp = _stable_stamp(payload)
    standby = [name for name in ["REDR", "DTML", "LRC2"] if name not in route_path]

    return make_result(
        module="PSP2",
        status=ACTIVE,
        confidence=0.75 if route_path else 0.5,
        input_type="package:route",
        decision="handoff_path_prepared",
        reason="package was stamped and assigned to a preview route",
        next_modules=route_path,
        standby=standby,
        details={
            "route_stamp": f"PSP2-{stamp}",
            "route_path": route_path,
            "payload": payload,
        },
    )
