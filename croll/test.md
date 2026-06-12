# Cross-L Test Guide

**Document Path:** `croll/test.md`  
**Status:** ACTIVE DRAFT  
**Purpose:** Test guidance for Cross-L examples using `.py`, `.json`, and `.lua` fragments

---

# 1. Purpose

This document gives an early test direction for Cross-L / CrossCode.

The goal is not to execute unrestricted code.

The goal is to test whether a Cross-L block can preserve:

- declared language
- boundary
- allowed input
- denied action
- return contract
- traceability
- review behavior

A Cross-L test should answer:

```text
Does this fragment stay inside its declared cross boundary?
Does it return a useful state/reason instead of uncontrolled behavior?
```

---

# 2. Minimal Test Rule

Every Cross-L fragment should be tested against these rules:

```text
1. It declares LANG.
2. It declares BOUNDARY.
3. It declares INPUT or READ.
4. It declares DENY.
5. It declares RETURN.
6. It returns state.
7. It returns reason.
8. It does not mutate truth by default.
9. It returns review/block on uncertainty or violation.
10. It can be logged by the parent system.
```

---

# 3. Expected Return Shape

Recommended return object:

```json
{
  "state": "pass|review|block|fail",
  "reason": "short_reason",
  "trace": ["INPUT", "EVALUATE", "RETURN"],
  "mutated": false,
  "review": false
}
```

Minimum return object:

```json
{
  "state": "review",
  "reason": "missing_context"
}
```

---

# 4. Test Matrix

| Case | Expected Result |
|---|---|
| Valid observe boundary | `pass` |
| Missing context | `review` |
| Mutation requested | `block` |
| Unknown boundary | `review` |
| Runtime error | `fail` or `review` with reason |
| Weak return such as `true` | reject / wrap as `review` |
| Missing state | reject / wrap as `review` |
| Missing reason | reject / wrap as `review` |

---

# 5. Cross-L Example: Lua

## 5.1 File

Suggested file:

```text
croll/examples/env_check.lua
```

## 5.2 Cross-L Block

```text
CROSS-L:ENV_CHECK
POINT:ENV_MODEW_CONDIEN
LANG:lua
BOUNDARY:observe
INPUT:ctx
READ:ENV,CONDIEN.LayerA
DENY:truth_mutation,file_write,network,merge
RETURN:state,reason,trace,mutated,review
REVIEW:on_uncertain
```

## 5.3 Lua Fragment

```lua
local M = {}

function M.evaluate(ctx)
  local trace = {"INPUT", "EVALUATE", "RETURN"}

  if ctx == nil then
    return {
      state = "review",
      reason = "missing_context",
      trace = trace,
      mutated = false,
      review = true
    }
  end

  if ctx.mutated == true then
    return {
      state = "block",
      reason = "mutation_not_allowed",
      trace = trace,
      mutated = false,
      review = true
    }
  end

  if ctx.boundary ~= "observe" then
    return {
      state = "review",
      reason = "unknown_or_unsafe_boundary",
      trace = trace,
      mutated = false,
      review = true
    }
  end

  return {
    state = "pass",
    reason = "observe_boundary_ok",
    trace = trace,
    mutated = false,
    review = false
  }
end

return M
```

## 5.4 Manual Lua Test Idea

A future Lua harness should test:

```text
ctx=nil                → review
ctx.mutated=true       → block
ctx.boundary=execute   → review
ctx.boundary=observe   → pass
```

---

# 6. Cross-L Example: Python

## 6.1 File

Suggested file:

```text
croll/examples/trace_check.py
```

## 6.2 Cross-L Block

```text
CROSS-L:TRACE_CHECK
POINT:RESULT_ROT_LRC2
LANG:python
BOUNDARY:trace-only
INPUT:ctx
READ:result,trace
DENY:truth_mutation,repo_write,network,merge
RETURN:state,reason,missing,trace,mutated,review
REVIEW:on_fail
```

## 6.3 Python Fragment

```python
def evaluate(ctx):
    trace = ["INPUT", "EVALUATE", "RETURN"]

    if not isinstance(ctx, dict):
        return {
            "state": "review",
            "reason": "invalid_context",
            "missing": ["ctx"],
            "trace": trace,
            "mutated": False,
            "review": True,
        }

    missing = []
    for key in ("cause", "action", "result"):
        if key not in ctx:
            missing.append(key)

    if missing:
        return {
            "state": "review",
            "reason": "missing_trace_fields",
            "missing": missing,
            "trace": trace,
            "mutated": False,
            "review": True,
        }

    return {
        "state": "pass",
        "reason": "trace_complete",
        "missing": [],
        "trace": trace,
        "mutated": False,
        "review": False,
    }
```

## 6.4 Manual Python Test Idea

```text
{}                                           → review
{"cause":"a"}                              → review
{"cause":"a","action":"b","result":"c"} → pass
non-dict input                               → review
```

---

# 7. Cross-L Example: JSON

## 7.1 File

Suggested file:

```text
croll/examples/boundary_rule.json
```

## 7.2 Cross-L Block

```text
CROSS-L:BOUNDARY_RULE
POINT:API_GATEWAY_CROSS
LANG:json
BOUNDARY:gateway-only
INPUT:request
DENY:truth_mutation,direct_merge,runtime_state_write
RETURN:state,reason,trace,mutated,review
REVIEW:on_violation
```

## 7.3 JSON Rule Object

```json
{
  "name": "BOUNDARY_RULE",
  "rules": [
    {
      "when": { "mutated": true },
      "return": {
        "state": "block",
        "reason": "mutation_not_allowed",
        "trace": ["INPUT", "CHECK_MUTATION", "RETURN"],
        "mutated": false,
        "review": true
      }
    },
    {
      "when": { "boundary": "gateway-only" },
      "return": {
        "state": "pass",
        "reason": "gateway_boundary_ok",
        "trace": ["INPUT", "CHECK_BOUNDARY", "RETURN"],
        "mutated": false,
        "review": false
      }
    }
  ],
  "default": {
    "state": "review",
    "reason": "no_rule_matched",
    "trace": ["INPUT", "DEFAULT_REVIEW", "RETURN"],
    "mutated": false,
    "review": true
  }
}
```

## 7.4 Manual JSON Test Idea

```text
{"mutated": true}                 → block
{"boundary": "gateway-only"}      → pass
{"boundary": "unknown"}           → review
{}                                  → review
```

---

# 8. Test Harness Concept

A future Cross-L test harness may follow this process:

```text
1. Read Cross-L metadata.
2. Extract LANG.
3. Confirm BOUNDARY and DENY exist.
4. Load fragment in safe mode.
5. Provide controlled ctx.
6. Capture return object.
7. Validate return contract.
8. Reject weak output.
9. Confirm mutated=false unless explicitly allowed.
10. Emit test report.
```

---

# 9. Suggested Python Pseudocode Harness

```python
REQUIRED_FIELDS = {"state", "reason"}

VALID_STATES = {"pass", "review", "block", "fail"}


def validate_cross_l_result(result):
    if not isinstance(result, dict):
        return {
            "state": "review",
            "reason": "weak_or_invalid_return",
            "mutated": False,
            "review": True,
        }

    missing = REQUIRED_FIELDS - set(result)
    if missing:
        return {
            "state": "review",
            "reason": "missing_return_fields",
            "missing": sorted(missing),
            "mutated": False,
            "review": True,
        }

    if result.get("state") not in VALID_STATES:
        return {
            "state": "review",
            "reason": "invalid_state",
            "mutated": False,
            "review": True,
        }

    if result.get("mutated") is True:
        return {
            "state": "block",
            "reason": "unexpected_mutation",
            "mutated": False,
            "review": True,
        }

    return result
```

---

# 10. Expected First Test Files

Suggested future files:

```text
croll/
├── README.md
├── test.md
├── examples/
│   ├── env_check.lua
│   ├── trace_check.py
│   └── boundary_rule.json
└── tests/
    ├── test_cross_l_contract.py
    ├── test_cross_l_json_rule.py
    └── test_cross_l_metadata.py
```

---

# 11. Definition of Passing

A Cross-L test passes when:

```text
- metadata is readable
- boundary is declared
- denied actions are declared
- fragment returns structured output
- output has state and reason
- unsafe conditions return review or block
- no truth mutation occurs by default
- result can be logged by parent system
```

---

# 12. Final Note

Cross-L testing should not begin by asking:

```text
Can this code run?
```

It should begin by asking:

```text
Can this code remain governed while participating in a cross point?
```

END
