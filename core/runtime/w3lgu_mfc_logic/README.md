# W3Lgu MFC Logic Layer

Status: draft / contract-safe
Scope: REDR, PSP2, DTML, LRC2 minimum functional concept logic

This folder keeps the first W3Lgu module logic implementation separate from the existing runtime agent wrappers.

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

This folder should become the template for later W3Lgu module specialization only after the four initial modules stay stable through tests.
