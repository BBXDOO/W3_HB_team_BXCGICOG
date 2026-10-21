# คู่มือ Orchestration: โฟลว เครื่องมือช่วย และคู่ทดแทน

AM: III — Process | Group: BUILD / OBSERVE / CONTINUE | Owner: BBX19

## สิ่งที่ใช้งานได้

ระบบใช้ทะเบียนความสามารถเลือกตัวทำงานจริง โดยแยกเจ้าของงาน ผู้ช่วย และผู้ตรวจผลออกจากกัน เครื่องมือช่วยคืนผลพร้อมหลักฐานให้เจ้าของเดิม ไม่รับ ownership หรืออนุมัติงานแทนมนุษย์

| Capability | ตัวทำงานที่เชื่อมแล้ว | ตรวจอะไร |
|---|---|---|
| `portable_paths` | `tools/check_portable_paths.py` | ชื่อพาธที่มีปัญหาบน Windows และชื่อชนกันแบบไม่แยกตัวพิมพ์ |
| `approval_metadata` | `tools/validate_metadata.py` | การมี reason คู่กับ approved-by ในไฟล์ |
| `file_review` | Origin executors ของ ChatGPT / Gemini / Grok / DeepSeek / Copilot-Gm | ไฟล์มีจริง hash และ Python/JSON syntax ภายในสิทธิ์ของโมดูล |

สองเครื่องมือแรกเก็บรายงานจริงที่ `repo_events/orchestration_support/` ส่วนคู่ตรวจไฟล์มี Origin execution log ของตัวเอง หลักฐาน support และการเลือกเก็บร่วมกับ task ใน runtime circuit การตรวจเหล่านี้เป็น local code ไม่ต้องเรียกบริการโมเดลภายนอก

## 1. เรียกโฟลวที่ลงทะเบียน

ในใบงาน root ที่มี `request_type: runtime_circuit` ใช้บล็อกต่อไปนี้แทนการเขียน stages เองได้:

```w3-circuit
{
  "workflow": "log_analysis",
  "input": {
    "payload": {
      "source_file": "core/memory/memory_store.json",
      "min_samples": 20,
      "window_size": 20
    }
  }
}
```

ชื่อ `log_analysis` ขยายเป็น LRC2 วิเคราะห์ → Gemini ตรวจรายงาน แผนที่ขยายแล้วจะถูกบันทึกก่อนเริ่มทำงาน Input เข้าขั้นแรก ขั้นต่อไปรับผลจากขั้นก่อนหน้า ข้อมูล log ถูก snapshot ก่อน runtime เขียนประวัติเพิ่ม รูปแบบ explicit `stages` เดิมยังใช้ได้ แต่ห้ามระบุ stages และ workflow พร้อมกัน

เรียกจาก root ของรีโป้:

```bash
python -m tools.request_cycle --request requests/YOUR_REQUEST.md
```

คง `request_id`, `target_module: LRC2`, `requester`, `final_signoff_required` และข้อมูลใบงานตาม [คู่มือวงจรเดิม](../runtime/REAL_REQUEST_CIRCUIT.md) การเลือก workflow ไม่ให้สิทธิ์เพิ่มแก่คำร้อง

เพิ่มโฟลวตามประเภทงานผ่าน trusted host:

```python
from workflows.support_catalog import FlowCatalog

flows = FlowCatalog()
flows.register("architecture_review", [
    {"id": "design", "task": "design", "module": "ChatGPT"},
    {"id": "review", "after": ["design"], "task": "verify", "module": "Gemini"},
])
# runtime ต้องมี executor/verifier ที่ทำงานประเภทนี้ได้จริงก่อน
runtime.run_flow(task, "architecture_review", {"intent": "รายละเอียดงาน"}, flows=flows)
```

ตัววางแผนตรวจ id ซ้ำ dependency ที่ขาด วงจร dependency และ module ที่ขัดกับ route ไม่สร้างความสามารถของ executor ขึ้นมาเอง สูตรสำเร็จที่ติดตั้งเริ่มต้นมี `log_analysis`; งานอื่นเพิ่มสูตรตามบริบทได้ รองรับชนิด task REQUEST / REPORT / ISSUE / SIGNAL / INTERNAL ของ Orchestration เดิม

## 2. ดูเครื่องมือและความสามารถ

```bash
python -m tools.orchestration_support --list
python -m tools.orchestration_support --inventory
```

`--list` แสดง adapter ที่ลงทะเบียน `--inventory` สำรวจ Python ใน tools/ โดยไม่ import หรือรันไฟล์ที่พบ ค่า registered หมายถึงมี adapter ไม่ได้หมายถึงเครื่องมือทุกตัวผ่าน health check หรือมีสิทธิ์ทุกงาน

## ช่วยอัตโนมัติเมื่อขั้นงานสะดุด

ระบุ requirement ในขั้นที่ต้องการให้มีผู้ช่วยไว้ล่วงหน้าได้:

```json
{
  "task": "design",
  "module": "ChatGPT",
  "request": {"intent": "รายละเอียดงาน"},
  "support": {
    "capability": "approval_metadata",
    "kind": "TOOL",
    "request": {"paths": ["docs/YOUR_OUTPUT.md"]}
  }
}
```

เมื่อขั้นนี้รันแล้วกลายเป็น BLOCKED ระบบจะเลือกและเรียกผู้ช่วยหนึ่งครั้งโดยอัตโนมัติ ถ้าตรวจผลช่วยผ่านจะหยุดที่ RETURNED ให้ host ตัดสินใจทำขั้นเดิมต่อ ไม่วนเรียก owner หรือผู้ช่วยซ้ำเอง ถ้าจะสร้างคู่เฉพาะทางใช้ `kind: SPECIALIST`, capability ที่ลงทะเบียน และ preferred ที่ต้องการแทนได้

ตัวอย่างข้างต้นใช้ได้เมื่อ blocker เกี่ยวกับ metadata และมีไฟล์ให้ตรวจแล้ว ไม่ใช่คำสั่งให้เครื่องมือนี้แก้ปัญหาทุกชนิด งานที่ไม่มี support requirement จะคง BLOCKED เพื่อให้ host เลือกวิธีช่วยตามหลักฐาน หาก runtime ไม่มี reference_root ต้องใช้ Python API กับ catalog ที่ host จัดให้; root request intake ตั้ง reference_root ไว้แล้ว

## 3. ช่วยงานที่ BLOCKED

ตัวอย่างตรวจ metadata ของไฟล์ที่เกี่ยวกับ blocker:

```bash
python -m tools.orchestration_support \
  --request requests/YOUR_REQUEST.md \
  --capability approval_metadata \
  --kind TOOL \
  --paths docs/YOUR_OUTPUT.md
```

ต้องเป็นใบงาน runtime_circuit ที่รันและบันทึกสถานะ BLOCKED แล้ว CLI ตรวจว่าเนื้อหาคำร้องตรงกับ snapshot และถือ task lock ก่อนลงมือ ข้อผิดพลาด metadata ยังคง BLOCKED และบันทึก findings โดยไม่แก้เอกสารเอง ถ้าผ่านจะเป็น RETURNED การผ่าน metadata ไม่รับรองคุณภาพเนื้อหาหรือว่าปัญหาอื่นของงานหายไป

เลือกคู่ทดแทนเพื่อตรวจไฟล์:

```bash
python -m tools.orchestration_support \
  --request requests/YOUR_REQUEST.md \
  --capability file_review \
  --kind SPECIALIST \
  --preferred Gemini \
  --paths docs/YOUR_OUTPUT.md
```

ระบบให้ preferred มาก่อน แต่จะข้ามตัวที่ไม่มี ไม่พร้อม อยู่นอก scope หรือเป็นเจ้าของงานเอง แล้วเลือกตัวที่ทำ capability เดียวกันได้ ชื่ออื่นเรียงเพื่อให้เลือกซ้ำได้อย่างแน่นอน ไม่ใช่การจัดอันดับความสามารถของโมดูล

สิทธิ์เริ่มต้นมาจาก Origin IDP ถ้าทุกตัวอ่านพาธนั้นไม่ได้ งานจะคง BLOCKED; host สามารถส่ง `authority_context` ที่ได้รับมอบหมายจริงผ่าน Python API ได้ CLI ไม่รับ authority จาก JSON คำร้อง

เมื่อต้องการลองขั้นเดิมต่อทันทีหลังช่วยผ่าน ให้เพิ่ม `--continue` ผู้ใช้ควรเลือก capability ให้ตรงกับ blocker การลองขั้นเดิมคือการเรียก owner ใหม่โดยตั้งใจ จึงไม่ควรใช้ถ้ายังมีผลข้างเคียงจากครั้งก่อนที่ต้องตรวจสอบ ไม่มีการย้อนรันขั้นที่เสร็จก่อนหน้านั้น

หากไม่ได้ใช้ `--continue` CLI บันทึก task ไว้ที่ RETURNED และยังไม่อัปเดต root result ผ่าน request_cycle เพราะการสแกนนั้นจะลองขั้นเดิมต่อ การเรียก request_cycle ครั้งถัดไปถือเป็นการสั่งทำงานต่อโดยชัดเจน ตรวจสถานะ support ล่าสุดได้จาก saved task และ CLI output

## 4. ใช้ผ่าน Python

```python
# trusted host ถือ lock ของ task ก่อนเรียก
runtime.support_for(
    task, "file_review", kind="SPECIALIST", preferred="Gemini",
    request={"paths": ["docs/YOUR_OUTPUT.md"]},
)
if task["status"] == "RETURNED":
    runtime.continue_work(task)  # เจ้าของเดิมรับงานกลับ; ตรวจผลขั้นเดิมอีกครั้ง
```

`support_for()` ใช้ default catalog เมื่อ runtime มี reference_root หรือรับ `catalog=` ที่ host สร้างเองได้ Adapter รับ task_id, source_id, payload, blocker, destination, effective stage, request และ selection โดยทำสำเนาเพื่อไม่ให้ handler เปลี่ยน task โดยตรง

## 5. เพิ่มเครื่องมือใด ๆ ใน tools/

ไม่จำเป็นต้องเขียนเครื่องมือใหม่ หากมีอยู่แล้ว ให้ host เชื่อม callable และ verifier ของเครื่องมือนั้น:

```python
from workflows.support_catalog import SupportCatalog, register_repository_tool

catalog = SupportCatalog()
register_repository_tool(
    catalog, repo_root,
    "tools/YOUR_EXISTING_TOOL.py",
    {"your_capability"},
    handler=call_existing_tool,
    verifier=check_actual_outcome,
)
runtime.support_for(task, "your_capability", catalog=catalog, request={"input": "..."})
```

`call_existing_tool(context)` ต้องคืน dict ที่มี `resolved: bool`, `mutated: bool` และข้อมูลผลจริง เช่น artifact และ hash ส่วน `check_actual_outcome(context, result)` คืน `{"passed": bool}` โดยอ่านผลจริงหรือใช้เกณฑ์ของงาน ไม่รับคำว่า success จากตัวทำงานเป็นข้อพิสูจน์เพียงอย่างเดียว Host เป็นผู้กำหนด input contract, สิทธิ์, timeout และการเชื่อมบริการเฉพาะเครื่องมือ

เครื่องมือมีผลเปลี่ยนไฟล์ได้ตามสิทธิ์ของ adapter ไม่มีข้อจำกัดว่าต้องเป็นเครื่องมือตรวจแบบอ่านอย่างเดียว การสแกนชื่อไฟล์ไม่สามารถทราบ input/ผลข้างเคียงของทุกเครื่องมือได้ จึงแยก inventory ออกจาก executable registration

## 6. เพิ่มคู่เฉพาะทางหรือการเชื่อมภายนอก

```python
from workflows.support_catalog import Adapter

catalog.register(Adapter(
    name="specialist:your_module",
    kind="SPECIALIST",
    module="YourModule",
    capabilities=frozenset({"your_capability"}),
    handler=execute_specialized_work,
    verifier=verify_specialized_result,
    available=check_connection,
    accepts=check_input_and_scope,
    request_types=frozenset({"ISSUE", "REQUEST"}),
))
```

ตัวเชื่อมอาจเป็นโค้ดภายในหรือการเชื่อมต่อภายนอก Host ดูแล credential/transport; คำร้องไม่กำหนด executable import หรือ shell command ตัว `available` ตรวจความพร้อมก่อนเลือก `accepts` ตรวจ input/scope ส่วน verifier ตรวจผลงานหลังเรียกแล้ว

## 7. พฤติกรรมของงาน Origin เดิม

`payload.partner` ยังระบุคู่ที่ต้องการได้ ถ้าระบุชื่อที่ไม่มี จะเลือก Origin อื่นที่พร้อมสำหรับ `file_review` และไม่ใช่เจ้าของงาน ให้สิทธิ์อ่านเฉพาะ receipt ของเจ้าของ ตรวจ hash/syntax และบันทึก requested partner กับ selected partner

ถ้าไม่ระบุคู่ ยังคงใช้เส้นทาง Orchestration + tools เดิม หากคู่ที่เรียกแล้วล้มเหลว จะใช้เส้นทางวินิจฉัยเดิม ไม่ลองคู่ถัดไปโดยเดาผลข้างเคียง การตรวจ receipt นี้ไม่เท่ากับมอบหมายให้คู่ใหม่สร้างเนื้อหาหรือแก้โค้ดแทนเจ้าของ งานเฉพาะทางต้องมี adapter/capability ของงานนั้น

## 8. ข้อผิดพลาดและการกู้คืน

- ไม่มีผู้ช่วยที่เหมาะสม: บันทึก selection และคง BLOCKED
- verifier ไม่ผ่าน: เก็บผลจริงและคง BLOCKED แม้ handler อ้างว่าแก้แล้ว
- ช่วยผ่าน: RETURNED; ไม่เปลี่ยน destination หรือ stage index
- การเรียกหรือการบันทึกหลังลงมือไม่แน่นอน: ReconciliationRequired; ไม่เปลี่ยนตัวช่วยแล้วทำซ้ำอัตโนมัติ
- Human gate เดิมยังมีผล; ไม่ใช้ผลช่วยงานแทนการอนุมัติ

อ้าง API `WorkflowRuntime.reconcile()` สำหรับยืนยันผลที่เกิดขึ้นจริงก่อนเริ่มใหม่ การเรียก reconcile เป็นหน้าที่ trusted host ที่ตรวจหลักฐานแล้ว ไม่ใช่การตั้ง flag เพื่อข้ามข้อผิดพลาด

## ตรวจสอบการทำงาน

```bash
python -m pytest tests/test_orchestration_support.py tests/test_orchestration_support_recovery.py tests/test_origin_collaboration.py tests/test_runtime_circuit_intake.py -q
```

ชุดทดสอบครอบคลุมไฟล์จริง การเลือกคู่ทดแทน scope/availability การตรวจผลเท็จ การเก็บผลเมื่อบันทึกล้มเหลว และการคืนงานหลังรีสตาร์ต ไม่ได้ยืนยันความสามารถของบริการภายนอกที่ยังไม่ได้เชื่อม
