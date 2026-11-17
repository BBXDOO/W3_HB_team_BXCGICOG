"""Read-only diagnostic for the W3-API -> E-CS -> Orchestration boundary.

This test intentionally does NOT claim end-to-end execution. It records the
current API contract and a separately constructed E-CS handoff plan. A real
integration test must replace the separate plan with evidence from a live
adapter and a shared correlation ID.
"""
from fastapi.testclient import TestClient

from w3_api.main import app
from cross_x.event_chain import build_event_chain


def test_api_accepts_inspection_intent_but_does_not_claim_execution():
    response = TestClient(app).post(
        "/w3/cross",
        json={
            "source": "BBX19",
            "intent": "inspect E-CS health",
            "target": "E-CS",
            "mode": "observe",
            "payload": {"inspection": "w3_systems_v1", "read_only": True},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "accepted"
    assert body["signal"]["traceable"] is True
    assert body["signal"]["mutated"] is False
    assert body["signal"]["w3db"]["mutated"] is False
    assert body["signal"]["ep_signal"]["mutated"] is False
    assert body["signal"]["runtime"]["mutated"] is False
    assert [stage["stage"] for stage in body["signal"]["runtime"]["stages"]] == [
        "REDR", "PSP2", "DTML", "LRC2"
    ]
    # No orchestration task ID or E-CS event-chain receipt is returned.
    assert "orchestration_evidence" not in body
    assert "ecs_chain" not in body


def test_ecs_can_plan_handoffs_but_is_not_an_executor():
    chain = build_event_chain(
        chain_id="W3-API-ECS-DIAGNOSTIC",
        systems=["W3-API", "E-CS", "Orchestration", "Agent-Workbench"],
        contracts={
            "W3-API": "accept_intent",
            "E-CS": "observe_handoff_only",
            "Orchestration": "run_approved_work",
            "Agent-Workbench": "inspect_ecs",
        },
    )
    events = chain.to_dict()["events"]
    assert [event["sequence"] for event in events] == [1, 2, 3, 4]
    assert all(event["status"] == "planned" for event in events)
    assert all(event["execute_allowed"] is False for event in events)
    assert chain.to_dict()["state"] == "planned"
