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
from src.w3db.store import W3DBStore, get_store

PROCESS_REFERENCES = (
    "protocol/w3lgu/README.md",
    "docs/cross_x_ecosystem.md",
    "core/runtime/process_layer.py",
)
PROCESS_STAGES = ("REDR", "PSP2", "DTML", "LRC2")


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
    return ProcessPackage(
        package_id=_stable_id("PKG", body),
        source=source,
        intent=intent,
        target=target or "auto",
        mode=mode,
        payload=dict(payload or {}),
        timestamp=timestamp or _now_iso(),
        tags=tags,
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
    """Run REDR/PSP2/DTML/LRC2 as a plan-only trace."""

    package = build_process_package(
        source=source,
        intent=intent,
        target=target,
        mode=mode,
        payload=payload,
        timestamp=timestamp,
    )
    pid = process_id or _stable_id("PROC", package.to_dict())
    redr = _redr_stage(package)
    psp2 = _psp2_stage(package)
    dtml = _dtml_stage(package)
    lrc2 = _lrc2_stage(package, process_id=pid, decision=dtml)
    return ProcessLayerResult(
        process_id=pid,
        package=package,
        stages=(redr, psp2, dtml, lrc2),
        memory_preview=_memory_preview(package, pid, lrc2),
        w3db_status=inspect_w3db_status(store=store),
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


def _redr_stage(package: ProcessPackage) -> StageRecord:
    return StageRecord(
        stage="REDR",
        action="read_classify_package",
        status="packaged",
        summary="REDR classified intent, applied tags, and duplicated package pointers to PSP2 and LRC2.",
        data={"tags": list(package.tags), "duplicate_to": list(package.duplicate_to)},
    )


def _psp2_stage(package: ProcessPackage) -> StageRecord:
    route = ["W3Lgu", "PX", package.target, "LRC2"]
    return StageRecord(
        stage="PSP2",
        action="stamp_route_only",
        status="routed",
        summary="PSP2 stamped the package and produced a route-only handoff trace.",
        data={"stamp": f"PSP2:{package.package_id}", "route": route},
    )


def _dtml_stage(package: ProcessPackage) -> StageRecord:
    risk = _risk_level(package.intent, package.payload)
    status = "review_required" if risk in {"yellow", "red"} else "approved_for_plan"
    return StageRecord(
        stage="DTML",
        action="inspect_destination_and_signal",
        status=status,
        summary="DTML inspected destination, signal, and intent; no execution authority was granted.",
        data={"risk": risk, "target": package.target, "execute_allowed": False},
    )


def _lrc2_stage(package: ProcessPackage, *, process_id: str, decision: StageRecord) -> StageRecord:
    return StageRecord(
        stage="LRC2",
        action="memory_log_preview",
        status="ready_to_append",
        summary="LRC2 prepared an immutable memory/log preview; no memory or W3DB write was performed.",
        data={"process_id": process_id, "package_id": package.package_id, "decision": decision.status},
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
