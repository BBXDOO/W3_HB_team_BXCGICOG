# CROLL / Cross-L

## Cross Language Governance Layer

**Document Path:** `croll/README.md`  
**Status:** ACTIVE DRAFT  
**System Relation:** W3 / W3Lgu / MPCP / Cross-X / Condien / Paper  
**Owner:** BBX19  
**Purpose:** Concept foundation for Cross-L / CrossLgu / CrossCode

---

# 1. Core Statement

Cross-L is a proposed cross-language insertion and governance layer.

It is not intended to replace W3Lgu, MPCP, Lua, Python, JSON, JavaScript, or any existing runtime language.

Cross-L exists to describe, limit, connect, and govern code or logic fragments that appear inside cross-system work.

In short:

```text
Cross-L = language between languages
CrossCode = governed code fragment inside a cross point
```

The purpose is not only value conversion.

The purpose is to preserve:

- meaning
- boundary
- role
- return contract
- execution context
- traceability
- platform adaptability

while allowing multiple languages or runtimes to participate in the same work.

---

# 2. Background

W3 is not a single-language system.

W3 contains multiple forms of expression and operation:

- W3Lgu for meaning / event / packet expression
- MPCP for adaptive operational structure
- Cross-X for cross-point coordination
- Condien for state / context / meaning containers
- Paper for task-scoped clarity
- Modew for bounded operational units
- external runtimes such as Python, JSON, Lua, JavaScript, shell, API, and future engines

Traditional integration usually depends on repeated conversion:

```text
System A value
→ convert
→ System B value
→ convert back
→ return value
```

This approach may become insufficient when the important object is not only a value, but also:

- local rule
- runtime behavior
- boundary condition
- context-specific interpretation
- ENV adaptation
- recovery logic
- review requirement
- trace requirement

Cross-L is proposed as a response to this problem.

Instead of moving only values, Cross-L carries a governed fragment with context and return rules.

---

# 3. Problem Statement

In a multi-platform, multi-agent, multi-runtime ecosystem, the following problems appear:

1. Value conversion loses meaning.
2. Different runtimes interpret the same data differently.
3. A code fragment may execute outside its intended boundary.
4. Agents may assume more authority than their role allows.
5. Schema may reject damaged format even when valid meaning remains.
6. A system may need local behavior without rewriting the core.
7. Platform-specific code may break portability.
8. A work item may require more than one cross point.
9. Not every unit needs to understand the whole ecosystem.
10. Returning only `true` or `false` is too weak for traceable governance.

Cross-L addresses these problems by making the insertion point explicit.

---

# 4. Definitions

## 4.1 Cross-L

Cross-L is a cross-language governance layer used to declare how a code or logic fragment is inserted into a W3 cross point.

It describes:

- where the fragment belongs
- what language it uses
- what it may read
- what it may not touch
- what boundary governs it
- what output it must return
- what system receives the output
- whether human review is required

## 4.2 CrossLgu

CrossLgu is the language-oriented name of the same concept.

It emphasizes that Cross-L belongs to the W3 language family and is related to W3Lgu, but it serves a different role.

## 4.3 CrossCode

CrossCode is the actual embedded or inserted code fragment governed by Cross-L.

Example languages:

- Python
- Lua
- JSON rule object
- JavaScript
- shell command wrapper
- future runtime language

## 4.4 Cross Point

A cross point is a point, phase, or area in a work item where multiple factors must meet in order to produce a valid result.

One work item may contain many cross points.

A cross point may involve more than two factors.

Example:

```text
Cross Point: MODEW_CONDIEN_ENV
Factors: Modew + Condien + ENV + Paper + Boundary
Expected Result: traceable decision state
```

## 4.5 Language Insertion

Language insertion means placing a code fragment from one language into a governed cross context without allowing that fragment to become uncontrolled authority.

---

# 5. Conceptual Position

Cross-L is not a normal programming language.

Cross-L is not only a transpiler.

Cross-L is not only an adapter.

Cross-L is not only a foreign function interface.

Cross-L is closer to:

```text
embedded cross-language governance
```

It governs how code fragments from different languages participate in one task while remaining bounded, traceable, and return-compatible.

---

# 6. Relation to W3 Systems

## 6.1 Relation to W3Lgu

W3Lgu expresses meaning, events, context, and packet structure.

Cross-L may use W3Lgu-like declarations, but its specific role is to govern inserted code fragments.

```text
W3Lgu  = meaning / event / packet language
Cross-L = inserted-code governance language
```

## 6.2 Relation to MPCP

MPCP provides adaptive operational structure.

Cross-L gives MPCP a possible method for portable behavior across platforms.

```text
MPCP structure remains stable.
Cross-L allows behavior fragments to adapt.
```

## 6.3 Relation to Cross-X

Cross-X coordinates cross points.

Cross-L describes the code or logic fragment used inside one or more cross points.

```text
Cross-X = cross-point coordinator
Cross-L = cross-code declaration and boundary layer
```

## 6.4 Relation to Paper

Paper defines the task scope and expected work.

Cross-L may reference Paper to make the code fragment task-scoped.

```text
Paper defines.
Cross-L inserts.
Modew executes.
MPCP validates.
LRC2 logs.
```

## 6.5 Relation to Condien

Condien carries state, context, and meaning.

Cross-L can declare which Condien layers a code fragment may read.

Example:

```text
READ:CONDIEN.LayerA,CONDIEN.LayerC
DENY:CONDIEN.LayerD
```

## 6.6 Relation to Modew

Modew is the bounded operational unit.

Cross-L should not replace Modew.

CrossCode should be executed or evaluated through a Modew or a similarly bounded executor.

---

# 7. Design Philosophy

Cross-L follows these principles:

## 7.1 Meaning Before Syntax

A valid meaning should not be destroyed only because a wrapper or syntax is damaged.

## 7.2 Boundary Before Execution

A fragment must declare its boundary before it can be trusted.

## 7.3 Return Contract Before Authority

A fragment must return a structured result before any system treats it as useful.

## 7.4 Role-Scoped Knowledge

A fragment does not need to know the whole W3 ecosystem.

It only needs to know the declared context, input, boundary, and return shape.

## 7.5 Multi-Platform Survival

Cross-L should support the idea that MPCP can exist across multiple platforms.

## 7.6 No Truth Mutation by Default

CrossCode should not mutate truth directly.

Mutation, if ever allowed, must be declared and governed by higher-level review.

## 7.7 Review on Uncertainty

If a fragment cannot determine a safe result, it should return `review`, not force `pass`.

---

# 8. Expected Benefits

Cross-L is expected to help with:

- portable rule fragments
- cross-runtime behavior reuse
- lower dependency on heavy conversion
- clearer boundary declarations
- safer embedded logic
- role-scoped AI execution
- traceable multi-language work
- local ENV adaptation
- modular behavior replacement
- reduced semantic drift between runtimes

---

# 9. Non-Goals

Cross-L is not intended to:

- replace W3Lgu
- replace MPCP
- replace Cross-X
- replace Lua / Python / JSON / JavaScript
- become an unrestricted scripting authority
- mutate source truth by default
- hide execution risk
- become a central document controlling all work

---

# 10. Basic Concept Form

A Cross-L block may contain:

```text
CROSS-L:<name>
POINT:<cross_point_name>
LANG:<language>
BOUNDARY:<boundary_name>
PAPER:<paper_id>
MODEW:<modew_name>
INPUT:<allowed_inputs>
READ:<allowed_context>
DENY:<forbidden_actions>
RETURN:<required_output_fields>
REVIEW:<review_policy>
CODE:[
  ... embedded code fragment ...
]
```

The important part is not the final syntax.

The important part is the contract:

```text
where + language + boundary + input + deny + return + review
```

---

# 11. Example: Lua CrossCode

```text
CROSS-L:ENV_CHECK
POINT:ENV_MODEW_CONDIEN
LANG:lua
BOUNDARY:observe
PAPER:env_adaptive_check
MODEW:CHECK
INPUT:ctx
READ:ENV,CONDIEN.LayerA
DENY:truth_mutation,file_write,network,merge
RETURN:state,reason,trace
REVIEW:on_uncertain
CODE:[
  local M = {}

  function M.evaluate(ctx)
    if ctx.env == "mobile" then
      return { state = "review", reason = "limited_env" }
    end

    if ctx.boundary ~= "observe" then
      return { state = "block", reason = "boundary_violation" }
    end

    return { state = "pass", reason = "ok" }
  end

  return M
]
```

---

# 12. Example: Python CrossCode

```text
CROSS-L:TRACE_CHECK
POINT:RESULT_ROT_LRC2
LANG:python
BOUNDARY:trace-only
INPUT:ctx
READ:result,trace
DENY:truth_mutation,repo_write,network
RETURN:state,reason,missing
REVIEW:on_fail
CODE:[
  def evaluate(ctx):
      missing = []
      for key in ["cause", "action", "result"]:
          if key not in ctx:
              missing.append(key)

      if missing:
          return {"state": "review", "reason": "missing_trace", "missing": missing}

      return {"state": "pass", "reason": "trace_complete", "missing": []}
]
```

---

# 13. Example: JSON Rule CrossCode

```text
CROSS-L:BOUNDARY_RULE
POINT:API_GATEWAY_CROSS
LANG:json
BOUNDARY:gateway-only
INPUT:request
DENY:["truth_mutation", "direct_merge", "runtime_state_write"]
RETURN:["state", "reason"]
CODE:[
  {
    "if": { "mutated": true },
    "then": { "state": "block", "reason": "mutation_not_allowed" },
    "else": { "state": "pass", "reason": "gateway_observe_only" }
  }
]
```

---

# 14. Academic Framing

Cross-L may be studied as a combination of ideas from:

- embedded scripting
- language interoperability
- domain-specific language design
- policy-as-code
- aspect-oriented thinking
- cross-cutting concern management
- workflow boundary control
- runtime governance
- multi-agent coordination
- human-in-the-loop systems

However, Cross-L is not identical to any one of these.

Its distinct focus is:

```text
multi-language fragment governance at cross points
```

The concept is especially relevant when:

- one task spans multiple runtimes
- one work item has multiple cross points
- behavior must move across platforms
- meaning must survive conversion
- fragments must be allowed but bounded
- not every participant should know the whole system

---

# 15. Risk Model

Cross-L introduces risks if not governed carefully:

## 15.1 Authority Drift

A code fragment may start acting like a system authority.

Mitigation:

- declare boundary
- require return contract
- validate output
- keep mutation disabled by default

## 15.2 Runtime Escape

A fragment may access file, network, or system functions beyond its intended scope.

Mitigation:

- sandbox
- deny list
- safe runtime wrapper
- limited exposed functions

## 15.3 Semantic Loss

A fragment may return weak output such as `true` or `false` without reason.

Mitigation:

- require `state`
- require `reason`
- require trace or review policy

## 15.4 False Portability

A fragment may appear portable but depend on hidden platform behavior.

Mitigation:

- declare platform assumptions
- test on target ENV
- keep fragment small

## 15.5 Over-Complex Cross Blocks

Cross-L blocks may become too powerful or too large.

Mitigation:

- one block, one cross purpose
- split large work into multiple cross points
- use Paper for task clarity

---

# 16. Practical Use Concept

A practical Cross-L execution pipeline may be:

```text
Paper defines task
→ Cross-X identifies cross point
→ Cross-L declares fragment boundary
→ Modew loads CrossCode
→ Condien supplies scoped context
→ Runtime evaluates fragment
→ Result returns as MPCP-compatible state
→ DTML / ROT validates
→ LRC2 logs
→ Human review if required
```

---

# 17. Minimal Return Contract

A safe Cross-L fragment should return at least:

```text
state
reason
```

Recommended fields:

```text
state
reason
trace
mutated
review
```

Example:

```json
{
  "state": "review",
  "reason": "missing_context",
  "trace": ["INPUT", "EVALUATE", "RETURN"],
  "mutated": false,
  "review": true
}
```

---

# 18. Expected Development Path

## Phase 0 — Concept Paper

Document concept, terminology, and examples.

## Phase 1 — Manual Blocks

Write Cross-L blocks manually in Markdown.

## Phase 2 — Parser Draft

Parse metadata fields without executing code.

## Phase 3 — Safe Evaluator

Allow limited evaluation of selected languages in sandbox mode.

## Phase 4 — Cross-X Integration

Attach Cross-L blocks to Cross-X plans.

## Phase 5 — MPCP Runtime Contract

Return outputs through MPCP contract validation.

## Phase 6 — Multi-Platform Test

Test fragments across Termux, Linux, cloud, and other available ENV.

---

# 19. Final Statement

Cross-L is proposed as a language insertion and governance layer for cross-system work.

It exists because future systems may need to move not only values, but also bounded behavior, meaning, and return contracts across platforms.

Cross-L should keep fragments small, bounded, traceable, and reviewable.

It should help W3 and MPCP survive multi-platform complexity without forcing every participant to understand everything.

```text
Do not let code fragments become authority.
Let them become governed participants.
```

---

END

---

# 20. Portable Reference Runtime

The `croll` directory includes a dependency-free Python reference runtime. It is a
planner and lookup layer only: it does not execute embedded code, write files, use
the network, mutate truth, or merge changes.

## Supported environments

- CPython 3.9 or newer
- Linux and cloud runners
- Windows PowerShell or Command Prompt
- macOS Terminal
- Android Termux

The runtime uses only the Python standard library, UTF-8 JSON output, `pathlib`
for context files, and `python -m croll` so callers do not depend on a platform-
specific script path. The CLI explicitly configures UTF-8 output, including on
Windows runners that inherit a legacy console code page, so Cross-L symbols and
Thai context can be emitted without `UnicodeEncodeError`.

## Stable commands

Run these commands from the repository root:

```sh
python -m croll lookup "1,1"
python -m croll plan "PX:[2,1]"
python -m croll list
python -m croll --version
```

Optional Paper context can be passed as inline JSON:

```sh
python -m croll plan "1,1" --context '{"paper_id":"demo"}'
```

For shells where JSON quoting is inconvenient (especially Windows), save a UTF-8
JSON object and prefix its path with `@`:

```sh
python -m croll plan "1,1" --context @paper-context.json
```

## Python API

```python
from croll import dispatch_workset, get_workset_from_px

workset = get_workset_from_px("1,1")
plan = dispatch_workset("PX:[2,1]", paper_context={"paper_id": "demo"})
```

Both APIs preserve the dictionary-based interface from the draft implementation.
Versioned outputs include `contract_version` so future adapters can negotiate
changes without relying on the package version alone. Unknown or malformed PX
values remain safe review results; they never enable execution.

## Compatibility policy

- Additive fields may be introduced within contract version `1.x`.
- Existing field meanings and safety defaults must not change within `1.x`.
- Removing or renaming fields requires a new contract version.
- `execution_allowed`, `mutated`, and every safety permission remain `false` in
  this planner package.
- The package remains dependency-free unless a future runtime is split into an
  explicitly optional component.

## Validation

```sh
python -m compileall croll
python -m unittest discover -s croll -p "test_*.py" -v
python -m croll plan "1,1"
```
