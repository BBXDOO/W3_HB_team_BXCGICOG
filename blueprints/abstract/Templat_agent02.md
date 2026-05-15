## แนวทางสร้าง **เทมเพลต** ที่ map กับ plan, context และข้อมูลพิเศษอื่นๆ — พร้อมตัวอย่างการ “อ่านเอกสาร”, “นำข้อมูล”, “วิเคราะห์”, “บันทึก” ฯลฯ — โดยเชื่อมกับ flow ของ agent แบบ dynamic

---

## 1. ตัวอย่างเทมเพลต Markdown  
(สมมติไฟล์ `blueprints/abstract/Template_agent01.md`)

````markdown name=blueprints/abstract/Template_agent01.md
# เทมเพลตเอเจนท์: {{ agent_type }}

## 1. ภารกิจ  
- ชื่องาน: {{ plan.task_name }}
- เป้าหมายหลัก: {{ plan.target }}
- รายละเอียด: {{ plan.desc }}
- ความเร่งด่วน: {{ plan.urgency | default("ธรรมดา") }}

## 2. ผู้รับผิดชอบ  
- บทบาท: {{ plan.role }}
- ผู้ ใช้บริการ: {{ context.user }}
- ลูกค้า: {{ context.customer | default("-") }}

## 3. ขั้นตอนดำเนินการ
{% if documents %}
1. อ่านเอกสารอ้างอิง:
   {% for doc in documents %}
   - {{ doc }}
   {% endfor %}
{% endif %}
2. วิเคราะห์ข้อมูลสำคัญ
3. สร้างสรุป/ผลลัพธ์
4. (ถ้าต้องบันทึก) บันทึกลง: {{ context.save_path | default("N/A") }}

## 4. ผลลัพธ์ที่คาดหวัง  
- {{ plan.expected_output | default("สรุป/คำแนะนำตามโจทย์") }}

## 5. ข้อมูลพิเศษประกอบ  
{{ plan.blueprint | default("") }}

---
**หมายเหตุ:** ฟิลด์ {{ ... }} จะถูก map อัตโนมัติจาก plan, context หรือข้อมูลพิเศษ
````

---

## 2. วิธี Map ข้อมูลพิเศษกับ plan, context ในโค้ด

```python
import markdown
from jinja2 import Template

def load_template_md(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()

def render_template(template_str, context_dict):
    """ใช้ Jinja2 เพื่อ map ข้อมูลลงเทมเพลต"""
    return Template(template_str).render(**context_dict)

# ตัวอย่างการเตรียม plan, context, documents
plan = {
    "task_name": "สรุปหัวข้อประชุม",
    "target": "จับใจความสำคัญ",
    "desc": "พูดง่าย ใช้ Actionable",
    "role": "moderator",
    "urgency": "สูง",
    "blueprint": "https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/refactor/v0.2/blueprints/abstract/Template_agent01.md"
}
context = {
    "user": "BBXDOO",
    "customer": "บริษัทA",
    "save_path": "outputs/meeting_summary.md"
}
documents = [
    "docs/meeting/meeting2026-05-15.txt",
    "docs/meeting/slides2026.pdf"
]

# โหลดและ render
template_str = load_template_md("blueprints/abstract/Template_agent01.md")
full_context = {
    "plan": plan,
    "context": context,
    "documents": documents,
    "agent_type": "ChatGPTAgent"
}
output_doc = render_template(template_str, full_context)

# บันทึกผลลัพธ์
with open("outputs/meeting_task_full.md", "w", encoding="utf8") as f:
    f.write(output_doc)
```

---

## 3. การอ่านไฟล์เอกสารในโฟลเดอร์ (เช่น docs/meeting/)

```python
import os

def find_documents(folder, pattern=".txt"):
    files = []
    for fname in os.listdir(folder):
        if fname.endswith(pattern):  # ใช้ pattern อื่นได้เช่น .pdf
            files.append(os.path.join(folder, fname))
    return files

# ใช้งาน
doc_list = find_documents("docs/meeting/", ".txt")
```

---

## 4. ตัวอย่างการใช้งานใน agent

สมมติใน agent (เช่น ChatGPTAgent)  
- รับ plan, context, documents, blueprint  
- สามารถนำไปวิเคราะห์, สร้างหรือบันทึกได้

```python
class ChatGPTAgent(RuntimeAgent):
    # ...
    def run(self, task, plan, context, documents=None, blueprint_template=None):
        # อ่านและ render เทมเพลต
        if blueprint_template:
            template_str = load_template_md(blueprint_template)
            full_ctx = {"plan": plan, "context": context, "documents": documents or [], "agent_type": self.__class__.__name__}
            doctext = render_template(template_str, full_ctx)
        else:
            doctext = "ไม่มีเทมเพลต"

        # วิเคราะห์/ย่อยข้อมูล, อาจรวม step การประมวลผล-เขียนไฟล์ ฯลฯ
        # ... เช่น สรุป, วิเคราะห์, ประเมิน
        # สุดท้ายบันทึก
        with open(context.get("save_path", "outputs/result.txt"), "w", encoding="utf8") as f:
            f.write(doctext)
        return f"บันทึกเทมเพลตผลลัพธ์แล้ว: {context.get('save_path')}"
```

---

## สรุป

- **Template (Markdown/Jinja2)** ใช้ map แสดงข้อมูล plan, context, เอกสาร, blueprint, etc.
- **ข้อมูลพิเศษอื่น ๆ**: ส่งเข้า agent (`run`) หรือ CLI ได้เอง เช่น save_path, urgency, documents, blueprint URL
- **ขั้นตอนวิเคราะห์/บันทึก/อ่านเอกสาร**: สามารถจับรวมเป็นลูปใน CLI หรือใน agent ตามตัวอย่างข้างบน
- **การอ่านโครงสร้างโฟลเดอร์**: ใช้ os.listdir, glob ฯลฯ แล้ว list path ส่งเข้า template หรือวิเคราะห์ต่อ

---

