# W3Lgu MFC Logic Layer

Status: draft / contract-safe
Scope: REDR, PSP2, DTML, LRC2 minimum functional concept logic

This folder keeps the first W3Lgu module logic implementation separate from the existing runtime agent wrappers.

Purpose:

- keep existing `core/runtime/agents/*.py` files stable
- define pure logic functions before runtime integration
- make unit tests possible without starting the API server
- keep all outputs non-mutating and traceable by default

Current rule:

```text
agent wrapper -> calls MFC logic -> returns contract result
```

No file in this folder should mutate source truth, call GitHub, open network requests, or execute runtime side effects.

Initial modules:

- `redr_mfc_logic.py` — classify incoming event / risk / route intent
- `psp2_mfc_logic.py` — create handoff path and route stamp
- `dtml_mfc_logic.py` — build decision trace and review state
- `lrc2_mfc_logic.py` — create lifecycle checkpoint preview
- `contracts.py` — shared result contract

This is intentionally small. It proves each declared role can perform at least one real action before deeper runtime bridge work begins.
