# agents_externalagents/task_agent.py
import uuid
import datetime
import json
from pathlib import Path

# ── Paths ───────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
TASK_QUEUE = REPO_ROOT / "core" / "memory" / "task_queue.json"

# ── Runtime Agents ───────────────────────────────────────
try:
    from core.runtime.agents import gemini, copilot_gm, grok, bbx19, deepseek
except ImportError:
    # mock agents (ใช้งานภายนอก ให้ comment ส่วนนี้ออกเมื่อใช้จริง)
    class MockAgent:
        def process_task(self, name, desc): return f"[Gemini] {name} :: {desc}"
        def orchestrate(self, name, desc): return f"[Copilot-Gm] {name} :: {desc}"
        def analyze(self, name, desc): return f"[Grok] {name} :: {desc}"
        def integrate(self, name, desc): return f"[BBX19] {name} :: {desc}"
        def evaluate(self, name, desc): return f"[DeepSeek] {name} :: {desc}"
    gemini = MockAgent()
    copilot_gm = MockAgent()
    grok = MockAgent()
    bbx19 = MockAgent()
    deepseek = MockAgent()

# ── AGENT NAME MAPPING ──────────────────────────────────
AGENT_FUNCTIONS = {
    "gemini":      lambda name, desc: gemini.process_task(name, desc),
    "copilot-gm":  lambda name, desc: copilot_gm.orchestrate(name, desc),
    "grok":        lambda name, desc: grok.analyze(name, desc),
    "bbx19":       lambda name, desc: bbx19.integrate(name, desc),
    "deepseek":    lambda name, desc: deepseek.evaluate(name, desc),
}

# ── JSON utility ────────────────────────────────────────
def read_json_queue():
    """อ่าน task_queue.json แบบ robust"""
    if not TASK_QUEUE.exists():
        return []
    try:
        return json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def write_json_queue(queue):
    """เขียน task_queue.json"""
    TASK_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    TASK_QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

# ── ฟังก์ชันสร้าง Task ─────────────────────────────────
def create_task(name: str, desc: str, agent: str = "copilot-gm", module: str = "W3Lgu"):
    task_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.now().isoformat()
    agent_norm = str(agent).strip().lower()
    task = {
        "task_id": task_id,
        "name": name,
        "desc": desc,
        "agent": agent_norm,
        "module": module,
        "timestamp": timestamp,
        "status": "queued"
    }
    # Save to queue
    queue = read_json_queue()
    queue.append(task)
    write_json_queue(queue)
    print(f"[TaskAgent] ✅ สร้าง Task แล้ว: {task_id}")
    return task

# ── ฟังก์ชันอัปเดตสถานะ ────────────────────────────────
def update_task_status(task_id: str, status: str):
    """อัปเดตสถานะของ task ในคิว"""
    queue = read_json_queue()
    found = False
    for task in queue:
        if task["task_id"] == task_id:
            task["status"] = status
            found = True
            break
    if found:
        write_json_queue(queue)
        return f"[TaskAgent] 🔄 อัปเดต Task {task_id} → {status}"
    else:
        return f"⚠️ Task {task_id} ไม่พบในคิว"

# ── Dispatch ─────────────────────────────────────────────
def dispatch_to_agent(name: str, desc: str, agent: str, task_id: str = None):
    """ส่งคำสั่งไปยังเอเจนท์ที่เลือก พร้อมอัปเดตสถานะ"""
    agent_norm = str(agent).strip().lower()
    if task_id:
        update_task_status(task_id, "running")

    print(f"[TaskAgent] 🚀 ส่งคำสั่งไปยัง {agent} …")
    try:
        if agent_norm in AGENT_FUNCTIONS:
            result = AGENT_FUNCTIONS[agent_norm](name, desc)
            if task_id:
                update_task_status(task_id, "done")
            return result
        else:
            if task_id:
                update_task_status(task_id, "failed")
            return f"⚠️ Agent '{agent}' ไม่พบในระบบ"
    except Exception as e:
        if task_id:
            update_task_status(task_id, "failed")
        return f"❌ เกิดข้อผิดพลาดใน {agent}: {e}"

# ── ฟังก์ชันแสดงรายการ Task ────────────────────────────
def list_tasks():
    """ดึงรายการ task ทั้งหมดจากคิวและแสดงสถานะ"""
    queue = read_json_queue()
    if not queue:
        return "ℹ️ ไม่มี task ในคิว"

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
    queue = read_json_queue()
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
