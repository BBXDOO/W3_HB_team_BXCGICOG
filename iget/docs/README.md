ปลายทาง:
/iget/docs/

สร้างทันที ชุดเริ่มต้นพร้อมใช้งาน

==================================================
FILE: /iget/docs/INDEX.md
==================================================

# IGET Documentation Center

IGET Internal Knowledge Layer

เอกสารทั้งหมดของระบบ IGET

## Files

- HOW_TO_USE.md
- HOW_IT_WORKS.md
- SCORING_RULES.md
- SIGNAL_SYSTEM.md
- PR_EXAMPLES.md
- TROUBLESHOOT.md
- CHANGELOG_IGET.md

## Status

IGET Production Active


==================================================
FILE: /iget/docs/HOW_TO_USE.md
==================================================

# How To Use IGET

## Purpose

IGET ใช้ประเมิน Pull Request อัตโนมัติ

## Flow

PR Open
→ Workflow Run
→ Analyze Files
→ Score PR
→ Post Comment

## Human Action

- อ่านผลลัพธ์
- ตรวจ Red Signal
- Merge เมื่อเหมาะสม

## Best Practice

- PR เล็ก
- มี test
- แยกงานชัดเจน
- หลีกเลี่ยงรวมหลาย feature


==================================================
FILE: /iget/docs/HOW_IT_WORKS.md
==================================================

# How IGET Works

## Core Engine

main.py
ศูนย์กลางระบบ

fetcher.py
ดึงข้อมูล PR

scorer.py
คำนวณคะแนน

reporter.py
สร้างผลลัพธ์

benchmark.py
จำลองเคสทดสอบ

## Runtime

GitHub Event
→ main.py
→ modules
→ comment output


==================================================
FILE: /iget/docs/SCORING_RULES.md
==================================================

# Scoring Rules

Base Score: 100

## Penalty

- ไฟล์มากเกินกำหนด
- lines changed สูง
- code without test
- risky files
- workflow change

## Bonus

- docs only
- small PR
- test included
- clear structure

## Output

85+   Green
60-84 Yellow
0-59  Red


==================================================
FILE: /iget/docs/SIGNAL_SYSTEM.md
==================================================

# Signal System

## Green

พร้อมตรวจขั้นสุดท้าย / merge ได้

## Yellow

มีความเสี่ยงบางส่วน
ควร review เพิ่ม

## Red

หยุดก่อน
ต้องตรวจละเอียด

## Visual Flow

🟩🟩🟨🟩
Stable

🟨🟥🟨
Need Review


==================================================
FILE: /iget/docs/PR_EXAMPLES.md
==================================================

# PR Examples

## Example A

2 files
20 lines
docs only

Result: Green

## Example B

5 files
300 lines
code no test

Result: Yellow

## Example C

18 files
1200 lines
workflow + secret keyword

Result: Red


==================================================
FILE: /iget/docs/TROUBLESHOOT.md
==================================================

# Troubleshoot

## No Comment Posted

- Check token
- Check workflow permission
- Check PR trigger

## Wrong Score

- Check file classify rules
- Check changed lines source

## Too Many Alerts

- Tune threshold
- Reduce duplicate comments


==================================================
FILE: /iget/docs/CHANGELOG_IGET.md
==================================================

# Changelog


## v9.0 — Active Runtime

- Idempotent summary comment updates with `<!-- iget:summary -->`
- Fork-safe `pull_request_target` workflow using trusted base code only
- Manual dispatch with explicit PR number
- Event-payload runtime resolution and strict repository/PR validation
- Shared retry-capable GitHub API session and actionable API errors
- Inline comments opt-in; summary reporting remains the reliable default

## v5

- scoring improved
- benchmark added
- inline comment support
- production stable

## Next

- EP signal export
- trust signal
- timeout retry
- multi repo mode


==================================================
COMMIT
==================================================

docs(iget): add internal documentation center

==================================================
ผลลัพธ์
==================================================

IGET เปลี่ยนจาก script tool
เป็น subsystem ที่มี knowledge layer สมบูรณ์
