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

# ── ฟังก์ชันหลัก ────────────────────────────────────────
def create_task(name: str, desc: str, agent: str = "Copilot-Gm", module: str = "W3Lgu"):
    """สร้าง Task ใหม่และบันทึกลงคิว"""
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

    # บันทึกลง task_queue.json
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


# ── Dispatch ─────────────────────────────────────────────
def dispatch_to_agent(name: str, desc: str, agent: str):
    """ส่งคำสั่งไปยังเอเจนท์ที่เลือก"""
    print(f"[TaskAgent] 🚀 ส่งคำสั่งไปยัง {agent} …")

    try:
        if agent == "Gemini":
            return gemini.process_task(name, desc)
        elif agent == "Copilot-Gm":
            return copilot_gm.orchestrate(name, desc)
        elif agent == "Grok":
            return grok.analyze(name, desc)
        elif agent == "BBX19":
            return bbx19.integrate(name, desc)
        elif agent == "DeepSeek":
            return deepseek.evaluate(name, desc)
        else:
            return f"⚠️ Agent '{agent}' ไม่พบในระบบ"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดใน {agent}: {e}"


# ── ตัวอย่างการใช้งาน ───────────────────────────────────
if __name__ == "__main__":
    task = create_task("ทดสอบระบบ", "ลองส่ง task ผ่าน TaskAgent", agent="Gemini")
    result = dispatch_to_agent(task["name"], task["desc"], task["agent"])
    print(f"[TaskAgent] ผลลัพธ์จาก {task['agent']}: {result}")
