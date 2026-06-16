# ROT_PAPER.md

MPCP Core Rotation Paper — System Control Framework

---

## PURPOSE

ROT คือกรอบหลักของระบบ  
ใช้กำหนด “วิธีทำงาน” ไม่ใช่ “ขั้นตอนทำงาน”

ROT defines how the system behaves  
NOT what the system executes

---

## CORE LAW

```text
SYSTEM = CAUSE → ACTION → RESULT
```

Rule:

- RESULT must be traceable to ACTION
- ACTION must be traceable to CAUSE
- Missing link = invalid system state

```text
NO TRUE / FALSE
ONLY RELATION
```

---

## STRUCTURE LAW

1. Structure comes before logic
2. Boundary comes before execution
3. Meaning comes before format

---

## SYSTEM LAYERS

```text
ROT      = Framework (rules & boundary)
PAPER    = Task definition (execution intent)
MODEW    = Execution unit
RESULT   = Outcome
PRX      = Perception (visual layer)
```

---

## AUTHORITY RULE

Flow direction:

```text
ROT → PAPER → MODEW → RESULT → PRX
```

Reverse control is forbidden.

- PRX ห้ามย้อนควบคุมระบบ
- RESULT ห้ามแก้ย้อนหลัง
- MODEW ห้ามออกนอก scope
- PAPER ห้ามข้าม ROT

---

## BOUNDARY LAW

ทุกการทำงานต้องมีขอบเขต

```text
IF scope is undefined
→ execution is invalid
```

---

## PAPER CONTROL LAW

Paper ต้องกำหนดให้ครบ:

```text
TASK:
SCOPE:
INCLUDE:
EXCLUDE:
MODEW:
CONDITION:
OUTPUT:
```

กฎ:

- ห้ามกว้าง
- ห้ามตีความ
- ห้ามข้ามขอบเขต
- ต้องระบุ “ใครเกี่ยว / ไม่เกี่ยว”

Paper validation rule:

A Paper is invalid if:

- SCOPE is missing
- INCLUDE / EXCLUDE is undefined
- MODEW is ambiguous
- OUTPUT is unclear

---

## MODEW LAW

```text
One Modew = One Purpose
```

- ห้ามรวมหลายหน้าที่
- ห้ามตีความเอง
- ทำตาม PAPER เท่านั้น

Modew constraint:

- Must not create new scope
- Must not access undefined layer
- Must not modify external state without Paper

---

## RESULT LAW

```text
RESULT = what happened
NOT what expected
```

- ห้ามแก้ RESULT
- ห้ามตกแต่ง RESULT
- RESULT ต้อง trace ได้

RESULT must include:

- action result
- related context
- environment snapshot (non-reduced)

---

## ERROR LAW

```text
ERROR = RESULT TYPE (misalignment)
```

ERROR is not always failure.  
ERROR is not always bug.  
ERROR is a signal of misalignment.

กฎ:

- Do not fix result
- Trace back to cause/action

---

## EXECUTION LAW

```text
ROT validates
PAPER defines
MODEW executes
RESULT records
PRX displays
```

---

## PROHIBITION

ห้าม:

- ใช้ RESULT ตัดสินย้อนหลัง
- ใช้ COLOR แทนความจริง
- ใช้ MODEW นอก scope
- ข้าม PAPER
- แก้ข้อมูลระหว่าง run

---

## PRX (LINE C) LAW

```text
PRX = perception only
```

PRX ใช้เพื่อ “เห็นเร็ว”

PRX is not logic.  
PRX is not truth.

```text
Color = signal
NOT decision truth
```

PRX must not:

- trigger execution
- override result
- hide critical state

---

## DECISION LAW

Fast decision allowed (Line C), but it must not replace trace.

---

## FLOW LAW

```text
EVENT
→ ROT check
→ PAPER assign
→ MODEW run
→ RESULT
→ PRX (optional)
```

---

## LEARNING LAW

Learning requires explanation.

ต้องตอบได้ว่า:

Result comes from:

- which cause
- which action
- under which environment

---

## ENV LAW

ENV must be preserved.

- ห้ามสรุป ENV จนเสียความจริง
- ห้ามตัด ENV ทิ้ง

```text
ENV = context truth
```

---

## CROSS-X / EVENT TAG LAW

ROT_PAPER does not define Cross-X execution.

The shared point with Cross-X is rule clarity:

```text
Before an event result becomes the start of a new event,
it should carry tags that tell downstream systems what it is related to.
```

These tags are not execution commands.
They are event relation markers.

Recommended tags:

```text
EVENT_TAGS:
  - category
  - related_system
  - related_boundary
  - related_paper
  - related_px
  - relation_type
  - next_event_hint
```

Purpose:

- show what the result is about
- show which system is more related by condition
- reduce interpretation burden for ROT
- reduce interpretation burden for connected systems
- allow REDR / PSP2 / MPCP to package or route later without forcing executor identity

Rule:

```text
Tags describe relation.
Tags do not execute.
Tags do not choose final executor.
Tags do not override Paper.
Tags do not override ROT.
```

---

## FINAL LAW

```text
Structure protects truth
Execution follows structure
Perception must not override truth
```

---

## FINAL STATEMENT

```text
Fix the cause
Not the result

Respect the boundary
Not the assumption

See fast
But understand correctly
```

---

## FAIL CONDITION LAW

System is invalid when:

- Missing CAUSE / ACTION / RESULT link
- Execution outside defined SCOPE
- MODEW violates boundary
- PAPER conflicts with ROT
- RESULT cannot be explained

```text
→ Must stop or fallback
```
