# Agent Alignment Tests v2 — Planning Draft (ChatGPT)

## เป้าหมาย
ร่างแนวคิดเตรียมยกระดับการทดสอบและ alignment ของ ChatGPT กับ MPCP/W3 concept ในเฟสถัดไป (v2)

---

## 1. จุดสำคัญที่เรียนรู้จาก v1
- ตรวจ alignment ยังเป็นแบบ keyword-based
- role “flow_architecture” ถูก bind แบบ declarative แต่ยังไม่ test พฤติกรรมจริง
- ไม่มี relation check ว่า flow/execution ไม่ไป overlap กับ governance หรือ validation

## 2. เป้าหมายของ v2 สำหรับ ChatGPT Agent
- เพิ่ม test ที่วัดว่า ChatGPT ตอบโจทย์ “flow architecture/execution support” จริง (ไม่ใช่เพียงแค่มีคำเหล่านี้ใน docs)
- ตรวจว่า ChatGPT ไม่ไปรับผิดชอบ governance หรือ validation
- คิด test ที่ inspect การ handoff, context bridging, หรือ execution flow clarity

## 3. แนวทาง/idea ที่อยากลองเพิ่ม
- สร้าง test ที่อ่าน section ใน doc โดยตรง (เช่น “Flow”, “Execution”, “Scope”) แล้วเช็กกับ action_label ของ agent
- ลอง test ว่า agent อื่น (Copilot-Gm, Gemini) ไม่ตอบสนอง “execution flow” task ถ้าถามด้วย test
- Exploration: เช็กความสัมพันธ์ระหว่าง ChatGPT กับ Cast (handoff ก่อน/หลัง runtime)

## 4. สิ่งที่ยังไม่ควรเร่ง
- ยังไม่ต้อง implement flow-based adaptive/self-modifying agent
- ยังไม่บังคับให้ agent ตัดสินใจ cross-module จริงใน runtime

---

## หมายเหตุ
ใช้เป็น brainstorm/notes ได้เต็มที่ ทีมใส่เพิ่มเติมได้เลย
