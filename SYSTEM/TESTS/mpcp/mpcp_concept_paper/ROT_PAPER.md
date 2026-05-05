📘 ROT_PAPER.md

MPCP Core Rotation Paper — System Control Framework


---

🧭 PURPOSE

ROT คือกรอบหลักของระบบ
ใช้กำหนด “วิธีทำงาน” ไม่ใช่ “ขั้นตอนทำงาน”

ROT defines how the system behaves
NOT what the system executes


---

🧠 CORE LAW

SYSTEM = CAUSE → ACTION → RESULT

NO TRUE / FALSE
ONLY RELATION


---

🔒 STRUCTURE LAW

1. Structure comes before logic


2. Boundary comes before execution


3. Meaning comes before format




---

📦 SYSTEM LAYERS

ROT      = Framework (rules & boundary)
PAPER    = Task definition (execution intent)
MODEW    = Execution unit
RESULT   = Outcome
PRX      = Perception (visual layer)


---

⚖️ AUTHORITY RULE

ROT > PAPER > MODEW > RESULT > PRX

PRX ห้ามย้อนควบคุมระบบ

RESULT ห้ามแก้ย้อนหลัง

MODEW ห้ามออกนอก scope

PAPER ห้ามข้าม ROT



---

🚧 BOUNDARY LAW

ทุกการทำงานต้องมีขอบเขต

IF scope is undefined
→ execution is invalid


---

📄 PAPER CONTROL LAW

Paper ต้องกำหนดให้ครบ:

TASK:
SCOPE:
INCLUDE:
EXCLUDE:
MODEW:
CONDITION:
OUTPUT:

กฎ

ห้ามกว้าง

ห้ามตีความ

ห้ามข้ามขอบเขต

ต้องระบุ “ใครเกี่ยว / ไม่เกี่ยว”



---

⚙️ MODEW LAW

One Modew = One Purpose

ห้ามรวมหลายหน้าที่

ห้ามตีความเอง

ทำตาม PAPER เท่านั้น



---

🔍 RESULT LAW

RESULT = what happened
NOT what expected

ห้ามแก้ RESULT

ห้ามตกแต่ง RESULT

RESULT ต้อง trace ได้



---

🧠 ERROR LAW

ERROR = RESULT TYPE (misalignment)

ไม่ใช่ failure

ไม่ใช่ bug เสมอ

คือสัญญาณความไม่สอดคล้อง


กฎ

Do not fix result
Trace back to cause/action


---

🎯 EXECUTION LAW

ROT validates
PAPER defines
MODEW executes
RESULT records
PRX displays


---

🚫 PROHIBITION

ห้าม:

ใช้ RESULT ตัดสินย้อนหลัง

ใช้ COLOR แทนความจริง

ใช้ MODEW นอก scope

ข้าม PAPER

แก้ข้อมูลระหว่าง run



---

🎨 PRX (LINE C) LAW

PRX = perception only

ใช้เพื่อ “เห็นเร็ว”

ไม่ใช่ logic

ไม่ใช่ truth


Color = signal
NOT decision truth


---

⚡ DECISION LAW

Fast decision allowed (Line C)
BUT must not replace trace


---

🔁 FLOW LAW

EVENT
→ ROT check
→ PAPER assign
→ MODEW run
→ RESULT
→ PRX (optional)


---

🧠 LEARNING LAW

Learning requires explanation

ต้องตอบได้ว่า:

Result comes from:
- which cause
- which action
- under which environment


---

🌍 ENV LAW

ENV must be preserved

ห้ามสรุป ENV

ห้ามตัด ENV ทิ้ง

ENV = context truth



---

🧩 FINAL LAW

Structure protects truth
Execution follows structure
Perception must not override truth


---

🔚 FINAL STATEMENT

Fix the cause
Not the result

Respect the boundary
Not the assumption

See fast
But understand correctly


---
