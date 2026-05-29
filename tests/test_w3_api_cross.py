from __future__ import annotations

from fastapi.testclient import TestClient

from src.w3db.store import W3DBStore
from w3_api.main import app

client = TestClient(app)


def test_w3_cross_returns_traceable_five_line_packet():
    response = client.post(
        "/w3/cross",
        json={
            "source": "BBX19",
            "intent": "align W3Lgu with W3DB and EP_SIGNAL",
            "target": "W3Lgu",
            "mode": "cross",
            "payload": {"contract": "do not rewrite source truth"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "accepted"
    assert body["timestamp"].endswith("Z")
    lines = body["w3lgu"].splitlines()
    assert [line.split(":", 1)[0] for line in lines] == ["MEM", "PATCH", "LAW", "EVENT", "SIGNAL"]
    assert "SOURCE:BBX19" in lines[0]
    assert "MODE:cross" in lines[1]
    assert "TARGET:W3Lgu" in lines[2]
    assert "INTENT:align" in lines[3]
    assert "STATUS:received" in lines[4]
    assert body["signal"]["type"] == "W3_API_CROSS"
    assert body["signal"]["traceable"] is True
    assert body["signal"]["mutated"] is False


def test_w3_cross_defaults_to_observe_and_auto_target():
    response = client.post(
        "/w3/cross",
        json={"source": "ChatGPT", "intent": "observe system health"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["signal"]["mode"] == "observe"
    assert body["signal"]["target"] is None
    assert "TARGET:auto" in body["w3lgu"]
    assert body["signal"]["w3db"]["mode"] == "append_plan_only"
    assert body["signal"]["w3db"]["mutated"] is False
    assert body["signal"]["ep_signal"]["mode"] == "preview_only"
    assert body["signal"]["ep_signal"]["mutated"] is False


def test_w3_cross_does_not_mutate_w3db_store():
    store = W3DBStore()

    response = client.post(
        "/w3/cross",
        json={"source": "Gemini", "intent": "route interpretation", "target": "MPCP"},
    )

    assert response.status_code == 200
    assert store.list_xiz() == []
    assert store.list_tuf() == []
    assert store.list_fbd() == []
    assert store.list_prx() == []


def test_w3_cross_validates_required_fields():
    response = client.post("/w3/cross", json={"source": "BBX19"})

    assert response.status_code == 422
