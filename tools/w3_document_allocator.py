#!/usr/bin/env python3
"""Create traceable AMS documents with BOX-aware allocation checks.

BOX remains planner-only.  This tool may read BOX registry/suggestions, but a
write happens only when the caller explicitly selects create/update mode and
supplies an authorization identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.check_portable_paths import path_problems
from wx.engine_index import BoxRegistryError, load_template_registry
from wx.indexor import suggest_references


AM_ROLES = {"I": "CORE_MEANING", "II": "ADAPTATION", "III": "OPERATIONAL"}
AMS_GROUPS = {"BUILD", "OBSERVE", "LEARN", "CONTINUE"}
WRITE_MODES = {"dry-run", "create", "update"}
BOX_MANAGED_ROOTS = (
    PurePosixPath("wx/templates"),
    PurePosixPath("wx/blueprints"),
    PurePosixPath("wx/references"),
    PurePosixPath("wx/registry"),
)


class AllocationError(ValueError):
    """Raised when a document cannot be allocated without guessing authority."""


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_relative_path(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        raise AllocationError("target path is required")
    path = PurePosixPath(value.strip())
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise AllocationError("target must be a repository-relative path without '..'")
    if path.suffix.lower() != ".md":
        raise AllocationError("target must be a Markdown (.md) file")
    problems = path_problems(path.as_posix())
    if problems:
        raise AllocationError("target is not portable: " + "; ".join(problems))
    return path


def _resolve_inside(root: Path, relative: PurePosixPath) -> Path:
    root = root.resolve()
    candidate = (root / Path(*relative.parts)).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise AllocationError("target escapes repository root") from exc
    return candidate


def _under(path: PurePosixPath, parent: PurePosixPath) -> bool:
    return path == parent or parent in path.parents


def _validate_lineage(root: Path, am_type: str, sources: Iterable[str]) -> list[str]:
    refs = [str(item).strip() for item in sources if str(item).strip()]
    if am_type in {"II", "III"} and not refs:
        raise AllocationError(f"AM:{am_type} requires at least one DERIVED_FROM reference")
    for ref in refs:
        source = PurePosixPath(ref)
        if source.is_absolute() or ".." in source.parts:
            raise AllocationError(f"unsafe DERIVED_FROM reference: {ref}")
        if not _resolve_inside(root, source).is_file():
            raise AllocationError(f"DERIVED_FROM source does not exist: {ref}")
    return refs


@dataclass(frozen=True)
class DocumentSpec:
    title: str
    target: str
    am_type: str
    group: str
    owner: str
    maker: str
    body: str
    derived_from: tuple[str, ...] = ()
    request_id: str | None = None
    note: str = "draft / review required"
    status: str = "draft"
    box_work_type: str | None = None

    def normalized(self, root: Path) -> tuple[PurePosixPath, list[str]]:
        if not self.title.strip() or not self.owner.strip() or not self.maker.strip():
            raise AllocationError("title, owner and maker are required")
        am_type = self.am_type.upper().replace("AM:", "").strip()
        if am_type not in AM_ROLES:
            raise AllocationError("AM type must be I, II or III")
        group = self.group.upper().strip()
        if group not in AMS_GROUPS:
            raise AllocationError("group must be BUILD, OBSERVE, LEARN or CONTINUE")
        return _safe_relative_path(self.target), _validate_lineage(root, am_type, self.derived_from)


def _duplicate_paths(root: Path, target: PurePosixPath) -> list[str]:
    wanted = target.name.casefold()
    matches: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative != target.as_posix() and path.name.casefold() == wanted:
            matches.append(relative)
    return sorted(matches)


def inspect_allocation(spec: DocumentSpec, *, repo_root: Path = REPOSITORY_ROOT) -> dict[str, Any]:
    """Build a non-mutating AMS/BOX allocation plan."""
    root = repo_root.resolve()
    target, lineage = spec.normalized(root)
    absolute = _resolve_inside(root, target)
    parent = absolute.parent
    if not parent.is_dir():
        raise AllocationError(f"target directory does not exist: {target.parent.as_posix()}")
    if absolute.is_symlink():
        raise AllocationError("target must not be a symlink")
    current = root
    for component in target.parent.parts:
        current = current / component
        if current.is_symlink():
            raise AllocationError("target path contains a symlinked directory")

    am_type = spec.am_type.upper().replace("AM:", "").strip()
    group = spec.group.upper().strip()
    duplicates = _duplicate_paths(root, target)
    box_managed = any(_under(target, prefix) for prefix in BOX_MANAGED_ROOTS)
    warnings: list[str] = []
    if duplicates:
        warnings.append("same filename exists elsewhere; review before creating another document")
    readme_present = target.name.casefold() == "readme.md" or (parent / "README.md").is_file()
    if not readme_present:
        warnings.append("target folder has no README.md; AMS folder identity is incomplete")
    if box_managed:
        warnings.append("target is BOX-managed source space; use library maintenance instead")

    try:
        registry = load_template_registry()
        box_registry = {"valid": True, "version": registry["version"], "error": None}
        suggestions = (
            suggest_references(work_type=spec.box_work_type)
            if spec.box_work_type
            else {
                "state": "not_requested",
                "planner_only": True,
                "execution_allowed": False,
                "mutated": False,
                "copy_allowed_by_runtime": False,
                "human_review_required": True,
                "suggestions": [],
            }
        )
    except BoxRegistryError as exc:
        box_registry = {"valid": False, "version": None, "error": str(exc)}
        suggestions = {
            "state": "registry_error",
            "planner_only": True,
            "execution_allowed": False,
            "mutated": False,
            "copy_allowed_by_runtime": False,
            "human_review_required": True,
            "suggestions": [],
        }
        warnings.append("BOX registry is invalid; fail closed")

    prohibited = box_managed or not box_registry["valid"]
    return {
        "contract_version": "1.0",
        "tool": "W3 Document Allocator",
        "target": target.as_posix(),
        "target_exists": absolute.exists(),
        "ams": {
            "type": am_type,
            "role": AM_ROLES[am_type],
            "group": group,
            "derived_from": lineage,
            "folder_readme_present": readme_present,
        },
        "box": {
            "planner_only": True,
            "execution_allowed": False,
            "registry": box_registry,
            "suggestions": suggestions["suggestions"],
            "suggestion_state": suggestions["state"],
            "target_state": "prohibited" if prohibited else "conditional",
            "reason": (
                "BOX-managed source space is outside allocator write scope"
                if box_managed
                else "write authority must come from the caller, not BOX"
            ),
        },
        "duplicates": duplicates,
        "warnings": warnings,
        "write_allowed": not prohibited,
        "mutated": False,
        "review": True,
    }


def render_document(spec: DocumentSpec, plan: dict[str, Any], *, created_at: str | None = None) -> str:
    """Render the AMS identity, body, movement, and owner sections."""
    at = created_at or _now()
    ams = plan["ams"]
    sources = ams["derived_from"]
    yaml_lineage = (
        "DERIVED_FROM:\n" + "\n".join(f"  - {json.dumps(item, ensure_ascii=False)}" for item in sources)
        if sources else "DERIVED_FROM: []"
    )
    target_parent = PurePosixPath(plan["target"]).parent.as_posix()
    movement = (
        "\n".join(
            f"- [{item}]({posixpath.relpath(item, start=target_parent)})"
            for item in sources
        )
        if sources else "- No upstream document declared (AM:I origin)."
    )
    request = spec.request_id or "none"
    body = spec.body.strip()
    return (
        "---\n"
        f"AM_TYPE: {ams['type']}\n"
        f"ROLE: {ams['role']}\n"
        f"GROUP: {ams['group']}\n"
        f"{yaml_lineage}\n"
        f"OWNER: {json.dumps(spec.owner.strip(), ensure_ascii=False)}\n"
        f"MAKER: {json.dumps(spec.maker.strip(), ensure_ascii=False)}\n"
        f"STATUS: {json.dumps(spec.status.strip(), ensure_ascii=False)}\n"
        f"REQUEST_ID: {json.dumps(request, ensure_ascii=False)}\n"
        f"CREATED_AT: {json.dumps(at)}\n"
        "---\n\n"
        f"# {spec.title.strip()}\n\n"
        "## Head line\n\n"
        f"1. Name: {spec.title.strip()}\n"
        f"2. AM {ams['type']} - {ams['group']}: {ams['role']}\n"
        f"3. ID: {request}\n"
        f"4. Note: {spec.note.strip()}\n\n"
        "## Body line\n\n"
        f"{body}\n\n"
        "## Movement line\n\n"
        f"{movement}\n\n"
        "## Owner line\n\n"
        f"- Owner: {spec.owner.strip()}\n"
        f"- Maker: {spec.maker.strip()}\n"
        f"- Log: {at}; status={spec.status.strip()}; request={request}\n"
    )


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=False, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".w3doc-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def allocate_document(
    spec: DocumentSpec,
    *,
    mode: str = "dry-run",
    authorized_by: str | None = None,
    expected_sha256: str | None = None,
    repo_root: Path = REPOSITORY_ROOT,
) -> dict[str, Any]:
    """Inspect, create, or update one document and return an artifact receipt."""
    if mode not in WRITE_MODES:
        raise AllocationError(f"unsupported mode: {mode}")
    root = repo_root.resolve()
    plan = inspect_allocation(spec, repo_root=root)
    target = _resolve_inside(root, _safe_relative_path(spec.target))
    before = target.read_bytes() if target.is_file() else None
    previous_sha = _sha256(before) if before is not None else None
    content = render_document(spec, plan).encode("utf-8")

    if mode == "dry-run":
        return {
            **plan,
            "status": "PLANNED",
            "mode": mode,
            "preview_sha256": _sha256(content),
            "bytes": len(content),
            "previous_sha256": previous_sha,
        }
    if not authorized_by or not authorized_by.strip():
        raise AllocationError("create/update requires an explicit authorized_by identity")
    if not plan["write_allowed"]:
        raise AllocationError("allocation is prohibited by BOX/path boundary")
    if mode == "create" and before is not None:
        raise AllocationError("target already exists; use update with expected_sha256")
    if mode == "update":
        if before is None:
            raise AllocationError("update target does not exist")
        if not expected_sha256 or expected_sha256 != previous_sha:
            raise AllocationError("update requires the current expected_sha256")

    _atomic_write(target, content)
    return {
        **plan,
        "status": "CREATED" if before is None else "UPDATED",
        "mode": mode,
        "authorized_by": authorized_by.strip(),
        "artifact": {
            "path": target.relative_to(root).as_posix(),
            "sha256": _sha256(content),
            "bytes": len(content),
            "previous_sha256": previous_sha,
            "kind": "w3.ams_document.markdown",
        },
        "mutated": True,
        "review": True,
    }


def make_orchestration_handler(
    spec: DocumentSpec,
    *,
    authorized_by: str,
    repo_root: Path = REPOSITORY_ROOT,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Return an explicit TOOL handler compatible with orchestration.assist()."""
    def handler(context: dict[str, Any]) -> dict[str, Any]:
        blocker = context.get("blocker") if isinstance(context, dict) else None
        if not isinstance(blocker, dict):
            raise AllocationError("orchestration blocker evidence is required")
        receipt = allocate_document(
            spec,
            mode="create",
            authorized_by=authorized_by,
            repo_root=repo_root,
        )
        return {
            "resolved": True,
            "evidence": f"{receipt['artifact']['path']}#sha256={receipt['artifact']['sha256']}",
            "receipt": receipt,
        }
    return handler


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create AMS documents with BOX-aware allocation checks")
    parser.add_argument("--title", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--am-type", required=True, choices=sorted(AM_ROLES))
    parser.add_argument("--group", required=True, choices=sorted(AMS_GROUPS))
    parser.add_argument("--owner", required=True)
    parser.add_argument("--maker", required=True)
    parser.add_argument("--body-file", required=True, help="UTF-8 body source; use - for stdin")
    parser.add_argument("--derived-from", action="append", default=[])
    parser.add_argument("--request-id")
    parser.add_argument("--note", default="draft / review required")
    parser.add_argument("--status", default="draft")
    parser.add_argument("--box-work-type")
    parser.add_argument("--mode", choices=sorted(WRITE_MODES), default="dry-run")
    parser.add_argument("--authorized-by")
    parser.add_argument("--expected-sha256")
    return parser


def main() -> int:
    parser = _parser()
    args = parser.parse_args()
    if args.body_file == "-":
        import sys
        body = sys.stdin.read()
    else:
        body = Path(args.body_file).read_text(encoding="utf-8")
    spec = DocumentSpec(
        title=args.title,
        target=args.target,
        am_type=args.am_type,
        group=args.group,
        owner=args.owner,
        maker=args.maker,
        body=body,
        derived_from=tuple(args.derived_from),
        request_id=args.request_id,
        note=args.note,
        status=args.status,
        box_work_type=args.box_work_type,
    )
    try:
        receipt = allocate_document(
            spec,
            mode=args.mode,
            authorized_by=args.authorized_by,
            expected_sha256=args.expected_sha256,
        )
    except (AllocationError, OSError) as exc:
        parser.exit(2, json.dumps({"status": "REJECTED", "error": str(exc)}, ensure_ascii=False) + "\n")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
