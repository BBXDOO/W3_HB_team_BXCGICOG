Name : MPCP Adapters  
AM Ⅲ - BUILD : ตัวเชื่อม MPCP กับ File.void, W3 executor และ W3DB; แต่ละ bridge มีขอบเขตต่างกัน: File.void ไม่เขียนไฟล์ขั้นสุดท้าย, W3 bridge ต้องรับ executor จาก host และ W3DB bridge สร้าง append candidate โดยไม่เขียนจริง  
Log time : 2026-11-22 (date only; time not recorded) ; ID : MPCP-ADAPTER-README-001  
≡ Dr1ra - RAMS

## Body — ตัวตนของพื้นที่และขอบเขต

`protocol/mpcp/adapter/` — ตัวเชื่อม MPCP กับ File.void, W3 executor และ W3DB; แต่ละ bridge มีขอบเขตต่างกัน: File.void ไม่เขียนไฟล์ขั้นสุดท้าย, W3 bridge ต้องรับ executor จาก host และ W3DB bridge สร้าง append candidate โดยไม่เขียนจริง

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/mpcp/MPCP_ORIGIN.md
  - protocol/mpcp/adapter/file_void_tool.py
DOCUMENT_PATH: protocol/mpcp/adapter/README.md
```

### หลักการอ่านและสิ่งที่ห้ามสับสน

- **ต้นทาง:** [file_void_tool.py](file_void_tool.py) เป็นแหล่งตรวจสอบข้อกำหนดหรือพฤติกรรมของพื้นที่นี้; การอธิบาย README ไม่แก้เนื้อหาต้นทาง
- **ขอบเขต:** การมีเอกสารหรือโค้ดไม่เท่ากับการอนุมัติ execution, deployment, persistence หรือการรับรองผลทดสอบ
- **การพิสูจน์:** แยก design claim ออกจาก implementation และ test evidence เสมอ; ให้ตรวจผลทดสอบเฉพาะชุดที่เกี่ยวข้องก่อนสรุปสถานะ
- **ความต่อเนื่อง:** รักษาความต่างระหว่าง Structure, Meaning, Paper, ROT และ Runtime ตามกติกาของ MPCP ไม่ให้ README นี้นิยามระบบอื่นแทนเจ้าของ

## Movement — แผนที่และเส้นทางอ้างอิง

### M1 — รายการภายใน `adapter/`

| รายการ | บทบาท |
|---|---|
| [README.md](README.md) | AMS README ของพื้นที่ |
| [__init__.py](__init__.py) | Python module / implementation |
| [file_void_tool.py](file_void_tool.py) | เอกสาร/โค้ดต้นทางหลัก |
| [w3_bridge.py](w3_bridge.py) | Python module / implementation |
| [w3db.py](w3db.py) | Python module / implementation |

### M2 — เอกสารภายนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [MPCP README](../README.md) | แผนที่ระบบแม่ |
| docs.origin | [MPCP Origin](../MPCP_ORIGIN.md) | ความหมายต้นทาง |
| docs.related | [เอกสาร/ระบบที่สัมพันธ์](../../files_void/README.md) | จุดตรวจสอบความสัมพันธ์โดยไม่รวม authority |
| docs.core | [Core vs Structure](../../../knowledge/philosophy/corevsstructure.md) | หลักรักษาความหมาย |
| docs.ams | [AMS Governance](../../../docs/governance/AMS.md) | กฎ AM และ Gradation |

---

OWNER : BBX19 — เจ้าของระบบ MPCP ตามเอกสารต้นทาง  
MAKER : ChatGPT / Codex — สร้างแผนที่ README ตาม AMS จากเอกสารและรายการไฟล์
