# Agent Rules and Memory

## Overview

The W3 Agent CI framework enforces a **rule-based governance policy** without relying on any external LLM APIs. Every check is deterministic: it runs a tool, inspects its exit code and output, and maps the result to a rule severity.

---

## Rule Severity: Negotiable vs Non-Negotiable

Rules are defined in `core/governance/rules/w3_ruleset.yml` and carry one of two severity levels:

| Severity | Label | CI Behaviour |
|----------|-------|-------------|
| `error` | **Non-negotiable** | CI job **fails** (`exit 1`) if the check fails. No override possible. |
| `warn` | **Negotiable** | CI job **passes** even if the check fails. Violation appears in the report. |

### Non-Negotiable Rules (severity: error)

These rules protect the integrity of the repository and cannot be bypassed:

| Rule ID | Name | What it checks |
|---------|------|----------------|
| RULE-001 | `module_validity` | All `module.json` files have required fields and valid structure. |
| RULE-002 | `metadata_approval_reason` | Every `approved-by` metadata field is paired with a `reason` field. |
| RULE-003 | `python_syntax` | All Python files compile without syntax errors (`python -m compileall`). |

### Negotiable Rules (severity: warn)

These rules represent best practices. Violations are reported but do not block merges:

| Rule ID | Name | What it checks |
|---------|------|----------------|
| RULE-004 | `json_schema_valid` | All `*.schema.json` files are valid JSON objects. |
| RULE-005 | `no_orphan_schemas` | Each `*.schema.json` has a paired `*.json` data file. |

---

## Flexibility: Overrides and Exceptions

For **negotiable rules** (`severity: warn`, `overridable: true`), a documented override can suppress the warning in the report and record the justification in the memory log.

### How to register an override

1. Open `core/governance/rules/w3_ruleset.yml`.
2. Add an entry to the `overrides` list:

```yaml
overrides:
  - rule_id: RULE-004
    approved_by: "BBX19"
    reason: "Schema is a draft-only template, no data file yet."
    date: "2026-05-06"
```

3. The `w3_agent_ci.py` script will:
   - Replace the check status with `pass` for that rule.
   - Prepend an `[OVERRIDE …]` note to the detail field in the report.
   - Append the override record to `core/memory/memory_store.json` via `memory_bus`.

> **Non-negotiable rules (`overridable: false`) cannot be overridden.** Fixing the underlying issue is the only path to a green CI.

---

## Memory Logging

### What is the memory store?

`core/memory/memory_store.json` is an **append-only JSON log** managed by `core/memory/memory_bus.py`. It records:

- CI run summaries (pass/fail, timestamp).
- Every override / exception applied during a run.
- Any other agent events routed through `memory_bus.add_memory()`.

### Record schema

Each record appended to `records[]` looks like:

```json
{
  "id": 6,
  "timestamp": "2026-05-06T13:24:00Z",
  "source": "w3_agent_ci",
  "topic": "ci_run",
  "content": "CI PASSED at 2026-05-06T13:24:00Z",
  "tags": ["ci", "run", "summary"],
  "score": 3
}
```

### What gets stored

| Event | `topic` | `tags` |
|-------|---------|--------|
| CI run summary | `ci_run` | `ci`, `run`, `summary` |
| Override applied | `override:<RULE_ID>` | `override`, rule ID, rule name |

### Resetting the memory store safely

The store is append-only by design. To reset it without losing the schema:

```bash
python - <<'EOF'
import json
from pathlib import Path

store = Path("core/memory/memory_store.json")
data = json.loads(store.read_text())
data["records"] = []          # clear entries
data["reset_at"] = "<date>"   # optional audit note
store.write_text(json.dumps(data, indent=2))
print("Memory store cleared.")
EOF
```

> Only reset when intentionally archiving or starting a new governance cycle. Keep the reset action in your PR description for traceability.

---

## Files Reference

| File | Purpose |
|------|---------|
| `core/governance/rules/w3_ruleset.yml` | Rule definitions and override registry |
| `core/memory/memory_bus.py` | Append-only memory I/O API |
| `core/memory/memory_store.json` | Persistent memory log |
| `tools/w3_agent_ci.py` | CI orchestration script |
| `w3_agent_report.md` | Human-readable run report (artifact) |
| `w3_agent_report.json` | Machine-readable run report (artifact) |
