"""IGET v9 PR governance entrypoint."""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

from .config import DEFAULT_API_URL, DEFAULT_TIMEOUT, VERSION
from .fetcher import GitHubAPIError, GitHubClient
from .proof import ProofTracer
from .reporter import build_comment, build_inline_comments, build_recommendations, build_summary_lines
from .scorer import (
    build_stats,
    classify_files,
    compute_score,
    detect_mode,
    get_semantic_state,
    get_state,
)

REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class RuntimeContext:
    repo: str
    pr: int
    token: str
    api_url: str = DEFAULT_API_URL
    timeout: float = DEFAULT_TIMEOUT
    dry_run: bool = False
    inline_comments: bool = False


def _load_event(path: Optional[str]) -> Mapping[str, Any]:
    if not path:
        return {}
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read GITHUB_EVENT_PATH: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("GITHUB_EVENT_PATH must contain a JSON object")
    return payload


def _event_pr(event: Mapping[str, Any]) -> Optional[Any]:
    pull_request = event.get("pull_request")
    if isinstance(pull_request, Mapping):
        return pull_request.get("number") or event.get("number")
    inputs = event.get("inputs")
    if isinstance(inputs, Mapping):
        return inputs.get("pr_number")
    return event.get("number")


def resolve_runtime_context(environ: Optional[Mapping[str, str]] = None) -> RuntimeContext:
    """Resolve v9 runtime context from explicit aliases and the GitHub event payload."""
    env = os.environ if environ is None else environ
    event = _load_event(env.get("GITHUB_EVENT_PATH"))
    repository = event.get("repository")
    event_repo = repository.get("full_name", "") if isinstance(repository, Mapping) else ""
    repo = env.get("REPO") or env.get("GITHUB_REPOSITORY") or str(event_repo)
    pr_value = (
        env.get("PR")
        or env.get("PR_NUMBER")
        or env.get("GITHUB_PR_NUMBER")
        or env.get("INPUT_PR_NUMBER")
        or _event_pr(event)
    )
    token = env.get("GITHUB_TOKEN") or env.get("GH_TOKEN") or ""

    missing = [name for name, value in (("REPO", repo), ("PR", pr_value), ("GITHUB_TOKEN", token)) if not value]
    if missing:
        raise RuntimeError(f"Missing required runtime values: {', '.join(missing)}")
    if not REPOSITORY_PATTERN.fullmatch(str(repo)):
        raise RuntimeError("REPO must use the 'owner/repository' format")
    try:
        pr = int(str(pr_value))
    except (TypeError, ValueError) as exc:
        raise RuntimeError("PR must be a positive integer") from exc
    if pr < 1:
        raise RuntimeError("PR must be a positive integer")
    try:
        timeout = float(env.get("IGET_HTTP_TIMEOUT", DEFAULT_TIMEOUT))
    except ValueError as exc:
        raise RuntimeError("IGET_HTTP_TIMEOUT must be numeric") from exc
    if timeout <= 0:
        raise RuntimeError("IGET_HTTP_TIMEOUT must be greater than zero")

    return RuntimeContext(
        repo=str(repo),
        pr=pr,
        token=str(token),
        api_url=env.get("GITHUB_API_URL", DEFAULT_API_URL),
        timeout=timeout,
        dry_run=_mapping_bool(env, "IGET_DRY_RUN"),
        inline_comments=_mapping_bool(env, "IGET_INLINE_COMMENTS"),
    )


def _mapping_bool(env: Mapping[str, str], name: str) -> bool:
    return str(env.get(name, "")).strip().lower() in {"1", "true", "yes", "on"}


def run(context: RuntimeContext, client: Optional[GitHubClient] = None) -> str:
    """Analyze one PR, publish one idempotent summary, and return the operation."""
    api = client or GitHubClient(
        context.token,
        api_url=context.api_url,
        timeout=context.timeout,
    )
    tracer = ProofTracer()
    files = api.fetch_pr_files(context.repo, context.pr)
    classified = classify_files(files, tracer)
    stats = build_stats(files, classified, tracer)
    mode = detect_mode(files, classified, stats, tracer)
    score, issues = compute_score(files, classified, mode, stats, tracer)
    state = get_state(score, tracer)
    semantic_state = get_semantic_state(score, state, classified, tracer)
    summary = build_summary_lines(files, classified, mode, tracer)
    recommendations = build_recommendations(
        files, classified, mode, stats["total_changes"], tracer
    )
    body = build_comment(
        score,
        state,
        issues,
        summary,
        recommendations,
        semantic_state=semantic_state,
        mpcp_result=tracer.to_mpcp_result(),
        tracer=tracer,
    )

    if context.dry_run:
        print(body)
        return "dry-run"

    operation = api.upsert_issue_comment(context.repo, context.pr, body)
    if context.inline_comments:
        for comment in build_inline_comments(files, classified, mode, tracer):
            try:
                api.post_inline_comment(
                    context.repo,
                    context.pr,
                    comment["path"],
                    comment["line"],
                    comment["body"],
                )
            except GitHubAPIError as exc:
                print(f"WARNING: inline comment skipped: {exc}", file=sys.stderr)
    return operation


def main() -> int:
    try:
        context = resolve_runtime_context()
        operation = run(context)
    except (RuntimeError, GitHubAPIError) as exc:
        print(f"ERROR: IGET v{VERSION}: {exc}", file=sys.stderr)
        return 1
    print(f"IGET v{VERSION}: {operation} summary for {context.repo}#{context.pr}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
