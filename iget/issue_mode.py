"""IGET issue dispatch mode for BBX19 brief-to-issue workflow.

This is a v10-preview layer on top of the active v9 governance runtime.
It creates traceable GitHub issues from a short brief while keeping module
invocation and repo mutation behind explicit human approval.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

DEFAULT_REPO = "BBXDOO/W3_HB_team_BXCGICOG"
DEFAULT_SOURCE = "BBX19"
DEFAULT_STATUS = "waiting_triage"
DEFAULT_MODE = "issue_dispatch"

MODULE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("IGET", ("iget", "issue", "pr", "pull request", "governance", "score", "proof", "witness")),
    ("W3-API", ("w3-api", "api", "gateway", "cross", "endpoint", "router", "fastapi")),
    ("DTML", ("dtml", "audit", "report", "overview", "docs", "document", "readme", "summary")),
    ("W3DB", ("w3db", "memory", "state", "trace", "log", "snapshot")),
    ("MPCP", ("mpcp", "protocol", "boundary", "law", "approval", "rule", "deny")),
    ("CROLL", ("croll", "cross-l", "cross l", "px", "table-x", "dispatch")),
    ("EP_SIGNAL", ("ep_signal", "ep-signal", "signal", "preview", "pulse")),
)


@dataclass(frozen=True)
class IssueBrief:
    title: str
    brief: str
    repo: str = DEFAULT_REPO
    source: str = DEFAULT_SOURCE
    intent: str = "feature"
    target: str = "IGET v10.0"
    risk: str = "unknown"
    approval_required: bool = True
    modules: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()


def _split_csv(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part.strip() for part in value.split(",") if part.strip())


def _prompt(name: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{name}{suffix}: ").strip()
    if value:
        return value
    if default is not None:
        return default
    raise SystemExit(f"ERROR: {name} is required")


def _prompt_bool(name: str, default: bool = True) -> bool:
    default_text = "Y/n" if default else "y/N"
    value = input(f"{name} [{default_text}]: ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes", "1", "true", "on"}


def suggest_modules(title: str, brief: str, explicit: Iterable[str] = ()) -> tuple[str, ...]:
    """Return stable pseudo-module tags from explicit values and keyword hints."""
    ordered: list[str] = []

    def add(module: str) -> None:
        clean = module.strip().replace("@module:", "")
        if clean and clean not in ordered:
            ordered.append(clean)

    for module in explicit:
        add(module)

    text = f"{title}\n{brief}".lower()
    for module, keywords in MODULE_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            add(module)

    if not ordered:
        add("IGET")
    return tuple(ordered)


def build_issue_body(brief: IssueBrief) -> str:
    modules = brief.modules or suggest_modules(brief.title, brief.brief)
    module_lines = "\n".join(f"- @module:{module}" for module in modules)
    labels = ", ".join(brief.labels) if brief.labels else "none"
    approval = "true" if brief.approval_required else "false"
    created_at = datetime.now(timezone.utc).isoformat()

    return f"""# IGET Issue Brief

Source: {brief.source}
Intent: {brief.intent}
Target: {brief.target}
Mode: {DEFAULT_MODE}
Status: {DEFAULT_STATUS}
Risk: {brief.risk}
Approval required: {approval}
Labels: {labels}
Created at: {created_at}

## Brief

{brief.brief}

## Suggested modules

{module_lines}

## Boundary

- report only by default
- no repo mutation without BBX19 approval
- no module invocation without BBX19 approval
- no direct merge
- record trace before action

## Requested flow

BBX19 briefed the work from Termux. IGET should classify the issue, notify the
related pseudo-modules, wait for approval, then report back with evidence.
"""


def memory_dir() -> Path:
    return Path(__file__).resolve().parent / "memory"


def record_issue_memory(brief: IssueBrief, body: str, issue_url: str | None) -> Path:
    """Append a local trace record. The jsonl file is intentionally gitignored."""
    path = memory_dir() / "issues.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "type": "issue_dispatch_brief",
        "source": brief.source,
        "intent": brief.intent,
        "target": brief.target,
        "mode": DEFAULT_MODE,
        "status": DEFAULT_STATUS,
        "title": brief.title,
        "brief": brief.brief,
        "repo": brief.repo,
        "risk": brief.risk,
        "approval_required": brief.approval_required,
        "modules": list(brief.modules),
        "labels": list(brief.labels),
        "issue_url": issue_url,
        "body_preview": body,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


def create_github_issue(brief: IssueBrief, body: str) -> str:
    """Create a GitHub issue through the gh CLI and return its output/URL."""
    if shutil.which("gh") is None:
        raise RuntimeError("GitHub CLI 'gh' not found. Install/login first: pkg install gh && gh auth login")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fh:
        fh.write(body)
        body_file = fh.name
    try:
        cmd = ["gh", "issue", "create", "--repo", brief.repo, "--title", brief.title, "--body-file", body_file]
        for label in brief.labels:
            cmd.extend(["--label", label])
        result = subprocess.run(cmd, check=False, text=True, capture_output=True)
    finally:
        try:
            os.unlink(body_file)
        except OSError:
            pass

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"gh issue create failed: {stderr}")
    return result.stdout.strip()


def new_issue(args: argparse.Namespace) -> int:
    interactive = bool(args.interactive) or not (args.title and args.brief)
    title = args.title or _prompt("Title") if interactive else args.title
    brief_text = args.brief or _prompt("Brief") if interactive else args.brief
    target = args.target or (_prompt("Target", "IGET v10.0") if interactive else "IGET v10.0")
    risk = args.risk or (_prompt("Risk", "unknown") if interactive else "unknown")
    approval_required = args.approval_required
    if interactive and args.approval_required is None:
        approval_required = _prompt_bool("Approval required", True)
    if approval_required is None:
        approval_required = True

    modules = suggest_modules(str(title), str(brief_text), _split_csv(args.modules))
    labels = _split_csv(args.labels)
    brief = IssueBrief(
        title=str(title),
        brief=str(brief_text),
        repo=args.repo,
        source=args.source,
        intent=args.intent,
        target=str(target),
        risk=str(risk),
        approval_required=bool(approval_required),
        modules=modules,
        labels=labels,
    )
    body = build_issue_body(brief)

    if args.dry_run:
        print(body)
        if args.record_memory:
            path = record_issue_memory(brief, body, None)
            print(f"\nMemory trace: {path}")
        return 0

    if not args.yes:
        print(body)
        if not sys.stdin.isatty():
            print("\nERROR: refusing to create issue without --yes in non-interactive mode", file=sys.stderr)
            return 2
        if not _prompt_bool("Create GitHub issue now", False):
            print("Cancelled. No issue created.")
            return 0

    try:
        issue_url = create_github_issue(brief, body)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(issue_url)
    if args.record_memory:
        path = record_issue_memory(brief, body, issue_url)
        print(f"Memory trace: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m iget issue", description="IGET issue dispatch mode")
    sub = parser.add_subparsers(dest="command")

    new = sub.add_parser("new", help="Create a W3/IGET issue brief")
    new.add_argument("--title")
    new.add_argument("--brief")
    new.add_argument("--repo", default=os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or DEFAULT_REPO)
    new.add_argument("--source", default=os.environ.get("IGET_SOURCE", DEFAULT_SOURCE))
    new.add_argument("--intent", default="feature")
    new.add_argument("--target")
    new.add_argument("--risk")
    new.add_argument("--modules", help="Comma-separated module names, e.g. IGET,W3-API,DTML")
    new.add_argument("--labels", help="Comma-separated GitHub labels. Omit if labels do not exist.")
    new.add_argument("--approval-required", dest="approval_required", action="store_true", default=None)
    new.add_argument("--no-approval-required", dest="approval_required", action="store_false")
    new.add_argument("--interactive", action="store_true", help="Ask for missing fields step by step")
    new.add_argument("--dry-run", action="store_true", help="Print issue body without creating a GitHub issue")
    new.add_argument("--yes", action="store_true", help="Create without confirmation")
    new.add_argument("--record-memory", action="store_true", help="Append local iget/memory/issues.jsonl trace")
    new.set_defaults(func=new_issue)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
