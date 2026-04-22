MPCP_UNIFIED_LANGUAGE_PAPER.md

มาตรฐานภาษาเดียวของระบบ MPCP

เอกสารฉบับนี้กำหนดกฎกลางของระบบ MPCP ว่า

«ทุกข้อมูลเข้า (Input)
ทุกข้อมูลออก (Output)
ทุกการสื่อสารระหว่าง Layer
ต้องใช้ภาษาของ MPCP เท่านั้น»

ระบบสามารถใช้ engine ภายในแบบใดก็ได้
แต่เมื่อมีการรับ-ส่งข้อมูล จะต้องผ่านกฎภาษาเดียวเสมอ

---

หลักการสำคัญ

หลายระบบภายในได้
แต่ภาษากลางต้องมีเพียงหนึ่งเดียว

---

เป้าหมาย

- ลดความซับซ้อน
- ลดการแปลข้อมูลหลายรอบ
- ลดการตีความผิด
- debug ง่าย
- ใช้ได้ทุกแพลตฟอร์ม
- คุมมาตรฐานทั้งระบบ

---

ขอบเขตการบังคับใช้

ใช้กับทุกส่วนของระบบ:

- รับข้อมูลจากผู้ใช้
- รับข้อมูลจากไฟล์
- รับข้อมูลจากเครือข่าย
- ส่งข้อมูลออก
- คุยกันระหว่าง Layer
- คุยกันระหว่าง Modew
- Blueprint
- Logging
- Runtime Events

---

ตัวอย่างที่ถูกต้อง

Input

TASK:build,MODE:fast

Runtime Message

MODEW:Validation,STATE:run

Output

STATE:done,COLOR:Green,SYM:✓

---

ตัวอย่างที่ไม่ถูกต้อง

Layer A ใช้ JSON
Layer B ใช้ XML
Layer C ใช้ YAML
Layer D ใช้ text คนละแบบ

ผลเสีย:

- แปลหลายรอบ
- ช้า
- ตรวจสอบยาก
- สับสน

---

กฎ Layer

ระบบใช้ Layer แบบตัวอักษร ไม่ใช้ตัวเลข

Layer A
Layer B
Layer C
Layer D
Layer E

ทุก Layer ต้องใช้ภาษาเดียวกัน

---

กฎ Input / Output

ข้อมูลเข้า

ข้อมูลทุกชนิดต้องถูกแปลงเป็นรูปแบบ MPCP ก่อนเข้าระบบ

external input
→ adapter
→ MPCP format
→ process

ข้อมูลออก

ผลลัพธ์ทุกชนิดต้องออกเป็นรูปแบบ MPCP ก่อนส่งออก

result
→ MPCP format
→ external target

---

กฎ Library

Library ภายนอกใช้ได้

แต่ห้ามบังคับภาษาเข้าระบบ

ต้องผ่านตัวกลางเสมอ

native lib
→ bridge
→ MPCP language

---

กฎ Blueprint

Blueprint ต้องใช้ภาษา MPCP เช่นกัน

TARGET:android
LIB:fs,net,store
MODE:min

---

กฎ Logging

Log ต้องอ่านรู้เรื่องทันที

TIME:now,MODEW:Auth,STATE:done

---

ประโยชน์

- เปิดไฟล์แล้วเข้าใจ
- ย้ายแพลตฟอร์มง่าย
- เขียน parser เดียว
- ดูแลระบบง่าย
- ลด dependency chaos

---

ข้อห้าม

- ห้ามสร้างภาษาย่อยแยกทีม
- ห้ามใช้หลาย syntax ปะปน
- ห้ามให้ library ภายนอกควบคุม grammar ระบบ
- ห้ามส่งข้อมูลดิบข้าม Layer โดยไม่มีรูปแบบกลาง

---

สรุปกฎสูงสุด

หลาย engine ได้
แต่หนึ่งภาษาเท่านั้น

---

สถานะ

MPCP Core Law v1

---

เจ้าของระบบ

BBX19
