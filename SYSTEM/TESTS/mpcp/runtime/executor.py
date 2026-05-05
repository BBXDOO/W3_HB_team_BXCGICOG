# mpcp/runtime/executor.py

# =========================
# IMPORTS
# =========================
from typing import Dict, Tuple

# =========================
# SIMPLE REGISTRY
# =========================
# map TASK → Modew class
PILLAR_REGISTRY = {}


def register(name: str, cls):
    if not callable(cls):
        raise TypeError("Modew must be callable/class")
    PILLAR_REGISTRY[name] = cls


# =========================
# MPCP PARSER (strict simple)
# =========================
def parse_mpcp(text: str) -> Dict[str, str]:
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
# PAPER VALIDATOR
# =========================
REQUIRED_FIELDS = ["TASK", "SCOPE", "INCLUDE", "EXCLUDE", "MODEW", "OUTPUT"]


def validate_paper(data: Dict[str, str]) -> Tuple[bool, str]:
    # --- required fields ---
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            return False, f"MISSING:{field}"

    # --- include / exclude overlap ---
    include = set([x.strip() for x in data["INCLUDE"].split(",") if x.strip()])
    exclude = set([x.strip() for x in data["EXCLUDE"].split(",") if x.strip()])

    if include & exclude:
        return False, "CONFLICT:INCLUDE_EXCLUDE"

    # --- scope sanity ---
    if data["SCOPE"] == "*" or len(data["SCOPE"].strip()) == 0:
        return False, "INVALID:SCOPE"

    # --- modew mapping must exist ---
    task = data["TASK"]
    if task not in PILLAR_REGISTRY:
        return False, "NO_MODEW_REGISTERED"

    return True, "OK"


# =========================
# OUTPUT NORMALIZER (PRX layer)
# =========================
def to_mpcp_output(result: Dict) -> str:
    if not isinstance(result, dict):
        return "STATE:FAILED,COLOR:Red,SYM:✕"

    state = result.get("state", "FAILED")

    if state == "SUCCESS":
        return "STATE:SUCCESS,COLOR:Green,SYM:✓"

    if state == "WAIT":
        return "STATE:WAIT,COLOR:Yellow,SYM:!"

    if state == "STOP":
        return "STATE:STOP,COLOR:Red,SYM:✕"

    return "STATE:FAILED,COLOR:Red,SYM:✕"


# =========================
# TRACE VALIDATION (ROT LAW)
# =========================
def validate_trace(result: Dict) -> Tuple[bool, str]:
    if not isinstance(result, dict):
        return False, "INVALID_RESULT"

    if "cause" not in result:
        return False, "MISSING_CAUSE"

    if "action" not in result:
        return False, "MISSING_ACTION"

    return True, "OK"


# =========================
# CORE EXECUTOR
# =========================
def run(text: str) -> str:
    # -------------------------
    # 1. PARSE
    # -------------------------
    data = parse_mpcp(text)

    # -------------------------
    # 2. VALIDATE PAPER
    # -------------------------
    ok, reason = validate_paper(data)
    if not ok:
        return f"STATE:FAILED,COLOR:Red,SYM:✕,REASON:{reason}"

    # -------------------------
    # 3. RESOLVE MODEW
    # -------------------------
    task = data["TASK"]
    modew_cls = PILLAR_REGISTRY.get(task)

    try:
        modew = modew_cls()
    except Exception:
        return "STATE:FAILED,COLOR:Red,SYM:✕,REASON:MODEW_INIT_FAIL"

    # -------------------------
    # 4. INJECT CONTEXT
    # -------------------------
    for k, v in data.items():
        if hasattr(modew, "set_context"):
            modew.set_context(k, v)

    # -------------------------
    # 5. EXECUTE
    # -------------------------
    try:
        result = modew.run()
    except Exception:
        return "STATE:FAILED,COLOR:Red,SYM:✕,REASON:EXECUTION_ERROR"

    # -------------------------
    # 6. TRACE CHECK (ROT LAW)
    # -------------------------
    ok, reason = validate_trace(result)
    if not ok:
        return f"STATE:FAILED,COLOR:Red,SYM:✕,REASON:{reason}"

    # -------------------------
    # 7. OUTPUT (PRX only)
    # -------------------------
    return to_mpcp_output(result)


# =========================
# EXAMPLE MODEW (SAFE DEFAULT)
# =========================
class DefaultModew:
    def __init__(self):
        self.context = {}

    def set_context(self, k, v):
        self.context[k] = v

    def run(self):
        return {
            "state": "SUCCESS",
            "cause": "default_execution",
            "action": "noop"
        }


# register default (optional fallback)
register("default", DefaultModew)
