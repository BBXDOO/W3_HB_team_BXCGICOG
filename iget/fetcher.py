# ==========================================
# IGET v8.0 — GitHub API Fetcher
# Recovery / Resilience: checkpoint, retry, error_proof
# Ontology tag: iget:module = "fetcher"
# ==========================================

from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import GITHUB_PAGE_SIZE, MAX_FETCH_RETRY, ROLLBACK_ON_FAIL
from .proof import ProofTracer


# ── Session factory ────────────────────────────────────────────

def _build_session() -> requests.Session:
    """
    Shared retry-capable session.
    Recovery: exponential backoff on 429/5xx, pool reuse.
    Ontology tag: iget:resilience
    """
    session = requests.Session()
    retry = Retry(
        total              = MAX_FETCH_RETRY,
        connect            = MAX_FETCH_RETRY,
        read               = MAX_FETCH_RETRY,
        backoff_factor     = 0.5,
        status_forcelist   = (429, 500, 502, 503, 504),
        allowed_methods    = ("GET", "POST"),
        raise_on_status    = False,
    )
    adapter = HTTPAdapter(
        max_retries    = retry,
        pool_connections = 10,
        pool_maxsize   = 10,
    )
    session.mount("https://", adapter)
    session.mount("http://",  adapter)
    return session


def _build_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept":        "application/vnd.github+json",
    }


# ── Core fetch ────────────────────────────────────────────────

def fetch_pr_files(
    repo:    str,
    pr:      str,
    token:   str,
    tracer:  ProofTracer | None = None,
) -> list[dict] | None:
    """
    Fetch all files for a PR with pagination + checkpoint recovery.

    Checkpoint: accumulates pages; partial result preserved on error.
    Rollback: returns None (not partial) when ROLLBACK_ON_FAIL=True
              so caller gets a clean failure signal.

    Ontology tag: iget:fetch_pr_files
    """
    tracer = tracer or ProofTracer(enabled=False)
    headers  = _build_headers(token)
    base_url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
    session  = _build_session()

    all_files: list[dict] = []   # checkpoint accumulator
    page = 1

    tracer.record(
        "fetch_start",
        f"begin fetch PR#{pr} repo={repo}",
        {"repo": repo, "pr": pr},
        "iget:fetch_start",
    )

    while True:
        params = {"per_page": GITHUB_PAGE_SIZE, "page": page}
        try:
            res = session.get(base_url, headers=headers, params=params, timeout=15)
        except requests.RequestException as exc:
            # error_proof: log and return clean failure
            tracer.record(
                "fetch_network_error",
                f"network error on page {page}: {exc}",
                {"page": page, "error": str(exc)},
                "iget:error",
            )
            return None if ROLLBACK_ON_FAIL else (all_files or None)

        if res.status_code != 200:
            tracer.record(
                "fetch_http_error",
                f"HTTP {res.status_code} on page {page}",
                {"status": res.status_code, "page": page},
                "iget:error",
            )
            return None if ROLLBACK_ON_FAIL else (all_files or None)

        batch = res.json()
        if not batch:
            break

        all_files.extend(batch)
        tracer.record(
            f"fetch_page_{page}",
            f"fetched {len(batch)} files (total {len(all_files)})",
            {"page": page, "batch_size": len(batch)},
            "iget:fetch_page",
        )

        if len(batch) < GITHUB_PAGE_SIZE:
            break
        page += 1

    tracer.record(
        "fetch_complete",
        f"fetched {len(all_files)} files total",
        {"total_files": len(all_files)},
        "iget:fetch_complete",
    )
    return all_files


# ── Comment posting ────────────────────────────────────────────

def post_issue_comment(
    repo:    str,
    pr:      str,
    token:   str,
    body:    str,
    tracer:  ProofTracer | None = None,
) -> bool:
    """
    Post a comment on a PR/issue.
    error_proof: returns False on failure, never raises.
    Ontology tag: iget:post_comment
    """
    tracer = tracer or ProofTracer(enabled=False)
    headers = _build_headers(token)
    url     = f"https://api.github.com/repos/{repo}/issues/{pr}/comments"
    session = _build_session()

    try:
        res = session.post(url, headers=headers, json={"body": body}, timeout=15)
        ok  = res.status_code in (200, 201)
    except requests.RequestException as exc:
        tracer.record("post_comment_error", str(exc), None, "iget:error")
        return False

    tracer.record(
        "post_comment",
        f"comment posted: {ok} (HTTP {res.status_code})",
        {"status": res.status_code},
        "iget:post_comment",
    )
    return ok


def post_inline_comment(
    repo:    str,
    pr:      str,
    token:   str,
    path:    str,
    line:    int,
    body:    str,
    tracer:  ProofTracer | None = None,
) -> bool:
    """
    Post an inline review comment on a PR file.
    error_proof: returns False on failure, never raises.
    Ontology tag: iget:post_inline_comment
    """
    tracer  = tracer or ProofTracer(enabled=False)
    headers = _build_headers(token)
    url     = f"https://api.github.com/repos/{repo}/pulls/{pr}/comments"
    payload = {"path": path, "line": line, "body": body}
    session = _build_session()

    try:
        res = session.post(url, headers=headers, json=payload, timeout=15)
        ok  = res.status_code in (200, 201)
    except requests.RequestException as exc:
        tracer.record("post_inline_error", str(exc), None, "iget:error")
        return False

    tracer.record(
        "post_inline",
        f"inline comment on {path}:{line} → {ok}",
        {"path": path, "line": line, "status": res.status_code},
        "iget:post_inline_comment",
    )
    return ok
