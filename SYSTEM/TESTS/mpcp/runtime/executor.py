from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3


# =========================
# Stage A
# =========================
def stage_A(input_data, context):
    return {
        "task": "design",
        "state": "SUCCESS",   # machine
        "color": "🟢"         # human
    }


# =========================
# Stage D
# =========================
def stage_D(input_data, context):
    if not input_data:
        return {
            "state": "STOP",
            "color": "🔴",
            "error": "missing input"
        }

    result = execute_with_w3(input_data["task"])

    if result is None:
        return {
            "task": input_data["task"],
            "state": "WAIT",
            "color": "🔵"
        }

    return {
        "task": input_data["task"],
        "result": result,
        "state": "SUCCESS",
        "color": "🟢"
    }


# =========================
# RUN ENGINE
# =========================
def run(task_name):
    p = Pillar(task_name)

    # register stages
    p.set_stage("A", stage_A)
    p.set_stage("D", stage_D)

    result = p.run()

    # ---------- control ----------
    if isinstance(result, dict):
        state = result.get("state")

        if state == "STOP":
            return {
                "status": "STOP",
                "data": result
            }

        if state == "WAIT":
            return {
                "status": "WAIT",
                "data": result
            }

    return {
        "status": "SUCCESS",
        "data": result
    }
