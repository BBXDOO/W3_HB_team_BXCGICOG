"""Event-bound Paper distribution with host authority and durable return binding.

Paper carries only its local command. ROT owns normalization; the host selects
routes, authenticates permits and verifies actual results. Distribution is local
and sequential in this version; it is not a remote-agent or parallel scheduler.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Callable, Mapping

from ..env.boundary import CrossLEnvironmentBoundary
from ..kernel.contract import MPCPContract
from ..kernel.rot import MPCPRot
from .executor import PILLAR_REGISTRY, run_packet


def fingerprint(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    allow_nan=False).encode()).hexdigest()


def prepare_paper_pack(pack: Mapping, *, resolve_reference: Callable | None = None) -> dict:
    """Resolve reference strings explicitly; never guess commands from their text."""
    data = deepcopy(dict(pack))
    for key in ("PAPER_PACK_ID", "CHAIN_ID", "EVENT_ID", "RESPONSIBLE_MODULE", "RETURN_TO"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"PAPER:{key}_REQUIRED")
    if data["RETURN_TO"] != data["RESPONSIBLE_MODULE"]:
        raise ValueError("PAPER:RETURN_TO_MUST_MATCH_RESPONSIBLE_MODULE")
    source = data.get("PAPERS")
    if not isinstance(source, list) or not source:
        raise ValueError("PAPER:PAPERS_REQUIRED")
    commands, references = [], {}
    for item in source:
        if isinstance(item, str):
            if resolve_reference is None:
                raise ValueError("PAPER:REFERENCE_RESOLVER_REQUIRED")
            command = deepcopy(resolve_reference(item))
        else:
            command = deepcopy(item)
        if not isinstance(command, dict):
            raise ValueError("PAPER:RESOLVER_MUST_RETURN_COMMAND")
        pid = command.get("PAPER_ID")
        if not isinstance(pid, str) or not pid.strip() or pid in references:
            raise ValueError("PAPER:UNIQUE_PAPER_ID_REQUIRED")
        for key in ("EVENT_ID", "PAPER_PACK_ID"):
            if key in command and command[key] != data[key]:
                raise ValueError(f"PAPER:CONFLICTING_{key}")
        command["EVENT_ID"] = data["EVENT_ID"]
        references[pid] = item if isinstance(item, str) else data.get("SOURCE_REFERENCES", {}).get(pid)
        commands.append(command)
    data["PAPERS"] = commands
    data["PAPERS"] = MPCPRot.normalize_paper_pack(data)
    data["SOURCE_REFERENCES"] = references
    return data


@dataclass(frozen=True)
class PaperPermit:
    """Trusted-host grant bound to exact prepared work, not request credentials.

    Construct only after authenticating the operator outside this API. Fields
    claiming an approver inside a Paper never create a permit.
    """
    pack_hash: str
    paper_id: str
    modew: str
    evidence: str
    active: bool = True

    def permits(self, pack_hash, paper_id, modew):
        return (self.active is True and self.pack_hash == pack_hash and self.paper_id == paper_id
                and self.modew == modew and isinstance(self.evidence, str) and bool(self.evidence.strip()))


class PaperPackRuntime:
    """Distribute independent Papers; retain actual results and never replay uncertainty."""

    def __init__(self, directory: Path):
        self.directory = Path(directory).resolve()

    @contextmanager
    def _locked(self, identity):
        # Kernel locks survive neither process exit nor PID reuse. No stale-lock
        # deletion or unsafe retry is needed after a worker dies.
        import fcntl
        self.directory.mkdir(parents=True, exist_ok=True)
        with (self.directory / (identity + ".lock")).open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def _path(self, pack):
        identity = fingerprint([pack["CHAIN_ID"], pack["EVENT_ID"], pack["PAPER_PACK_ID"]])
        return self.directory / (identity + ".json"), identity

    def _save(self, path, snapshot):
        fd, name = tempfile.mkstemp(dir=self.directory, prefix=".paper-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(snapshot, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, path)
            directory_fd = os.open(self.directory, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if os.path.exists(name):
                os.unlink(name)

    @staticmethod
    def _report(snapshot):
        entries = snapshot["papers"]
        statuses = [entry["status"] for entry in entries.values()]
        state = "SUCCESS" if all(s == "COMPLETED" for s in statuses) else (
            "STOP" if "STOPPED" in statuses else "WAIT")
        return {"schema": "mpcp.paper_pack.result.1", "state": state,
                "chain_id": snapshot["pack"]["CHAIN_ID"], "event_id": snapshot["pack"]["EVENT_ID"],
                "paper_pack_id": snapshot["pack"]["PAPER_PACK_ID"],
                "return_to": snapshot["pack"]["RETURN_TO"], "pack_hash": snapshot["pack_hash"],
                "papers": deepcopy(entries)}

    @staticmethod
    def _check_result(paper, result, verify):
        MPCPContract.validate_result_envelope(result, strict=True)
        if result["cause"] != paper["TASK"]:
            raise ValueError("PAPER:RESULT_CAUSE_MISMATCH")
        verdict = verify(deepcopy(paper), deepcopy(result))
        if not isinstance(verdict, dict) or type(verdict.get("passed")) is not bool:
            raise ValueError("PAPER:VERIFIER_MUST_RETURN_BOOLEAN_PASSED")
        if result["state"] in {"STOP", "fail", "block"}:
            status = "STOPPED"
        elif result["state"] not in {"SUCCESS", "done"} or verdict["passed"] is not True:
            status = "WAITING"
        elif result.get("review"):
            status = "WAITING_REVIEW"
        else:
            status = "COMPLETED"
        return status, verdict

    def run(self, pack: Mapping, *, routes: Mapping[str, str], permits=(),
            verify: Callable, condien=None) -> dict:
        """Prepared pack in; event-bound returns out. Never select routes from TARGET.

        No payload from sibling Papers or full ROT rulebook is injected. The
        whole route/context set is checked before any executor is called.
        """
        if not callable(verify):
            raise ValueError("PAPER:HOST_VERIFIER_REQUIRED")
        prepared = prepare_paper_pack(pack)
        contexts = {}
        for paper in prepared["PAPERS"]:
            pid = paper["PAPER_ID"]
            name = routes.get(pid)
            if not isinstance(name, str) or name not in PILLAR_REGISTRY:
                raise ValueError(f"PAPER:REGISTERED_HOST_ROUTE_REQUIRED:{pid}")
            if paper.get("MODEW") and paper["MODEW"] != name:
                raise ValueError(f"PAPER:DECLARED_MODEW_ROUTE_CONFLICT:{pid}")
            payload = deepcopy(paper.get("CONTENT"))
            reads = CrossLEnvironmentBoundary._strings(paper.get("READ"), "READ")
            denies = CrossLEnvironmentBoundary._strings(paper.get("DENY"), "DENY")
            context = {**deepcopy(paper), "CHAIN_ID": prepared["CHAIN_ID"], "MODEW": name,
                       "PAYLOAD": payload}
            if reads:
                if condien is None:
                    raise ValueError("PAPER:DECLARED_CONDIEN_CONTEXT_REQUIRED")
                context["CONDIEN"] = CrossLEnvironmentBoundary.scope_condien(condien, reads, denies)
            contexts[pid] = context
        # The grant binds the host route and scoped context as well as commands.
        pack_hash = fingerprint({"pack": prepared, "contexts": contexts})
        path, identity = self._path(prepared)
        with self._locked(identity):
            if path.exists():
                snapshot = json.loads(path.read_text(encoding="utf-8"))
                if snapshot["pack_hash"] != pack_hash:
                    raise ValueError("PAPER:SAVED_WORK_CHANGED_USE_NEW_EVENT_OR_PACK")
            else:
                snapshot = {"pack": prepared, "pack_hash": pack_hash,
                            "papers": {p["PAPER_ID"]: {"status": "PENDING", "modew": routes[p["PAPER_ID"]],
                                                       "history": []} for p in prepared["PAPERS"]}}
                self._save(path, snapshot)
            for paper in prepared["PAPERS"]:
                pid = paper["PAPER_ID"]
                entry = snapshot["papers"][pid]
                if entry["status"] == "IN_PROGRESS":
                    entry["status"] = "NEEDS_RECONCILIATION"
                    self._save(path, snapshot)
                if entry["status"] == "COMPLETED":
                    try:
                        status, verdict = self._check_result(paper, entry["result"], verify)
                        if status == "WAITING_REVIEW" and entry.get("review_accepted_hash") == fingerprint(entry["result"]):
                            status = "COMPLETED"
                        entry.update(status=status, verification=verdict)
                    except Exception as exc:
                        entry.update(status="NEEDS_RECONCILIATION", error=str(exc))
                    self._save(path, snapshot)
                if entry["status"] != "PENDING":
                    continue
                permit = next((p for p in permits if isinstance(p, PaperPermit)
                               and p.permits(pack_hash, pid, entry["modew"])), None)
                if permit is None:
                    continue
                entry.update(status="IN_PROGRESS", authority_evidence=permit.evidence)
                self._save(path, snapshot)  # save before effects; a restart never blindly retries
                try:
                    result = run_packet(contexts[pid])
                    entry["result"] = deepcopy(result)
                    status, verdict = self._check_result(paper, result, verify)
                    entry.update(status=status, verification=verdict)
                    entry["history"].append({"event": "RETURN", "state": result["state"], "status": status})
                    self._save(path, snapshot)
                except Exception as exc:
                    entry.update(status="NEEDS_RECONCILIATION", error=str(exc))
                    self._save(path, snapshot)
                    # Independent Papers may continue; this result is never marked complete.
            return self._report(snapshot)

    def reconcile(self, pack: Mapping, paper_id: str, *, observed_result: dict,
                  evidence: str, verify: Callable, review_accepted=False) -> dict:
        """Trusted host records observed effects without repeating execution.

        Review may accept the exact saved successful result. It cannot turn a
        STOP/WAIT or failed verification into completed work.
        """
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("PAPER:RECONCILIATION_EVIDENCE_REQUIRED")
        prepared = prepare_paper_pack(pack)
        path, identity = self._path(prepared)
        with self._locked(identity):
            snapshot = json.loads(path.read_text(encoding="utf-8"))
            if snapshot["pack"] != prepared:
                raise ValueError("PAPER:SAVED_WORK_CHANGED")
            entry = snapshot["papers"][paper_id]
            if entry["status"] not in {"IN_PROGRESS", "NEEDS_RECONCILIATION", "WAITING", "WAITING_REVIEW", "STOPPED"}:
                raise ValueError("PAPER:UNSETTLED_RESULT_REQUIRED")
            paper = next(p for p in prepared["PAPERS"] if p["PAPER_ID"] == paper_id)
            status, verdict = self._check_result(paper, observed_result, verify)
            if status == "WAITING_REVIEW" and review_accepted is True:
                if observed_result != entry.get("result"):
                    raise ValueError("PAPER:REVIEW_REQUIRES_EXACT_SAVED_RESULT")
                status = "COMPLETED"
                entry["review_accepted_hash"] = fingerprint(observed_result)
            entry["history"].append({"event": "RECONCILE", "evidence": evidence,
                                     "previous_result": entry.get("result"), "previous_status": entry["status"]})
            entry.update(status=status, result=deepcopy(observed_result), verification=verdict)
            self._save(path, snapshot)
            return self._report(snapshot)
