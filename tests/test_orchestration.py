import importlib.util
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location("w3_orchestration", Path(__file__).resolve().parents[1] / "workflows" / "orchestration.py")
orc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orc)


def task():
    return orc.new_task("W3-ORC-20260929-1", "ISSUE", "HIGH", {"module": "Cast", "tier": 2},
                        {"summary": "stalled"}, source_id="RQ-1", human_review_required=True)


def test_support_returns_to_original_route_and_human_closes(tmp_path):
    t = task()
    orc.advance(t, "INSPECTING", actor="orchestrator", detail="checked")
    orc.advance(t, "QUEUED", actor="orchestrator", detail="ready")
    orc.route(t, {"module": "ChatGPT"}, actor="orchestrator",
              notify=lambda handoff: {"delivered": True, "evidence": "repo_events/handoff-1.json"})
    assert t["status"] == "ROUTED"
    with pytest.raises(ValueError):
        orc.advance(t, "COMPLETED", actor="orchestrator", detail="premature")
    orc.advance(t, "ACKNOWLEDGED", actor="ChatGPT", detail="accepted", evidence="ack-1")
    orc.advance(t, "IN_PROGRESS", actor="ChatGPT", detail="working")
    t["blocker"] = {"reason": "missing context"}
    orc.advance(t, "BLOCKED", actor="ChatGPT", detail="needs help")
    orc.assist(t, kind="TOOL", name="lookup", actor="orchestrator",
               handler=lambda context: {"resolved": True, "evidence": "lookup-1"})
    assert t["status"] == "RETURNED" and t["destination"]["module"] == "ChatGPT"
    orc.advance(t, "IN_PROGRESS", actor="ChatGPT", detail="resumed")
    orc.advance(t, "VERIFYING", actor="ChatGPT", detail="result ready", evidence="result-1")
    with pytest.raises(ValueError, match="human approval"):
        orc.advance(t, "COMPLETED", actor="orchestrator", detail="close")
    orc.approve(t, human="BBX19", evidence="review-1")
    orc.advance(t, "COMPLETED", actor="orchestrator", detail="closed")
    path = orc.save(t, tmp_path)
    assert path.exists() and t["completed_at"] and t["source_id"] == "RQ-1"


def test_failed_support_keeps_blocked_state():
    t = task()
    t["status"] = "BLOCKED"
    t["blocker"] = {"reason": "unknown"}
    def broken(_):
        raise RuntimeError("adapter unavailable")
    orc.assist(t, kind="SPECIALIST", name="expert", actor="orchestrator", handler=broken)
    assert t["status"] == "BLOCKED"
    assert not t["support"]
