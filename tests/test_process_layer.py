from dataclasses import FrozenInstanceError

import pytest

from core.runtime.process_layer import inspect_memory_status, inspect_w3db_status, run_w3_process_layer
from src.w3db.store import W3DBStore


def test_process_layer_runs_four_stages_without_mutation():
    store = W3DBStore()
    result = run_w3_process_layer(
        source="BBX19",
        intent="align Cross-X with W3DB memory",
        target="W3DB",
        mode="cross",
        payload={"contract": "do not rewrite source truth"},
        process_id="proc-test",
        timestamp="2026-05-31T00:00:00Z",
        store=store,
    )

    body = result.to_dict()
    assert result.process_id == "proc-test"
    assert body["mutated"] is False
    assert body["package"]["package_id"].startswith("PKG-")
    assert [stage["stage"] for stage in body["stages"]] == ["REDR", "PSP2", "DTML", "LRC2"]
    assert body["stages"][0]["data"]["duplicate_to"] == ["PSP2", "LRC2"]
    assert body["stages"][0]["data"]["route_scope"] == "cross_series"
    assert "W3DB" in body["stages"][0]["data"]["cross_routes"]
    assert body["stages"][0]["data"]["unknown_routes"] == []
    assert body["stages"][0]["data"]["execute_allowed"] is False
    assert body["stages"][1]["action"] == "stamp_route_only"
    assert body["stages"][1]["data"]["route_scope"] == "cross_series"
    assert "PX" in body["stages"][1]["data"]["cross_routes"]
    assert body["stages"][2]["data"]["execute_allowed"] is False
    assert body["stages"][2]["data"]["route_scope"] == "cross_series"
    assert body["memory_preview"]["mutated"] is False
    assert body["w3db_status"]["stats"] == {"xiz": 0, "tuf": 0, "fbd": 0, "whb": 0, "prx": 0}


def test_process_layer_marks_risky_intent_for_review():
    result = run_w3_process_layer(source="Codex", intent="delete public token", target="main")

    dtml = result.to_dict()["stages"][2]
    assert dtml["stage"] == "DTML"
    assert dtml["status"] == "review_required"
    assert dtml["data"]["risk"] == "red"


def test_process_package_is_immutable():
    result = run_w3_process_layer(source="REDR", intent="observe", process_id="immutable")

    with pytest.raises(FrozenInstanceError):
        result.package.intent = "mutated"  # type: ignore[misc]


def test_w3db_and_memory_status_are_inspectable_without_append():
    store = W3DBStore()

    w3db = inspect_w3db_status(store=store)
    memory = inspect_memory_status()

    assert w3db["backend"] == "memory"
    assert w3db["mutated"] is False
    assert w3db["stats"] == {"xiz": 0, "tuf": 0, "fbd": 0, "whb": 0, "prx": 0}
    assert memory["backend"] == "json"
    assert memory["mutated"] is False
    assert "memory_file" in memory
