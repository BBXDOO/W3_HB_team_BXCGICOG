# ROT Baseline for MPCP

Status: ACTIVE DRAFT  
Owner: BBX19  
Scope: MPCP / Paper / Paper Pack / CROLL / Cross-L boundary

---

## 1. Purpose

ROT is the minimum law layer for MPCP runtime governance.

ROT does not translate language, does not infer missing intent, and does not execute work.
Its job is to make sure a Paper command is clear enough that MPCP can route it without guessing.

In W3 terms:

```text
W3Lgu / Paper normalizer = convert language / shorthand / synonym
Cross-L = return values into the same language/value core
REDR = read / reduce / classify before packaging
ROT = verify rule shape, relation, and boundary
CROLL / Cross-L = plan only, after ROT accepts the command shape
PSP2 = distribution layer inside W3Lgu flow
MPCP = event-first governance, not unit-first dispatch
Modew / executor = run only after review/authority
```

---

## 2. ROT as rule framework

ROT is closer to a framework than a command runner.

It does not order work.  
It does not select language meaning.  
It does not decide the user's intention.  
It does not create execution authority.  
It does not choose the unit that must perform the work.

ROT only defines the rules that must be clear before another layer may continue.

```text
ROT says: this command shape is valid / invalid
ROT says: this command has boundary / no boundary
ROT says: this result envelope is valid / invalid
ROT says: this Paper Pack can be traced / cannot be traced
ROT does not say: run this now
ROT does not say: send this to unit X
```

The command language can evolve outside ROT.  
The Paper format can evolve outside ROT.  
Paper Pack can grow into multi-site / multi-agent governance outside ROT.

ROT stays stable by enforcing only the minimum law surface.

---

## 3. ROT reader flow

A system that comes to read ROT should follow this shape:

```text
1. Select rule category
2. Read rule / boundary surface
3. Attach Paper or Paper Pack
4. Attach event / event reference when available
5. Return to REDR before packaging
6. Package and send Paper onward
```

The reader may send:

```text
CATEGORY
PAPER or PAPER_PACK
EVENT or EVENT_REF
CONTEXT_REF
ENV_REF
STACK_REF
META
```

ROT validates this structure. It does not decide the work unit.

---

## 4. REDR before packaging

When Cross-L returns values back into the shared language/value core, the value should pass REDR first.

```text
Cross-L return
→ REDR read/reduce/classify
→ package
→ Paper / Paper Pack
→ event governance
```

Reason:

```text
Cross-L may normalize value shape
REDR prepares the value for system-readable packaging
Paper carries the work content and governance marker
ROT checks rule clarity and boundary
```

ROT should not directly wrap raw Cross-L values into an execution package.

---

## 5. W3Lgu vs MPCP distribution boundary

Inside W3Lgu structure:

```text
PSP2 = distributor / transport / package spread layer
```

Inside MPCP structure:

```text
MPCP = event-first governance
```

MPCP does not need to care whether a Paper will govern another system.
It must care that the event, Paper content, boundary, and return contract are clear.

Therefore Paper should specify content tightly, not the exact unit that must execute it.

```text
Good: TASK + INTENT + SCOPE + BOUNDARY + EVENT_REF
Avoid: force unit X to perform this action
```

The responsible unit is selected later by logic, context, capability, and ENV.

---

## 6. Paper command minimum

A short Paper command must be normalized before it reaches ROT.

Required fields:

```text
TASK      = what work is requested
INTENT    = why / operation purpose
SCOPE     = allowed work area
BOUNDARY  = boundary manifest id or boundary marker
```

Optional fields reserved for extension:

```text
PAPER_ID
PAPER_PACK_ID
CATEGORY
EVENT_ID
EVENT_REF
CONTENT
TARGET
TARGETS
PX
MODEW
ROLE
CONTEXT_REF
ENV_REF
STACK_REF
KNOWLEDGE_BASE_REF
REDR_STATE
PACKAGE_REF
PSP2_STATE
RETURN_CONTRACT
REVIEW
DENY
META
```

Note:

```text
TARGET / TARGETS are content or governance markers.
They must not be treated as forced executor identity by ROT.
```

ROT rejects unknown fields by default so Paper commands cannot drift into ambiguous formats.

---

## 7. Paper Pack

Paper Pack is a bundle of Paper commands controlled under one governance boundary.

Minimum structure:

```json
{
  "PAPER_PACK_ID": "PACK-001",
  "CATEGORY": "CROLL_PLAN",
  "SCOPE": "CROSS_L_ONLY",
  "BOUNDARY": "W3-INTERNAL",
  "PAPERS": [
    {
      "PAPER_ID": "PAPER-001",
      "TASK": "Create CROLL plan",
      "INTENT": "PLAN_ONLY",
      "PX": "PX:[2,1]",
      "EVENT_REF": "EV-001"
    },
    {
      "PAPER_ID": "PAPER-002",
      "TASK": "Validate dispatch plan",
      "INTENT": "VALIDATE_ONLY",
      "PX": "PX:[2,2]",
      "EVENT_REF": "EV-002"
    }
  ]
}
```

Pack-level `CATEGORY`, `SCOPE`, `BOUNDARY`, `CONTEXT_REF`, `ENV_REF`, `STACK_REF`, and `KNOWLEDGE_BASE_REF` can be inherited by child papers.
This leaves room for future multi-site / multi-agent governance without turning ROT into an executor.

---

## 8. Result envelope

Canonical strict result shape:

```json
{
  "schema": "mpcp.result.v1",
  "state": "SUCCESS",
  "cause": "Paper command accepted",
  "action": "Validate and plan",
  "result": {},
  "error": null,
  "trace": [],
  "law": {
    "validated": true,
    "blocked_by": null
  },
  "restore": {
    "supported": false,
    "checkpoint": null,
    "rollback_hint": null
  },
  "meta": {
    "return_code": 0,
    "format": "dict",
    "version": 1
  },
  "source_truth_mutated": false,
  "env_mutated": false,
  "event_container_mutated": false
}
```

Halt states must include `error`:

```text
STOP
fail
block
```

---

## 9. Stack baseline

When a system can keep stack, each stack frame should have at least one trace marker:

```text
EVENT_ID
PAPER_ID
TASK
STATE
RESULT
```

ROT does not interpret the full stack yet. It only checks that frames are traceable.

---

## 10. Minimum knowledge baseline

ROT does not carry the full knowledge base.
It only needs to know which baseline is being used.

Minimum:

```json
{
  "BASELINE": "MPCP-ROT-BASELINE-v1"
}
```

Future systems may replace or extend the baseline without changing Paper command shape.

---

## 11. CROLL / Cross-L rule

CROLL and Cross-L must stay plan-only until MPCP/ROT/Modew approve execution.

Recommended order:

```text
Paper / Paper Pack
→ W3Lgu / normalizer
→ Cross-L value return if needed
→ REDR read/reduce/classify
→ ROT validate paper command
→ MPCP boundary / Condien / Modew review
→ CROLL / Cross-L plan
→ validate result envelope
→ executor only if approved
```

Default return for CROLL / Cross-L planning:

```json
{
  "allowed_to_execute": false,
  "requires_modew_review": true,
  "source_truth_mutated": false,
  "env_mutated": false
}
```

---

## 12. Absolute rule

ROT must make short Paper commands usable without interpretation.

That means:

```text
No language conversion inside ROT
No missing-intent guessing inside ROT
No command issuing inside ROT
No execution inside ROT
No forced executor/unit selection inside ROT
No source-truth mutation inside ROT
No environment mutation inside ROT
```

If a command is unclear, ROT must stop and return a reason.
