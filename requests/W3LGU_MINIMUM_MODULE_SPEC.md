# W3Lgu Minimum Module Spec Request

ID: RQ-W3LGU-MINIMUM-MODULE-SPEC
TIMESTAMP: 2026-06-20
REQUESTER: BBX19
STATUS: draft / request / minimum-baseline
SCOPE: W3Lgu modules, `core/runtime`, `core/runtime/agents/base.py`, `core/runtime/engine_v2.py`
MUTATION: false for this document; this request only defines minimum spec and gap notes.

IMPLEMENTATION NOTE: 2026-07-07 alignment pass added minimum route preservation,
review flags, runtime validation summaries, and no-fake-success behavior for the
core surfaces listed in this request.

IMPLEMENTATION NOTE: 2026-07-08 checklist closure pass made W3Lgu runtime
validation strict, added explicit LRC2 unknown identity objects, carried route
metadata through REDR stage records, and documented Logic27 as advisory-only.

---

## 1. Purpose

This request defines the minimum baseline that every W3Lgu module must satisfy before it can be treated as a real runtime participant.

The goal is not to make every module large. The goal is to prevent a module from being represented as complete when it only contains a small placeholder, local proof, or isolated template.

Minimum means:

```text
small enough to implement safely,
complete enough to preserve W3Lgu meaning,
traceable enough for review,
and honest enough to show what is still missing.
```

---

## 2. Current reference files checked

This spec was drafted after inspecting these current runtime surfaces:

- `core/runtime/agents/base.py`
- `core/runtime/engine_v2.py`
- `core/runtime/engine.py`
- `core/runtime/process_layer.py`
- `core/runtime/w3lgu_mfc_logic/README.md`
- `core/runtime/w3lgu_mfc_logic/redr_mfc_logic.py`
- `core/runtime/w3lgu_mfc_logic/psp2_mfc_logic.py`
- `core/runtime/w3lgu_mfc_logic/dtml_mfc_logic.py`
- `core/runtime/w3lgu_mfc_logic/lrc2_mfc_logic.py`
- `core/runtime/w3lgu_mfc_logic/contracts.py`
- `core/runtime/w3lgu_mfc_logic/event_field.py`
- `core/runtime/w3lgu_mfc_logic/logic27_registry.py`
- `core/runtime/w3lgu_mfc_logic/logic27_selector.py`
- `tests/test_w3lgu_mfc_logic.py`
- `tests/test_cross_x_config.py`
- `requests/requests_a001`
- `wx/references/wx_box_cn_fold_recovery_anchor.md`

---

## 3. W3Lgu module minimum contract

Every W3Lgu module must expose or preserve these fields in its result contract:

| Field | Required | Meaning |
| --- | --- | --- |
| `module` | yes | Uppercase module identity, e.g. `REDR`, `PSP2`, `DTML`, `LRC2`. |
| `status` | yes | One of `ACTIVE`, `WAIT`, `REVIEW_REQUIRED`, `STANDBY`, `STOP`, `ERROR`, `UNAVAILABLE`, or a documented extension. |
| `confidence` | yes | Float from `0.0` to `1.0`; must not imply completion by itself. |
| `input_type` | yes | Short type label describing what was read, routed, reviewed, or recorded. |
| `decision` | yes | Machine-readable decision label. |
| `reason` | yes | Human-readable reason. |
| `next` / `next_modules` | yes | Ordered next handoff candidates. |
| `standby` | yes | Modules intentionally not activated now. |
| `details` | yes | Module-specific trace payload. |
| `mutated` | yes | Must default to `false`; `true` requires explicit approved adapter. |
| `traceable` | yes | Must show whether the result can be audited. |
| `review` | conditional | Required when route is unknown, cross-system, risky, or incomplete. |

No module may report `COMPLETED` unless it actually performed an approved local executor action and produced a real artifact or verified result.

---

## 4. Shared identity minimum

Every package or event crossing W3Lgu runtime should preserve these identity fields when available:

```text
chain_id
process_id
event_id
package_id
sequence
source
target
route_scope
predecessor
successor
owner_scope
mutated
traceable
```

If a field is unknown, the module must preserve the unknown state explicitly instead of silently dropping it.

Recommended unknown form:

```json
{
  "unknown": true,
  "reason": "missing_from_input",
  "review": true
}
```

---

## 5. Module-specific minimums

### 5.1 REDR minimum

REDR is the reader and package builder.

Minimum responsibilities:

- Read input without mutating source truth.
- Normalize input into a package envelope.
- Tag route, risk, trace, memory, structure, and signal hints.
- Create or preserve `package_id`.
- Duplicate package pointers to PSP2 and LRC2 by default.
- Send risk or governance markers to DTML for review.
- Preserve original payload inside a non-mutating package.

Current status:

- **Partial pass, improved 2026-07-07.** `redr_mfc_logic.py` builds a package, tags input, creates copies for PSP2/LRC2, marks source mutation as false, and now preserves shared identity fields when present.
- Remaining gap: REDR still needs broader integration tests for every identity field and upstream UI/API package shapes.

Minimum next step:

- Add required identity preservation and explicit unknown handling to REDR package output.

---

### 5.2 PSP2 minimum

PSP2 is the pointer-stamp and package transport station.

Minimum responsibilities:

- Receive package.
- Do not inspect, rewrite, approve, or execute payload content.
- Stamp package with deterministic route stamp.
- Preserve source, target, package identity, and event identity.
- Route to local and cross-system destinations when declared.
- Never drop unknown or external destination silently.
- Classify route scope as one of:

```text
local_w3lgu
cross_series
external
mixed
unknown
```

- Send a short handoff summary to LRC2.
- Return `REVIEW_REQUIRED` when a route is unknown, external, or cross-system without a bridge contract.
- Preserve all unsupported destinations in `details.unknown_routes` or `details.cross_routes`.

Current status:

- **Partial pass, improved 2026-07-07.** `psp2_mfc_logic.py` now separates local W3Lgu routes, cross-series systems, and unknown routes.
- It can stamp a package, preserve unknown/cross destinations, classify `route_scope`, and return `REVIEW_REQUIRED` when a cross or unknown route lacks a bridge contract.
- Remaining gap: WHUB/W3-API adapter execution is still not connected; PSP2 remains route/stamp/review-only.

Minimum next step:

- Continue expanding the route registry as WHUB/W3-API adapters become concrete.
- Keep tests proving that PSP2 preserves unknown/cross destinations instead of dropping them.

---

### 5.3 DTML minimum

DTML is the decision and detection authority.

Minimum responsibilities:

- Inspect route intent, destination, risk, governance, and review signals.
- Decide whether a package can continue, must wait, must stop, or needs human review.
- Never mutate source payload.
- Emit a decision trace with reason and review state.
- Stop or review suspicious cross-system handoffs.
- Preserve trace identity for LRC2.

Current status:

- **Partial pass, improved 2026-07-07.** Current MFC logic can build decision traces and review state, and now reviews unknown/cross route metadata emitted by PSP2.
- Remaining gap: DTML still needs full bridge-contract policy rules before any execution adapter is allowed.

Minimum next step:

- Add decision rules for `route_scope`, `unknown_routes`, `cross_routes`, and missing bridge contracts.

---

### 5.4 LRC2 minimum

LRC2 is the lifecycle recorder and immutable history preview.

Minimum responsibilities:

- Receive copies from REDR and PSP2.
- Record every stage preview without mutating source truth.
- Create checkpoint key or ledger preview.
- Preserve success, failure, wait, review, stop, and unavailable states.
- Preserve package/event/chain identity.
- Make record phase explicit.
- Never overwrite historical truth.

Current status:

- **Partial pass, improved 2026-07-07.** Current MFC logic creates a checkpoint preview, stable key, route stamp reference, prior stage summary, and preserved identity when available.
- Remaining gap: immutable append behavior is still a preview and requires an approved append adapter.

Minimum next step:

- Require `chain_id`, `event_id`, `package_id`, `route_stamp`, and prior stage summaries when available.

---

### 5.5 Logic27 minimum

Logic27 is a local event-field selector, not a global authority model.

Minimum responsibilities:

- Select a logic slot from event field context.
- Preserve chain/event identity.
- Mark proposal-only or reference-only outputs clearly.
- Never claim authority over unrelated systems.

Current status:

- **Partial pass.** Current selector preserves event identity and marks reference-only/proposal-only details.
- Gap: Logic27 should be documented as advisory unless an approved runtime adapter consumes it.

Minimum next step:

- Add a small test or doc rule that Logic27 cannot approve execution by itself.

---

## 6. Runtime minimums

### 6.1 `core/runtime/agents/base.py`

Minimum responsibilities:

- Provide a safe default for every runtime agent.
- Never fabricate success.
- Return `UNAVAILABLE` when no real executor exists.
- Require module-specific `execute()` before reporting `COMPLETED`.
- Preserve review flag and mutation state.

Current status:

- **Pass for no-fake-success baseline.** Current `execute()` returns `UNAVAILABLE`, `mutated: False`, `review: True`, and no artifacts when a module lacks a local executor.

Gap:

- Base contract should be documented as the required fallback for all W3Lgu runtime agents.
- Agent wrappers should be checked to ensure none bypass this rule with fabricated success text.

---

### 6.2 `core/runtime/engine_v2.py`

Minimum responsibilities:

- Build traceable context with `trace_id`, source, target, mode, payload, and timestamp.
- Dispatch through registered agents.
- Require dictionary result from `execute()`.
- Treat only `COMPLETED` as success.
- Save runtime memory with status that reflects real agent result.
- Return failure with trace ID on exception.

Current status:

- **Partial pass, improved 2026-07-07.** `engine_v2.py` builds trace IDs, dispatches to agents, requires dict results, treats only `COMPLETED` as successful, and now returns a non-mutating result validation summary.

Gap:

- It does not yet block execution on every missing W3Lgu-specific identity field; current behavior reports `review_required` validation metadata for incomplete W3Lgu module results.
- It should grow from validation summary to strict adapter boundary before WHUB/cross execution.

Minimum next step:

- Add a result validator or adapter boundary for W3Lgu module outputs.

---

### 6.3 `core/runtime/engine.py`

Minimum responsibilities:

- Legacy engine must not report fake success for placeholder execution.

Current status:

- **Pass for no-fake-success baseline, improved 2026-07-07.** `engine.py` remains legacy/demo-style but no longer reports placeholder `SUCCESS`; it returns `UNAVAILABLE`, `mutated: false`, and `review: true`.

Minimum next step:

- Mark `engine.py` as legacy/demo-only or align it with `engine_v2.py` / `RuntimeAgent.execute()` no-fake-success behavior.

---

### 6.4 `core/runtime/process_layer.py`

Minimum responsibilities:

- Provide plan-only REDR → PSP2 → DTML → LRC2 trace.
- Avoid source truth mutation by default.
- Preserve package and process identity.
- Keep optional persistence behind explicit approved adapter.

Current status:

- **Partial pass, improved 2026-07-07.** It defines immutable package and stage records, marks default output as plan-only, avoids automatic persistence, and now carries route-scope/cross-route metadata in stage records.

Gap:

- `PROCESS_STAGES` remains the local plan-only trace (`REDR`, `PSP2`, `DTML`, `LRC2`) by design.
- Cross-system execution is intentionally not connected; only route metadata is preserved.

Minimum next step:

- Add optional cross-chain stage metadata without making process layer execute external systems.

---

## 7. Pass / fail summary

| Surface | Status | Reason |
| --- | --- | --- |
| `core/runtime/agents/base.py` | PASS | Safe fallback prevents fabricated completion. |
| `core/runtime/engine_v2.py` | PASS for minimum checklist | Strict W3Lgu field validation exists; non-dict agent outputs become non-success review results; success remains `COMPLETED` only. |
| `core/runtime/engine.py` | PASS for no-fake-success | Legacy placeholder no longer reports `SUCCESS`; it returns `UNAVAILABLE`. |
| `core/runtime/process_layer.py` | PASS for plan-only route metadata | REDR/PSP2/DTML/LRC2 stages preserve route scope/cross/unknown metadata without external execution. |
| `redr_mfc_logic.py` | PARTIAL | Package/tag/copy behavior and identity preservation exist; broader package-source coverage remains. |
| `psp2_mfc_logic.py` | PARTIAL | Local/cross/unknown routes are preserved; adapter execution remains intentionally disconnected. |
| `dtml_mfc_logic.py` | PARTIAL | Review trace covers unknown/cross route metadata; bridge-contract policy needs deeper rules. |
| `lrc2_mfc_logic.py` | PASS for preview identity checklist | Checkpoint preview preserves route stamp/prior summary/identity and emits explicit unknown objects for missing identity fields. |
| `logic27_selector.py` | PASS for advisory guard | Event identity is preserved and Logic27 is explicitly advisory/proposal-only with no execution approval authority. |

---

## 8. Required test minimums before calling W3Lgu module work complete

At minimum, add or preserve tests for:

1. REDR creates package and duplicate pointers to PSP2/LRC2.
2. PSP2 stamps local routes.
3. PSP2 preserves unknown routes and returns review instead of dropping them.
4. PSP2 preserves cross-system routes without executing them.
5. DTML reviews unknown/cross routes.
6. LRC2 records route stamp and prior stage summary.
7. Base agent fallback returns `UNAVAILABLE`, not success.
8. `engine_v2.py` refuses non-dict agent results.
9. Legacy `engine.py` does not report placeholder `SUCCESS`, or is marked demo-only.
10. Logic27 cannot approve execution by itself.

---

## 9. Safe implementation order

```text
1. Document and freeze the minimum contract.
2. Add tests for unknown/cross route preservation.
3. Update PSP2 route registry and result details.
4. Update DTML route-scope review rules.
5. Update LRC2 checkpoint identity requirements.
6. Add W3Lgu result validator for engine_v2.
7. Mark engine.py legacy/demo-only or remove fake success behavior.
8. Only then connect WHUB / W3-API / cross adapters.
```

---

## 10. Non-negotiable guardrails

- PSP2 must never silently drop a destination.
- Unknown is a review state, not a deletion rule.
- Cross-system route is a preserved handoff, not an automatic execution.
- BOX / wx may point, describe, index, and export references, but must not execute or approve merge.
- W3Lgu may carry meaning and packet shape, but must not be reduced to parser-first or local-only pipeline.
- Runtime must not report success without a real executor and artifact/result.
- Every module must be small enough to review and complete enough not to cut future development paths.

---

## 11. Acceptance criteria for this request

This request is accepted when:

- The minimum spec is present in `requests/`.
- Future W3Lgu patches can cite this document as baseline.
- PSP2 work is not considered complete until unknown/cross routes are preserved.
- `base.py`, `engine_v2.py`, and `core/runtime` changes are reviewed against this spec before implementation.
