# MPCP — Lib และ Condien equipment รอบแรก

วันที่: 2026-10-24 (Asia/Bangkok) | ผู้ดูแล: ChatGPT / Codex ตามคำมอบหมาย BBX19

## ขอบเขตที่ใช้เป็นฐาน

ตรวจ `protocol/mpcp/test_condien_blueprint.py`, Paper/File.void/sandbox tests และเครื่องมือเดิมก่อนปรับงาน เทสเดิมแสดงว่า Condien มี layer access, carry-forward, rebase และ profile representation แต่ยังไม่มีอุปกรณ์เก็บ state เต็มข้าม process ส่วน Library มี declaration และการหา language runtime อยู่แล้ว

## สิ่งที่เติม

- `Condien.to_state/from_state`: trusted persistence representation ที่รักษา identity, payload, READ/DENY ระดับ layer/key, active layer, carry/history และ predecessor name แยกจาก inspection view เดิม
- `CondienStore`: SQLite standard-library equipment เก็บ revision ใหม่ ไม่แก้รุ่นเก่า มี expected revision conflict, snapshot hash verification และ explicit predecessor link ที่เรียกคืน object ความต่อเนื่องได้
- `LibraryRegistry`: ลงทะเบียนและเปิดใช้ builder ของอุปกรณ์จริง แยกจากรายการชื่อใน config ไม่รันหรือสร้างสิทธิ์จากการลงทะเบียน และไม่แอบแทนที่ route ของ host อื่น
- `condien-view`: Modew อ่านบริบทที่ ENV กรองไว้แล้ว ใช้ผลรูป MPCP และตรวจเทียบ scoped context จริง
- `tools/mpcp_condien.py`: save อย่างชัดเจนหรือ inspect metadata รุ่น
- `tools/mpcp_papers.py`: โหลด snapshot ที่ host เลือก ผูก CONTEXT_REF กับสิทธิ์ของ Paper แล้วใช้อุปกรณ์ที่มีในทะเบียนเท่านั้น

SQLite เป็นอุปกรณ์เสริมของการจัดเก็บ ไม่เป็น dependency ที่ถูก import บังคับในตัว Condien/Blueprint core หากต้องการใช้ storage ต้องนำเข้า module และเตรียม runtime ที่รองรับเอง

## หลักฐาน

[ผลรัน CLI แยก process พร้อม snapshot/source hashes](2026-10-24_lib_condien_equipment.json)

ตัวอย่างเก็บบริบทจริงแล้วเปิด process ใหม่ให้ Paper อ่าน Layer B ได้เฉพาะ `title` ค่า `excluded` และ Layer D ไม่ถูกส่งออก carry-forward value ถูกเรียกคืนได้จาก storage

ผลตรวจ: 79 tests และ 2 subtests ผ่าน มี utcnow warnings เดิม 4 รายการ ชุด MPCP sanity ผ่าน 81/81 และ Condien/Blueprint foundation ผ่าน 69/69 ตรวจ AMS headers, ลิงก์ใหม่, workflow YAML และ git diff --check ผ่าน ผลเหล่านี้เป็นการตรวจในเครื่อง ยังไม่ใช่ผล hosted CI

## ข้อจำกัดที่คงไว้

ยังไม่เลือกหรือจำแนกความหมายของข้อมูลเข้า layer เอง ไม่ auto-select library จากเจตนา ไม่เติมอุปกรณ์ทุกชื่อใน config ไม่ sync cloud/W3DB และยังไม่ยืนยันการใช้งานจริงบน Android/iOS/Windows

ฐานข้อมูลเต็มเป็นพื้นที่ของ trusted host รวมข้อมูลที่ไม่อนุญาตให้ runtime อ่าน การตรวจตัวตนและสิทธิ์ยังเป็นหน้าที่ host ผลทดสอบยืนยัน process restart/transaction conflict ไม่ใช่การรับรองการกู้ดิสก์หรือไฟดับทุกกรณี

## ทางเข้า

- [Library equipment](../../../protocol/mpcp/lib/README.md)
- [Condien storage และวิธีเรียก tool](../../../src/core/README.md)
- [Tests](../../../tests/test_mpcp_condien_equipment.py)
