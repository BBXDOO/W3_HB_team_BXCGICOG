# Agent Alignment Tests v2 — Planning Draft (Copilot-Gm)

## เป้าหมาย
แนวคิดเตรียมรอบปรับปรุง test alignment สำหรับ Copilot-Gm (governance/structural consistency) ใน v2

---

## 1. จุดที่เรียนรู้จาก v1
- role “governance” ยังไม่มี test ว่า guard boundary จริง
- governance/structural consistency ยัง test แค่ชื่อ/keyword
- ไม่ cross check กับ role อื่น (เช่น, ตรวจ law/boundary กับ ROT ไม่ปน execution)

## 2. เป้าหมาย v2 สำหรับ Copilot-Gm Agent
- ตรวจ governance policy, compliance checker
- เพิ่ม test policy enforcement กับ action ของ agent อื่น
- วัดว่าการ judge boundary/law แยกจาก execution/paper/result จริง

## 3. test idea
- fixture: simulate cross-agent policy check
- test policy handoff ระหว่าง Copilot-Gm กับ ROT/Condien
- negative test: Copilot-Gm ไม่ควร trigger execution/flow

## 4. สิ่งที่ไม่ควรเร่ง
- automation ของ authority law/rot
- governance auto-correction

---

## หมายเหตุ
ทีมเติม pattern/checklist/idea ได้เต็มที่