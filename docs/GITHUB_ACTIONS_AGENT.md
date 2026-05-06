# W3 Agent CI — GitHub Actions Workflow

## Overview

The file `.github/workflows/w3_agent_ci.yml` defines the **W3 Agent CI** workflow.  
It runs automatically on every `push` and `pull_request` to any branch, providing deterministic rule-based validation of the repository.

---

## Workflow Steps

| Step | What it does |
|------|-------------|
| Checkout code | Clones the repository at the current commit |
| Set up Python 3.11 | Installs CPython |
| Install dependencies | `pip install -r requirements.txt` (includes `jsonschema`) |
| Run W3 Agent CI checks | Executes `python tools/w3_agent_ci.py` |
| Upload report artifacts | Always uploads `w3_agent_report.md` and `w3_agent_report.json` (retained 30 days) |

---

## Triggering the Workflow

The workflow fires on:

- **Push** — any branch  
- **Pull request** — any target branch  

On pull requests the PR body is passed to the orchestrator via the `W3_PR_BODY` environment variable so that the override parser can read `W3-OVERRIDES:` sections.

---

## Artifacts

After each run two report files are uploaded as the `w3-agent-reports` artifact:

| File | Format | Contents |
|------|--------|---------|
| `w3_agent_report.md` | Markdown | Human-readable summary table + collapsible check outputs |
| `w3_agent_report.json` | JSON | Machine-readable findings, overrides, timestamps |

Artifacts are retained for **30 days**.

### Downloading artifacts

Via GitHub UI: *Actions → workflow run → Artifacts → w3-agent-reports*

Via `gh` CLI:
```bash
gh run download <run-id> --name w3-agent-reports
```

---

## Interpreting Results

### CI passes (exit 0)

All `error`-severity rules either passed or were validly overridden.  
`warn` and `info` findings may still appear in the report.

### CI fails (exit 1)

One or more `error`-severity rules failed without a valid override.  
Check the workflow logs and the downloaded `w3_agent_report.md` for details.

### Report table icons

| Icon | Meaning |
|------|---------|
| ✅ | Rule passed |
| ❌ | Rule failed (blocks CI if severity = error) |
| 🚫 | Rule failed but overridden via PR body |
| 🔴 | Error severity |
| 🟡 | Warn severity |
| 🔵 | Info severity |

---

## Overriding Rules in a PR

Add a `W3-OVERRIDES:` section to the PR description:

```
W3-OVERRIDES:
- rule_id: W3-003
  reason: Hotfix — metadata added in follow-up PR #456
```

See [AGENT_RULES_AND_MEMORY.md](./AGENT_RULES_AND_MEMORY.md) for the full override specification.

---

## Local Execution

Run the same checks locally before pushing:

```bash
# from repo root
pip install -r requirements.txt
python tools/w3_agent_ci.py
```

Reports are written to `w3_agent_report.md` and `w3_agent_report.json` in the repo root.  
Those files are listed in `.gitignore` and will not be committed.

---

## Memory Logging

Every CI run appends a summary record to `core/memory/memory_store.json` via `core/memory/memory_bus.add_memory()`.  
This provides a persistent, searchable audit trail of all CI runs and any overrides that were applied.
