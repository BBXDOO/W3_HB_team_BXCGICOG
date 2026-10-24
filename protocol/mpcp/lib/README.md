Name : MPCP Library — รายการและอุปกรณ์ที่เรียกใช้ได้\
AM Ⅲ - BUILD : ตัวเชื่อม runtime และอุปกรณ์ภายใต้กรอบ MPCP\
Log time : 2026-10-24 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : MPCP-LIB-README-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาทและขอบเขต

Library รับใช้ MPCP โดยไม่กำหนด grammar เลือกผู้ทำ หรืออนุมัติ execution แทนระบบ กฎ core/bridge/optional เดิมยังเป็นต้นทางการจัดกลุ่ม รุ่นนี้เริ่มเพิ่มอุปกรณ์ที่ใช้งานได้จากของที่มีอยู่ก่อน

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/mpcp/mpcp_lib_paper/mpcp_lib_paper.md
  - protocol/mpcp/MPCP_ORIGIN.md
```

`LibraryRegistry` แยกหลักฐานสามแบบ:

| ทางเรียก | ความหมาย |
|---|---|
| `library_group()` | ชื่อความสามารถที่ประกาศใน config ไม่รับรองว่ามี implementation ทุกชื่อ |
| `resolve_language()` | พบ executable ที่เรียกได้ใน ENV หรือรู้จัก data format ไม่รับรองว่า workflow สำเร็จ |
| `equipment_report()` | มี builder ที่ host ลงทะเบียน พร้อมกลุ่มและขอบเขตที่ประกาศ ยังต้องรันและตรวจผลจริง |

Host ใช้ `register_equipment()` ลงทะเบียน builder ของอุปกรณ์ แล้ว `activate_equipment()` เชื่อมเข้าตัว executor โดยยังไม่สร้างหรือรัน Modew การขอชื่ออุปกรณ์ที่ไม่มีจะหยุดก่อนลงทะเบียนชุดนั้น และไม่เขียนทับ route ที่ host อื่นลงทะเบียนไว้

CLI Paper ลงทะเบียนอุปกรณ์จริงสองแบบ:

- `file-void-text`: template → File.void → external text writer; รองรับ Markdown/ข้อความตามขอบเขตเดิม
- `condien-view`: อ่านเฉพาะบริบทที่ Paper/ENV กรองแล้ว ไม่โหลดฐานข้อมูลทั้งก้อนเข้า Modew

อุปกรณ์จัดเก็บ Condien ใช้ `CondienStore` ผ่าน trusted host tool แยกการจัดเก็บเต็มจาก scoped runtime reads ผลของ Modew ยังคงคืนรูป MPCP และผ่าน host verifier เดิม การมี builder ในทะเบียนไม่สร้างสิทธิ์ข้าม ROT/Paper

ยังไม่ได้เติม core/bridge/optional ทั้งรายการ ไม่มีการดาวน์โหลด/ติดตั้ง lib อัตโนมัติ และยังไม่ทำ environment builder สำหรับทุกแพลตฟอร์ม `CONDIEN_LIBS` ใน Event Template เป็นคำขอเชิงหน้าที่ ไม่ถูกเดาให้ตรงกับอุปกรณ์โดยอัตโนมัติ

## Movement — การนำทาง

### M1 — สิ่งที่มีใน lib/

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | ขอบเขตและทางใช้งาน Library |
| [registry.py](registry.py) | กลุ่ม lib, runtime binding และ host equipment registration |
| [pillar.py](pillar.py) | โครง Pillar และ named operations |
| [__init__.py](__init__.py) | exports เดิม |

### M2 — เอกสารและอุปกรณ์ที่สัมพันธ์กัน

- docs.origin : [Library Paper](../mpcp_lib_paper/mpcp_lib_paper.md)
- docs.paper-runtime : [Paper Runtime](../runtime/README.md)
- docs.condien : [Condien และ storage equipment](../../../src/core/README.md)
- docs.text : [File.void text Modew](../modew/file_artifact.py)
- docs.context : [Condien scoped view Modew](../modew/condien_view.py)
- docs.tests : [Equipment/storage tests](../../../tests/test_mpcp_condien_equipment.py)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex
