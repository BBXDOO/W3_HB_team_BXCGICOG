Name : W3DB — World 3 Database (protocol interface and tests)  
AM Ⅲ - BUILD : โค้ดและการทดสอบ W3DB ในพื้นที่ protocol  
Log time : 2026-11-22 (date only; time not recorded) ; ID : W3DB-README-001  
≡ Cr1ra - RAMS

## Body — บทบาทและขอบเขต

`protocol/w3db/` เป็นพื้นที่ไฟล์ประกอบและการทดสอบ W3DB ในระบบ W3 ตามเอกสาร [W3DB_MANAUL.md](W3DB_MANAUL.md) ซึ่งอธิบาย World 3 Database สำหรับ log, state, perception, law และ relation flow

เอกสารคู่มือระบุส่วนประกอบ **XIZ** (action log), **TUF** (state snapshot), **FBD** (failure/risk), **WHB** (law/context) และ **PRX** (perception output) รวมถึงการเรียกใช้ `src.w3db` และตัวอย่าง CRUD/flow ข้อความเหล่านี้เป็นข้อกำหนดจากคู่มือ ไม่ใช่หลักฐานยืนยันผลรันล่าสุด

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/w3db/W3DB_MANAUL.md
  - protocol/README.md
  - knowledge/philosophy/corevsstructure.md
DOCUMENT_ID: W3DB-README-001
DOCUMENT_PATH: protocol/w3db/README.md
```

### สิ่งที่รักษาและขอบเขต

- **Preserve:** นิยาม XIZ/TUF/FBD/WHB/PRX และตัวอย่างการใช้งานจากคู่มือ W3DB
- **Adapt:** เพิ่มแผนที่ไฟล์และเส้นทางอ้างอิงเพื่อให้ตรวจสอบการทำงานต่อได้
- **Do not redefine:** ไม่เปลี่ยน data model, สิทธิ์การแก้ไข, immutable policy หรือ semantics ของระบบต้นทาง
- **Verification:** `test_crud.py` และ `test_flow.py` เป็นไฟล์ทดสอบที่มีอยู่ แต่ README นี้ไม่ได้อ้างว่าทดสอบผ่าน; ตัวอย่าง import แบบ `SYSTEM.TESTS.EP_SIGNAL` ในคู่มือควรตรวจสอบกับโครงสร้างปัจจุบันก่อนนำไปรัน

## Movement — การนำทาง

### M1 — รายการในโฟลเดอร์นี้

| รายการ | บทบาท |
|---|---|
| [README.md](README.md) | ขอบเขตและแผนที่ AMS ของพื้นที่นี้ |
| [W3DB_MANAUL.md](W3DB_MANAUL.md) | คู่มือภาษาไทย นิยามองค์ประกอบและตัวอย่างการใช้ W3DB |
| [__init__.py](__init__.py) | Python package initializer |
| [test_crud.py](test_crud.py) | โค้ดทดสอบ CRUD |
| [test_flow.py](test_flow.py) | โค้ดทดสอบ relation flow |

### M2 — เอกสารอ้างอิงนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [Protocol](../README.md) | ขอบเขตของกลุ่ม protocol |
| docs.core | [Core vs Structure](../../knowledge/philosophy/corevsstructure.md) | หลักการรักษาความหมาย |
| docs.ams | [Architecture Mapping Standard](../../docs/governance/AMS.md) | กฎ AM Type และ Gradation |
| docs.ep | [EP_SIGNAL](../EP_SIGNAL/README.md) | ระบบสัญญาณที่คู่มือยกตัวอย่างการเชื่อมต่อ |
| docs.mpcp | [MPCP](../mpcp/README.md) | ระบบที่เกี่ยวข้องในกลุ่ม protocol |

---

OWNER : BBX19 — เจ้าของระบบ W3 ตามเอกสารระดับ protocol  
MAKER : ChatGPT / Codex — สร้าง README ใหม่จากคู่มือและรายการไฟล์จริงตาม AMS
