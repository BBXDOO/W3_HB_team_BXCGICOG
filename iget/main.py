import os
import sys

from .fetcher import fetch_pr_files, post_issue_comment, post_inline_comment
from .scorer import classify_files, build_stats, compute_score, detect_mode, get_state
from .reporter import (
    build_summary_lines,
    build_recommendations,
    build_inline_comments,
    build_comment,
)

# ==========================================
# ENV
# ==========================================
repo = os.getenv("REPO")
pr = os.getenv("PR")
token = os.getenv("GITHUB_TOKEN")

# ==========================================
# FETCH PR FILES (with pagination)
# ==========================================
files = fetch_pr_files(repo, pr, token)

if files is None:
    print("ERROR: Failed to fetch PR files", file=sys.stderr)
    sys.exit(1)

# ==========================================
# CLASSIFY & SCORE
# ==========================================
classified = classify_files(files)
stats = build_stats(files, classified)
mode = detect_mode(files, classified, stats)
score, issues = compute_score(files, classified, mode, stats)
state = get_state(score)

# ==========================================
# BUILD OUTPUT
# ==========================================
total_changes = stats["total_changes"]
summary_lines = build_summary_lines(files, classified, mode)
recommend = build_recommendations(files, classified, mode, total_changes)
inline_comments = build_inline_comments(files, classified, mode)
body = build_comment(score, state, issues, summary_lines, recommend)

# ==========================================
# POST INLINE COMMENTS
# ==========================================
for c in inline_comments:
    post_inline_comment(repo, pr, token, c["path"], c["line"], c["body"])

# ==========================================
# POST SUMMARY COMMENT
# ==========================================
post_issue_comment(repo, pr, token, body)
