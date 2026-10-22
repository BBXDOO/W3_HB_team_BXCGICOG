# Callback Templates

AM: III / Process | Group: BUILD / CONTINUE | Owner: BBX19

`assignment.template.md` ใช้เริ่มใบงาน root ส่วน JSON แต่ละไฟล์เป็นคำตั้งต้นสำหรับการตอบ ให้คัดลอกเฉพาะ kind, decision/message_type, reason, annotations, evidence ลงในฟอร์มที่ระบบสร้างใน responses/ เพื่อรักษา binding ของงานจริง การคัดลอกไฟล์ JSON ต้นแบบทั้งไฟล์ไปกดใช้งานจะไม่ผ่าน เพราะยังไม่มี binding

| ไฟล์ | ใช้เมื่อ |
|---|---|
| approve.template.json | ตรวจรับผลตามขอบเขต |
| request_changes.template.json | ขอแก้ไขก่อนรับ |
| hold.template.json | พักการตัดสินใจ |
| reject.template.json | ปฏิเสธผล/คำร้องและจบคำร้อง |
| cancel.template.json | ยกเลิกคำร้อง |
| acknowledge.template.json | แจ้งรับทราบ |
| progress.template.json | แจ้งความคืบหน้า |
| help.template.json | แจ้งความต้องการความช่วยเหลือ |
| delivery.template.json | แจ้งส่งมอบพร้อมหลักฐาน |
| delegation.template.md | บันทึกขอบเขตการมอบหมายให้ตัวแทน |

NOTE ทั้งสี่แบบเป็นบันทึกการสื่อสาร ไม่ถือเป็นการอนุมัติหรือหลักฐานว่าผลงานผ่านการตรวจ การดำเนินงานปลายทางยังใช้ executor / support / verifier ของวงจรเดิม
