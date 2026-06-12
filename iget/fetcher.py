"""IGET v9 resilient GitHub API client."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import COMMENT_MARKER, DEFAULT_API_URL, DEFAULT_TIMEOUT, GITHUB_PAGE_SIZE, VERSION


class GitHubAPIError(RuntimeError):
    """Raised when GitHub returns an unexpected response."""


class GitHubClient:
    """Small reusable GitHub client with retries, pagination and comment upsert."""

    def __init__(
        self,
        token: str,
        *,
        api_url: str = DEFAULT_API_URL,
        timeout: float = DEFAULT_TIMEOUT,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.session = session or build_session()
        self.headers = build_headers(token)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        response = self.session.request(
            method,
            f"{self.api_url}{path}",
            headers=self.headers,
            timeout=self.timeout,
            **kwargs,
        )
        if not 200 <= response.status_code < 300:
            detail = response.text.strip().replace("\n", " ")[:300]
            raise GitHubAPIError(
                f"GitHub API {method} {path} returned {response.status_code}: {detail or 'no response body'}"
            )
        return response

    def _pages(self, path: str) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        page = 1
        while True:
            response = self._request(
                "GET",
                path,
                params={"per_page": GITHUB_PAGE_SIZE, "page": page},
            )
            batch = response.json()
            if not isinstance(batch, list):
                raise GitHubAPIError(f"GitHub API GET {path} returned a non-list payload")
            items.extend(batch)
            if len(batch) < GITHUB_PAGE_SIZE:
                return items
            page += 1

    def fetch_pr_files(self, repo: str, pr: int) -> List[Dict[str, Any]]:
        return self._pages(f"/repos/{repo}/pulls/{pr}/files")

    def list_issue_comments(self, repo: str, pr: int) -> List[Dict[str, Any]]:
        return self._pages(f"/repos/{repo}/issues/{pr}/comments")

    def upsert_issue_comment(self, repo: str, pr: int, body: str) -> str:
        """Create or update the latest IGET summary and return the operation."""
        existing = None
        for comment in reversed(self.list_issue_comments(repo, pr)):
            comment_body = str(comment.get("body", ""))
            user = comment.get("user") or {}
            login = str(user.get("login", ""))
            is_iget = COMMENT_MARKER in comment_body or comment_body.startswith("## 🔍 IGET v")
            is_bot = user.get("type") == "Bot" or login.endswith("[bot]")
            if is_iget and is_bot and comment.get("id"):
                existing = comment
                break

        if existing:
            self._request(
                "PATCH",
                f"/repos/{repo}/issues/comments/{existing['id']}",
                json={"body": body},
            )
            return "updated"

        self._request(
            "POST",
            f"/repos/{repo}/issues/{pr}/comments",
            json={"body": body},
        )
        return "created"

    def post_inline_comment(self, repo: str, pr: int, path: str, line: int, body: str) -> None:
        self._request(
            "POST",
            f"/repos/{repo}/pulls/{pr}/comments",
            json={"path": path, "line": line, "side": "RIGHT", "body": body},
        )


def build_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"W3-IGET/{VERSION}",
    }


def build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        status=4,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "PATCH"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


# Compatibility functions for callers using the pre-v9 module API.
def fetch_pr_files(repo: str, pr: int, token: str):
    return GitHubClient(token).fetch_pr_files(repo, int(pr))


def post_issue_comment(repo: str, pr: int, token: str, body: str):
    GitHubClient(token).upsert_issue_comment(repo, int(pr), body)
    return True


def post_inline_comment(repo: str, pr: int, token: str, path: str, line: int, body: str):
    GitHubClient(token).post_inline_comment(repo, int(pr), path, line, body)
    return True
