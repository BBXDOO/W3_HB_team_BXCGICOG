---
request_id: RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001
task_keyword: governance
target_module: Copilot-Gm
requester: BBX19
language: th
request_type: document_creation
document_kind: thai_markdown_guide
artifact_path: BBX19/notes/THAI_MARKDOWN_GUIDE.md
authority_requested: create_one_document_in_bbx19_notes
final_signoff_required: true
mutated: false
review: true
---

# Request: คู่มือการใช้ Markdown ฉบับภาษาไทย

## Intent

มอบหมายให้ `Copilot-Gm` สร้างคู่มือ Markdown ภาษาไทยหนึ่งฉบับ โดยใช้ `Gemini` เป็นคู่งานสำหรับตรวจความถูกต้อง ความเข้ากันได้ของ renderer และบันทึกกิจกรรมที่ตรวจย้อนกลับได้

คำร้องนี้ใช้ทดสอบความสามารถจริงของสายงาน:

```text
request → Orchestration inspect/route → Copilot-Gm create → Gemini verify/record
→ Orchestration verify → BBX19 final sign-off
```

ให้ใช้กลไกที่มีอยู่ก่อน ห้ามสร้างโมดูล ระบบ routing, registry หรือคู่มือซ้ำเพื่อหลีกเลี่ยงข้อจำกัดที่พบ

## Participants

- Primary / document owner: `Copilot-Gm`
- Partner / validator / activity recorder: `Gemini`
- Orchestrator: `workflows/orchestration.py` หรือผู้เรียกที่ปฏิบัติตาม Orchestration contract
- Final authority: `BBX19`

## Authorized output

BBX19 อนุญาตเฉพาะคำร้องนี้ให้ `Copilot-Gm` สร้างหรือปรับไฟล์:

`BBX19/notes/THAI_MARKDOWN_GUIDE.md`

สิทธิครั้งนี้ไม่ขยายเป็นสิทธิจัดการไฟล์อื่นใน `BBX19/notes/` และไม่เปลี่ยน owner หรือ write scope ถาวรของโมดูล

## Required content

คู่มือต้องเขียนเป็นภาษาไทย อ่านได้สำหรับผู้เริ่มต้น และมีตัวอย่างที่คัดลอกไปทดลองได้ ครอบคลุมอย่างน้อย:

1. รูปแบบ Markdown พื้นฐาน: หัวข้อ ย่อหน้า รายการ ลำดับเลข code และ code block
2. การสร้างตาราง รวม alignment และข้อจำกัดของตาราง Markdown
3. การใช้สีพื้นหลังกับตาราง
4. การใช้สีร่วมกับข้อความ
5. การสร้างลิงก์ ทั้งข้อความ URL รูปภาพ anchor และ relative path
6. ตัวหนา ตัวเอียง ตัวขีดฆ่า และการขีดเส้นใต้
7. การสร้างเส้นแนวนอนและเส้นขอบ/เส้นแนวตั้ง
8. การเพิ่มความหนาของเส้น
9. เทคนิคอื่น ๆ ที่ใช้งานได้จริง เช่น blockquote, checklist, details/summary, escaping และ line break
10. ตารางสรุปว่า syntax ใดเป็น Markdown มาตรฐาน, GitHub Flavored Markdown (GFM), HTML/CSS fallback หรือขึ้นกับ renderer

## Accuracy rules

- ต้องแยก Markdown มาตรฐาน, GFM และ HTML/CSS ให้ชัด
- สีพื้นหลัง สีข้อความ การขีดเส้นใต้ เส้นแนวตั้ง และความหนาเส้น ไม่ใช่ความสามารถมาตรฐานของ Markdown ทุก renderer; ห้ามอธิบายว่าใช้ได้ทั่วไปโดยไม่มีคำเตือน
- ตัวอย่าง HTML/CSS ต้องระบุว่า GitHub อาจกรอง style หรือไม่แสดงผลตามที่คาด
- ใช้ตัวอย่างที่ปลอดภัย ไม่ฝัง script และไม่ใช้ remote tracking resource
- หากความสามารถต่างกันระหว่าง GitHub, Obsidian, Pure Writer หรือ renderer อื่น ให้ระบุว่า “ขึ้นกับ renderer” และไม่เดาผลลัพธ์

## Gemini partner work

Gemini ต้อง:

1. ตรวจความถูกต้องของ syntax และคำอธิบาย
2. ตรวจว่าคู่มือไม่สับสนระหว่าง Markdown, GFM และ HTML/CSS
3. ตรวจลิงก์ภายในและตัวอย่าง relative path
4. ระบุข้อจำกัดหรือ unknown โดยไม่แก้เจตนาของต้นฉบับ
5. บันทึกกิจกรรมและผลตรวจไว้ใน `repo_events/` โดยอ้าง `request_id` นี้

ชื่อ event ที่คาดหวังเมื่อมีการปฏิบัติงาน:

- `repo_events/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001_EXECUTION.md`
- `repo_events/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001_GEMINI_VALIDATION.md`

ไฟล์ event ต้องเป็นหลักฐานตามเหตุการณ์จริง ห้ามสร้างสถานะ `COMPLETED` หรือ `validated` ล่วงหน้า

## Orchestration behavior

1. รับและตรวจคำร้องโดยรักษา `request_id`
2. route งานสร้างเอกสารไปยัง Copilot-Gm และส่ง handoff คู่ขนานให้ Gemini
3. ต้องมีหลักฐาน ACK ก่อนเปลี่ยนจาก `ROUTED` เป็น `ACKNOWLEDGED`
4. หาก Copilot-Gm runtime ปัจจุบันทำได้เพียง governance review และยังสร้างไฟล์ไม่ได้ ให้บันทึก `BLOCKED` พร้อมเหตุผล แล้วเรียก document-writing specialist/tool ผ่าน `assist()` ที่มี adapter ชัดเจน
5. ผู้ช่วยที่ถูกเรียกไม่รับช่วง ownership; artifact ยังคงเป็นผลงานภายใต้คำร้องของ Copilot-Gm
6. ส่ง artifact ให้ Gemini ตรวจ และส่งกลับ Orchestration เพื่อ `VERIFYING`
7. ห้ามปิด `COMPLETED` จนกว่าจะมี artifact จริง ผลตรวจ Gemini และ evidence ครบ
8. Final closure ต้องรอ BBX19 sign-off

## Required return contract

- `status`
- `request_id`
- `primary_module`
- `partner_module`
- `artifact_path`
- `artifact_sha256`
- `gemini_validation_event`
- `orchestration_evidence`
- `summary`
- `limitations`
- `unknowns`
- `mutated`
- `review`
- `final_signoff`

## Completion conditions

งานสร้างถือว่าผ่านเมื่อ:

- มีไฟล์จริงที่ `BBX19/notes/THAI_MARKDOWN_GUIDE.md`
- เนื้อหาครบหัวข้อหลักและแยก renderer compatibility อย่างถูกต้อง
- Gemini สร้าง validation event จากการตรวจจริงใน `repo_events/`
- Orchestration มี route, acknowledgement, artifact และ verification evidence ที่ตรวจย้อนกลับได้
- ไม่มีการสร้างคู่มือหรือ source request ซ้ำโดยไม่มีเหตุผล

สถานะ `ROUTED`, `ACKNOWLEDGED`, การมี draft เพียงอย่างเดียว หรือผลจาก executor ที่ไม่สร้าง artifact ไม่ถือว่า `COMPLETED`
