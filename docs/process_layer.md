# W3 Process Layer — REDR / PSP2 / DTML / LRC2

This layer completes the W3 process chain around Cross-X. It is intentionally
plan-only by default: it creates packages, route stamps, decision traces, and
memory previews without mutating W3DB, EP_SIGNAL, W3Lgu, or source truth.

## Flow

```text
Intent
→ REDR  read / classify / tag / duplicate package
→ PSP2  stamp / route only
→ DTML  inspect destination, signal, and intent
→ LRC2  prepare immutable memory/log preview
→ Human Review + Governance Gate before any persistence or execution
```

## Stage responsibilities

| Stage | Responsibility | Must not do |
|---|---|---|
| REDR | Read intent, classify it, tag it, and duplicate the package pointer to PSP2 + LRC2. | Rewrite payload truth or execute. |
| PSP2 | Stamp the package and produce route-only handoff traces. | Inspect/approve content or mutate payloads. |
| DTML | Inspect destination, risk, signal, and intent; emit review status. | Grant execution authority by itself. |
| LRC2 | Prepare immutable memory/log preview for append-only recording. | Write memory/W3DB unless an approved adapter calls persistence explicitly. |

## Runtime contract

Implementation: `core/runtime/process_layer.py`

Outputs include:

- immutable `ProcessPackage`
- four `StageRecord` entries
- `memory_preview` for LRC2
- `w3db_status` inspection showing current in-process W3DB availability
- `mutated: false` unless a separate approved persistence adapter is called

## Personal workspaces

Each process unit now has a private module workspace:

- `modules/REDR/` — requests, packages, reports, logs
- `modules/PSP2/` — requests, routes, reports, logs
- `modules/DTML/` — requests, decisions, reports, logs
- `modules/LRC2/` — requests, memory, reports, logs

These folders are operational space, not truth authority. They can hold requests,
plans, reports, route traces, decision previews, or memory previews while Human
Review and Governance Gate remain in control.

## W3DB and memory status

- `src/w3db/store.py` is currently an in-process memory store for W3DB records.
- `core/memory/memory_bus.py` is a lightweight JSON memory bus.
- The process layer inspects both surfaces but does not append by default.
