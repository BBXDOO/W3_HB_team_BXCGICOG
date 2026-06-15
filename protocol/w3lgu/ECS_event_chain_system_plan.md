# E-CS — Event Chain System Plan

STATUS: draft / plan-only
SCOPE: W3Lgu event-chain orchestration
OWNER: BBX19
RELATION: W3Lgu / 6room / Cross-X / MPCP / W3DB / EP_SIGNAL / LRC2

---

## 0. Purpose

`E-CS` means `Event Chain System`.

It is the chain layer that turns one event result into the next event decision.

It does not replace 6room.

```text
6room = choose event logic rooms
E-CS  = chain event → result → next event
```

E-CS answers:

```text
What is this event?
Which logic should be used?
Which systems must respond?
What should happen if the event is unclear?
What result should trigger the next event?
```

---

## 1. Position in W3Lgu

```text
DATA IN
→ W3Lgu
→ REDR / Package
→ 6room Logic Selector
→ E-CS Event Chain
→ Cross-X / MPCP / PX / W3DB_APPEND / EP_SIGNAL / LRC2
→ Return Contract
→ Next Event | STOP | WAIT | REVIEW
```

E-CS sits after 6room selects logic rooms, but before Cross-X opens cooperation and before deeper systems are activated.

---

## 2. Core concept

```text
[Event-1]
  Type Data   : ...
  Type Logic  : ...
  Systems     : ...
  Results     : ...

Results → [Event-2]
```

Events are not isolated.

Every result can become:

```text
1. Final result
2. Next event
3. Review request
4. Standby return
5. Stop / Wait state
6. Recovery event
```

---

## 3. Add Logic Chain

`Add Logic Chain` is the rule-building part of E-CS.

It creates a decision chain for:

```text
1. What is this event?
2. What data type is involved?
3. What logic room(s) should be used?
4. Which systems are active?
5. Which systems stay standby?
6. What result is valid?
7. What happens if the event is unclear?
8. What next event should be opened?
```

---

## 4. Minimum E-CS frame

```text
E-CS:
  event_id: <Event-N>
  source: GLOBAL | LOCAL | APP | PORT
  type_data: <data type>
  intent: <intent>
  logic_chain: <logic name>
  rooms: [Ca, Cu, Re, Si, Ap, Ev]
  active_systems: [...]
  standby_systems: [...]
  cross_state: STANDBY | ACTIVE | REVIEW
  confidence: 0 | 0.5 | 1
  result: <result>
  next: <Event-N+1 | STOP | WAIT | REVIEW>
  mutated: false
```

Default:

```text
mutated: false
```

---

## 5. Confidence / ambiguity handling

E-CS must support unclear events.

```text
0   = not enough information / unclear
0.5 = partially clear / ambiguous / needs observation
1   = clear enough inside event boundary
```

Rules:

```text
If confidence = 1:
  continue selected flow.

If confidence = 0.5:
  open clarification / observation / DTML review.

If confidence = 0:
  STOP or WAIT; do not activate deep systems.
```

Unclear event route:

```text
[Event-N]
  confidence: 0.5
  result: UNCLEAR
  next: REVIEW_OR_OBSERVE
  systems: REDR, DTML, LRC2
  cross_state: STANDBY or REVIEW
```

---

## 6. System activation law

E-CS must not wake all systems by default.

```text
Only systems required by the logic chain become ACTIVE.
Other known systems must return STANDBY.
```

This prevents unnecessary load and keeps W3 event-driven.

Example:

```text
Event: simple source sync
Active: W3Lgu, REDR, PSP2, PX, LRC2
Standby: File.void, Codex, Cross-L
```

---

## 7. Cross-X relation

E-CS does not perform crossing itself.

```text
E-CS selects whether crossing is needed.
Cross-X opens the cross point.
```

Cross-state rules:

```text
STANDBY
= one-system or local-only event; no cross required.

ACTIVE
= multiple systems must cooperate.

REVIEW
= source truth / governance / merge / recovery / ambiguity is involved.
```

---

## 8. Logic chain types

Initial draft chain types:

```text
sync_check
recovery_trace
governance_review
health_review
manifest_handoff
signal_return
ambiguity_review
external_logic_intake
```

These are not locked to event names.

Example: `git_pull` can become:

```text
UPDATED       → sync_check → health_review
CONFLICT      → recovery_trace → human_review
CRITICAL_DIFF → governance_review
FAILED        → ambiguity_review or recovery_trace
```

---

## 9. Example: Termux git pull

Event-1:

```text
E-CS:
  event_id: Event-1
  source: LOCAL, GLOBAL
  type_data: source_control
  intent: sync_repo
  logic_chain: sync_check
  rooms: [Ev, Si, Cu, Re]
  active_systems: [W3Lgu, REDR, PSP2, PX, Git, LRC2]
  standby_systems: [File.void, Cross-L, Codex]
  cross_state: ACTIVE
  confidence: 1
  result: UPDATED | CONFLICT | FAILED | NO_CHANGE
  next: Event-2
  mutated: false
```

If result is UPDATED:

```text
E-CS:
  event_id: Event-2
  type_data: repo_state
  logic_chain: health_review
  rooms: [Ev, Si, Re]
  active_systems: [Hospitication, EP_SIGNAL, Rytm, LRC2]
  result: HEALTH_OK | REVIEW
  next: STOP | REVIEW
```

If result is CONFLICT:

```text
E-CS:
  event_id: Event-2
  type_data: repo_conflict
  logic_chain: recovery_trace
  rooms: [Ev, Si, Ap, Ca, Cu, Re]
  active_systems: [DTML, MPCP, LRC2, Human Review]
  cross_state: REVIEW
  confidence: 1
  result: REVIEW_REQUIRED
  next: HUMAN_REVIEW
```

If result is unclear:

```text
E-CS:
  event_id: Event-2
  logic_chain: ambiguity_review
  rooms: [Ev, Ap, Si]
  active_systems: [REDR, DTML, LRC2]
  cross_state: REVIEW
  confidence: 0.5
  result: UNCLEAR
  next: WAIT_OR_REVIEW
```

---

## 10. External logic chain intake

Because logic may be developed outside the repo, E-CS should connect to logic packs through an intake layer.

Proposed future path:

```text
protocol/w3lgu/logic_packs/
protocol/w3lgu/logic_packs/registry.json
```

External chain requirements:

```text
1. declare source / owner
2. declare event types covered
3. declare rooms used
4. declare systems allowed
5. declare standby behavior
6. declare ambiguity behavior
7. declare return contract
8. declare mutation authority
9. require review before active use
```

---

## 11. Return contract

Every E-CS step should return:

```text
RETURN:
  event_id: <Event-N>
  logic_chain: <logic>
  state: ACTIVE | STANDBY | SUCCESS | STOP | WAIT | REVIEW_REQUIRED | ERROR
  confidence: 0 | 0.5 | 1
  result: <result>
  next: <Event-N+1 | STOP | WAIT | REVIEW>
  mutated: false
  trace: <optional>
```

---

## 12. Non-goals

```text
E-CS is not runtime.
E-CS is not Cross-X.
E-CS is not a truth authority.
E-CS is not a replacement for MPCP Paper/ROT.
E-CS does not wake every system.
```

---

## 13. One-line summary

```text
E-CS turns event results into the next event chain, while Add Logic Chain decides what the event is, what logic applies, what systems respond, and how unclear events are handled.
```
