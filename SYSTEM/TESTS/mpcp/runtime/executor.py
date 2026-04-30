from mpcp.pillar import Pillar


# =========================
# SIMPLE REGISTRY (no guess)
# =========================
PILLAR_REGISTRY = {}


def register(name, builder_fn):
    if not callable(builder_fn):
        raise TypeError("builder_fn must be callable")
    PILLAR_REGISTRY[name] = builder_fn


# =========================
# MPCP PARSER (strict)
# =========================
def parse_mpcp(text):
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
# OUTPUT NORMALIZER
# =========================
def to_mpcp_output(result):
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
# CORE EXECUTOR
# =========================
def run(text):
    # --- parse ---
    data = parse_mpcp(text)

    task = data.get("TASK")
    if not task:
        return "STATE:FAILED,COLOR:Red,SYM:✕"

    # --- resolve ---
    builder = PILLAR_REGISTRY.get(task)
    if not builder:
        return "STATE:FAILED,COLOR:Red,SYM:✕"

    pillar = builder()

    # --- inject context ---
    for k, v in data.items():
        pillar.set_context(k, v)

    # --- execute ---
    result = pillar.run()

    # --- normalize output ---
    return to_mpcp_output(result)
