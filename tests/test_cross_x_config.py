from dataclasses import FrozenInstanceError

import pytest

from config import load_w3_config, validate_w3_config
from cross_x import CrossXRequest, build_cross_x_plan


def test_w3_config_bundle_covers_current_ecosystem():
    config = load_w3_config()

    assert validate_w3_config(config) == []
    assert config.environment["schema_version"] == "W3-RUNTIME-0.3"
    assert config.environment["compatibility"]["iget"] == "v8.0"
    assert config.environment["compatibility"]["PX"] is True
    assert "PX" in config.ecosystem["components"]
    assert "W3DB_APPEND" in config.ecosystem["components"]
    assert "EP_SIGNAL_RYTM" in config.ecosystem["components"]
    assert config.cross_system["cross_x"]["truth_mutation"] is False
    assert config.component_path("px") == "protocol/w3lgu/px.py"


def test_cross_x_plan_builds_full_non_mutating_chain():
    plan = build_cross_x_plan(
        source="BBX19",
        intent="align PX with W3DB append flow",
        target="W3DB",
        mode="cross",
        payload={"contract": "do not rewrite source truth", "confidence": 0.75},
        cross_id="cross-test",
        timestamp="2026-05-31T00:00:00Z",
    )

    body = plan.to_dict()
    assert plan.cross_id == "cross-test"
    assert body["timestamp"] == "2026-05-31T00:00:00Z"
    assert body["mutated"] is False
    assert body["governance"]["human_review_required"] is True
    assert body["governance"]["truth_mutation_allowed"] is False
    assert body["chain"] == ["W3-API", "W3Lgu", "REDR", "PSP2", "DTML", "PX", "W3DB_APPEND", "EP_SIGNAL", "EP_SIGNAL_RYTM", "LRC2", "Hospitication", "IGET"]
    assert body["w3lgu"].splitlines()[0].startswith("MEM:")
    assert body["px"]["relation"] == "cross_x.workflow_improvement"
    assert body["append_envelope"]["kind"] == "PX"
    assert body["ep_signal"]["mode"] == "preview_only"
    assert body["ep_signal"]["rytm"]["mode"] == "preview_only"
    assert body["ep_signal"]["rytm"]["mutated"] is False
    assert body["ep_signal"]["rytm"]["rytm_signal"].endswith("//BIN.")
    assert [stage["stage"] for stage in body["process_trace"]["stages"]] == ["REDR", "PSP2", "DTML", "LRC2"]
    assert body["process_trace"]["mutated"] is False


def test_cross_x_rejects_unsupported_modes():
    with pytest.raises(ValueError):
        build_cross_x_plan(source="BBX19", intent="execute directly", mode="execute")


def test_cross_x_request_is_immutable():
    request = CrossXRequest(source="Codex", intent="plan", target="PX")

    with pytest.raises(FrozenInstanceError):
        request.source = "mutated"  # type: ignore[misc]
