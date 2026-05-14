#!/usr/bin/env python3
"""
W3 Agent CI Orchestrator
Path: tools/w3_agent_ci.py

Rule-based CI agent — no external LLM APIs required.

Loads rules from core/governance/rules/w3_ruleset.yml, runs each check,
produces w3_agent_report.md and w3_agent_report.json, logs overrides to
core/memory/memory_store.json via core/memory/memory_bus.py, and returns
exit code 1 on any error-severity finding.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # PyYAML (optional at runtime)
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
RULESET_PATH = REPO_ROOT / "core" / "governance" / "rules" / "w3_ruleset.yml"
REPORT_MD = REPO_ROOT / "w3_agent_report.md"
REPORT_JSON = REPO_ROOT / "w3_agent_report.json"
MEMORY_BUS = REPO_ROOT / "core" / "memory" / "memory_bus.py"

# Add repo root to sys.path so we can import core.memory.memory_bus
sys.path.insert(0, str(REPO_ROOT))


# ── Helpers ───────────────────────────────────────────────────────────────────



def _parse_ruleset_without_yaml(path: Path) -> dict:
    """Minimal parser for this repo's simple ruleset YAML subset."""
    rules = []
    overrides = []
    version = ""
    created = ""
    section = None
    current = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        if line.startswith("version:"):
            version = line.split(":", 1)[1].strip().strip('"')
            continue
        if line.startswith("created:"):
            created = line.split(":", 1)[1].strip().strip('"')
            continue
        if line.startswith("rules:"):
            if current:
                (rules if section == "rules" else overrides).append(current)
                current = None
            section = "rules"
            continue
        if line.startswith("overrides:"):
            if current:
                (rules if section == "rules" else overrides).append(current)
                current = None
            if line.strip().endswith("[]"):
                section = "overrides"
                continue
            section = "overrides"
            continue

        if line.lstrip().startswith("- "):
            if current:
                (rules if section == "rules" else overrides).append(current)
            current = {}
            kv = line.lstrip()[2:]
            if ":" in kv:
                k, v = kv.split(":", 1)
                current[k.strip()] = v.strip().strip('"')
            continue

        if current is not None and ":" in line:
            k, v = line.strip().split(":", 1)
            v = v.strip()
            if v in ("true", "false"):
                current[k] = (v == "true")
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                current[k] = [x.strip().strip("'").strip('"') for x in inner.split(",") if x.strip()]
            elif v.startswith('"') and v.endswith('"'):
                current[k] = v[1:-1]
            elif v:
                current[k] = v

    if current:
        (rules if section == "rules" else overrides).append(current)

    return {"version": version, "created": created, "rules": rules, "overrides": overrides}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_ruleset() -> dict:
    if yaml is not None:
        with open(RULESET_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return _parse_ruleset_without_yaml(RULESET_PATH)


def run_subprocess(cmd: list[str]) -> tuple[int, str]:
    """Run a command, return (returncode, combined output)."""
    result = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode, result.stdout


def log_memory(topic: str, content: str, tags: list[str]) -> None:
    """Append an entry to the memory store via memory_bus."""
    try:
        from core.memory.memory_bus import add_memory  # type: ignore
        add_memory(
            source="w3_agent_ci",
            topic=topic,
            content=content,
            tags=tags,
            score=3,
        )
    except Exception as exc:  # pragma: no cover
        print(f"[memory_bus] Warning: could not log to memory store: {exc}")


# ── Checks ────────────────────────────────────────────────────────────────────

def check_validate_modules() -> tuple[str, str]:
    """
    Run tools/validate_modules.py.
    Returns (status, detail) where status in {'pass','fail'}.
    """
    code, output = run_subprocess([sys.executable, "tools/validate_modules.py"])
    status = "pass" if code == 0 else "fail"
    return status, output.strip()


def check_validate_metadata() -> tuple[str, str]:
    """
    Run tools/validate_metadata.py.
    """
    code, output = run_subprocess([sys.executable, "tools/validate_metadata.py"])
    status = "pass" if code == 0 else "fail"
    return status, output.strip()


def check_compileall() -> tuple[str, str]:
    """
    Compile all Python files to detect syntax errors.
    """
    code, output = run_subprocess(
        [sys.executable, "-m", "compileall", "-q", "."]
    )
    status = "pass" if code == 0 else "fail"
    detail = output.strip() if output.strip() else "(no output — all files OK)"
    return status, detail


def check_json_schema() -> tuple[str, str]:
    """
    Validate every *.schema.json file is itself a valid JSON document and
    is parseable. Also warns if there is no corresponding data file.
    Returns ('pass'|'warn', detail).
    """
    import jsonschema  # noqa: F401 — just ensure library is importable

    schema_files = [
        p for p in REPO_ROOT.rglob("*.schema.json")
        if ".git" not in p.parts
    ]

    if not schema_files:
        return "pass", "No *.schema.json files found."

    lines: list[str] = []
    has_issue = False

    for sf in sorted(schema_files):
        rel = sf.relative_to(REPO_ROOT)
        try:
            with open(sf, "r", encoding="utf-8") as f:
                schema = json.load(f)
            # Basic structural check: must be a JSON object
            if not isinstance(schema, dict):
                lines.append(f"  WARN  {rel}: root is not a JSON object")
                has_issue = True
            else:
                lines.append(f"  OK    {rel}")
        except json.JSONDecodeError as exc:
            lines.append(f"  WARN  {rel}: invalid JSON — {exc}")
            has_issue = True

        # Check for paired data file
        data_file = sf.with_suffix("").with_suffix(".json")  # strip .schema.json → .json
        # More reliable: remove ".schema" suffix
        paired = sf.parent / (sf.stem.replace(".schema", "") + ".json")
        if not paired.exists() and not data_file.exists():
            lines.append(f"  WARN  {rel}: no paired data file found (RULE-005)")
            has_issue = True

    detail = "\n".join(lines)
    status = "warn" if has_issue else "pass"
    return status, detail


# ── Check dispatcher ──────────────────────────────────────────────────────────

CHECK_FN = {
    "validate_modules": check_validate_modules,
    "validate_metadata": check_validate_metadata,
    "compileall": check_compileall,
    "json_schema": check_json_schema,
}


# ── Report builders ───────────────────────────────────────────────────────────

def build_md_report(run_ts: str, results: list[dict], has_errors: bool) -> str:
    lines: list[str] = []
    lines.append("# W3 Agent CI Report")
    lines.append(f"\n**Generated:** {run_ts}")
    lines.append(f"**Result:** {'❌ FAILED' if has_errors else '✅ PASSED'}")
    lines.append("\n---\n")
    lines.append("## Check Results\n")
    lines.append("| Rule ID | Name | Severity | Status | Detail |")
    lines.append("|---------|------|----------|--------|--------|")
    for r in results:
        icon = {"pass": "✅", "fail": "❌", "warn": "⚠️", "skip": "⏭️"}.get(r["status"], "❓")
        detail_short = (r["detail"][:80] + "…") if len(r["detail"]) > 80 else r["detail"]
        detail_short = detail_short.replace("\n", " ")
        lines.append(
            f"| {r['rule_id']} | {r['name']} | `{r['severity']}` "
            f"| {icon} {r['status'].upper()} | {detail_short} |"
        )

    lines.append("\n---\n")
    lines.append("## Full Check Output\n")
    for r in results:
        lines.append(f"### {r['rule_id']} — {r['name']}")
        lines.append(f"- **Severity:** `{r['severity']}`")
        lines.append(f"- **Status:** {r['status'].upper()}")
        lines.append(f"\n```\n{r['detail']}\n```\n")

    lines.append("---")
    lines.append(
        "\n> Report generated by `tools/w3_agent_ci.py`. "
        "Non-negotiable (`error`) violations cause CI failure; "
        "negotiable (`warn`) violations are reported only."
    )
    return "\n".join(lines)


def build_json_report(run_ts: str, results: list[dict], has_errors: bool) -> dict:
    return {
        "generated": run_ts,
        "passed": not has_errors,
        "results": results,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    run_ts = now_iso()
    print(f"[w3_agent_ci] Starting rule-based CI checks — {run_ts}")

    ruleset = load_ruleset()
    rules: list[dict] = ruleset.get("rules", [])
    overrides: list[dict] = ruleset.get("overrides", [])

    # Build override lookup {rule_id: override_record}
    override_map: dict[str, dict] = {o["rule_id"]: o for o in overrides}

    results: list[dict] = []
    has_errors = False

    for rule in rules:
        rule_id: str = rule["id"]
        name: str = rule["name"]
        severity: str = rule["severity"]
        check_key: str = rule.get("check", "")

        print(f"  → [{rule_id}] {name} (severity={severity}) …", end=" ", flush=True)

        fn = CHECK_FN.get(check_key)
        if fn is None:
            status, detail = "skip", f"No check function registered for '{check_key}'"
        else:
            status, detail = fn()

        # Honour overrides for negotiable rules
        if rule_id in override_map and rule.get("overridable", False):
            ov = override_map[rule_id]
            override_note = (
                f"[OVERRIDE by {ov.get('approved_by','?')} on {ov.get('date','?')}: "
                f"{ov.get('reason','no reason given')}]"
            )
            status = "pass"
            detail = override_note + "\n" + detail
            log_memory(
                topic=f"override:{rule_id}",
                content=override_note,
                tags=["override", rule_id, name],
            )

        # Determine if this finding blocks CI
        if status == "fail" and severity == "error":
            has_errors = True

        print(status.upper())

        results.append(
            {
                "rule_id": rule_id,
                "name": name,
                "severity": severity,
                "check": check_key,
                "status": status,
                "detail": detail,
            }
        )

    # Write reports
    md_content = build_md_report(run_ts, results, has_errors)
    json_content = build_json_report(run_ts, results, has_errors)

    REPORT_MD.write_text(md_content, encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps(json_content, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n[w3_agent_ci] Reports written:")
    print(f"  {REPORT_MD}")
    print(f"  {REPORT_JSON}")

    # Log CI run summary to memory
    summary = "CI PASSED" if not has_errors else "CI FAILED (error-severity violations found)"
    log_memory(
        topic="ci_run",
        content=f"{summary} at {run_ts}",
        tags=["ci", "run", "summary"],
    )

    if has_errors:
        print("\n[w3_agent_ci] ❌ Non-negotiable violations detected — exiting with code 1.")
        return 1

    print("\n[w3_agent_ci] ✅ All checks passed (or only negotiable warnings).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
