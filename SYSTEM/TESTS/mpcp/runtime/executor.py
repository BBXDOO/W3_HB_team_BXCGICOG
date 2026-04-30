from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3


def stage_A(input_data, context):
    return {
        "task": "design",
        "status": "🟢"
    }


def stage_D(input_data, context):
    if not input_data:
        raise ValueError("Stage D: missing input")

    result = execute_with_w3(input_data["task"])

    return {
        "task": input_data["task"],
        "result": result,
        "status": "🔵" if result is None else "🟢"
    }


def run(task_name):
    p = Pillar(task_name)

    p.set_stage("A", stage_A)
    p.set_stage("D", stage_D)

    result = p.run()

    if isinstance(result, dict):
        status = result.get("status")

        if status == "🔴":
            return {"status": "STOP", "data": result}

        if status == "🔵":
            return {"status": "WAIT", "data": result}

    return {"status": "SUCCESS", "data": result}
