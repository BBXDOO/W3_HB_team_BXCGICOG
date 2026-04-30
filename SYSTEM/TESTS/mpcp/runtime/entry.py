from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3


def stage_A(input_data, context):
    # design stage
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


def main():
    p = Pillar("demo")

    # register stages
    p.set_stage("A", stage_A)
    p.set_stage("D", stage_D)

    try:
        result = p.run()

        if isinstance(result, dict):
            status = result.get("status")

            if status == "🔴":
                print("STOP: not recommended")
                return

            if status == "🔵":
                print("WAIT: still processing")
                return

        print("SUCCESS:", result)

    except Exception as e:
        print("ERROR:", str(e))


if __name__ == "__main__":
    main()
