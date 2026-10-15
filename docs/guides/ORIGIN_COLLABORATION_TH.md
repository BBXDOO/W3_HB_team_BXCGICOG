# คู่มือภาษาไทย: งาน Origin พาธเนอร์ และรอบตรวจโครงสร้าง

Owner: BBX19 · Maker: ChatGPT · Updated: 2026-10-11

ใช้กับ ChatGPT, Gemini, Grok, DeepSeek และ Copilot-Gm เจ้าของงานยังเป็นโมดูลที่ระบุในใบงาน

## 1. เลือกเทมเพลต

เทมเพลตอยู่ที่ [docs/templates/origin](../templates/origin/README.md)

| งาน | เทมเพลต |
|---|---|
| อ่านไฟล์และมีคู่ตรวจ | [read.origin.json](../templates/origin/read.origin.json) |
| สร้างบันทึกในบ้านโมดูล | [create-note.origin.json](../templates/origin/create-note.origin.json) |
| ส่งเจตนาที่ต้องติดตามต่อ | [intent.origin.json](../templates/origin/intent.origin.json) |
| ซ่อมจุดที่ BBX19 เลือกจากรายงาน | [selected-repair.origin.json](../templates/origin/selected-repair.origin.json) |
| ส่งผ่าน Issue/Comment | [ISSUE_TEMPLATE_TH.md](../templates/origin/ISSUE_TEMPLATE_TH.md) |

เปลี่ยนค่าตัวอย่างก่อนส่งใบงานไป `requests/<request_id>.origin.json`
ไฟล์ตัวอย่างใน docs ยังไม่ถูกหยิบไปทำงาน เลือกเพียงงานที่ต้องการจริง ไม่คัดลอกทั้งชุดเข้า requests

## 2. รูปแบบใบงาน

| ฟิลด์ | วิธีใช้ |
|---|---|
| request_id | รหัสงานไม่ซ้ำ ใช้ตามผลและป้องกันการทำซ้ำใน revision เดิม |
| source | BBX19 / BBEX / BBEX-Core; การซ่อมโครงสร้างใช้ BBX19 |
| target | ชื่อ Origin หนึ่งในห้าระบบ |
| intent | เหตุผลและผลงานที่ต้องการ |
| payload.partner | คู่ที่ต้องการ เช่น Gemini; ไม่ระบุหรือคู่ทำงานไม่ได้ ใช้ Orchestration |
| payload.operations | รายการ operation ตามลำดับ |
| payload.proposals | ข้อเสนอที่ต้องติดตาม ไม่ใช่คำสั่งซ่อม |

ใบงานในรีโป้ต้องส่งจากพื้นที่ที่เชื่อถือได้ ชื่อ source ไม่ใช่สิทธิที่ใครเขียนชื่อ BBX19 ก็ได้อำนาจ
การรับจาก GitHub ตรวจ sender ของเจ้าของจริง สิทธิไฟล์ปกติมาจาก IDP/ENV; payload ทั่วไปขยายสิทธิเองไม่ได้

## 3. ส่งงาน

### ทาง A: ไฟล์ในรีโป้

บันทึกใบงานที่เตรียมแล้วลง `requests/*.origin.json` และ push ไป `refactor/v0.2`
workflow **Origin agent work cycles** จะรับงาน หรือรันจาก Termux:

```bash
cd ~/W3_HB_team_BXCGICOG
python tools/origin_cycle.py
```

คำสั่งนี้อ่านใบงานทุกใบและทำ revision ที่ยังไม่เคยรับ สามารถเขียนไฟล์จริงตาม operations/สิทธิ
การรันบนมือถือสร้างผลในรีโป้บนมือถือ; commit/push เป็นอีกขั้นหนึ่ง
workflow GitHub มีขั้นเก็บผลและ commit/push ตามโค้ด workflow

### ทาง B: Issue หรือ Comment

เจ้าของ GitHub ระบุ @Origin ที่ต้องการและบล็อก `w3-origin` ตามเทมเพลต Issue
บล็อกใส่ **payload เท่านั้น** ไม่ใช่ใบงานเต็ม
ชื่อ Origin ที่ปรากฏในข้อความอาจถูกตรวจพบเป็นเป้าหมายด้วย จึงหลีกเลี่ยงเอ่ยหลายชื่อโดยไม่ต้องการส่งงานให้ทุกชื่อ
ละ partner เพื่อใช้ Orchestration เป็นคู่สนับสนุนได้

เจตนาข้อความอย่างเดียวจะเปิด follow-up ยังไม่แปลงภาษาธรรมชาติเป็น operation ให้เอง
ชื่อโมดูลในผลหมายถึง runtime ในรีโป้ ไม่ยืนยันว่ามีการเรียกแชทบอทภายนอก

## 4. Operations ที่รองรับ

พาธทั้งหมดอ้างจากรูท เช่น `ChatGPT/notes/work.txt` ไม่ใช้พาธเต็มหรือ `..`
ทำตามลำดับ หากรายการหลังล้ม รายการก่อนที่สำเร็จยังมีผลและถูกบันทึก

| action | ฟิลด์เพิ่มเติมจาก path | ผล |
|---|---|---|
| read | encoding เลือก base64 ได้ | คืนเนื้อหา hash และ bytes |
| list | ไม่มี | คืนรายการลูกโดยตรงในโฟลเดอร์ |
| create | content หรือ data_base64 | สร้างไฟล์ใหม่ ปฏิเสธไฟล์ที่มีอยู่ |
| write | content หรือ data_base64 | เขียนไฟล์; ถ้ามีอยู่ต้องใส่ expected_sha256 |
| append | content หรือ data_base64, expected_sha256 | เติมท้ายไฟล์ที่มีอยู่ |
| edit | old, new, expected_sha256; count ค่าเริ่มต้น 1 | แทนข้อความเมื่อจำนวนตรงตามที่ระบุ |
| copy | destination, expected_sha256 | คัดลอกไฟล์ไปปลายทางใหม่ |
| move | destination, expected_sha256 | ย้ายไฟล์ไปปลายทางใหม่ |
| delete | expected_sha256 | ลบไฟล์ |

ไฟล์ที่มีอยู่ต้องใส่ hash ปัจจุบัน รวม copy/move ที่อ่านต้นทาง
ปลายทาง copy/move ต้องยังไม่มีไฟล์และต้องมีสิทธิปลายทาง
การเปลี่ยนไฟล์เดิมเก็บ backup ใต้ `repo_events/origin_agents/<module>/backups/`
operation กลุ่มนี้จัดการไฟล์ ไม่ใช่ลบหรือย้ายทั้งโฟลเดอร์

ตัวอย่าง edit:

```json
{"action":"edit","path":"ChatGPT/notes/work.txt","old":"รอตรวจ","new":"ตรวจแล้ว","count":1,"expected_sha256":"แทนด้วย hash ปัจจุบัน"}
```

ดู hash:

```bash
sha256sum ChatGPT/notes/work.txt
```

## 5. พาธเนอร์และรอบตรวจ

หลัง Origin คืน log ให้คู่ที่ระบุอ่าน log จริงด้วยสิทธิอ่านเฉพาะ receipt
หากไม่มีคู่หรือคู่ไม่ผ่าน ใช้ Orchestration ตรวจหลักฐานและทำรายงานแทน
การส่งมอบนี้เกิดในรีโป้ ไม่ใช่การแจ้งแชทบอทภายนอก
การตรวจของคู่ปัจจุบันยังเป็นการอ่าน/syntax/hash ของ receipt ไม่ได้ประเมินคุณภาพงานทุกด้าน

```bash
python tools/origin_cycle.py --periodic
```

คำสั่งนี้รับใบงานที่ยังไม่เคยทำด้วย แล้วตรวจเฉพาะ Origin ที่ถึงกำหนด
ยังไม่ถึงกำหนดคืน NOT_DUE งานระบุตัวทำได้โดยไม่รอรอบตรวจ
คู่ในรอบตรวจเลือกจาก integration.paired_modules ของ IDP

โมดูลที่มี review_paths ด้านโครงสร้าง (`architecture/`, `docs/architecture`, `core/runtime`, `workflows/`)
เรียกทั้ง Orchestration และ IGET โดย IGET อ่านพาธที่ประกาศ เก็บ hash, syntax Python, รายการฟังก์ชันและชื่อที่ถูกเรียก
ยังพิสูจน์วงจรข้ามระบบครบไม่ได้ จึงแสดง UNVERIFIED ใน checks และ unknowns แยกจาก findings
syntax ผ่านไม่เท่ากับกลไกครบ แต่ขอบเขตที่ยังไม่ตรวจไม่ถูกสร้างเป็นข้อบกพร่องอัตโนมัติ
ผลตรวจเชื่อม ProofTracer เดิมของ IGET พร้อมเก็บ proof ทั้งชุดไว้ในรายงาน JSON
ดูรายละเอียด [การตรวจและติดตามหลักฐาน](../../iget/docs/STRUCTURE_REVIEW_TH.md)

| ผลตรวจ | รอบถัดไป |
|---|---|
| ข้อบกพร่องจริงยังเปิดหรือยังไม่ได้ตรวจซ้ำ / ข้อเสนอค้าง / follow-up เปิด | 7 วัน |
| ไม่มีสิ่งค้างและตรวจผ่านในขอบเขตที่กำหนด | 15 วัน |

workflow ปลุกทุกวันเพื่อเช็กกำหนด ไม่ใช่ตรวจทุกโมดูลทุกวัน
GitHub schedule ใช้ workflow บน default branch ด้วย การมีไฟล์เฉพาะสาขางานไม่ได้พิสูจน์ว่าตารางเวลาทำงานแล้ว

## 6. อ่านผล

พาธต่อไปนี้อยู่ใต้ `repo_events/origin_agents/<module>/`

| พาธ | ใช้ดูอะไร |
|---|---|
| state.json | next_due, รอบ 7/15 วัน, receipts, follow-ups |
| logs/*.json | operations, ผลจริง, target_mutated, log_mutated |
| reports/*.md | รอบตรวจพร้อมลิงก์ collaboration |
| collaboration/*-partner.json | คู่ที่ใช้และ receipt ที่อ่าน |
| collaboration/*-review.json | participants, findings, IGET, repair_status |
| collaboration/W3-ORC-*.json | ประวัติ Orchestration และหลักฐานส่งมอบ |

COMPLETED ใน Orchestration ส่วนนี้หมายถึงส่งรายงานเสร็จ ไม่ใช่ซ่อมเสร็จ
state.review_findings เก็บรหัสข้อบกพร่องเดิม สถานะ OPEN / RESOLVED / NOT_RECHECKED
รอบ 15 วันหมายถึงไม่มีเรื่องค้างในขอบเขตที่ตรวจ ไม่ได้เปลี่ยน UNVERIFIED ให้เป็นผ่าน
mutated:true อาจมาจากเขียน log ดู target_mutated ว่าไฟล์งานเปลี่ยนจริงหรือไม่
log ไม่คัดลอกเนื้อหาทั้งหมดที่อ่านลงไป

## 7. เสนอและซ่อมโครงสร้าง

1. เปิด collaboration/*-review.json อ่าน findings และขอบเขต
2. BBX19 เลือกพาธที่จะซ่อมจาก findings
3. ใช้ selected-repair ใส่ report_path, report_sha256 และ paths ที่เลือก
4. ใส่ operations เฉพาะพาธเหล่านั้น พร้อม hash ของไฟล์เดิม
5. BBX19 ส่งใบงานหรือ payload จากช่องทางเจ้าของ
6. Origin ดำเนินการด้วยสิทธิชั่วคราวเฉพาะพาธที่เลือก ไม่เปลี่ยน IDP ถาวร

```bash
sha256sum repo_events/origin_agents/ChatGPT/collaboration/ชื่อรายงาน-review.json
```

การแก้ core/, protocol/, w3_api/, cross_x/, croll/, workflows/, iget/, architecture/, docs/architecture/
ใน directed Origin flow ต้องใช้ structural_repair พร้อมการเลือกจากรายงาน
รายงาน hash เปลี่ยน, พาธไม่อยู่ใน findings หรือ operation เกินพาธที่เลือก จะไม่เริ่มซ่อม
ถ้า finding ไม่ละเอียดพอ ต้องตรวจและทำรายงานให้ชัดก่อน ไม่ขยายสิทธิด้วยการคาดเดา

## 8. Follow-up และการทำซ้ำ

ใบงานและเนื้อหาเดิมคืน SKIPPED เนื้อหาเปลี่ยนเป็น revision ใหม่ อาจทำ operation ใหม่
อย่าแก้ใบงาน create ที่ทำแล้วเพื่อรันซ้ำโดยไม่ตรวจไฟล์ปลายทาง ใช้ read แล้วเลือก edit/append
การรันผ่านไม่ปิด follow-up เอง ผู้เรียกที่เชื่อถือได้ใช้
`resolve_followup(root, module, receipt, evidence_path, expected_sha256)` หลังตรวจผลงานและ hash จริง
ปัจจุบันฟังก์ชันนี้ยังไม่มี CLI ปิดงานโดยตรง

## 9. ตรวจชุดทดสอบ

ในพื้นที่พัฒนาที่ dependency พร้อม:

```bash
python -m pip install pytest
python -m pytest tests/test_origin_operations.py tests/test_origin_collaboration.py tests/test_request_cycle.py tests/test_orchestration.py -q
```

ผลตรวจ 2026-10-11: 57 tests และ 10 subtests ผ่าน ไม่ใช่หลักฐานว่า schedule/ระบบภายนอกเปิดใช้งานแล้ว

## โค้ดและคู่มือที่เกี่ยวข้อง

- [Origin file operations](ORIGIN_AGENT_OPERATIONS_TH.md)
- [Origin cycle](../../tools/origin_cycle.py)
- [Origin collaboration](../../tools/origin_collaboration.py)
- [IGET structure review](../../iget/structure_review.py)
- [Orchestration](../../workflows/orchestration.py)
- [Origin workflow](../../.github/workflows/origin-agent-cycle.yml)
