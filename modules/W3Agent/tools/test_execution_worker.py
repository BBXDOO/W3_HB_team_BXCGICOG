"""Tests for IGET execution_worker.

รันแบบเดียวกับ test อื่นในรีโป:
    PYTHONPATH=. python -m pytest modules/W3Agent/tools/test_execution_worker.py -q

ไม่ต้องมี github หรือ AI — Python ล้วน รันบน Termux ได้
"""

import importlib.util
import sys
from pathlib import Path


def load_worker():
    tools_dir = Path(__file__).resolve().parent
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))

    path = tools_dir / "execution_worker.py"
    spec = importlib.util.spec_from_file_location("w3_execution_worker", path)
    module = importlib.util.module_from_spec(spec)

    assert spec and spec.loader
    spec.loader.exec_module(module)

    return module


def test_worker_blocks_when_not_approved():
    worker = load_worker()

    result = worker.run_worker(
        issue_number=300,
        issue_title="test",
        issue_body="## Brief\nfix something",
        approval_status="held_by_bbx19",      # ไม่ใช่สถานะอนุมัติ
        write_files=False,
    )

    assert result.status == "blocked_not_approved"
    assert result.drafts == []
    assert any("approval required" in n.lower() for n in result.notes)


def test_worker_drafts_generic_scaffold_when_approved():
    worker = load_worker()

    result = worker.run_worker(
        issue_number=301,
        issue_title="add helper to core/utils.py",
        issue_body="## Brief\ncreate core/utils.py with a helper",
        approval_status="approved_by_bbx19",
        write_files=False,
    )

    assert result.status == "drafted"
    assert len(result.drafts) == 1
    draft = result.drafts[0]
    assert draft.mutation is False
    assert draft.needs_human_review is True
    assert "core/utils.py" in draft.target_path


def test_worker_result_never_reports_mutation():
    worker = load_worker()

    result = worker.run_worker(
        issue_number=302,
        issue_title="anything",
        issue_body="## Brief\nanything at all",
        approval_status="approved_run_requested",
        write_files=False,
    )

    payload = result.as_dict()
    assert payload["mutation"] is False
    assert payload["return_to"] == "IGET"
    for d in payload["drafts"]:
        assert d["mutation"] is False
        assert d["needs_human_review"] is True


def test_register_custom_builder():
    worker = load_worker()

    @worker.register_builder("TESTMOD")
    def _build(issue_title, brief, plan):
        return worker.PatchDraft(
            target_path="test/output.py",
            content="# test",
            summary="test draft",
            module="TESTMOD",
        )

    assert worker.has_builder("TESTMOD")

    result = worker.run_worker(
        issue_number=303,
        issue_title="test custom",
        issue_body="## Brief\nuse @module:TESTMOD here",
        approval_status="approved_by_bbx19",
        write_files=False,
    )

    assert result.status == "drafted"
    assert any(d.module == "TESTMOD" for d in result.drafts)


def test_render_worker_comment_keeps_boundary():
    worker = load_worker()

    result = worker.run_worker(
        issue_number=304,
        issue_title="x",
        issue_body="## Brief\nx",
        approval_status="approved_by_bbx19",
        write_files=False,
    )

    comment = worker.render_worker_comment(result)

    assert "MUTATION: `false`" in comment
    assert "RETURN_TO: `IGET`" in comment
    assert "BBX19 reviews and places" in comment

