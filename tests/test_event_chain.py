from __future__ import annotations

import pytest

from cross_x.event_chain import bind_event_return, build_event_chain


def _chain():
    return build_event_chain(
        chain_id="test-chain",
        systems=("CROLL", "BOX"),
        contracts={"CROLL": "observe_handoff_only", "BOX": "reference_only"},
    )


def test_build_event_chain_records_order_and_contracts():
    chain = _chain()

    assert chain.state == "planned"
    assert [event.system for event in chain.events] == ["CROLL", "BOX"]
    assert chain.events[0].predecessor is None
    assert chain.events[0].successor == "BOX"
    assert chain.events[1].predecessor == "CROLL"
    assert chain.events[1].successor is None
    assert chain.events[0].contract == "observe_handoff_only"


def test_build_event_chain_rejects_unsafe_identifier():
    with pytest.raises(ValueError):
        build_event_chain(
            chain_id="bad:id",
            systems=("CROLL",),
            contracts={"CROLL": "observe_handoff_only"},
        )


def test_inactive_system_is_recorded_without_execution():
    chain = build_event_chain(
        chain_id="test-chain",
        systems=("CROLL", "MPCP"),
        contracts={"CROLL": "observe_handoff_only", "MPCP": "modew_execute"},
        system_states={"MPCP": "disabled"},
    )

    assert chain.state == "partial"
    inactive = chain.events[1]
    assert inactive.status == "inactive"
    assert inactive.return_value["handled"] is True
    assert inactive.return_value["reason"] == "system_not_in_use"


def test_bind_event_return_returns_new_chain_without_mutating_original():
    chain = _chain()
    event = chain.events[0]

    updated = bind_event_return(
        chain,
        event_id=event.event_id,
        return_value={"state": "SUCCESS", "reason": "smoke_test"},
        status="completed",
        execute_allowed=False,
    )

    assert chain.events[0].return_value is None
    assert chain.state == "planned"
    assert updated is not chain
    assert updated.events[0].return_value["state"] == "SUCCESS"
    assert updated.events[0].status == "completed"
    assert updated.state == "in_progress"


def test_bind_event_return_rejects_terminal_double_bind():
    chain = _chain()
    event = chain.events[0]
    updated = bind_event_return(
        chain,
        event_id=event.event_id,
        return_value={"state": "SUCCESS"},
        status="completed",
        execute_allowed=False,
    )

    with pytest.raises(ValueError):
        bind_event_return(
            updated,
            event_id=event.event_id,
            return_value={"state": "SUCCESS_AGAIN"},
            status="completed",
            execute_allowed=False,
        )


def test_waiting_event_can_resume_with_return_history():
    chain = _chain()
    event = chain.events[0]
    waiting = bind_event_return(
        chain,
        event_id=event.event_id,
        return_value={"state": "WAIT", "reason": "dependency"},
        status="waiting",
        execute_allowed=False,
    )

    resumed = bind_event_return(
        waiting,
        event_id=event.event_id,
        return_value={"state": "SUCCESS", "reason": "dependency_ready"},
        status="completed",
        execute_allowed=False,
    )

    assert resumed.events[0].return_value["state"] == "SUCCESS"
    assert resumed.events[0].return_history[0]["state"] == "WAIT"


def test_stopped_event_sets_chain_state_to_stopped():
    chain = _chain()
    event = chain.events[0]

    updated = bind_event_return(
        chain,
        event_id=event.event_id,
        return_value={"state": "STOP", "reason": "blocked"},
        status="stopped",
        execute_allowed=False,
    )

    assert updated.state == "stopped"
    assert updated.events[0].status == "stopped"
