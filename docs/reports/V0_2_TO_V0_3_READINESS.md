# v0.2 Final Lock → v0.3 Readiness Gate

## Purpose

This report records the remaining v0.2 truth lock before the project moves toward v0.3. It is an explanation and readiness artifact only; it does not change runtime behavior.

## v0.2 truth lock

| Layer | Current rule | Readiness meaning |
|---|---|---|
| Registry / protocol / source code | Truth | Module roles, protocol contracts, source behavior, and tests define what is real. |
| Config | Orientation map | Config points humans and agents toward systems, defaults, and cross-system paths; it does not override truth. |
| Docs | Explanation / public boundary / branch strategy | Docs explain operating meaning, review boundaries, and movement toward public release. |

## Cross Gateway proof

| Component | v0.2 lock | v0.3 readiness note |
|---|---|---|
| W3-API | Gateway-only | Accepts intent and returns trace plans without mutating runtime truth. |
| Cross-X | Plan-only | Builds coordination plans and process traces without executing cross-system mutation. |
| W3DB append | Append-plan / append-only at approved points | A gateway may show append envelopes; persistence requires an approved append path. |
| EP_SIGNAL / RYTM | Preview / signal trace | Signal previews expose traceability, not source-truth mutation. |

## Process layer stability

| Role | Stable responsibility | Mutation boundary |
|---|---|---|
| REDR | Package request/intent into a readable handoff. | Does not mutate truth. |
| PSP2 | Route/stamp packages and produce route trace. | Does not mutate truth. |
| DTML | Review decision/risk and expose governance concern. | Does not approve or execute by itself. |
| LRC2 | Log/memory preview and continuity trace. | Does not write permanent memory without a gate. |

The process layer must stay non-mutating until a clear Human Review and Governance Gate authorizes any persistence adapter.

## v0.3 readiness gate

v0.3 movement is ready only when:

- proof docs exist for the major cross-system boundaries;
- tests cover important contracts and non-mutation guarantees;
- public/private boundary is clear;
- `main` is treated as public-facing stable surface, not active development base;
- `refactor/v0.2` remains the active integration base until a reviewed transition;
- G-State is documented as awareness foundation, not execution engine;
- no component silently gains authority outside its declared responsibility.

## Stop conditions

Do not move to v0.3 if:

- W3-API starts mutating W3DB, EP_SIGNAL, W3Lgu, MPCP, or runtime state directly;
- Cross-X becomes an executor instead of a planner;
- REDR, PSP2, DTML, or LRC2 start mutating truth without an approved gate;
- config is used as authority instead of orientation;
- docs claim behavior not backed by registry, protocol, source code, and tests;
- G-State is treated as workflow engine, state-machine replacement, or runtime executor.

## Conclusion

v0.2 is ready to close only when truth, orientation, explanation, gateway proof, process stability, and G-State awareness are aligned. v0.3 should begin from this locked foundation, not from a rewrite.
