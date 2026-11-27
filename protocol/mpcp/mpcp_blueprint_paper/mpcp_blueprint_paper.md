---
AM_TYPE: II
ROLE: DESIGN_SPECIFICATION
GROUP: CONTINUE
DERIVED_FROM:
  - protocol/mpcp/MPCP_ORIGIN.md
OWNER: BBX19
---

**Gradation** `≡ Dd2mc - mpcp` · [แผนที่โฟลเดอร์](README.md)

mpcp_BLUEPRINT_PAPER.md

มาตรฐาน Blueprint ของระบบ mpcp

เอกสารฉบับนี้กำหนดรูปแบบ Blueprint สำหรับระบบ mpcp

Blueprint คือแบบแผนสำหรับสร้างระบบ, สร้างสภาพแวดล้อม, เลือก Library, กำหนดโครงสร้าง และทำให้ระบบสร้างซ้ำได้เหมือนเดิม

«Blueprint ไม่ใช่การรันงาน
Blueprint คือแผนสำหรับการรันงาน»

---

หลักการสำคัญ

เขียนครั้งเดียว
สร้างได้ทุกที่

---

เป้าหมาย

- สร้างระบบซ้ำได้
- ย้ายแพลตฟอร์มง่าย
- ลดการตั้งค่ามือ
- คุมมาตรฐาน
- ใช้ข้อความอ่านง่าย
- ใช้ภาษา mpcp เท่านั้น

---

ใช้กับอะไรได้บ้าง

- Runtime Environment
- Mobile Build
- Desktop Build
- Library Selection
- Partition Layout
- Deployment Package
- Recovery Setup

---

โครงสร้างมาตรฐาน

Blueprint ใช้รูปแบบข้อความสั้น กระชับ ชัดเจน

KEY:VALUE
KEY:VALUE
KEY:VALUE

---

ตัวอย่างพื้นฐาน

NAME:mpcp_CORE
TARGET:android
MODE:min
LIB:fs,net,store
PARTITION:A,B,C,D

---

ค่าหลักที่แนะนำ

NAME

ชื่อ Blueprint

NAME:MOBILE_CORE

TARGET

แพลตฟอร์มเป้าหมาย

TARGET:linux
TARGET:android
TARGET:ios

MODE

รูปแบบการติดตั้ง

MODE:min
MODE:full
MODE:test

LIB

ชุด Library ที่ใช้

LIB:fs,parser,store,net

PARTITION

พื้นที่จัดเก็บ

PARTITION:A,B,C,D,E

---

Blueprint สำหรับมือถือ

NAME:mpcp_PHONE
TARGET:android
MODE:min
LIB:fs,store,net,sensor
PARTITION:A,B,C

---

Blueprint สำหรับ iOS

NAME:mpcp_IOS
TARGET:ios
MODE:stable
LIB:fs,store,net
PARTITION:A,B,C,D

---

Blueprint สำหรับ Linux

NAME:mpcp_LINUX
TARGET:linux
MODE:full
LIB:fs,store,net,process,shell
PARTITION:A,B,C,D,E

---

กฎสำคัญ

กฎที่ 1

Blueprint ใช้ภาษา mpcp เท่านั้น

กฎที่ 2

Blueprint ต้องอ่านรู้เรื่องทันที

กฎที่ 3

Blueprint ต้องสร้างซ้ำได้

กฎที่ 4

Blueprint ต้องไม่ผูกกับแพลตฟอร์มเดียว

กฎที่ 5

Blueprint ต้องแก้ไขง่าย

---

สิ่งที่ Blueprint ไม่ใช่

- ไม่ใช่ source code
- ไม่ใช่ runtime log
- ไม่ใช่คำสั่งเฉพาะครั้งเดียว
- ไม่ใช่ event packet

---

การใช้งานจริง

LOAD BLUEPRINT
→ CHECK TARGET
→ LOAD LIB
→ CREATE PARTITION
→ START RUNTIME

---

ขอบเขตการนำไปใช้ — Local setup

ลำดับด้านบนเป็นแบบแผน ไม่ใช่การรับรองว่าทุก TARGET มี runtime หรืออุปกรณ์จริงพร้อมใช้งาน การทดลอง Workbench วันที่ 2026-10-27 ใช้ `TARGET:local` ผ่าน W3Lgu gate → ENV → MPCP Modew เพื่อสร้าง partition และ setup manifest เท่านั้น ส่วนเอกสาร device profile และ playtest plan เกิดจาก Paper แยกผ่าน File.void handoff และ external writer ที่ตรวจผลแล้ว ไม่ใช่การบูต Android หรือรัน APK

หลักฐาน: [OPPO probe result](../../../w3_tool_store/agent_workbench/profiles/oppo_android_probe/RESULT_2026-10-27.md)

---

การจัดเก็บไฟล์

/blueprints/
core.bp
mobile.bp
linux.bp
ios.bp
test.bp

---

ประโยชน์

- เปิดไฟล์แล้วเข้าใจ
- setup เร็ว
- deploy ง่าย
- clone environment ได้
- scale ได้หลายเครื่อง

---

ข้อห้าม

- ห้ามยัด logic runtime ลง blueprint
- ห้ามเขียนวกวน
- ห้ามผูก path ตายตัว
- ห้ามใส่ค่าลับลง blueprint ตรง ๆ

---

สรุปกฎสูงสุด

Blueprint คือแผน
ไม่ใช่การกระทำ

---

สถานะ

mpcp Blueprint Standard v1

---

เจ้าของระบบ

BBX19
