# ==========================================
# IGET v5 — GitHub API Fetcher
# ==========================================

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import GITHUB_PAGE_SIZE


def build_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


def build_session():
    """Shared retry-capable session for better API reliability and speed."""
    session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.4,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "POST"),
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_pr_files(repo, pr, token):
    """
    Fetch all files for a PR, handling pagination for very large PRs.
    Returns a list of file objects or None on error.
    """
    headers = build_headers(token)
    base_url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"

    all_files = []
    page = 1
    session = build_session()

    while True:
        params = {"per_page": GITHUB_PAGE_SIZE, "page": page}
        res = session.get(base_url, headers=headers, params=params, timeout=15)

        if res.status_code != 200:
            return None

        batch = res.json()
        if not batch:
            break

        all_files.extend(batch)
        if len(batch) < GITHUB_PAGE_SIZE:
            break
        page += 1

    return all_files


def post_issue_comment(repo, pr, token, body):
    """Post a comment on a PR/issue."""
    headers = build_headers(token)
    url = f"https://api.github.com/repos/{repo}/issues/{pr}/comments"
    session = build_session()
    res = session.post(url, headers=headers, json={"body": body}, timeout=15)
    return res.status_code in (200, 201)


def post_inline_comment(repo, pr, token, path, line, body):
    """Post an inline review comment on a PR file."""
    headers = build_headers(token)
    url = f"https://api.github.com/repos/{repo}/pulls/{pr}/comments"
    payload = {"path": path, "line": line, "body": body}
    session = build_session()
    res = session.post(url, headers=headers, json=payload, timeout=15)
    return res.status_code in (200, 201)
