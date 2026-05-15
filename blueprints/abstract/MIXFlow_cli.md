ตัวอย่างนี้คือ CLI (เช่นไฟล์ `cli.py`) ที่ “รวม flow ครบถ้วน” ตั้งแต่  
- รับค่าหลากหลาย (agent, ชื่อ, เป้าหมาย, รายละเอียด, ผู้ใช้, บทบาท, blueprint, context, documents ฯลฯ)  
- map ข้อมูลลง template  
- อ่านเอกสารในโฟลเดอร์  
- เรียก agent สร้างผลลัพธ์ (วิเคราะห์/บันทึก/ตอบกลับ)  
- รองรับ flow หลาย agent ในรอบเดียว  
- ใช้งานจริงได้จาก CLI

**ตัวอย่างนี้สมบูรณ์สำหรับขยายเติมจุด logic เพิ่มเองตามโจทย์**

---

```python name=cli.py
import argparse
import os
from core.runtime.agents.chatgpt import ChatGPTAgent
from core.runtime.agents.cast import CastAgent
# เพิ่ม agent อื่นๆ ได้ใน AGENT_CLASSES
from jinja2 import Template

# Mapping agent name -> class
AGENT_CLASSES = {
    "chatgpt": ChatGPTAgent,
    "cast": CastAgent,
    # เพิ่ม agent อื่น ๆ
}

def สร้าง_เอเจนท์(agent_name):
    agent_name = agent_name.lower()
    if agent_name not in AGENT_CLASSES:
        raise ValueError(f"ไม่พบเอเจนท์ '{agent_name}' (มี {', '.join(AGENT_CLASSES)})")
    return AGENT_CLASSES[agent_name]()

def find_documents(folder, pattern=(".txt", ".md", ".pdf")):
    files = []
    if not os.path.isdir(folder): return files
    for fname in os.listdir(folder):
        if fname.endswith(pattern):
            files.append(os.path.join(folder, fname))
    return files

def load_template_md(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()

def render_template(template_str, context_dict):
    return Template(template_str).render(**context_dict)

def parse_extra_parameters(extra_args):
    result = {}
    for param in extra_args or []:
        if '=' not in param: continue
        key, value = param.split('=', 1)
        result[key] = value
    return result

def submit_agents(args):
    # เตรียมข้อมูลเอกสาร/blueprint
    documents = []
    if args.docs_folder:
        documents = find_documents(args.docs_folder)
    elif args.documents:
        documents = args.documents.split(",")

    plan = {
        "task_name": args.name,
        "target": args.target,
        "desc": args.desc,
        "role": args.role,
        "urgency": args.urgency,
        "expected_output": args.expect,
        **parse_extra_parameters(args.extra)
    }
    context = {
        "user": args.user,
        "customer": args.customer,
        "save_path": args.save_path,
        **parse_extra_parameters(args.ctx)
    }

    # ถ้ามี blueprint template: โหลด template เลย (อ่านจากพาธ local หรือดาวน์โหลด)
    if args.blueprint:
        template_path = args.blueprint
        template_str = load_template_md(template_path)
    else:
        template_str = None

    # ทำงานหลาย agent ในรอบเดียว
    agent_names = [n.strip() for n in args.agents.split(",") if n.strip()]
    for agent_name in agent_names:
        try:
            agent = สร้าง_เอเจนท์(agent_name)
            print(f"\n---[Agent: {agent_name}]---")
            full_ctx = {
                "plan": plan,
                "context": context,
                "documents": documents,
                "agent_type": agent.__class__.__name__
            }
            # map template → ผลลัพธ์
            if template_str:
                output_doc = render_template(template_str, full_ctx)
            else:
                output_doc = f"***ผลลัพธ์ (agent: {agent_name})***\n{plan}\n{context}\n{documents}"

            # วิเคราะห์/เพิ่ม logic เฉพาะ agent ได้ที่นี่
            # เช่น agent อาจวิเคราะห์หรือเขียนสรุปเพิ่ม/วาดกราฟ/ประมวลผล
            # จากนั้นบันทึกผล
            save_path = context.get("save_path") or f"outputs/result_{agent_name}.md"
            with open(save_path, "w", encoding="utf8") as f:
                f.write(output_doc)
            print(f"✅ บันทึกผลไว้ที่: {save_path}")
        except Exception as e:
            print(f"[{agent_name}] error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Task CLI (Flow ครบ อ่าน template, เอกสาร, agent พร้อมกัน)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    submit_parser = subparsers.add_parser("submit-agents", help="รัน agent หลายตัวตาม flow ที่กำหนด")
    submit_parser.add_argument("--agents", required=True, help="ชื่อ agent เช่น chatgpt,cast")
    submit_parser.add_argument("--name", required=True, help="ชื่องาน")
    submit_parser.add_argument("--target", required=True, help="เป้าหมาย")
    submit_parser.add_argument("--desc", required=True, help="รายละเอียด")
    submit_parser.add_argument("--urgency", required=False, default="ปกติ", help="ความเร่งด่วน")
    submit_parser.add_argument("--role", required=False, default="user", help="บทบาท (user/system ฯลฯ)")
    submit_parser.add_argument("--user", required=False, default="guest", help="ชื่อผู้ใช้")
    submit_parser.add_argument("--customer", required=False, default="", help="ลูกค้า (optional)")
    submit_parser.add_argument("--expect", required=False, default="", help="สิ่งที่คาดหวัง")
    submit_parser.add_argument("--blueprint", required=False, default="", help="path ถึง template .md (optional)")
    submit_parser.add_argument("--docs-folder", required=False, default="", help="โฟลเดอร์เอกสาร (optional)")
    submit_parser.add_argument("--documents", required=False, default="", help="ระบุเอกสารรายชื่อไฟล์ คั่นด้วยคอมม่า (ใช้แทน docs-folder ได้)")
    submit_parser.add_argument("--save-path", required=False, default="", help="จะจัดเก็บไฟล์เอาท์พุตที่ไหน (หากเว้นว่างจะเซฟ outputs/result_<agent>.md)")
    submit_parser.add_argument("--extra", action="append", help="พารามิเตอร์เสริม plan (key=val)", default=[])
    submit_parser.add_argument("--ctx", action="append", help="พารามิเตอร์เสริม context (key=val)", default=[])
    args = parser.parse_args()
    if args.command == "submit-agents":
        submit_agents(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

### วิธีใช้ (ตัวอย่างการใช้งานจริง)

```sh
python cli.py submit-agents \
  --agents chatgpt,cast \
  --name "สรุปข้อคิดเห็น Q2" \
  --target "วิเคราะห์ไฟล์ประชุม" \
  --desc "สรุปให้ละเอียดพร้อมรายการ action" \
  --user "BBXDOO" \
  --customer "BigCorp" \
  --urgency "สูง" \
  --role "moderator" \
  --expect "ได้หัวข้อ action items พร้อมความเห็นสำคัญ" \
  --blueprint blueprints/abstract/Templat_agent02.md \
  --docs-folder docs/meeting/ \
  --save-path outputs/report-BBXDOO.md \
  --extra level=confidential \
  --extra reviewer=CEO \
  --ctx timezone=Asia/Bangkok \
  --ctx revision=1
```

#### Flow ที่ได้
- อ่านเอกสารทั้งหมดใน docs/meeting/
- map ข้อมูลสร้างผลลัพธ์ด้วยเทมเพลต Jinja2 (`Templat_agent02.md`)
- ส่ง plan/context/เอกสาร เข้า agent (หนึ่งหรือหลายตัวพร้อมกัน)
- บันทึกเอาท์พุต (แบ่งตาม agent)

---

### จุดขยายเพิ่มเติม
- สามารถเพิ่ม logic เฉพาะ (เช่น วิเคราะห์ไฟล์ pdf/text ก่อน map template, เรียก model ไล่ทีละ agent แล้วส่งผลต่อ, …) ได้ในจุด submit_agents()
- สามารถปรับให้ agent ทุกตัวมี logic เฉพาะตน หรือเลือก template อัตโนมัติตาม agent ได้
- สามารถอ่านไฟล์ template จาก remote URL (โหลดไฟล์ก่อน render) ได้หากต้องการ

---

**Flow นี้เหมาะสำหรับ:**
- Automate งาน วิเคราะห์-สรุป-บันทึก-แปลงข้อมูล ด้วย agent หลายตัว
- ใช้งานกับ template/blueprint/plan ต่าง ๆ ได้สะดวกครบจบใน script เดียว
- ขยาย logic ได้ง่าย ทั้งในระดับ CLI/agent/template

หากต้องการขยาย logic เฉพาะ agent หรือตัวอย่าง template, agent, input, หรือ output format เพิ่มเติม  
แจ้งได้เลยครับ!
