"""Concrete file capabilities for the five Origin participants.

IDP is loaded from the repository, not from the task. Extra grants arrive only
through the ENV's out-of-band authority_context. Legacy executors remain intact.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import json
import os
import stat
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ORIGINS = ("ChatGPT", "Gemini", "Grok", "DeepSeek", "Copilot-Gm")
ROOT = Path(__file__).resolve().parents[3]
MUTATIONS = {"create", "write", "append", "edit", "delete", "copy", "move"}


def timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temp = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temp, mode)
        os.replace(temp, path)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()


def record_event(root, module, result):
    event_id = uuid.uuid4().hex
    event_path = (root / f"repo_events/origin_agents/{module}/logs/{event_id}.json").resolve()
    if not event_path.is_relative_to(root):
        raise ValueError("Origin event directory escapes repository")
    def without_content(value):
        if isinstance(value, dict):
            return {k: without_content(v) for k, v in value.items() if k not in {"content", "data_base64"}}
        if isinstance(value, list):
            return [without_content(v) for v in value]
        return value
    result["target_mutated"] = bool(result["mutated"])
    result.update(mutated=True, log_mutated=True, log_path=str(event_path.relative_to(root)))
    event = without_content(result)
    event.update(event_id=event_id, created_at=timestamp(), module=module)
    atomic_write(event_path, (json.dumps(event, ensure_ascii=False, indent=2) + "\n").encode())
    return result


@contextmanager
def repository_lock(root):
    """Serialize Origin operations/cycles, keeping locks outside the repo."""
    lock = Path(tempfile.gettempdir()) / ("w3-origin-" + digest(str(root).encode()) + ".lock")
    with lock.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt
            handle.write(b"0")
            handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class OriginFiles:
    def __init__(self, module, authority=None):
        if module not in ORIGINS:
            raise ValueError("Not an Origin participant")
        self.module = module
        self.authority = authority if isinstance(authority, dict) else {}
        self.root = Path(self.authority.get("repo_root", ROOT)).resolve()
        self.profile_path = self.root / "core/identity/profiles" / (module + ".idp.json")
        self.profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        if self.profile.get("module") != module:
            raise ValueError("IDP module mismatch")
        coordinates = self.profile.get("context_root") or self.profile.get("context_coordinates") or {}
        home = (coordinates.get("context_root") or coordinates.get("path") or "").strip("/")
        self.path(home)  # reject a malformed context root
        if Path(home).parts[0] != module:
            raise ValueError("IDP context root does not belong to this participant")
        # Origin house ownership is the module directory, including nested IDP coordinates.
        home = module
        self.grants = [{"path": home, "operations": ["read", "list", *MUTATIONS]},
                       {"path": "modules/" + module, "operations": ["read", "list", *MUTATIONS]}]
        self.grants += self.profile.get("file_capabilities", {}).get("scopes", [])
        self.grants += self.authority.get("origin_scopes", {}).get(module, [])
        self.events = self.path("repo_events/origin_agents/" + module)

    def path(self, value):
        raw = Path(value)
        if raw.is_absolute() or ".." in raw.parts or not raw.parts:
            raise ValueError("Expected a repository-relative path without '..'")
        path = (self.root / raw).resolve()
        if not path.is_relative_to(self.root) or ".git" in raw.parts:
            raise ValueError("Path escapes repository or points to Git internals")
        return path

    def permitted(self, path, operation):
        for grant in self.grants:
            scope = self.path(grant["path"])
            if (path == scope or path.is_relative_to(scope)) and operation in grant.get("operations", []):
                return True
        return False

    def require(self, path, operation):
        if not self.permitted(path, operation):
            raise PermissionError(f"IDP/ENV does not grant {operation}: {path.relative_to(self.root)}")

    def record(self, result):
        """New immutable event per invocation; never put file contents in logs."""
        return record_event(self.root, self.module, result)

    def apply(self, operation):
        action = operation["action"]
        path = self.path(operation["path"])
        self.require(path, action)
        before = path.read_bytes() if path.is_file() else None
        result = {"action": action, "path": str(path.relative_to(self.root)), "mutated": False}
        self.last_outcome = result
        if action == "read":
            if before is None:
                raise FileNotFoundError(str(path))
            result.update(sha256=digest(before), bytes=len(before))
            if operation.get("encoding") == "base64":
                result["data_base64"] = base64.b64encode(before).decode("ascii")
            else:
                result["content"] = before.decode("utf-8")
            return result
        if action == "list":
            if not path.is_dir():
                raise NotADirectoryError(str(path))
            result["entries"] = [str(p.relative_to(self.root)) for p in sorted(path.iterdir())
                                 if p.resolve().is_relative_to(self.root)]
            return result
        if action not in MUTATIONS:
            raise ValueError("Unsupported file action: " + str(action))
        if path.is_dir():
            raise IsADirectoryError("Directory mutation is not a file operation")
        if action == "create" and path.exists():
            raise FileExistsError(str(path))
        if action in {"append", "edit", "delete", "move"} and before is None:
            raise FileNotFoundError(str(path))
        if before is not None and operation.get("expected_sha256") != digest(before):
            raise ValueError("Read current content first and supply expected_sha256 before changing it")
        destination = None
        if action in {"copy", "move"}:
            self.require(path, "read")
            if before is None:
                raise FileNotFoundError(str(path))
            destination = self.path(operation["destination"])
            self.require(destination, "create")
            if destination.exists():
                raise FileExistsError(str(destination))
            data = before
        elif action == "delete":
            data = None
        elif action == "edit":
            text = before.decode("utf-8")
            old, new = operation["old"], operation["new"]
            if not old or text.count(old) != operation.get("count", 1):
                raise ValueError("Edit must match exactly the declared number of occurrences")
            data = text.replace(old, new).encode("utf-8")
        else:
            data = (base64.b64decode(operation["data_base64"], validate=True)
                    if "data_base64" in operation else operation["content"].encode("utf-8"))
            if action == "append":
                data = before + data
        if before is not None:
            backup = self.path(f"repo_events/origin_agents/{self.module}/backups/{uuid.uuid4().hex}.bin")
            atomic_write(backup, before)
            result["backup_path"] = str(backup.relative_to(self.root))
        if action == "delete":
            path.unlink()
            result["mutated"] = True
        else:
            target = destination or path
            atomic_write(target, data)
            result.update(mutated=True, sha256=digest(data), bytes=len(data))
            if destination:
                result["destination"] = str(destination.relative_to(self.root))
            if destination:
                os.chmod(target, stat.S_IMODE(path.stat().st_mode))
            if target.read_bytes() != data:
                raise OSError("Written content failed verification")
            result.update(sha256=digest(data), bytes=len(data))
            if destination:
                result["destination"] = str(destination.relative_to(self.root))
            if action == "move":
                path.unlink()
        result.update(mutated=True, previous_sha256=digest(before) if before is not None else None)
        return result

    def review(self, paths=None):
        """Inspect actual bytes/syntax and IDP/manifest role contracts.

        Findings are scoped observations, not a claim of ecosystem correctness.
        """
        paths = paths if paths is not None else self.profile.get("file_capabilities", {}).get("review_paths", [])
        if not isinstance(paths, list) or not paths:
            raise ValueError("Review requires explicit paths or IDP review_paths")
        findings, evidence = [], []
        for value in paths:
            path = self.path(value)
            self.require(path, "read")
            if not path.exists():
                findings.append({"kind": "missing_path", "path": value})
                continue
            files = [path] if path.is_file() else sorted(path.rglob("*"))
            for file in files:
                if not file.is_file():
                    continue
                self.path(str(file.relative_to(self.root)))
                self.require(file.resolve(), "read")
                data = file.read_bytes()
                reference = str(file.relative_to(self.root))
                evidence.append({"path": reference, "sha256": digest(data), "bytes": len(data)})
                try:
                    if file.suffix == ".py":
                        ast.parse(data, filename=reference)
                    elif file.suffix == ".json":
                        json.loads(data)
                except (ValueError, SyntaxError, UnicodeError) as exc:
                    findings.append({"kind": "invalid_syntax", "path": reference, "reason": str(exc)})
        return {"findings": findings, "evidence": evidence,
                "coverage": "existence, byte hashes, Python/JSON syntax for declared review paths",
                "role": self.profile["identity"]["designation"],
                "responsibilities": self.profile.get("responsibilities", [])}


def execute_origin(agent, task, plan, context):
    """Return None for old calls so their existing behavior is preserved."""
    request_type = agent.resolve_context_value(context, "request_type")
    if request_type not in {"origin_file_operations", "origin_review"}:
        return None
    authority = context.get("authority_context", {}) if isinstance(context, dict) else {}
    result = {"contract_version": "1.0", "module": agent.module_name, "task": task,
              "capability": request_type, "status": "FAILED", "mutated": False,
              "traceable": True, "review": False, "artifacts": [], "operations": []}
    try:
        fs = OriginFiles(agent.module_name, authority)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result.update(reason=str(exc), review=True, summary="IDP could not be loaded; no file task executed.")
        root = Path(authority.get("repo_root", ROOT)).resolve() if isinstance(authority, dict) else ROOT
        return record_event(root, agent.module_name, result)
    with repository_lock(fs.root):
        try:
            if request_type == "origin_review":
                result.update(fs.review(agent.resolve_context_value(context, "review_paths")))
                result["status"] = "REVIEW_REQUIRED" if result["findings"] else "COMPLETED"
                result["review"] = bool(result["findings"])
            else:
                operations = agent.resolve_context_value(context, "operations")
                if not isinstance(operations, list) or not operations:
                    raise ValueError("A non-empty operations list is required")
                for operation in operations:
                    outcome = fs.apply(operation)
                    result["operations"].append(outcome)
                    result["mutated"] |= outcome["mutated"]
                result["status"] = "COMPLETED"
            result["summary"] = f"{agent.module_name}: {request_type} {result['status']}"
        except (OSError, ValueError, KeyError, TypeError) as exc:
            partial = getattr(fs, "last_outcome", {})
            if partial.get("mutated") and partial not in result["operations"]:
                result["operations"].append(partial)
                result["mutated"] = True
            result.update(status="FAILED", reason=str(exc), review=True,
                          summary="Origin action stopped; completed operations remain listed.")
        return fs.record(result)
