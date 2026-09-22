---
request_id: RQ-CAST-PLATFORM-W3-DATAFLOW-001
task_keyword: structural_review
target_module: Copilot-Gm
requester: BBX19
language: th
request_type: paired_module_flow_study
authority_requested: create_report_and_private_pattern
final_signoff_required: true
mutated: false
review: true
---

# Request: Platform ↔ W3 Data Flow Cycle Test

## Intent

ทดสอบวงจร Request จริง โดยให้ `Copilot-Gm` เป็นคู่โมดูลสำหรับตรวจและจัดรูปความสัมพันธ์ของข้อมูลระหว่าง Platform กับ W3 ว่าแต่ละส่วนรับอะไร ส่งอะไร และส่งต่อไปยังส่วนใด โดยยึดโครงสร้างที่มีอยู่ใน repository ก่อน

งานนี้ต้องสร้างผลลัพธ์แยก 2 ชนิด:
1. **Report** — รายงานสำหรับการตรวจ/review
2. **Private Pattern** — บันทึกรูปแบบการมอง/จัดโครงสร้างของ Cast แยกจากรายงาน เพื่อใช้เป็นประสบการณ์/รูปแบบภายในของโมดูล ไม่ให้ปะปนกับข้อเท็จจริงของรายงาน

## Pair Module

- Primary/paired module: `Copilot-Gm`
- Requested workspace: `modules/Copilot-Gm/`
- ใช้ความสามารถขั้นต่ำของโมดูล: read / reason / structural adaptation / document / report
- Specialty เป็นเหตุผลในการเลือก Copilot-Gm ไม่ใช่ข้อห้ามความสามารถอื่น

## Source / Evidence First

ให้อ่านของจริงก่อน โดยอย่างน้อยตรวจ:
- `docs/architecture/mytec_info/W3UNIVE.md`
- `w3_api/`
- `cross_x/`
- `config/ecosystem.json`
- `config/cross_system.json`
- source/protocol ที่ถูกอ้างถึงจากเอกสารเหล่านี้เท่าที่จำเป็น

ห้ามเติม flow ที่ source ไม่รองรับโดยไม่แยกเป็น observation/proposal/unknown

## Task

สร้างวงจรข้อมูล `Platform ↔ W3` โดยตอบอย่างน้อย:

1. Platform/external side ส่งข้อมูลชนิดใดเข้าสู่ W3
2. จุดรับแรกของ W3 คืออะไร และ normalize/shape อะไร
3. จากจุดรับ ข้อมูล/packet/plan/signal ถูกส่งต่อไปยังระบบใด
4. แต่ละระบบ **รับอะไร → ทำอะไร → ส่งอะไรต่อ**
5. จุดใดเป็น gateway-only / plan-only / preview-only / append-only / executor
6. เส้นทาง return จาก W3 กลับ Platform มีอะไรบ้าง
7. จุดใดยังเป็น unknown หรือยังไม่มี runtime connection จริง
8. แยกเส้นทางที่ source ยืนยันแล้ว ออกจากเส้นทางที่เป็นเพียง proposed/possible flow

## Minimum Flow Shape

ใช้รูปแบบนี้เป็นขั้นต่ำ แต่ Cast สามารถปรับ representation ได้:

```text
Platform / External
  ↓ send: ...
W3 entry / gateway
  ↓ receive: ...
  ↓ produce: ...
Next system
  ↓ receive: ...
  ↓ return/handoff: ...
...
W3 return boundary
  ↓
Platform / External
```

และสร้างตารางขั้นต่ำ:

| Node/System | Receives | Activity | Sends/Returns | Boundary | Evidence |
|---|---|---|---|---|---|

## Output A — Report

สร้างรายงานที่:

`modules/Cast/reports/RQ-CAST-PLATFORM-W3-DATAFLOW-001_REPORT.md`

รายงานต้อง:
- อ้าง `request_id`
- แยก FACT / OBSERVATION / UNKNOWN / PROPOSAL
- มี data-flow diagram แบบข้อความ
- มี receive/send matrix
- ระบุ evidence path
- ไม่ตีความ plan/preview เป็น execution จริง
- ไม่ประกาศ CLOSED; รอ BBX19 final sign-off

## Output B — Cast Private Pattern

สร้างบันทึกแยกจากรายงานที่:

`modules/Cast/artifacts/private/RQ-CAST-PLATFORM-W3-DATAFLOW-001_PATTERN.md`

บันทึกนี้ใช้เก็บ **รูปแบบ/ประสบการณ์ในการจัดความสัมพันธ์ของ Cast** จากกิจกรรมนี้ เช่น:
- วิธีแยก receive / transform / handoff / return
- วิธีแยก fact จาก inferred connection
- pattern ที่ Cast เห็นว่านำกลับมาใช้กับ flow อื่นได้
- unexplained points ที่ควรเก็บไว้สำหรับกิจกรรมครั้งถัดไป

กติกา:
- ห้ามให้ private pattern กลายเป็น source truth ของ Platform/W3
- ต้อง trace กลับ request และ report ได้
- ถ้ามีข้อสรุปใหม่ที่ source ไม่ยืนยัน ให้ติดป้าย observation/unknown
- ไม่ rewrite source documents

## Return Contract

คืนอย่างน้อย:
- status
- request_id
- module: Cast
- report_path
- private_pattern_path
- evidence
- unknowns
- mutated
- review
- final_signoff_required
- closed: false

## Completion Condition

การทดสอบระดับ artifact ถือว่าสำเร็จเมื่อมีทั้ง:
- Report จริงใน `modules/Cast/reports/`
- Private Pattern จริงใน `modules/Cast/artifacts/private/`
- ทั้งคู่ trace กลับ `RQ-CAST-PLATFORM-W3-DATAFLOW-001`

การ route/acknowledge เพียงอย่างเดียวไม่ถือว่าสำเร็จ และ final closure ต้องรอ BBX19 sign-off.
