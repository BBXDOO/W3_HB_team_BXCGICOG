import os
import sys

from .fetcher import fetch_pr_files, post_issue_comment, post_inline_comment
from .reporter import (
    build_comment,
    build_inline_comments,
    build_recommendations,
    build_summary_lines,
)
from .scorer import build_stats, classify_files, compute_score, detect_mode, get_state


def _resolve_runtime_env() -> tuple[str, str, str]:
    """IGET v6 runtime env resolution with backward-compatible aliases."""
    repo = os.getenv("REPO") or os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("PR") or os.getenv("PR_NUMBER") or os.getenv("GITHUB_PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

    missing = [
        name
        for name, value in (("REPO", repo), ("PR", pr), ("GITHUB_TOKEN", token))
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required environment values: {', '.join(missing)}")
    return repo, pr, token


def main() -> int:
    try:
        repo, pr, token = _resolve_runtime_env()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    files = fetch_pr_files(repo, pr, token)
    if files is None:
        print("ERROR: Failed to fetch PR files", file=sys.stderr)
        return 1

    classified = classify_files(files)
    stats = build_stats(files, classified)
    mode = detect_mode(files, classified, stats)
    score, issues = compute_score(files, classified, mode, stats)
    state = get_state(score)

    total_changes = stats["total_changes"]
    summary_lines = build_summary_lines(files, classified, mode)
    recommend = build_recommendations(files, classified, mode, total_changes)
    inline_comments = build_inline_comments(files, classified, mode)
    body = build_comment(score, state, issues, summary_lines, recommend)

    for c in inline_comments:
        post_inline_comment(repo, pr, token, c["path"], c["line"], c["body"])

    post_issue_comment(repo, pr, token, body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
