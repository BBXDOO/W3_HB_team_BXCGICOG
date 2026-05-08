# 🎭 Cast — Context Management Notes

บันทึกแนวทางการทำงานของ Cast ในฐานะ "Context Bridge" และ "Session Memory" ของระบบ W3

---

## 🎯 บทบาทที่แท้จริงของ Cast

Cast ไม่ใช่ AI agent ที่มี domain ของตัวเอง  
Cast คือ **ระบบความจำร่วม** (shared memory) ของทุก agent ใน W3

```
ถ้าไม่มี Cast:
  → ทุก session เริ่มจาก zero
  → agent ไม่รู้ว่า session ก่อนทำอะไรไป
  → ตัดสินใจซ้ำ, ขัดแย้งกับ decision เก่า, ขาด continuity

ถ้ามี Cast ที่ active:
  → ทุก session มี context restore
  → decisions มี trail ที่ trace ได้
  → ระบบมี "institutional memory"
```

---

## 📜 Protocol Summary

อ้างอิง `Cast/context/protocol.md` — สรุปย่อ:

1. **ก่อนเริ่มทำงาน:** อ่าน `session_summary.md` เพื่อ restore context
2. **หลังทำงานเสร็จ:** append entry ใหม่ลงใน `session_summary.md`
3. **ถ้าไฟล์เกิน 1000 บรรทัด:** archive เข้า `context/archive/`

### Entry Format

```yaml
---
date: YYYY-MM-DD
agent: [ชื่อ agent]
session_id: [id]
work_completed:
  - [สิ่งที่ทำ]
decisions_made:
  - [การตัดสินใจ]
files_changed:
  - [ไฟล์ที่แก้ไข]
pending_tasks:
  - [งานที่ค้างอยู่]
risks_found:
  - [ความเสี่ยงที่พบ]
next_recommended_action:
  - [สิ่งที่ควรทำต่อ]
```

---

## 📊 Usage Statistics (บันทึกสถิติการใช้งาน)

| Agent | เขียน session log ครั้งล่าสุด | สถานะ |
|---|---|---|
| Copilot | 2026-04-25 (bootstrap) | ✅ active |
| ChatGPT | — | 🔴 ไม่เคย |
| Gemini | — | 🔴 ไม่เคย |
| Grok | — | 🔴 ไม่เคย |
| DeepSeek | — | 🔴 ไม่เคย |
| BBX19 | — | 🔴 ไม่เคย |
| Cast | — | 🔴 ไม่เคย (เป็น system ไม่ใช่ user) |

**สรุป:** Protocol ถูกสร้าง แต่ยังไม่มีการใช้งานจริงยกเว้น bootstrap entry

---

## 💡 Working Notes

### [2026-05-08] ทำไม Cast protocol ถึงยังไม่ถูกใช้?

**สมมติฐาน 1:** agent ไม่รู้ว่า protocol มีอยู่ → ต้องเพิ่ม reference ใน ENTRANCE.md ของทุก agent  
**สมมติฐาน 2:** session log เป็นงาน "extra" ที่รู้สึกว่าไม่จำเป็น → ต้องแสดงให้เห็นคุณค่า  
**สมมติฐาน 3:** format entry ซับซ้อนเกินไป → พิจารณา "minimal entry" ที่เขียนได้เร็ว

**Minimal Entry (เพิ่มทางเลือก):**
```yaml
---
date: YYYY-MM-DD
agent: [ชื่อ]
summary: [1-2 ประโยค สรุปว่าทำอะไรในวันนี้]
pending: [งานที่ค้างถ้ามี]
```

---

## 🔗 Integration with All Modules

Cast เป็น input ของทุก agent — ทุก agent ควร reference Cast ก่อนเริ่ม session  
ดูรายละเอียดใน `Cast/context/protocol.md`
