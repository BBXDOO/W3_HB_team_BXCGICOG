# ==========================================
# IGET v7.0 — Benchmark
# v5 profiles + semantic state + proof trace
# ==========================================

import json
from datetime import datetime, timezone

from .config import VERSION
from .proof import ProofTracer
from .scorer import (
    build_stats,
    classify_files,
    compute_score,
    detect_mode,
    get_semantic_state,
    get_state,
)

# ── Benchmark profiles (v5 original) ──────────────────────────
BENCHMARK_PROFILES = [
    {
        "name": "tiny-fix",
        "description": "Small single-file bug fix",
        "files": [{"filename": "src/utils.py", "changes": 8}],
    },
    {
        "name": "docs-only",
        "description": "Documentation update",
        "files": [
            {"filename": "README.md", "changes": 40},
            {"filename": "docs/guide.md", "changes": 15},
        ],
    },
    {
        "name": "feature-with-tests",
        "description": "New feature with test coverage",
        "files": [
            {"filename": "src/auth.py", "changes": 120},
            {"filename": "src/models.py", "changes": 60},
            {"filename": "tests/test_auth.py", "changes": 80},
        ],
    },
    {
        "name": "feature-no-tests",
        "description": "Feature without tests (should penalise)",
        "files": [
            {"filename": "src/auth.py", "changes": 120},
            {"filename": "src/models.py", "changes": 60},
        ],
    },
    {
        "name": "large-pr",
        "description": "Large PR with many files",
        "files": [
            {"filename": f"src/module_{i}.py", "changes": 50}
            for i in range(20)
        ],
    },
    {
        "name": "risky-secret",
        "description": "PR touching a secrets file",
        "files": [
            {"filename": "config/credentials.yml", "changes": 10},
            {"filename": "src/app.py", "changes": 30},
        ],
    },
    {
        "name": "very-large-pr",
        "description": "Very large PR simulating 150-file repo refactor",
        "files": [
            {"filename": f"src/file_{i}.py", "changes": 20}
            for i in range(150)
        ],
    },
    {
        "name": "workflow-change",
        "description": "PR that modifies a CI workflow file",
        "files": [
            {"filename": ".github/workflows/ci.yml", "changes": 25},
            {"filename": "src/main.py", "changes": 10},
        ],
    },
    {
        "name": "mixed-docs-code",
        "description": "Mixed documentation and code changes",
        "files": [
            {"filename": "README.md", "changes": 30},
            {"filename": "src/core.py", "changes": 50},
            {"filename": "tests/test_core.py", "changes": 40},
        ],
    },
]


# ── Runner ─────────────────────────────────────────────────────

def run_benchmark(profiles=None):
    """
    Run scoring benchmark against all profiles.
    v7.0: adds semantic_state + proof trace per profile.
    Returns a list of result dicts.
    """
    if profiles is None:
        profiles = BENCHMARK_PROFILES

    results = []
    for profile in profiles:
        tracer = ProofTracer()
        files = profile["files"]

        classified = classify_files(files, tracer=tracer)
        stats      = build_stats(files, classified, tracer=tracer)
        mode       = detect_mode(files, classified, stats, tracer=tracer)
        score, issues = compute_score(files, classified, mode, stats, tracer=tracer)
        state      = get_state(score, tracer=tracer)
        semantic   = get_semantic_state(score, state, classified, tracer=tracer)

        results.append({
            "profile":       profile["name"],
            "description":   profile["description"],
            "total_files":   len(files),
            "total_changes": sum(f.get("changes", 0) for f in files),
            "mode":          mode,
            "score":         score,
            "state":         state,
            # v7.0 additions
            "semantic_key":  semantic["semantic_key"],
            "semantic_label":semantic["label"],
            "semantic_proof":semantic["proof"],
            "issues":        issues,
            "proof_trace":   tracer.to_mpcp_result(),
        })

    return results


# ── Formatters ─────────────────────────────────────────────────

def format_benchmark_report(results):
    """Format benchmark results as a human-readable markdown report."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# IGET v{VERSION} — Benchmark Report",
        f"_Generated: {ts}_",
        "",
        "| Profile | Files | Changes | Mode | Score | State | Semantic |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for r in results:
        state_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(r["state"], "⚪")
        sem_icon   = {
            "safe":     "✅",
            "caution":  "⚠️",
            "critical": "🚨",
            "unknown":  "❓",
        }.get(r["semantic_key"], "❓")

        lines.append(
            f"| {r['profile']} | {r['total_files']} | {r['total_changes']} "
            f"| {r['mode']} | {r['score']} | {state_icon} {r['state']} "
            f"| {sem_icon} {r['semantic_key']} |"
        )

    lines += ["", "## Details", ""]
    for r in results:
        lines.append(f"### {r['profile']}")
        lines.append(f"_{r['description']}_")
        lines.append(f"- Score: **{r['score']}** ({r['state']})")
        lines.append(f"- Semantic: **{r['semantic_key']}** — {r['semantic_label']}")
        if r["semantic_proof"]:
            for p in r["semantic_proof"]:
                lines.append(f"  - {p}")
        if r["issues"]:
            lines.append("- Issues: " + ", ".join(r["issues"]))
        # proof trace summary
        trace = r["proof_trace"]
        steps = " → ".join(e["step"] for e in trace.get("trace", []))
        lines.append(f"- Trace ({trace.get('elapsed_sec', 0)}s): `{steps}`")
        lines.append("")

    return "\n".join(lines)


# ── Entry point ────────────────────────────────────────────────

if __name__ == "__main__":
    results = run_benchmark()
    report  = format_benchmark_report(results)
    print(report)

    with open("/tmp/iget_benchmark_v7.json", "w") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print("\nJSON saved to /tmp/iget_benchmark_v7.json")
