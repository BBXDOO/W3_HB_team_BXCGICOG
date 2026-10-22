# Callback — วงจรคำตอบฝั่งมนุษย์

AM: III / Process | Group: BUILD / OBSERVE / CONTINUE | Owner: BBX19

## Head — ใช้ทำอะไร

เก็บเทมเพลตและฟอร์มคำตอบของ BBX19 / BBEX ให้เชื่อมกับใบงานเดิม ใช้คำตอบเดียวตั้งแต่รักษาเจตนา บันทึกคำตัดสิน ไปจนถึง Orchestration เปลี่ยนสถานะและส่งงานต่อ

**ใช้งานจากมือถือ:** เปิด `callback_path` ในผลรายงาน → แก้คำตอบในไฟล์ → commit ที่สาขา `refactor/v0.2` ด้วยบัญชีเจ้าของรีโป้ → ระบบบันทึกคำตอบและอัปเดตผลใบงานเดิม

ระบบไม่กรอกคำอนุมัติให้ล่วงหน้า และไม่ถือว่า BBX19 ตรวจเองหากผู้รับมอบหมายเป็นผู้ดำเนินการ

## Body — ส่วนประกอบ

| พื้นที่/โค้ด | หน้าที่ |
|---|---|
| [templates/](templates/README.md) | แบบมอบหมาย ตอบรับ คืบหน้า ขอช่วย ส่งมอบ และคำตัดสิน |
| [responses/](responses/README.md) | ฟอร์มที่ผูกกับงานจริง ระบบสร้างให้เมื่อรอคำตอบ |
| `workflows/human_callback.py` | เชื่อม intent ของ BBEX กับ decision ของ BBX19 และสถานะ Orchestration |
| `tools/human_callback.py` | จุดใช้งานเดียวสำหรับรัน เตรียม ตอบ และกู้คืน |
| `tools/human_callback_legacy.py` | นำผลเก่ามาเชื่อมโดยไม่เรียก executor เดิมซ้ำ |
| `.github/workflows/w3_human_callback.yml` | รับคำตอบจากเจ้าของรีโป้บน GitHub |

## Movement — ตอบรายงานบน GitHub

1. เปิด `requests/results/REQUEST_ID_RESULT.json` แล้วดู `callback_path` ซึ่งจะระบุไฟล์ JSON ใน responses/
2. เปิดไฟล์นั้น เลือกแก้ไขด้วยปุ่มดินสอ
3. แก้เฉพาะ `kind`, `decision` หรือ `message_type`, `reason`, `annotations`, `evidence` ไม่แก้ `binding`, `request_id`, `schema`
4. ใส่เหตุผลและขอบเขตที่ต้องการให้ชัด แล้ว commit ไป `refactor/v0.2` ด้วยบัญชี BBXDOO ซึ่งเป็นเจ้าของรีโป้
5. ดู Actions ชื่อ **W3 Human Callback** แล้วกลับไปดูผลใบงานเดิม ระบบแจ้งสถานะจริง ไม่ถือว่า commit สำเร็จเท่ากับงานเสร็จ

ตัวอย่างส่วนที่ต้องแก้สำหรับตรวจรับ:

```json
"kind": "DECISION",
"decision": "APPROVE",
"reason": "ตรวจผลตามขอบเขตและข้อจำกัดแล้ว ยอมรับรายงานรอบนี้",
"annotations": ["ส่วนความสามารถที่ยังไม่ครบให้พัฒนาต่อ"],
"evidence": []
```

คงส่วนอื่นของฟอร์มไว้ การ commit ฟอร์มโดยเจ้าของบัญชีและ URL ของ Actions run เป็นหลักฐานที่ host บันทึกเพิ่มให้ ใส่ลิงก์รายงานหรือความคิดเห็นเพิ่มใน evidence ได้ ฟอร์มเปล่าไม่ถูกประมวลผลเป็นการอนุมัติ

ถ้าแก้ผ่าน PR ให้เจ้าของรีโป้เป็นผู้ merge เพื่อสร้าง owner event ถ้า event มาจากบัญชีอื่น workflow จะไม่รับเป็นคำตัดสินของ BBX19

สำหรับรายงานเก่าที่ยังไม่มี callback_path ให้เตรียมก่อนด้วยคำสั่งในหัวข้อถัดไป หรือใช้ workflow_dispatch โหมด prepare เมื่อ workflow นี้แสดงในเมนู Actions แล้ว เลือกสาขา refactor/v0.2 และระบุพาธคำร้อง

## คำตอบแต่ละแบบมีผลอย่างไร

| kind / ค่า | ผลต่อวงจร |
|---|---|
| DECISION / APPROVE | BBX19 บันทึกคำตัดสิน → ตรวจผลงานซ้ำ → เดินแผนเดิมต่อ อาจจบหรือไปรอผลขั้นถัดไป |
| DECISION / REVIEW | บันทึกข้อแก้ไข ผูกกับเจ้าของและขั้นเดิม เข้า BLOCKED เพื่อแก้/ขอเครื่องมือช่วย |
| DECISION / HOLD | เก็บเหตุผลพัก อยู่ที่ gate/blocker เดิม ยังไม่อนุมัติ |
| DECISION / REJECT | จบคำร้องเป็น REJECTED โดยไม่รายงานว่างานสำเร็จ |
| DECISION / CANCEL | จบคำร้องเป็น CANCELLED โดยไม่ย้อนลบผลงานที่เกิดแล้ว |
| NOTE / ACKNOWLEDGE | บันทึกว่ารับทราบ ไม่มีสิทธิ์อนุมัติแฝง |
| NOTE / PROGRESS | บันทึกความคืบหน้าในวงจรเดิม |
| NOTE / HELP | บันทึกว่าต้องการความช่วยเหลือ ยังไม่เดา capability หรือรันเครื่องมือจากข้อความ |
| NOTE / DELIVER | บันทึกการส่งมอบและหลักฐาน ยังต้องผ่าน executor/verifier และการตรวจรับตามเงื่อนไข |

NOTE ใช้ `decision: ""` และเพิ่ม `message_type` ตามตาราง รายการส่งมอบหรือขอช่วยเป็นข้อมูลสำหรับประสานงาน ไม่เปลี่ยนสถานะเป็นสำเร็จโดยลำพัง

หลัง REVIEW ผู้ดูแลวงจรใช้ `revise_stage()` หรือ `support_for()` ของ runtime เดิมตามปัญหาและสิทธิ์ ไม่ต้องเปิดใบงานคนละสาย การเปลี่ยน input ต้องผูกหลักฐานการแก้ไขและตรวจผลใหม่ก่อนอนุมัติ

## ใช้ผ่าน Termux หรือ trusted host

เริ่มใบงานด้วยไฟล์จาก assignment.template.md วางใน requests/ แล้วเรียก:

```bash
python -m tools.human_callback --request requests/YOUR_REQUEST.md --run
```

เตรียมฟอร์มให้คำร้องที่มีผลอยู่แล้ว:

```bash
python -m tools.human_callback --request requests/YOUR_REQUEST.md --prepare
```

แก้ฟอร์มตาม callback_path แล้วใช้:

```bash
python -m tools.human_callback \
  --request requests/YOUR_REQUEST.md \
  --apply BBEX-Core/private/callback/responses/YOUR_GENERATED_FORM.json \
  --human BBX19 \
  --evidence 'ลิงก์คำตอบจริงหรือบันทึกคำตัดสิน'
```

ผลบนเครื่องยังต้อง commit/push เพื่อให้ GitHub เห็น คำสั่งนี้ไม่ push เอง ส่วน GitHub workflow จัดการบันทึกผลขึ้นรีโป้ให้

ทางเดิม `python -m tools.runtime_circuit_intake --request ... --review --human BBX19 --evidence ...` ยังใช้ได้ แต่เรียก pipeline เดียวกันแล้ว ไม่ข้าม BBEX/BBX19 ไปตั้ง approval อีกชุดหนึ่ง

## การมอบหมายให้ตัวแทน

Local host ใช้ `--human BBX19 --actor Codex --delegation-evidence 'คำมอบหมายจริง'` พร้อม evidence ของคำตอบ ตัวตนของผู้มอบหมาย ผู้ดำเนินการ และหลักฐานถูกบันทึกแยกใน receipt GitHub owner workflow นี้ใช้คำตัดสินตรงจากเจ้าของบัญชี ไม่รับการอ้างชื่อ BBX19 จาก callback JSON

ดู [แบบมอบหมาย](templates/delegation.template.md) การเขียนชื่อผู้อนุมัติใน JSON อย่างเดียวไม่สร้างอำนาจ การยืนยัน identity เป็นหน้าที่ host; CLI เป็นขอบเขตผู้ปฏิบัติงานที่ได้รับสิทธิ์แล้ว ไม่ใช่ public API

## เจตนาและหลักฐานที่เชื่อมกัน

- ใบงานต้นฉบับถูกผูกด้วย hash และเก็บข้อความไว้ใน intent_record ของ BBEX
- desired_outcome ใช้ค่าที่คุณระบุ ถ้าใบงานเก่าไม่มี ใช้เงื่อนไขผลและการตรวจของแผนเดิม พร้อมบันทึกว่ามาจากการแปลง contract ไม่ใช่ข้อความใหม่จากมนุษย์
- คำตอบผูก task_id, intent_id, stage index, stage hash และ result hash
- BBX19 สร้าง decision_record ที่ชี้กลับ intent_id และระบุขั้นงานที่ตัดสิน
- Orchestration ใช้ receipt เดียวกันเป็นหลักฐานของ human approval/คำตอบ และอัปเดต root result, Check-in, request log และ memory
- การส่งคำตอบเดิมซ้ำเป็น SKIPPED โดยไม่รันเจ้าของงานซ้ำ ฟอร์มเก่าใช้กับผลใหม่ไม่ได้

บันทึกหลักอยู่ใน `repo_events/runtime_circuit/TASK_ID/human-callback-*.json` ส่วนสถานะล่าสุดอยู่ใน `repo_events/runtime_circuit/tasks/TASK_ID.json` ชื่อ private จัดพื้นที่ตาม W3 ไม่ได้เปลี่ยนสิทธิ์ของ GitHub repository

## รายงานเดิมและขอบเขตความสามารถ

คำร้อง runtime_circuit ใหม่เตรียมฟอร์มให้อัตโนมัติ งานเก่าที่มี root result นำเข้าผ่าน --prepare ได้โดยรักษา receipt เก่าเป็นสำเนาหลักฐานและไม่สร้างผลงานซ้ำ งานเอกสารเดิมมีตัวตรวจไฟล์ hash และเกณฑ์คู่มือก่อนอนุมัติ

งานเก่าที่ยังไม่มีผลงานจริง เช่น BBX19 กำลังรอคำตัดสินแต่ไม่มีรายงานที่ต้องการ สามารถตอบ NOTE / HOLD / REVIEW / REJECT / CANCEL ในวงจรเดียวกันได้ การ APPROVE จะไม่ทำให้ executor ที่ยังทำงานไม่ได้กลายเป็นสำเร็จ ต้องเติมตัวทำงานและเกณฑ์ตรวจของงานนั้นก่อน

ตัว BBX19Agent และ BBEXCoreAgent ยังเป็นตัวเชื่อมฝั่งมนุษย์ ระบบเก็บและส่งต่อสิ่งที่ได้รับมอบหมาย โดยไม่สร้างตัวตนมนุษย์จำลองขึ้นมาทำการตัดสินแทน

## การกู้คืน

GitHub worker commit/push receipt สถานะ PENDING ก่อนเริ่มเปลี่ยนสถานะหรือเดิน executor ต่อ หากบันทึกปลายทางหรือการเชื่อมต่อล้มเหลว ระบบจะไม่ใช้คำตอบนั้นซ้ำเอง หลักฐานการกู้คืนเก็บเป็น Actions artifact ด้วย 14 วัน

ผู้ดูแลต้องตรวจผลจริงก่อนยืนยันผ่าน trusted host:

```bash
python -m tools.human_callback \
  --request requests/YOUR_REQUEST.md \
  --reconcile CALLBACK_ID \
  --outcome NOT_APPLIED \
  --human BBX19 \
  --evidence 'หลักฐานว่าไม่มีการดำเนินการเกิดขึ้น'
```

NOT_APPLIED อนุญาตให้ส่งคำตอบเดิมใหม่เมื่อยืนยันว่า task ยังไม่เดินต่อ APPLIED ใช้ยืนยันผลที่เกิดแล้ว ไม่ตั้ง task เป็น COMPLETED แทนการตรวจ หาก approval เคยเกิดแล้วต้องมีหลักฐานตรง receipt และกรณีที่ executor ถูกขัดจังหวะยังใช้ reconciliation ของ runtime เดิม

## ทดสอบและอ้างอิง

```bash
python -m pytest tests/test_human_callback.py tests/test_human_callback_event.py tests/test_human_callback_legacy.py tests/test_bbex_intent.py tests/test_bbx19_action.py -q
```

IDP อ้างอิง: BBX19 v2.0 และ BBEX-Core v2.1 ที่ `BBX19/modules/BBX19/idp/IDP-V2.0/` ไม่คัดลอกเนื้อหา private IDP ลงในเทมเพลต

## ลิงก์ตอบกลับท้ายรายงาน

ผลใบงานมี `report_path` ชี้ไปยังรายงานอ่านง่ายที่ `requests/results/REQUEST_ID_REPORT.md` ด้านล่างมีลิงก์เปิดฟอร์มคำตอบของงานนั้นและคู่มือ ลิงก์เดียวกันแสดงท้าย execution report ใน repo_events/ ด้วย ไฟล์ผลของ executor ที่มี hash เช่น LRC2 JSON จะไม่ถูกแก้เพื่อแทรกลิงก์ แต่แนบเป็นผลงานต้นฉบับในรายงานอ่านง่าย

หากมี PR ที่เกี่ยวข้อง ให้ระบุ `discussion_url` ในใบงานก่อนเริ่ม หรือเพิ่มภายหลังใน [channels.json](channels.json) ตาม request_id โดยไม่ต้องแก้คำร้องเดิมที่ผูก hash ไว้ ระบบจึงแสดงลิงก์ไปคอมเมนต์ PR เพิ่มด้วย และจะไม่เดาหมายเลข PR เอง

คอมเมนต์เป็นช่องทางสื่อสาร/หลักฐาน การใช้ฟอร์มและ owner callback workflow เป็นทางที่เปลี่ยนสถานะอัตโนมัติ หากตอบเฉพาะคอมเมนต์ ยังต้องให้ trusted host นำคำตอบนั้นเข้าวงจรพร้อมหลักฐาน งานที่ปิดแล้วจะแสดงว่าจบแล้วและไม่ขอตรวจรับซ้ำ
