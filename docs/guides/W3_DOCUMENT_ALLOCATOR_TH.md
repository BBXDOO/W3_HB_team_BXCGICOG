---
AM_TYPE: III
ROLE: OPERATIONAL
GROUP: BUILD
DERIVED_FROM:
  - docs/governance/AMS.md
  - docs/box/README_TH.md
  - docs/box/BOUNDARY_TH.md
  - docs/box/AMS/Group_4.md
OWNER: BBX19
MAKER: Codex
STATUS: draft
REQUEST_ID: W3-DOCUMENT-ALLOCATOR-MFC
---

# W3 Document Allocator — คู่มือขั้นต่ำ

## Head line

1. Name: W3 Document Allocator
2. AM III - BUILD: Operational Tool
3. ID: W3-DOCUMENT-ALLOCATOR-MFC
4. Note: เครื่องมือสร้างเอกสาร AMS โดยรักษาขอบเขต BOX

## Body line

เครื่องมือนี้ตรวจ AM Type, lineage, พาธ, เอกสารชื่อซ้ำ และ BOX reference ก่อนสร้าง Markdown จากนั้นคืน artifact receipt ที่มีพาธ digest และหลักฐานผู้อนุญาต

BOX ยังคงเป็น `planner-only`: การพบ template หรือ reference ไม่ได้ให้สิทธิเขียนไฟล์ การเขียนจริงต้องใช้ `--mode create|update` พร้อม `--authorized-by`

### โหมด

- `dry-run` — ตรวจและแสดงแผน ไม่เขียนไฟล์
- `create` — สร้างไฟล์ใหม่ ห้ามทับไฟล์เดิม
- `update` — ปรับไฟล์เดิมเมื่อ `--expected-sha256` ตรงกับฉบับปัจจุบัน

### ตัวอย่างตรวจแผน

```bash
python tools/w3_document_allocator.py \
  --title "คู่มือ Markdown ภาษาไทย" \
  --target BBX19/notes/THAI_MARKDOWN_GUIDE.md \
  --am-type II \
  --group LEARN \
  --owner Copilot-Gm \
  --maker Copilot-Gm \
  --body-file /tmp/markdown-guide-body.md \
  --derived-from docs/governance/AMS.md \
  --request-id RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001 \
  --mode dry-run
```

เมื่อแผนผ่านและมีผู้อนุญาต จึงเปลี่ยนเป็น:

```bash
  --mode create --authorized-by BBX19
```

### Boundary

- ไม่สร้างเนื้อหาแทนโมดูลเจ้าของงาน
- ไม่ตีความ BOX suggestion ว่าเป็น write authority
- ไม่เขียน `wx/templates/`, `wx/blueprints/`, `wx/references/` หรือ `wx/registry/`
- ไม่รับ absolute path หรือ `..`
- ไม่ทับไฟล์เดิมในโหมด create
- การ update ต้องใช้ digest ปัจจุบัน
- ผลลัพธ์ทุกครั้งยังมี `review: true`

### Orchestration

`make_orchestration_handler()` สร้าง handler สำหรับ `orchestration.assist()` ได้ แต่ Orchestration ต้องบันทึก blocker ก่อน และต้องส่งสิทธิผู้อนุญาตเข้ามาอย่างชัดเจน

## Movement line

- [AMS](../governance/AMS.md)
- [BOX overview](../box/README_TH.md)
- [BOX boundary](../box/BOUNDARY_TH.md)
- [AMS Group 4](../box/AMS/Group_4.md)
- Tool: `tools/w3_document_allocator.py`
- Tests: `tests/test_w3_document_allocator.py`

## Owner line

- Owner: BBX19
- Maker: Codex
- Log: draft MFC; human review required

