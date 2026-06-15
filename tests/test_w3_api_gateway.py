from __future__ import annotations

import importlib

from fastapi.testclient import TestClient

from w3_api.main import app

client = TestClient(app)


def test_health_endpoint_reports_online_without_mutation():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["status"] == "online"
    assert data["service"] == "W3-API"


def test_root_main_reuses_canonical_app():
    root_main = importlib.import_module("main")

    assert root_main.app is app


def test_w3_cross_accepts_minimal_request_and_returns_gateway_contract():
    response = client.post(
        "/w3/cross",
        json={"source": "BBX19", "intent": "review W3 system"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert "w3lgu" in data
    assert data["signal"]["type"] == "W3_API_CROSS"
    assert data["signal"]["traceable"] is True
    assert data["signal"]["mutated"] is False


def test_w3_cross_keeps_focus_inside_payload_trace():
    response = client.post(
        "/w3/cross",
        json={
            "source": "BBX19",
            "intent": "review",
            "target": "W3",
            "mode": "cross",
            "payload": {"focus": "system"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["signal"]["target"] == "W3"
    assert data["signal"]["mode"] == "cross"
