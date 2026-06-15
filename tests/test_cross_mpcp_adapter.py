from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from cross_x import (
    EXECUTION_CAPABILITY,
    MPCPExecutionApproval,
    bind_event_return,
    build_cross_mpcp_handoff,
    build_event_chain,
    execute_cross_handoff,
)


def _chain():
    return build_event_chain(
        chain_id="cross-mpcp-test",
        systems=("CrossCode",),
        contracts={"CrossCode": "approved_modew_execution"},
    )


def _cross_envelope(event_id: str):
    return {
        "contract_version": "1.0",
        "kind": "cross-code-dispatch",
        "chain_id": "cross-mpcp-test",
        "event_id": event_id,
        "state": "planned",
        "execution_allowed": False,
        "mutated": False,
    }


def _approval(event_id: str, *, task: str = "verify"):
    return MPCPExecutionApproval(
        chain_id="cross-mpcp-test",
        event_id=event_id,
        task=task,
        approved_by="BBX19",
    )


def test_cross_mpcp_executes_one_modew_and_binds_return_immutably():
    chain = _chain()
    event = chain.events[0]
    handoff = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        context={"BOUNDARY": "read_only", "PX": "LNEV'0001"},
        review_approved=True,
    )
    calls = []

    def executor(text):
        calls.append(text)
        return {
            "state": "SUCCESS",
            "cause": "verify",
            "result": "verified",
            "mutated": False,
        }

    result = execute_cross_handoff(
        chain,
        handoff,
        _approval(event.event_id),
        executor=executor,
    )

    assert calls == ["TASK:verify,BOUNDARY:read_only,PX:LNEV'0001"]
    assert chain.state == "planned"
    assert chain.events[0].return_value is None
    assert result.executed is True
    assert result.state == "SUCCESS"
    assert result.chain is not chain
    assert result.chain.state == "completed"
    returned = result.chain.events[0]
    assert returned.status == "completed"
    assert returned.execute_allowed is True
    assert returned.mutated is False
    assert returned.return_value["handled"] is True
    assert returned.return_value["approved_by"] == "BBX19"
    assert returned.return_value["mpcp"]["result"] == "verified"


def test_cross_mpcp_rejects_unreviewed_handoff_without_calling_executor():
    chain = _chain()
    event = chain.events[0]
    handoff = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        review_approved=False,
    )
    calls = []

    with pytest.raises(PermissionError, match="human review"):
        execute_cross_handoff(
            chain,
            handoff,
            _approval(event.event_id),
            executor=lambda text: calls.append(text),
        )

    assert calls == []
    assert chain.events[0].return_value is None


def test_cross_mpcp_approval_is_scoped_to_chain_event_task_and_capability():
    chain = _chain()
    event = chain.events[0]
    handoff = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        review_approved=True,
    )

    with pytest.raises(PermissionError, match="scope"):
        execute_cross_handoff(
            chain,
            handoff,
            _approval(event.event_id, task="apply"),
            executor=lambda text: {"state": "SUCCESS", "cause": "verify"},
        )
    approval_without_capability = MPCPExecutionApproval(
        chain_id=chain.chain_id,
        event_id=event.event_id,
        task="verify",
        approved_by="BBX19",
        capabilities=(),
    )
    with pytest.raises(PermissionError, match=EXECUTION_CAPABILITY):
        execute_cross_handoff(
            chain,
            handoff,
            approval_without_capability,
            executor=lambda text: {"state": "SUCCESS", "cause": "verify"},
        )


def test_cross_mpcp_stop_result_stops_chain_and_preserves_error():
    chain = _chain()
    event = chain.events[0]
    handoff = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        review_approved=True,
    )

    result = execute_cross_handoff(
        chain,
        handoff,
        _approval(event.event_id),
        executor=lambda text: {
            "state": "STOP",
            "cause": "verify",
            "error": "BOUNDARY_DENIED",
        },
    )

    assert result.chain.state == "stopped"
    assert result.chain.events[0].status == "stopped"
    assert result.return_value["mpcp"]["error"] == "BOUNDARY_DENIED"


def test_cross_mpcp_non_mapping_or_unknown_result_fails_closed():
    chain = _chain()
    event = chain.events[0]
    handoff = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        review_approved=True,
    )

    result = execute_cross_handoff(
        chain,
        handoff,
        _approval(event.event_id),
        executor=lambda text: "bad result",
    )

    assert result.state == "STOP"
    assert result.chain.state == "stopped"
    assert (
        result.return_value["mpcp"]["error"]
        == "MPCP_EXECUTOR_RETURNED_NON_MAPPING"
    )


def test_cross_mpcp_executor_exception_is_bound_as_stop_return():
    chain = _chain()
    event = chain.events[0]
    handoff = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        review_approved=True,
    )

    def broken_executor(text):
        raise RuntimeError("worker unavailable")

    result = execute_cross_handoff(
        chain,
        handoff,
        _approval(event.event_id),
        executor=broken_executor,
    )

    assert result.state == "STOP"
    assert result.chain.state == "stopped"
    assert result.return_value["mpcp"]["error"].startswith(
        "MPCP_EXECUTOR_ERROR:RuntimeError"
    )


def test_event_return_can_only_be_bound_once():
    chain = _chain()
    event = chain.events[0]
    updated = bind_event_return(
        chain,
        event_id=event.event_id,
        return_value={"state": "SUCCESS"},
        status="completed",
        execute_allowed=True,
    )

    with pytest.raises(ValueError, match="already has a return"):
        bind_event_return(
            updated,
            event_id=event.event_id,
            return_value={"state": "SUCCESS"},
            status="completed",
            execute_allowed=True,
        )
    with pytest.raises(TypeError):
        updated.events[0].return_value["state"] = "STOP"  # type: ignore[index]
    nested = bind_event_return(
        _chain(),
        event_id=_chain().events[0].event_id,
        return_value={"mpcp": {"state": "SUCCESS", "trace": ["A", "B"]}},
        status="completed",
        execute_allowed=True,
    )
    with pytest.raises(TypeError):
        nested.events[0].return_value["mpcp"]["state"] = "STOP"  # type: ignore[index]
    assert nested.to_dict()["events"][0]["return_value"]["mpcp"]["trace"] == [
        "A",
        "B",
    ]
    with pytest.raises(FrozenInstanceError):
        updated.state = "stopped"  # type: ignore[misc]


def test_waiting_event_can_resume_without_losing_return_history():
    chain = _chain()
    event = chain.events[0]
    waiting = bind_event_return(
        chain,
        event_id=event.event_id,
        return_value={"state": "WAIT", "reason": "dependency"},
        status="waiting",
        execute_allowed=True,
    )
    completed = bind_event_return(
        waiting,
        event_id=event.event_id,
        return_value={"state": "SUCCESS", "result": "resumed"},
        status="completed",
        execute_allowed=True,
    )

    record = completed.events[0]
    assert completed.state == "completed"
    assert record.return_value["state"] == "SUCCESS"
    assert record.return_history[0]["state"] == "WAIT"
    assert completed.to_dict()["events"][0]["return_history"] == [
        {"state": "WAIT", "reason": "dependency"}
    ]


def test_cross_mpcp_context_cannot_override_task_or_inject_delimiters():
    chain = _chain()
    event = chain.events[0]
    approval = _approval(event.event_id)

    task_override = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        context={"TASK": "apply"},
        review_approved=True,
    )
    with pytest.raises(ValueError, match="override TASK"):
        execute_cross_handoff(
            chain,
            task_override,
            approval,
            executor=lambda text: {"state": "SUCCESS"},
        )

    injection = build_cross_mpcp_handoff(
        _cross_envelope(event.event_id),
        task="verify",
        context={"BOUNDARY": "safe,MODE:execute"},
        review_approved=True,
    )
    with pytest.raises(ValueError, match="delimiter"):
        execute_cross_handoff(
            chain,
            injection,
            approval,
            executor=lambda text: {"state": "SUCCESS"},
        )
