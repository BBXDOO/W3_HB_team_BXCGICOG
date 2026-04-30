from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3
from mpcp.runtime.trace import trace


class MPCPExecutor:

    def __init__(self):
        self.pillar = Pillar("mpcp-runtime", pillar_type="CORE")

        # register stages (ไม่ใช้ lambda ลอย ๆ แล้ว)
        self.pillar.set_stage("A", self.stage_input)
        self.pillar.set_stage("D", self.stage_execute)

    # ------------------------
    # STAGES
    # ------------------------

    def stage_input(self, _, context):
        task = context.get("task")
        trace("A", task)
        return task

    def stage_execute(self, task, context):
        trace("D", task)

        try:
            result = execute_with_w3(task)
            trace("D_RESULT", result)
            return result

        except Exception as e:
            trace("ERROR", str(e))
            raise

    # ------------------------
    # RUN
    # ------------------------

    def run(self, task: str):
        context = {
            "task": task,
            "system": "MPCP"
        }

        return self.pillar.run_with_context(context)
