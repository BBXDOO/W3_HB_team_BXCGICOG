# W3 Session Log v2

Purpose:
Training records + system improvement bridge for TODO and IGET.

---

## Rules

- 1 session = 1 record
- Keep short
- Failure = usable data
- Repeated issue = pattern
- Every session should produce learning or action

---

## Session Template

## Session ID: S-0001
Date:
Challenge ID:
Category: Logic / Code / DIY / Outframe / Review
Mode: Practice / Test / Real Case

Result: Pass / Fail / Partial
Confidence: High / Mid / Low

Input:
(short challenge description)

Decision:
(what was chosen)

Reason:
(why)

Score:
0-25

Lesson:
(what learned)

Pattern Tag:
logic / speed / naming / risk / governance / structure

System Output:

TODO:
- [P1]
- [P2]

IGET:
- scoring rule
- warning rule
- summary improve

Report:
(short summary for future review)

Next Action:
Continue / Retest / Escalate / Archive

---

# Active Records

## Session ID: S-0001
Date: 2026-04-19
Challenge ID: CH-LOGIC-001
Category: Logic
Mode: Practice

Result: Partial
Confidence: Mid

Input:
PR changed 1 file but 420 lines, no tests.

Decision:
Yellow

Reason:
Single file only, but large change.

Score:
16

Lesson:
Large single-file changes need heavier penalty.

Pattern Tag:
risk / governance

System Output:

TODO:
- [P1] Review large-file threshold

IGET:
- if single_file_changes > 300: score -= 15
- add summary note: large concentrated change

Report:
Current system underestimates concentrated risk.

Next Action:
Retest
