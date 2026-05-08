# 📓 ChatGPT — Design Decisions & Working Notes

พื้นที่นี้บันทึกเหตุผลการออกแบบและการตัดสินใจสำคัญของโมดูล ChatGPT  
ทุก entry ควรระบุ: context → decision → rationale → outcome (ถ้ามี)

---

## 📐 Design Decisions

### [2026-05-08] โครงสร้าง flow-lab vs prototypes

**Context:** มีคำถามว่า flow ระดับ concept ควรอยู่ที่ไหน  
**Decision:** แยก flow-lab (ทดลอง/ยังไม่พร้อม) ออกจาก prototypes (พร้อม simulate)  
**Rationale:**
- flow-lab = พื้นที่คิดแบบไม่มีแรงกดดัน ไม่ต้อง QA ก่อน
- prototypes = พื้นที่ที่มี test-case ประกบ พร้อมให้ Gemini validate
- การแยกช่วยให้รู้ทันทีว่า artifact ไหนใช้งานได้จริงแล้ว

**Outcome:** ดูโฟลเดอร์ `prototypes/live.md` สำหรับ prototype ที่ผ่าน validation แล้ว

---

### [2026-05-08] การเลือกใช้ MPCP ใน test harness

**Context:** ระบบต้องการ state management สำหรับ flow ที่ซับซ้อน  
**Decision:** ใช้ MPCP (Multi-Protocol Control Point) เป็น backbone ของ test harness  
**Rationale:**
- MPCP รองรับ state transition ที่ชัดเจน (idle → run → done/fail)
- ใช้ร่วมกับ W3DB ได้ทันที — ไม่ต้องสร้าง state machine ใหม่
- ดู `notes/mpcp.json` สำหรับ config จริง

**Outcome:** test-harness.md ใช้ MPCP state model เป็นพื้นฐาน

---

## 🔬 Experiment Log

### [2026-05-08] ทดสอบ simulation primitives

**ทดสอบอะไร:** UX interaction model ระหว่าง agent กับ user input  
**สิ่งที่ได้เรียนรู้:**
- User input ที่ไม่มี schema กำกับทำให้ agent ตีความต่างกัน
- ต้องกำหนด "input contract" ก่อนจะทำ simulation ได้ถูก
- ดูรายละเอียดใน `ux-sim/simulation-primitives.md`

**สิ่งที่ต้องทำต่อ:**
- [ ] สร้าง input contract schema สำหรับ ux-sim
- [ ] เชื่อม simulation output กับ Gemini validation flow

---

## 📋 Working Notes

**[2026-05-08]** พื้นที่นี้เริ่มใช้งานจริง — จะเพิ่ม entry ทุกครั้งที่มีการตัดสินใจสำคัญหรือพบข้อสังเกตที่ควรบันทึกไว้

**[TODO]**
- [ ] เพิ่ม design-bridge rationale ใน notes นี้
- [ ] สร้าง experiments-index ที่มี entry จริง (แทน placeholder เดิม)
- [ ] link ทุก prototype กลับมาที่ notes นี้เพื่อ traceability

---

## 🔗 Cross-module Notes

- **→ Gemini:** ส่ง prototype ที่พร้อม validate ผ่าน `modules/ChatGPT/requests/`
- **→ Grok:** หาก flow มีประเด็น narrative → แจ้ง Grok ผ่าน issue tag `#cross-module`
- **← BBX19:** requirement หลักอยู่ที่ `BBX19/directives/base.md`
