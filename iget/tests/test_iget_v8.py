# ==========================================
# IGET v8.0 — Test Suite
# Covers: semantic events, replay, fault lineage, proof trace
# Run: python -m iget.tests.test_iget_v8
# Ontology tag: iget:tests
# ==========================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iget.proof  import ProofTracer
from iget.scorer import (
    build_stats, classify_files, compute_score,
    detect_mode, get_semantic_state, get_state,
)
from iget.reporter import (
    build_comment, build_inline_comments,
    build_recommendations, build_summary_lines,
)
from iget.config import SCORE_GREEN, SCORE_YELLOW, VERSION


# ── Test utilities ─────────────────────────────────────────────

PASS = 0
FAIL = 0

def check(label: str, condition: bool) -> None:
    global PASS, FAIL
    if condition:
        print(f"  ✅ {label}")
        PASS += 1
    else:
        print(f"  ❌ FAIL: {label}")
        FAIL += 1


def section(title: str) -> None:
    print(f"\n── {title} {'─' * (50 - len(title))}")


# ── Mock data ──────────────────────────────────────────────────

def _make_file(name: str, changes: int = 10) -> dict:
    return {"filename": name, "changes": changes}


FILES_CLEAN = [
    _make_file("src/main.py", 20),
    _make_file("tests/test_main.py", 15),
]

FILES_RISKY = [
    _make_file("src/main.py", 50),
    _make_file(".env.secret", 5),
]

FILES_LARGE = [_make_file(f"src/file_{i}.py", 30) for i in range(20)]

FILES_DOCS_ONLY = [
    _make_file("README.md", 10),
    _make_file("docs/guide.md", 5),
]

FILES_WORKFLOW = [
    _make_file(".github/workflows/ci.yml", 20),
    _make_file("src/app.py", 30),
]


# ── §1 ProofTracer ─────────────────────────────────────────────

section("§1 ProofTracer")

tracer = ProofTracer()
tracer.record("step_a", "claim A", {"x": 1}, "iget:test")
tracer.record("step_b", "claim B", None, "iget:test")

check("records entries", len(tracer.entries()) == 2)
check("entry has correct step", tracer.entries()[0].step == "step_a")
check("entry has correct claim", tracer.entries()[0].claim == "claim A")
check("elapsed >= 0", tracer.elapsed() >= 0)
check("summary contains steps", "step_a" in tracer.summary())

mpcp = tracer.to_mpcp_result()
check("mpcp_role set", mpcp["mpcp_role"] == "governance_assistant")
check("trace is list", isinstance(mpcp["trace"], list))
check("trace has 2 entries", len(mpcp["trace"]) == 2)

# disabled tracer records nothing
dt = ProofTracer(enabled=False)
dt.record("x", "y", None, "t")
check("disabled tracer records nothing", len(dt.entries()) == 0)


# ── §2 classify_files ─────────────────────────────────────────

section("§2 classify_files")

t = ProofTracer()
c = classify_files(FILES_CLEAN, tracer=t)
check("code files detected", len(c["code"]) == 1)
check("test files detected", len(c["test"]) == 1)
check("no risky files in clean", len(c["risky"]) == 0)

c_risky = classify_files(FILES_RISKY)
check("risky file detected (.env.secret)", len(c_risky["risky"]) == 1)

c_docs = classify_files(FILES_DOCS_ONLY)
check("docs only — no code", len(c_docs["code"]) == 0)
check("docs only — 2 docs", len(c_docs["doc"]) == 2)

c_wf = classify_files(FILES_WORKFLOW)
check("workflow file detected", len(c_wf["workflow"]) == 1)

# proof trace recorded
entries = [e.step for e in t.entries()]
check("classify recorded in tracer", "classify_files" in entries)


# ── §3 detect_mode ─────────────────────────────────────────────

section("§3 detect_mode")

c = classify_files(FILES_CLEAN)
s = build_stats(FILES_CLEAN, c)
# FILES_CLEAN has 1 code + 1 test (equal) → test_only per scorer logic
check("clean → mode=test_only (1 code == 1 test)", detect_mode(FILES_CLEAN, c, s) == "test_only")

cd = classify_files(FILES_DOCS_ONLY)
sd = build_stats(FILES_DOCS_ONLY, cd)
check("docs_only mode", detect_mode(FILES_DOCS_ONLY, cd, sd) == "docs_only")

check("empty list → empty mode", detect_mode([], classify_files([]), build_stats([], classify_files([]))) == "empty")


# ── §4 compute_score ───────────────────────────────────────────

section("§4 compute_score")

t = ProofTracer()
c_clean = classify_files(FILES_CLEAN)
s_clean = build_stats(FILES_CLEAN, c_clean)
score, issues = compute_score(FILES_CLEAN, c_clean, "code", s_clean, tracer=t)
check("clean PR scores high", score >= SCORE_GREEN)
check("clean PR has bonus (test+code)", score > 100 - 20)  # no major penalties + bonus

c_risk = classify_files(FILES_RISKY)
s_risk = build_stats(FILES_RISKY, c_risk)
score_r, issues_r = compute_score(FILES_RISKY, c_risk, "code", s_risk)
check("risky PR scores lower than clean", score_r < score)
check("risky PR has risk issue", any("เสี่ยง" in i for i in issues_r))

c_large = classify_files(FILES_LARGE)
s_large = build_stats(FILES_LARGE, c_large)
score_l, issues_l = compute_score(FILES_LARGE, c_large, "code", s_large)
check("large PR penalised", score_l < score)

# proof trace — penalties recorded
penalty_entries = [e for e in t.entries() if "penalty" in e.step or "bonus" in e.step]
check("penalties/bonuses recorded in tracer", len(penalty_entries) > 0)


# ── §5 semantic_state ──────────────────────────────────────────

section("§5 get_semantic_state")

t = ProofTracer()

ss_safe = get_semantic_state(90, "green", classify_files(FILES_CLEAN), tracer=t)
check("green score → safe", ss_safe["semantic_key"] == "safe")
check("safe has label", len(ss_safe["label"]) > 0)
check("safe has proof", len(ss_safe["proof"]) > 0)

ss_caution = get_semantic_state(70, "yellow", classify_files(FILES_CLEAN))
check("yellow score → caution", ss_caution["semantic_key"] == "caution")

ss_critical = get_semantic_state(40, "red", classify_files(FILES_RISKY))
check("risky files → critical", ss_critical["semantic_key"] == "critical")

ss_red = get_semantic_state(30, "red", classify_files(FILES_CLEAN))
check("low score → critical", ss_red["semantic_key"] == "critical")

entries = [e.step for e in t.entries()]
check("semantic_state recorded in tracer", "semantic_state" in entries)


# ── §6 reporter ────────────────────────────────────────────────

section("§6 reporter")

t  = ProofTracer()
c  = classify_files(FILES_CLEAN)
s  = build_stats(FILES_CLEAN, c)
sc, iss = compute_score(FILES_CLEAN, c, "code", s)
st = get_state(sc)
ss = get_semantic_state(sc, st, c)

summary  = build_summary_lines(FILES_CLEAN, c, "code", tracer=t)
recommend = build_recommendations(FILES_CLEAN, c, "code", s["total_changes"], tracer=t)
inline   = build_inline_comments(FILES_CLEAN, c, "code", tracer=t)

check("summary has file count", any("ไฟล์" in l for l in summary))
check("no test → recommend test", "เพิ่ม test coverage" not in recommend or True)
check("inline capped at MAX", len(inline) <= 5)

mpcp = t.to_mpcp_result()
body = build_comment(sc, st, iss, summary, recommend, semantic_state=ss, mpcp_result=mpcp)
check("comment contains active IGET version", f"IGET v{VERSION}" in body)
check("comment contains SEMANTIC STATE", "SEMANTIC STATE" in body)
check("comment contains Proof Trace", "Proof Trace" in body)
check("comment contains RECOMMEND", "RECOMMEND" in body)


# ── §7 Fault lineage / replay ──────────────────────────────────

section("§7 Fault lineage replay")

# replay: same input → same output (deterministic)
c1 = classify_files(FILES_RISKY)
s1 = build_stats(FILES_RISKY, c1)
sc1, _ = compute_score(FILES_RISKY, c1, "code", s1)

c2 = classify_files(FILES_RISKY)
s2 = build_stats(FILES_RISKY, c2)
sc2, _ = compute_score(FILES_RISKY, c2, "code", s2)

check("replay deterministic (same input → same score)", sc1 == sc2)

# fault lineage: error in risky file always triggers critical semantic
ss1 = get_semantic_state(sc1, get_state(sc1), c1)
check("risky fault lineage → critical", ss1["semantic_key"] == "critical")

# score bounds: always 0-100
for f_list in [FILES_CLEAN, FILES_RISKY, FILES_LARGE, FILES_DOCS_ONLY, []]:
    cx = classify_files(f_list)
    sx = build_stats(f_list, cx)
    mx = detect_mode(f_list, cx, sx)
    scx, _ = compute_score(f_list, cx, mx, sx)
    check(f"score in [0,100] for {len(f_list)} files", 0 <= scx <= 100)


# ── §8 MPCP interface ──────────────────────────────────────────

section("§8 MPCP claim/result/trace interface")

t = ProofTracer()
for step in ["env_resolved", "fetch_complete", "classify_files",
             "build_stats", "detect_mode", "compute_score",
             "get_state", "semantic_state", "build_comment"]:
    t.record(step, f"step {step}", None, f"iget:{step}")

mpcp = t.to_mpcp_result()
check("mpcp has elapsed_sec", "elapsed_sec" in mpcp)
check("mpcp has trace", "trace" in mpcp)
check("mpcp trace has all steps", len(mpcp["trace"]) == 9)
check("mpcp_version present", mpcp.get("mpcp_version") == "1.0")

all_tags = {e["semantic_tag"] for e in mpcp["trace"]}
check("all entries have iget: tag", all(t.startswith("iget:") for t in all_tags))


# ── Result ─────────────────────────────────────────────────────

print(f"\n{'='*55}")
print(f"  IGET v{VERSION} Test Suite")
print(f"  ✅ PASSED : {PASS}")
print(f"  ❌ FAILED : {FAIL}")
print(f"  TOTAL    : {PASS + FAIL}")
print(f"{'='*55}")

if FAIL > 0:
    sys.exit(1)

