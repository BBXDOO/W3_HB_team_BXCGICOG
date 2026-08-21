"""W3 REDR/PSP2/DTML/LRC2 process layer.

This layer turns an intent into a traceable package flow without executing source
truth changes. It gives REDR, PSP2, DTML, and LRC2 a shared runtime contract:

REDR  -> read, classify, tag, and duplicate package intent
PSP2  -> stamp and route only
DTML  -> inspect destination/risk and emit decision signal
LRC2  -> create an immutable memory/log preview

The default output is plan-only. Optional persistence must be called explicitly by
an approved adapter or human-reviewed workflow.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from core.memory import memory_bus
from core.runtime.agents.dtml import DTMLAgent
from core.runtime.agents.lrc2 import LRC2Agent
from core.runtime.agents.psp2 import PSP2Agent
from core.runtime.agents.redr import REDRAgent
from protocol.w3lgu.core import W3LguFiveLineProgram
from src.w3db.store import W3DBStore, get_store

PROCESS_REFERENCES = (
    "protocol/w3lgu/README.md",
    "docs/cross_x_ecosystem.md",
    "core/runtime/process_layer.py",
)
PROCESS_STAGES = ("REDR", "PSP2", "DTML", "LRC2")
LOCAL_W3LGU_TARGETS = {"REDR", "PSP2", "DTML", "LRC2", "W3LGU"}
CROSS_SERIES_TARGETS = {"PX", "W3DB", "W3DB_APPEND", "EP_SIGNAL", "EP_SIGNAL_RYTM", "HOSPITICATION", "IGET", "WHUB", "WHOME", "W3-API"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _canonical(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _stable_id(prefix: str, value: Mapping[str, Any]) -> str:
    digest = hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest().upper()[:16]
    return f"{prefix}-{digest}"


@dataclass(frozen=True)
class ProcessPackage:
    """Immutable package carried through REDR → PSP2 → DTML → LRC2."""

    package_id: str
    source: str
    intent: str
    target: str = "auto"
    mode: str = "observe"
    payload: Mapping[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_now_iso)
    tags: tuple[str, ...] = ()
    duplicate_to: tuple[str, ...] = ("PSP2", "LRC2")
    route_scope: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "source": self.source,
            "intent": self.intent,
            "target": self.target,
            "mode": self.mode,
            "payload": dict(self.payload),
            "timestamp": self.timestamp,
            "tags": list(self.tags),
            "duplicate_to": list(self.duplicate_to),
            "route_scope": self.route_scope,
        }


@dataclass(frozen=True)
class StageRecord:
    """One non-mutating process-layer stage record."""

    stage: str
    action: str
    status: str
    summary: str
    data: Mapping[str, Any] = field(default_factory=dict)
    mutated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "action": self.action,
            "status": self.status,
            "summary": self.summary,
            "mutated": self.mutated,
            "data": dict(self.data),
        }


@dataclass(frozen=True)
class ProcessLayerResult:
    """Full W3 process-layer trace."""

    process_id: str
    package: ProcessPackage
    stages: tuple[StageRecord, ...]
    memory_preview: Mapping[str, Any]
    w3db_status: Mapping[str, Any]
    agent_results: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)
    mutated: bool = False
    references: tuple[str, ...] = PROCESS_REFERENCES

    def to_dict(self) -> dict[str, Any]:
        return {
            "process_id": self.process_id,
            "mutated": self.mutated,
            "package": self.package.to_dict(),
            "stages": [stage.to_dict() for stage in self.stages],
            "memory_preview": dict(self.memory_preview),
            "w3db_status": dict(self.w3db_status),
            "agent_results": {
                name: dict(result) for name, result in self.agent_results.items()
            },
            "references": list(self.references),
        }


def build_process_package(
    *,
    source: str,
    intent: str,
    target: str | None = None,
    mode: str = "observe",
    payload: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
) -> ProcessPackage:
    """Create the REDR package envelope without side effects."""

    body = {
        "source": source,
        "intent": intent,
        "target": target or "auto",
        "mode": mode,
        "payload": dict(payload or {}),
    }
    tags = _derive_tags(intent=intent, target=target or "auto", payload=dict(payload or {}))
    route_scope = _route_scope(target or "auto", payload=dict(payload or {}))
    return ProcessPackage(
        package_id=_stable_id("PKG", body),
        source=source,
        intent=intent,
        target=target or "auto",
        mode=mode,
        payload=dict(payload or {}),
        timestamp=timestamp or _now_iso(),
        tags=tags,
        route_scope=route_scope,
    )


def run_w3_process_layer(
    *,
    source: str,
    intent: str,
    target: str | None = None,
    mode: str = "observe",
    payload: Mapping[str, Any] | None = None,
    process_id: str | None = None,
    timestamp: str | None = None,
    store: W3DBStore | None = None,
) -> ProcessLayerResult:
    """Run the four agent executors as one non-persisting MFC trace.

    ``process_layer`` owns orchestration only.  Classification, routing,
    decision inspection, and lifecycle checkpoint semantics remain in the
    corresponding MFC functions reached through each agent's ``execute()``.
    """

    package = build_process_package(
        source=source,
        intent=intent,
        target=target,
        mode=mode,
        payload=payload,
        timestamp=timestamp,
    )
    pid = process_id or _stable_id("PROC", package.to_dict())
    chain_id = pid
    event_id = _stable_id("EV", package.to_dict())
    identity = {
        "chain_id": chain_id,
        "process_id": pid,
        "event_id": event_id,
        "package_id": package.package_id,
        "sequence": 1,
        "source": package.source,
        "target": package.target,
        "route_scope": package.route_scope,
        "predecessor": "W3-API",
        "successor": "REDR",
        "owner_scope": "W3_PROCESS_LAYER",
    }
    request = {
        "source": package.source,
        "intent": package.intent,
        "target": package.target,
        "mode": package.mode,
        "payload": {**dict(package.payload), **identity},
    }

    redr_result = REDRAgent().execute(
        package.intent,
        {"role": "reader", "target": package.target},
        {"request": request, **identity},
    )
    redr_package = redr_result.get("details", {}).get("package", {})

    route = ["W3Lgu", "PX", package.target, "LRC2"]
    psp2_result = PSP2Agent().execute(
        package.intent,
        {"role": "router", "next": route},
        {"request": request, "package": redr_package, **identity},
    )

    dtml_result = DTMLAgent().execute(
        package.intent,
        {"role": "decision_trace"},
        {"request": request, "payload": psp2_result, **identity},
    )

    psp2_details = psp2_result.get("details", {})
    checkpoint_record = {
        "text": package.intent,
        **identity,
        "route_scope": psp2_details.get("route_scope", package.route_scope),
        "route_stamp": psp2_details.get("route_stamp"),
        "prior_stage_summary": dtml_result.get("summary"),
        "decision": dtml_result.get("decision"),
        "status": dtml_result.get("status"),
        "details": {
            "identity": psp2_details.get("identity", identity),
            "route_scope": psp2_details.get("route_scope", package.route_scope),
            "route_stamp": psp2_details.get("route_stamp"),
            "prior_stage_summary": dtml_result.get("summary"),
        },
    }
    lrc2_result = LRC2Agent().execute(
        package.intent,
        {"role": "lifecycle_review"},
        {"request": request, "payload": checkpoint_record, **identity},
    )

    agent_results = {
        "REDR": redr_result,
        "PSP2": psp2_result,
        "DTML": dtml_result,
        "LRC2": lrc2_result,
    }
    stages = tuple(
        _stage_from_agent_result(name, result, package)
        for name, result in agent_results.items()
    )
    return ProcessLayerResult(
        process_id=pid,
        package=package,
        stages=stages,
        memory_preview=_memory_preview(package, pid, stages[-1]),
        w3db_status=inspect_w3db_status(store=store),
        agent_results=agent_results,
    )


def run_w3lgu_packet_process_layer(
    program: W3LguFiveLineProgram,
    *,
    payload: Mapping[str, Any] | None = None,
    process_id: str | None = None,
    timestamp: str | None = None,
    store: W3DBStore | None = None,
) -> ProcessLayerResult:
    """Bridge one validated W3-API five-line packet into the MFC chain."""

    packet_payload = dict(payload or {})
    contract = program.law.get("CONTRACT")
    if contract:
        packet_payload.setdefault("contract", contract)

    return run_w3_process_layer(
        source=program.memory.get("SOURCE", "W3-API") or "W3-API",
        intent=program.event.get("INTENT", "observe") or "observe",
        target=program.law.get("TARGET", "auto"),
        mode=program.patch.get("MODE", "observe") or "observe",
        payload=packet_payload,
        process_id=process_id,
        timestamp=timestamp,
        store=store,
    )


def inspect_w3db_status(*, store: W3DBStore | None = None) -> dict[str, Any]:
    """Return W3DB in-memory status without writing records."""

    active_store = store or get_store()
    return {
        "backend": "memory",
        "available": True,
        "mutated": False,
        "stats": active_store.stats(),
        "note": "W3DBStore is active in-process memory; persistence requires an explicit approved append adapter.",
    }


def inspect_memory_status() -> dict[str, Any]:
    """Return core memory bus status without appending records."""

    info = memory_bus.runtime_info()
    return {
        "backend": "json",
        "available": bool(info.get("exists")),
        "mutated": False,
        "records": info.get("records", 0),
        "memory_file": info.get("memory_file"),
        "runtime": info.get("runtime", {}),
    }


def _stage_from_agent_result(
    stage: str,
    result: Mapping[str, Any],
    package: ProcessPackage,
) -> StageRecord:
    """Expose an MFC result through the stable process-layer stage shape."""

    details = result.get("details") if isinstance(result.get("details"), Mapping) else {}
    data = dict(details)
    data["result"] = dict(result)
    data["execute_allowed"] = False

    if stage == "REDR":
        redr_package = details.get("package") if isinstance(details.get("package"), Mapping) else {}
        tags = redr_package.get("tag_summary", list(package.tags))
        data.update(
            {
                "tags": list(tags),
                "duplicate_to": list(package.duplicate_to),
                "route_scope": package.route_scope,
                "cross_routes": _route_inventory(package)["cross_routes"],
                "unknown_routes": _route_inventory(package)["unknown_routes"],
            }
        )
    elif stage == "PSP2":
        # Keep the established process-layer projection stable while the full
        # MFC scope (including local + cross = mixed) remains in data.result.
        route = ["W3Lgu", "PX", package.target, "LRC2"]
        inventory = _route_inventory(package, route=route)
        data.update(
            {
                "stamp": details.get("route_stamp"),
                "route": route,
                "route_scope": _inventory_scope(inventory),
                "cross_routes": inventory["cross_routes"],
                "unknown_routes": inventory["unknown_routes"],
                "bridge_contract": bool(details.get("bridge_contract")),
            }
        )
    elif stage == "DTML":
        data.setdefault("risk", _risk_level(package.intent, package.payload))
        data.setdefault("target", package.target)
        data.setdefault("route_scope", package.route_scope)

    status_map = {
        "REDR": {"ACTIVE": "packaged"},
        "PSP2": {"ACTIVE": "routed"},
        "DTML": {"ACTIVE": "approved_for_plan"},
        "LRC2": {"ACTIVE": "ready_to_append"},
    }
    raw_status = str(result.get("status", "WAIT"))
    stable_status = status_map.get(stage, {}).get(raw_status, raw_status.lower())
    action_map = {
        "REDR": "read_classify_package",
        "PSP2": "stamp_route_only",
        "DTML": "inspect_destination_and_signal",
        "LRC2": "memory_log_preview",
    }
    return StageRecord(
        stage=stage,
        action=action_map[stage],
        status=stable_status,
        summary=str(result.get("summary") or result.get("reason") or ""),
        data=data,
        mutated=bool(result.get("mutated", False)),
    )


def _memory_preview(package: ProcessPackage, process_id: str, stage: StageRecord) -> dict[str, Any]:
    return {
        "record_type": "process_layer_trace",
        "source": "LRC2",
        "topic": process_id,
        "content": f"{package.source} -> {package.target}: {package.intent}",
        "tags": ["REDR", "PSP2", "DTML", "LRC2", *package.tags],
        "status": stage.status,
        "mutated": False,
    }


def _derive_tags(*, intent: str, target: str, payload: Mapping[str, Any]) -> tuple[str, ...]:
    tags = {"cross_x", "process_layer", target.lower().replace("-", "_")}
    lower = f"{intent} {_canonical(dict(payload))}".lower()
    for token in ("risk", "governance", "w3db", "ep_signal", "w3lgu", "px", "memory"):
        if token in lower:
            tags.add(token)
    return tuple(sorted(tags))


def _risk_level(intent: str, payload: Mapping[str, Any]) -> str:
    text = f"{intent} {_canonical(dict(payload))}".lower()
    if any(word in text for word in ("delete", "overwrite", "secret", "credential", "token")):
        return "red"
    if any(word in text for word in ("mutate", "execute", "deploy", "merge", "public")):
        return "yellow"
    return "green"


def _normalize_target(value: str) -> str:
    return str(value or "").upper().strip().replace(" ", "_")


def _route_inventory(package: ProcessPackage, *, route: list[str] | None = None) -> dict[str, list[str]]:
    candidates = [_normalize_target(package.target)]
    explicit = package.payload.get("next") or package.payload.get("next_modules") or []
    if isinstance(explicit, str):
        candidates.append(_normalize_target(explicit))
    else:
        try:
            candidates.extend(_normalize_target(item) for item in explicit)
        except TypeError:
            candidates.append(_normalize_target(explicit))
    if route:
        candidates.extend(_normalize_target(item) for item in route)

    cross = []
    unknown = []
    for candidate in candidates:
        if not candidate or candidate in {"AUTO", "W3", "MAIN"}:
            continue
        if candidate in CROSS_SERIES_TARGETS:
            if candidate not in cross:
                cross.append(candidate)
        elif candidate not in LOCAL_W3LGU_TARGETS and candidate not in unknown:
            unknown.append(candidate)
    return {"cross_routes": cross, "unknown_routes": unknown}


def _inventory_scope(inventory: Mapping[str, list[str]]) -> str:
    cross = bool(inventory.get("cross_routes"))
    unknown = bool(inventory.get("unknown_routes"))
    if cross and unknown:
        return "mixed"
    if cross:
        return "cross_series"
    if unknown:
        return "unknown"
    return "local_w3lgu"


def _route_scope(target: str, payload: Mapping[str, Any]) -> str:
    candidates = {_normalize_target(target)}
    explicit = payload.get("next") or payload.get("next_modules") or []
    if isinstance(explicit, str):
        candidates.add(_normalize_target(explicit))
    else:
        try:
            candidates.update(_normalize_target(item) for item in explicit)
        except TypeError:
            candidates.add(_normalize_target(explicit))

    candidates.discard("")
    local = bool(candidates & LOCAL_W3LGU_TARGETS)
    cross = bool(candidates & CROSS_SERIES_TARGETS)
    unknown = bool(candidates - LOCAL_W3LGU_TARGETS - CROSS_SERIES_TARGETS - {"AUTO", "W3", "MAIN"})
    if sum(bool(item) for item in (local, cross, unknown)) > 1:
        return "mixed"
    if cross:
        return "cross_series"
    if local:
        return "local_w3lgu"
    if unknown:
        return "unknown"
    return "local_w3lgu"
