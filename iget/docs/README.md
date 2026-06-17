# IGET Docs Center

เอกสารศูนย์กลางของระบบ **IGET v9.0 — Reliable Semantic PR Governance Runtime**

IGET คือระบบช่วยอ่าน Pull Request แล้วแปลงสัญญาณที่กระจัดกระจายให้เป็นคะแนน สถานะ สี เหตุผล ความเสี่ยง และคำแนะนำสำหรับมนุษย์ตรวจ PR

> IGET ไม่ได้แทน maintainer  
> IGET ช่วยให้ maintainer เห็นความเสี่ยงเร็วขึ้นและตัดสินใจได้มีหลักฐานมากขึ้น

---

## สถานะ

| รายการ | ค่า |
|---|---|
| Runtime | v9.0 |
| Scope | GitHub Pull Request governance |
| Output หลัก | Summary comment แบบ idempotent |
| Inline comment | opt-in |
| Authority | Human final decision |
| Safety | ใช้ trusted base code ผ่าน `pull_request_target` |

---

## เอกสารในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| [INDEX.md](INDEX.md) | ดัชนีเอกสาร IGET ทั้งหมด |
| [HOW_TO_USE.md](HOW_TO_USE.md) | วิธีใช้งานและ flow หลัก |
| [HOW_IT_WORKS.md](HOW_IT_WORKS.md) | อธิบาย runtime และโมดูลภายใน |
| [SCORING_RULES.md](SCORING_RULES.md) | กติกาคะแนน penalty / bonus / state |
| [SIGNAL_SYSTEM.md](SIGNAL_SYSTEM.md) | ระบบสี Green / Yellow / Red และ semantic state |
| [PR_EXAMPLES.md](PR_EXAMPLES.md) | ตัวอย่าง PR และผลที่คาดว่าจะได้ |
| [TROUBLESHOOT.md](TROUBLESHOOT.md) | วิธีตรวจเมื่อ comment ไม่ขึ้น คะแนนผิด หรือแจ้งเตือนเยอะ |
| [CHANGELOG_IGET.md](CHANGELOG_IGET.md) | ประวัติการเปลี่ยนแปลงของ IGET |

---

## Flow ภาพรวม

```text
GitHub PR Event / Manual Dispatch
→ resolve_runtime_context
→ fetch PR files
→ classify files
→ build stats
→ detect mode
→ compute score
→ map state + semantic state
→ build summary comment
→ upsert existing IGET comment
```

---

## หลักการออกแบบ

1. **มนุษย์เป็นผู้ตัดสินสุดท้าย** — IGET ให้สัญญาณ ไม่สั่ง merge
2. **ไม่รันโค้ดจาก PR โดยตรง** — ลดความเสี่ยงจาก fork / untrusted code
3. **สรุปต้องอ่านง่าย** — ใช้คะแนน สี เหตุผล และคำแนะนำ
4. **ตรวจซ้ำได้** — ใช้ proof trace และ summary marker
5. **ลด noise** — อัปเดต comment เดิมแทนการโพสต์ซ้ำ

---

## คำสั่งทดสอบหลัก

จาก root repo:

```bash
PYTHONPATH=. python -m pytest iget/tests -q
```

รันแบบ dry-run ผ่าน runtime context:

```bash
REPO=OWNER/REPO PR=1 GITHUB_TOKEN=xxx IGET_DRY_RUN=1 \
PYTHONPATH=. python -m iget.main
```

---

## หมายเหตุสำหรับ W3 / BOX ในอนาคต

เอกสารชุดนี้ควรอยู่ใกล้ระบบ IGET ก่อน เพื่อให้เปิดดูโค้ดแล้วเข้าใจทันที

อนาคตสามารถทำดัชนีรวมใน BOX ได้ เช่น:

```text
wx/index/iget_docs.md
wx/index/test_manuals_by_system.md
wx/index/governance_runtime_docs.md
```

---

## สรุป

README นี้เป็นหน้าหลักของเอกสาร IGET docs ไม่ใช่ไฟล์รวม dump ของเอกสารหลายไฟล์

รายละเอียดแยกอยู่ในไฟล์ย่อย เพื่อให้อ่านง่าย แก้ง่าย และใช้เป็น knowledge layer ต่อได้
