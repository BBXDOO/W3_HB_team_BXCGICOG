# BOX / Library-WX — วิธีใช้งานภาษาไทย

คู่มือนี้อธิบายการค้นหา อ้างอิง คัดลอก และลงทะเบียน template โดยรักษาหลัก
planner-only และ copy-before-use

## 1. สิ่งที่ต้องมี

- Python 3.9 ขึ้นไป
- เปิดคำสั่งจาก root ของ repository สำหรับตัวอย่าง CLI
- ไม่ต้องติดตั้ง dependency เพิ่มสำหรับ Engine-Index และ CROLL unit tests
- หากทดสอบ W3-API ให้ติดตั้ง `requirements.txt`

```bash
python --version
python tools/check_portable_paths.py
```

## 2. ดูรายการที่มีอยู่

### 2.1 สำหรับมนุษย์

เปิดไฟล์เหล่านี้:

- `wx/index/by_px.md` — ค้นจาก PX
- `wx/index/by_work_type.md` — ค้นจากประเภทงาน
- `wx/index/by_agent_role.md` — ค้นจากบทบาท agent
- `wx/registry/template_registry.json` — metadata ต้นทางที่ระบบใช้

### 2.2 ด้วย Python

```bash
python - <<'PY'
from wx.engine_index import search_by_px

item = search_by_px("PX:[1,1]")
print(item)
PY
```

ฟังก์ชันค้นหาหลัก:

```python
from wx.engine_index import (
    find_templates,
    search_by_px,
    search_by_rytm,
    search_by_work_type,
)

search_by_px("1,1")
search_by_work_type("FAST_PATCH")
search_by_rytm("ROCK")
find_templates(px="1,1", work_type="FAST_PATCH", rytm="ROCK")
```

ผลลัพธ์เป็น metadata สำเนาในหน่วยความจำ การแก้ dictionary ที่ได้จะไม่แก้ registry บนดิสก์

## 3. ขอคำแนะนำจาก Indexor

```bash
python - <<'PY'
from pprint import pprint
from wx.indexor import suggest_references

pprint(suggest_references(px="2,1"))
PY
```

ค่าความปลอดภัยสำคัญในผลลัพธ์:

```json
{
  "planner_only": true,
  "execution_allowed": false,
  "mutated": false,
  "copy_allowed_by_runtime": false,
  "human_review_required": true
}
```

Indexor จะแนะนำตำแหน่งเท่านั้น ไม่คัดลอกไฟล์ให้

## 4. ใช้ BOX ร่วมกับ CROLL

### 4.1 พฤติกรรมเดิม — ไม่เรียก BOX

```bash
python -m croll --compact plan "PX:[1,1]"
```

response จะไม่มี `suggested_template`

### 4.2 เปิด suggestion อย่างชัดเจน

```bash
python -m croll --compact plan "PX:[1,1]" --box-suggestion
```

ตัวอย่างส่วนที่เพิ่ม:

```json
{
  "suggested_template": {
    "template_id": "PAPER:FAST_PATCH_V1",
    "path": "wx/templates/paper/fast_patch.md",
    "reference_only": true
  }
}
```

ไม่ว่ามี suggestion หรือไม่ CROLL ยังคงต้องคืน:

```json
{
  "execution_allowed": false,
  "mutated": false,
  "review": true
}
```

## 5. ใช้ BOX ผ่าน W3-API

endpoint เดิมใช้ได้เหมือนเดิม:

```http
POST /w3/cross/plan
Content-Type: application/json
```

### 5.1 ไม่ขอ BOX suggestion

```json
{
  "px": "1,1"
}
```

### 5.2 ขอ BOX suggestion

```json
{
  "px": "1,1",
  "include_box_suggestion": true
}
```

ตัวอย่างทดสอบในเครื่อง:

```bash
python -m pip install -r requirements.txt
python -m pytest \
  tests/test_box_integration.py \
  tests/test_w3_api_cross_plan.py \
  tests/test_cross_x_config.py -q
```

## 6. อ่าน template ผ่าน PortDC

PortDC คืน source เป็นข้อมูล แต่ไม่สร้างไฟล์ปลายทาง:

```bash
python - <<'PY'
from wx.portdc import export_registered_template

result = export_registered_template("PAPER:FAST_PATCH_V1")
print(result["source_path"])
print(result["human_copy_required"])
print(result["content"][:120])
PY
```

ค่าที่ต้องคงไว้:

- `execution_allowed: false`
- `mutated: false`
- `write_performed: false`
- `human_copy_required: true`

## 7. คัดลอก template ไปใช้งาน

BOX ไม่ทำขั้นตอนนี้แทนผู้ใช้ ให้มนุษย์หรือเครื่องมือที่ได้รับอนุมัติคัดลอกเอง เช่น:

```bash
mkdir -p codex/work
cp wx/templates/paper/fast_patch.md codex/work/fast_patch_001.md
```

หลังคัดลอก:

1. แก้เฉพาะไฟล์ใน workspace
2. คง `template_id` เดิมไว้เป็น reference/provenance
3. เพิ่มข้อมูลของงาน เช่น requester, purpose หรือ source path ในสำเนา
4. ตรวจ diff ก่อน commit
5. ขอ human review ตาม boundary ของงาน

> ตำแหน่ง workspace เป็นตัวอย่าง ผู้ใช้ต้องเลือกพื้นที่ที่สอดคล้องกับ agent และ governance จริง

## 8. บันทึก Log-Info แบบ manual

BOX runtime ไม่เขียน log เอง หาก governance อนุญาต ให้ append JSON หนึ่งบรรทัดด้วยเครื่องมือที่
ผู้ใช้ควบคุม เช่น:

```bash
python - <<'PY'
import json
from pathlib import Path

record = {
    "timestamp": "2026-06-12T10:00:00Z",
    "requester": "Codex",
    "action": "copy_template",
    "template_id": "PAPER:FAST_PATCH_V1",
    "target_path": "codex/work/fast_patch_001.md",
    "purpose": "PX:1,1 reviewed patch plan",
}

with Path("wx/log_info/creations.jsonl").open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
PY
```

กติกา:

- append เท่านั้น ไม่แก้บรรทัดเก่า
- บันทึก `create`, `generate`, `borrow`, `export`
- การอ่านหรือศึกษาไม่จำเป็นต้องบันทึก
- ห้ามใส่ token, password, patient data หรือข้อมูลลับลง log

## 9. เพิ่ม template ใหม่อย่างถูกต้อง

### ขั้นที่ 1 — สร้างไฟล์ต้นฉบับ

ตัวอย่าง `wx/templates/paper/new_paper.md`:

```markdown
---
template_id: PAPER:NEW_PAPER_V1
version: 1.0.0
scope: CROSS_L_ONLY
boundary: observe
deny: truth_mutation, direct_merge
owner: BBX19
status: draft
created_at: 2026-06-12
---

# New Paper
```

### ขั้นที่ 2 — เพิ่ม registry entry

เพิ่ม object ใน `wx/registry/template_registry.json` โดยให้ metadata ต่อไปนี้ตรงกับ front matter:

- `template_id`
- `version`
- `owner`
- `status`
- `boundary`

path ต้อง:

- เป็น repository-relative path
- อยู่ภายใน repository
- ชี้ไปยังไฟล์ที่มีอยู่จริง
- ไม่มี `..` หรือ absolute path

### ขั้นที่ 3 — ปรับ human index

อัปเดตอย่างน้อยหนึ่งไฟล์ตามลักษณะงาน:

- `wx/index/by_px.md`
- `wx/index/by_work_type.md`
- `wx/index/by_agent_role.md`

### ขั้นที่ 4 — ตรวจสอบ

```bash
python -m unittest discover -s wx -p "test_*.py" -v
python tools/check_portable_paths.py
python -m croll --compact plan "PX:[1,1]" --box-suggestion
```

## 10. การแก้ไข template ต้นฉบับ

กฎ “ห้ามแก้โดยตรง” หมายถึง **ห้ามแก้ต้นฉบับเพื่อทำงาน instance หนึ่ง** การบำรุงรักษา
Library-WX ยังทำได้ แต่ต้องเป็นการเปลี่ยนแปลงที่ตั้งใจและผ่าน review:

1. เปลี่ยน version เมื่อ contract/โครงสร้างเปลี่ยน
2. อัปเดต registry ให้ตรงกับ front matter
3. รักษา ID เดิมเมื่อ backward-compatible
4. สร้าง ID/version ใหม่เมื่อการเปลี่ยนแปลงทำลาย compatibility
5. ไม่แก้สำเนางานเก่าให้ชี้ความหมายใหม่ย้อนหลัง

## 11. การแก้ปัญหาเบื้องต้น

### `registered BOX source does not exist`

ตรวจ `path` ใน registry ว่าตรงกับชื่อไฟล์จริงและ case ถูกต้อง

### `path must be repository-relative`

ห้ามใช้ `/absolute/path`, drive letter หรือ `../`

### `front matter ... does not match`

ตรวจ `template_id`, `version`, `owner`, `status`, `boundary` ระหว่างไฟล์กับ registry

### ไม่พบ suggestion

- ตรวจ PX format เช่น `1,1` หรือ `PX:[1,1]`
- ตรวจว่า entry มี `status: active`
- ตรวจว่า PX อยู่ใน array `px`
- PX ที่ไม่รู้จักจะคืน review plan และ suggestion เป็น `null`/ไม่มีค่า
