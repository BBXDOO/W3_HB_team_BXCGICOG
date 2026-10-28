# System inspection — ตัวเชื่อมตรวจ W3

AM Ⅲ · BUILD / OBSERVE / CONTINUE · OWNER: BBX19 · MAKER: ChatGPT

## Body

ตัวเชื่อมใน trusted host รันชุดตรวจที่กำหนดของ MPCP, E-CS, W3Lgu MFC Logic,
Cross-X, CROLL, Table-X และ PX แล้วส่งรายงานให้ Gemini ตรวจหลักฐานซ้ำ
ใช้ Orchestration เดิมรับงานจริงผ่าน Root Request ไม่ใช้ Issue preview เป็นตัวรัน

ชุดทดสอบแต่ละระบบรันในสำเนาใหม่ แยกจาก checkout ต้นทาง มี timeout 180 วินาที
เก็บ input hashes, stdout, exit code และ JUnit XML ระบบหนึ่งล้มจะไม่หยุดการตรวจ
ชุดอิสระถัดไป รายงานปัญหาแยกตามระบบก่อนเดินต่อ ไม่เพิ่มสิทธิ์หรือปิด blocker แทน

latest.json ชี้ผลคืบหน้าตั้งแต่เริ่มและอัปเดตหลังแต่ละระบบ หาก host หยุดกลางทาง
จะเห็น IN_PROGRESS กับผลที่เก็บแล้ว ไม่ได้รายงานว่าจบ Git ในสำเนาเป็น snapshot
ชั่วคราวของ protocol/src สำหรับ MPCP inventory ไม่ใช่ Git revision ของต้นทาง

PASS หมายถึงชุดตรวจที่ระบุผ่านทั้งหมด; skipped tests เป็น PARTIAL;
FAIL/BLOCKED/TIMEOUT เก็บไว้ตามจริง การเก็บรายงานครบไม่เท่ากับระบบทั้งหมดผ่าน
นี่คือ inspection circuit ไม่ใช่การสร้าง production pipeline ใหม่ระหว่างเจ็ดระบบ

ต้องมี Python และ dependencies ใน requirements.txt โดยเฉพาะ pytest
หาก host ไม่มี pytest จะได้รายงาน BLOCKED แยกแต่ละระบบ พร้อมตรวจชุดถัดไปต่อ
การแยกสำเนามีไว้ไม่ให้ชุดทดสอบเขียน checkout จริง ไม่ใช่ security sandbox

## Movement

- [runner.py](runner.py): catalog คงที่, รันชุดตรวจ, เก็บรายงานและตัวตรวจหลักฐาน
- [Workbench tools](../README.md): กลับรายการเครื่องมือ
- [Root Request B](../../../../requests/RQ-W3-SYSTEM-INSPECTION-B-20261028-001.md): ใบงานจริง
- [ผลล่าสุด](../../../../repo_events/system_inspections/latest.json): มีหลังรันครั้งแรก
- ต้นทาง: tools/runtime_circuit_intake.py, tools/orchestration_support.py,
  workflows/runtime_circuit.py และชุดทดสอบเดิมใน catalog

เรียกจาก root: `python tools/request_cycle.py --request requests/RQ-W3-SYSTEM-INSPECTION-B-20261028-001.md`

สิ่งที่เรียนรู้: การมีขั้น B ในข้อความไม่ส่งงาน ต้องมี recipe, executor, verifier
และ event/CLI ที่เรียกมันจริง การตรวจต้องบอกขอบเขต ไม่ใช้คำว่า COMPLETED แทนสุขภาพระบบ
