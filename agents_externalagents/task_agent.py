# agents_externalagen/task_agent.py
import uuid
import datetime
import json
from pathlib import Path

# ── Paths ───────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
TASK_QUEUE = REPO_ROOT / "core" / "memory" / "task_queue.json"

# ── Runtime Agents ───────────────────────────────────────
from core.runtime.agents import gemini, copilot_gm, grok, bbx19, deepseek

# ── ฟังก์ชันสร้าง Task ─────────────────────────────────
def create_task(name: str, desc: str, agent: str = "Copilot-Gm", module: str = "W3Lgu"):
    task_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.now().isoformat()

    task = {
        "task_id": task_id,
        "name": name,
        "desc": desc,
        "agent": agent,
        "module": module,
        "timestamp": timestamp,
        "status": "queued"
    }

    save_to_queue(task)
    print(f"[TaskAgent] ✅ สร้าง Task แล้ว: {task_id}")
    return task


def save_to_queue(task: dict):
    """บันทึก task ลงไฟล์คิว"""
    queue = []
    if TASK_QUEUE.exists():
        try:
            queue = json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            queue = []
    queue.append(task)
    TASK_QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")


# ── ฟังก์ชันอัปเดตสถานะ ────────────────────────────────
def update_task_status(task_id: str, status: str):
    """อัปเดตสถานะของ task ในคิว"""
    if not TASK_QUEUE.exists():
        return f"⚠️ ไม่มี task_queue.json"

    queue = json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
    for task in queue:
        if task["task_id"] == task_id:
            task["status"] = status
            TASK_QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
            return f"[TaskAgent] 🔄 อัปเดต Task {task_id} → {status}"
    return f"⚠️ Task {task_id} ไม่พบในคิว"


# ── Dispatch ─────────────────────────────────────────────
def dispatch_to_agent(name: str, desc: str, agent: str, task_id: str = None):
    """ส่งคำสั่งไปยังเอเจนท์ที่เลือก พร้อมอัปเดตสถานะ"""
    if task_id:
        update_task_status(task_id, "running")

    print(f"[TaskAgent] 🚀 ส่งคำสั่งไปยัง {agent} …")
    try:
        if agent == "Gemini":
            result = gemini.process_task(name, desc)
        elif agent == "Copilot-Gm":
            result = copilot_gm.orchestrate(name, desc)
        elif agent == "Grok":
            result = grok.analyze(name, desc)
        elif agent == "BBX19":
            result = bbx19.integrate(name, desc)
        elif agent == "DeepSeek":
            result = deepseek.evaluate(name, desc)
        else:
            result = f"⚠️ Agent '{agent}' ไม่พบในระบบ"

        if task_id:
            update_task_status(task_id, "done")
        return result

    except Exception as e:
        if task_id:
            update_task_status(task_id, "failed")
        return f"❌ เกิดข้อผิดพลาดใน {agent}: {e}"


# ── ฟังก์ชันแสดงรายการ Task ────────────────────────────
def list_tasks():
    """ดึงรายการ task ทั้งหมดจากคิวและแสดงสถานะ"""
    if not TASK_QUEUE.exists():
        return "⚠️ ไม่มี task_queue.json"

    try:
        queue = json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "⚠️ task_queue.json ไม่สามารถอ่านได้"

    if not queue:
        return "ℹ️ ไม่มี task ในคิว"

    # สร้างตารางสรุป
    lines = []
    lines.append("| Task ID  | Agent       | Name                | Status   | Timestamp           |")
    lines.append("|----------|-------------|---------------------|----------|---------------------|")
    for task in queue:
        lines.append(
            f"| {task['task_id']} | {task['agent']:<11} | {task['name']:<19} | {task['status']:<8} | {task['timestamp']} |"
        )

    return "\n".join(lines)


# ── ฟังก์ชัน Filter Task ────────────────────────────────
def filter_tasks(status: str):
    """ดึงเฉพาะ task ที่มีสถานะตรงกับที่กำหนด"""
    if not TASK_QUEUE.exists():
        return "⚠️ ไม่มี task_queue.json"

    try:
        queue = json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "⚠️ task_queue.json ไม่สามารถอ่านได้"

    filtered = [t for t in queue if t["status"] == status]
    if not filtered:
        return f"ℹ️ ไม่มี task ที่สถานะ = {status}"

    lines = []
    lines.append(f"📋 Task ที่สถานะ = {status}")
    lines.append("| Task ID  | Agent       | Name                | Timestamp           |")
    lines.append("|----------|-------------|---------------------|---------------------|")
    for task in filtered:
        lines.append(
            f"| {task['task_id']} | {task['agent']:<11} | {task['name']:<19} | {task['timestamp']} |"
        )

    return "\n".join(lines)


# ── ตัวอย่างการใช้งาน ───────────────────────────────────
if __name__ == "__main__":
    # สร้าง task ใหม่
    task = create_task("ทดสอบระบบ", "ลองส่ง task ผ่าน TaskAgent", agent="Gemini")
    result = dispatch_to_agent(task["name"], task["desc"], task["agent"], task["task_id"])
    print(f"[TaskAgent] ผลลัพธ์จาก {task['agent']}: {result}")

    # แสดงรายการ task ทั้งหมด
    print("\n[TaskAgent] 📋 รายการ Task ปัจจุบัน:")
    print(list_tasks())

    # แสดงเฉพาะ task ที่สถานะ = done
    print("\n[TaskAgent] 📋 Task ที่เสร็จแล้ว:")
    print(filter_tasks("done"))
