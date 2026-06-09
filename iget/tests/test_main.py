"""Tests for IGET v9 runtime resolution and orchestration."""

import json

import pytest

from iget.main import RuntimeContext, resolve_runtime_context, run


class FakeClient:
    def __init__(self):
        self.upserts = []
        self.inline = []

    def fetch_pr_files(self, repo, pr):
        return [
            {"filename": "iget/main.py", "changes": 20, "additions": 15, "deletions": 5},
            {"filename": "iget/tests/test_main.py", "changes": 10, "additions": 10, "deletions": 0},
        ]

    def upsert_issue_comment(self, repo, pr, body):
        self.upserts.append((repo, pr, body))
        return "updated"

    def post_inline_comment(self, repo, pr, path, line, body):
        self.inline.append((repo, pr, path, line, body))


def test_runtime_context_uses_aliases_and_v9_defaults():
    context = resolve_runtime_context({
        "GITHUB_REPOSITORY": "owner/repo",
        "PR_NUMBER": "42",
        "GH_TOKEN": "token",
    })
    assert context.repo == "owner/repo"
    assert context.pr == 42
    assert context.timeout == 20.0
    assert context.inline_comments is False


def test_runtime_context_reads_pull_request_event(tmp_path):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({
        "number": 17,
        "repository": {"full_name": "owner/from-event"},
        "pull_request": {"number": 17},
    }), encoding="utf-8")
    context = resolve_runtime_context({"GITHUB_EVENT_PATH": str(event), "GITHUB_TOKEN": "token"})
    assert (context.repo, context.pr) == ("owner/from-event", 17)


def test_runtime_context_reads_manual_dispatch_input(tmp_path):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({
        "repository": {"full_name": "owner/repo"},
        "inputs": {"pr_number": "31"},
    }), encoding="utf-8")
    context = resolve_runtime_context({"GITHUB_EVENT_PATH": str(event), "GITHUB_TOKEN": "token"})
    assert context.pr == 31


@pytest.mark.parametrize("repo,pr", [("invalid", "1"), ("owner/repo", "zero"), ("owner/repo", "0")])
def test_runtime_context_rejects_invalid_identifiers(repo, pr):
    with pytest.raises(RuntimeError):
        resolve_runtime_context({"REPO": repo, "PR": pr, "GITHUB_TOKEN": "token"})


def test_run_updates_one_summary_and_uses_v9_marker():
    api = FakeClient()
    operation = run(RuntimeContext("owner/repo", 8, "token"), api)
    assert operation == "updated"
    assert len(api.upserts) == 1
    assert "<!-- iget:summary -->" in api.upserts[0][2]
    assert "IGET v9.0" in api.upserts[0][2]
    assert api.inline == []


def test_dry_run_does_not_write_comment(capsys):
    api = FakeClient()
    operation = run(RuntimeContext("owner/repo", 8, "token", dry_run=True), api)
    assert operation == "dry-run"
    assert api.upserts == []
    assert "IGET v9.0" in capsys.readouterr().out
