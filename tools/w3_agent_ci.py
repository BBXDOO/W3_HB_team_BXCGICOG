#!/usr/bin/env python3
"""
W3 Agent CI Orchestrator
Path: tools/w3_agent_ci.py

Purpose:
- Load w3_ruleset.yml
- Parse PR-body overrides (W3-OVERRIDES section)
- Run each check defined in the ruleset
- Log run summary and overrides to core/memory/memory_bus.py
- Produce w3_agent_report.md and w3_agent_report.json
- Exit 1 if any *error*-severity finding is unresolved

Override format in PR body:
  W3-OVERRIDES:
  - rule_id: W3-003
    reason: Hotfix path; metadata will be updated in follow-up PR #456

Author: W3 / Copilot-Gm
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Optional YAML support – stdlib only fallback
# ---------------------------------------------------------------------------
try:
    import yaml  # type: ignore
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
RULESET_PATH = REPO_ROOT / "core" / "governance" / "rules" / "w3_ruleset.yml"
REPORT_MD = REPO_ROOT / "w3_agent_report.md"
REPORT_JSON = REPO_ROOT / "w3_agent_report.json"

# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(msg: str) -> None:
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# YAML / ruleset loader (stdlib fallback using simple line parser)
# ---------------------------------------------------------------------------

def _parse_ruleset_stdlib(text: str) -> list[dict]:
    """
    Minimal YAML parser for the flat w3_ruleset.yml structure.
    Handles the exact schema used in core/governance/rules/w3_ruleset.yml.
    """
    rules: list[dict] = []
    current: dict | None = None
    in_override = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # Start of a new rule entry
        if re.match(r"^  - id:", line):
            if current is not None:
                rules.append(current)
            current = {}
            in_override = False
            current["id"] = line.split(":", 1)[1].strip().strip('"')
            continue

        if current is None:
            continue

        # override block start
        if re.match(r"^\s+override:", line):
            in_override = True
            current.setdefault("override", {})
            continue

        if in_override:
            m = re.match(r"^\s+(\w+):\s*(.+)$", line)
            if m:
                key, val = m.group(1), m.group(2).strip()
                # Coerce YAML booleans represented as literal strings
                val_lower = val.lower()
                if val_lower == "true":
                    bool_val: str | bool = True
                elif val_lower == "false":
                    bool_val = False
                else:
                    bool_val = val
                current["override"][key] = bool_val
            continue

        # scalar fields
        m = re.match(r"^\s+(\w+):\s*(.+)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            # Remove YAML block-scalar indicator ('>' for folded, '|' for literal)
            # that may appear when pyyaml is unavailable and we parse manually.
            val = val.lstrip(">|").strip()
            current[key] = val

    if current is not None:
        rules.append(current)

    return rules


def load_ruleset() -> list[dict]:
    text = RULESET_PATH.read_text(encoding="utf-8")
    if _HAS_YAML:
        data = yaml.safe_load(text)
        return data.get("rules", [])
    return _parse_ruleset_stdlib(text)


# ---------------------------------------------------------------------------
# PR-body override parser
# ---------------------------------------------------------------------------
_OVERRIDE_SECTION_RE = re.compile(
    r"W3-OVERRIDES\s*:\s*\n(.*?)(?=\n\n|\Z)", re.DOTALL | re.IGNORECASE
)
_RULE_ID_RE = re.compile(r"rule_id\s*:\s*([A-Z0-9\-]+)", re.IGNORECASE)
_REASON_RE = re.compile(r"reason\s*:\s*(.+)", re.IGNORECASE)


def parse_overrides(pr_body: str) -> dict[str, str]:
    """
    Parse the W3-OVERRIDES section from a PR body string.
    Returns a dict mapping rule_id -> reason (empty string if not provided).

    Example PR body section:
        W3-OVERRIDES:
        - rule_id: W3-003
          reason: Hotfix; metadata added in follow-up #456
    """
    overrides: dict[str, str] = {}
    if not pr_body:
        return overrides

    m = _OVERRIDE_SECTION_RE.search(pr_body)
    if not m:
        return overrides

    section = m.group(1)
    # split on list item markers
    items = re.split(r"(?m)^\s*-\s+rule_id", section)
    for item in items:
        if not item.strip():
            continue
        # reconstruct the rule_id line
        block = "rule_id" + item
        id_match = _RULE_ID_RE.search(block)
        reason_match = _REASON_RE.search(block)
        if id_match:
            rule_id = id_match.group(1).strip().upper()
            reason = reason_match.group(1).strip() if reason_match else ""
            overrides[rule_id] = reason

    return overrides


# ---------------------------------------------------------------------------
# Individual check runners
# ---------------------------------------------------------------------------

def _run_script(script_name: str) -> tuple[bool, str]:
    """Run a tools/*.py script and return (passed, output)."""
    script = TOOLS_DIR / script_name
    if not script.exists():
        return False, f"Script not found: {script}"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def _run_python_compile() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "."],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


CHECK_RUNNERS: dict[str, Any] = {
    "python_compile": _run_python_compile,
    "validate_modules": lambda: _run_script("validate_modules.py"),
    "validate_metadata": lambda: _run_script("validate_metadata.py"),
    "validate_json_schemas": lambda: _run_script("validate_json_schemas.py"),
}


# ---------------------------------------------------------------------------
# Memory bus logging
# ---------------------------------------------------------------------------

def _log_to_memory(topic: str, content: str, tags: list[str], score: int = 3) -> None:
    """Log a summary record to core/memory/memory_bus via add_memory."""
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from core.memory.memory_bus import add_memory  # type: ignore
        add_memory(
            source="w3_agent_ci",
            topic=topic,
            content=content,
            tags=tags,
            score=score,
        )
    except Exception as exc:  # pragma: no cover
        _log(f"[WARN] Could not write to memory_bus: {exc}")


# ---------------------------------------------------------------------------
# Report generators
# ---------------------------------------------------------------------------

def _build_report(
    findings: list[dict],
    overrides_applied: list[dict],
    run_ts: str,
    has_errors: bool,
) -> tuple[str, dict]:
    """Return (markdown_text, json_dict)."""

    # ── JSON ──────────────────────────────────────────────────────────────
    report_json: dict = {
        "schema": "w3_agent_report/1.0",
        "generated_at": run_ts,
        "result": "FAIL" if has_errors else "PASS",
        "findings": findings,
        "overrides_applied": overrides_applied,
    }

    # ── Markdown ──────────────────────────────────────────────────────────
    lines: list[str] = []
    lines.append("# W3 Agent CI Report")
    lines.append(f"\n**Generated:** {run_ts}")
    lines.append(f"**Result:** {'❌ FAIL' if has_errors else '✅ PASS'}\n")
    lines.append("---\n")

    lines.append("## Findings\n")
    lines.append("| Rule ID | Title | Severity | Status | Note |")
    lines.append("|---------|-------|----------|--------|------|")

    for f in findings:
        sev = f["severity"].upper()
        sev_icon = {"ERROR": "🔴", "WARN": "🟡", "INFO": "🔵"}.get(sev, "⚪")
        status_icon = "✅" if f["passed"] else ("🚫" if f.get("overridden") else "❌")
        note = f.get("override_reason", "") if f.get("overridden") else ""
        lines.append(
            f"| {f['rule_id']} | {f['title']} | {sev_icon} {sev} | {status_icon} | {note} |"
        )

    if overrides_applied:
        lines.append("\n## Overrides Applied\n")
        for ov in overrides_applied:
            lines.append(f"- **{ov['rule_id']}** – {ov['reason']}")

    lines.append("\n---\n")
    lines.append("## Check Outputs\n")
    for f in findings:
        lines.append(f"<details><summary>{f['rule_id']} – {f['title']}</summary>\n")
        lines.append("```")
        lines.append(f.get("output", "").strip() or "(no output)")
        lines.append("```")
        lines.append("</details>\n")

    return "\n".join(lines), report_json


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def main() -> int:
    run_ts = _now()
    _log(f"\n{'='*60}")
    _log(f"  W3 Agent CI  —  {run_ts}")
    _log(f"{'='*60}\n")

    # 1. Load ruleset -------------------------------------------------------
    rules = load_ruleset()
    _log(f"Loaded {len(rules)} rule(s) from {RULESET_PATH.relative_to(REPO_ROOT)}\n")

    # 2. Parse PR-body overrides (injected via env var by the workflow) ------
    pr_body = os.environ.get("W3_PR_BODY", "")
    overrides = parse_overrides(pr_body)
    if overrides:
        _log(f"Detected {len(overrides)} override(s) in PR body: {list(overrides.keys())}\n")

    # 3. Run checks ----------------------------------------------------------
    findings: list[dict] = []
    overrides_applied: list[dict] = []
    has_errors = False

    for rule in rules:
        rule_id: str = rule.get("id", "UNKNOWN")
        title: str = rule.get("title", "")
        severity: str = rule.get("severity", "info").lower()
        check_key: str = rule.get("check", "")
        override_cfg: dict = rule.get("override", {})

        _log(f"▶  [{rule_id}] {title}")

        runner = CHECK_RUNNERS.get(check_key)
        if runner is None:
            _log(f"   ⚠  No runner for check '{check_key}' — skipping\n")
            findings.append({
                "rule_id": rule_id,
                "title": title,
                "severity": severity,
                "passed": True,
                "skipped": True,
                "output": f"No runner registered for check key: {check_key}",
            })
            continue

        passed, output = runner()

        finding: dict = {
            "rule_id": rule_id,
            "title": title,
            "severity": severity,
            "passed": passed,
            "output": output,
        }

        if passed:
            _log(f"   ✅ PASSED\n")
        else:
            # Check for override
            if rule_id in overrides and override_cfg.get("allowed", False):
                reason = overrides[rule_id]
                requires_reason = override_cfg.get("requires_reason", False)
                if requires_reason and not reason:
                    _log(f"   ❌ OVERRIDE REJECTED — rule {rule_id} requires a non-empty reason\n")
                    finding["overridden"] = False
                    if severity == "error":
                        has_errors = True
                else:
                    _log(f"   🚫 OVERRIDDEN — reason: {reason or '(none provided)'}\n")
                    finding["overridden"] = True
                    finding["override_reason"] = reason
                    overrides_applied.append({"rule_id": rule_id, "reason": reason})
                    # Log override to memory bus
                    _log_to_memory(
                        topic=f"override:{rule_id}",
                        content=f"Rule {rule_id} overridden. Reason: {reason}",
                        tags=["ci", "override", rule_id],
                        score=4,
                    )
            else:
                _log(f"   ❌ FAILED\n")
                finding["overridden"] = False
                if severity == "error":
                    has_errors = True

        findings.append(finding)

    # 4. Write reports -------------------------------------------------------
    md_text, json_data = _build_report(findings, overrides_applied, run_ts, has_errors)

    REPORT_MD.write_text(md_text, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    _log(f"Reports written:\n  {REPORT_MD.name}\n  {REPORT_JSON.name}\n")

    # 5. Log run summary to memory bus ---------------------------------------
    error_ids = [f["rule_id"] for f in findings if not f.get("passed") and not f.get("overridden") and f["severity"] == "error"]
    summary = (
        f"CI run {run_ts}: result={'FAIL' if has_errors else 'PASS'}, "
        f"findings={len(findings)}, overrides={len(overrides_applied)}, "
        f"errors={error_ids if error_ids else 'none'}"
    )
    _log_to_memory(
        topic="ci_run_summary",
        content=summary,
        tags=["ci", "summary", "w3_agent_ci"],
        score=5,
    )

    # 6. Final status --------------------------------------------------------
    _log("=" * 60)
    if has_errors:
        _log("❌  CI FAILED — one or more error-severity rules are unresolved.")
        _log("=" * 60)
        return 1

    _log("✅  CI PASSED — all error-severity rules resolved.")
    _log("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
