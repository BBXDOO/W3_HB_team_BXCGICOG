Name : REA MCP Probe — ทดลองตรวจชิ้นงาน W3\
AM Ⅲ - BUILD : ตัวเรียก REA MCP จริงและเก็บหลักฐานผล/ข้อจำกัด\
Log time : 2026-10-25 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : W3-REA-MCP-PROBE-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาท

เครื่องมือนี้เปิด REA MCP server ผ่าน stdio ด้วย MCP SDK ที่ติดตั้งอยู่กับ REA แล้วเรียกเครื่องมือจริง ไม่มี mock และไม่เรียก implementation ภายในแทน MCP

```yaml
AM_TYPE: III
ROLE: PROCESS
DERIVED_FROM:
  - w3_tool_store/agent_workbench/README.md
  - w3_tool_store/xrea/docs/mcp-contracts.md
  - w3_tool_store/xrea/docs/sqlite-databases.md
```

ใช้ REA ที่ build แล้วในสำเนาแยกผ่าน `--rea-root` ไม่แก้ prototype ใน `w3_tool_store/xrea/` และไม่ติดตั้งลงการตั้งค่า MCP ของบัญชีหรือแอปโดยอัตโนมัติ โค้ดนี้เป็นตัวเรียกทดสอบของ W3 ยังไม่ได้คัดลอก REA core มาสร้าง editor ใหม่

### เตรียม REA แยกจากต้นแบบ

จาก root ของรีโป้ คัดลอก source ที่ Git ติดตามไปยังพื้นที่ทดลอง:

```sh
mkdir -p local_workspace/rea-runtime
git archive HEAD:w3_tool_store/xrea | tar -x -C local_workspace/rea-runtime
```

ในสำเนา REA ใช้ Node/npm ตาม `.nvmrc` และ `package.json#packageManager` ของสำเนานั้น แล้วรัน `npm ci --ignore-scripts --no-audit --no-fund` และ `npm run build:cached` รอบแรกทดสอบด้วย Node 24.18.0 / npm 11.16.0 / REA 6.5.0 การใช้ ignore-scripts ไม่ได้ยืนยันว่า optional native providers พร้อมใช้

ตัวอย่างเรียกจาก root รีโป้ หลังเตรียม offline Condien snapshot และ build REA แล้ว:

```sh
node w3_tool_store/agent_workbench/tools/rea_mcp_probe/run.mjs \
  --rea-root local_workspace/rea-runtime \
  --sqlite local_workspace/context.sqlite \
  --javascript blueprints/GGinventory/w3openland \
  --source-path core/engine.ts \
  --source-path core/storage.ts \
  --output local_workspace/rea-probe-001
```

โฟลเดอร์ output ต้องเป็นชื่อใหม่และ parent ต้องมีอยู่แล้ว เลือก Node ที่ใช้รัน server แยกได้ด้วย `--node /absolute/path/to/node` ถ้าเครื่องมือ REA SQLite ใช้ Node รุ่นไม่รองรับ จะต้องรายงาน unavailable ตามจริง

SQLite ต้องเป็น snapshot ที่หยุดเขียนแล้วหรือได้จาก backup workflow ที่ให้ consistency ฐานข้อมูลตัวอย่างรอบแรกใช้ SQLite backup ของฐาน Condien ที่ปิด writer แล้ว และเพิ่ม revision/บริบทผ่าน CondienStore ของ W3 ในสำเนาทดลอง ไม่เขียนต้นฉบับ

### สิ่งที่เรียกและหลักฐานที่เก็บ

- MCP initialize และ `tools/list` จริง เก็บรายชื่อเครื่องมือ โดยไม่พ่น output schemas ทั้งหมดออกหน้าจอ
- `binary_session` สำหรับสถานะ provider
- `inspect_sqlite_database` เลือกเฉพาะ metadata columns ของตาราง `snapshots` ไม่อ่าน payload เต็มของ Condien
- `analyze_javascript_application` สำหรับ directory ที่ระบุ และ source paths ที่เลือก
- `get_evidence_bundle` เก็บ record เต็ม รวม partial Evidence ที่ REA รักษาไว้เมื่อการวิเคราะห์หยุด
- hash ของ input ก่อน/หลัง รวม SQLite sidecars ที่มีอยู่ และผลทดลอง `ps` จาก Node โดยไม่เก็บ process-table rows หรือ ambient environment

ไฟล์ `summary.json` สรุปสถานะ `OBSERVATIONS_COLLECTED`, `BLOCKED` หรือ `STOP` ส่วนไฟล์ผลแต่ละ call เป็นคำตอบดิบจาก REA MCP การเรียกทุก tool ผ่านไม่ได้แปลว่า W3 ทำงานถูกต้องทุกกรณี และ error หรือ coverage ที่เป็น partial/unknown ห้ามตีความเป็นผลตรวจผ่าน

Exit code 0 = เก็บ observations จาก calls ที่เลือกโดยไม่มี tool error และ input ไม่เปลี่ยน; 2 = BLOCKED/STOP ดูหลักฐานก่อนตัดสิน Runtime error ก่อนเริ่ม เช่น output ซ้ำหรือ SDK ไม่พร้อม อาจจบด้วย Node error โดยยังไม่มี summary

### ผลรอบแรกในสภาพแวดล้อม ChatGPT Work

เชื่อมต่อจริงและพบ 207 tools แต่ `binary_session`, SQLite inspection และ JavaScript analysis ถูกหยุดที่ process ownership เพราะ `ps` ที่ Node เรียกจบด้วย `fatal library error, lookup self` พบอาการเดียวกันจาก Node test เล็กที่ไม่ผ่าน REA ด้วย

JavaScript call เก็บ partial Evidence ของ GGinventory ไว้ 1 record และอ่านคืนผ่าน MCP ได้ แต่ parsed JavaScript files = 0 จึงยังไม่ยืนยันผลวิเคราะห์ logic ส่วน SQLite ยังไม่มีผลตรวจ schema/rows จาก REA ข้อมูล input ที่เป็นไฟล์ปกติไม่เปลี่ยน และ prototype ไม่ถูกแก้

ไม่มีการปิดหรือข้าม ownership checks การแก้เหตุที่ `ps` ล้มจาก Node ยังไม่สำเร็จในสภาพแวดล้อมนี้ และไม่ใช่หลักฐานว่า W3 มี defect ตามรายงานนั้น

## Movement — การนำทาง

### M1 — สิ่งที่มีในโฟลเดอร์นี้

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | วิธีใช้และขอบเขตของ probe |
| [run.mjs](run.mjs) | MCP client เปิด server และเก็บผลจริง |

### M2 — เอกสารอ้างอิงนอกพื้นที่

- docs.parent : [Workbench tools](../README.md)
- docs.mcp : [REA MCP contracts](../../../xrea/docs/mcp-contracts.md)
- docs.sqlite : [REA SQLite inspection](../../../xrea/docs/sqlite-databases.md)
- docs.environment : [REA installation/prerequisites](../../../xrea/docs/installation.md)
- docs.report : [รายงานรอบแรก](../../../../modules/ChatGPT/reports/2026-10-25_REA_MCP_FIRST_USE.md)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex
