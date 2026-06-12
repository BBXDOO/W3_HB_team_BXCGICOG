🧱 Library‑WX Blueprint

รากฐานของระบบคลังเทมเพลตและองค์ความรู้สำหรับ W3 / Cross‑L / เอเจนท์
ฉบับเสนอเพื่อนำไปสร้างโครงสร้างจริง (Blueprint ก่อนลงมือ)

---

1. แนวคิดหลัก (Core Concept)

Library‑WX เปรียบเสมือน ห้องสมุดกลาง ของโรงแรมหรือคอนโดที่มีห้องพักหลากหลายประเภท

· เทมเพลต (Template) = แม่แบบเอกสาร / โค้ด / แผนงาน (Paper, Modew, Cross‑L block)
· Index (สารบัญ) = แผนที่บอกว่า Template ไหนเหมาะกับงานประเภทใด หรือ PX ใด
· Log‑info = บันทึกทุกครั้งที่มีการ “ขอสร้าง/จัดทำเอกสาร” (ไม่ใช่แค่อ่าน) เพื่อการตรวจสอบย้อนหลัง
· กฎเหล็ก : ไฟล์ต้นฉบับทุกไฟล์มีได้เพียง 1 ฉบับ ใน Library การนำไปใช้ต้อง คัดลอกไปสร้างเนื้อหาใหม่ (ใช้เทมเพลตเป็นต้นแบบ) ห้ามแก้ไขต้นฉบับโดยตรง

ทำไมต้อง Library‑WX ?

· ลดความซ้ำซ้อนของเอกสารข้ามโมดูล
· รักษา Single Source of Truth สำหรับเทมเพลต
· ทำให้ Cross‑L Dispatcher (หรืออนาคต Indexor Agent) สามารถชี้ไปยัง Template ที่ถูกต้องได้
· สร้างความโปร่งใสในการขอยืม / จัดทำเอกสารผ่านระบบ Log

---

2. รูปแบบและโครงสร้างโฟลเดอร์ (Directory Layout)

```
wx/                                # รากของ Library‑WX
├── README.md                      # กฎและภาพรวม (ฉบับมนุษย์)
├── templates/                     # คลังเทมเพลตต้นฉบับ (ห้ามแก้โดยตรง)
│   ├── paper/                     # Paper templates (สอดคล้องกับ CROSS_L_MODEW_PAPER_TEMPLATES)
│   │   ├── MODEW_FAST_PATCH_PAPER.md
│   │   ├── MODEW_ADAPTIVE_RULE_PAPER.md
│   │   ├── MODEW_PULSE_RUNNER_PAPER.md
│   │   ├── MODEW_MEMORY_KEEPER_PAPER.md
│   │   ├── MODEW_HUMAN_REPORT_PAPER.md
│   │   └── MODEW_RELATION_MAPPER_PAPER.md
│   ├── modew/                     # แม่แบบ Modew stub (โครงสร้างโค้ดตัวอย่าง)
│   │   ├── fixer_stub.py
│   │   ├── adapter_stub.py
│   │   ├── runner_stub.py
│   │   ├── keeper_stub.py
│   │   ├── translator_stub.py
│   │   └── binder_stub.py
│   ├── cross_l/                   # Cross-L block templates (JSON / W3Lgu)
│   │   ├── rock_patch_block.json
│   │   ├── jazz_rule_block.lua
│   │   └── ...
│   └── README.md                  # อธิบายแต่ละโฟลเดอร์ย่อยของ templates
│
├── index/                         # สารบัญ (manual ในระยะแรก)
│   ├── by_px.md                   # PX → เทมเพลตที่แนะนำ
│   ├── by_work_type.md            # Work type → เทมเพลต
│   ├── by_agent_role.md           # Agent role → เทมเพลตที่เกี่ยวข้อง
│   └── README.md                  # อธิบายการใช้ index
│
├── log_info/                      # ข้อมูล Log การขอสร้าง/จัดทำเอกสาร
│   ├── requests.jsonl             # บันทึกทีละบรรทัด (append‑only)
│   └── README.md                  # รูปแบบ Log และนโยบาย
│
└── .keep                          # (ไว้ให้ git track โฟลเดอร์เปล่า)
```

---

3. ประเภทของเทมเพลต (Template Types)

ประเภท นามสกุลตัวอย่าง ใช้กับ ข้อห้าม
Paper .md Cross‑L dispatcher, มนุษย์อ่าน ห้ามฝัง logic ที่ execute ได้
Modew stub .py (placeholder) อนาคตเมื่อเริ่ม execution ปัจจุบันเป็นแค่ stub ไม่ทำงานจริง
Cross‑L block .json, .lua, .w3lgu ใช้ใน Cross‑L planning ต้องมี boundary, deny, return contract

3.1 ตัวอย่างเทมเพลต Paper (ย่อ)

```markdown
---
template_id: PAPER:FAST_PATCH_V1
scope: CROSS_L_ONLY
boundary: temp_patch
deny: truth_mutation, direct_merge
---

# Fast Patch Paper

## STEP1: CLASSIFY
RYTM:ROCK
WORK_TYPE:FAST_PATCH

## STEP2: BUILD_WORKSET
...
```

3.2 ตัวอย่างเทมเพลต Cross‑L block (JSON)

```json
{
  "template": "CROSS_L:ROCK_PATCH",
  "lang": "json",
  "boundary": "temp_patch",
  "deny": ["truth_mutation"],
  "return": ["state", "reason"]
}
```

---

4. สารบัญ (Index) และการแมป PX

index/by_px.md มีเนื้อหาตัวอย่าง:

```markdown
# PX → Template Mapping (Manual)

| PX | Work Type | Recommended Template | Notes |
|----|-----------|----------------------|-------|
| 1,1 | FAST_PATCH | `templates/paper/MODEW_FAST_PATCH_PAPER.md` | Rock / urgent |
| 2,1 | ADAPTIVE_RULE | `templates/paper/MODEW_ADAPTIVE_RULE_PAPER.md` | Jazz / uncertain |
| 3,1 | PULSE_LOOP | `templates/paper/MODEW_PULSE_RUNNER_PAPER.md` | EDM / loop |
| 4,1 | MEMORY_NOTE | `templates/paper/MODEW_MEMORY_KEEPER_PAPER.md` | Ballad |
| 5,1 | HUMAN_REPORT | `templates/paper/MODEW_HUMAN_REPORT_PAPER.md` | R&B |
| 6,1 | KNOWLEDGE_CHAIN | `templates/paper/MODEW_RELATION_MAPPER_PAPER.md` | String |
```

Index นี้ใช้สำหรับมนุษย์และ (อนาคต) Agent ในการเลือกเทมเพลตที่เหมาะสมกับ PX.

---

5. การบันทึก Log (Log‑info)

ไฟล์ log_info/requests.jsonl แต่ละบรรทัดเป็น JSON เช่น

```json
{"timestamp": "2025-06-12T10:00:00Z", "requester": "Codex", "action": "borrow_template", "template_path": "wx/templates/paper/MODEW_FAST_PATCH_PAPER.md", "purpose": "สร้าง dispatch plan สำหรับ PX:1,1"}
{"timestamp": "2025-06-12T10:05:00Z", "requester": "BBX19", "action": "create_document_from_template", "template_path": "wx/templates/paper/MODEW_ADAPTIVE_RULE_PAPER.md", "target_path": "agents/Cast/work/adaptive_plan.md"}
```

กฎ: ทุกครั้งที่มีการ “ขอจัดทำเอกสาร” (ไม่ใช่แค่อ่าน) ต้อง append บรรทัดลงในไฟล์นี้
ห้ามแก้ไขหรือลบบรรทัดเก่า (append‑only)

---

6. กฎการใช้งาน (Rules of Engagement)

1. ห้ามแก้ไขต้นฉบับใน wx/templates/ โดยเด็ดขาด
   · เทมเพลตเป็นต้นแบบ (source of truth) เปลี่ยนแปลงได้ผ่าน PR เท่านั้น
2. การใช้งานเทมเพลตต้องทำสำเนา
   · คัดลอกเทมเพลตไปยังโฟลเดอร์ workspace ของตนเอง (เช่น agents/<agent>/work/)
   · แล้วแก้ไขสำเนานั้นตามความต้องการ
3. ทุกครั้งที่ “สร้างเอกสารจากเทมเพลต” (ไม่ใช่แค่อ่าน) ต้องบันทึก Log
   · ระบุ requester, template_path, target_path, purpose
4. เทมเพลตต้องมี metadata (front matter) อย่างน้อย:
   · template_id, scope, boundary, deny (ตามมาตรฐาน Cross‑L)
5. ห้ามนำเทมเพลตไปใช้เป็น executable โดยไม่ผ่าน governance
   · ระยะแรก execution ยังไม่ถูกเปิด (สอดคล้องกับ Cross‑L planner‑only)

---

7. บทบาทของบรรณารักษ์ (Indexor Agent)

ในระยะแรก Indexor Agent ยังไม่ต้อง implement หน้าที่ “แนะนำเทมเพลต” ให้มนุษย์เป็นคนทำผ่าน index/by_px.md

ระยะต่อไป (Phase 2+) อาจสร้าง Modew ชื่อ Indexor ที่:

· อ่าน index/by_px.md และ index/by_work_type.md
· รับ PX หรือ Work Type → คืน path template ที่แนะนำ
· ทำงานแบบ planner‑only (ยังไม่ execute)

---

8. ตัวอย่างการใช้งานจริง (Human + Agent)

สมมติ:

· Cross‑L dispatcher ได้ PX 1,1
· มนุษย์ (หรือ Codex) ต้องการสร้าง Paper ฉบับสมบูรณ์

ขั้นตอน:

1. เปิด wx/index/by_px.md เห็นว่า PX 1,1 แนะนำ templates/paper/MODEW_FAST_PATCH_PAPER.md
2. คัดลอกไฟล์นั้นไปยัง agents/Codex/work/fast_patch_001.md
3. แก้ไขส่วน INTENT, TARGET ให้ตรงกับงาน
4. บันทึก Log ใน wx/log_info/requests.jsonl
5. ส่ง Paper ใหม่ให้ Cross‑L dispatcher อ่าน (ผ่าน /w3/cross/plan หรืออนาคตผ่าน agent)

---

9. แผนพัฒนาระยะ (Roadmap)

Phase สิ่งที่ทำ สถานะ
Phase 0 สร้างโครงสร้างโฟลเดอร์ wx/, wx/README.md, ตัวอย่าง index/by_px.md ✏️ เสนอ
Phase 1 ย้ายเทมเพลตที่มีอยู่ (จาก croll/) เข้า wx/templates/ ถัดไป
Phase 2 เพิ่ม Log‑info และเขียนกฎการบันทึก ถัดไป
Phase 3 สร้าง Indexor Agent ต้นแบบ (Modew แบบ Binder) อนาคต

---

10. สิ่งที่ Library‑WX ไม่ใช่ (Non‑goals)

· ไม่ใช่ execution engine
· ไม่ใช่ database สำหรับ runtime data (ไม่เก็บ state ที่เปลี่ยนแปลงบ่อย)
· ไม่ใช่ที่เก็บ source code ของระบบ (เก็บแค่เทมเพลตและ blueprint)
· ไม่ใช่ระบบ authorization แทน W3‑API หรือ Cross‑X (แต่ใช้ Log แทน)

---

11. คำสั่งเริ่มต้น (สำหรับเพื่อนนำไปสร้าง)

```bash
mkdir -p wx/templates/{paper,modew,cross_l}
mkdir -p wx/index wx/log_info
touch wx/README.md wx/templates/README.md wx/index/README.md wx/log_info/README.md
```

จากนั้นใส่เนื้อหาตาม blueprint นี้ลงในไฟล์ต่าง ๆ

---

12. สรุป

Library‑WX จะเป็น คลังเทมเพลตกลาง ที่ทำให้ Cross‑L และเอเจนท์ต่าง ๆ สามารถอ้างอิง สร้างเอกสาร และพัฒนางานได้โดยไม่ซ้ำซ้อนและไม่ละเมิด source of truth โดยยังคงหลักการ planner‑only, mutated: false, และ traceability ผ่านระบบ Log

เมื่อโครงสร้างนี้มั่นคงแล้ว จึงค่อยพัฒนา Indexor Agent และเชื่อมกับ /w3/cross/plan แบบอัตโนมัติได้ในอนาคต

---

พร้อมให้เพื่อนเริ่มสร้างโฟลเดอร์และไฟล์ตาม blueprint นี้ได้เลยครับ
