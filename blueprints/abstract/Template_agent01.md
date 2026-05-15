## ต่อไปนี้เป็นเทมเพลต cli.py ที่ยืดหยุ่นมากขึ้น ― สามารถรับ “พารามิเตอร์พิเศษอื่นๆ” เพิ่มได้แบบ dynamic ซึ่งจะถูกส่งเข้า agent (เช่น blueprint, role, หรือ parameter user-defined ใดๆ)  
พร้อมตัวอย่างการใช้งานจริงจาก CLI

---

```python name=cli.py
import argparse

# นำเข้า agent ที่ใช้งาน
from core.runtime.agents.chatgpt import ChatGPTAgent
from core.runtime.agents.cast import CastAgent
# เพิ่ม agent อื่น ๆ ได้ โดยแก้ที่ AGENT_CLASSES ด้านล่าง

# dictionary สำหรับ mapping agent name => class
AGENT_CLASSES = {
    "chatgpt": ChatGPTAgent,
    "cast": CastAgent,
    # "gemini": GeminiAgent,
    # เพิ่มชื่อ-agent และ class ตามต้องการ
}

def สร้าง_เอเจนท์(agent_name):
    """คืนค่าอินสแตนซ์ agent จากชื่อ"""
    agent_name = agent_name.lower()
    if agent_name not in AGENT_CLASSES:
        raise ValueError(f"เอเจนท์ '{agent_name}' ไม่ถูกต้อง (ระบบรองรับ: {', '.join(AGENT_CLASSES)})")
    return AGENT_CLASSES[agent_name]()

def เรียกใช้_เอเจนท์(agent_instance, ชื่องาน, แผน, คอนเท็กซ์):
    """เรียกใช้ run() ของ agent"""
    return agent_instance.run(ชื่องาน, แผน, คอนเท็กซ์)

def parse_extra_parameters(extra_args):
    """
    รับ argument format: --extra key1=value1 --extra key2=value2 ...  
    คืน dict {"key1": value1, ...}
    """
    result = {}
    if extra_args:
        for param in extra_args:
            if '=' not in param:
                continue
            key, value = param.split('=', 1)
            result[key] = value
    return result

def submit_agents(args):
    print(f"\n=== เรียกใช้ {args.num_agents} agent(s) ===")
    agent_names = [a.strip() for a in args.agents.split(",") if a.strip()]
    if len(agent_names) != args.num_agents:
        print("จำนวนชื่อ agent ไม่ตรงกับจำนวนที่ระบุ")
        return

    extra_plan = parse_extra_parameters(args.extra or [])
    extra_ctx = parse_extra_parameters(args.ctx or [])

    for agent_name in agent_names:
        try:
            agent = สร้าง_เอเจนท์(agent_name)
            print(f"\n[Agent: {agent_name}] ...")
            # แผนงานหลักที่ส่งเข้า agent
            plan = {
                "role": args.role,
                "responsibilities": [args.target, args.desc],
                **extra_plan  # ใส่พารามิเตอร์พิเศษด้าน plan (dict)
            }
            # คอนเท็กซ์หลัก
            context = {
                "user": args.user,
                **extra_ctx  # ใส่คอนเท็กซ์พิเศษ
            }
            result = เรียกใช้_เอเจนท์(agent, args.name, plan, context)
            print("ผลลัพธ์:", result)
        except Exception as e:
            print(f"[{agent_name}] error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Task CLI (ภาษาไทย/พารามิเตอร์พิเศษ)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser("submit-agents", help="สร้างและเรียกใช้ agent หลายตัว")
    submit_parser.add_argument("--num-agents", type=int, required=True, help="จำนวน agent")
    submit_parser.add_argument("--agents", required=True, help="ชื่อ agent (คั่นด้วย comma เช่น chatgpt,cast)")
    submit_parser.add_argument("--name", required=True, help="ชื่อของงาน")
    submit_parser.add_argument("--target", required=True, help="เป้าหมายหลักของงาน")
    submit_parser.add_argument("--desc", required=True, help="รายละเอียดงาน/คำอธิบายเพิ่มเติม")
    submit_parser.add_argument("--role", required=False, default="user", help="บทบาทในการดำเนินงาน (เช่น user/system/approver)")
    submit_parser.add_argument("--user", required=False, default="guest", help="ชื่อผู้ใช้/รหัส/identity")
    # รับ argument พิเศษเพิ่มเติมสำหรับ plan/context (key=value)
    submit_parser.add_argument("--extra", action="append", help="เพิ่ม parameter พิเศษใน plan: --extra key1=val1 --extra key2=val2", default=[])
    submit_parser.add_argument("--ctx", action="append", help="เพิ่ม parameter พิเศษใน context: --ctx key3=val3", default=[])

    args = parser.parse_args()
    if args.command == "submit-agents":
        submit_agents(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

## ตัวอย่างการใช้งาน

### ตัวอย่าง 1: ระบุ agent หลายตัว เป้าหมาย ภาษาไทย + พารามิเตอร์พิเศษ (blueprint, abstract)
```sh
python cli.py submit-agents \
    --num-agents 2 \
    --agents chatgpt,cast \
    --name "คิดบทพูด" \
    --target "พรีเซนต์สินค้าใหม่" \
    --desc "เน้นคุณค่าที่ไม่เหมือนใคร" \
    --role "copywriter" \
    --user "BBXDOO" \
    --extra blueprint=https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/blueprints/abstract \
    --extra urgency=สูงมาก \
    --ctx customer=บริษัทA \
    --ctx channel=Facebook
```
**เอาท์พุตที่ได้**  
จะวนลูปรันแต่ละ agent  
- Field ทุกตัวถูกส่งเข้า plan/context ตามค่าที่ใส่
- แสดงผลลัพธ์ agent run อย่างชัดเจน

### ตัวอย่าง 2: agent เดียว, เพิ่ม context/plan พิเศษ
```sh
python cli.py submit-agents \
    --num-agents 1 \
    --agents chatgpt \
    --name "สรุปหัวข้อประชุม" \
    --target "จับใจความสำคัญและข้อสรุป" \
    --desc "ใช้ภาษากระชับ พูดง่าย" \
    --extra blueprint=ประชุมทีม \
    --ctx language=TH
```

---

### หมายเหตุ  
- ฟิลด์ `--extra` ถูกเติมเข้า plan (dict)  
- ฟิลด์ `--ctx` ถูกเติมเข้า context (dict)
- สามารถเพิ่ม parameter อะไรก็ได้ — เช่น blueprint, level, urgency, reference, ฯลฯ

#### ขยาย agent ใหม่/agent อื่นๆ:  
เพียง import และใส่ชื่อ agent ใหม่ใน AGENT_CLASSES  
หาก agent ของคุณรับ parameter อื่นๆ เพิ่ม อาจ custom ฟังก์ชัน เรียกใช้_เอเจนท์ เพิ่มเติมได้เช่นกัน

---

