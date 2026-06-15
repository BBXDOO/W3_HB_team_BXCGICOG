from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from protocol.w3lgu import (
    MINIMUM_LAWS,
    LRC2Ledger,
    PointOfConvergence,
    PXPosition,
    W3LguError,
    W3LguPacket,
    W3LguPair,
    W3LguOperationalRuntime,
    operational_template,
    parse_line,
    validate_minimum_laws,
)


def test_production_template_exposes_exactly_27_numbered_laws_and_six_rooms():
    template = operational_template()

    assert validate_minimum_laws()
    assert len(MINIMUM_LAWS) == 27
    assert [law["number"] for law in template["laws"]] == list(range(1, 28))
    assert [room["code"] for room in template["rooms"]] == ["CA", "CU", "RE", "SI", "AP", "EV"]
    assert template["px_example"] == "LNCU'0001"
    assert template["poc"] == "Cross-X"


def test_px_notation_maps_horizontal_position_and_room_vertical_axis():
    px = PXPosition.parse("PX:LNCU'0001")

    assert px.room == "CU"
    assert px.x == 1
    assert px.y == 2
    assert px.relative_point == (1, 2)
    assert px.to_text() == "LNCU'0001"


@pytest.mark.parametrize(
    ("line", "expected_room"),
    (
        ("CAUSE:rain,ROOM:CA", "CA"),
        ("CAUSE:rain,RESULT:flood", "CU"),
        ("RESULT:stable", "RE"),
        ("SITUATION:offline", "SI"),
        ("APPEARANCE:latency", "AP"),
        ("EVENT:sync", "EV"),
    ),
)
def test_operational_runtime_classifies_all_six_rooms(line: str, expected_room: str):
    result = W3LguOperationalRuntime().process_line(line, cross_id="cross-room-test")

    assert result.package.room.code == expected_room
    assert result.package.px.room == expected_room
    assert result.package.poc.cross_id == "cross-room-test"


def test_operational_chain_performs_four_roles_and_records_every_stage():
    ledger = LRC2Ledger()
    runtime = W3LguOperationalRuntime(ledger=ledger)

    result = runtime.process_line(
        "EVENT:route,TARGET:W3DB,ROOM:EV,PX:LNEV'0007,STATE:ready,CONF:1",
        cross_id="cross-production",
        timestamp="2026-06-15T00:00:00.000Z",
    )

    assert [stage.stage for stage in result.stages] == ["REDR", "PSP2", "DTML", "LRC2"]
    assert result.stages[0].data["duplicate_to"] == ("PSP2", "LRC2")
    assert result.stages[1].data["payload_changed"] is False
    assert result.decision == "READY"
    assert result.signal == "GREEN"
    assert result.execute_allowed is False
    assert len(result.lrc2_records) == 4
    assert len(ledger) == 4
    assert ledger.verify()


def test_half_confidence_is_review_not_truth_or_failure():
    result = W3LguOperationalRuntime().process_line(
        "EVENT:observe,ROOM:AP,CONF:0.5",
        cross_id="cross-half",
    )

    assert result.decision == "REVIEW"
    assert result.signal == "YELLOW"
    assert result.stages[2].data["reasons"] == ("CONFIDENCE_HALF",)


def test_unresolved_marker_stops_but_is_still_recorded():
    ledger = LRC2Ledger()
    result = W3LguOperationalRuntime(ledger=ledger).process_line(
        "EVENT:route!,TARGET:UNKNOWN,ROOM:EV",
        cross_id="cross-stop",
    )

    assert result.decision == "STOP"
    assert result.signal == "RED"
    assert "UNRESOLVED_OR_HARMFUL_MARKER" in result.stages[2].data["reasons"]
    assert result.stages[-1].status == "RECORDED"
    assert len(ledger) == 4
    assert ledger.verify()


def test_lrc2_append_is_idempotent_and_hash_linked():
    ledger = LRC2Ledger()
    first = ledger.append(
        event_id="EVT-1:REDR",
        package_id="PKG-1",
        stage="REDR",
        status="PACKAGED",
        payload={"value": 1},
        timestamp="2026-06-15T00:00:00.000Z",
    )
    duplicate = ledger.append(
        event_id="EVT-1:REDR",
        package_id="PKG-CHANGED",
        stage="REDR",
        status="CHANGED",
        payload={"value": 2},
    )
    second = ledger.append(
        event_id="EVT-1:PSP2",
        package_id="PKG-1",
        stage="PSP2",
        status="ROUTED",
        payload={"value": 3},
    )

    assert duplicate is first
    assert len(ledger) == 2
    assert second.previous_hash == first.record_hash
    assert ledger.verify()
    with pytest.raises(FrozenInstanceError):
        first.status = "EDITED"  # type: ignore[misc]


def test_explicit_px_must_match_room_and_confidence_must_be_valid():
    runtime = W3LguOperationalRuntime()

    with pytest.raises(W3LguError, match="conflicts"):
        runtime.process_line("EVENT:test,ROOM:CA,PX:LNEV'0001")
    with pytest.raises(W3LguError, match="between 0 and 1"):
        runtime.process_line("EVENT:test,CONF:2")


@pytest.mark.parametrize(
    "cross_id",
    (
        "cross'X0009",
        "cross\nEVENT:forged",
        "cross,STATE:STOP",
        "cross:STATE:STOP",
        " cross with spaces ",
    ),
)
def test_poc_rejects_delimiter_unsafe_cross_ids(cross_id: str):
    runtime = W3LguOperationalRuntime()

    with pytest.raises(W3LguError, match="POC cross_id must use"):
        runtime.process_line("EVENT:test", cross_id=cross_id)
    with pytest.raises(W3LguError, match="POC cross_id must use"):
        PointOfConvergence(cross_id, 1, 1)


def test_operational_runtime_rejects_duplicate_governance_keys_before_recording():
    ledger = LRC2Ledger()
    runtime = W3LguOperationalRuntime(ledger=ledger)
    packet = W3LguPacket(
        (
            W3LguPair("EVENT", "route"),
            W3LguPair("STATE", "READY"),
            W3LguPair("STATE", "STOP"),
        ),
        source="EVENT:route,STATE:READY,STATE:STOP",
    )

    with pytest.raises(W3LguError, match="keys must be unique: STATE"):
        runtime.process_packet(packet, cross_id="cross-duplicate")
    assert len(ledger) == 0


def test_operational_runtime_rejects_duplicate_cross_id_from_text():
    runtime = W3LguOperationalRuntime()

    with pytest.raises(W3LguError, match="keys must be unique: CROSS_ID"):
        runtime.process_line(
            "EVENT:test,CROSS_ID:cross-safe,CROSS_ID:cross-other"
        )


def test_operational_runtime_validates_packet_cross_id_before_rendering_poc():
    runtime = W3LguOperationalRuntime()

    with pytest.raises(W3LguError, match="POC cross_id must use"):
        runtime.process_line("EVENT:test,CROSS_ID:cross'X9999")


def test_stable_derived_px_and_ids_make_replay_observable():
    runtime = W3LguOperationalRuntime()
    packet = parse_line("CAUSE:load,RESULT:slow,TARGET:QUEUE")

    first = runtime.process_packet(packet, cross_id="cross-replay")
    second = runtime.process_packet(packet, cross_id="cross-replay")

    assert first.event_id == second.event_id
    assert first.package.package_id == second.package.package_id
    assert first.package.px == second.package.px
    assert len(runtime.ledger) == 4
    assert runtime.ledger.verify()
