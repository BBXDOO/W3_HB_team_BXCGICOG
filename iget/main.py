# ==========================================
# IGET v7.0 — Main Entry Point
# Semantic pipeline: fetch → classify → score → semantic → report
# Ontology tag: iget:module = "main"
# MPCP role: governance_assistant
# ==========================================

from __future__ import annotations

import os
import sys

from .fetcher import fetch_pr_files, post_inline_comment, post_issue_comment
from .proof   import ProofTracer
from .reporter import (
    build_comment,
    build_inline_comments,
    build_recommendations,
    build_summary_lines,
)
from .scorer import (
    build_stats,
    classify_files,
    compute_score,
    detect_mode,
    get_semantic_state,
    get_state,
)


# ── Environment resolution ─────────────────────────────────────

def _resolve_runtime_env() -> tuple[str, str, str]:
    """
    IGET v7 runtime env resolution.
    Supports both direct vars and GitHub Actions aliases.
    error_proof: raises RuntimeError with missing var names.
    Ontology tag: iget:env_resolution
    """
    repo  = os.getenv("REPO")  or os.getenv("GITHUB_REPOSITORY")
    pr    = os.getenv("PR")    or os.getenv("PR_NUMBER") or os.getenv("GITHUB_PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

    missing = [
        name
        for name, value in (("REPO", repo), ("PR", pr), ("GITHUB_TOKEN", token))
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required environment values: {', '.join(missing)}")
    return repo, pr, token  # type: ignore[return-value]


# ── Main pipeline ──────────────────────────────────────────────

def main() -> int:
    """
    IGET v7.0 — full semantic governance pipeline.

    Pipeline:
        env_resolve
        → fetch_pr_files        (with recovery)
        → classify_files        (with proof)
        → build_stats
        → detect_mode
        → compute_score         (with causal proof)
        → get_state
        → get_semantic_state    (v7 new)
        → build_summary / recommend / inline
        → build_comment         (with semantic + proof trace)
        → post_inline_comments
        → post_issue_comment

    Ontology tag: iget:main_pipeline
    MPCP claim: governance_assistant v7.0
    """

    # ── 1. Init tracer ────────────────────────────────────────
    tracer = ProofTracer()
    tracer.record("pipeline_start", "IGET v7.0 pipeline started", None, "iget:pipeline_start")

    # ── 2. Resolve env ────────────────────────────────────────
    try:
        repo, pr, token = _resolve_runtime_env()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    tracer.record("env_resolved", f"repo={repo} pr={pr}", None, "iget:env_resolved")

    # ── 3. Fetch PR files (with checkpoint/recovery) ──────────
    files = fetch_pr_files(repo, pr, token, tracer=tracer)
    if files is None:
        print("ERROR: Failed to fetch PR files", file=sys.stderr)
        tracer.record("pipeline_error", "fetch failed — abort", None, "iget:error")
        return 1

    # ── 4. Classify ───────────────────────────────────────────
    classified = classify_files(files, tracer=tracer)

    # ── 5. Stats + Mode ───────────────────────────────────────
    stats = build_stats(files, classified, tracer=tracer)
    mode  = detect_mode(files, classified, stats, tracer=tracer)

    # ── 6. Score (causal proof recorded inside) ───────────────
    score, issues = compute_score(files, classified, mode, stats, tracer=tracer)

    # ── 7. State + Semantic State (v7) ────────────────────────
    state          = get_state(score, tracer=tracer)
    semantic_state = get_semantic_state(score, state, classified, tracer=tracer)

    # ── 8. Build output sections ──────────────────────────────
    total_changes   = stats["total_changes"]
    summary_lines   = build_summary_lines(files, classified, mode, tracer=tracer)
    recommend       = build_recommendations(files, classified, mode, total_changes, tracer=tracer)
    inline_comments = build_inline_comments(files, classified, mode, tracer=tracer)

    # ── 9. Finalise proof trace ───────────────────────────────
    tracer.record("pipeline_complete", f"score={score} state={state} "
                  f"semantic={semantic_state['semantic_key']}", None, "iget:pipeline_complete")
    mpcp_result = tracer.to_mpcp_result()

    # ── 10. Assemble comment ──────────────────────────────────
    body = build_comment(
        score, state, issues,
        summary_lines, recommend,
        semantic_state = semantic_state,
        mpcp_result    = mpcp_result,
        tracer         = tracer,
    )

    # ── 11. Post inline comments ──────────────────────────────
    for c in inline_comments:
        post_inline_comment(repo, pr, token, c["path"], c["line"], c["body"], tracer=tracer)

    # ── 12. Post main comment ─────────────────────────────────
    post_issue_comment(repo, pr, token, body, tracer=tracer)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
