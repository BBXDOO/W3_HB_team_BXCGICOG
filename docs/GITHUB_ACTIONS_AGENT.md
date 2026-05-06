# GitHub Actions Agent Workflow

## Overview

The file `.github/workflows/w3_agent_ci.yml` defines the **W3 Agent CI** workflow. It runs automatically on every `push` and `pull_request` event, executes the rule-based agent checks, and uploads the resulting reports as build artifacts.

---

## Workflow File

```yaml
# .github/workflows/w3_agent_ci.yml
name: W3 Agent CI

on:
  push:
  pull_request:

jobs:
  w3-agent-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
      - name: Run W3 Agent CI checks
        run: python tools/w3_agent_ci.py
      - name: Upload CI reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: w3-agent-reports
          path: |
            w3_agent_report.md
            w3_agent_report.json
```

---

## Trigger Events

| Trigger | Behaviour |
|---------|-----------|
| `push` (any branch) | Runs checks immediately on the pushed commit. |
| `pull_request` | Runs checks against the PR head commit; result is shown as a status check. |

---

## Job Steps

1. **Checkout** — full repository checkout via `actions/checkout@v4`.
2. **Python setup** — installs the latest Python 3.x release.
3. **Install dependencies** — installs `requirements.txt` (production) and `requirements-dev.txt` (CI tooling, e.g. PyYAML).
4. **Run checks** — executes `tools/w3_agent_ci.py`, which:
   - Loads `core/governance/rules/w3_ruleset.yml`.
   - Runs each registered check (validate_modules, validate_metadata, compileall, json_schema).
   - Writes `w3_agent_report.md` and `w3_agent_report.json`.
   - Exits `1` if any `error`-severity rule failed; exits `0` otherwise.
5. **Upload artifacts** — always runs (even on failure) to make reports available for download from the Actions UI.

---

## Exit Codes and CI Status

| Exit code | Meaning |
|-----------|---------|
| `0` | All non-negotiable checks passed. Negotiable warnings may still be present in the report. |
| `1` | One or more non-negotiable (`error`) checks failed. The job is marked **failed** and the PR is blocked (if branch protection is enabled). |

---

## Artifacts

After each run two files are uploaded under the artifact name **`w3-agent-reports`**:

| File | Description |
|------|-------------|
| `w3_agent_report.md` | Human-friendly Markdown report with a summary table and full check output. |
| `w3_agent_report.json` | Machine-readable JSON with all check results, suitable for downstream tooling. |

Download artifacts from the **Actions** tab → select the workflow run → **Artifacts** section.

---

## Adding or Modifying Rules

1. Edit `core/governance/rules/w3_ruleset.yml`.
2. To add a new check, also register a handler in the `CHECK_FN` dict in `tools/w3_agent_ci.py`.
3. Use `severity: error` for non-negotiable rules and `severity: warn` for negotiable ones.
4. Open a PR — the workflow will validate your changes automatically.

---

## Troubleshooting

| Symptom | Resolution |
|---------|------------|
| `ModuleNotFoundError: yaml` | Ensure `requirements-dev.txt` contains `PyYAML>=6` and is installed. |
| `ModuleNotFoundError: jsonschema` | Ensure `requirements.txt` contains `jsonschema>=4.10.3`. |
| Reports not uploaded | Check the "Upload CI reports" step; `if: always()` ensures it runs even on failure. |
| Memory store not updated | Verify `core/memory/memory_store.json` is writable in the runner environment. |
