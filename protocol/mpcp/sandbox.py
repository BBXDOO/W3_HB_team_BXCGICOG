"""Bounded local setup capability for agent experiments; no deployment authority.

Run through tools/mpcp_sandbox.py, which supplies a fresh source copy and cwd.
This is workspace separation, not an OS security boundary for hostile Python.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from protocol.mpcp.env.gateway import MPCPEnvironmentGateway
from protocol.mpcp.env.models import ExecutionAgreement
from protocol.mpcp.modew.base_modew import BaseModew
from protocol.mpcp.runtime.executor import register, run_packet
from protocol.mpcp.runtime.trace import clear_trace, get_trace_log
from protocol.w3lgu import W3LguOperationalRuntime, run_line
from src.core.blueprint import parse_blueprint


class MaterializeBlueprint(BaseModew):
    """Produce actual partition directories and a verifiable setup manifest.

    Only the portable local profile is implemented. LIB is a declaration, never
    an implicit install. A separate Modew owns action; Blueprint stays data.
    """

    def stage_D_process(self, data):
        blueprint = parse_blueprint(data["PAYLOAD"]["blueprint"])
        if blueprint.target != "local":
            raise ValueError("UNSUPPORTED_TARGET: only local setup is implemented")
        spec = blueprint.to_dict()
        unsupported = set(spec) - {"BLUEPRINT", "TARGET", "MODE", "LIB", "PARTITION", "BOUNDARY", "TRACE", "ENV"}
        if unsupported:
            raise ValueError("UNSUPPORTED_BLUEPRINT_FIELDS:" + ",".join(sorted(unsupported)))
        if spec.get("BOUNDARY") != "sandbox-local-only":
            raise ValueError("BOUNDARY must be sandbox-local-only")
        libraries = spec.get("LIB", [])
        if not set(libraries) <= {"file", "storage"}:
            raise ValueError("UNSUPPORTED_LIBRARY: local profile supports file,storage")
        partitions = spec.get("PARTITION", [])
        if not partitions or len(partitions) != len(set(partitions)):
            raise ValueError("PARTITION must contain distinct names")
        if not all(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", p) for p in partitions):
            raise ValueError("INVALID_PARTITION: simple names only")
        if any(p.casefold() == "setup.json" for p in partitions):
            raise ValueError("INVALID_PARTITION: reserved manifest name")
        # All declarations are checked before the first filesystem side effect.
        root = Path("artifacts")
        root.mkdir(exist_ok=False)
        for name in partitions:
            (root / name).mkdir()
        manifest = root / "setup.json"
        manifest.write_text(json.dumps({"blueprint": spec, "partitions": partitions,
                                      "libraries_resolved": libraries}, indent=2), encoding="utf-8")
        digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
        return {"manifest": str(manifest), "sha256": digest, "partitions": partitions,
                "partition_directories_verified": all((root / p).is_dir() for p in partitions)}


def execute_request(request: dict, *, execute: bool, run_id: str) -> dict:
    """Run W3Lgu gate → ENV/agreement → real MPCP Modew → W3Lgu result.

    The caller grants only this sandbox's fixed capability via --execute.
    Request data cannot select an arbitrary builder, module, command or path.
    """
    if not isinstance(request, dict) or set(request) - {"blueprint", "event"}:
        raise ValueError("request accepts only blueprint and event")
    if not isinstance(request.get("blueprint"), str):
        raise ValueError("blueprint text required")
    event = request.get("event", "EVENT:setup,TARGET:MPCP,ROOM:EV,CONF:1")
    runtime = W3LguOperationalRuntime()
    gate = runtime.process_line(event, cross_id=run_id)
    language = run_line(event)
    clear_trace()
    result = None
    returned = None
    if gate.decision == "READY":
        gateway = MPCPEnvironmentGateway()
        work = gateway.prepare(
            {"kind": "cross-code-dispatch", "chain_id": run_id, "event_id": gate.event_id,
             "cross_l_plan": {"scope": "CROSS_L_ONLY", "modew": "sandbox_materialize",
                              "review": True, "workset": {
                                  "tag_group": ["GEN"], "lang_candidate": ["PY"],
                                  "boundary": "sandbox-local-only", "deny": ["truth_mutation"],
                                  "return_contract": ["state", "reason", "trace"]}}},
            payload={"blueprint": request["blueprint"]},
            paper={"TASK": "sandbox_materialize", "INTENT": "materialize local setup",
                   "LANGUAGE_TAG": "GEN:PY"},
        )
        register("sandbox_materialize", MaterializeBlueprint)
        agreement = None
        if execute:
            agreement = ExecutionAgreement(
                agreement_id=run_id, lender="sandbox-cli", borrower="MPCP",
                capability=work.modew, chain_id=run_id, event_id=work.event_id,
                boundary=work.boundary, approved_by="sandbox-cli:--execute",
            )

        def capture(packet):
            nonlocal result
            result = run_packet(dict(packet))
            return result

        returned = gateway.execute(work, agreement=agreement, executor=capture)
        state = returned["result"]["state"]
    else:
        state = "STOP" if gate.decision == "STOP" else "WAIT"
    outcome = runtime.process_line(
        f"EVENT:setup.result,ROOM:RE,RESULT:{state},TARGET:MPCP,STATE:{state}",
        cross_id=run_id,
    )
    artifact = result.get("result") if result else None
    verified = False
    if state == "SUCCESS" and isinstance(artifact, dict):
        path = Path(artifact["manifest"])
        verified = (path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"]
                    and artifact["partition_directories_verified"])
    return {
        "schema": "w3.agent-sandbox.result.1", "run_id": run_id, "state": state,
        "scope": "local_setup_only", "execute_requested": execute,
        "gate": gate.to_dict(), "language_trace_id": language.trace_id,
        "mpcp": result, "cross_l_return": returned, "outcome": outcome.to_dict(),
        "executor_trace": get_trace_log(),
        "ledger": [record.to_dict() for record in runtime.ledger.records()],
        "ledger_verified": runtime.ledger.verify(), "artifact_verified": verified,
        "phase_ready": False,
        "remaining": [
            "Android/iOS/Linux build and deployment executors are not implemented here",
            "Blueprint modes min/full/stable/test need a separate agreed installation profile",
            "REA MCP adapter and W3 orchestration integration are not implemented here",
            "Local setup evidence is insufficient to certify the whole W3 next phase",
        ],
    }
