from dataclasses import FrozenInstanceError

import pytest

from config import W3ConfigBundle, load_w3_config, validate_w3_config
from cross_x import CrossXRequest, audit_cross_systems, build_cross_x_plan, build_event_chain


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


def test_event_chain_normalizes_safe_ids_and_supervisor():
    chain = build_event_chain(
        chain_id="  cross-safe  ",
        systems=("W3Lgu",),
        contracts={"W3Lgu": "five_line_packet_contract"},
        supervisor="  CODEX_SUPERVISOR  ",
    )

    assert chain.chain_id == "cross-safe"
    assert chain.supervisor == "CODEX_SUPERVISOR"


@pytest.mark.parametrize("supervisor", ("", " bad value ", "AI,MODE:execute"))
def test_event_chain_rejects_unsafe_supervisor(supervisor):
    with pytest.raises(ValueError, match="supervisor"):
        build_event_chain(
            chain_id="safe",
            systems=("W3Lgu",),
            contracts={"W3Lgu": "five_line_packet_contract"},
            supervisor=supervisor,
        )


def test_event_chain_returns_value_when_system_is_inactive():
    chain = build_event_chain(
        chain_id="inactive-test",
        systems=("W3Lgu", "PX"),
        contracts={
            "W3Lgu": "five_line_packet_contract",
            "PX": "position_pointer_not_execution",
        },
        system_states={"W3Lgu": "active", "PX": "inactive"},
    )

    body = chain.to_dict()
    assert body["state"] == "partial"
    assert body["events"][0]["status"] == "planned"
    assert body["events"][0]["return_value"] is None
    assert body["events"][1]["status"] == "inactive"
    assert body["events"][1]["return_value"] == {
        "state": "inactive",
        "reason": "system_not_in_use",
        "configured_state": "inactive",
        "handled": True,
    }


def test_cross_system_audit_reports_all_current_chain_members_ready():
    report = audit_cross_systems(load_w3_config())

    assert report["status"] == "ready"
    assert report["checked"] == 12
    assert report["issues"] == []
    assert all(system["path_exists"] for system in report["systems"])


@pytest.mark.parametrize(
    ("chain", "contracts", "expected"),
    (
        ([{"bad": "entry"}], {}, "chain[0]"),
        ([""], {}, "chain[0]"),
        (["W3Lgu"], [], "contracts must be an object"),
    ),
)
def test_config_validation_reports_malformed_chain_without_crashing(
    chain, contracts, expected
):
    config = load_w3_config()
    malformed_cross = dict(config.cross_system)
    malformed_cross["chain"] = chain
    malformed_cross["contracts"] = contracts
    malformed = W3ConfigBundle(
        environment=config.environment,
        ecosystem=config.ecosystem,
        cross_system=malformed_cross,
        paths=config.paths,
    )

    errors = validate_w3_config(malformed)

    assert any(expected in error for error in errors)
