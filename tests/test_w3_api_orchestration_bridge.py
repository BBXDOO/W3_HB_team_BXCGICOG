"""Contract tests for a host-gated W3-API/E-CS/Orchestration bridge."""
import pytest
from w3_api.adapters.orchestration_bridge import run_inspection_bridge


def test_bridge_denies_unauthorized_execution():
    calls = []
    with pytest.raises(PermissionError):
        run_inspection_bridge(
            api_receipt={"id": "receipt-001", "status": "accepted"},
            inspection="w3_systems_v1",
            runner=lambda *_: calls.append(True),
        )
    assert calls == []


def test_bridge_correlates_host_result_and_ecs_returns():
    seen = []
    def trusted_runner(api_id, inspection):
        seen.append((api_id, inspection))
        return {"task_id": "W3-ORC-TEST-001", "status": "COMPLETED", "evidence": ["test-report"]}
    result = run_inspection_bridge(
        api_receipt={"id": "receipt-001", "status": "accepted"},
        inspection="w3_systems_v1",
        runner=trusted_runner, authorized=True,
    )
    assert seen == [("receipt-001", "w3_systems_v1")]
    assert result["task_id"] == "W3-ORC-TEST-001"
    assert result["ecs"]["state"] == "completed"
    assert all(event["execute_allowed"] is False for event in result["ecs"]["events"])
    assert result["ecs"]["events"][1]["return_value"]["task_id"] == result["task_id"]


def test_bridge_keeps_human_waiting_visible():
    result = run_inspection_bridge(
        api_receipt={"id": "receipt-002", "status": "accepted"},
        inspection="w3_systems_v1",
        runner=lambda *_: {"task_id": "W3-ORC-TEST-002", "status": "WAITING_HUMAN"},
        authorized=True,
    )
    assert result["ecs"]["state"] == "in_progress"
    assert result["ecs"]["events"][1]["status"] == "waiting"
    assert result["ecs"]["events"][2]["status"] == "planned"
