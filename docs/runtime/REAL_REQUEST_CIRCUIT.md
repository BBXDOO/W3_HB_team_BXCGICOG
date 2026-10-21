# วงจรรับใบงานจริงและผลลัพธ์ตามบริบท

- AM type: III Process
- Group: BUILD / OBSERVE / LEARN
- Owner: BBX19 / W3
- Status: implemented local path; final human sign-off retained

## เส้นทางที่เชื่อมแล้ว

`requests/*.md` ที่ประกาศ `request_type: runtime_circuit`
→ `tools/request_cycle.py` → `WorkflowRuntime` / Orchestration
→ `engine_v2.run` → executor ของแต่ละโมดูล → ตรวจผลจากไฟล์/ข้อมูลจริง
→ เก็บ snapshot / ผลแต่ละขั้น → รอการตรวจของมนุษย์เมื่อถึงเงื่อนไข

คำร้องชนิดเดิมยังใช้เส้นทางเดิม เพื่อไม่เปลี่ยนขอบเขตหรือเจตนาของคำร้องเก่า
โดยไม่ประกาศ การใช้วงจรนี้จึงเลือกได้ผ่านชนิดคำร้องอย่างชัดเจน
ตัวรับใบงานเดิมรองรับทั้งสองเส้นทางแล้ว

## งานจริงที่รันในชุดนี้

ใบงาน: [RQ-LRC2-LOG-ANALYSIS-001](../../requests/RQ-LRC2-LOG-ANALYSIS-001.md)

- ข้อมูล: `core/memory/memory_store.json` ที่มีอยู่ในรีโป้จริง ณ ตอนรับงาน
- เก็บ snapshot ข้อมูล 105 รายการก่อนการรันจะเพิ่มประวัติของตัวเอง
- LRC2 คำนวณผลจริงจากข้อมูล: 13 กลุ่มโมดูล/งาน
- สถานะในประวัติ: success 57, review 27, blocked 1, unknown 20
- ไม่พบ explicit error signature ที่เกิดซ้ำตามกฎปัจจุบัน จึงไม่สร้างแพทเทิร์นขึ้นเอง
- มี 1 กลุ่มที่มีผลสำเร็จ/ล้มเหลวครบเกณฑ์ 20 ตัวอย่างสำหรับ historical frequency
- Gemini อ่าน report และ snapshot จริง ตรวจ hash, จำนวนข้อมูล, trace และคำนวณซ้ำ
- LRC2 และ Gemini จบขั้นงานของตน ใบงานรวมอยู่ `WAITING_HUMAN`

ตัวเลข success หมายถึงสถานะที่ประวัติบันทึกไว้ ไม่ใช่การรับรองย้อนหลังว่า
ทุกงานในประวัติตอบโจทย์เดิมครบถ้วน ความไม่แน่ใจนี้แสดงอยู่ในรายงาน

รายงาน: [LRC2 log analysis](../../modules/LRC2/reports/log_analysis/cd827151abaf423584a0368eba8d08cd.json)

ผลทั้งวงจร: [request result](../../requests/results/RQ-LRC2-LOG-ANALYSIS-001_RESULT.json)

## เรียกใช้

จากรูทรีโป้:

```bash
python -m tools.request_cycle --request requests/RQ-LRC2-LOG-ANALYSIS-001.md
```

หากใบงานเดิมค้างรอคน จะไม่เรียก executor ซ้ำ และ pending scan ที่สถานะไม่เปลี่ยน
จะคืน SKIPPED โดยไม่สร้าง check-in ซ้ำ คำร้องที่เปลี่ยนเนื้อหาแต่ใช้ request_id เดิม
จะถูกปฏิเสธ ต้องใช้การ revise อย่างมีหลักฐานหรือใช้ request_id ใหม่

หลังมนุษย์ตรวจรายงานจริงแล้ว สภาพแวดล้อมที่เชื่อถือได้บันทึกการตัดสินใจได้ด้วย:

```bash
python -m tools.runtime_circuit_intake \
  --request requests/RQ-LRC2-LOG-ANALYSIS-001.md \
  --review --human BBX19 --evidence '<reference-to-actual-human-decision>'
```

คำสั่งนี้ไม่ยืนยันตัวตนผ่านเครือข่าย ผู้เรียก/host ต้องเป็นผู้ยืนยันสิทธิ์และตัวตน
และต้องอ้างการตัดสินใจที่เกิดขึ้นจริง ไม่ใส่คำอนุมัติขึ้นมาแทนมนุษย์

## ผลลัพธ์ของ LRC2 ที่มีจริง

`log_analysis` รับ `records` หรือ `source_file` ซึ่งเป็น JSON records/list หรือ JSONL
ภายในรีโป้ ใช้กฎ provisional ที่เปิดดูได้ แยก success/failure/blocked/review/
pending/cancelled/unknown โดยไม่ทิ้งรายการที่ยังไม่เข้าใจ

- จัดกลุ่มตาม module/task จาก log และรองรับรูปแบบ memory bus เดิม
- หา explicit error signature ที่ซ้ำ พร้อม record references
- สะสมคะแนน risk ในหน้าต่างล่าสุด (failure=2, blocked=1, review=0.5)
- นับ adverse streak และบอกว่าเรียงด้วย timestamp หรือใช้ลำดับข้อมูลเดิม
- แยกจำนวน outcome ที่ใช้ประมาณออกจากสถานะที่ยังไม่จบหรือไม่ทราบ
- คำนวณ historical frequency และ Wilson 95% interval เมื่อ sample ครบเกณฑ์

การประมาณมีสมมุติฐานว่ากลุ่มงานเปรียบเทียบกันได้ ยังไม่ใช่โมเดลพยากรณ์ที่ผ่าน
การสอบเทียบกับอนาคต ข้อมูลน้อยยังวิเคราะห์/จัดหมวดได้ แต่ไม่สร้างเปอร์เซ็นต์
การคาดการณ์ขึ้นมาโดยไม่มีตัวอย่างรองรับ

## Executor ตามบทบาทและบริบท

host ลงทะเบียน Python callable ผ่าน `engine_v2.run(..., executors={...})` หรือ
`request_cycle.process(path, executors={...}, verifiers={...})` ได้
callback ได้ task, plan และ context รวม intent, payload, เนื้อหาคำร้องเต็ม,
source request, ประวัติประกอบ และ trace ตัว executor อาจใช้โค้ดเฉพาะทาง,
เครื่องมือ, model service หรือการเชื่อมกับ host AI ตามสภาพแวดล้อมจริง
ไม่จำกัดว่าทุกการเชื่อมต้องเป็น API ของผู้ให้บริการรายเดียว

- การลงทะเบียนมาจาก host เท่านั้น ไม่โหลดคำสั่ง/ชื่อฟังก์ชันจาก JSON ในคำร้อง
- ตัวที่ไม่ได้ลงทะเบียนยังใช้ executor เดิมของโมดูล ไม่แทนที่ความสามารถเก่า
- ผลต้องประกาศ module ตรงกับผู้ปฏิบัติที่เลือก มิฉะนั้นผลตรวจไม่ผ่าน
- งาน/ความสามารถใหม่ต้องมี verifier ที่ตรวจผลตามโจทย์ ไม่ผ่านเพราะมีไฟล์เฉยๆ
- verifier ของ LRC2 ตรวจไฟล์กับ input snapshot จริง; Gemini คำนวณ checks เอง
  ไม่รับค่าผ่านจากใบงานมาแทนการตรวจหลักฐาน

ช่องทางลงทะเบียนนี้ไม่ได้ทำให้ทุกโมดูลมีความสามารถคิดหรือสร้างงานทุกชนิดทันที
งานที่ต้องพึ่งการให้เหตุผล/การสร้างเนื้อหาแบบ AI ต้องมี executor จริงที่ host จัดให้
จนกว่าจะมีตัวปฏิบัติและเกณฑ์ตรวจที่เหมาะสม วงจรจะไม่ยืนยันว่าโจทย์นั้นสำเร็จ

## การอนุมัติและการย้ายเครื่อง

ตัวรับใบงานใช้ review_policy=final: ขั้นกลางที่ตรวจผลผ่านเดินต่อได้ในขอบเขตที่ระบุ
และหยุดเมื่อถึง final sign-off ถ้าโมดูลใดร้องขอ review โดยตรง ยังหยุดที่ขั้นนั้นทันที
ค่าเริ่มต้นของ WorkflowRuntime สำหรับผู้เรียกเดิมยังเป็น each_stage

หลักฐานของเส้นทางรับใบงานเก็บเป็นพาธสัมพัทธ์กับรูทรีโป้ จึง clone/ย้ายไป Termux
แล้วเปิด snapshot, ตรวจรายงาน และทำต่อได้ เมื่อเรียก WorkflowRuntime โดยตรง
สามารถระบุ reference_root เพื่อเลือกการเก็บอ้างอิงแบบนี้ได้

การอ้างอิงของงานจริงที่รันก่อนเพิ่มรูปแบบพาธสัมพัทธ์ ถูกย้ายรูปแบบโดย host พร้อม
เหตุการณ์ EVIDENCE_REFERENCES_RELOCATED ใน history; ไม่ได้รันโมดูลหรืออนุมัติงานซ้ำ

## การทดสอบ

ชุดทดสอบรวมถึงค่าที่คำนวณด้วยมือจาก fixture, การเปลี่ยนโมดูล/โจทย์,
ไม่คาดการณ์เมื่อ sample ไม่พอ, input ไม่ถูกแก้, การตรวจ artifact/hash จริง,
รับใบงานจริงผ่าน request_cycle, ใช้ Gemini executor จริง, หยุดรอมนุษย์,
กันเรียกซ้ำ/สแกนพร้อมกัน, กัน report ถูกแก้หลังตรวจ และ clone ข้อมูลไปอีกรูทแล้ว review ต่อ

งานนำร่องข้างต้นใช้ประวัติจริงเพิ่มเติมจากชุดทดสอบ ไม่ใช้ fixture แทนประวัติจริง
