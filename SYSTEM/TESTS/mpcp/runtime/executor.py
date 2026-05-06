# mpcp/runtime/executor.py

from mpcp.runtime.trace import trace as mpcp_trace
from mpcp.kernel.contract import MPCPContract
from mpcp.kernel.rot import MPCPRot
from mpcp.kernel.system import validate_system_context


# =========================
# SIMPLE REGISTRY
# =========================
PILLAR_REGISTRY = {}


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
    """
    Execute an MPCP task string.

    Flow:  A (parse) → ROT input check → B (resolve) → C (inject) →
           D (execute) → ROT output check → E (return)

    Returns a result dict: {"state": ..., "cause": ..., ...}
    Use to_mpcp_output(result) to convert to the external MPCP string format.
    """
    data = {}
    try:
        # -------------------------
        # A: INPUT → PARSE
        # -------------------------
        # `data` is pre-initialised so the FAIL_SAFE block can always read
        # data.get("TASK") for cause — even if parse_mpcp() itself raises
        # (cause will be None in that case, which is the correct behaviour).
        # -------------------------
        data = parse_mpcp(text)
        mpcp_trace("A:INPUT", data, env=data)

        # -------------------------
        # ROT VALIDATION (INPUT)
        # Checks: system name (optional), contract structure (TASK required).
        # Also runs validate_core with a synthetic STOP result to confirm
        # the CAUSE (event with TASK) is traceable before execution begins.
        # -------------------------
        validate_system_context(data)
        MPCPContract.validate_input(data)
        MPCPRot.validate_core(data, {"state": "STOP"})  # verify CAUSE linkage pre-execution
        mpcp_trace("ROT:INPUT_VALID", {"TASK": data.get("TASK")}, env=data)

        # -------------------------
        # B: RESOLVE MODEW
        # -------------------------
        task = data.get("TASK")
        builder = PILLAR_REGISTRY.get(task)

        if not builder:
            result = {
                "state": "STOP",
                "cause": task,
                "error": f"MODEW_NOT_FOUND:{task}",
            }
            mpcp_trace("B:STOP", result, env=data)
            return result

        pillar = builder()
        mpcp_trace("B:MODEW_RESOLVED", {"task": task}, env=data)

        # -------------------------
        # C: INJECT CONTEXT
        # -------------------------
        for k, v in data.items():
            pillar.set_context(k, v)
        mpcp_trace("C:CONTEXT_INJECTED", data, env=data)

        # -------------------------
        # D: EXECUTE
        # -------------------------
        result = pillar.run()
        mpcp_trace("D:EXECUTED", {"state": result.get("state")}, env=data)

        # -------------------------
        # ROT VALIDATION (OUTPUT)
        # Checks: result structure and CAUSE→RESULT traceability.
        # -------------------------
        MPCPContract.validate_output(result)
        MPCPRot.validate_core(data, result)
        MPCPRot.validate_fail_condition(data, result)
        mpcp_trace("ROT:OUTPUT_VALID", {"state": result.get("state")}, env=data)

        # -------------------------
        # E: RETURN (internal dict)
        # Use to_mpcp_output(result) for external MPCP string format.
        # -------------------------
        mpcp_trace("E:RETURN", result.get("state"), env=data)
        return result

    except Exception as e:
        # -------------------------
        # FAIL SAFE (ROT compliant)
        # Includes cause so CAUSE→ACTION→RESULT chain is preserved.
        # -------------------------
        err_result = {
            "state": "STOP",
            "cause": data.get("TASK") if data else None,
            "error": str(e),
        }
        mpcp_trace("FAIL_SAFE", str(e), env=data)
        return err_result
