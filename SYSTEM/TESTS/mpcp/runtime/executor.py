from mpcp.lib.pillar import Pillar
from mpcp.adapter.w3_bridge import execute_with_w3
from mpcp.runtime.trace import trace


class MPCPExecutor:

    def __init__(self):
        self.pillar = Pillar("MAIN")

        self.pillar.set_stage("A", self.stage_input)
        self.pillar.set_stage("D", self.stage_execute)
        self.pillar.set_stage("F", self.stage_output)

    # ------------------------

    def stage_input(self, _, ctx):
        task = ctx["task"]
        trace("A", task)
        return task

    def stage_execute(self, task, ctx):
        trace("D", task)

        result = execute_with_w3(task)

        trace("D_RESULT", result)
        return result

    def stage_output(self, result, ctx):
        trace("F", result)
        return {
            "system": "MPCP",
            "status": "SUCCESS",
            "result": result
        }

    # ------------------------

    def run(self, task):
        context = {
            "task": task
        }

        return self.pillar.run(context)
