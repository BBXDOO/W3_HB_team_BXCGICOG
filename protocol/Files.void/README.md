Name : File.void — unresolved transmissive concept  
AM Ⅰ - BUILD : แนวคิด File.void ว่าด้วย unresolved transmissive state และการ manifest ชั่วคราวโดยไม่เปลี่ยน source truth; ไม่ใช่ที่เก็บ artifact และไม่อนุญาต final write โดยตัวมันเอง  
Log time : 2026-11-22 (date only; time not recorded) ; ID : FILES-VOID-README-001  
≡ Br2ra - RAMS

## Body — บทบาทและขอบเขต

แนวคิด File.void ว่าด้วย unresolved transmissive state และการ manifest ชั่วคราวโดยไม่เปลี่ยน source truth; ไม่ใช่ที่เก็บ artifact และไม่อนุญาต final write โดยตัวมันเอง

```yaml
AM_TYPE: I
ROLE: CORE_CONCEPT
DERIVED_FROM:
  - protocol/Files.void/File_void.md
DOCUMENT_PATH: protocol/Files.void/README.md
```

**ขอบเขต:** README นี้อธิบายเฉพาะ `protocol/Files.void/` ไม่ขยายสิทธิ์ของระบบอื่นและไม่ยืนยันผลทดสอบที่ไม่ได้มีหลักฐาน

## Movement — การนำทาง

### M1 — รายการในโฟลเดอร์นี้

| รายการ | ประเภท |
|---|---|
| [File_void.md](File_void.md) | เอกสาร |
| [README.md](README.md) | README / AMS |
| [void.runtime.spec.md](void.runtime.spec.md) | เอกสาร |

### M2 — เอกสารอ้างอิงนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [พื้นที่ protocol](../README.md) | พื้นที่ protocol |
| docs.core | [หลักความต่อเนื่องของความหมาย](../../knowledge/philosophy/corevsstructure.md) | หลักความต่อเนื่องของความหมาย |
| docs.runtime | [Python implementation แยกพื้นที่](../files_void/README.md) | Python implementation แยกพื้นที่ |
| docs.mpcp | [ระบบ MPCP](../mpcp/README.md) | ระบบ MPCP |
| docs.ams | [กฎ AMS](../../docs/governance/AMS.md) | กฎ AMS |

---

### บันทึกเนื้อหา README เดิม (รักษาข้อมูลต้นทาง)

# File.void

```txt
┌──────────────────────────────────────────────┐
│ File.void                                    │
├──────────────────────────────────────────────┤
│ [/]                                          │
│ unresolved transmissive state                │
│                                              │
│ env : [File.void + lib]                      │
│                                              │
│ persist  → preserve source continuity        │
│ transfer → runtime transmission              │
│ resolve  → contextual resolution             │
│ manifest → temporary artifact emergence      │
│ return   → restore unresolved state          │
│                                              │
│ [/] : ~ {manifest}                           │
│                                              │
│ env : [File.void + pdf.lib]                  │
│ → temporary PDF manifestation                │
│ → source remains unresolved                  │
│                                              │
│ :/ SAVE → persist manifestation externally   │
│ :/ COPY → duplicate manifestation state      │
│                                              │
│ File.void does not store artifacts.          │
│ It preserves the ability for form to emerge. │
└──────────────────────────────────────────────┘
```

## Runtime package

Concept docs stay in `protocol/Files.void/` because `File.void` is the W3 concept name.
The importable Python tool lives in `protocol/files_void/`.

```python
from protocol.files_void import file_void_tool

result = file_void_tool(
    action="manifest",
    source_ref="BOX:CROSS_L_BLOCK",
    source_body="return {state='pass'}",
    env="lua.env",
    lib="lua.lib",
    artifact_type="lua",
    mpcp_task="manifest_cross_code",
)
```

## MPCP / Blueprint adapter

MPCP or Blueprint-style contexts can call File.void through:

```python
from protocol.mpcp.adapter.file_void_tool import call_file_void_tool, build_file_void_operation
```

- `call_file_void_tool(context)` accepts KEY:VALUE-style context dictionaries.
- `build_file_void_operation(action)` returns an operation callback compatible with `protocol.mpcp.lib.Pillar`.

## Boundary contract

- File.void is a staging / manifestation layer only.
- File.void may manifest, copy, release, or create a persistence handoff record.
- File.void must not write final storage directly.
- `:/ SAVE` means `persist_handoff`, not direct write.
- `[/] != artifact` remains an invariant.
- Source truth must remain unchanged.

---

OWNER : BBX19 — เจ้าของแนวคิด/ระบบตามข้อมูลต้นทาง  
MAKER : ChatGPT / Codex — ปรับ README ให้สอดคล้อง AMS โดยรักษาเนื้อหาเดิม
