# W3 RAMS README Assistant — คู่มือใช้งานและบันทึกอัปเกรด

สถานะ: Experimental / Opt-in / Non-evaluating
พื้นที่: `w3_tool_store/agent_workbench/tools/rams_readme_assistant/`
วันที่เริ่ม: 2026-11-22
ผู้จัดทำ: ChatGPT / Codex

## วัตถุประสงค์
ช่วยตรวจพบ README.md ที่ขาดและสร้าง README แบบ RAMS เมื่อถูกเรียกใช้ ไม่ตรวจตัดสินความถูกต้องของเอกสาร ไม่บังคับแก้ไขไฟล์เดิม ไม่เปลี่ยนกฎหรือ schema ของ BOX, WX, CN-FOLD, Library-X

## วิธีใช้
จาก Git root:

```bash
python w3_tool_store/agent_workbench/tools/rams_readme_assistant/rams_readme_assistant.py --scope docs --levels A,B --mode dry-run
```

ตรวจรายการ `PLANNED` ก่อน แล้วจึงเรียกด้วย `--mode create` เพื่อสร้างเฉพาะ README ที่ไม่มีอยู่ (การเรียก create เป็นการอนุญาตเขียนจากผู้เรียก)

```bash
python w3_tool_store/agent_workbench/tools/rams_readme_assistant/rams_readme_assistant.py --scope docs --levels A,B --mode create
```

`--levels` คือระดับโฟลเดอร์แบบ absolute จาก Git root: `docs/` = A, `docs/foo/` = B, `docs/foo/bar/` = C. สามารถจำกัด `--scope` ไปยังโฟลเดอร์อื่นได้ แต่ระดับยังอ้างอิง Git root

## รูปแบบที่สร้าง
- Head สี่บรรทัด; บรรทัดที่ 4 เป็น `≡ Ar1ra - RAMS` / `≡ Br1ra - RAMS` ตามระดับโฟลเดอร์
- Body ไม่เดาหน้าที่ของโฟลเดอร์จากชื่อ
- M1 แสดงไฟล์/โฟลเดอร์ที่สังเกตได้จริง ณ เวลาสร้าง ไม่รวม README ที่กำลังสร้าง
- M2 ไม่สร้างความสัมพันธ์นอกโฟลเดอร์โดยคาดเดา
- OWNER/MAKER กำหนดได้ด้วย `--owner` และ `--maker`

RAMS Gradation ไม่ใช่ Gradation ID Address ของรายการในแผนผัง

## Trigger integration
Trigger ภายนอกสามารถเรียก CLI นี้หลังเกิดการเปลี่ยนแปลงโฟลเดอร์ โดยใช้ `--mode dry-run` เป็นค่าเริ่มต้น การสร้างอัตโนมัติต้องตั้งค่า `--mode create` โดยผู้ดูแล Trigger เอง ไม่มี background watcher หรือ hook ถูกติดตั้งในต้นแบบนี้

## การทดสอบ
```bash
python -m unittest discover -s w3_tool_store/agent_workbench/tools/rams_readme_assistant -p 'test_*.py' -v
```
ชุดทดสอบสร้าง repository จำลองใน TemporaryDirectory เท่านั้น

## การอัปเกรด
1. ตรวจ dry-run และทดสอบใน sandbox ก่อน
2. แก้ formatter/discovery เฉพาะในไดเรกทอรีต้นแบบนี้
3. รัน unittest และตรวจตัวอย่าง A/B/C
4. อัปเดตบันทึกเวอร์ชันและขอบเขตการเปลี่ยนแปลง
5. หากจะเชื่อม BOX/WX/CN-FOLD/Library-X ให้ตรวจ contract และ schema ต้นทางก่อน ห้ามสร้างกฎหรือ authority ซ้ำ

## การอัปเดต README ที่มีอยู่
เวอร์ชันนี้ตั้งใจ **ไม่รองรับ update/overwrite** เมื่อพบ README อยู่แล้วจะรายงาน `EXISTS` เท่านั้น หากต้องการ refresh M1 ให้เพิ่มขั้นตอนเสนอ diff และอนุมัติแยกในรุ่นถัดไป

## บันทึกการเปลี่ยนแปลง
- 2026-11-22 — v0.1 experimental: เพิ่ม discovery, dry-run/create, RAMS A-Z, M1 จาก filesystem, M2 แบบไม่เดา, skip existing, ป้องกัน symlink traversal, SHA-256 receipt และ isolated tests

## ข้อจำกัด
- ไม่อ่านความหมายเชิงสถาปัตยกรรมจากเนื้อหาไฟล์
- ไม่ประเมินเอกสารตาม rules/schema
- ไม่ติดตั้ง trigger อัตโนมัติ
- ไม่ปรับ README เดิม
- ไม่รองรับการสร้างหลายไฟล์แบบ transaction เดียว
- `create` ไม่สร้างโฟลเดอร์ใหม่ และไม่เข้า BOX-managed roots โดยอัตโนมัติ
