"""Host-gated, read-only bridge for W3-API inspection requests.

This module does not expose an unauthenticated execution endpoint.
A trusted host supplies the orchestration runner and verifies the caller.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from cross_x.event_chain import bind_event_return, build_event_chain

INSPECTION = "w3_systems_v1"


def run_inspection_bridge(
    *,
    api_receipt: dict[str, Any],
    inspection: str,
    runner: Callable[[str, str], dict[str, Any]],
    authorized: bool = False,
) -> dict[str, Any]:
    """Correlate a host-authorized run with E-CS events; no source-truth writes."""
    if authorized is not True:
        raise PermissionError("trusted host authorization required")
    if inspection != INSPECTION:
        raise ValueError("unsupported inspection")
    if not isinstance(api_receipt, dict) or not isinstance(api_receipt.get("id"), str):
        raise ValueError("valid W3-API receipt required")
    correlation_id = api_receipt["id"]
    if not correlation_id or len(correlation_id) > 120:
        raise ValueError("invalid API correlation id")
    chain = build_event_chain(
        chain_id="API-" + correlation_id,
        systems=["W3-API", "Orchestration", "Agent-Workbench"],
        contracts={
            "W3-API": "accept_intent",
            "Orchestration": "host_authorized_inspection",
            "Agent-Workbench": "inspection_result",
        },
    )
    chain = bind_event_return(
        chain, event_id=chain.events[0].event_id,
        return_value={"api_id": correlation_id, "status": api_receipt.get("status")},
        status="completed", execute_allowed=False,
    )
    # The host owns execution and authority; E-CS only records its outcome.
    result = runner(correlation_id, inspection)
    if not isinstance(result, dict) or not isinstance(result.get("status"), str):
        raise ValueError("host runner must return a status object")
    task_id = result.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        raise ValueError("host runner must return a real task_id")
    chain = bind_event_return(
        chain, event_id=chain.events[1].event_id,
        return_value={"task_id": task_id, "status": result["status"]},
        status="completed" if result["status"] == "COMPLETED" else "waiting",
        execute_allowed=False,
    )
    if result["status"] == "COMPLETED":
        chain = bind_event_return(
            chain, event_id=chain.events[2].event_id,
            return_value={"task_id": task_id, "evidence": result.get("evidence", [])},
            status="completed", execute_allowed=False,
        )
    return {"api_id": correlation_id, "task_id": task_id, "ecs": chain.to_dict(), "orchestration": result}
