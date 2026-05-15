ตัวอย่างนี้เป็น “เทมเพลต” สำหรับ CLI (cli.py) เพื่อเรียกใช้งาน agent ใน `core/runtime/agents` ตามจำนวนเอเจนท์, ชื่อเอเจนท์, เป้าหมาย หรือ parameter เพิ่มเติม (เขียนอธิบาย/รับค่าจากผู้ใช้เป็นภาษาไทย) รวมถึงส่วนสำคัญทั้งหมดตั้งแต่ import, ฟังก์ชัน ไปจนถึง main

**ตัวอย่างสมมติว่า มี agent หลายตัวใน core/runtime/agents (เช่น ChatGPTAgent, CastAgent ฯลฯ)  
และ func `run()` ของแต่ละ agent รับ task(plan/context)**

---

```python name=cli.py
import argparse

# นำเข้า agent ที่ใช้งาน
from core.runtime.agents.chatgpt import ChatGPTAgent
from core.runtime.agents.cast import CastAgent
# นำเข้า agent อื่นๆ เพิ่มเติมได้ เช่น
# from core.runtime.agents.gemini import GeminiAgent

# dictionary สำหรับ map ชื่อ agent ภาษาไทย => class
AGENT_CLASSES = {
    "chatgpt": ChatGPTAgent,
    "cast": CastAgent,
    # เพิ่มชื่อ-agent และ class ที่นี่
    # "gemini": GeminiAgent,
}

def สร้าง_เอเจนท์(agent_name):
    """คืนค่าอินสแตนซ์ agent จากชื่อ"""
    agent_name = agent_name.lower()
    if agent_name not in AGENT_CLASSES:
        raise ValueError(f"เอเจนท์ '{agent_name}' ไม่อยู่ในระบบ กรุณาระบุชื่อเอเจนท์ที่ถูกต้อง (มี: {', '.join(AGENT_CLASSES)})")
    return AGENT_CLASSES[agent_name]()

def เรียกใช้_เอเจนท์(agent_instance, ชื่องาน, เป้าหมาย, รายละเอียด, context=None):
    """เรียกใช้ run() ของ agent"""
    plan = {"role": "user", "responsibilities": [เป้าหมาย, รายละเอียด]}
    context = context or {}
    return agent_instance.run(ชื่องาน, plan, context)

def submit_agents(args):
    print(f"\n=== เรียกใช้จำนวนเอเจนท์ {args.num_agents} ตัว ===")
    agent_names = [a.strip() for a in args.agents.split(",") if a.strip()]
    if len(agent_names) != args.num_agents:
        print("จำนวนชื่อเอเจนท์ที่ระบุไม่ตรงกับจำนวนเอเจนท์ที่ต้องการ")
        return

    for agent_name in agent_names:
        try:
            agent = สร้าง_เอเจนท์(agent_name)
            print(f"\n[เอเจนท์: {agent_name}] กำลังดำเนินการ...")
            result = เรียกใช้_เอเจนท์(agent, args.name, args.target, args.desc)
            print("ผลลัพธ์:", result)
        except Exception as e:
            print(f"[{agent_name}] เกิดข้อผิดพลาด: {e}")

def main():
    parser = argparse.ArgumentParser(description="Task CLI สำหรับเรียกใช้เอเจนท์ (ภาษาไทย)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ==== คำสั่ง submit-agents ====
    submit_parser = subparsers.add_parser("submit-agents", help="สร้างและเรียกใช้เอเจนท์พร้อมกันหลายตัว")
    submit_parser.add_argument("--num-agents", type=int, required=True, help="จำนวนเอเจนท์ที่ต้องการใช้งาน")
    submit_parser.add_argument("--agents", required=True, help="ชื่อเอเจนท์ (เช่น chatgpt,cast) คั่นด้วย comma")
    submit_parser.add_argument("--name", required=True, help="ชื่อของงาน (Job Name)")
    submit_parser.add_argument("--target", required=True, help="เป้าหมายหลักของงาน")
    submit_parser.add_argument("--desc", required=True, help="รายละเอียดงาน/คำอธิบายเพิ่มเติม")

    args = parser.parse_args()
    if args.command == "submit-agents":
        submit_agents(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

## **อธิบายการสร้าง/ส่วนสำคัญในเทมเพลต**
- รองรับภาษาไทยทุกจุด (prompt, อธิบาย, output)
- สามารถใส่ชื่อเอเจนท์ได้หลายตัวพร้อมกัน ผ่าน parameter --num-agents และ --agents
- ตัวอย่าง:  
  ```
  python cli.py submit-agents --num-agents 2 --agents chatgpt,cast --name "แปลข้อความ" --target "แปลจากอังกฤษเป็นไทย" --desc "ใช้โครงสร้างทางภาษาแบบเป็นทางการ"
  ```
- เพิ่ม agent อื่นๆ ได้ใน AGENT_CLASSES ที่เดียว  
- กำหนด/แก้ไขการ map name/class ได้ง่าย

## **หมายเหตุ**
- หากอยากรับ parameter อื่นๆ เพิ่ม (เช่น context พิเศษ ฯลฯ) สามารถเพิ่ม argument ใน submit_parser และปรับ func เรียกใช้_เอเจนท์ ได้
- agent ทุกตัวที่ใช้ run() ตามเทมเพลตฐาน สามารถใช้งานร่วมกับโมเดลนี้ได้เลย

