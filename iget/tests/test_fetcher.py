"""Tests for IGET v9 GitHub API behavior."""

import json

import pytest

from iget.config import COMMENT_MARKER
from iget.fetcher import GitHubAPIError, GitHubClient, build_headers


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload
        self.text = text or (json.dumps(payload) if payload is not None else "")

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0)


def client(responses):
    return GitHubClient("token", session=FakeSession(responses), timeout=7)


def test_headers_report_v9_user_agent_and_api_version():
    headers = build_headers("secret")
    assert headers["User-Agent"] == "W3-IGET/9.0"
    assert headers["X-GitHub-Api-Version"] == "2022-11-28"
    assert headers["Authorization"] == "Bearer secret"


def test_fetch_pr_files_uses_one_client_and_pagination():
    first = [{"filename": f"file-{index}.py"} for index in range(100)]
    api = client([FakeResponse(payload=first), FakeResponse(payload=[{"filename": "last.py"}])])
    files = api.fetch_pr_files("owner/repo", 12)
    assert len(files) == 101
    assert [call[2]["params"]["page"] for call in api.session.calls] == [1, 2]
    assert all(call[2]["timeout"] == 7 for call in api.session.calls)


def test_upsert_updates_legacy_iget_bot_comment():
    comments = [
        {
            "id": 44,
            "body": "## 🔍 IGET v6.0\nold result",
            "user": {"login": "github-actions[bot]", "type": "Bot"},
        }
    ]
    api = client([FakeResponse(payload=comments), FakeResponse(payload={"id": 44})])
    operation = api.upsert_issue_comment("owner/repo", 5, f"{COMMENT_MARKER}\n## 🔍 IGET v9.0")
    assert operation == "updated"
    assert api.session.calls[-1][0] == "PATCH"
    assert api.session.calls[-1][1].endswith("/issues/comments/44")


def test_upsert_does_not_overwrite_human_comment_with_iget_heading():
    comments = [{"id": 9, "body": "## 🔍 IGET v6.0", "user": {"login": "person", "type": "User"}}]
    api = client([FakeResponse(payload=comments), FakeResponse(status_code=201, payload={"id": 10})])
    assert api.upsert_issue_comment("owner/repo", 5, f"{COMMENT_MARKER}\nresult") == "created"
    assert api.session.calls[-1][0] == "POST"


def test_api_error_contains_status_without_hiding_failure():
    api = client([FakeResponse(status_code=403, text="Resource not accessible")])
    with pytest.raises(GitHubAPIError, match="403.*Resource not accessible"):
        api.fetch_pr_files("owner/repo", 1)
