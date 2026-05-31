from dataclasses import FrozenInstanceError

import pytest

from protocol.w3lgu import append_px_to_w3db, parse_five_line_program, px_from_five_line, px_to_append_envelope
from src.w3db.append_flow import append_envelope_to_w3db, build_append_envelope
from src.w3db.store import W3DBStore
from w3_api.adapters.w3db_adapter import build_w3db_trace_plan


def _program():
    return parse_five_line_program(
        """
        MEM:SOURCE:BBX19
        PATCH:MODE:cross
        LAW:TARGET:W3Lgu
        EVENT:INTENT:align_W3Lgu_with_W3DB
        SIGNAL:STATUS:received
        """
    )


def test_px_anchor_from_five_line_is_immutable_and_reference_only():
    px = px_from_five_line(_program())

    assert px.px_id.startswith("PX-")
    assert px.source == "BBX19"
    assert px.target == "W3Lgu"
    assert px.subject == "align_W3Lgu_with_W3DB"
    assert "protocol/w3lgu/RML01.md" in px.references
    assert px.payload["event"]["INTENT"] == "align_W3Lgu_with_W3DB"

    with pytest.raises(FrozenInstanceError):
        px.target = "MUTATED"  # type: ignore[misc]


def test_append_envelope_is_deterministic_and_append_only():
    envelope_a = build_append_envelope(
        kind="PX",
        source="BBX19",
        target="W3DB",
        subject="same",
        payload={"b": 2, "a": 1},
        references=("protocol/w3lgu/RML01.md",),
        timestamp="2026-05-30T00:00:00Z",
    )
    envelope_b = build_append_envelope(
        kind="PX",
        source="BBX19",
        target="W3DB",
        subject="same",
        payload={"a": 1, "b": 2},
        references=("protocol/w3lgu/RML01.md",),
        timestamp="2026-05-30T99:99:99Z",
    )

    assert envelope_a.append_id == envelope_b.append_id
    assert envelope_a.to_dict()["payload"] == {"b": 2, "a": 1}


def test_append_px_to_w3db_creates_relation_records_and_idempotent_replay():
    store = W3DBStore()
    px = px_from_five_line(_program())

    first = append_px_to_w3db(px, store=store, confidence=0.75)
    second = append_px_to_w3db(px, store=store, confidence=0.75)

    assert first.appended is True
    assert first.status == "appended"
    assert second.appended is False
    assert second.status == "already_appended"
    assert first.xiz_id == second.xiz_id
    assert store.stats() == {"xiz": 1, "tuf": 1, "fbd": 1, "whb": 1, "prx": 1}
    assert store.read_xiz(first.xiz_id).immutable is True


def test_append_envelope_to_w3db_rejects_duplicate_when_not_idempotent():
    store = W3DBStore()
    envelope = px_to_append_envelope(px_from_five_line(_program()))

    append_envelope_to_w3db(envelope, store=store, idempotent=True)

    with pytest.raises(KeyError):
        append_envelope_to_w3db(envelope, store=store, idempotent=False)


def test_w3_api_trace_plan_includes_px_and_append_envelope_without_mutation():
    plan = build_w3db_trace_plan("12345678-aaaa", _program())

    assert plan["mode"] == "append_plan_only"
    assert plan["mutated"] is False
    assert plan["px"]["source"] == "BBX19"
    assert plan["px"]["target"] == "W3Lgu"
    assert plan["append_envelope"]["kind"] == "PX"
    assert plan["append_envelope"]["payload"]["px_id"].startswith("PX-")
