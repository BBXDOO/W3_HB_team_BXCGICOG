# W3Lgu 6room Event Logic Plan

STATUS: draft / plan-only
SCOPE: W3Lgu event logic layer
OWNER: BBX19
AUTHOR-NOTE: Drafted from BBX19 6room sketch and current W3Lgu/Cross-X repository structure.

---

## 0. Purpose

`6room` is proposed as the event-logic selector layer inside W3Lgu.

It does not replace W3Lgu, REDR, Cross-X, MPCP, W3DB, EP_SIGNAL, or LRC2.

It answers one question:

```text
When an event enters W3Lgu, which logic rooms should be active, and which systems should remain standby?
```

Core rule:

```text
Logic must not be locked to event shape.
Event shape is evidence.
Logic is selected from data type, intent, source, risk, boundary, and previous result.
```

---

## 1. Current repo relation

Current declared chain in `config/cross_system.json`:

```text
W3-API
→ W3Lgu
→ REDR
→ PSP2
→ DTML
→ PX
→ W3DB_APPEND
→ EP_SIGNAL
→ EP_SIGNAL_RYTM
→ LRC2
→ Hospitication
→ IGET
```

Proposed 6room position:

```text
W3-API / DATA IN
→ W3Lgu
→ REDR / Package
→ 6room
→ PSP2 / DTML / PX
→ Cross-X / MPCP / W3DB_APPEND / EP_SIGNAL / LRC2
→ Return Contract
```

6room should be added as a W3Lgu event-logic layer before deep routing and before Cross-X opens system cooperation.

---

## 2. Role split

```text
W3Lgu
= language / packet / meaning layer

REDR
= read, classify, tag, package; no source-truth mutation

6room
= choose event logic rooms; mark active/standby; emit logic plan

Cross-X
= cross-point coordinator; connects only systems needed to answer the event

MPCP
= operational field / Paper / ROT / Condien / Modew boundary

PSP2
= route / stamp / transport-only boundary

DTML
= decision trace review boundary

PX
= position pointer / event-position relation

W3DB_APPEND, LRC2
= evidence / append / continuity memory

EP_SIGNAL, Rytm
= signal return / readable rhythm preview

Hospitication, IGET
= health / governance review where needed
```

---

## 3. 6 rooms

```text
room1: Cause          (สาเหตุ)       .Ca
room2: Cause/result   (เหตุ/ผล)      .Cu
room3: Results        (ผลลัพธ์)      .Re
room4: Situation      (สถานการณ์)   .Si
room5: It appears     (ปรากฏการณ์)  .Ap
room6: Event          (เหตุการณ์)    .Ev
```

Important:

```text
room1-6 are not mandatory sequential steps.
They are selectable logic rooms.
```

Example:

```text
Event: git_pull updated cleanly
Active rooms: Ev, Si, Cu, Re
Standby rooms: Ca, Ap
```

```text
Event: git_pull conflict
Active rooms: Ev, Si, Ap, Ca, Cu, Re
Standby rooms: none or only non-related extensions
```

---

## 4. Data/event shape

Minimum event frame:

```text
[Event-N]
  Source      : GLOBAL | LOCAL | APP | PORT
  Type Data   : ...
  Intent      : ...
  Type Logic  : ...
  Active      : room list
  Standby     : room list
  Cross       : ACTIVE | STANDBY | REVIEW
  Systems     : system list
  Results     : ...
  Next        : Event-N+1 | STOP | WAIT | REVIEW
```

Compact W3Lgu-like sketch:

```text
6R'Ev,Si,Cu,Re:LOCAL'Termux/git_pull;RE:UPDATED;NEXT:HEALTH_SCAN.
```

Conflict sketch:

```text
6R'Ev,Si,Ap,Ca,Cu,Re:LOCAL'Termux/git_pull;AP:MERGE_CONFLICT;RE:STOP;NEXT:HUMAN_REVIEW.
```

---

## 5. Logic selector input

6room should choose logic using:

```text
1. Type Data
2. Source Class: GLOBAL / LOCAL / APP / PORT
3. Intent
4. Boundary
5. Risk level
6. Target system
7. Previous result
8. Current system state
9. Required return contract
```

This means the same event name can use different logic.

Example: `git pull`

```text
No conflict        → sync_check
Conflict           → recovery_trace
Critical file diff → governance_review
Repo health issue  → hospitication_scan
```

---

## 6. Cross-X relation

6room must not create a second cross-point system.

```text
6room = selects event logic
Cross-X = opens the cross point for systems that must respond
```

Cross-X state rules:

```text
If one system can answer the event:
  Cross-X = STANDBY

If multiple systems must cooperate:
  Cross-X = ACTIVE

If source truth / governance / merge / recovery is involved:
  Cross-X = ACTIVE + REVIEW
```

---

## 7. Standby law

Systems that are not needed for the current event must be explicitly marked as standby.

```text
STANDBY does not mean missing.
STANDBY means intentionally not activated for this event.
```

Return state options:

```text
ACTIVE
STANDBY
SUCCESS
STOP
WAIT
REVIEW_REQUIRED
ERROR
```

Minimum return contract:

```text
RETURN:
  system: <name>
  state: ACTIVE | STANDBY | SUCCESS | STOP | WAIT | REVIEW_REQUIRED | ERROR
  event: <event_id>
  mutated: true | false
  result: <summary>
  next: <next_event | stop | wait | review>
  trace: <optional_ref>
```

Default mutation rule:

```text
mutated: false
```

unless explicitly approved by human/governance flow.

---

## 8. External logic intake slot

Because logic packs may continue to be developed outside the repo, 6room should have an intake lane.

Proposed location:

```text
protocol/w3lgu/logic_packs/
```

Initial index idea:

```text
protocol/w3lgu/logic_packs/registry.json
```

Potential registry shape:

```json
{
  "schema_version": "W3LGU-LOGIC-PACK-0.1",
  "status": "draft",
  "packs": [
    {
      "id": "6room-core",
      "status": "draft",
      "source": "BBX19",
      "rooms": ["Ca", "Cu", "Re", "Si", "Ap", "Ev"],
      "mutation_authority": false,
      "requires_review": true
    }
  ]
}
```

External logic pack requirements:

```text
1. Must declare source / owner.
2. Must declare room(s) affected.
3. Must declare input shape.
4. Must declare return contract.
5. Must declare mutation authority.
6. Must be reviewable before becoming active.
7. Must support standby state.
```

---

## 9. Proposed integration phases

### Phase 0 — Document only

Create this plan and keep 6room as draft.

### Phase 1 — Contract draft

Create a small `6room` event contract with no runtime execution.

Possible files:

```text
protocol/w3lgu/6room_event_logic_plan.md
protocol/w3lgu/logic_packs/registry.json
```

### Phase 2 — Parser-safe markers

Add parser-safe markers only:

```text
6R
Ca
Cu
Re
Si
Ap
Ev
STANDBY
ACTIVE
```

No mutation.

### Phase 3 — Cross-X handoff preview

Allow 6room to emit a plan that Cross-X can read:

```text
logic_rooms: [Ev, Si, Re]
cross_state: ACTIVE | STANDBY | REVIEW
systems: [REDR, PSP2, DTML, PX, W3DB_APPEND, EP_SIGNAL]
```

### Phase 4 — Runtime bridge

Only after review, connect to runtime / MPCP / W3DB_APPEND preview flows.

---

## 10. Example route: Termux git pull

```text
DATA   : LOCAL, GLOBAL
EVENT  : Termux/git_pull
INTENT : sync_repo
```

Event-1:

```text
[Event-1]
  Source      : LOCAL, GLOBAL
  Type Data   : source_control
  Intent      : sync_repo
  Type Logic  : sync_check
  Active      : Ev, Si, Cu, Re
  Standby     : Ca, Ap, File.void, Cross-L, Codex
  Cross       : ACTIVE
  Systems     : W3Lgu, REDR, PSP2, DTML, PX, Git, LRC2
  Results     : UPDATED | CONFLICT | FAILED | NO_CHANGE
  Next        : Event-2
```

If UPDATED:

```text
[Event-2]
  Type Data   : repo_state
  Type Logic  : health_review
  Active      : Ev, Si, Re
  Systems     : Hospitication, EP_SIGNAL, Rytm, LRC2
  Results     : HEALTH_OK | REVIEW
```

If CONFLICT:

```text
[Event-2]
  Type Data   : repo_conflict
  Type Logic  : recovery_trace
  Active      : Ev, Si, Ap, Ca, Cu, Re
  Cross       : ACTIVE + REVIEW
  Systems     : DTML, MPCP, LRC2, Human Review
  Results     : STOP | WAIT | REVIEW_REQUIRED
```

---

## 11. Open questions

```text
1. Should 6room live in W3Lgu core, papers, or logic_packs first?
2. Should room order be visual-only, or should parser preserve declared order?
3. Should Truth Scale 0 / 0.5 / 1 live in 6room or in a separate truth/evidence layer?
4. Should Cross-X consume 6room output directly or through W3Lgu packet only?
5. How should external logic packs be accepted, reviewed, and promoted?
```

---

## 12. Non-goals

```text
6room is not a runtime executor.
6room is not a new Cross-X.
6room is not a truth authority.
6room is not a replacement for MPCP Paper/ROT.
6room is not required to wake every system.
```

---

## 13. One-line summary

```text
6room lets W3Lgu read an event, choose the right logic rooms, keep unused systems standby, and hand only necessary cooperation to Cross-X.
```
