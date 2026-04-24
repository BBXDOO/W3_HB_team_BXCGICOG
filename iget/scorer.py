# ==========================================
# IGET v5 — Scoring Engine
# ==========================================

from .config import (
    CODE_EXT, DOC_EXT, CONFIG_EXT, RISK_WORDS,
    FILES_WARN, FILES_LARGE, CHANGES_WARN, CHANGES_LARGE,
    SCORE_GREEN, SCORE_YELLOW,
)


def classify_files(files):
    """
    Classify PR files into categories.
    Returns a dict with keys: code, doc, test, risky, config, workflow.
    """
    code_files = []
    doc_files = []
    test_files = []
    risky_files = []
    config_files = []
    workflow_files = []

    for f in files:
        name = f["filename"]
        low = name.lower()

        if low.endswith(CODE_EXT):
            code_files.append(f)

        if low.endswith(DOC_EXT):
            doc_files.append(f)

        if low.endswith(CONFIG_EXT):
            config_files.append(f)

        # Test detection: file or directory named test/spec/tests/__tests__
        if (
            "test" in low
            or "spec" in low
            or low.endswith("_test.py")
            or low.endswith("_test.go")
            or "/__tests__/" in low
        ):
            test_files.append(f)

        # Workflow files
        if ".github/workflows/" in low or ".github/actions/" in low:
            workflow_files.append(f)

        # Risk detection: only non-test, non-doc files
        if not low.endswith(DOC_EXT):
            if any(word in low for word in RISK_WORDS):
                risky_files.append(f)

    return {
        "code": code_files,
        "doc": doc_files,
        "test": test_files,
        "risky": risky_files,
        "config": config_files,
        "workflow": workflow_files,
    }


def detect_mode(files, classified):
    """
    Detect the primary nature of the PR.
    Returns a string: 'docs_only', 'test_only', 'mixed', 'code'
    """
    total = len(files)
    if total == 0:
        return "empty"

    doc_count = len(classified["doc"])
    test_count = len(classified["test"])
    code_count = len(classified["code"])

    if doc_count == total:
        return "docs_only"

    if test_count > 0 and code_count == test_count:
        return "test_only"

    if doc_count > 0 and code_count > 0:
        return "mixed"

    return "code"


def compute_score(files, classified, mode):
    """
    Compute a 0-100 PR health score with improved accuracy and fewer false positives.
    Returns (score, issues) tuple.
    """
    total_files = len(files)
    total_changes = sum(f.get("changes", 0) for f in files)
    score = 100
    issues = []

    # ── SIZE SCORING ──────────────────────────────────────────────
    # Use proportional thresholds to reduce false positives on borderline PRs
    if total_files > FILES_LARGE:
        score -= 15
        issues.append("🔴 PR ใหญ่เกินควร")
    elif total_files > FILES_WARN:
        score -= 8
        issues.append("🟡 เปลี่ยนหลายไฟล์")

    if total_changes > CHANGES_LARGE:
        score -= 20
        issues.append("🔴 เปลี่ยนหนักมาก")
    elif total_changes > CHANGES_WARN:
        score -= 12
        issues.append("🔴 แก้ไขจำนวนมาก")

    # ── CODE WITHOUT TESTS ────────────────────────────────────────
    # Only penalise when there are non-trivial code changes and zero tests
    has_meaningful_code = (
        len(classified["code"]) > 0
        and mode not in ("docs_only", "test_only")
    )
    if has_meaningful_code and len(classified["test"]) == 0:
        # Penalty scales with number of changed code files (capped)
        penalty = min(20, 5 * len(classified["code"]))
        score -= penalty
        issues.append("🟡 มี code change แต่ไม่มี test")

    # ── RISKY FILES ───────────────────────────────────────────────
    if len(classified["risky"]) > 0:
        score -= 30
        issues.append("🔴 พบไฟล์เสี่ยง")

    # ── WORKFLOW FILE CHANGES ─────────────────────────────────────
    if len(classified["workflow"]) > 0:
        score -= 10
        issues.append("🟡 มีการเปลี่ยน workflow files")

    # ── BONUSES ───────────────────────────────────────────────────
    if mode == "docs_only":
        issues.append("🔵 Documentation PR")
        score += 5

    # Small-PR safety bonus: few files, few changes
    if total_files <= 3 and total_changes <= 100:
        score += 5

    # Test coverage bonus
    if len(classified["test"]) > 0 and len(classified["code"]) > 0:
        score += 5

    # ── CLAMP ────────────────────────────────────────────────────
    score = max(0, min(100, score))

    return score, issues


def get_state(score):
    """Map numeric score to traffic-light state."""
    if score >= SCORE_GREEN:
        return "green"
    if score >= SCORE_YELLOW:
        return "yellow"
    return "red"
