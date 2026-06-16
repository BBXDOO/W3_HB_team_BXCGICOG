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
ROT = verify rule shape, relation, and boundary
CROLL / Cross-L = plan only, after ROT accepts the command shape
Modew / executor = run only after review/authority
```

---

## 2. ROT as rule framework

ROT is closer to a framework than a command runner.

It does not order work.  
It does not select language meaning.  
It does not decide the user's intention.  
It does not create execution authority.

ROT only defines the rules that must be clear before another layer may continue.

```text
ROT says: this command shape is valid / invalid
ROT says: this command has boundary / no boundary
ROT says: this result envelope is valid / invalid
ROT says: this Paper Pack can be traced / cannot be traced
ROT does not say: run this now
```

The command language can evolve outside ROT.  
The Paper format can evolve outside ROT.  
Paper Pack can grow into multi-site / multi-agent governance outside ROT.

ROT stays stable by enforcing only the minimum law surface.

---

## 3. Paper command minimum

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
TARGET
TARGETS
PX
MODEW
ROLE
CONTEXT_REF
STACK_REF
KNOWLEDGE_BASE_REF
RETURN_CONTRACT
REVIEW
DENY
META
```

ROT rejects unknown fields by default so Paper commands cannot drift into ambiguous formats.

---

## 4. Paper Pack

Paper Pack is a bundle of Paper commands controlled under one governance boundary.

Minimum structure:

```json
{
  "PAPER_PACK_ID": "PACK-001",
  "SCOPE": "CROSS_L_ONLY",
  "BOUNDARY": "W3-INTERNAL",
  "PAPERS": [
    {
      "PAPER_ID": "PAPER-001",
      "TASK": "Create CROLL plan",
      "INTENT": "PLAN_ONLY",
      "PX": "PX:[2,1]"
    },
    {
      "PAPER_ID": "PAPER-002",
      "TASK": "Validate dispatch plan",
      "INTENT": "VALIDATE_ONLY",
      "PX": "PX:[2,2]"
    }
  ]
}
```

Pack-level `SCOPE`, `BOUNDARY`, `CONTEXT_REF`, `STACK_REF`, and `KNOWLEDGE_BASE_REF` can be inherited by child papers.
This leaves room for future multi-site / multi-agent governance without turning ROT into an executor.

---

## 5. Result envelope

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

## 6. Stack baseline

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

## 7. Minimum knowledge baseline

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

## 8. CROLL / Cross-L rule

CROLL and Cross-L must stay plan-only until MPCP/ROT/Modew approve execution.

Recommended order:

```text
Paper / Paper Pack
→ W3Lgu / normalizer
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

## 9. Absolute rule

ROT must make short Paper commands usable without interpretation.

That means:

```text
No language conversion inside ROT
No missing-intent guessing inside ROT
No command issuing inside ROT
No execution inside ROT
No source-truth mutation inside ROT
No environment mutation inside ROT
```

If a command is unclear, ROT must stop and return a reason.
