"""Trusted local host runner: W3-API receipt -> real saved runtime circuit.

NOT an HTTP endpoint. The host must authenticate and authorize before calling
run_inspection_bridge(..., authorized=True, runner=...). Human approval stays
with the existing callback workflow. Writes inspection evidence only.
"""
from __future__ import annotations

import json
from pathlib import Path

from tools.runtime_circuit_intake import run_request


def make_inspection_runner(repo_root: str | Path):
    root = Path(repo_root).resolve()

    def run(api_id: str, inspection: str) -> dict:
        if inspection != "w3_systems_v1":
            raise ValueError("inspection not allowlisted")
        if not isinstance(api_id, str) or not api_id:
            raise ValueError("API receipt ID required")
        # A request's ID and body must remain stable for resumable execution.
        request_id = "RQ-API-ECS-" + api_id
        request_file = f"requests/{request_id}.md"
        source = root / request_file
        spec = {"workflow": "system_inspection", "input": {"payload": {"inspection": inspection}}}
        body = (
            "---\n"
            f"request_id: {request_id}\n"
            "task_keyword: design\n"
            "target_module: ChatGPT\n"
            "requester: BBX19\n"
            "request_type: runtime_circuit\n"
            "priority: NORMAL\n"
            "final_signoff_required: true\n"
            "---\n"
            "# Read-only API E-CS inspection\n"
            f"API correlation: {api_id}\n"
            "```w3-circuit\n" + json.dumps(spec, sort_keys=True) + "\n```\n"
        )
        # Never overwrite an existing request; reject content drift.
        if source.exists():
            if source.read_text(encoding="utf-8") != body:
                raise ValueError("existing request differs; reconciliation required")
        else:
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(body, encoding="utf-8")
        request = {
            "request_id": request_id,
            "requester": "BBX19",
            "priority": "NORMAL",
            "target_module": "ChatGPT",
            "final_signoff_required": True,
            "_request_text": body,
            "_request_file": request_file,
        }
        result = run_request(request=request, repo_root=root, target_module="ChatGPT")
        return {
            "task_id": Path(result["orchestration_evidence"]).stem,
            "status": result["status"],
            "evidence": [result["orchestration_evidence"], *[
                item["path"] for item in result.get("artifacts", []) if item.get("path")
            ]],
            "callback_path": result.get("callback_path"),
            "request_id": request_id,
        }

    return run
