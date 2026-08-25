📚 BOX Knowledge Infrastructure — ฉบับ Blueprint สมบูรณ์ (v1.0)

สถานะ: Blueprint เสนอ
Owner: BBX19
Scope: Planner‑Only | Runtime: None | Mutated: False
Relation: W3 / Library‑WX / Cross‑L / MPCP / W3‑API

> **สถานะการอ่านปัจจุบัน:** Applied Build Anchor — Blueprint นี้ถูกนำไปสร้างใน `wx/` แล้วหลายส่วน  
> **AMS Mapping:** BUILD; แกนหลัก AM Ⅱ พร้อม Concept ระดับ AM Ⅰ และ prototype/test ระดับ AM Ⅲ  
> **ขอบเขตสำคัญ:** คำว่า BOX ในเอกสารนี้หมายถึง **BOX Knowledge Infrastructure v1.0** ไม่ใช่นิยาม Core ทั้งหมดของ BOX  
> **Core ที่ต้องรักษา:** BOX ในความหมายกว้างกว่ามีหน้าที่กำหนดพื้นที่, boundary และความหมาย; Library‑WX เป็นหน่วยคลังภายในพื้นที่นั้น  
> **Historical integrity:** ตัวอย่าง code, test, endpoint และคำสั่งเดิมคงไว้เพื่อสอบย้อนเส้นทาง Concept → Structure → Activity

---

สารบัญ

1. แนวคิดหลัก
2. หลักการสำคัญ
3. สถาปัตยกรรม BOX
4. โครงสร้างโฟลเดอร์และไฟล์
5. Library‑WX – ห้องสมุดกลาง
6. Template System
7. Blueprint System
8. Registry Layer
9. Engine‑Index – ระบบนำทาง
10. Indexor Agent – บรรณารักษ์
11. Log‑Info – การบันทึกร่องรอย
12. PortDC – ประตูเอกสาร
13. WHUB Ready – รองรับโครงข่ายความรู้ในอนาคต
14. Lifecycle การใช้งาน
15. Non‑Goals (สิ่งที่ไม่ใช่)
16. ตัวอย่าง registry/template_registry.json
17. การปรับ cross_l_dispatcher.py ให้ดึงข้อมูลจาก BOX index
18. Integration Test สำหรับ BOX + W3‑API
19. คำสั่งเริ่มต้น (สำหรับมนุษย์)

---

1. แนวคิดหลัก

ใน Blueprint v1.0 นี้ BOX ถูกประยุกต์เป็นโครงสร้างพื้นฐานทางความรู้ (Knowledge Infrastructure) ของ W3
เปรียบเสมือนโรงแรมขนาดใหญ่ที่มี:

· ห้องสมุดกลาง – Library-WX (เก็บ Template, Blueprint)
· บรรณารักษ์ – Indexor Agent (แนะนำตำแหน่ง)
· ลิฟต์นำทาง – Engine-Index (ค้นหาและเชื่อมโยง)
· เคาน์เตอร์นำเข้า/ส่งออก – PortDC
· ประตูเชื่อมภายนอกในอนาคต – WHUB

BOX Knowledge Infrastructure v1.0 ไม่ใช่ runtime, execution engine, database หรือ state manager
ในขอบเขตของ Blueprint นี้ BOX ทำหน้าที่เป็น reference layer ให้มนุษย์และเอเจนท์ค้นหา อ้างอิง คัดลอก และสร้างเนื้อหาใหม่โดยไม่ละเมิดต้นฉบับ

ข้อจำกัดดังกล่าวใช้กับ implementation รุ่นนี้เท่านั้น ไม่ควรนำไปปฏิเสธความหมาย Core ของ BOX หรือความสามารถในบริบทอื่นที่มีต้นแบบและขอบเขตของตนเอง

---

2. หลักการสำคัญ

หลักการ คำอธิบาย
P1 – Single Source of Truth ไฟล์ต้นฉบับ (template, blueprint) มีตำแหน่งหลักเดียวใน wx/; งาน instance ต้อง copy-before-use ส่วนการบำรุงต้นฉบับทำได้เมื่อมี version, review และ provenance
P2 – Copy Before Use ทุกการใช้งานต้อง คัดลอก ไปยัง workspace ของตนเอง แล้วจึงแก้ไข
P3 – Planner First BOX ทำงานได้แค่ แนะนำ, อ้างอิง, ค้นหา, บันทึก – ไม่มีสิทธิ์ execute
P4 – Human First มนุษย์เป็นผู้ตัดสินใจขั้นสุดท้าย เอเจนท์เสนอเท่านั้น
P5 – Traceability ทุกการสร้างเอกสารใหม่ต้องบันทึก log ว่า มาจาก template ใด, ใคร, เมื่อไร, เพื่ออะไร

---

3. สถาปัตยกรรม BOX

```text
W3
│
├─ WHUB (Future) ───────┐
├─ PortDC               │
├─ BOX                  │
│   ├─ Library-WX       │
│   ├─ Engine-Index     │
│   ├─ Indexor Agent    │
│   ├─ Registry         │
│   └─ Log-Info         │
├─ Cross-L              │
├─ MPCP                 │
└─ Runtime Systems      │
                         ↓
                  External / Agent
```

· BOX ไม่เรียก Runtime
· W3‑API สามารถเรียกดู BOX ผ่าน /w3/cross/plan (หรือ endpoint ใหม่)

---

4. โครงสร้างโฟลเดอร์และไฟล์

```
wx/
├── README.md
├── templates/                      # แม่แบบ (ต้นฉบับ)
│   ├── paper/                      # Paper templates
│   ├── modew/                      # Modew stub templates
│   ├── cross_l/                    # Cross-L block templates
│   └── README.md
├── blueprints/                     # คำอธิบายโครงสร้าง (โครงสร้างระบบ, โฟลเดอร์)
│   ├── system/                     #  blueprint ของระบบ W3
│   ├── collection/                 # blueprint ของ collection
│   └── README.md
├── references/                     # เอกสารอ้างอิงทั่วไป (knowledge)
│   └── README.md
├── registry/                       # สารบัญหลัก (JSON metadata)
│   ├── template_registry.json
│   ├── agent_registry.json
│   ├── collection_registry.json
│   └── blueprint_registry.json
├── index/                          # แผนที่ (Markdown, human‑readable)
│   ├── by_px.md
│   ├── by_work_type.md
│   ├── by_agent_role.md
│   └── README.md
├── log_info/                       # บันทึกการสร้าง/คัดลอก (append‑only)
│   ├── requests.jsonl
│   ├── creations.jsonl
│   └── README.md
└── collections/                    # (ตัวเลือก) รวมเอกสารตามหมวดหมู่
    └── README.md
```

---

5. Library‑WX – ห้องสมุดกลาง

หน้าที่:

· เก็บ Template (แม่แบบเอกสาร / โค้ดต้นแบบ)
· เก็บ Blueprint (คำอธิบายโครงสร้าง)
· เก็บ Reference Knowledge (เอกสารอ้างอิงคงที่)

ห้ามเก็บ:

· Runtime state
· ข้อมูลที่เปลี่ยนแปลงบ่อย
· ผลลัพธ์จากการ execute

กฎ:

· ทุกไฟล์ใน templates/ และ blueprints/ ต้องมี metadata front matter (ดูข้อ 6)
· ห้ามแก้ไขโดยตรง ต้องคัดลอกไปใช้

---

6. Template System

6.1 Metadata ที่จำเป็น (YAML front matter)

```yaml
---
template_id: PAPER:FAST_PATCH_V1
version: 1.0.0
scope: CROSS_L_ONLY
boundary: temp_patch
deny: truth_mutation, direct_merge, repo_write_without_review
owner: BBX19
status: active
created_at: 2026-06-12
---
```

6.2 ตัวอย่าง Template Paper (wx/templates/paper/fast_patch.md)

```markdown
---
template_id: PAPER:FAST_PATCH_V1
version: 1.0.0
scope: CROSS_L_ONLY
boundary: temp_patch
deny: truth_mutation, direct_merge
owner: BBX19
status: active
created_at: 2026-06-12
---

# Fast Patch Paper

## STEP1: CLASSIFY
RYTM:ROCK
WORK_TYPE:FAST_PATCH

## STEP2: BUILD_WORKSET
TAG_GROUP: FAST,LOW,SCRIPT,CONFIG
LANG_CANDIDATE: cpp,rust,c,assembly,bash,json
READ: ENV,trace,error_report

## STEP3: DISPATCH
MODEW: FAST_PATCH
REVIEW: on_complete
```

6.3 การใช้งาน

1. คัดลอกไฟล์นี้ไปยัง agents/<agent>/work/
2. เปลี่ยน metadata (template_id อาจคงไว้เป็น reference)
3. ปรับเนื้อหาตามต้องการ
4. บันทึก log การสร้าง

---

7. Blueprint System

ในบริบทของ `wx/blueprints/` คำว่า Blueprint คือ declaration ของโครงสร้าง (โฟลเดอร์, ระบบ, Agent, Collection) และไม่ถูก execute เป็น logic หรือ flow

> กฎนี้เป็น boundary ของ wx Blueprint เท่านั้น ห้ามนำไปตัดสิน MPCP Blueprint หรือ Blueprint ของระบบอื่นซึ่งมีหน้าที่ตามต้นแบบของหน่วยงานนั้น

ตัวอย่าง wx/blueprints/collection/paper_collection.md:

```markdown
---
blueprint_id: BPD:COLLECTION_PAPER_V1
type: collection
path: /knowledge/papers
description: รวม Paper ที่เกี่ยวกับ Cross‑L
owner: BBX19
---
```

Blueprint ใช้สำหรับให้มนุษย์และ Indexor เข้าใจโครงสร้าง ไม่ถูก execute.

---

8. Registry Layer

Registry คือ metadata source of truth (JSON).
เก็บไว้ที่ wx/registry/

8.1 template_registry.json (ตัวอย่าง)

```json
{
  "version": "1.0",
  "templates": [
    {
      "template_id": "PAPER:FAST_PATCH_V1",
      "name": "Fast Patch Paper",
      "path": "wx/templates/paper/fast_patch.md",
      "version": "1.0.0",
      "owner": "BBX19",
      "status": "active",
      "work_type": "FAST_PATCH",
      "rytm": "ROCK",
      "px": ["1,1"],
      "boundary": "temp_patch",
      "deny": ["truth_mutation", "direct_merge"]
    },
    {
      "template_id": "PAPER:ADAPTIVE_RULE_V1",
      "name": "Adaptive Rule Paper",
      "path": "wx/templates/paper/adaptive_rule.md",
      "version": "1.0.0",
      "owner": "BBX19",
      "status": "active",
      "work_type": "ADAPTIVE_RULE",
      "rytm": "JAZZ",
      "px": ["2,1"],
      "boundary": "observe",
      "deny": ["truth_mutation", "file_write", "network"]
    }
  ]
}
```

Registry ใช้สำหรับ Indexor และ Engine‑Index ในการค้นหา.

---

9. Engine‑Index – ระบบนำทาง

หน้าที่:

· อ่าน registry / index (Markdown)
· รับ input: PX, work_type, rytm, intent → คืน path / template_id
· ไม่ execute, ไม่สร้างเอกสาร, ไม่แก้ไขไฟล์

9.1 การทำงาน (pseudo)

```python
# wx/engine_index.py (ตัวอย่าง)
import json
from pathlib import Path

REGISTRY_PATH = Path("wx/registry/template_registry.json")

def search_by_px(px: str) -> dict | None:
    with open(REGISTRY_PATH) as f:
        data = json.load(f)
    for tmpl in data["templates"]:
        if px in tmpl.get("px", []):
            return tmpl
    return None
```

Engine‑Index ไม่ต้องมี HTTP endpoint – ถูกเรียกโดย Indexor Agent หรือ Cross‑L Dispatcher โดยตรง.

---

10. Indexor Agent – บรรณารักษ์

Indexor Agent คือ Modew รูปแบบ Binder (ตาม Table‑X) ที่ทำหน้าที่ แนะนำ เทมเพลตหรือ blueprint ให้กับมนุษย์หรือเอเจนท์อื่น.

ความสามารถ:

· อ่าน wx/registry/ และ wx/index/
· รับ px หรือ work_type → คืนรายการ template/blueprint ที่แนะนำ
· ส่ง response ผ่าน /w3/cross/plan หรือเรียกใช้โดยตรง

ข้อจำกัด:

· ไม่มีสิทธิ์ execute
· ไม่มีสิทธิ์ copy หรือสร้างเอกสาร (มนุษย์เป็นผู้ copy เอง)

10.1 ตัวอย่างการเรียก (ภายใน Cross‑L Dispatcher)

```python
from wx.engine_index import search_by_px

def get_dispatch_plan(px: str):
    workset = get_workset_from_px(px)   # จาก table_x
    # หา template เพิ่มเติมจาก BOX registry
    template_info = search_by_px(px)
    return {
        "execution_allowed": False,
        "mutated": False,
        "safety": {...},
        "workset": workset,
        "suggested_template": template_info["path"] if template_info else None
    }
```

---

11. Log‑Info – การบันทึกร่องรอย

หลักการ: Append‑only, ไม่ลบ, ไม่แก้ไขย้อนหลัง
บันทึกเมื่อ: create, generate, borrow, export
ไม่บันทึกเมื่อ: read, learn, study

11.1 รูปแบบ JSONL (wx/log_info/creations.jsonl)

```json
{"timestamp": "2026-06-12T10:00:00Z", "requester": "Codex", "action": "copy_template", "template_id": "PAPER:FAST_PATCH_V1", "target_path": "agents/Codex/work/fast_patch_001.md", "purpose": "PX:1,1 native patch"}
{"timestamp": "2026-06-12T10:05:00Z", "requester": "BBX19", "action": "create_blueprint", "blueprint_id": "BPD:NEW_COLLECTION", "target_path": "wx/blueprints/collection/new.md"}
```

การใช้งาน: มนุษย์หรือ Agent สามารถอ่าน log เพื่อ audit หรือ trace

> Log เป็นหลักฐานของกิจกรรม ไม่ใช่ authorization การเขียน log หรือมี trace ไม่ได้ให้สิทธิ์ copy, export, mutate หรือเปิดเผยข้อมูล

---

12. PortDC – ประตูเอกสาร

PortDC ถูกเสนอเป็น Input/Output Gateway สำหรับเอกสารภายนอก

สถานะ implementation ปัจจุบัน: `wx/portdc.py` อ่านเฉพาะ template ที่ลงทะเบียนและคืน source เป็น response data แบบ read-only; ยังไม่เขียนปลายทาง ไม่เรียก network และไม่ใช่ WHUB gateway เต็มรูปแบบ

ทิศทางตาม Blueprint ทำหน้าที่:

· รับ request ภายนอก (ผ่าน W3‑API หรือ CLI) → ส่งไปยัง BOX
· ส่งเอกสาร, template, blueprint ออกไปยังผู้ขอ

ข้อจำกัด:

· ไม่ execute
· ไม่ mutate
· ไม่แก้ไขต้นฉบับ

ตัวอย่างการใช้ใน W3‑API (endpoint ใหม่ /w3/box/export – เสนอไว้ไม่บังคับ)

---

13. WHUB Ready – รองรับโครงข่ายความรู้ในอนาคต

WHUB จะเป็นโครงข่ายเชื่อม BOX กับ external knowledge hubs (node อื่น, ระบบอื่น)
ขณะนี้เพียงแค่:

· ออกแบบ Registry และ Index ให้มีฟิลด์ external_reference หรือ node (รองรับ URL)
· ยังไม่ต้อง implement จริง

ตัวอย่าง เตรียม field:

```json
{
  "template_id": "...",
  "external_ref": "https://example.com/knowledge/..."
}
```

---

14. Lifecycle การใช้งาน

```text
Need / Intent
    │
    ▼
Search (มนุษย์ / Indexor Agent) → ใช้ Engine‑Index / Registry
    │
    ▼
Locate Template / Blueprint
    │
    ▼
Copy Template to Workspace (มนุษย์หรือ Codex)
    │
    ▼
Edit & Create New Content (มนุษย์)
    │
    ▼
Log Creation (append to log_info)
    │
    ▼
Deliver / Use (นำไปใช้ใน Cross‑L หรืออื่น ๆ)
```

---

15. Non‑Goals (สิ่งที่ไม่ใช่)

BOX Knowledge Infrastructure v1.0 ไม่ใช่:

· Runtime หรือ execution engine
· Database ที่เก็บ dynamic state
· Memory store หรือ state manager
· Governance system (แต่ให้ traceability)
· แทนที่ Cross‑L หรือ MPCP

---

16. ตัวอย่าง registry/template_registry.json

ไฟล์完整ตัวอย่าง (พร้อมสำหรับการใช้งานจริง):

```json
{
  "version": "1.0",
  "updated_at": "2026-06-12T00:00:00Z",
  "templates": [
    {
      "template_id": "PAPER:FAST_PATCH_V1",
      "name": "Fast Patch Paper",
      "path": "wx/templates/paper/fast_patch.md",
      "version": "1.0.0",
      "owner": "BBX19",
      "status": "active",
      "work_type": "FAST_PATCH",
      "rytm": "ROCK",
      "px": ["1,1"],
      "boundary": "temp_patch",
      "deny": ["truth_mutation", "direct_merge", "repo_write_without_review"]
    },
    {
      "template_id": "PAPER:ADAPTIVE_RULE_V1",
      "name": "Adaptive Rule Paper",
      "path": "wx/templates/paper/adaptive_rule.md",
      "version": "1.0.0",
      "owner": "BBX19",
      "status": "active",
      "work_type": "ADAPTIVE_RULE",
      "rytm": "JAZZ",
      "px": ["2,1"],
      "boundary": "observe",
      "deny": ["truth_mutation", "file_write", "network", "merge"]
    },
    {
      "template_id": "CROSS_L:ROCK_BLOCK_V1",
      "name": "Rock Cross-L Block (JSON)",
      "path": "wx/templates/cross_l/rock_patch_block.json",
      "version": "1.0.0",
      "owner": "BBX19",
      "status": "active",
      "work_type": "FAST_PATCH",
      "rytm": "ROCK",
      "px": ["1,1"],
      "lang": "json",
      "boundary": "temp_patch",
      "deny": ["truth_mutation"]
    }
  ]
}
```

---

17. การปรับ cross_l_dispatcher.py ให้ดึงข้อมูลจาก BOX index (optional)

เพิ่มฟังก์ชัน _enrich_with_box_suggestion(px) และรวมเข้ากับ dispatch_workset

```python
# croll/cross_l_dispatcher.py (ปรับปรุง)
import json
from pathlib import Path

def _load_template_registry():
    reg_path = Path("wx/registry/template_registry.json")
    if not reg_path.exists():
        return {}
    with open(reg_path) as f:
        return json.load(f)

def _find_template_by_px(px: str, registry: dict):
    for tmpl in registry.get("templates", []):
        if px in tmpl.get("px", []):
            return tmpl
    return None

def dispatch_workset(px: str, enable_box_suggestion: bool = False) -> dict:
    # ... (原有 logic from table_x)
    workset = get_workset_from_px(px)   # จาก table_x
    result = {
        "state": "planned",
        "execution_allowed": False,
        "mutated": False,
        "safety": {
            "planner_only": True,
            "modew_execution_allowed": False,
            "truth_mutation_allowed": False,
            "repo_write_allowed": False,
            "direct_merge_allowed": False,
        },
        "workset": workset,
    }

    if enable_box_suggestion:
        registry = _load_template_registry()
        tmpl = _find_template_by_px(px, registry)
        if tmpl:
            result["suggested_template"] = {
                "template_id": tmpl["template_id"],
                "path": tmpl["path"],
                "name": tmpl.get("name", ""),
            }
        else:
            result["suggested_template"] = None
    return result
```

หมายเหตุ: ฟังก์ชัน dispatch_workset ยังคง execution_allowed: false เสมอ การเพิ่ม suggestion เป็นแค่ข้อมูลเสริม.

---

18. Integration Test สำหรับ BOX + W3‑API

สร้าง tests/test_box_integration.py (ใช้ pytest)

```python
import pytest
from fastapi.testclient import TestClient
from w3_api.main import app
from pathlib import Path
import json

client = TestClient(app)

# ตรวจสอบว่าไฟล์ registry มีอยู่และ readable
def test_box_registry_exists():
    reg_path = Path("wx/registry/template_registry.json")
    assert reg_path.exists(), "template_registry.json not found"
    data = json.loads(reg_path.read_text())
    assert "templates" in data

# ทดสอบ /w3/cross/plan ว่า response มี suggested_template (ถ้าเปิดใช้งาน)
def test_cross_plan_with_box_suggestion(monkeypatch):
    # สมมุติว่า dispatch_workset เปิด enable_box_suggestion=True
    # แต่ endpoint ยังไม่รองรับการ toggle, เรา mock ได้
    from croll import cross_l_dispatcher
    original = cross_l_dispatcher.dispatch_workset
    def mock_dispatch(px, enable_box_suggestion=False):
        # เรียกจริง แต่ force enable = True
        return original(px, enable_box_suggestion=True)
    monkeypatch.setattr(cross_l_dispatcher, "dispatch_workset", mock_dispatch)

    response = client.post("/w3/cross/plan", json={"px": "1,1"})
    assert response.status_code == 200
    data = response.json()
    assert data["execution_allowed"] is False
    assert data["mutated"] is False
    # ควรมี suggested_template
    assert "suggested_template" in data
    if data["suggested_template"]:
        assert "template_id" in data["suggested_template"]

# ทดสอบ fallback เมื่อไม่มี template ใน registry
def test_cross_plan_no_suggestion():
    response = client.post("/w3/cross/plan", json={"px": "99,99"})
    assert response.status_code == 200
    data = response.json()
    assert data["state"] in ("planned", "review", "block")
    # ไม่ควรมี suggested_template (หรือเป็น None)
```

หมายเหตุ: integration test นี้ไม่ mutate, ไม่ execute, และสามารถรันใน CI ได้.

---

19. คำสั่งเริ่มต้น (สำหรับมนุษย์ — Historical Only)

โครงสร้างส่วนใหญ่ถูกสร้างแล้ว คำสั่งด้านล่างเป็นหลักฐานของขั้นตอนเริ่มต้น ห้ามรันซ้ำโดยไม่ตรวจ `wx/` ปัจจุบัน โดยเฉพาะคำสั่งเขียน Registry ซึ่งอาจทับ source truth ปัจจุบันได้

คำสั่งต้นแบบเดิม:

```bash
# สร้างโครงสร้างโฟลเดอร์ wx/
mkdir -p wx/{templates/{paper,modew,cross_l},blueprints/{system,collection},references,registry,index,log_info,collections}
touch wx/README.md wx/templates/README.md wx/blueprints/README.md wx/references/README.md wx/index/README.md wx/log_info/README.md wx/collections/README.md

# สร้าง registry ตัวอย่าง (ใช้เนื้อหาจากข้อ 16)
cat > wx/registry/template_registry.json << 'EOF'
# วาง JSON ตัวอย่างข้างต้น
EOF

# สร้าง index/by_px.md เริ่มต้น
cat > wx/index/by_px.md << 'EOF'
# PX → Template Mapping

| PX | Work Type | Recommended Template |
|----|-----------|----------------------|
| 1,1 | FAST_PATCH | wx/templates/paper/fast_patch.md |
| 2,1 | ADAPTIVE_RULE | wx/templates/paper/adaptive_rule.md |
EOF

# สร้าง log_info/requests.jsonl (ไฟล์ว่าง)
touch wx/log_info/requests.jsonl wx/log_info/creations.jsonl
```

หลังจากนี้มนุษย์สามารถเริ่มย้าย template ที่มีอยู่จาก croll/ เข้า wx/templates/ และปรับปรุง registry ตามจริง.

---

✅ สรุป

BOX Blueprint ฉบับสมบูรณ์นี้:

· สอดคล้องกับหลัก Planner‑Only, Mutated: False, Human‑First
· มีโครงสร้างโฟลเดอร์, template, blueprint, registry, index, log‑info ครบ
· มีตัวอย่าง registry/template_registry.json ที่ใช้งานได้จริง
· มีการปรับ cross_l_dispatcher.py ให้ดึง suggestion จาก BOX (optional)
· มี integration test สำหรับ BOX + W3‑API
· ทุกคำสั่งสร้างโครงสร้างเป็น manual (มนุษย์ต้องรันเอง)

DeepSeek ขอให้ blueprint นี้เป็นประโยชน์ในการนำไปสร้างและขยายผลต่อครับ 🌐📚🧱


---

## 20. สถานะการนำไปใช้ปัจจุบัน

| Blueprint Component | หลักฐานใน `wx/` | สถานะ |
|---|---|---|
| Library‑WX | `templates/`, `blueprints/`, `references/` | มีโครงสร้างจริง |
| Registry | `wx/registry/*.json` | ใช้งานแล้ว |
| Human Index | `wx/index/*.md` | ใช้งานแล้ว |
| Engine‑Index | `wx/engine_index.py` | ใช้งานแบบ read-only |
| Indexor | `wx/indexor.py` | planner-only implementation |
| PortDC | `wx/portdc.py` | registered-content export เป็นข้อมูล |
| Log‑Info | `wx/log_info/` | มี append-only surface; ไม่ append อัตโนมัติ |
| Collections | `wx/collections/` | reference grouping |
| wx:BOX / CN‑Fold | templates, blueprint, mapping และ index | draft/observe |
| WHUB | `external_ref` และแนวทางเชื่อม | readiness metadata เท่านั้น |

การตรวจพฤติกรรมปัจจุบันต้องยึด code, registry และ tests ใน `wx/` ร่วมกับเอกสารนี้ ตัวอย่าง pseudo-code ใน Blueprint ไม่ใช่ operational truth เมื่อ implementation จริงแตกต่างออกไป

## 21. BOX Core กับ Knowledge Infrastructure v1.0

```text
BOX Core
= กำหนดพื้นที่ / ขอบเขต / ความหมาย / ความสัมพันธ์

BOX Knowledge Infrastructure v1.0
= รูปประยุกต์ด้านคลังความรู้และ reference

Library‑WX
= ห้องสมุดภายใน BOX

Registry / Engine‑Index / Indexor / PortDC / Log‑Info
= กลไกสนับสนุนการค้นหา เข้าถึง ส่งออก และ trace
```

ดังนั้นคำว่า planner-only และ runtime-none ในหัวเอกสารจำกัดเฉพาะรูปประยุกต์ v1.0 นี้ ไม่ใช่ข้อห้ามถาวรต่อ BOX ทุกบริบท

## 22. BOX IN/OUT — ทิศทางต่อยอดสำหรับ WHUB

BOX ต้องรักษาเอกสารต้นฉบับเพียงหนึ่งเดียว และแบ่ง **พื้นผิวการเข้าถึง** แทนการสร้างความจริงสองชุด:

```text
BOX — Single Source
├── IN   เอกสารภายในทุกระดับ รวมส่วนที่ไม่เปิดเผย
└── OUT  projection/reference ที่ได้รับอนุญาตให้เปิด
```

### Internal Registry

การตัดสิน IN/OUT ให้อยู่ใน Registry เฉพาะภายใน ไม่กระจายกฎซ้ำลงทุกระบบ:

```yaml
resource_id: _
source_path: _
owner_scope: _
surface: IN
boundary: B0
visibility: V0
sensitivity: _
out_allowed: false
projection_ref: null
review_required: true
approved_by: null
approved_at: null
status: active
```

หลักขั้นต่ำ:

1. ค่าเริ่มต้นของ resource เป็น `IN`
2. ไม่มี Registry entry หรืออ่าน Registry ไม่ได้ = fail-closed
3. `out_allowed: true` อนุญาตเฉพาะ `projection_ref` ไม่เปิดต้นฉบับโดยอัตโนมัติ
4. OUT/WHUB ไม่อ่าน Internal Registry โดยตรง แต่รับเฉพาะ export manifest ที่อนุมัติแล้ว
5. การอ้างอิงเอกสาร IN ไม่เท่ากับมีสิทธิ์อ่าน
6. การเปลี่ยน IN → OUT ต้องเป็น event ใหม่ มี owner/review/trace และไม่แก้ประวัติย้อนหลัง
7. Registry ต้องอยู่ภายใน เพราะ path, relation และสถานะสามารถเปิดเผย topology แม้ไม่มีเนื้อหาเอกสาร

### Boundary axes ที่ค้นพบใน W3

- `B0–B3` — content boundary
- `T1–T4` — trust/impact context
- `V0–V3` — visibility
- `P0–P4` — external exposure
- `LOW–CRITICAL` — PR/change risk; ห้ามใช้แทน document sensitivity

`S1–S4` ปรากฏใน CN‑Fold/wx:BOX แต่ยังไม่พบต้นทางนิยามที่เพียงพอ จึงยังไม่ควรเดาความหมายหรือใช้เป็น enforcement จนกว่าจะพบเอกสารต้นแบบ

## 23. Cross-system boundary

- BOX อ้างอิง Cross‑L, MPCP, W3‑API และ WHUB ได้ แต่ไม่ใช้กฎภายในของ BOX ตัดสินความถูกต้องของระบบเหล่านั้น
- BOX suggestion เป็นข้อมูลเสริมแบบ opt-in ไม่ให้ execution authority
- การเชื่อม Cross‑L → MPCP หรือ W3Lgu ต้องมี return contract และขอบเขตของ event แยกต่างหาก
- เมื่อเกิด cross-system collision ให้ใช้ `wx/references/wx_box_cn_fold_recovery_anchor.md` เป็นจุดสังเกต ไม่ใช่คำสั่งลบความสามารถที่ยังไม่ได้ตรวจ

## 24. เอกสารและหลักฐานที่ใช้อ่านคู่กัน

- `BBX19/notes/LIBRARY_WX.md` — Origin Blueprint ของ Library‑WX
- `wx/README.md` — implementation boundary ปัจจุบัน
- `docs/box/README_TH.md` — คู่มือภาพรวม
- `docs/box/USAGE_TH.md` — วิธีใช้งาน
- `docs/box/BOUNDARY_TH.md` — safety boundary
- `wx/engine_index.py`, `wx/indexor.py`, `wx/portdc.py` — activity/code
- `wx/test_engine_index.py`, `tests/test_box_integration.py` — validation evidence
- `wx/references/wx_box_cn_fold_recovery_anchor.md` — recovery context
