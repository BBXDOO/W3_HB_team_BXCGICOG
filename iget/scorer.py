# ==========================================
# IGET v8.0 — Scoring Engine
# Semantic state + causal proof annotation
# Ontology tag: iget:module = "scorer"
# ==========================================

from __future__ import annotations

from .config import (
    CODE_EXT, CONFIG_EXT, DOC_EXT, RISK_WORDS,
    FILES_WARN, FILES_LARGE,
    CHANGES_WARN, CHANGES_LARGE,
    SCORE_GREEN, SCORE_YELLOW,
    SEMANTIC_STATES,
)
from .proof import ProofTracer


# ── File classification ────────────────────────────────────────

def classify_files(
    files:  list[dict],
    tracer: ProofTracer | None = None,
) -> dict:
    """
    Classify PR files into semantic categories.

    Returns dict: code, doc, test, risky, config, workflow.
    Ontology tag: iget:classify_files
    """
    tracer = tracer or ProofTracer(enabled=False)

    code_files = doc_files = test_files = []
    risky_files = config_files = workflow_files = []
    code_files, doc_files, test_files = [], [], []
    risky_files, config_files, workflow_files = [], [], []

    for f in files:
        name = f["filename"]
        low  = name.lower()

        is_test = (
            "test" in low
            or "spec" in low
            or low.endswith("_test.py")
            or low.endswith("_test.go")
            or "/__tests__/" in low
        )

        if is_test:
            test_files.append(f)

        if not is_test and low.endswith(CODE_EXT):
            code_files.append(f)

        if low.endswith(DOC_EXT):
            doc_files.append(f)

        if low.endswith(CONFIG_EXT):
            config_files.append(f)

        if ".github/workflows/" in low or ".github/actions/" in low:
            workflow_files.append(f)

        if (
            not low.endswith(DOC_EXT)
            and not is_test
            and any(word in low for word in RISK_WORDS)
        ):
            risky_files.append(f)

    result = {
        "code":     code_files,
        "doc":      doc_files,
        "test":     test_files,
        "risky":    risky_files,
        "config":   config_files,
        "workflow": workflow_files,
    }

    tracer.record(
        "classify_files",
        f"code={len(code_files)} doc={len(doc_files)} "
        f"test={len(test_files)} risky={len(risky_files)}",
        {k: len(v) for k, v in result.items()},
        "iget:classify_files",
    )
    return result


# ── Stats ──────────────────────────────────────────────────────

def build_stats(
    files:      list[dict],
    classified: dict,
    tracer:     ProofTracer | None = None,
) -> dict:
    """
    Pre-compute numeric stats in one place.
    Ontology tag: iget:build_stats
    """
    tracer = tracer or ProofTracer(enabled=False)
    stats = {
        "total_files":   len(files),
        "total_changes": sum(f.get("changes", 0) for f in files),
        "doc_count":     len(classified["doc"]),
        "test_count":    len(classified["test"]),
        "code_count":    len(classified["code"]),
        "risky_count":   len(classified["risky"]),
        "workflow_count":len(classified["workflow"]),
    }
    tracer.record(
        "build_stats",
        f"total_files={stats['total_files']} changes={stats['total_changes']}",
        stats,
        "iget:build_stats",
    )
    return stats


# ── Mode detection ─────────────────────────────────────────────

def detect_mode(
    files:      list[dict],
    classified: dict,
    stats:      dict | None = None,
    tracer:     ProofTracer | None = None,
) -> str:
    """
    Detect the primary nature of the PR.
    Returns: 'empty', 'docs_only', 'test_only', 'mixed', 'code'
    Ontology tag: iget:detect_mode
    """
    tracer = tracer or ProofTracer(enabled=False)
    stats  = stats or build_stats(files, classified)
    total  = stats["total_files"]

    if total == 0:
        mode = "empty"
    elif stats["doc_count"] == total:
        mode = "docs_only"
    elif stats["test_count"] > 0 and stats["code_count"] == stats["test_count"]:
        mode = "test_only"
    elif stats["doc_count"] > 0 and stats["code_count"] > 0:
        mode = "mixed"
    else:
        mode = "code"

    tracer.record(
        "detect_mode",
        f"PR mode = {mode}",
        {"mode": mode, "total_files": total},
        "iget:detect_mode",
    )
    return mode


# ── Scoring ────────────────────────────────────────────────────

def compute_score(
    files:      list[dict],
    classified: dict,
    mode:       str,
    stats:      dict | None = None,
    tracer:     ProofTracer | None = None,
) -> tuple[int, list[str]]:
    """
    Compute 0-100 PR health score with causal proof annotation.

    Each deduction is recorded as a proof entry so reviewers can
    trace exactly why a score changed.
    Ontology tag: iget:compute_score
    """
    tracer = tracer or ProofTracer(enabled=False)
    stats  = stats or build_stats(files, classified)

    total_files   = stats["total_files"]
    total_changes = stats["total_changes"]
    code_count    = stats["code_count"]
    test_count    = stats["test_count"]

    score  = 100
    issues: list[str] = []

    # — file count penalty —
    if total_files > FILES_LARGE:
        score -= 15
        issues.append("🔴 PR ใหญ่เกินควร")
        tracer.record("score_penalty", "-15 ไฟล์เกิน FILES_LARGE",
                      {"total_files": total_files}, "iget:score_penalty")
    elif total_files > FILES_WARN:
        score -= 8
        issues.append("🟡 เปลี่ยนหลายไฟล์")
        tracer.record("score_penalty", "-8 ไฟล์เกิน FILES_WARN",
                      {"total_files": total_files}, "iget:score_penalty")

    # — change size penalty —
    if total_changes > CHANGES_LARGE:
        score -= 20
        issues.append("🔴 เปลี่ยนหนักมาก")
        tracer.record("score_penalty", "-20 changes เกิน CHANGES_LARGE",
                      {"total_changes": total_changes}, "iget:score_penalty")
    elif total_changes > CHANGES_WARN:
        score -= 12
        issues.append("🔴 แก้ไขจำนวนมาก")
        tracer.record("score_penalty", "-12 changes เกิน CHANGES_WARN",
                      {"total_changes": total_changes}, "iget:score_penalty")

    # — missing test penalty —
    has_meaningful_code = code_count > 0 and mode not in ("docs_only", "test_only")
    if has_meaningful_code and test_count == 0:
        penalty = min(20, 5 * code_count)
        score  -= penalty
        issues.append("🟡 มี code change แต่ไม่มี test")
        tracer.record("score_penalty", f"-{penalty} ไม่มี test",
                      {"code_count": code_count}, "iget:score_penalty")

    # — risk penalty —
    if stats["risky_count"] > 0:
        score -= 30
        issues.append("🔴 พบไฟล์เสี่ยง")
        tracer.record("score_penalty", "-30 risky files",
                      {"risky_count": stats["risky_count"]}, "iget:score_risk")

    # — workflow penalty —
    if stats["workflow_count"] > 0:
        score -= 10
        issues.append("🟡 มีการเปลี่ยน workflow files")
        tracer.record("score_penalty", "-10 workflow changed",
                      {"workflow_count": stats["workflow_count"]}, "iget:score_penalty")

    # — bonus: docs-only —
    if mode == "docs_only":
        issues.append("🔵 Documentation PR")
        score += 5
        tracer.record("score_bonus", "+5 docs-only PR", None, "iget:score_bonus")

    # — bonus: small clean PR —
    if total_files <= 3 and total_changes <= 100:
        score += 5
        tracer.record("score_bonus", "+5 small clean PR", None, "iget:score_bonus")

    # — bonus: code+test present —
    if test_count > 0 and code_count > 0:
        score += 5
        tracer.record("score_bonus", "+5 code+test present", None, "iget:score_bonus")

    final = max(0, min(100, score))
    tracer.record(
        "compute_score",
        f"final score = {final}",
        {"score": final, "issues": issues},
        "iget:compute_score",
    )
    return final, issues


# ── State mapping ──────────────────────────────────────────────

def get_state(
    score:  int,
    tracer: ProofTracer | None = None,
) -> str:
    """
    Map numeric score → traffic-light state.
    Ontology tag: iget:get_state
    """
    tracer = tracer or ProofTracer(enabled=False)

    if score >= SCORE_GREEN:
        state = "green"
    elif score >= SCORE_YELLOW:
        state = "yellow"
    else:
        state = "red"

    tracer.record(
        "get_state",
        f"score={score} → state={state}",
        {"score": score, "state": state},
        "iget:get_state",
    )
    return state


# ── Semantic state annotation (v8) ────────────────────────

def get_semantic_state(
    score:      int,
    state:      str,
    classified: dict,
    tracer:     ProofTracer | None = None,
) -> dict:
    """
    Derive semantic meaning of the PR beyond the numeric score.

    Returns a dict with:
      - semantic_key: one of SEMANTIC_STATES keys
      - label:        human-readable Thai description
      - proof:        reasons for this semantic classification

    Ontology tag: iget:semantic_state
    """
    tracer = tracer or ProofTracer(enabled=False)
    proof  = []

    if classified["risky"]:
        semantic_key = "critical"
        proof.append("พบไฟล์ที่มี pattern ความเสี่ยงสูง")
    elif state == "red":
        semantic_key = "critical"
        proof.append(f"คะแนนต่ำกว่าเกณฑ์ (score={score})")
    elif state == "yellow":
        semantic_key = "caution"
        proof.append(f"คะแนนอยู่ในโซนระวัง (score={score})")
    elif state == "green":
        semantic_key = "safe"
        proof.append(f"คะแนนผ่านเกณฑ์ (score={score})")
    else:
        semantic_key = "unknown"
        proof.append("ไม่สามารถจำแนกได้")

    label = SEMANTIC_STATES.get(semantic_key, "")

    result = {
        "semantic_key": semantic_key,
        "label":        label,
        "proof":        proof,
    }

    tracer.record(
        "semantic_state",
        f"semantic={semantic_key}: {label}",
        result,
        "iget:semantic_state",
    )
    return result
