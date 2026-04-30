from mpcp.runtime.executor import run


class MPCPManager:
    def __init__(self):
        self.flows = []

    # -------------------------
    # เพิ่ม flow (ไม่ใช่ job เดี่ยว)
    # -------------------------
    def add_flow(self, flow_name, steps):
        """
        steps = ["design", "analysis", ...]
        """
        self.flows.append({
            "name": flow_name,
            "steps": steps,
            "current": 0,
            "results": []
        })

    # -------------------------
    # execute flow ทั้งหมด
    # -------------------------
    def execute(self):
        outputs = []

        for flow in self.flows:
            flow_result = self._run_flow(flow)
            outputs.append(flow_result)

        return outputs

    # -------------------------
    # core flow engine
    # -------------------------
    def _run_flow(self, flow):
        while flow["current"] < len(flow["steps"]):
            task = flow["steps"][flow["current"]]

            result = run(task)
            flow["results"].append(result)

            status = result.get("status")

            if status == "STOP":
                return {
                    "flow": flow["name"],
                    "status": "STOP",
                    "step": task,
                    "results": flow["results"]
                }

            if status == "WAIT":
                return {
                    "flow": flow["name"],
                    "status": "WAIT",
                    "step": task,
                    "results": flow["results"]
                }

            # SUCCESS → ไป step ถัดไป
            flow["current"] += 1

        return {
            "flow": flow["name"],
            "status": "SUCCESS",
            "results": flow["results"]
        }
