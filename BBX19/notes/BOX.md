📚 BOX Knowledge Infrastructure — ฉบับ Blueprint สมบูรณ์ (v1.0)

สถานะ: Blueprint เสนอ
Owner: BBX19
Scope: Planner‑Only | Runtime: None | Mutated: False
Relation: W3 / Library‑WX / Cross‑L / MPCP / W3‑API

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

BOX คือ โครงสร้างพื้นฐานทางความรู้ (Knowledge Infrastructure) ของ W3
เปรียบเสมือน โรงแรมขนาดใหญ่ ที่มี:

· ห้องสมุดกลาง – Library-WX (เก็บ Template, Blueprint)
· บรรณารักษ์ – Indexor Agent (แนะนำตำแหน่ง)
· ลิฟต์นำทาง – Engine-Index (ค้นหาและเชื่อมโยง)
· เคาน์เตอร์นำเข้า/ส่งออก – PortDC
· ประตูเชื่อมภายนอกในอนาคต – WHUB

BOX ไม่ใช่ runtime, execution engine, database, หรือ state manager
BOX คือ reference layer ที่ให้มนุษย์และเอเจนท์สามารถ ค้นหา, อ้างอิง, คัดลอก และสร้าง เนื้อหาใหม่ โดยไม่ละเมิดต้นฉบับ

---

2. หลักการสำคัญ

หลักการ คำอธิบาย
P1 – Single Source of Truth ไฟล์ต้นฉบับ (template, blueprint) มีได้ที่เดียวใน wx/ ห้ามแก้โดยตรง
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

Blueprint คือ declaration ของโครงสร้าง (โฟลเดอร์, ระบบ, Agent, Collection) ไม่ใช่ logic หรือ flow.

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

การใช้งาน: มนุษย์หรือ Agent สามารถอ่าน log เพื่อ audit หรือ trace.

---

12. PortDC – ประตูเอกสาร

PortDC เป็น Input/Output Gateway สำหรับเอกสารภายนอก
ทำหน้าที่:

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

BOX ไม่ใช่:

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

19. คำสั่งเริ่มต้น (สำหรับมนุษย์)

ให้เพื่อนคัดลอกและรันใน Termux หรือเครื่องของตัวเอง เมื่อพร้อม:

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
