import importlib.util
from pathlib import Path


def load_approval_gate():
    path = Path(__file__).resolve().parent / "approval_gate.py"
    spec = importlib.util.spec_from_file_location("approval_gate", path)
    module = importlib.util.module_from_spec(spec)

    assert spec and spec.loader
    spec.loader.exec_module(module)

    return module


def test_parse_approval_command():
    gate = load_approval_gate()

    command = gate.parse_approval_command("/iget approve")

    assert command is not None
    assert command.action == "approve"
    assert command.raw == "/iget approve"


def test_extract_module_tags_from_issue_body():
    gate = load_approval_gate()

    body = """
    ## Suggested modules

    - @module:IGET
    - @module:MPCP
    - @module:IGET
    """

    assert gate.extract_module_tags(body) == ["IGET", "MPCP"]


def test_authorized_actor():
    gate = load_approval_gate()

    assert gate.is_authorized_actor("BBXDOO") is True
    assert gate.is_authorized_actor("BBX19") is True
    assert gate.is_authorized_actor("random-user") is False


def test_build_approval_response_contains_trace_and_plan():
    gate = load_approval_gate()

    issue_body = """
Source: BBX19
Mode: issue_dispatch
Risk: medium

## Brief

ตรวจชุดโค้ดและ logic ว่าระดับความสามารถทำงานได้ตรงตามคอนเซปหรือไม่

## Suggested modules

- @module:W3DB
- @module:LRC2
"""

    response = gate.build_approval_response(
        issue_number=264,
        issue_title="ตรวจความสมบูรณ์โค้ดของโมดูล LRC2",
        issue_body=issue_body,
        comment_body="/iget approve",
        actor="BBXDOO",
    )

    assert "IGET Approval Gate" in response
    assert "Status: `approved_by_bbx19`" in response
    assert "`@module:W3DB`" in response
    assert "`@module:LRC2`" in response
    assert "RETURN_TO: `IGET`" in response
    assert "MUTATION: `false`" in response
    assert "TRACE: `approval_gate`" in response


def test_reject_command_stops_flow():
    gate = load_approval_gate()

    response = gate.build_approval_response(
        issue_number=1,
        issue_title="Test",
        issue_body="## Suggested modules\n\n- @module:IGET",
        comment_body="/iget reject",
        actor="BBX19",
    )

    assert "Status: `rejected_by_bbx19`" in response
    assert "Next mode: `stop`" in response


def test_unauthorized_actor_is_denied():
    gate = load_approval_gate()

    response = gate.build_approval_response(
        issue_number=1,
        issue_title="Test",
        issue_body="## Suggested modules\n\n- @module:IGET",
        comment_body="/iget approve",
        actor="unknown-user",
    )

    assert "approval_denied" in response
    assert "MUTATION: `false`" in response
    assert "TRACE: `approval_gate_denied`" in response
