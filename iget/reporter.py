# ==========================================
# IGET v9 — Reporter
# ==========================================

from .config import COMMENT_MARKER, MAX_INLINE_COMMENTS, VERSION, CODE_EXT


FLOW_ICONS = {
    "green": "🟩",
    "yellow": "🟨",
    "red": "🟥"
}

IMPACT_TEXT = {
    "green": "🟢 ความเสี่ยงจากสัญญาณไฟล์ต่ำ; ให้ required checks และมนุษย์ตัดสิน merge",
    "yellow": "🟡 มีความเสี่ยงบางส่วน ควรตรวจเพิ่ม",
    "red": "🔴 เสี่ยงสูง ควร review ก่อน merge"
}


def build_flow(state):
    icon = FLOW_ICONS[state]
    return ["🟩", icon, icon, "🟩", icon, "🟩"]


def build_recommendations(files, classified, mode, total_changes):
    """Generate contextual recommendations, avoiding redundant noise."""
    recommend = []

    if mode == "docs_only":
        recommend.append("ตรวจเนื้อหา/คำสะกดก่อน merge")

    if (
        mode not in ("docs_only", "test_only")
        and len(classified["code"]) > 0
        and len(classified["test"]) == 0
    ):
        recommend.append("เพิ่ม test coverage")

    if total_changes > 400:
        recommend.append("ลดขนาด PR")

    if len(files) > 12:
        recommend.append("แยก PR เป็นงานย่อย")

    if len(classified["risky"]) > 0:
        recommend.append("ตรวจไฟล์เสี่ยงทันที")

    if len(classified["workflow"]) > 0:
        recommend.append("ตรวจ workflow changes ก่อน merge")

    if not recommend:
        recommend.append("ไม่พบข้อเสนอเพิ่มจาก IGET; ให้ required checks และมนุษย์ตัดสิน merge")

    return recommend


def build_summary_lines(files, classified, mode):
    """Build the summary section lines."""
    total_files = len(files)
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

    if mode == "docs_only":
        lines.append("- โหมด: Documentation Only")
    elif mode == "test_only":
        lines.append("- โหมด: Tests Only")

    return lines


def build_inline_comments(files, classified, mode):
    """Generate targeted inline comments, anti-spam capped."""
    comments = []

    for f in files:
        name = f["filename"]
        changes = f.get("changes", 0)
        low = name.lower()

        if changes > 250:
            comments.append({
                "path": name,
                "line": 1,
                "body": "🔴 ไฟล์นี้แก้ไขจำนวนมาก ควรตรวจละเอียด"
            })

        if (
            mode not in ("docs_only", "test_only")
            and low.endswith(CODE_EXT)
            and "test" not in low
            and len(classified["test"]) == 0
        ):
            comments.append({
                "path": name,
                "line": 1,
                "body": "🟡 พิจารณาเพิ่ม test สำหรับส่วนนี้"
            })

    return comments[:MAX_INLINE_COMMENTS]


def build_comment(score, state, issues, summary_lines, recommend):
    """Assemble the full PR comment body."""
    flow = build_flow(state)
    impact = IMPACT_TEXT[state]

    body = f"{COMMENT_MARKER}\n## 🔍 IGET v{VERSION}\n\n"

    body += "### FLOW\n"
    body += "".join(flow) + f" ({score}%)\n\n"

    body += "### SUMMARY\n"
    body += "\n".join(summary_lines) + "\n"

    body += "\n### RISK\n"
    if issues:
        for i in issues:
            body += f"- {i}\n"
    else:
        body += "- 🟢 ไม่พบความเสี่ยงเด่นชัด\n"

    body += "\n### IMPACT\n"
    body += impact + "\n"

    body += "\n### RECOMMEND\n"
    for r in recommend:
        body += f"- {r}\n"

    body += "\n---\n"
    body += f"_Powered by W3 IGET Governance Engine v{VERSION}_"

    return body
