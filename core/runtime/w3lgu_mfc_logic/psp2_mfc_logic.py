from __future__ import annotations

from hashlib import sha1
from typing import Any, Dict, Iterable, List, Mapping

from .contracts import ACTIVE, REVIEW_REQUIRED, WAIT, make_result, normalize_text

LOCAL_W3LGU_MODULES = ["REDR", "PSP2", "DTML", "LRC2"]
CROSS_SERIES_SYSTEMS = [
    "W3-API",
    "W3LGU",
    "PX",
    "W3DB_APPEND",
    "EP_SIGNAL",
    "EP_SIGNAL_RYTM",
    "HOSPITICATION",
    "IGET",
    "WHUB",
    "WHOME",
]
KNOWN_MODULES = LOCAL_W3LGU_MODULES + CROSS_SERIES_SYSTEMS
ROUTE_MARKERS = {
    "DTML": {"dtml", "decision", "trace", "review", "law", "governance"},
    "LRC2": {"lrc2", "memory", "checkpoint", "record", "history", "lifecycle", "continuity"},
    "REDR": {"redr", "risk", "event", "classify", "triage"},
}
IDENTITY_FIELDS = (
    "chain_id",
    "process_id",
    "event_id",
    "package_id",
    "sequence",
    "source",
    "target",
    "predecessor",
    "successor",
    "owner_scope",
)
NODE_REGISTRY: Dict[str, str] = {
    "REDR": "ni:redr",
    "DTML": "ni:dtml",
    "LRC2": "ni:lrc2",
    "MNPS": "ni:mnps",
    "TL-S": "ni:tls",
}
CROSS_PREFIX = "xs:"
ROOM_ORDER = ["CA", "CU", "RE", "SI", "AP", "EV"]


def register_node(target: str, address: str) -> None:
    NODE_REGISTRY[target.upper().strip()] = address


def _as_payload(package: Any) -> Dict[str, Any]:
    if isinstance(package, Mapping):
        return dict(package)
    return {"text": normalize_text(package)}


def _stable_stamp(payload: Dict[str, Any]) -> str:
    raw = normalize_text(payload)
    return sha1(raw.encode("utf-8")).hexdigest()[:12]


def generate_px_stamp(package: Dict[str, Any], system_id: str = "") -> str:
    raw = package.get("package_id") or package.get("_px") or str(package)
    digest = sha1(raw.encode("utf-8")).hexdigest()
    seq = int(digest[:4], 16) % 9999 + 1
    room = _resolve_room(package)
    px = f"LN{room}'{seq:04d}"
    if system_id:
        px = f"{system_id}/{px}"
    return f"PX:{px}"


def _resolve_room(package: Dict[str, Any]) -> str:
    room = package.get("_room", "CU").upper().strip()
    if room in ROOM_ORDER:
        return room
    return "CU"


def resolve_node(target: str) -> str:
    t = target.upper().strip()
    node = NODE_REGISTRY.get(t)
    if node:
        return node
    return f"{CROSS_PREFIX}{t.lower()}"


def _normalize_name(value: Any) -> str:
    return str(value).upper().strip().replace(" ", "_")


def _iter_values(value: Any) -> Iterable[Any]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]


def _normalize_modules(value: Any) -> List[str]:
    modules = []
    for item in _iter_values(value):
        name = _normalize_name(item)
        if name in KNOWN_MODULES and name not in modules:
            modules.append(name)
    return modules


def _route_inventory(value: Any) -> Dict[str, List[str]]:
    local: List[str] = []
    cross: List[str] = []
    unknown: List[str] = []

    for item in _iter_values(value):
        name = _normalize_name(item)
        if not name:
            continue
        if name == "PSP2":
            continue
        if name in LOCAL_W3LGU_MODULES:
            if name not in local:
                local.append(name)
        elif name in CROSS_SERIES_SYSTEMS:
            if name not in cross:
                cross.append(name)
        elif name not in unknown:
            unknown.append(name)

    return {"local": local, "cross": cross, "unknown": unknown}


def _route_scope(local: List[str], cross: List[str], unknown: List[str]) -> str:
    if unknown and not local and not cross:
        return "unknown"
    scopes = []
    if local:
        scopes.append("local_w3lgu")
    if cross:
        scopes.append("cross_series")
    if unknown:
        scopes.append("unknown")
    if len(scopes) > 1:
        return "mixed"
    return scopes[0] if scopes else "local_w3lgu"


def _identity(payload: Mapping[str, Any], stamp: str, route_scope: str) -> Dict[str, Any]:
    package = payload.get("package") if isinstance(payload.get("package"), Mapping) else {}
    package_identity = package.get("identity") if isinstance(package.get("identity"), Mapping) else {}
    identity: Dict[str, Any] = {}
    unknown = []
    for field in IDENTITY_FIELDS:
        value = payload.get(field)
        if value in (None, ""):
            value = package_identity.get(field)
        if value in (None, ""):
            value = package.get(field)
        if value in (None, ""):
            unknown.append(field)
        else:
            identity[field] = value
    identity["route_scope"] = route_scope
    identity["route_stamp"] = f"PSP2-{stamp}"
    identity["mutated"] = False
    identity["traceable"] = True
    if unknown:
        identity["unknown"] = {"fields": unknown, "reason": "missing_from_input", "review": True}
    return identity


def validate_routing_path(route_plan: Any) -> bool:
    """Validate the explicit handoff path used by :class:`PSP2Agent`."""
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
        name = _normalize_name(step)
        if not name or name == "PSP2" or name in normalized:
            return False
        normalized.append(name)

    return True


def _detect_route(payload: Dict[str, Any], text: str) -> List[str]:
    route_path: List[str] = []

    inventory = _route_inventory(payload.get("next") or payload.get("next_modules") or payload.get("target"))
    for module in [*inventory["local"], *inventory["cross"], *inventory["unknown"]]:
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
    """Create a route stamp and handoff preview for a W3Lgu package."""

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

    explicit_value = payload.get("next") or payload.get("next_modules") or payload.get("target")
    inventory = _route_inventory(explicit_value)
    route_path = _detect_route(payload, text)
    route_quality = "explicit" if explicit_value else "inferred"
    stamp = _stable_stamp(payload)
    route_scope = _route_scope(inventory["local"], inventory["cross"], inventory["unknown"])
    bridge_contract = bool(payload.get("bridge_contract") or payload.get("adapter_contract"))
    review_required = (
        payload.get("status") == REVIEW_REQUIRED
        or bool(inventory["unknown"])
        or (bool(inventory["cross"]) and not bridge_contract)
    )
    status = REVIEW_REQUIRED if review_required else ACTIVE
    confidence = 0.9 if route_quality == "explicit" and not review_required else 0.7
    standby = [name for name in LOCAL_W3LGU_MODULES if name not in route_path and name != "PSP2"]

    return make_result(
        module="PSP2",
        status=status,
        confidence=confidence,
        input_type="package:route",
        decision="handoff_path_prepared",
        reason=(
            "package was stamped and assigned to a review-preserved route"
            if review_required
            else "package was stamped and assigned to a preview route"
        ),
        next_modules=route_path,
        standby=standby,
        review=review_required,
        details={
            "route_stamp": f"PSP2-{stamp}",
            "route_path": route_path,
            "route_scope": route_scope,
            "route_quality": route_quality,
            "local_routes": inventory["local"],
            "cross_routes": inventory["cross"],
            "unknown_routes": inventory["unknown"],
            "bridge_contract": bridge_contract,
            "handoff_summary": f"PSP2 stamped PSP2-{stamp}; scope={route_scope}; next={route_path}",
            "identity": _identity(payload, stamp, route_scope),
            "payload": payload,
        },
    )
