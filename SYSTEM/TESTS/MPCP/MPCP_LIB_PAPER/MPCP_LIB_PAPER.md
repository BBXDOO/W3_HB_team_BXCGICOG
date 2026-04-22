MPCP_LIB_PAPER.md

มาตรฐาน Library ของระบบ MPCP

เอกสารฉบับนี้กำหนดแนวทางการใช้ Library ภายในระบบ MPCP

เป้าหมายหลักคือ:

«ทำให้ MPCP อยู่รอด ใช้งานได้ และย้ายระบบได้
บนทุกแพลตฟอร์ม»

เช่น:

- Linux
- Android
- iOS
- Sandbox Runtime
- Embedded Environment

---

หลักการสำคัญ

Library รับใช้ระบบ
ระบบไม่รับใช้ Library

---

เป้าหมาย

- ใช้ได้หลายแพลตฟอร์ม
- เปลี่ยน lib ได้
- ลดการผูกติดระบบภายนอก
- ใช้ทรัพยากรต่ำ
- debug ง่าย
- ควบคุมได้เอง

---

โครงสร้าง Library ของ MPCP

แบ่งเป็น 3 กลุ่มหลัก

1. Core Lib
2. Bridge Lib
3. Optional Lib

---

1. Core Lib

เป็น library ที่ระบบต้องมีเสมอ

memory
parser
file
time
string
math
event
storage

คุณสมบัติ:

- เล็ก
- เสถียร
- ใช้ทุกระบบ
- เปลี่ยนน้อย

---

2. Bridge Lib

ใช้เชื่อมแต่ละแพลตฟอร์ม

linux.bridge
android.bridge
ios.bridge
web.bridge

หน้าที่:

- เรียก native API
- เข้าถึง file system
- network
- process
- permission

แต่ผลลัพธ์ต้องแปลงกลับเป็นภาษา MPCP

---

3. Optional Lib

โหลดเมื่อจำเป็น

crypto
compress
media
gpu
ai
camera
sensor

ไม่ใช่แกนหลักของระบบ

---

กฎสำคัญ

กฎที่ 1

Library ภายนอก ห้ามกำหนด grammar ของระบบ

กฎที่ 2

ทุก lib ต้องผ่าน bridge หรือ adapter

กฎที่ 3

Input / Output ของ lib ต้องคืนค่าเป็นรูปแบบ MPCP

กฎที่ 4

ถอด lib ออกได้โดยไม่ทำลาย core

---

ตัวอย่าง

ไม่ถูกต้อง

ระบบใช้ syntax ของ library ตรง ๆ

ถูกต้อง

native lib
→ bridge
→ MPCP format
→ system use

---

รูปแบบการตอบกลับ

ตัวอย่าง file lib

PATH:/user/data
STATE:ok

ตัวอย่าง network lib

HOST:api.site
STATUS:200
TIME:124

---

Blueprint การเลือก lib

TARGET:android
CORE:yes
BRIDGE:android
OPTIONAL:camera,crypto
MODE:min

---

การจัดเก็บ

/lib/core/
/lib/bridge/
/lib/optional/
/lib/cache/

---

ประโยชน์

- ย้ายระบบง่าย
- ลด lock-in
- ใช้ lib เฉพาะที่จำเป็น
- เปลี่ยน platform ง่าย
- คุมมาตรฐานได้เอง

---

ข้อห้าม

- ห้ามยัด lib ใหญ่เกินจำเป็น
- ห้ามให้ lib คุม flow ระบบ
- ห้ามผูกติด OS ใด OS หนึ่ง
- ห้ามใช้ lib โดยไม่มี bridge

---

สรุปกฎสูงสุด

ใช้ lib ได้ทุกตัว
แต่ต้องพูดภาษา MPCP

---

สถานะ

MPCP Survival Library Standard v1

---

เจ้าของระบบ

BBX19
