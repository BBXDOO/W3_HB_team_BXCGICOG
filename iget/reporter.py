# ==========================================
# IGET v9 — Reporter
# Semantic output + proof-ready formatting
# Ontology tag: iget:module = "reporter"
# ==========================================

from __future__ import annotations

from .config import COMMENT_MARKER, CODE_EXT, MAX_INLINE_COMMENTS, VERSION
from .proof  import ProofTracer


FLOW_ICONS = {
    "green":  "🟩",
    "yellow": "🟨",
    "red":    "🟥",
}

IMPACT_TEXT = {
    "green":  "🟢 ความเสี่ยงจากสัญญาณไฟล์ต่ำ; ให้ required checks และมนุษย์ตัดสิน merge",
    "yellow": "🟡 มีความเสี่ยงบางส่วน ควรตรวจเพิ่ม",
    "red":    "🔴 เสี่ยงสูง ควร review ก่อน merge",
}


# ── Flow indicator ─────────────────────────────────────────────

def build_flow(state: str) -> list[str]:
    icon = FLOW_ICONS[state]
    return ["🟩", icon, icon, "🟩", icon, "🟩"]


# ── Recommendations ────────────────────────────────────────────

def build_recommendations(
    files:         list[dict],
    classified:    dict,
    mode:          str,
    total_changes: int,
    tracer:        ProofTracer | None = None,
) -> list[str]:
    """
    Generate contextual recommendations.
    Ontology tag: iget:build_recommendations
    """
    tracer  = tracer or ProofTracer(enabled=False)
    recommend: list[str] = []

    if mode == "docs_only":
        recommend.append("ตรวจเนื้อหา/คำสะกดก่อน merge")

    if (
        mode not in ("docs_only", "test_only")
        and classified["code"]
        and not classified["test"]
    ):
        recommend.append("เพิ่ม test coverage")

    if total_changes > 400:
        recommend.append("ลดขนาด PR")

    if len(files) > 12:
        recommend.append("แยก PR เป็นงานย่อย")

    if classified["risky"]:
        recommend.append("ตรวจไฟล์เสี่ยงทันที")

    if classified["workflow"]:
        recommend.append("ตรวจ workflow changes ก่อน merge")

    if not recommend:
        recommend.append("ไม่พบข้อเสนอเพิ่มจาก IGET; ให้ required checks และมนุษย์ตัดสิน merge")

    tracer.record(
        "build_recommendations",
        f"{len(recommend)} recommendations",
        recommend,
        "iget:build_recommendations",
    )
    return recommend


# ── Summary lines ──────────────────────────────────────────────

def build_summary_lines(
    files:      list[dict],
    classified: dict,
    mode:       str,
    tracer:     ProofTracer | None = None,
) -> list[str]:
    """
    Build the summary section lines.
    Ontology tag: iget:build_summary
    """
    tracer        = tracer or ProofTracer(enabled=False)
    total_files   = len(files)
    total_changes = sum(f.get("changes", 0) for f in files)

    lines = [
        f"- ไฟล์ที่เปลี่ยน: {total_files}",
        f"- บรรทัดที่เปลี่ยน: {total_changes}",
        f"- ไฟล์โค้ด: {len(classified['code'])}",
        f"- ไฟล์เอกสาร: {len(classified['doc'])}",
        f"- ไฟล์ทดสอบ: {len(classified['test'])}",
    ]

    if classified["workflow"]:
        lines.append(f"- ไฟล์ workflow: {len(classified['workflow'])}")

    mode_labels = {
        "docs_only": "Documentation Only",
        "test_only": "Tests Only",
        "mixed":     "Mixed (Code + Docs)",
        "empty":     "Empty PR",
    }
    if mode in mode_labels:
        lines.append(f"- โหมด: {mode_labels[mode]}")

    tracer.record(
        "build_summary",
        f"{total_files} files / {total_changes} changes / mode={mode}",
        None,
        "iget:build_summary",
    )
    return lines


# ── Inline comments ────────────────────────────────────────────

def build_inline_comments(
    files:      list[dict],
    classified: dict,
    mode:       str,
    tracer:     ProofTracer | None = None,
) -> list[dict]:
    """
    Generate targeted inline comments, anti-spam capped.
    Ontology tag: iget:build_inline_comments
    """
    tracer   = tracer or ProofTracer(enabled=False)
    comments: list[dict] = []

    for f in files:
        name    = f["filename"]
        changes = f.get("changes", 0)
        low     = name.lower()

        if changes > 250:
            comments.append({
                "path": name,
                "line": 1,
                "body": "🔴 ไฟล์นี้แก้ไขจำนวนมาก ควรตรวจละเอียด",
            })

        if (
            mode not in ("docs_only", "test_only")
            and low.endswith(CODE_EXT)
            and "test" not in low
            and not classified["test"]
        ):
            comments.append({
                "path": name,
                "line": 1,
                "body": "🟡 พิจารณาเพิ่ม test สำหรับส่วนนี้",
            })

    result = comments[:MAX_INLINE_COMMENTS]
    tracer.record(
        "build_inline_comments",
        f"{len(result)} inline comments",
        None,
        "iget:build_inline_comments",
    )
    return result


# ── Main comment body ──────────────────────────────────────────

def build_comment(
    score:          int,
    state:          str,
    issues:         list[str],
    summary_lines:  list[str],
    recommend:      list[str],
    semantic_state: dict | None = None,
    mpcp_result:    dict | None = None,
    tracer:         ProofTracer | None = None,
) -> str:
    """
    Assemble the full PR comment body.

    v9 carries forward the base-branch semantic contracts:
      - Semantic State section
      - Proof Trace summary (optional, collapsed)
      - MPCP result tag

    Ontology tag: iget:build_comment
    """
    tracer = tracer or ProofTracer(enabled=False)
    flow   = build_flow(state)
    impact = IMPACT_TEXT[state]

    body  = f"{COMMENT_MARKER}\n## 🔍 IGET v{VERSION}\n\n"

    # FLOW
    body += "### FLOW\n"
    body += "".join(flow) + f" ({score}%)\n\n"

    # SUMMARY
    body += "### SUMMARY\n"
    body += "\n".join(summary_lines) + "\n"

    # RISK
    body += "\n### RISK\n"
    if issues:
        for i in issues:
            body += f"- {i}\n"
    else:
        body += "- 🟢 ไม่พบความเสี่ยงเด่นชัด\n"

    # IMPACT
    body += "\n### IMPACT\n"
    body += impact + "\n"

    # SEMANTIC STATE (v8)
    if semantic_state:
        body += "\n### SEMANTIC STATE\n"
        body += f"- สถานะ: **{semantic_state['label']}**\n"
        for p in semantic_state.get("proof", []):
            body += f"  - {p}\n"

    # RECOMMEND
    body += "\n### RECOMMEND\n"
    for r in recommend:
        body += f"- {r}\n"

    # PROOF TRACE (v8 — collapsed section)
    if mpcp_result and mpcp_result.get("trace"):
        elapsed  = mpcp_result.get("elapsed_sec", 0)
        steps    = " → ".join(e["step"] for e in mpcp_result["trace"])
        body += "\n<details>\n"
        body += f"<summary>🔬 Proof Trace ({elapsed}s)</summary>\n\n"
        body += f"```\n{steps}\n```\n"
        body += "</details>\n"

    body += "\n---\n"
    body += f"_Powered by W3 IGET Governance Engine v{VERSION}_"

    tracer.record("build_comment", "comment body assembled", None, "iget:build_comment")
    return body
