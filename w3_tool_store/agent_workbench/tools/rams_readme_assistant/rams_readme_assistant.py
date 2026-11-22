#!/usr/bin/env python3
"""Opt-in, non-evaluating RAMS README helper. No policy/schema mutation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

SKIP = {".git", ".venv", "venv", "__pycache__", "node_modules"}
EXCLUDED = {"README.md"}

def safe_scope(root: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("scope must be a repository-relative directory")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("symlink scope is not supported")
    resolved = current.resolve()
    if not resolved.is_dir() or not resolved.is_relative_to(root.resolve()):
        raise ValueError("scope must be an existing directory inside repository")
    return resolved

def folders(root: Path, scope: Path, levels: set[int]):
    stack = [scope]
    while stack:
        directory = stack.pop()
        depth = len(directory.relative_to(root).parts)
        if depth in levels:
            yield directory, depth
        if depth >= max(levels):
            continue
        children = sorted((p for p in directory.iterdir() if p.is_dir() and
                           p.name not in SKIP and not p.is_symlink()), key=lambda p: p.name.encode())
        stack.extend(reversed(children))

def grade(depth: int) -> str:
    if depth < 1 or depth > 26:
        raise ValueError("RAMS supports folder levels A-Z")
    return chr(64 + depth) + "r1ra"

def make_readme(root: Path, folder: Path, depth: int, owner: str, maker: str) -> str:
    relative = folder.relative_to(root).as_posix()
    children = sorted((p for p in folder.iterdir() if not p.is_symlink() and
                       p.name not in EXCLUDED), key=lambda p: p.name.encode())
    entries = []
    for item in children:
        kind = "folder" if item.is_dir() else "file"
        entries.append(f"| [`{item.name}`](./{quote(item.name, safe='')}{'/' if item.is_dir() else ''}) | {kind} |")
    movement = "\n".join(entries) if entries else "| (empty) | — |"
    today = datetime.now(timezone.utc).date().isoformat()
    slug = re.sub(r"[^A-Z0-9]+", "-", relative.upper()).strip("-") or "ROOT"
    return (f"Name : {relative} — W3 directory index  \n"
            "AM Ⅱ - BUILD : RAMS directory description (non-evaluating)  \n"
            f"Log time : {today} (UTC) ; ID : RAMS-{slug}-001  \n"
            f"≡ {grade(depth)} - RAMS\n\n"
            "## Body\n\n"
            f"This README indexes the observed contents of `{relative}/`. "
            "The directory's purpose is not inferred from its name; "
            "add an owner-confirmed description when available.\n\n"
            "## Movement\n\n### M1 — Observed entries\n\n"
            "| Entry | Type |\n|---|---|\n" + movement + "\n\n"
            "### M2 — Related documents\n\n"
            "- No external relationships asserted automatically.\n\n"
            f"OWNER : {owner}  \nMAKER : {maker}\n")

def run(root: Path, scope: str, levels: set[int], mode: str, owner: str, maker: str):
    root = root.resolve()
    if not root.is_dir() or not (root / ".git").exists():
        raise ValueError("repo-root must contain a .git directory or file")
    target = safe_scope(root, scope)
    records = []
    for folder, depth in folders(root, target, levels):
        readme = folder / "README.md"
        if readme.exists() or readme.is_symlink():
            records.append({"path": str(readme.relative_to(root)), "status": "EXISTS"})
            continue
        content = make_readme(root, folder, depth, owner, maker)
        digest = hashlib.sha256(content.encode()).hexdigest()
        status = "PLANNED"
        if mode == "create":
            # Exclusive creation: no overwrite even if another process creates it.
            fd = os.open(readme, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
                    stream.write(content)
            except BaseException:
                readme.unlink(missing_ok=True)
                raise
            status = "CREATED"
        records.append({"path": str(readme.relative_to(root)), "status": status, "sha256": digest})
    return {"mode": mode, "scope": scope, "levels": sorted(levels), "records": records,
            "mutated": any(r["status"] == "CREATED" for r in records)}

def main():
    parser = argparse.ArgumentParser(description="Opt-in RAMS README discovery and creation")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--scope", required=True)
    parser.add_argument("--levels", required=True, help="Absolute Git folder levels, e.g. A,B")
    parser.add_argument("--mode", choices=("dry-run", "create"), default="dry-run")
    parser.add_argument("--owner", default="BBX19")
    parser.add_argument("--maker", default="W3 RAMS README Assistant")
    args = parser.parse_args()
    try:
        levels = {ord(s.strip().upper()) - 64 for s in args.levels.split(",")}
        if not levels or any(n < 1 or n > 26 for n in levels):
            raise ValueError("levels must contain letters A-Z")
        result = run(args.repo_root, args.scope, levels, args.mode, args.owner, args.maker)
    except (ValueError, OSError) as exc:
        parser.exit(2, json.dumps({"status": "REJECTED", "error": str(exc)}) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
