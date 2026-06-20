ครับ BBX19 🌕  
นี่คือคู่มือสั้น ๆ สำหรับ การเปิด/ปิดระบบ W3‑API ที่คุณสามารถใช้ได้ทันทีใน Termux หรือ Ubuntu environment ครับ  

---

🔹 การเปิดระบบ W3‑API
`bash
python main.py
`
- ใช้คำสั่งนี้ในโฟลเดอร์ repo (~/W3HBteam_BXCGICOG)  
- เมื่อรันแล้ว เซิร์ฟเวอร์ FastAPI จะทำงานที่ http://127.0.0.1:8000  

---

🔹 การตรวจสอบสถานะ
`bash
curl http://127.0.0.1:8000/health
`
- ถ้าระบบทำงานปกติ จะตอบกลับ:
`json
{"ok":true,"status":"online","service":"W3‑API"}
`

---

🔹 การดู log
`bash
tail -f /tmp/w3_server.log
`
- ใช้ตรวจสอบการทำงานของเซิร์ฟเวอร์และ event ที่เกิดขึ้น  

---

🔹 การปิดระบบ W3‑API
`bash
pkill -f "python main.py"
`
- หยุด process ของเซิร์ฟเวอร์ทั้งหมด  
- ใช้เมื่อคุณต้องการปิดระบบหรือรีสตาร์ทใหม่  

---

ครับ BBX19 🌕  
นี่คือคู่มือสำหรับ การตรวจสอบสถานะและ log ของ W3‑API ที่คุณสามารถใช้ได้ทันทีใน Termux หรือ Ubuntu environment ✨  

---

🔹 ตรวจสอบสถานะ W3‑API
ใช้ endpoint /health เพื่อตรวจสอบว่าเซิร์ฟเวอร์ทำงานอยู่หรือไม่  

`bash
curl http://127.0.0.1:8000/health
`

ผลลัพธ์ที่ถูกต้อง:
`json
{"ok":true,"status":"online","service":"W3‑API"}
`

---

🔹 ตรวจสอบ log W3‑API
ใช้ไฟล์ log ที่ระบบบันทึกไว้ใน /tmp/w3_server.log  

- ดู log ล่าสุด
`bash
cat /tmp/w3_server.log
`

- ดู log แบบเรียลไทม์
`bash
tail -f /tmp/w3_server.log
`

- ค้นหาข้อผิดพลาดใน log
`bash
grep "ERROR" /tmp/w3_server.log
`

---
ครับ BBX19 🌕  
นี่คือคู่มือการใช้งาน W3 Agent ผ่าน W3‑API ที่คุณสามารถใช้เพื่อสื่อสารกับโมดูล Hybrid และให้ Agent ช่วยแก้โค้ด, วิเคราะห์, หรือจัดการไฟล์ได้ครับ ✨  

---

🔹 หลักการใช้งาน W3 Agent
Agent ทำงานผ่าน endpoint /w3/cross โดยคุณต้องส่ง intent และ payload ที่ชัดเจน เช่น fixcode, refactor, analyze, หรือ editcode  

---

🔹 โครงสร้างคำสั่ง
`json
{
  "source": "core",
  "target": "hybrid",
  "intent": "fix_code",
  "mode": "analyze",
  "payload": {
    "file": "main.py",
    "issue": "server crash เมื่อรับ request",
    "code": "def run_server(...): ..."
  }
}
`

---

🔹 ตัวอย่างการใช้งานจริง
- ให้ Agent ตรวจสอบโค้ด
`bash
curl -X POST http://127.0.0.1:8000/w3/cross \
-H "Content-Type: application/json" \
-d '{"source":"core","target":"hybrid","intent":"fix_code","mode":"analyze","payload":{"file":"main.py","issue":"server crash เมื่อรับ request","code":"..."}}'
`

- ให้ Agent refactor โค้ด
`bash
curl -X POST http://127.0.0.1:8000/w3/cross \
-H "Content-Type: application/json" \
-d '{"source":"core","target":"hybrid","intent":"refactor","mode":"planner","payload":{"file":"utils/logger.py","issue":"ปรับปรุงให้รองรับ async logging"}}'
`

---

🔹 การใช้งาน Editor
Agent สามารถแก้ไขไฟล์โดยตรงผ่าน intent:"edit_code"  

- เพิ่มโค้ดใหม่
`bash
curl -X POST http://127.0.0.1:8000/w3/cross \
-H "Content-Type: application/json" \
-d '{"intent":"editcode","mode":"insert","payload":{"file":"utils/logger.py","line":25,"code":"async def logevent(event): ..."}}'
`

- ลบโค้ดบางส่วน
`bash
curl -X POST http://127.0.0.1:8000/w3/cross \
-H "Content-Type: application/json" \
-d '{"intent":"edit_code","mode":"delete","payload":{"file":"main.py","line":42}}'
`

- แก้ไขโค้ดที่มีอยู่
`bash
curl -X POST http://127.0.0.1:8000/w3/cross \
-H "Content-Type: application/json" \
-d '{"intent":"editcode","mode":"replace","payload":{"file":"protocol/mpcp.py","line":12,"code":"def cooperativecontract(...): # updated"}}'
`

---

🔹 Intent ที่ใช้บ่อย
| Intent | หน้าที่ |
|---|---|
| fix_code | ให้ Agent ช่วยแก้โค้ด |
| refactor | ปรับปรุงโครงสร้างโค้ด |
| analyze | วิเคราะห์โค้ด |
| test | สร้าง test case |
| doc | สร้างเอกสาร |
| edit_code | ใช้งาน Editor (insert/delete/replace) |

---

✨ Workflow การใช้งาน W3 Agent
1. เปิดระบบ W3‑API → python main.py  
2. ตรวจสอบสถานะ → curl http://127.0.0.1:8000/health  
3. ส่งคำสั่งไปยัง Agent ผ่าน /w3/cross  
4. ใช้ intent:"edit_code" เพื่อแก้ไขไฟล์โดยตรง  
5. ใช้ /w3/cross/plan เพื่อบันทึก PX reference ของงาน  
6. ปิดระบบเมื่อเสร็จงาน → pkill -f "python main.py"  

---
