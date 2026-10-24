#!/usr/bin/env python3
"""Agent CLI: JSON request in, isolated working copy and retained evidence out."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]


def digest_files(root, names):
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}


def run_sandbox(source: Path, output: Path, request: dict, *, execute=False, timeout=60):
    source, output = source.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    run_id = "W3-SBX-" + uuid.uuid4().hex
    # Git inventory excludes secrets/untracked work; copied bytes include the
    # caller's current edits to tracked files so agents can compare candidates.
    inventory = subprocess.run(["git", "ls-files", "-z", "--", "protocol", "src"],
                               cwd=source, capture_output=True, check=True).stdout
    names = [s.decode() for s in inventory.split(b"\0") if s]
    # A new runner may not yet be tracked during development.
    if "protocol/mpcp/sandbox.py" not in names:
        names.append("protocol/mpcp/sandbox.py")
    for name in names:
        path = source / name
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(source):
            raise ValueError(f"snapshot requires regular in-repository files: {name}")
    before = digest_files(source, names)
    snapshot = output / "source"
    for name in names:
        target = snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    if before != digest_files(snapshot, names):
        raise RuntimeError("source changed during snapshot; retry")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=source,
                              capture_output=True, text=True, check=True).stdout.strip()
    workspace = output / "workspace"
    workspace.mkdir()
    (output / "request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
    worker = (
        "import json,sys; sys.path.insert(0,sys.argv[1]); "
        "from protocol.mpcp.sandbox import execute_request; "
        "r=execute_request(json.load(open(sys.argv[2])),execute=sys.argv[3]=='1',run_id=sys.argv[4]); "
        "open(sys.argv[5],'w').write(json.dumps(r,ensure_ascii=False,indent=2))"
    )
    env = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "LC_ALL", "SYSTEMROOT"}}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "HOME": str(workspace), "TMPDIR": str(workspace)})
    report = output / "result.json"
    error = None
    returncode = None
    try:
        with (output / "worker.log").open("w") as log:
            child = subprocess.run([sys.executable, "-I", "-c", worker, str(snapshot),
                                    str(output / "request.json"), str(int(execute)), run_id, str(report)],
                                   cwd=workspace, env=env, stdout=log, stderr=log, timeout=timeout)
            returncode = child.returncode
        if returncode != 0:
            error = f"worker_exit:{returncode}; see worker.log"
    except subprocess.TimeoutExpired:
        error = "worker_timeout"
    result = json.loads(report.read_text()) if report.exists() and not error else {
        "schema": "w3.agent-sandbox.result.1", "run_id": run_id,
        "state": "STOP", "error": error or "worker_result_missing", "phase_ready": False,
    }
    result["provenance"] = {
        "revision": revision, "source_sha256": before,
        "original_source_unchanged": before == digest_files(source, names),
        "snapshot_unchanged": before == digest_files(snapshot, names),
        "worker_returncode": returncode,
    }
    if not all(result["provenance"][k] for k in ("original_source_unchanged", "snapshot_unchanged")):
        result.update(state="STOP", error="source_mutation_detected", phase_ready=False)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory, retained after run")
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--execute", action="store_true", help="permit local sandbox setup only")
    args = parser.parse_args()
    try:
        result = run_sandbox(args.source_root, args.output, json.loads(args.request.read_text()), execute=args.execute)
    except (OSError, ValueError, subprocess.SubprocessError, RuntimeError) as exc:
        print(json.dumps({"state": "STOP", "error": str(exc)}))
        return 1
    print(json.dumps({"state": result["state"], "result": str(args.output.resolve() / "result.json"),
                      "artifact_verified": result.get("artifact_verified", False), "phase_ready": False}))
    return 0 if result["state"] == "SUCCESS" and result.get("artifact_verified") else 2


if __name__ == "__main__":
    raise SystemExit(main())
