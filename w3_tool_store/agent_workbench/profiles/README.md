Name : Agent Workbench — Profiles\
AM Ⅱ - BUILD : การประยุกต์เครื่องมือให้เข้ากับระบบเฉพาะ\
Log time : 2026-10-24 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : W3-AWB-PROFILES-README-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาทของพื้นที่

โฟลเดอร์นี้รองรับข้อกำหนดการใช้เครื่องมือกับระบบเฉพาะ เช่น MPCP และ W3Lgu โดยอ้างกติกาต้นทางของระบบนั้น และแยกจากโค้ดเครื่องมือที่ใช้ร่วมกัน

**สถานะ: มี OPPO Android probe สำหรับ local Blueprint + File.void แล้ว ดูผลและข้อจำกัดใน README ย่อย เป็นการสร้างโครงและเอกสาร ไม่ใช่การรัน APK หรือจำลอง OPPO/ColorOS**

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md
  - w3_tool_store/agent_workbench/README.md
```

เมื่อเพิ่ม profile ให้บอกระบบเป้าหมาย ต้นทางกติกา เครื่องมือที่ใช้ input/output ขอบเขตสิทธิ์ ข้อมูลแวดล้อมที่ต้องมี วิธีตรวจผล และสิ่งที่ยังไม่รองรับ ไม่ใช้ profile แทนสิทธิ์อนุมัติของผู้ใช้หรือกติกาของระบบเป้าหมาย

profile ที่มีเพียงแผนหรือเอกสารต้องระบุสถานะนั้น การเชื่อมใช้งานได้ต้องมีหลักฐานจากการรันและข้อจำกัดให้ตรวจสอบ

## Movement — การนำทางในพื้นที่

### M1 — สิ่งที่มีอยู่ในโฟลเดอร์นี้

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | ขอบเขตของพื้นที่ profiles |
| [oppo_android_probe/](oppo_android_probe/README.md) | local Blueprint + File.void; มี [ผลทดลอง 2026-10-27](oppo_android_probe/RESULT_2026-10-27.md) แยกจากการทดสอบเครื่องจริง |

### M2 — เอกสารอ้างอิงนอกพื้นที่

- docs.parent : [Agent Workbench](../README.md)
- docs.core : [Core vs Structure](../../../knowledge/philosophy/corevsstructure.md)
- docs.mpcp : [MPCP](../../../protocol/mpcp/README.md)
- docs.w3lgu : [W3Lgu](../../../protocol/w3lgu/README.md)
- docs.sandbox : [ขอบเขต MPCP sandbox ปัจจุบัน](../../../tools/agent_sandbox/README.md)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex
