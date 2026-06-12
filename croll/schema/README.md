# CROLL lightweight contracts

ไฟล์ในโฟลเดอร์นี้เป็น JSON Schema Draft 2020-12 สำหรับแลกเปลี่ยนข้อมูลกับ WHUB
และระบบภายในเครือข่าย W3 โดยไม่เปลี่ยน CROLL ให้เป็น schema engine ขนาดใหญ่

- `boundary.schema.json` — ประกาศเจ้าของ ขอบเขตเครือข่าย สิ่งที่อนุญาต/ห้าม และ review
- `workset.schema.json` — ผล lookup จาก Table-X
- `dispatch-plan.schema.json` — แผนที่ CROLL สร้าง โดยล็อกว่าไม่ execute และไม่ mutate

Runtime ใช้ `croll/contracts.py` ตรวจ safety invariants ด้วย Python standard library ส่วนระบบ
ภายนอกสามารถใช้ JSON Schema validator มาตรฐานกับไฟล์เหล่านี้ได้

กติกาเวอร์ชัน `1.x`: เพิ่ม field ได้เมื่อไม่ทำลาย compatibility แต่การเปลี่ยนความหมายของ
field, ลด deny, หรือเปิด execution ต้องใช้ contract version ใหม่และผ่านการทบทวนของ W3
