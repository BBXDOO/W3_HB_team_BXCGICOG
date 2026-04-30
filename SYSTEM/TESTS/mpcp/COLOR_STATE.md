MPCP COLOR & STATE SYSTEM SPECIFICATION

Version: v1.0
Status: Production Ready

---

1. PURPOSE

ระบบสีนี้ถูกออกแบบเพื่อใช้เป็น กลไกการตัดสินใจอย่างรวดเร็ว (Fast Decision System)
โดยไม่ต้องพึ่งการอ่านข้อมูลทั้งหมด

เห็นสี → ตัดสินใจได้ทันที

---

2. CORE PRINCIPLE

สี = สถานะ (State)
ไม่ใช่ = ความสวยงาม / อารมณ์

- ไม่ยึดติดกับสัญลักษณ์
- ใช้แทน “ผลลัพธ์” หรือ “สถานะของพื้นที่ข้อมูล”
- รองรับการใช้งานข้ามระบบ (OS / Mobile / Web / Runtime)

---

3. COLOR DEFINITIONS

3.1 Primary State

Color| Meaning| Definition
🟢| พร้อมใช้| ใช้งานได้ทันที
🟡| พอใช้| ใช้ได้แต่ต้องระวัง
🔴| ไม่แนะนำ| ไม่ควรใช้งาน
🔵| ยังไม่จบ| รอข้อมูล / ห้ามสรุป

---

3.2 Risk & Observation Layer (Flag)

Symbol| Meaning| Definition
⚫️| อันตราย| ต้องศึกษาเพิ่มก่อนใช้
ℹ️| จุดสังเกต| มีข้อมูลเพิ่มเติม

Flag ≠ State
Flag = Layer เสริม

---

4. COLOR LOGIC RULES

4.1 Single Color

ใช้แทนสถานะหลัก (State)

---

4.2 Dual Color (Composite State)

สีแรก = สถานะหลัก
สีที่สอง = ตัวปรับการตัดสินใจ

Examples

Code| Meaning
🔵🟢| กำลังดำเนินการ + แนวทางถูก
🔵🔴| กำลังดำเนินการ + ไม่แนะนำ
🟢🔴| ผ่านเงื่อนไข + มีความเสี่ยง

---

4.3 Constraints

- ใช้ไม่เกิน 2 สี
- อ่านซ้าย → ขวา
- ห้ามสลับลำดับ

---

5. SCORE SYSTEM

ใช้เพื่อแปลง “ข้อมูลเชิงตัวเลข” → “สถานะสี”

Score (%)| Color
90–100| 🟢
75–90| 🟡
50–75| 🔴
0–50| 🔵

---

6. PINNED SYSTEM

Pinned = Flag สำคัญที่ต้องติดตาม

Type
⚫️
เทา

---

7. DATA STRUCTURE (DataBoard CF-A)

7.1 Structure

A. Group Name
B. Columns:
   - TAX / Type
   - จำนวนรอบสะสม
   - รอบคงที่
   - รอบเปลี่ยนรูป
   - รอบความเสี่ยง
   - รอบเพิ่มเติม
   - E-Tric
   - Pinned Comment

C. Output Row Format

---

7.2 Example

... | Tax | 250 | 198 | 33 | 2 | 267 | 🔵🔴 / ℹ️ //link

---

7.3 Interpretation

🔵🔴 = ยังไม่จบ + ไม่แนะนำ
ℹ️ = มีข้อมูลเพิ่มเติม

---

8. EXECUTION LOGIC (FOR MPCP)

if state == "🔴":
    action = "STOP"

elif state == "🔵":
    action = "WAIT"

elif state == "🟢":
    action = "EXECUTE"

elif state == "🟡":
    action = "EXECUTE_WITH_CAUTION"

---

9. SYSTEM ARCHITECTURE POSITION

Color System = Decision Layer

Integration:

MPCP
 ├── Pillar (A–F)
 ├── Runtime
 ├── Adapter (W3Lgu)
 └── Color Decision Layer ← (This system)

---

10. DESIGN GOAL

- ใช้ได้ทันที
- ไม่ต้องอธิบาย
- ไม่ต้องตีความ
- ใช้ข้ามระบบได้

---

11. FINAL STATEMENT

Color = State
State = Decision
Decision = Action

---

END OF DOCUMENT
