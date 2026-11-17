"""Explicit local smoke run: real HTTP handler -> trusted host -> Orchestration -> E-CS.

Run only in a disposable checkout or an intentionally writable test workspace.
This invokes the repository's actual system inspection suites and creates
request, evidence and human callback files. It NEVER approves the callback.
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from w3_api.main import app
from w3_api.adapters.orchestration_bridge import run_inspection_bridge
from w3_api.adapters.trusted_inspection_host import make_inspection_runner


def main():
    response = TestClient(app).post("/w3/cross", json={
        "source": "BBX19",
        "intent": "inspect E-CS health",
        "target": "E-CS",
        "mode": "observe",
        "payload": {"inspection": "w3_systems_v1", "read_only": True},
    })
    response.raise_for_status()
    receipt = response.json()
    assert receipt["status"] == "accepted"
    assert receipt["signal"]["mutated"] is False
    result = run_inspection_bridge(
        api_receipt=receipt,
        inspection="w3_systems_v1",
        runner=make_inspection_runner(Path(__file__).resolve().parents[1]),
        authorized=True,  # local explicit operator invocation, never HTTP-supplied
    )
    assert result["api_id"] == receipt["id"]
    assert result["orchestration"]["task_id"] == result["task_id"]
    assert result["ecs"]["events"][1]["return_value"]["task_id"] == result["task_id"]
    assert all(not e["execute_allowed"] for e in result["ecs"]["events"])
    print(json.dumps({
        "api_id": result["api_id"],
        "task_id": result["task_id"],
        "status": result["orchestration"]["status"],
        "request_id": result["orchestration"]["request_id"],
        "callback_path": result["orchestration"]["callback_path"],
        "evidence": result["orchestration"]["evidence"],
        "ecs_state": result["ecs"]["state"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
