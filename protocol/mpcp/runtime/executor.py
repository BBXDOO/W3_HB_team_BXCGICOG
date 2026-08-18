# mpcp/runtime/executor.py

from .trace import trace as mpcp_trace
from ..kernel.contract import MPCPContract
from ..kernel.rot import MPCPRot
from ..kernel.system import validate_system_context


# =========================
# SIMPLE REGISTRY
# =========================
PILLAR_REGISTRY = {}


def _stop_envelope(cause, reason: str, *, action: str, modew: str, env: dict | None = None) -> dict:
    return MPCPContract.build_result_envelope(
        {"state": "STOP", "cause": cause, "reason": reason, "error": reason},
        cause=cause,
        action=action,
        modew=modew,
        env_before=env,
    )


def register(name, builder_fn):
    if not callable(builder_fn):
        raise TypeError("builder_fn must be callable")
    PILLAR_REGISTRY[name] = builder_fn


# =========================
# MPCP PARSER
# =========================
def parse_mpcp(text: str):
    if not isinstance(text, str):
        raise TypeError("Input must be string")

    parts = text.split(",")
    data = {}

    for part in parts:
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        data[k.strip().upper()] = v.strip()

    return data


# =========================
# OUTPUT FORMATTER (external only)
# =========================
def to_mpcp_output(result: dict) -> str:
    """
    Convert an internal result dict to the MPCP string format used for
    external communication (e.g. display, logging, inter-system packets).

    Format: STATE:<state>,COLOR:<color>,SYM:<symbol>

    Color mapping (aligned with COLOR_STATE.md):
      Green  → SUCCESS, done, ready
      Yellow → WAIT, wait, warn, run, idle
      Red    → STOP, fail, block
    """
    if not isinstance(result, dict):
        return "STATE:STOP,COLOR:Red,SYM:✕"

    state = result.get("state", "STOP")

    _GREEN = ("SUCCESS", "done", "ready")
    _YELLOW = ("WAIT", "wait", "warn", "run", "idle")
    _RED = ("STOP", "fail", "block")

    if state in _GREEN:
        return f"STATE:{state},COLOR:Green,SYM:✓"

    if state in _YELLOW:
        return f"STATE:{state},COLOR:Yellow,SYM:!"

    if state in _RED:
        return f"STATE:{state},COLOR:Red,SYM:✕"

    # Unknown state — conservative fallback
    return f"STATE:STOP,COLOR:Red,SYM:✕"


# =========================
# CORE EXECUTOR (ROT aligned)
# =========================
def run(text: str) -> dict:
    """Parse MPCP text, then pass the normalized packet to ``run_packet``."""

    try:
        return run_packet(parse_mpcp(text))
    except Exception as exc:
        mpcp_trace("FAIL_SAFE", str(exc), env={})
        return _stop_envelope(None, str(exc), action="parse", modew="unresolved")


def run_packet(packet: dict) -> dict:
    """Execute a packet after its language and ENV boundary was resolved.

    A–F are semantic layers in a Pillar, not executor step numbers. Runtime
    operations therefore use descriptive trace names.
    """

    data = {}
    try:
        if not isinstance(packet, dict):
            raise TypeError("MPCP packet must be dict")
        data = dict(packet)
        mpcp_trace("INPUT:ACCEPTED", data, env=data)

        validate_system_context(data)
        MPCPContract.validate_input(data)
        MPCPRot.validate_core(data, {"state": "STOP"})
        mpcp_trace("ROT:INPUT_VALID", {"TASK": data.get("TASK")}, env=data)

        task = data.get("TASK")
        modew_name = data.get("MODEW") or task
        builder = PILLAR_REGISTRY.get(modew_name)
        if not builder:
            result = _stop_envelope(
                task,
                f"MODEW_NOT_FOUND:{modew_name}",
                action="modew_resolve",
                modew=str(modew_name),
                env=data,
            )
            mpcp_trace("MODEW:NOT_FOUND", result, env=data)
            return result

        pillar = builder()
        mpcp_trace("MODEW:RESOLVED", {"task": task, "modew": modew_name}, env=data)

        for k, v in data.items():
            pillar.set_context(k, v)
        mpcp_trace("CONTEXT:INJECTED", data, env=data)

        result = pillar.run()
        mpcp_trace("MODEW:EXECUTED", {"state": result.get("state")}, env=data)

        result = MPCPContract.build_result_envelope(
            result,
            cause=task,
            action="modew_execute",
            modew=str(modew_name),
            role=str(data.get("ROLE", "default")),
            env_before=data,
        )
        MPCPContract.validate_result_envelope(result, strict=True)
        MPCPRot.validate_core(data, result)
        MPCPRot.validate_fail_condition(data, result)
        result["law"]["validated"] = True
        mpcp_trace("ROT:OUTPUT_VALID", {"state": result.get("state")}, env=data)
        mpcp_trace("RESULT:RETURN", result.get("state"), env=data)
        return result

    except Exception as exc:
        err_result = _stop_envelope(
            data.get("TASK") if data else None,
            str(exc),
            action="runtime_fail_safe",
            modew=str(data.get("MODEW") or data.get("TASK") or "unresolved"),
            env=data,
        )
        mpcp_trace("FAIL_SAFE", str(exc), env=data)
        return err_result
