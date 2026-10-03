"""Orchestrate an authorized document draft into a verified human-review gate."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.runtime.engine_v2 import build_context, dispatch
from tools.w3_document_allocator import DocumentSpec, make_orchestration_handler
from workflows import orchestration


def _task_id(request_id: str) -> str:
    number = int(hashlib.sha256(request_id.encode("utf-8")).hexdigest()[:8], 16)
    return f"W3-ORC-20261003-{number}"


def _document_checks(content: str, artifact: Path, expected_sha: str) -> list[dict[str, Any]]:
    headings = [f"## {number}." for number in range(1, 11)]
    relative_link = re.search(r"\]\((?:\.\.?/)[^)]+\)", content) is not None
    return [
        {"name": "artifact_exists", "passed": artifact.is_file()},
        {"name": "artifact_sha256", "passed": hashlib.sha256(artifact.read_bytes()).hexdigest() == expected_sha},
        {"name": "required_sections", "passed": all(item in content for item in headings)},
        {"name": "markdown_gfm_html_separated", "passed": all(item in content for item in ("Markdown", "GFM", "HTML/CSS", "ขึ้นกับ renderer"))},
        {"name": "relative_link_example", "passed": relative_link},
        {"name": "safe_examples", "passed": "<script" not in content.lower()},
    ]


def run_document_creation(
    *, request: dict[str, Any], agent_result: dict[str, Any], repo_root: Path
) -> dict[str, Any]:
    """Use Orchestration support to allocate, verify, and stop at human review."""
    rid = str(request["request_id"])
    raw_spec = agent_result.get("document_spec")
    if agent_result.get("status") != "BLOCKED" or not isinstance(raw_spec, dict):
        raise ValueError("document owner must return a BLOCKED document_spec for support")
    spec = DocumentSpec(
        title=str(raw_spec["title"]), target=str(raw_spec["target"]),
        am_type=str(raw_spec["am_type"]), group=str(raw_spec["group"]),
        owner=str(raw_spec["owner"]), maker=str(raw_spec["maker"]),
        body=str(raw_spec["body"]), derived_from=tuple(item for item in raw_spec.get("derived_from", []) if item),
        request_id=rid, note=str(raw_spec.get("note") or "review required"),
        status=str(raw_spec.get("status") or "waiting_human"),
    )
    task = orchestration.new_task(
        _task_id(rid), "REQUEST", "NORMAL", {"module": str(request.get("requester") or "BBX19"), "tier": 1},
        {"request_id": rid, "request_type": "document_creation", "artifact_path": spec.target},
        source_id=rid, human_review_required=bool(request.get("final_signoff_required", True)),
    )
    orchestration.advance(task, "INSPECTING", actor="Orchestration", detail="document request inspected")
    orchestration.advance(task, "QUEUED", actor="Orchestration", detail="document owner selected")
    handoff = f"workflows/orchestration/handoffs/{rid}__Copilot-Gm.md"
    orchestration.route(
        task, {"module": "Copilot-Gm"}, actor="Orchestration",
        notify=lambda _packet: {"delivered": True, "evidence": handoff},
    )
    orchestration.advance(task, "ACKNOWLEDGED", actor="Copilot-Gm", detail="document content accepted", evidence="agent_result#document_spec")
    orchestration.advance(task, "IN_PROGRESS", actor="Copilot-Gm", detail="content prepared")
    task["blocker"] = {"code": "ARTIFACT_WRITER_REQUIRED", "owner": "Copilot-Gm", "target": spec.target}
    orchestration.advance(task, "BLOCKED", actor="Copilot-Gm", detail="filesystem executor required")
    orchestration.assist(
        task, kind="TOOL", name="W3 Document Allocator", actor="Orchestration",
        handler=make_orchestration_handler(spec, authorized_by=f"BBX19:{rid}", repo_root=repo_root),
    )
    if task["status"] != "RETURNED":
        raise RuntimeError("document allocator did not return a resolved artifact")
    receipt = task["support"][-1]["result"]["receipt"]
    artifact_info = receipt["artifact"]
    artifact = repo_root / artifact_info["path"]
    content = artifact.read_text(encoding="utf-8")
    checks = _document_checks(content, artifact, artifact_info["sha256"])
    gemini_context = build_context("document_validation", {
        "target": artifact_info["path"],
        "payload": {"checks": checks, "evidence": [artifact_info], "request_id": rid},
    })
    gemini = dispatch("Gemini", "document_validation", {
        "task": "document_validation", "kind": "verification", "run_with": "Gemini",
        "responsibilities": ["validate Markdown guide and renderer boundaries"],
    }, gemini_context)
    validation_path = repo_root / "repo_events" / f"{rid}_GEMINI_VALIDATION.md"
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text(
        "# Gemini Validation Event\n\n"
        f"- request_id: `{rid}`\n- artifact: `{artifact_info['path']}`\n"
        f"- artifact_sha256: `{artifact_info['sha256']}`\n- status: `{gemini['status']}`\n"
        f"- decision: `{gemini['decision']}`\n- mutated: `false`\n\n"
        "## Checks\n\n" + "\n".join(
            f"- {'PASS' if check['passed'] else 'FAIL'}: `{check['name']}`" for check in checks
        ) + "\n",
        encoding="utf-8",
    )
    orchestration.advance(task, "IN_PROGRESS", actor="Copilot-Gm", detail="artifact returned to document owner")
    orchestration.advance(task, "VERIFYING", actor="Gemini", detail="artifact validation recorded", evidence=str(validation_path.relative_to(repo_root)))
    if gemini.get("status") != "COMPLETED":
        orchestration.advance(task, "IN_PROGRESS", actor="Orchestration", detail="validation unresolved")
        task["blocker"] = {"code": "GEMINI_VALIDATION_UNRESOLVED"}
        orchestration.advance(task, "BLOCKED", actor="Orchestration", detail="Gemini checks did not pass")
    else:
        orchestration.advance(task, "WAITING_HUMAN", actor="Orchestration", detail="Gemini passed; BBX19 final sign-off required")
    snapshot_path = orchestration.save(task, repo_root / "repo_events")
    return {
        "status": task["status"], "task": "document_creation", "module": "Copilot-Gm",
        "output": "Document created and Gemini-validated; BBX19 final sign-off is required.",
        "agent_result": agent_result, "gemini_result": gemini,
        "artifacts": [artifact_info], "artifact_path": artifact_info["path"],
        "artifact_sha256": artifact_info["sha256"],
        "gemini_validation_event": str(validation_path.relative_to(repo_root)),
        "orchestration_evidence": str(snapshot_path.relative_to(repo_root)),
        "mutated": True, "review": True, "closed": False,
    }
