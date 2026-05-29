# IGET v8.0 — Semantic PR Governance Update

IGET v8.0 is the active CI/runtime version for semantic PR governance. This
update preserves the existing `iget` package and older documentation below while
fixing the stale `iget_v7.*` import path that caused GitHub Actions to fail.

## v8 operational notes

- Canonical smoke suite: `python -m iget.tests.test_iget_v8`
- Compatibility wrapper: `python -m iget.tests.test_iget_v7`
- Active engine version: `iget.config.VERSION`
- GitHub Actions workflow: `.github/workflows/iget.yml`
- Public import path remains stable: `import iget`

The v8 suite keeps semantic state, proof trace, replay determinism, and
MPCP-compatible trace output. Tests should assert against `iget.config.VERSION`
rather than hard-coded version text.

---

IGET (v1) — W3 0.5 PR Flow Assistant

Version: v1
Status: Active
Owner: BBX19
Environment: W3 / GitHub Pull Request Workflow

---

Overview

IGET is a lightweight governance assistant for Pull Requests.

Its purpose is to reduce complex GitHub review signals into a clear human-readable flow using:

- Summary
- Risk indication
- Decision support
- Fast visual status

IGET is built for practical use, low overhead, and real workflow conditions.

---

Core Philosophy

IGET follows the W3 0.5 concept:

«Balance between strict automation and human judgment.»

Not every PR should be blocked.
Not every PR should be trusted blindly.

The system helps identify what needs attention, what is safe, and what should be reviewed further.

---

W3 Color Trigger System

IGET uses visual status layers for fast understanding.

Color| Meaning
🟩 Green| Ready / Safe / Low Risk
🟨 Yellow| Caution / Needs Review
🟥 Red| High Risk / Hold / Inspect

Colors are used so humans can understand status instantly without reading long reports.

---

2 Modes

1. Normal Run

Used on real Pull Requests.

IGET scans change signals and summarizes:

- files changed
- lines changed
- file types
- possible risks
- readiness level
- recommendations

---

2. Soft Run

Used for pre-decision support before merge.

Shows:

- Choice → possible direction
- Pre-test → expected outcome
- Recommend → actions likely to pass

Useful during uncertain or active development periods.

---

Primary Check (v1)

Main indicators used in current version:

- total changed files
- total changed lines
- code / docs / test ratio
- risky filenames
- documentation-only mode
- PR size pressure

Default behavior begins in soft balance mode.

---

Example Output

Green PR

FLOW
🟩🟩🟩🟩🟩🟩 (100%)

IMPACT
Safe level. Ready to merge.

---

Yellow PR

FLOW
🟩🟨🟨🟩🟨🟩 (72%)

IMPACT
Some risk detected. Review recommended.

---

Red PR

FLOW
🟥🟥🟥🟨🟥🟥 (38%)

IMPACT
High risk. Inspect before merge.

---

Why IGET Exists

Modern PR systems often produce too much noise.

IGET converts complexity into:

- readable signals
- simple summaries
- better merge confidence
- faster human decisions

---

Design Principles

- Fast
- Clear
- Lightweight
- Human-friendly
- Git-native
- Expandable
- Real-world practical

---

Current Structure

iget/
├── README.md
├── SPEC_V1.md
└── main.py

---

Next Evolution

v2 Targets

- Line C scoring model
- EP packet output
- trust memory signals
- workflow type detection
- historical learning layer

---

Notes

IGET does not replace maintainers.
IGET assists maintainers.

Final judgment remains human.

---

Identity Statement

Built under practical limits.
Designed for real use.
Improved through live operation.

---

End of README
# IGET (v1) — W3 0.5 PR Flow Assistant

IGET คือปลั๊กอิน/บอตสำหรับ Pull Request ที่ “แปล” ขั้นตอน GitHub ที่ซับซ้อนให้เป็น **Flow + สี + ความเสี่ยง + เงื่อนไขขั้นต่ำ** เพื่อให้เข้าใจได้ทันทีโดยไม่ต้องอ่านคู่มือยาว

## W3 0.5 + Color Trigger
IGET ใช้แนวคิด “ความคลุมเครือที่ควบคุมได้ (W3 0.5)” เพื่ออธิบายสถานการณ์เป็นระดับ:

- 🟩 **Green** = พร้อม/ปลอดภัย/ความเสี่ยงต่ำ
- 🟨 **Yellow** = ยังไม่พัง แต่มีความเสี่ยง/ควรระวัง/ควรแก้ก่อน merge
- 🟥 **Red** = ความเสี่ยงสูง/ควรหยุดและแก้/ไม่ผ่านขั้นต่ำ

สีเป็นภาษาสากล ช่วยให้เกิด “ภาพจำ” ของวิธีใช้งานโดยไม่ต้องจำศัพท์ GitHub จำนวนมาก

## 2 Modes
### 1) Normal Run (สรุปสิ่งที่เกิดขึ้นจริง)
PR เดินตามกระบวนการจริง (lint/review/merge) แล้ว IGET สรุปออกมาเป็นภาษามนุษย์:
- เกิดอะไรขึ้นบ้าง
- เรียก check/action อะไร
- จุดเสี่ยง/จุดพังอยู่ตรงไหน
- สรุปผลท้ายทาง

### 2) Soft Run (ช่วยตัดสินใจก่อน/ระหว่างทาง)
Soft Run แสดง 3 ส่วน:
- **A) Choice** — ทางเลือกที่เป็นไปได้ตอนนี้
- **B) Pre-test** — จำลอง/คาดการณ์ว่าจะเกิดอะไรขึ้นจากสัญญาณจริง
- **C) Recommend** — เงื่อนไขขั้นต่ำที่เป็นไปได้เพื่อให้ผ่าน

## Primary Check (v1)
- `lint` คือ check หลักที่ใช้ตัดสิน state
- ค่าเริ่มต้นของระบบ: `soft mode`

## Where this lives
เอกสารทั้งหมดของ IGET v1 อยู่ในโฟลเดอร์ `iget/`:
- `README.md` ภาพรวมแนวคิด
- `SPEC_V1.md` สเปกโหนด/สถานะ/การ render
- `CONFIG_SCHEMA.md` โครงสร้าง `.iget.yml`
- `OUTPUT_FORMAT.md` รูปแบบข้อความคอมเมนต์ PR
