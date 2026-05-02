# คู่มือ .json ฉบับเข้าใจง่าย (ภาษาไทย) — สำหรับทีมที่ไม่ถนัดโค้ด

นี่คือคู่มือสั้น ๆ ที่สอนแบบเป็นขั้นตอนว่าควรเขียน .json ยังไงให้ถูกต้อง ปลอดภัย และอ่านง่าย พร้อมคำสั่งที่ใช้บ่อยเมื่อต้องแก้บนมือถือหรือผ่าน terminal

สรุปสั้น ๆ
- JSON = ข้อความ (text) รูปแบบมาตรฐานสำหรับแลกเปลี่ยนข้อมูล (machine-readable)
- ใช้กับ config, data exchange, API, template ฯลฯ
- ข้อดี: เรียบง่าย, รองรับทุกภาษา, อ่านโดยโปรแกรมได้
- ข้อจำกัด: ไม่มีคอมเมนต์, ต้องเป็นรูปแบบที่ถูกต้องเป๊ะ

1) โครงสร้างพื้นฐานและชนิดข้อมูล
- Object: {...} — เก็บคู่คีย์:ค่า (key must be string ใน double quotes)
- Array: [...] — ลำดับค่าหลายค่า
- String: "ข้อความ" — ต้องใช้ double quotes เสมอ
- Number: 123, -12.34 — ไม่มีเครื่องหมาย +, ไม่มี quotes
- Boolean: true / false
- null — ค่าที่ว่างเปล่า

สัญลักษณ์สำคัญ
- { } : เริ่ม/ปิด object
- [ ] : เริ่ม/ปิด array
- "key": value : key และ value คั่นด้วย colon (:)
- , : คั่นคู่ key/value หรือลำดับใน array
- " " : ข้อความต้องอยู่ใน double quotes เท่านั้น

ตัวอย่าง JSON ถูกต้อง
```
{
  "task_id": "W3-PR-30",
  "state": "in_progress",
  "count": 120,
  "members": ["BBXDOO", "alice"],
  "meta": null
}
```

2) ข้อห้าม / ข้อผิดพลาดที่พบบ่อย
- ห้ามใช้ single quotes: { 'key': 'value' } ผิด
- ห้ามมี trailing comma: { "a":1, } ผิด
- ห้ามใส่ comment แบบ // หรือ /* */ — JSON ไม่รองรับ comment
- ห้ามมี NaN / Infinity / undefined
- คีย์ต้องอยู่ใน double quotes เสมอ
- ระวังการ escape: เครื่องหมายพิเศษ ใน string ต้อง escape ด้วย slash เช่น \" \\\\ \n \t \uXXXX

3) การตั้งชื่อไฟล์ / เวอร์ชัน
- ใช้ชื่อลงตัวและสื่อความหมาย: resume_header.json, identities_v1.json
- หาก schema สำคัญ ให้ใส่เวอร์ชัน: data.schema.v1.json หรือ field "schema_version": "1.0"
- เวลา timestamp ให้ใช้ ISO 8601: "2025-12-01T14:30:00Z"

4) แนวทางการเขียน field (best practices)
- เลือก naming style เดียว: snake_case หรือ camelCase (ตัวอย่างใช้ snake_case)
- ใส่ field ที่จำเป็นเท่านั้น และถ้าเป็น optional โปรดระบุใน docs/schema ว่า optional
- ตัวอย่าง header สำหรับ resume:
```
{
  "keyword": "REBOOT_WORK",
  "task_id": "W3-PR-30",
  "repo": "W3_HB_team_BXCGICOG",
  "state": "in_progress",
  "next_action": "run identity_backup_sync.sh --resume --task W3-PR-30",
  "contact": "BBXDOO",
  "timestamp": "2025-12-01T14:30:00Z"
}
```

5) การตรวจสอบความถูกต้อง (validation)
- แนะนำใช้ JSON Schema เพื่อบังคับโครงสร้าง (type, required, pattern)
- ตัวอย่าง schema สั้น ๆ:
```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["keyword","task_id","timestamp"],
  "properties": {
    "keyword": {"type":"string"},
    "task_id": {"type":"string"},
    "timestamp": {"type":"string","format":"date-time"},
    "state": {"type":"string"},
    "next_action": {"type":"string"},
    "contact": {"type":"string"}
  }
}
```
- เครื่องมือ validate:
  - ajv-cli (node): `ajv validate -s schema.json -d data.json`
  - jq (เบื้องต้น): `jq empty data.json` (เช็กว่ายัง parse ได้)
  - python: `python -m json.tool data.json` (format check)

6) คำสั่งใช้งานที่แนะนำ (บนมือถือผ่าน Termux / VS Code terminal)
- เช็กความถูกต้อง / แสดงแบบสวย:
  - python: `python -m json.tool file.json`
  - jq: `jq '.' file.json`
- อ่านค่า field:
  - `jq '.task_id' file.json`
  - `jq -r '.next_action' file.json` (raw string)
- เพิ่ม/แก้ไข field แล้วบันทึก:
  - `jq '.new_field = "value"' file.json > tmp && mv tmp file.json`
  - อัปเดต nested: `jq '.meta.count = 5' file.json > tmp && mv tmp file.json`
- ลบ field:
  - `jq 'del(.unwanted)' file.json > tmp && mv tmp file.json`
- Format (prettify) ด้วย prettier:
  - `npx prettier --write file.json` หรือใน VS Code กด Format Document

7) การใช้ JSON patch / merge
- หากต้องการเปลี่ยนเฉพาะส่วนใช้ jsonpatch (RFC6902)
- ตัวอย่างเครื่องมือ: `jsonpatch` (npm) หรือ `jq` สำหรับการเปลี่ยนแบบเล็ก ๆ
- ระวังการ merge โดยตรงกับ object ใน JavaScript ที่อาจทำให้เกิด prototype pollution หากข้อมูลมาจากแหล่งไม่เชื่อถือ

8) ตัวอักษรพิเศษและ Escape sequences
- \n : newline
- \t : tab
- \\ : backslash
  (หมายเหตุ: ใน JSON ต้องใช้สอง backslash `\\` เพื่อแทน backslash จริงหนึ่งตัว)
- \" : double quote ภายใน string
- \uFFFF : unicode codepoint
ตัวอย่าง:
```
{ "note": "Line1\nLine2", "quote": "She said \"hi\"" }
```

9) ความปลอดภัย / ข้อควรระวัง
- ห้ามเก็บ secrets (password, tokens) ในไฟล์ .json ที่เก็บใน repo สาธารณะ
- ถาต้องเก็บ secret ให้ใช้ GitHub Secrets, environment variables หรือ vault
- ไม่ trust JSON ที่ผู้ใช้ส่งมาโดยตรง—validate ก่อนประมวลผล
- จำกัดขนาดไฟล์ถ้าจะ parseบน client (มือถือมีหน่วยความจำจำกัด)

10) ตัวอย่าง workflow แบบง่าย (ทีมที่ใช้ .json สื่อสาร)
- สร้าง template header resume_header.json และบอกทุกคนใส่ header นี้ก่อนเนื้อหา
- ก่อน push ให้รัน `python -m json.tool` หรือ `jq` ตรวจ syntax
- ใช้ JSON Schema ใน CI (Actions) เพื่อตรวจทุก PR
- ตั้งชื่อไฟล์ตาม pattern: w3-backup_
