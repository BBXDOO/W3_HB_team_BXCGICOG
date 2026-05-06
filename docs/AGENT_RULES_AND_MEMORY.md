# W3 Agent Rules & Memory Logging

## Overview

The W3 Agent CI framework provides **deterministic, rule-based checks** that run on every push and pull request.  
Rules are defined in `core/governance/rules/w3_ruleset.yml` and executed by `tools/w3_agent_ci.py`.

---

## Rule Structure

Each rule in `w3_ruleset.yml` contains:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g. `W3-001`) |
| `title` | Short human-readable name |
| `severity` | `error` \| `warn` \| `info` |
| `description` | What the rule checks and why it matters |
| `check` | Internal key mapping to a check runner in the orchestrator |
| `override.allowed` | Whether a PR author may request an override |
| `override.requires_reason` | Whether the override must include a non-empty reason |

---

## Negotiable vs Non-Negotiable Rules

### 🔴 Non-Negotiable (override.allowed: false)

These rules can **never** be overridden and will always block CI if they fail:

| Rule ID | Title |
|---------|-------|
| W3-001 | Python compile check |
| W3-002 | Module JSON validation |

Broken Python syntax or invalid module manifests represent fundamental failures that must be fixed before merging.

### 🟡 Negotiable (override.allowed: true)

These rules may be overridden via the PR body with a required explanation:

| Rule ID | Title | Requires Reason |
|---------|-------|-----------------|
| W3-003 | Governance metadata validation | ✅ Yes |
| W3-004 | JSON schema validation | ✅ Yes |

---

## Override Mechanism (PR Body Format)

To override one or more rules, add a `W3-OVERRIDES:` section anywhere in your PR body:

```
W3-OVERRIDES:
- rule_id: W3-003
  reason: Hotfix path; metadata will be updated in follow-up PR #456
- rule_id: W3-004
  reason: Schema update is intentional and reviewed by BBX19
```

### Rules for overrides

1. The `rule_id` must match an existing rule ID exactly (case-insensitive).
2. If the rule sets `override.requires_reason: true`, the `reason` field **must** be non-empty — otherwise the override is rejected and the rule still fails.
3. Overrides are logged to `core/memory/memory_bus` with full context (rule ID + reason + timestamp).
4. Non-negotiable rules (`override.allowed: false`) **cannot** be overridden even if a `W3-OVERRIDES` section is present.

---

## Severity Levels

| Severity | Effect |
|----------|--------|
| `error` | Causes CI to exit with code 1 (blocks PR merge) |
| `warn` | Reported in the artifact but does **not** block CI |
| `info` | Informational only; never blocks CI |

---

## Memory Logging

Every CI run writes records to `core/memory/memory_bus` via `add_memory()`:

| Event | topic | tags | score |
|-------|-------|------|-------|
| Run summary | `ci_run_summary` | `["ci", "summary", "w3_agent_ci"]` | 5 |
| Override applied | `override:<rule_id>` | `["ci", "override", "<rule_id>"]` | 4 |

The memory store is located at `core/memory/memory_store.json`.  
You can query it with:

```python
from core.memory.memory_bus import search_memory
search_memory("ci_run_summary")
search_memory("override:W3-003")
```

---

## Adding New Rules

1. Add a new entry to `core/governance/rules/w3_ruleset.yml`.
2. Register a corresponding runner function in `tools/w3_agent_ci.py` under `CHECK_RUNNERS`.
3. Update this document.
