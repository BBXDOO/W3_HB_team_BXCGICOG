from dataclasses import FrozenInstanceError

import pytest

from config import load_w3_config, validate_w3_config
from cross_x import CrossXRequest, build_cross_x_plan, build_event_chain


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
    event_chain = body["event_chain"]
    assert event_chain["chain_id"] == "cross-test"
    assert event_chain["supervisor"] == "AI_SUPERVISOR"
    assert event_chain["mutated"] is False
    assert [event["system"] for event in event_chain["events"]] == body["chain"]
    assert [event["sequence"] for event in event_chain["events"]] == list(range(1, 13))
    assert event_chain["events"][0]["predecessor"] is None
    assert event_chain["events"][-1]["successor"] is None
    assert all(event["execute_allowed"] is False for event in event_chain["events"])
    assert event_chain["events"][1]["contract"] == "five_line_packet_contract"
    assert body["w3lgu"].splitlines()[0].startswith("MEM:")
    assert "CHAIN_ID:cross-test" in body["w3lgu"].splitlines()[0]
    assert "ECS_STATE:planned" in body["w3lgu"].splitlines()[3]
    assert "EXECUTE_ALLOWED:false" in body["w3lgu"].splitlines()[4]
    assert body["px"]["relation"] == "cross_x.workflow_improvement"
    assert body["append_envelope"]["kind"] == "PX"
    assert body["ep_signal"]["mode"] == "preview_only"
    assert body["ep_signal"]["rytm"]["mode"] == "preview_only"
    assert body["ep_signal"]["rytm"]["mutated"] is False
    assert body["ep_signal"]["rytm"]["rytm_signal"].endswith("//BIN.")
    assert [stage["stage"] for stage in body["process_trace"]["stages"]] == ["REDR", "PSP2", "DTML", "LRC2"]
    assert body["process_trace"]["mutated"] is False
    assert body["system_audit"]["status"] == "ready"
    assert body["system_audit"]["checked"] == len(body["chain"])
    assert body["system_audit"]["issues"] == []


def test_cross_x_rejects_unsupported_modes():
    with pytest.raises(ValueError):
        build_cross_x_plan(source="BBX19", intent="execute directly", mode="execute")


@pytest.mark.parametrize(
    "cross_id",
    (
        "foo,CHAIN_ID:evil",
        "foo\nCHAIN_ID:evil",
        "",
    ),
)
def test_cross_x_rejects_w3lgu_unsafe_cross_ids(cross_id):
    with pytest.raises(ValueError, match="chain_id"):
        build_cross_x_plan(source="Codex", intent="trace", cross_id=cross_id)


def test_cross_x_request_is_immutable():
    request = CrossXRequest(source="Codex", intent="plan", target="PX")

    with pytest.raises(FrozenInstanceError):
        request.source = "mutated"  # type: ignore[misc]


def test_event_chain_rejects_duplicate_system_handoffs():
    with pytest.raises(ValueError, match="unique"):
        build_event_chain(
            chain_id="duplicate",
            systems=("W3Lgu", "W3Lgu"),
            contracts={"W3Lgu": "five_line_packet_contract"},
        )
