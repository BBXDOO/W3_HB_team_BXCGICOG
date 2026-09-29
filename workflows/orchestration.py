"""Evidence-led coordination for W3 tasks.

Adapters deliver notifications and execute support work; this module never
executes arbitrary task payloads or grants approval on behalf of a human.
"""
from __future__ import annotations

import json
from copy import deepcopy
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

STATUSES = {
    "RECEIVED", "INSPECTING", "QUEUED", "ROUTED", "ACKNOWLEDGED",
    "IN_PROGRESS", "BLOCKED", "ASSISTING", "RETURNED", "VERIFYING",
    "WAITING_HUMAN", "COMPLETED", "REJECTED", "CANCELLED", "FAILED",
}
TRANSITIONS = {
    "RECEIVED": {"INSPECTING", "REJECTED", "CANCELLED"},
    "INSPECTING": {"QUEUED", "REJECTED", "WAITING_HUMAN"},
    "QUEUED": {"ROUTED", "CANCELLED"},
    "ROUTED": {"ACKNOWLEDGED", "BLOCKED", "FAILED"},
    "ACKNOWLEDGED": {"IN_PROGRESS", "BLOCKED"},
    "IN_PROGRESS": {"BLOCKED", "VERIFYING", "FAILED"},
    "BLOCKED": {"ASSISTING", "WAITING_HUMAN", "FAILED"},
    "ASSISTING": {"RETURNED", "BLOCKED", "FAILED"},
    "RETURNED": {"IN_PROGRESS", "BLOCKED"},
    "VERIFYING": {"COMPLETED", "IN_PROGRESS", "WAITING_HUMAN"},
    "WAITING_HUMAN": {"QUEUED", "ASSISTING", "VERIFYING", "CANCELLED"},
}
KINDS = {"REQUEST", "REPORT", "ISSUE", "SIGNAL", "INTERNAL"}
PRIORITIES = {"CRITICAL", "HIGH", "NORMAL", "LOW"}
ID_RE = re.compile(r"^W3-ORC-[0-9]+-[0-9]+$")
Handler = Callable[[dict[str, Any]], dict[str, Any]]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate(task: dict[str, Any]) -> None:
    """Validate the fields that determine safe lifecycle decisions."""
    if not isinstance(task, dict) or not ID_RE.fullmatch(str(task.get("task_id", ""))):
        raise ValueError("invalid task_id")
    if task.get("type") not in KINDS or task.get("priority") not in PRIORITIES:
        raise ValueError("invalid type or priority")
    origin = task.get("origin")
    if not isinstance(origin, dict) or not isinstance(origin.get("module"), str) or not origin["module"].strip():
        raise ValueError("origin.module required")
    if type(origin.get("tier")) is not int or not 0 <= origin["tier"] <= 7:
        raise ValueError("origin.tier must be 0..7")
    if not isinstance(task.get("payload"), dict) or any(not isinstance(task.get(key), str) or not task[key] for key in ("created_at", "updated_at")):
        raise ValueError("payload and timestamps required")
    if task.get("status") not in STATUSES:
        raise ValueError("invalid status")
    if not isinstance(task.get("history"), list) or not isinstance(task.get("evidence"), list):
        raise ValueError("history and evidence must be lists")
    if not isinstance(task.get("route"), list) or not isinstance(task.get("support"), list):
        raise ValueError("route and support must be lists")
    if type(task.get("mutated")) is not bool or type(task.get("human_review_required")) is not bool:
        raise ValueError("mutated and human_review_required must be booleans")


def new_task(task_id: str, kind: str, priority: str, origin: dict[str, Any], payload: dict[str, Any],
             *, source_id: str | None = None, human_review_required: bool = False) -> dict[str, Any]:
    at = timestamp()
    task = dict(task_id=task_id, type=kind, priority=priority, origin=origin, payload=payload,
                source_id=source_id, created_at=at, updated_at=at, status="RECEIVED",
                destination=None, route=[], history=[], evidence=[], blocker=None,
                support=[], human_review_required=human_review_required, human_approval=None,
                mutated=False, completed_at=None)
    validate(task)
    task["history"].append(dict(at=at, event="RECEIVED", actor=origin["module"], detail="intake"))
    return task


def advance(task: dict[str, Any], status: str, *, actor: str, detail: str,
            evidence: str | None = None) -> dict[str, Any]:
    validate(task)
    if not isinstance(actor, str) or not actor.strip() or not isinstance(detail, str) or not detail.strip() or status not in TRANSITIONS.get(task["status"], set()):
        raise ValueError(f"invalid transition {task['status']} -> {status}")
    if status == "ROUTED" and not task.get("destination"):
        raise ValueError("destination required before routing")
    if status == "ACKNOWLEDGED" and not evidence:
        raise ValueError("acknowledgement evidence required")
    if status == "ASSISTING" and not task.get("blocker"):
        raise ValueError("blocker required before support")
    if status == "RETURNED" and not task.get("support"):
        raise ValueError("support result required")
    if status == "VERIFYING" and (not isinstance(evidence, str) or not evidence.strip()):
        raise ValueError("verification evidence required")
    if status == "COMPLETED":
        verifying_at = next((i for i in range(len(task["history"]) - 1, -1, -1)
                             if task["history"][i]["event"] == "VERIFYING"), None)
        if verifying_at is None or not any(isinstance(item.get("ref"), str) and item["ref"].strip()
                                           for item in task["evidence"] if item.get("at") == task["history"][verifying_at]["at"]):
            raise ValueError("verification evidence required")
        if task.get("human_review_required") and not task.get("human_approval"):
            raise ValueError("human approval required")
    at = timestamp()
    task["status"], task["updated_at"] = status, at
    if status in {"QUEUED", "ASSISTING", "IN_PROGRESS", "VERIFYING"}:
        task["human_approval"] = None
    if evidence:
        task["evidence"].append(dict(at=at, ref=evidence, actor=actor))
    task["history"].append(dict(at=at, event=status, actor=actor, detail=detail))
    if status == "COMPLETED":
        task["completed_at"] = at
    return task


def route(task: dict[str, Any], destination: dict[str, Any], *, actor: str,
          notify: Handler) -> dict[str, Any]:
    """Record handoff; adapter acknowledgement is separate from delivery."""
    validate(task)
    if task["status"] != "QUEUED" or not isinstance(destination, dict) or not isinstance(destination.get("module"), str) or not destination["module"].strip():
        raise ValueError("queued task and destination.module required")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("routing actor required")
    target = deepcopy(destination)
    result = notify({"task_id": task["task_id"], "source_id": task.get("source_id"),
                     "destination": deepcopy(target), "payload": deepcopy(task["payload"])})
    if not isinstance(result, dict) or result.get("delivered") is not True or not isinstance(result.get("evidence"), str) or not result["evidence"].strip():
        raise ValueError("notification delivery and evidence required")
    task["destination"] = target
    task["route"].append(dict(destination=deepcopy(target), at=timestamp(), notification=result["evidence"]))
    return advance(task, "ROUTED", actor=actor, detail="handoff delivered", evidence=result["evidence"])


def assist(task: dict[str, Any], *, kind: str, name: str, actor: str, handler: Handler) -> dict[str, Any]:
    """Invoke a registered support adapter only after a blocker is recorded."""
    if task["status"] != "BLOCKED" or kind not in {"SPECIALIST", "TOOL"} or not name:
        raise ValueError("blocked task and named support adapter required")
    advance(task, "ASSISTING", actor=actor, detail=f"{kind}:{name}")
    try:
        result = handler({"task_id": task["task_id"], "source_id": task.get("source_id"),
                          "blocker": task["blocker"], "destination": task["destination"]})
        if not isinstance(result, dict) or not result.get("evidence") or not isinstance(result.get("resolved"), bool):
            raise ValueError("support result needs resolved and evidence")
    except Exception as exc:
        advance(task, "BLOCKED", actor=actor, detail=f"support failed: {type(exc).__name__}")
        return task
    task["support"].append(dict(kind=kind, name=name, result=result, at=timestamp()))
    if result["resolved"]:
        task["blocker"] = None
        return advance(task, "RETURNED", actor=actor, detail="support returned to owner", evidence=result["evidence"])
    return advance(task, "BLOCKED", actor=actor, detail="blocker remains", evidence=result["evidence"])


def approve(task: dict[str, Any], *, human: str, evidence: str) -> None:
    validate(task)
    if task["status"] not in {"WAITING_HUMAN", "VERIFYING"} or not isinstance(human, str) or not human.strip() or not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("human approval requires identity and evidence at review gate")
    task["human_approval"] = dict(human=human, evidence=evidence, at=timestamp())
    task["evidence"].append(dict(at=timestamp(), actor=human, ref=evidence))


def save(task: dict[str, Any], directory: Path) -> Path:
    """Write one validated snapshot atomically; caller controls the storage root."""
    validate(task)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{task['task_id']}.json"
    if path.is_symlink():
        raise ValueError("symlink task path")
    fd, temporary = tempfile.mkstemp(prefix=".orc-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(task, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path
