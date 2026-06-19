"""IGET Approval Gate for W3Agent.

Purpose:
- Read BBX19 approval comments such as `/iget approve`
- Build an approval trace response
- Prepare the next execution intent from the original issue brief
- Keep default action mode report-only unless a later approved worker handles the brief

This file does not mutate repo content.
It does not execute module work by itself.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


APPROVAL_COMMAND_RE = re.compile(
    r"^\s*/iget\s+(approve|reject|hold|ask|run)\b(?P<args>.*)$",
    re.IGNORECASE | re.MULTILINE,
)

MODULE_TAG_RE = re.compile(r"@module:([A-Za-z0-9_.:-]+)")


@dataclass(frozen=True)
class ApprovalCommand:
    action: str
    args: str = ""
    raw: str = ""


def dedupe(items: Iterable[str]) -> list[str]:
    ordered: list[str] = []
    for item in items:
        clean = str(item).strip()
        if clean and clean not in ordered:
            ordered.append(clean)
    return ordered


def parse_approval_command(comment_body: str | None) -> ApprovalCommand | None:
    """Parse `/iget approve`, `/iget reject`, `/iget hold`, `/iget ask`, or `/iget run`."""
    if not comment_body:
        return None

    match = APPROVAL_COMMAND_RE.search(comment_body)
    if not match:
        return None

    return ApprovalCommand(
        action=match.group(1).lower(),
        args=(match.group("args") or "").strip(),
        raw=match.group(0).strip(),
    )


def is_approval_comment(comment_body: str | None) -> bool:
    return parse_approval_command(comment_body) is not None


def extract_module_tags(*parts: object) -> list[str]:
    found: list[str] = []

    for part in parts:
        if isinstance(part, (list, tuple, set)):
            found.extend(extract_module_tags(*part))
            continue

        text = str(part or "")
        found.extend(match.group(1).strip() for match in MODULE_TAG_RE.finditer(text))

    return dedupe(found)


def extract_section(issue_body: str, heading: str) -> str:
    """Extract a markdown section by heading name. Returns empty string if missing."""
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(issue_body or "")
    if not match:
        return ""
    return match.group("body").strip()


def extract_issue_field(issue_body: str, field_name: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(field_name)}:\s*(?P<value>.+)$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(issue_body or "")
    if not match:
        return ""
    return match.group("value").strip()


def build_execution_plan(issue_title: str, issue_body: str, modules: list[str]) -> list[str]:
    brief = extract_section(issue_body, "Brief")
    target = extract_issue_field(issue_body, "Target") or "unknown"
    risk = extract_issue_field(issue_body, "Risk") or "unknown"

    plan = [
        f"Read original issue brief: {brief[:120] if brief else 'missing brief'}",
        f"Confirm target: {target}",
        f"Confirm risk level: {risk}",
        "Collect evidence before any code/doc change",
        "Return findings to IGET / BBX19 before mutation",
    ]

    for module in modules:
        plan.append(f"Request `{module}` response according to its module response contract")

    if "LRC2" in issue_title or "LRC2" in brief:
        plan.append("Special note: LRC2 is mentioned; include log/record/continuity readiness in review")

    return plan


def render_plan_items(items: list[str]) -> str:
    return "\n".join(f"- [ ] {item}" for item in items)


def build_approval_response(
    *,
    issue_number: int | str,
    issue_title: str,
    issue_body: str,
    comment_body: str,
    actor: str = "BBX19",
) -> str:
    """Build responder comment for an approval command."""
    command = parse_approval_command(comment_body)

    if command is None:
        raise ValueError("APPROVAL_GATE_FAIL: APPROVAL_COMMAND_REQUIRED")

    modules = extract_module_tags(issue_body)
    created_at = datetime.now(timezone.utc).isoformat()

    if command.action == "approve":
        status = "approved_by_bbx19"
        next_mode = "prepare_execution_plan"
    elif command.action == "run":
        status = "approved_run_requested"
        next_mode = "prepare_execution_plan"
    elif command.action == "reject":
        status = "rejected_by_bbx19"
        next_mode = "stop"
    elif command.action == "hold":
        status = "held_by_bbx19"
        next_mode = "wait"
    else:
        status = "question_requested_by_bbx19"
        next_mode = "ask_target_module"

    plan = build_execution_plan(issue_title, issue_body, modules)

    return f"""## ✅ IGET Approval Gate

Issue: #{issue_number}
Title: {issue_title}
Actor: {actor}
Command: `{command.raw}`
Status: `{status}`
Next mode: `{next_mode}`
Created at: {created_at}

### Dispatch modules

{chr(10).join(f"- `@module:{module}`" for module in modules) if modules else "- none detected"}

### Execution plan preview

{render_plan_items(plan)}

### Boundary

- approval comment was detected
- repo mutation is still disabled by default
- module invocation is still disabled until the next approved worker step
- evidence must be collected before action
- result must return to IGET / BBX19

### Return contract

RETURN_TO: `IGET`
APPROVAL_REQUIRED: `true`
MUTATION: `false`
TRACE: `approval_gate`
"""
