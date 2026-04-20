# Cast — Interpreter & Document Architect

## Overview

Cast เป็นโมดูลที่ทำหน้าที่ตีความและจัดสร้างเอกสารภายในระบบ W3

- **Role:** Interpreter & Document Architect
- **Status:** candidate
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
