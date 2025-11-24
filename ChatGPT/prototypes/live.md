# ChatGPT Live Prototype Protocol

## Purpose
Design space for rapid human–AI prototyping.
Output must be testable, reversible, and safe for failure.

---

## Input Sources
- direct human request
- module-to-module request
- autonomous request (only reversible)

---

## Output Types
- flow diagram
- pseudo-UX / draft interface
- prototype logic (no production)

---

## Hard Rules
R1 — no production logic
R2 — no irreversible changes
R3 — no destructive mutations
R4 — fail fast → log → escalate

---

## Failure Handling
1. stop execution
2. document incident in `/Grok/insight-vault/incidents.md`
3. escalate to Gemini

Incident path is immutable.

No escalation → no merge.

---

## Test Requirement
Every prototype must include:
- minimal scenario
- edge case
- rollback note

---

## Principle
P1 — Speed assigned to ChatGPT module
P2 — Instability risk absorbed by ChatGPT module
P3 — Team resources protected at all times
