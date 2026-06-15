# W3Lgu MFC Logic Layer

Status: draft / contract-safe / reference-only
Scope: REDR, PSP2, DTML, LRC2 minimum functional concept logic

This folder keeps the first W3Lgu module logic implementation separate from the existing runtime agent wrappers.

## Scope Guard

This folder is a W3Lgu local MFC proof and reference implementation only.

It is not a global system standard, not a Cross-Series conformance suite, and not an authority model for Codex, Copilot, Cross-L, Modew, W3-API, MPCP, IGET, or other system-owned projects.

Other systems may reuse the result shape if useful, but they must keep their own owner tests and contracts.

Purpose:

- keep existing `core/runtime/agents/*.py` files stable
- define pure logic functions before runtime integration
- make unit tests possible without starting the API server
- keep all outputs traceable by default

Current rule:

```text
agent wrapper -> calls MFC logic -> returns contract result
```

No file in this folder should call GitHub, open network requests, or execute runtime side effects.

Initial modules:

- `redr_mfc_logic.py` — classify incoming event / risk / route intent
- `psp2_mfc_logic.py` — create handoff path and route stamp
- `dtml_mfc_logic.py` — build decision trace and review state
- `lrc2_mfc_logic.py` — create lifecycle checkpoint preview
- `contracts.py` — shared result contract
- `event_field.py` — local event-field identity object
- `logic27_registry.py` — local 3x3x3 logic slot registry
- `logic27_selector.py` — local event-field logic slot selector

This is intentionally small. It proves each declared role can perform at least one real action before deeper runtime bridge work begins.

## Phase 1.1 Standard Direction

The first working standard is not to make every module large. The standard is to make each module prove one real action that matches its declared role.

Minimum standard:

```text
input -> module logic -> decision -> next / standby -> shared result contract -> unit test
```

Module roles in this folder:

| Module | Minimum action | Output expectation |
| --- | --- | --- |
| REDR | classify event intent and risk | next module path or wait/review state |
| PSP2 | create route stamp and handoff preview | route path, route quality, standby list |
| DTML | create decision trace and review state | trace list, review state, next module path |
| LRC2 | create checkpoint preview | checkpoint key, record phase, stable output |

Standard statuses:

- `ACTIVE` — module can continue the flow
- `WAIT` — module needs clearer input
- `REVIEW_REQUIRED` — module found a review condition
- `STANDBY` — module is intentionally not activated
- `STOP` — module should not continue
- `ERROR` — contract/status error

## Phase 1.2 Local Event Field + Logic27

The local Event Field and Logic27 files test whether a field-based logic selector can keep event identity visible while choosing a logic slot.

Minimum field identity:

```text
chain_id / event_id / sequence / owner_scope / mutated / traceable
```

Local selector goal:

```text
event field -> logic slot -> next / standby -> contract result
```

This phase is intentionally local. Cross-Series and E-CS remain the shared identity backbone; this folder only proves a W3Lgu MFC reading pattern.

This folder should become the template for later W3Lgu module specialization only after the four initial modules and local field tests stay stable through tests.
