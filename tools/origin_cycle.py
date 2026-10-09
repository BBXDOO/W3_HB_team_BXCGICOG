#!/usr/bin/env python3
"""Origin work cycles: immediate directed intake, durable follow-up, 7/15 days."""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from functools import wraps
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.runtime.agents import get_agent
from core.runtime.agents.origin_operations import ORIGINS, OriginFiles, atomic_write, digest, repository_lock


def iso(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def load_state(root, module):
    path = root / "repo_events/origin_agents" / module / "state.json"
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise ValueError("Invalid Origin cycle state")
        return state
    return {"interval_days": 7, "next_due": None, "followups": [], "receipts": {}}


def write_state(root, module, state):
    path = root / "repo_events/origin_agents" / module / "state.json"
    atomic_write(path, (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode())


def serialized_cycle(function):
    @wraps(function)
    def locked(root, *args, **kwargs):
        with repository_lock(root / "origin-cycle-state"):
            return function(root, *args, **kwargs)
    return locked


@serialized_cycle
def directed_work(root, module, request, now=None):
    """Repo/ENV intake has already established who delivered this request.

    Source names in a payload describe intent, never filesystem authority.
    A named request bypasses the periodic timer without moving its due date.
    """
    now = now or datetime.now(timezone.utc)
    identity = str(request["request_id"])
    request_hash = digest(json.dumps(request, sort_keys=True, ensure_ascii=False).encode())
    receipt = identity + ":" + request_hash
    # Admission and receipt state are serialized separately from executor locks.
    # Scheduler workflow concurrency ensures one worker per repository run.
    state = load_state(root, module)
    if receipt in state["receipts"]:
        return {"status": "SKIPPED", "module": module, "reason": "request revision already handled"}
    payload = dict(request.get("payload", {}))
    payload["request_type"] = "origin_file_operations" if payload.get("operations") else "origin_review"
    result = get_agent(module).execute(str(request.get("intent") or identity),
                                     {},
                                     {"payload": payload, "request": request,
                                      "authority_context": {"repo_root": str(root)}})
    # A text-only request is acknowledged/reviewed, not falsely completed.
    outstanding = result["status"] != "COMPLETED" or not payload.get("operations") or bool(payload.get("proposals"))
    if outstanding:
        state["followups"].append({"request_id": identity, "receipt": receipt,
                                   "status": "OPEN", "source": request.get("source"),
                                   "intent": request.get("intent"), "result_log": result["log_path"],
                                   "proposals": payload.get("proposals", []),
                                   "reason": result.get("reason") or "Intent needs explicit execution steps",
                                   "created_at": iso(now)})
        state["interval_days"] = 7
        sooner = iso(now + timedelta(days=7))
        state["next_due"] = min(state["next_due"], sooner) if state["next_due"] else sooner
    state["receipts"][receipt] = {"at": iso(now), "status": result["status"], "log": result["log_path"]}
    write_state(root, module, state)
    return result


@serialized_cycle
def resolve_followup(root, module, receipt, evidence_path, expected_sha256):
    """Close only through an explicit ENV call with a readable artifact proof."""
    fs = OriginFiles(module, {"repo_root": str(root)})
    path = fs.path(evidence_path)
    fs.require(path, "read")
    if digest(path.read_bytes()) != expected_sha256:
        raise ValueError("Follow-up resolution evidence differs from supplied hash")
    with repository_lock(root):
        state = load_state(root, module)
        found = False
        for item in state["followups"]:
            if item["receipt"] == receipt:
                item.update(status="RESOLVED", evidence={"path": evidence_path, "sha256": expected_sha256})
                found = True
        if not found:
            raise ValueError("Unknown follow-up receipt")
        write_state(root, module, state)


@serialized_cycle
def periodic_work(root, module, now=None, force=False):
    now = now or datetime.now(timezone.utc)
    state = load_state(root, module)
    if not force and state["next_due"] and datetime.fromisoformat(state["next_due"].replace("Z", "+00:00")) > now:
        return {"module": module, "status": "NOT_DUE", "next_due": state["next_due"]}
    result = get_agent(module).execute("periodic role review", {},
                                     {"request_type": "origin_review", "authority_context": {"repo_root": str(root)}})
    pending = [item for item in state["followups"] if item["status"] == "OPEN"]
    clean = result["status"] == "COMPLETED" and not result.get("findings") and not pending
    state.update(interval_days=15 if clean else 7, last_review=iso(now),
                 next_due=iso(now + timedelta(days=15 if clean else 7)),
                 findings=result.get("findings", []), last_log=result["log_path"])
    report_id = uuid.uuid4().hex
    report_path = root / "repo_events/origin_agents" / module / "reports" / (report_id + ".md")
    report = (f"# {module} — Origin work cycle\n\n"
              f"- Role: {result.get('role', 'unknown')}\n"
              f"- Reviewed at: {iso(now)}\n- Status: {result['status']}\n"
              f"- Scope: {result.get('coverage', 'review failed')}\n"
              f"- Next interval: {state['interval_days']} days\n- Next due: {state['next_due']}\n"
              f"- Execution log: {result['log_path']}\n- Open follow-ups: {len(pending)}\n\n"
              "## Findings and evidence\n\n```json\n" +
              json.dumps({"findings": result.get("findings", []), "pending": pending,
                          "evidence": result.get("evidence", []), "reason": result.get("reason")},
                         ensure_ascii=False, indent=2) + "\n```\n")
    atomic_write(report_path, report.encode())
    state["last_report"] = str(report_path.relative_to(root))
    write_state(root, module, state)
    return {**result, "next_due": state["next_due"], "interval_days": state["interval_days"],
            "report_path": state["last_report"], "pending_count": len(pending)}


def intake_github(event, event_name, authorized_login="BBXDOO"):
    """Resolve a mention as work, not as an authorization grant.

    This adapter only accepts the project owner's actual GitHub actor.
    BBEX intent records enter via repository requests, not a spoofed username.
    """
    if event.get("sender", {}).get("login", "").casefold() != authorized_login.casefold():
        return []
    issue = event.get("issue", {})
    if issue.get("pull_request"):
        return []
    content = event.get("comment", {}) if event_name == "issue_comment" else issue
    text = (content.get("title", "") + "\n" + (content.get("body") or ""))
    structured = re.search(r"```w3-origin\s*\n(.*?)\n```", text, re.S)
    payload = json.loads(structured.group(1)) if structured else {}
    if not isinstance(payload, dict):
        raise ValueError("w3-origin block must be an object")
    targets = [module for module in ORIGINS if re.search(r"(?<![\w-])@?" + re.escape(module) + r"(?![\w-])", text, re.I)]
    return [{"request_id": f"GH-{event_name}-{issue.get('number')}-{content.get('id')}",
             "source": "BBX19", "source_url": content.get("html_url"), "target": module,
             "intent": text, "payload": payload} for module in targets]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--github-event", type=Path)
    parser.add_argument("--event-name", default="issues")
    parser.add_argument("--authorized-login", default="BBXDOO")
    parser.add_argument("--periodic", action="store_true")
    args = parser.parse_args()
    root = args.repo.resolve()
    results = []
    if args.github_event:
        event = json.loads(args.github_event.read_text())
        for request in intake_github(event, args.event_name, args.authorized_login):
            results.append(directed_work(root, request["target"], request))
    for path in sorted((root / "requests").glob("*.origin.json")):
        request = json.loads(path.read_text(encoding="utf-8"))
        if request.get("source") in {"BBX19", "BBEX", "BBEX-Core"} and request.get("target") in ORIGINS:
            results.append(directed_work(root, request["target"], request))
    if args.periodic:
        for module in ORIGINS:
            results.append(periodic_work(root, module))
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(result.get("status") == "FAILED" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
