Name : Agent Workbench — Tools\
AM Ⅱ - BUILD : การจัดพื้นที่สำหรับโครงการเครื่องมือที่พัฒนาแยก\
Log time : 2026-10-24 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : W3-AWB-TOOLS-README-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาทของพื้นที่

โฟลเดอร์นี้รองรับโครงการเครื่องมือที่เอเจนท์ใช้ทำงาน โดยแยกแต่ละเครื่องมือออกจาก prototype ต้นทางและจากข้อมูลของผู้ใช้เครื่องมือ

**สถานะ: มีเอกสารกำหนดพื้นที่ ยังไม่มีโค้ดเครื่องมือหรือสำเนาจาก xrea ในโฟลเดอร์นี้**

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md
  - w3_tool_store/agent_workbench/README.md
```

เมื่อเพิ่มเครื่องมือ ให้สร้างโฟลเดอร์ของเครื่องมือนั้นพร้อม README แบบ AMS อธิบายหน้าที่ วิธีเรียก ข้อมูลเข้า/ออก dependency ผลกระทบ วิธีตรวจผล และสถานะที่มีหลักฐานจริง README ของโค้ดหรือกระบวนการปฏิบัติงานให้ระบุ AM:III ตามเนื้อหา

หากคัดลอกโค้ดจาก xrea ให้เก็บที่มา เวอร์ชันหรือ commit รายการที่คัดลอก การปรับแก้ และ license/copyright notice ไว้กับเครื่องมือปลายทาง การเป็นเจ้าของโครงการ W3 ไม่ได้เปลี่ยนผู้พัฒนาต้นฉบับ

## Movement — การนำทางในพื้นที่

### M1 — สิ่งที่มีอยู่ในโฟลเดอร์นี้

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | ขอบเขตของพื้นที่ tools; ยังไม่มีโครงการเครื่องมือย่อย |

### M2 — เอกสารอ้างอิงนอกพื้นที่

- docs.parent : [Agent Workbench](../README.md)
- docs.core : [Core vs Structure](../../../knowledge/philosophy/corevsstructure.md)
- docs.prototype : [xrea](../../xrea/README.md)
- docs.sandbox : [คู่มือ MPCP sandbox ที่อยู่ในพาธเดิม](../../../tools/agent_sandbox/README.md)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex
