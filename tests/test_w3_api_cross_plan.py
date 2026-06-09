from __future__ import annotations

from fastapi.testclient import TestClient

from w3_api.main import app

client = TestClient(app)


def assert_plan_safety(data: dict) -> None:
    assert data["execution_allowed"] is False
    assert data["mutated"] is False
    assert data["review"] is True
    assert data["scope"] == "CROSS_L_ONLY"
    assert data["safety"]["planner_only"] is True
    assert data["safety"]["modew_execution_allowed"] is False
    assert data["safety"]["truth_mutation_allowed"] is False
    assert data["safety"]["repo_write_allowed"] is False
    assert data["safety"]["direct_merge_allowed"] is False


def test_w3_cross_plan_valid_px_returns_dispatch_plan():
    response = client.post("/w3/cross/plan", json={"px": "1,1"})

    assert response.status_code == 200
    data = response.json()
    assert_plan_safety(data)
    assert data["state"] == "planned"
    assert data["modew"] == "Fixer"
    assert data["action"] == "call_modew_stub_only"
    assert data["workset"]["rytm"] == "ROCK"
    assert data["workset"]["work_type"] == "FAST_PATCH"
    assert data["workset"]["boundary"] == "temp_patch"


def test_w3_cross_plan_px_format_with_prefix():
    response = client.post("/w3/cross/plan", json={"px": "PX:[2,1]"})

    assert response.status_code == 200
    data = response.json()
    assert_plan_safety(data)
    assert data["state"] == "planned"
    assert data["modew"] == "Adapter"
    assert data["workset"]["rytm"] == "JAZZ"
    assert data["workset"]["work_type"] == "ADAPTIVE_RULE"


def test_w3_cross_plan_invalid_px_returns_review_plan():
    response = client.post("/w3/cross/plan", json={"px": "99,99"})

    assert response.status_code == 200
    data = response.json()
    assert_plan_safety(data)
    assert data["state"] == "review"
    assert data["modew"] == "UNKNOWN"
    assert data["action"] == "review_before_dispatch"
    assert data["workset"]["rytm"] == "UNKNOWN"
    assert "not found" in data["reason"]


def test_w3_cross_plan_missing_px_is_validation_error():
    response = client.post("/w3/cross/plan", json={})

    assert response.status_code == 422


def test_w3_cross_plan_with_paper_context_marker():
    response = client.post(
        "/w3/cross/plan",
        json={"px": "1,1", "paper_context": {"paper_id": "demo", "scope": "CROSS_L_ONLY"}},
    )

    assert response.status_code == 200
    data = response.json()
    assert_plan_safety(data)
    assert data["workset"]["paper_context_received"] is True
    assert data["workset"]["paper_context_keys"] == ["paper_id", "scope"]
