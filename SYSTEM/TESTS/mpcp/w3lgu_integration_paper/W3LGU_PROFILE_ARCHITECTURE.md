# W3Lgu Profile Architecture

## 1. Purpose
เอกสารนี้กำหนด architecture ของ profile สำหรับ `W3Lgu` เพื่อให้ W3Lgu สามารถทำหน้าที่เป็นภาษากลางของ ecosystem ได้ โดยไม่ทำให้ทุก artifact, message, และ paper ถูกยัดอยู่ในรูปแบบเดียวจนสับสน

แนวคิดหลักคือ:
- หนึ่งภาษา
- หลาย profile
- grammar core เดียว
- purpose ต่างกันได้
- vocabulary ต่างกันได้ในกรอบที่ควบคุมได้

---

## 2. Core Rule
**One language, multiple profiles.**

W3Lgu เป็นภาษากลางเดียวของ ecosystem  
แต่การใช้งานจริงต้องแบ่ง profile ตามหน้าที่ เพื่อให้:
- blueprint ไม่ชน runtime
- condien declaration ไม่ชน paper
- result record ไม่ชน governance law
- signal summary ไม่ชน truth record

---

## 3. Why Profiles Are Necessary
ถ้าใช้ “ภาษาเดียวแบบไม่แบ่ง profile” จะเกิดปัญหาหลัก:
1. syntax เริ่มบวม
2. message คนละชนิดดูเหมือนกันหมด
3. คนอ่านไม่รู้ว่าข้อความนี้มี authority ระดับไหน
4. runtime message กับ blueprint declaration เริ่มปะปน
5. result กับ signal ถูกเข้าใจผิดว่าเท่ากัน
6. governance statement อาจถูกนำไปใช้เหมือน runtime command

ดังนั้น profile คือวิธีคุมบริบทของภาษา  
โดยไม่ทำลายหลัก “ภาษาเดียว”

---

## 4. Grammar Core
ทุก profile ของ W3Lgu ควรใช้ grammar core เดียวกัน:

- `KEY:VALUE`
- รองรับหลายคู่ค่าในหนึ่งบรรทัด
- รองรับหลายบรรทัด
- อ่านเร็ว
- ไม่ใช้ JSON/XML/YAML เป็น canonical form
- ไม่สร้าง syntax island เฉพาะ subsystem

นี่เป็นแกนสำคัญในการทำให้:
- parser core ใช้ร่วมกันได้
- ระบบหลายส่วนแลกเปลี่ยนกันได้
- มนุษย์อ่านและ debug ได้ง่าย

---

## 5. Proposed Profile Set

### 5.1 W3Lgu-Governance
ใช้กับ:
- law
- boundary
- structural rules
- authority rules
- prohibition rules

ตัวอย่างสิ่งที่ควรอยู่ใน profile นี้:
- ROT laws
- boundary declarations
- authority constraints

### 5.2 W3Lgu-Paper
ใช้กับ:
- task intent
- scope
- include/exclude
- condition
- output target

profile นี้มี authority ในเชิง task definition แต่ไม่ใช่ law layer

### 5.3 W3Lgu-MPCP-Blueprint
ใช้กับ:
- system plan
- target/mode/lib/bridge/partition
- reusable system setup
- deployment/runtime shape declaration

profile นี้เป็น declarative plan  
ไม่ใช่ runtime behavior log

### 5.4 W3Lgu-MPCP-Runtime
ใช้กับ:
- modew state exchange
- runtime events
- condien binding in run context
- continuity signaling
- result linkage signals

profile นี้เป็น execution-facing protocol  
แต่ต้องไม่ override governance/profile อื่น

### 5.5 W3Lgu-Condien
ใช้กับ:
- condien declaration
- condien layer access
- condien meaning/state expression
- condien inspection
- condien-modew-paper binding

### 5.6 W3Lgu-Result
ใช้กับ:
- what happened record
- cause/action/result linkage
- environment-aware evidence expression

profile นี้ต้องไม่ถูกใช้เป็น signal-only layer

### 5.7 W3Lgu-Signal
ใช้กับ:
- PRX
- fast read
- color/state/symbol summaries
- quick surface visibility

profile นี้ไม่ใช่ truth authority  
และห้ามแทน result/governance profile

---

## 6. Shared Profile Rules
ทุก profile ต้องยึดกฎร่วมดังนี้:

1. ใช้ grammar core เดียวกัน
2. profile ต่างกันได้ที่ purpose และ vocabulary
3. ห้ามสร้าง dialect ที่ขัดกับแกนภาษา
4. profile ต้อง map ข���ามกันได้ในระดับที่จำเป็น
5. signal profile ห้าม override truth profile
6. governance profile ห้ามถูกลดให้เป็น mere UI text
7. result profile ห้ามถูกตกแต่งจนเสีย evidence quality

---

## 7. Authority Awareness
ภาษาเดียวไม่แปลว่า authority เท่ากัน

ตัวอย่าง:
- governance statement
- paper intent declaration
- runtime state exchange
- result evidence record
- PRX signal

ทั้งหมดอาจใช้ W3Lgu ได้  
แต่ authority ไม่เท่ากัน  
จึงต้องรู้ว่าแต่ละข้อความอยู่ใน profile ใด

นี่คือเหตุผลที่เอกสารหรือข้อความใหม่ในระบบควรตอบได้ว่า:

> “ข้อความนี้ใช้ W3Lgu profile ไหน?”

---

## 8. Architecture View
สามารถมองภาพรวมได้ดังนี้:

- `W3Lgu` = language core
- `Profile` = context-specific expression mode
- `MPCP` = execution structure using selected W3Lgu profiles
- `Condien` = meaning/state layer represented through W3Lgu-Condien
- `Paper` = task intent through W3Lgu-Paper
- `Blueprint` = reusable plan through W3Lgu-MPCP-Blueprint
- `Result` = evidence record through W3Lgu-Result
- `PRX` = perception signal through W3Lgu-Signal

---

## 9. Final Summary
W3Lgu ควรเป็นภาษากลางของ ecosystem  
แต่เพื่อกันความสับสนและกันการตีความผิด จำเป็นต้องใช้แนวคิด **multiple profiles over one language core**

แนวทางนี้ทำให้:
- ระบบยังคง “ภาษาเดียว”
- แต่ artifact แต่ละชนิดยังรักษาบทบาทเฉพาะของตัวเองได้
- และ subsystem สามารถร่วมงานกันได้โดยไม่กลายเป็น monolithic syntax blob
