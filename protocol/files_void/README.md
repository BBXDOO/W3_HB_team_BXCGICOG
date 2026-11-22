Name : protocol.files_void — Python staging package  
AM Ⅲ - BUILD : Python package สำหรับ create, resolve, manifest, copy, persist_handoff และ release ของ File.void; ไม่เขียน artifact ขั้นสุดท้าย ไม่แก้ source truth และไม่อนุมัติ persistence  
Log time : 2026-11-22 (date only; time not recorded) ; ID : FILES_VOID-README-001  
≡ Br1ra - RAMS

## Body — บทบาทและขอบเขต

Python package สำหรับ create, resolve, manifest, copy, persist_handoff และ release ของ File.void; ไม่เขียน artifact ขั้นสุดท้าย ไม่แก้ source truth และไม่อนุมัติ persistence

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/Files.void/README.md
DOCUMENT_PATH: protocol/files_void/README.md
```

**ขอบเขต:** README นี้อธิบายเฉพาะ `protocol/files_void/` ไม่ขยายสิทธิ์ของระบบอื่นและไม่ยืนยันผลทดสอบที่ไม่ได้มีหลักฐาน

## Movement — การนำทาง

### M1 — รายการในโฟลเดอร์นี้

| รายการ | ประเภท |
|---|---|
| [README.md](README.md) | README / AMS |
| [__init__.py](__init__.py) | Python source / test |
| [core.py](core.py) | Python source / test |
| [tool.py](tool.py) | Python source / test |

### M2 — เอกสารอ้างอิงนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [พื้นที่ protocol](../README.md) | พื้นที่ protocol |
| docs.concept | [แนวคิดต้นทาง](../Files.void/README.md) | แนวคิดต้นทาง |
| docs.mpcp | [MPCP integration](../mpcp/README.md) | MPCP integration |
| docs.ams | [กฎ AMS](../../docs/governance/AMS.md) | กฎ AMS |

---

### บันทึกเนื้อหา README เดิม (รักษาข้อมูลต้นทาง)

# protocol.files_void

Importable runtime/tool package for the W3 `File.void` concept.

Concept documents remain in `protocol/Files.void/`.
Python code lives here because dotted directory names are not importable as normal packages.

## Role

`protocol.files_void` is a bounded staging layer:

- create an unresolved File.void record
- resolve it against an ENV/lib pair
- manifest a temporary artifact representation
- copy active manifestation state
- create a persistence handoff record
- release the manifestation

It does **not** write final artifacts, mutate source truth, or approve persistence.

## Tool call

```python
from protocol.files_void import file_void_tool

result = file_void_tool(
    action="manifest",
    source_ref="BOX:CROSS_L_BLOCK",
    source_body="return {state='pass'}",
    artifact_type="lua",
    env="lua.env",
    lib="lua.lib",
    mpcp_task="manifest_cross_code",
)
```

## MPCP adapter

```python
from protocol.mpcp.adapter.file_void_tool import call_file_void_tool

result = call_file_void_tool({
    "TASK": "manifest_cross_code",
    "ACTION": "manifest",
    "SOURCE_REF": "BOX:CROSS_L_BLOCK",
    "SOURCE_BODY": "return {state='pass'}",
    "ARTIFACT_TYPE": "lua",
})
```

---

OWNER : BBX19 — เจ้าของแนวคิด/ระบบตามข้อมูลต้นทาง  
MAKER : ChatGPT / Codex — ปรับ README ให้สอดคล้อง AMS โดยรักษาเนื้อหาเดิม
