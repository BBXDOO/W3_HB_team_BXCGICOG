# Cast — Deep Reasoning / Structural Adaptation / Decision Support

## Overview

Cast เป็นโมดูลที่ทำหน้าที่ตีความและจัดสร้างเอกสารภายในระบบ W3

- **Role:** Deep Reasoning / Structural Adaptation / Decision Support
- **Status:** partial-active (IDP v2)
- **Reports to:** BBX19

---

## Responsibilities

1. **Interpretation** — รับข้อมูลดิบจากโมดูลอื่น แล้วตีความให้ชัดเจนและใช้งานได้
2. **Document Architecture** — ออกแบบและสร้างโครงสร้างเอกสารที่สอดคล้องกับมาตรฐาน W3
3. **Formatting & Standardization** — แปลง output ให้อยู่ในรูปแบบที่โมดูลอื่นรับได้

---

## Directory Structure

```
Cast/
 ├── ENTRANCE.md
 ├── README.md
 ├── self-review.md
 ├── idp/
 │    └── Cast.idp.json
 ├── modules/
 ├── notes/
 ├── artifacts/
 └── tasks/
```

---

## Integration

- รับ directive จาก **BBX19**
- ส่งผล (interpreted output / documents) ให้โมดูลที่เกี่ยวข้อง

## Runtime ที่ใช้ได้และขอบเขต

`structural_inspect`, `structural_adapt`, `capability_learn` รับ
`payload.source_paths` เป็นรายการไฟล์ UTF-8 ภายในขอบเขตอ่านของ manifest
และพื้นที่ Cast เอง ตัว host เลือก repo_root ผ่าน authority_context;
payload เลือกเครื่องหรือพาธผลลัพธ์ไม่ได้

ตัวปฏิบัติอ่าน IDP v2, อ้างอิงบริบท `Cast/context/session_summary.md`,
เก็บ hash/symbols/imports/calls ของไฟล์จริง แล้วสร้างรายงาน JSON ใน
`modules/Cast/reports/` แยกจาก private pattern ใน
`modules/Cast/artifacts/private/` ผลนี้เป็น static inspection และข้อเสนอ
ที่ยังไม่ apply ไม่ใช่การพิสูจน์ runtime ครบเชน การฝึกโมเดล หรือการแก้ซอร์สอัตโนมัติ
`COMPLETED` รับรองเฉพาะการสร้างผลงานตรวจนี้ และยัง `review: true`

reason/interpret จัดข้อมูลที่ผู้เรียกส่งมาโดยชัดเจน ประวัติ memory ที่ Engine
ค้นพบไม่ใช้แทน observations ของงานใหม่ งานเอกสารอิสระ/deep reasoning
ที่เกินขอบเขตนี้ยังต้องมีตัวปฏิบัติของ host; ไม่ถือว่า IDP คือการติดตั้งความสามารถครบแล้ว

ต้นทางบทบาท: `BBX19/modules/BBX19/idp/IDP-V2.0/Cast-IDP.md`
และ `core/identity/profiles/Cast.idp.json`; manifest runtime อยู่ `modules/Cast/module.json`
