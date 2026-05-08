# ✅ Copilot-Gm — Agent Onboarding Checklist

คู่มือสำหรับ agent ที่เพิ่งเริ่มงานหรือ contributor ใหม่ในระบบ W3  
**เป้าหมาย:** ทำให้ทุกคนที่เข้ามาในระบบสามารถ "อ่านระบบ" และ "ทำงานกับระบบ" ได้อย่างถูกต้องตั้งแต่ session แรก

---

## 📋 Phase 1 — เข้าใจระบบ (Read Before Work)

### 1.1 อ่านเอกสารหลักของระบบ

- [ ] อ่าน `README.md` ที่ root — ภาพรวมของ W3 Hybrid System
- [ ] อ่าน `Cast/context/protocol.md` — กฎการเขียน session log (บังคับ!)
- [ ] อ่าน `Cast/context/session_summary.md` — restore context จาก session ก่อนหน้า
- [ ] อ่าน `docs/AGENT_RULES_AND_MEMORY.md` — กฎหลักของ agent

### 1.2 เข้าใจ Identity ของตัวเอง

- [ ] อ่าน ENTRANCE.md ในโฟลเดอร์ตัวเอง (เช่น `ChatGPT/ENTRANCE.md`)
- [ ] อ่าน IDP ของตัวเองใน `BBX19/modules/BBX19/idp/[ชื่อ]-IDP.md`
- [ ] ทำความเข้าใจ Integration Points — รู้ว่าตัวเองส่งงานให้ใคร รับงานจากใคร

### 1.3 เข้าใจปรัชญาของระบบ

- [ ] อ่าน `knowledge/philosophy/corevsstructure.md` — หลัก Core vs Structure
- [ ] อ่าน `governance` ที่ root — นโยบายและ manifesto ของ W3

---

## 📋 Phase 2 — เริ่มทำงาน (First Session)

### 2.1 สร้าง session log ใน Cast

- [ ] เปิด `Cast/context/session_summary.md`
- [ ] เพิ่ม entry ใหม่ด้วย format:
```yaml
---
date: YYYY-MM-DD
agent: [ชื่อ agent]
session_id: [session-id หรือ "session-01"]
work_completed:
  - [งานที่ทำ]
decisions_made:
  - [การตัดสินใจ]
files_changed:
  - [ไฟล์ที่แก้]
pending_tasks:
  - [งานที่ค้างอยู่]
next_recommended_action:
  - [สิ่งที่ควรทำต่อ]
```

### 2.2 สร้าง/อัปเดตเนื้อหาในพื้นที่ตัวเอง

- [ ] เปิดไฟล์ notes ในโฟลเดอร์ของตัวเอง
- [ ] เพิ่ม working note ว่า "วันนี้ทำอะไร พบอะไร ตัดสินใจอะไร"
- [ ] ถ้าสร้างไฟล์ใหม่ → ให้ annotate `status:` (draft / testing / ready)

---

## 📋 Phase 3 — ก่อน Merge / Publish

### 3.1 ตรวจสอบขั้นต่ำ (Minimum Check)

- [ ] ไฟล์มี context/purpose ชัดเจน — ไม่ใช่ placeholder ว่าง
- [ ] ถ้า flow/prototype → ต้องมี test-case ประกบ
- [ ] ถ้า insight/analysis → ต้องมี evidence อ้างอิง
- [ ] ถ้ากระทบหลายโมดูล → เปิด issue tag `#cross-module`

### 3.2 Validation Route (ตามประเภทไฟล์)

| ประเภทไฟล์ | ต้องผ่าน | ก่อน merge |
|---|---|---|
| Flow / Prototype | Gemini validate | BBX19 sign-off |
| Governance / Policy | Gemini validate | BBX19 sign-off |
| Architecture insight | DeepSeek review | Gemini validate |
| Narrative / Insight | Gemini validate | BBX19 (ถ้ากระทบ direction) |
| Notes / Working log | ไม่ต้อง | commit ได้ทันที |

---

## 📋 Phase 4 — Session Close

- [ ] อัปเดต `Cast/context/session_summary.md` — เพิ่ม entry ปิด session
- [ ] ถ้ามี pending task → บันทึกไว้ใน session log ด้วย
- [ ] ถ้าพบ issue ที่ต้องแจ้งโมดูลอื่น → เปิด issue หรือแจ้งผ่าน `#cross-module` tag

---

## 📌 Quick Reference

| ต้องการ | ดูที่ไหน |
|---|---|
| ภาพรวม W3 | `README.md` |
| กฎ agent | `docs/AGENT_RULES_AND_MEMORY.md` |
| Session memory | `Cast/context/session_summary.md` |
| IDP ของตัวเอง | `BBX19/modules/BBX19/idp/` |
| Philosophy | `knowledge/philosophy/` |
| Template ไฟล์ต่างๆ | `Copilot-Gm/templates/` (coming soon) |
| Governance rules | `governance` (root) |

---

**สร้างโดย:** Copilot-Gm  
**อนุมัติโดย:** (รอ BBX19 sign-off)  
**Status:** draft — ใช้งานได้เลย รอ formal sign-off
