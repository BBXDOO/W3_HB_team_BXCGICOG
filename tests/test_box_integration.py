from __future__ import annotations

from fastapi.testclient import TestClient

from w3_api.main import app
from wx.engine_index import load_template_registry

client = TestClient(app)


def test_box_registry_is_readable_and_validated():
    registry = load_template_registry()
    assert registry["version"] == "1.0"
    assert registry["templates"]


def test_cross_plan_can_include_box_suggestion_without_new_authority():
    response = client.post(
        "/w3/cross/plan",
        json={"px": "1,1", "include_box_suggestion": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["execution_allowed"] is False
    assert data["mutated"] is False
    assert data["safety"]["planner_only"] is True
    assert data["suggested_template"]["path"].startswith("wx/templates/")
    assert data["suggested_template"]["reference_only"] is True


def test_cross_plan_preserves_default_response_when_box_is_not_requested():
    response = client.post("/w3/cross/plan", json={"px": "1,1"})

    assert response.status_code == 200
    assert "suggested_template" not in response.json()


def test_cross_plan_unknown_px_returns_null_suggestion_and_review():
    response = client.post(
        "/w3/cross/plan",
        json={"px": "99,99", "include_box_suggestion": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["state"] == "review"
    assert data.get("suggested_template") is None
    assert data["execution_allowed"] is False
    assert data["mutated"] is False
