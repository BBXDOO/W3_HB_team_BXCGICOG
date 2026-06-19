# ─────────────────────────────────────────────────────────────────
# PATCH: ต่อ execution_worker เข้า auto_responder
# วิธีวาง: เพิ่มโค้ดด้านล่างนี้เข้า modules/W3Agent/tools/auto_responder.py
# ไม่ต้องแก้ของเดิม — แค่ "เพิ่ม" import + handler + แก้ main 3 บรรทัด
# ─────────────────────────────────────────────────────────────────


# ── (1) เพิ่มที่ส่วน import ด้านบน (ใกล้ approval_gate) ──

from approval_gate import (
    build_approval_response,
    is_approval_comment,
    parse_approval_command,          # ← เพิ่ม
    resolve_approval_state,          # ← เพิ่ม
    build_execution_plan,            # ← เพิ่ม
    extract_module_tags as gate_extract_module_tags,  # ← เพิ่ม (กันชื่อชน)
)
from execution_worker import run_worker, render_worker_comment   # ← เพิ่ม


# ── (2) เพิ่ม handler ใหม่ (วางถัดจาก handle_approval_comment) ──

def handle_execution_worker(info, repo):
    """หลัง BBX19 อนุมัติแล้ว → ให้ worker ร่าง patch จริง

    ทำงานต่อจาก handle_approval_comment:
      - อ่านคำสั่งอนุมัติซ้ำ เพื่อดู state
      - ถ้า approved → เรียก run_worker() ร่าง patch
      - คอมเมนต์สรุปกลับ issue
      - worker เขียนไฟล์ลง worker_output/ ให้ BBX19 วางเอง

    Boundary: worker ไม่ commit ไม่ push — BBX19 คือคนวาง
    """
    command = parse_approval_command(info.get("comment_body", ""))
    if command is None:
        print("[auto_responder] worker: no approval command; skip")
        return

    status, next_mode = resolve_approval_state(command.action)

    # ทำงานเฉพาะตอน approve/run เท่านั้น
    if next_mode != "prepare_execution_plan":
        print(f"[auto_responder] worker: state '{status}' not executable; skip")
        return

    modules = gate_extract_module_tags(info["body"])
    plan = build_execution_plan(info["title"], info["body"], modules)

    result = run_worker(
        issue_number=info["number"],
        issue_title=info["title"],
        issue_body=info["body"],
        approval_status=status,
        plan=plan,
        output_dir="worker_output",
        write_files=True,
    )

    comment_issue(repo, info["number"], render_worker_comment(result))
    print(
        f"[auto_responder] worker: status={result.status} "
        f"drafts={len(result.drafts)} on #{info['number']}"
    )


# ── (3) แก้ main() — ในบล็อก issue_comment ──
#
#    หาโค้ดเดิมนี้:
#
#        if is_approval_comment(info.get("comment_body")):
#            handle_approval_comment(info, repo)
#            return
#
#    แทนด้วย:
#
#        if is_approval_comment(info.get("comment_body")):
#            handle_approval_comment(info, repo)     # 1) ตอบ approval gate ก่อน
#            handle_execution_worker(info, repo)     # 2) แล้วให้ worker ร่าง patch
#            return
#
# ─────────────────────────────────────────────────────────────────
# เท่านี้ flow ก็ครบ:
#
#   /iget approve
#     → handle_approval_comment  (ยืนยันอนุมัติ + execution plan)
#     → handle_execution_worker  (ร่าง patch จริงลง worker_output/)
#     → BBX19 เปิด worker_output/ ดู patch แล้ววางผ่าน Termux
#
# ไม่มี AI commit เอง — BBX19 คือคนกดวางทุกครั้ง
# ─────────────────────────────────────────────────────────────────

