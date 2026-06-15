# W3Lgu Gemini Handoff Note

Status: handoff / reference-only / local MFC proof
Owner field: W3Lgu can continue under Gemini or the assigned W3Lgu owner.

This note exists so the next W3Lgu maintainer can see what was added without treating this folder as a global standard.

## Scope guard

This folder is a local W3Lgu MFC proof.

It is not the global W3Lgu standard, not a Cross-Series conformance suite, and not an authority model for Gemini, Codex, Copilot, Cross-L, Modew, W3-API, MPCP, IGET, or any other system-owned project.

Use this as a map, not as a command.

## What was added

The current additions are in:

```text
core/runtime/w3lgu_mfc_logic/
```

Added components:

```text
contracts.py
redr_mfc_logic.py
psp2_mfc_logic.py
dtml_mfc_logic.py
lrc2_mfc_logic.py
event_field.py
logic27_registry.py
logic27_selector.py
W3LGU_GEMINI_HANDOFF.md
```

Related tests:

```text
tests/test_w3lgu_mfc_logic.py
tests/test_w3lgu_event_field_logic27.py
```

Current verified local test count:

```text
14 tests PASS
```

## Layer 1: Shared local result contract

`contracts.py` defines the local return shape used by the MFC logic modules.

Important fields:

```text
module
status
confidence
input_type
decision
reason
next
standby
mutated
traceable
details
```

Default safety assumptions:

```text
mutated = False
traceable = True
```

This is only the local result contract for this folder. If Gemini continues W3Lgu as the main owner field, Gemini can keep, replace, or extend this shape.

## Layer 2: Four local MFC module proofs

The first local proof covers four modules:

```text
REDR  -> classify event intent / risk / route
PSP2  -> create route path and route stamp
DTML  -> build decision trace and review state
LRC2  -> create lifecycle checkpoint preview
```

Minimum flow:

```text
input -> module logic -> decision -> next / standby -> contract result -> unit test
```

These four modules prove a minimum action. They do not define the full W3Lgu language model.

## Layer 3: EventField

`event_field.py` adds a local event-field identity object.

Minimum identity carried by the field:

```text
chain_id
event_id
sequence
source
intent
context
signals
confidence
mutated
traceable
owner_scope
borrowed_from
```

Purpose:

```text
keep chain/event identity visible while local logic reads the event field
```

Important rule:

```text
source = identity
intent / context / signals = logic selection material
```

Do not treat source alone as a reason to change logic route.

Example: `source="Cross-X"` does not automatically mean borrow-field mode. Borrowing must come from explicit intent/context such as `borrow_field=True`.

## Layer 4: Logic27 Registry

`logic27_registry.py` defines a local 3x3x3 registry:

```text
3 layers x 9 coordinates = 27 logic slots
```

Slot id format:

```text
L<layer>-C<coordinate>
```

Examples:

```text
L1-C1 = input_clear
L2-C1 = route_decision
L2-C3 = route_review
L2-C8 = borrow_field
L3-C2 = shadow_copy
L3-C5 = result_memory
```

Each slot contains:

```text
slot_id
layer
coordinate
name
purpose
default_status
next_modules
standby_modules
proposal_only
```

This is a local reading table, not a permanent W3Lgu law.

## Layer 5: Logic27 Selector

`logic27_selector.py` reads an EventField and chooses a local Logic27 slot.

Current selector examples:

```text
route / handoff     -> L2-C1
unclear / fuzzy     -> L3-C2
borrow_field=True   -> L2-C8
risk / review       -> L2-C3
memory / checkpoint -> L3-C5
```

Selector output keeps:

```text
logic_slot
event_identity
event_field
proposal_only
reference_only
```

The selector returns through the shared local contract, so it still exposes:

```text
status
next
standby
mutated
traceable
details
```

## Chain and return behavior

The important addition is not only logic selection. The important addition is that local W3Lgu MFC logic now carries event identity through the result.

Minimum chain identity:

```text
chain_id
event_id
sequence
owner_scope
```

Expected behavior:

```text
input/event field enters
logic reads the event field
logic slot is selected
next / standby are returned
identity remains visible in details.event_identity
mutated remains false
traceable remains true
```

The local flow is:

```text
EventField -> Logic27 slot -> next / standby -> contract result
```

The earlier module flow remains:

```text
REDR -> PSP2 -> DTML -> LRC2
```

These two flows can be bridged later, but this handoff note does not claim that runtime integration is complete.

## What is not done yet

Not integrated yet:

```text
parser.py
runtime.py
px.py
W3-API main endpoint
Cross-Series main contract
E-CS runtime chain backbone
Gemini-owned W3Lgu language logic
```

This folder is not yet the full W3Lgu runtime.

## Gemini continuation notes

Recommended next maintainer steps:

```text
1. Read README.md first.
2. Read this handoff note second.
3. Treat event_field.py and logic27_selector.py as local proof only.
4. Decide whether Gemini keeps, replaces, or expands Logic27.
5. Keep chain_id/event_id/sequence visible in any replacement.
6. Do not remove mutated=false and traceable=true behavior without owner approval.
7. If connecting to Cross-Series or E-CS, use their current shared contract as source of truth.
```

Critical safety note:

```text
Passing tests here means local proof is stable.
It does not mean global W3Lgu conformance.
```

## Quick test command

```bash
python -m unittest tests/test_w3lgu_mfc_logic.py tests/test_w3lgu_event_field_logic27.py
```

Expected result at this handoff point:

```text
Ran 14 tests
OK
```

## One-line summary

W3Lgu local MFC now has a return contract, four module proofs, EventField identity, Logic27 slots, Logic27 selector, visible chain/event return, and reference-only tests. Gemini can continue from here without inheriting this as a forced standard.
