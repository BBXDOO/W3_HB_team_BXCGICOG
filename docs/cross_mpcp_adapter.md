# Cross → MPCP Adapter Standard

## Purpose

Cross วางแผนและรักษา trace ส่วน MPCP ควบคุมการ execute ผ่าน Modew
adapter นี้เป็น boundary ระหว่างสองบทบาท และห้าม Cross planner ให้สิทธิ์ execute
แก่ตัวเอง

```text
Cross-X / E-CS
      ↓ plan
Cross-L / Cross-Code envelope
      ↓ normalize
Cross-MPCP handoff
      ↓ approval gate
MPCP → one Modew task
      ↓ result
immutable E-CS return binding
```

## Required contracts

### Cross envelope

- `kind=cross-code-dispatch`
- มี `chain_id` และ `event_id`
- state ต้องพร้อม ไม่ใช่ `inactive` หรือ `review`
- `execution_allowed` ต้องยังเป็น `false`

### MPCP handoff

สร้างด้วย `build_cross_mpcp_handoff(...)` และมี:

- identity ตรงกับ E-CS
- Modew `task` เพียงหนึ่งงาน
- context ที่ไม่สามารถ override `TASK`
- `review_approved=true` เมื่อ human/governance review เสร็จแล้ว
- ไม่ให้ execution authority ด้วยตัวเอง

### Approval

`MPCPExecutionApproval` ผูกสิทธิ์กับ:

- chain เดียว
- event เดียว
- task เดียว
- reviewer ที่ระบุได้
- capability `cross.mpcp.execute`

approval ของ event หรืองานอื่นใช้แทนกันไม่ได้

## Return contract

MPCP result ถูกห่อเป็น:

```json
{
  "adapter_version": "1.0",
  "handled": true,
  "executed": true,
  "task": "verify",
  "approved_by": "BBX19",
  "state": "SUCCESS",
  "mpcp": {
    "state": "SUCCESS",
    "cause": "verify",
    "result": "verified"
  }
}
```

จากนั้น `bind_event_return(...)` จะสร้าง `EventChain` ชุดใหม่:

- ไม่แก้ chain เดิม
- terminal event รับ return ได้ครั้งเดียว
- event สถานะ `waiting` resume ได้ โดย return เดิมจะย้ายเข้า `return_history`
- `SUCCESS/done/ready` → `completed`
- `WAIT/wait/warn/run/idle` → `waiting`
- `STOP/fail/block/unknown` → `stopped`
- chain ใดมี event `stopped` จะมี state `stopped`
- `mutated` จะเป็นจริงเฉพาะเมื่อ MPCP result ประกาศชัดเจน

## Fail-closed rules

adapter ต้องไม่เรียก executor เมื่อ:

- identity ไม่ตรง
- approval scope ไม่ตรง
- capability ขาด
- review ยังไม่ผ่าน
- event ไม่อยู่ในสถานะ `planned`
- event มี return อยู่แล้ว
- context พยายาม override `TASK`
- context มี MPCP delimiter

executor ที่คืนค่าชนิดอื่นแทน mapping หรือคืน state ที่ไม่รู้จัก จะถูกบันทึกเป็น
`STOP` ไม่ถือเป็น success

## Example

```python
from cross_x import (
    MPCPExecutionApproval,
    build_cross_mpcp_handoff,
    execute_cross_handoff,
)

handoff = build_cross_mpcp_handoff(
    cross_code_envelope,
    task="verify",
    context={"BOUNDARY": "read_only"},
    review_approved=True,
)
approval = MPCPExecutionApproval(
    chain_id=chain.chain_id,
    event_id=handoff["event_id"],
    task="verify",
    approved_by="BBX19",
)
result = execute_cross_handoff(chain, handoff, approval)
updated_chain = result.chain
```
