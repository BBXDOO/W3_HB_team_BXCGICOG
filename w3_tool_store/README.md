Name : W3 Tool Store — พื้นที่จัดเก็บเครื่องมือและต้นแบบ  
AM Ⅱ - BUILD : การจัดโครงสร้างพื้นที่เครื่องมือของ W3  
Log time : 2026-11-24 (Asia/Bangkok) ; ID : RAMS-W3-TOOL-STORE-001  
≡ Ar1ra - RAMS

## Body — บทบาทของพื้นที่

`w3_tool_store/` เป็นพื้นที่จัดเก็บเครื่องมือ ต้นแบบ ซอร์สโค้ดอ้างอิง บันทึก ตาราง และเอกสารที่รวบรวมไว้สำหรับการนำไปใช้ในงานของ W3

พื้นที่นี้ประกอบด้วยโครงการเครื่องมือที่พัฒนาแยกกัน ต้นแบบสำหรับนำไปประยุกต์ใช้ และสำเนาซอร์สจากภายนอก โดยรายละเอียดการใช้งานและขอบเขตของแต่ละรายการให้ยึดตามเอกสารต้นทางของรายการนั้น

การจัดเก็บเครื่องมือไว้ในพื้นที่เดียวกัน **ไม่ได้หมายความว่าเครื่องมือทั้งหมดเชื่อมต่อกันใน Runtime** หรือได้รับสิทธิ์ดำเนินการกับระบบหลักของ W3

## Movement — การนำทางในพื้นที่

### M1 — สิ่งที่มีอยู่ในโฟลเดอร์นี้

| Path | Description |
|---|---|
| [`agent_workbench/`](agent_workbench/README.md) | พื้นที่สร้างและเก็บเครื่องมือสำหรับเอเจนท์ รวมถึง profiles และเครื่องมือตรวจสอบ |
| [`compiled/`](compiled/BOOTSTRAP_REFERENCE.md) | พื้นที่เก็บเอกสารที่รวบรวมจากบันทึก มี `BOOTSTRAP_REFERENCE.md` |
| [`hybrid_syncap/`](hybrid_syncap/HYBRID_CROSS_SYSTEM_NOTES.md) | พื้นที่เก็บบันทึกแนวคิด HybridCross / Hybrid-SynCap (สถานะ draft ตามเอกสาร) |
| [`modew_pack_template/`](modew_pack_template/README.md) | ต้นแบบ W3 Plugin / Modew Pack พร้อมโครงสร้างและขอบเขตการใช้งาน |
| [`notes/`](notes/XREA_IMPORT_TH.md) | พื้นที่เก็บบันทึกและเอกสารอ้างอิง รวมถึงบันทึกการนำเข้า REA |
| [`personal_sandbox_template/`](personal_sandbox_template/README.md) | ต้นแบบ Personal Sandbox สำหรับคัดลอกไปพัฒนาเป็นโครงการแยก |
| [`screen_translator/`](screen_translator/README.md) | โครงการแอป Android สำหรับแปลหน้าจอและอ่านภาษาไทย |
| [`sheets/`](sheets/tool_map.csv) | พื้นที่เก็บตาราง มี `tool_map.csv` |
| [`w3console/`](w3console/README.md) | System Console ทดลองสำหรับดูแผนที่ระบบ อ่านไฟล์ เขียนบันทึก และตามหลักฐานของโค้ด |
| [`xrea/`](xrea/README.md) | สำเนาซอร์สต้นทาง REA สำหรับอ้างอิงและนำไปประยุกต์ใช้ |

### M2 — เอกสารที่เกี่ยวข้องนอกพื้นที่

| เอกสาร | ความสัมพันธ์ |
|---|---|
| [AMS README](../docs/box/AMS/AMS_README.txt) | อ้างอิงรูปแบบ Head / Body / Movement / OWNER / MAKER |
| [Architecture Mapping Standard](../docs/governance/AMS.md) | เอกสาร governance ที่ README ของ Agent Workbench อ้างอิง |
| [Core vs Structure](../knowledge/philosophy/corevsstructure.md) | เอกสารแนวคิดที่ README ของ Agent Workbench อ้างอิง |

รายการ M2 นี้อ้างอิงตาม [README ของ Agent Workbench](agent_workbench/README.md) ไม่ได้ยืนยันการเชื่อมต่อ Runtime หรือสร้างอำนาจของระบบขึ้นใหม่

---

OWNER : BBX19  
MAKER : ChatGPT / Codex — จัดรูปแบบ README จากโครงสร้างและเอกสารที่ตรวจสอบได้
