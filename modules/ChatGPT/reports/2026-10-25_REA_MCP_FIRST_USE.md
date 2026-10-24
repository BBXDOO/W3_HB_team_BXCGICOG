# REA MCP — ทดลองกับชิ้นงาน W3 ครั้งแรก

วันที่ตามบริบทผู้ใช้: 2026-10-25 (Asia/Bangkok)

## งานที่ลองจริง

ใช้ source snapshot ใน `w3_tool_store/xrea` รุ่น REA 6.5.0 คัดลอกไปพื้นที่รันแยก ติดตั้งด้วย Node 24.18.0 / npm 11.16.0 ตามของโครงการ `npm ci --ignore-scripts --no-audit --no-fund` ติดตั้งสำเร็จ และ `npm run build:cached` ผ่าน 3 tasks มี bundler warnings เรื่อง ineffective dynamic import 2 รายการ การรันเป็น source copy จึงไม่มี git metadata สำหรับ dirty-cache hash และ remote caching ถูกปิดตามผล build

ไม่แก้ prototype ไม่ติดตั้ง server ลง client settings ไม่เพิ่ม provider ไม่ปิด process ownership checks และไม่เปลี่ยน source ของ W3 เพื่อให้ผลตรวจผ่าน

เป้าหมาย:

1. Offline SQLite snapshot ที่ได้จาก W3 CondienStore มีสอง revisions และหนึ่งบริบทที่เชื่อม predecessor เป็นชิ้นงานทดสอบที่เตรียมด้วย API จริงในสำเนาแยก ไม่ใช่ผลที่ REA ตรวจยืนยันแล้ว
2. โครงการ `blueprints/GGinventory/w3openland` เลือก `core/engine.ts` และ `core/storage.ts` สำหรับ static JavaScript/TypeScript analysis

## ผล MCP

| ขั้น | ผลที่สังเกต |
|---|---|
| initialize + tools/list | เชื่อมต่อได้จริง พบ 207 tools |
| binary_session | error ขณะตรวจ provider readiness เพราะ process ownership prerequisite |
| inspect_sqlite_database | ถูกปฏิเสธก่อน worker ตรวจ schema/rows ไม่มีผลตรวจ SQLite จาก REA |
| analyze_javascript_application | เก็บ partial Evidence ได้ แต่หยุดก่อน parse source ผ่าน worker |
| get_evidence_bundle | อ่าน retained record กลับผ่าน MCP ได้จริง 1 record |
| input hashes ก่อน/หลัง | ตรงกัน รวม SQLite sidecars ที่ตรวจใน probe |
| prototype diff | ไม่มีการเปลี่ยนแปลง |

สถานะรวม **BLOCKED** ไม่ใช่ผลตรวจผ่านของระบบ W3

## ข้อจำกัดที่ทำซ้ำได้

REA เรียก `ps -axo pid=,ppid=,pgid=,uid=,stat=,command=` แล้วได้ `fatal library error, lookup self` จึงปฏิเสธการเตรียม owned process

Node test เล็กที่เรียกคำสั่งเดียวกันโดยไม่ใช้ REA ก็ได้ exit 1 เช่นกัน ทั้ง Node 24.18.0 ที่ pin ไว้และ Node 24.22.1 ในเครื่อง ส่วนการเรียก ps โดยตรงจาก shell/Python ใน exec surface ผ่าน การสังเกตนี้แยกปัญหาการเรียก process ใน host ออกจากเนื้องาน W3 ได้บางส่วน แต่ยังไม่ได้ยืนยัน root cause ระดับระบบ

เอกสาร REA ระบุ prerequisite นี้ใน `docs/installation.md` ส่วน Linux owned-process จึงยังไม่ควรข้าม check หรือสรุปว่าเป็น defect ของ Condien/GGinventory

มีการลองเส้นทางเปิด directory/ZIP เพิ่มเติมในช่วงสำรวจ: directory ผ่าน open_binary ไม่รองรับและต้องใช้ analyze_javascript_application ตามคำแนะนำ ส่วนการเปิด ZIP ติด readiness prerequisite เดียวกัน ผลสรุปหลักด้านบนมาจาก probe ที่เลือก API JavaScript ถูกทางแล้ว

## สิ่งที่ partial Evidence บอกได้

REA เก็บ graph และ source-selection metadata ของ GGinventory ไว้ แม้ขั้นวิเคราะห์หยุด record มี artifact graph 75 nodes / 74 edges แต่ coverage เป็น partial; semantic graph มี 31 nodes / 0 relations และ coverage เป็น partial

`parsed_javascript_files=0`, `skipped_javascript_files=2`, `findings=0` **จึงไม่ใช่หลักฐานว่าโค้ดไม่มีข้อผิดพลาด** ห้ามใช้จำนวน graph nodes แทนการยืนยันว่าตรวจ logic สำเร็จ

จุดที่เห็นประโยชน์จริงรอบนี้คือ MCP boundary, diagnostic และการรักษา partial Evidence ให้เอเจนท์นำมาพิจารณาต่อได้ ส่วนการใช้วิเคราะห์ W3 เต็มทางยังต้องแก้ host prerequisite ก่อน

## ทางใช้ต่อ

- [REA MCP probe และวิธีเรียกซ้ำ](../../../w3_tool_store/agent_workbench/tools/rea_mcp_probe/README.md)
- [Structured observation summary](2026-10-25_rea_mcp_first_use.json) — ระบุ evidence ID, coverage, diagnostics, source/prototype identity และ hash ของ raw files
- [REA SQLite contract](../../../w3_tool_store/xrea/docs/sqlite-databases.md)
- [REA process prerequisites](../../../w3_tool_store/xrea/docs/installation.md)

Raw MCP replies และ complete retained bundle ถูกเก็บใน output directory ของ probe ระหว่างการรัน Structured summary เป็นสรุปที่ถอดจาก observations ไม่ใช่ canonical bundle สำหรับนำเข้า REA
