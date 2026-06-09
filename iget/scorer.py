# ==========================================
# IGET v9 — Scoring Engine
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

        if not low.endswith(DOC_EXT) and not is_test and any(word in low for word in RISK_WORDS):
            risky_files.append(f)

    return {
        "code": code_files,
        "doc": doc_files,
        "test": test_files,
        "risky": risky_files,
        "config": config_files,
        "workflow": workflow_files,
    }


def build_stats(files, classified):
    """Pre-compute commonly used numeric stats in one place."""
    return {
        "total_files": len(files),
        "total_changes": sum(f.get("changes", 0) for f in files),
        "doc_count": len(classified["doc"]),
        "test_count": len(classified["test"]),
        "code_count": len(classified["code"]),
        "risky_count": len(classified["risky"]),
        "workflow_count": len(classified["workflow"]),
    }


def detect_mode(files, classified, stats=None):
    """
    Detect the primary nature of the PR.
    Returns a string: 'docs_only', 'test_only', 'mixed', 'code'
    """
    stats = stats or build_stats(files, classified)
    total = stats["total_files"]

    if total == 0:
        return "empty"

    if stats["doc_count"] == total:
        return "docs_only"

    if stats["test_count"] > 0 and stats["code_count"] == stats["test_count"]:
        return "test_only"

    if stats["doc_count"] > 0 and stats["code_count"] > 0:
        return "mixed"

    return "code"


def compute_score(files, classified, mode, stats=None):
    """
    Compute a 0-100 PR health score with improved accuracy and fewer false positives.
    Returns (score, issues) tuple.
    """
    stats = stats or build_stats(files, classified)
    total_files = stats["total_files"]
    total_changes = stats["total_changes"]
    code_count = stats["code_count"]
    test_count = stats["test_count"]

    score = 100
    issues = []

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

    has_meaningful_code = code_count > 0 and mode not in ("docs_only", "test_only")
    if has_meaningful_code and test_count == 0:
        score -= min(20, 5 * code_count)
        issues.append("🟡 มี code change แต่ไม่มี test")

    if stats["risky_count"] > 0:
        score -= 30
        issues.append("🔴 พบไฟล์เสี่ยง")

    if stats["workflow_count"] > 0:
        score -= 10
        issues.append("🟡 มีการเปลี่ยน workflow files")

    if mode == "docs_only":
        issues.append("🔵 Documentation PR")
        score += 5

    if total_files <= 3 and total_changes <= 100:
        score += 5

    if test_count > 0 and code_count > 0:
        score += 5

    return max(0, min(100, score)), issues


def get_state(score):
    """Map numeric score to traffic-light state."""
    if score >= SCORE_GREEN:
        return "green"
    if score >= SCORE_YELLOW:
        return "yellow"
    return "red"
