# mpcp/runtime/executor.py


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
def to_mpcp_output(result: dict):
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
# CORE EXECUTOR (ROT aligned)
# =========================
def run(text: str):
    try:
        # -------------------------
        # A: INPUT → PARSE
        # -------------------------
        data = parse_mpcp(text)

        # -------------------------
        # ROT VALIDATION (INPUT)
        # -------------------------
        
        # -------------------------
        # B: RESOLVE MODEW
        # -------------------------
        task = data.get("TASK")
        builder = PILLAR_REGISTRY.get(task)

        if not builder:
            return to_mpcp_output({
                "state": "STOP",
                "error": f"MODEW_NOT_FOUND:{task}"
            })

        pillar = builder()

        # -------------------------
        # C: INJECT CONTEXT
        # -------------------------
        for k, v in data.items():
            pillar.set_context(k, v)

        # -------------------------
        # D: EXECUTE
        # -------------------------
        result = pillar.run()

        # -------------------------
        # ROT VALIDATION (OUTPUT)
        # -------------------------

        # -------------------------
        # E: RETURN (mpcp format)
        # -------------------------
        return to_mpcp_output(result)

    except Exception as e:
        # -------------------------
        # FAIL SAFE (ROT compliant)
        # -------------------------
        return to_mpcp_output({
            "state": "STOP",
            "error": str(e)
        })
