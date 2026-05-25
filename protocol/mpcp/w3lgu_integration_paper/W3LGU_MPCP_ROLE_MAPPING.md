# W3Lgu ↔ MPCP Role Mapping

## 1. Purpose
เอกสารนี้กำหนดความสัมพันธ์ระหว่าง `W3Lgu` และ `MPCP` ภายใ��ระบบ W3 เพื่อให้ทั้งสองส่วนทำงานร่วมกันได้อย่างชัดเจน โดยไม่ปะปนบทบาทกัน

เอกสารนี้มีเป้าหมายเพื่อ:
- ยืนยันว่า `W3Lgu` สามารถเป็นภาษาหลักของ ecosystem ได้
- ยืนยันว่า `MPCP` ยังคงเป็นโครงสร้าง execution และ orchestration หลัก
- ป้องกันความเข้าใจผิดว่า “ภาษา” คือ “ระบบทั้งหมด”
- ป้องกันความเข้าใจผิดว่า “execution structure” คือ “semantic language” ทั้งหมด
- ทำให้ Condien, Paper, Result, Blueprint, และ Runtime สามารถ map เข้ากับภาษาเดียวกันได้โดยไม่สูญเสียหน้าที่เฉพาะของตัวเอง

---

## 2. Core Statement
**MPCP controls operational structure and movement.**  
**W3Lgu controls operational expression, transmission, and intent-readable representation.**

เวอร์ชันไทย:

**MPCP ควบคุมโครงสร้างและการเคลื่อนของงาน**  
**W3Lgu ควบคุมภาษาในการแสดงออก การส่งผ่าน และการทำให้ intent อยู่ในรูปที่ระบบอื่นอ่านร่วมกันได้**

---

## 3. Why This Separation Matters
หากไม่แยกบทบาทระหว่าง `MPCP` และ `W3Lgu` ให้ชัด จะเกิดความเสี่ยงดังนี้:
- ภาษากลายเป็น execution runtime โดยไม่ตั้งใจ
- execution structure กลายเป็น local syntax island
- subsystem อื่นเริ่มตีความคำว่า “language” และ “runtime” ไม่ตรงกัน
- Condien ถูกลดเหลือแค่ข้อความ
- Blueprint ถูกใช้เหมือน script
- Result ถูกเข้าใจเป็น semantic truth authority
- Governance, validation, continuity, และ execution เริ่มผสมกันจนแยกขอบเขตไม่ได้

ดังนั้นการแยกบทบาทจึงไม่ใช่เรื่องของ naming อย่างเดียว  
แต่เป็นเรื่องของ survivability, maintainability, และ conceptual integrity ของทั้ง ecosystem

---

## 4. W3 Ecosystem Positioning
W3 ไม่ได้ถูกออกแบบเป็น monolithic AI system  
แต่เป็น **evolving operational ecosystem**

บทบาทระดับ ecosystem:
- `BBEX-Core` = philosophical anchor
- `Copilot-Gm` = governance / structural consistency
- `Gemini` = validation
- `Cast` = continuity + context bridge
- `MPCP` = operational structure / orchestration / runtime movement
- `W3Lgu` = language / expression / transmission / intent representation

การจัดแบบนี้ทำให้:
- execution ไม่ต้องแบก governance ทั้งหมด
- language ไม่ต้องแบก runtime ทั้งหมด
- validation ไม่ต้องแบก continuity
- continuity ไม่ต้องแบก orchestration
- ทั้งหมดเชื่อมกันผ่าน protocol และ relation ที่ชัด

---

## 5. Separation Principle

### 5.1 Execution is not language
- execution structure ≠ expression protocol
- orchestration ≠ transmission
- runtime movement ≠ readable representation

ดังนั้น `MPCP` ไม่ควรถูกใช้แทน “ภาษาทั้งระบบ”  
และ `W3Lgu` ไม่ควรถูกใช้แทน “execution system ทั้งระบบ”

### 5.2 Meaning is not syntax
- `Condien` เป็น meaning/state/context layer
- `W3Lgu` เป็นภาษาที่ใช้แสดง binding, transmission, inspection, declaration ของ Condien

ดังนั้น:
- Condien ≠ W3Lgu
- แต่ Condien ต้อง representable ผ่าน W3Lgu ได้

### 5.3 Governance is not execution
- Governance กำหนดกรอบ
- Execution ลงมือทำ
- Validation ตรวจความสอดคล้อง
- Continuity รักษาสายความต่อเนื่อง
- Language ทำให้ทั้งหมดสื่อสารร่วมกันได้

ห้ามยุบทั้งหมดให้กลายเป็น system function เดียว เพราะจะทำให้ระบบแข็งและเสี่ยงต่อ collapse

---

## 6. Canonical Role Mapping

### 6.1 MPCP
MPCP ทำหน้าที่เป็น:
- operational structure
- boundary-aware execution framework
- modew-based orchestration model
- paper-bound execution movement
- result recording discipline

MPCP ตอบคำถามประเภท:
- งานเคลื่อนอย่างไร
- งานอยู่ใต้ขอบเขตอะไร
- ใคร execute
- execution flow ถูก bind ด้วยอะไร
- result ต้องถูกบันทึกอย่างไร

### 6.2 W3Lgu
W3Lgu ทำหน้าที่เป็น:
- canonical operational language
- intent translation layer
- transmission format
- interoperable readable representation
- expression layer for operational state and intent

W3Lgu ตอบคำถามประเภท:
- งานนี้จะถูกเขียน/สื่อสารอย่างไร
- intent จะถูกส่งอย่างไร
- subsystem จะอ่านกันอย่างไร
- blueprint, result, runtime signal จะอยู่ในภาษาอะไร

### 6.3 Condien
Condien ทำหน้าที่เป็น:
- adaptive meaning/state/context layer
- continuity-supporting state space
- value/object/context carrier
- layer-aware meaning support

Condien ตอบคำถามประเภท:
- ตอนนี้ความหมายเชิงปฏิบัติการคืออะไร
- context อะไรกำลังกำกับ execution
- state/value/object ใดกำลังถูกพาอยู่
- อะไรเชื่อมผลลัพธ์ไปเป็นฐานใหม่ได้

### 6.4 Paper
Paper ทำหน้าที่เป็น:
- task intent declaration
- scope definition
- include/exclude constraint
- operational condition definition

### 6.5 ROT
ROT ทำหน้าที่เป็น:
- law / framework / structural authority
- relation discipline
- truth protection
- boundary authority

### 6.6 Result
Result ทำหน้าที่เป็น:
- what happened record
- action-linked record
- context/environment-linked record
- non-decorated evidence layer

### 6.7 PRX
PRX ทำหน้าที่เป็น:
- perception layer
- visual/signal quick-read layer
- non-authoritative representation

---

## 7. Functional Division Table

| Domain | MPCP | W3Lgu |
|---|---|---|
| Execution structure | Yes | No |
| Boundary discipline | Yes | No |
| Runtime orchestration | Yes | No |
| Canonical language | No | Yes |
| Inter-layer transmission | Uses it | Yes |
| Blueprint expression | Uses it | Yes |
| Result representation | Uses it | Yes |
| Condien representation | Uses it | Yes |
| Meaning/state ontology | Partial via Condien relation | No, representation only |

---

## 8. Dependency View

### Without MPCP
- W3Lgu remains a usable language
- but orchestration becomes weaker
- execution discipline fragments
- runtime movement loses structural control

### Without W3Lgu
- MPCP remains a usable structure
- but communication becomes fragmented
- blueprint/result/paper/runtime events may drift into incompatible local formats
- subsystem interoperability weakens

### Together
- MPCP gives operational skeleton
- W3Lgu gives operational speech
- Condien gives adaptive meaning
- ROT gives law
- Paper gives intent
- Result gives recorded reality

---

## 9. Role Hierarchy Proposal
เพื่อกันการตีความผิด สามารถมองการจัดตำแหน่งหน้าที่ได้ดังนี้:

- `BBEX-Core` = philosophy / anchor
- `Copilot-Gm` + `ROT` = governance / law / structural authority
- `MPCP` = operational structure
- `Condien` + `Cast` = meaning / context / continuity
- `W3Lgu` = language / expression / exchange
- `Gemini` = validation
- `PRX` = perception

หมายเหตุ:
นี่ไม่ใช่ลำดับอำนาจแบบแข็งทั้งหมด  
แต่เป็นการจัดตำแหน่งเพื่อให้แต่ละ subsystem ไม่กลืนกัน

---

## 10. Final Summary
W3Lgu สามารถเป็นภาษาหลักของ ecosystem ได้  
แต่ต้องอยู่ในบทบาทของ **canonical language / expression / transmission layer**

MPCP ยังคงเป็น execution structure และ orchestration framework  
และควรใช้ W3Lgu ผ่าน profile ที่เหมาะกับ execution, blueprint, runtime, result, และ Condien

การแยกบทบาทแบบนี้จะทำให้:
- ระบบอยู่รอดได้ดีขึ้น
- subsystem evolve แยกกันได้
- ไม่เกิด monolithic collapse
- และไม่ทำให้ concept drift ระหว่าง language, structure, meaning, และ governance
