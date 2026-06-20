# W3Lgu Minimum Module Spec Request

ID: RQ-W3LGU-MINIMUM-MODULE-SPEC
TIMESTAMP: 2026-06-20
REQUESTER: BBX19
STATUS: draft / request / minimum-baseline
SCOPE: W3Lgu modules, `core/runtime`, `core/runtime/agents/base.py`, `core/runtime/engine_v2.py`
MUTATION: false for this document; this request only defines minimum spec and gap notes.

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

- **Partial pass.** `redr_mfc_logic.py` builds a package, tags input, creates copies for PSP2/LRC2, and marks source mutation as false.
- Gap: cross-system identity fields such as `chain_id`, `event_id`, and `route_scope` are not yet a required package shape.

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

- **Fail for cross-system minimum / partial pass for local MFC proof.** `psp2_mfc_logic.py` currently recognizes only `REDR`, `PSP2`, `DTML`, and `LRC2` as known modules.
- It can stamp a package and prepare local route previews.
- Gap: cross-system destinations such as `PX`, `W3DB_APPEND`, `EP_SIGNAL`, `EP_SIGNAL_RYTM`, `Hospitication`, `IGET`, `WHUB`, or `W3-API` are not preserved as known cross routes.
- Gap: unknown requested modules are filtered out instead of being preserved for review.

Minimum next step:

- Replace local-only route validation with a route registry that separates local modules, cross-series systems, external routes, and unknown routes.
- Add tests proving that PSP2 preserves unknown/cross destinations instead of dropping them.

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

- **Partial pass.** Current MFC logic can build decision traces and review state.
- Gap: DTML should explicitly inspect route scope and unknown/cross destination risks once PSP2 preserves them.

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

- **Partial pass.** Current MFC logic creates a checkpoint preview and stable key.
- Gap: immutable append behavior and cross-chain identity are not yet enforced at the W3Lgu MFC result level.

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

- **Partial pass.** `engine_v2.py` builds trace IDs, dispatches to agents, requires dict results, and treats only `COMPLETED` as successful.

Gap:

- It does not yet enforce W3Lgu-specific fields such as `chain_id`, `event_id`, `package_id`, `route_scope`, `mutated`, `traceable`, and `review`.
- It should validate module results against the W3Lgu minimum contract before saving memory.

Minimum next step:

- Add a result validator or adapter boundary for W3Lgu module outputs.

---

### 6.3 `core/runtime/engine.py`

Minimum responsibilities:

- Legacy engine must not report fake success for placeholder execution.

Current status:

- **Fail for no-fake-success baseline.** `engine.py` still uses `simulate_agent()` and returns `status: SUCCESS` even though it is a placeholder.

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

- **Partial pass.** It defines immutable package and stage records, marks default output as plan-only, and avoids automatic persistence.

Gap:

- `PROCESS_STAGES` is still local-only: `REDR`, `PSP2`, `DTML`, `LRC2`.
- Cross-system route scope is not yet represented in stage records.

Minimum next step:

- Add optional cross-chain stage metadata without making process layer execute external systems.

---

## 7. Pass / fail summary

| Surface | Status | Reason |
| --- | --- | --- |
| `core/runtime/agents/base.py` | PASS | Safe fallback prevents fabricated completion. |
| `core/runtime/engine_v2.py` | PARTIAL | Traceable dispatch exists, but W3Lgu result validation is missing. |
| `core/runtime/engine.py` | FAIL | Placeholder simulation can still return `SUCCESS`. |
| `core/runtime/process_layer.py` | PARTIAL | Plan-only flow exists, but local-only stage model lacks cross-route preservation. |
| `redr_mfc_logic.py` | PARTIAL | Package/tag/copy behavior exists; chain identity contract missing. |
| `psp2_mfc_logic.py` | FAIL for cross minimum | Local stamp/route exists, but unknown/cross routes are filtered out. |
| `dtml_mfc_logic.py` | PARTIAL | Review trace exists; cross-route decision rules missing. |
| `lrc2_mfc_logic.py` | PARTIAL | Checkpoint preview exists; immutable cross-chain identity enforcement missing. |
| `logic27_selector.py` | PARTIAL | Event identity preserved; advisory-only authority needs explicit guard test/doc. |

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

