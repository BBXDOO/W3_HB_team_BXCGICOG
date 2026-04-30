from mpcp.runtime.executor import run


class MPCPManager:
    def __init__(self):
        self.flows = []

    # =========================
    # ADD FLOW
    # =========================
    def add_flow(self, flow_name, steps):
        if not isinstance(steps, list) or not steps:
            raise ValueError("steps must be a non-empty list")

        self.flows.append({
            "name": flow_name,
            "steps": steps,
            "current": 0,
            "results": [],
            "status": "PENDING"
        })

    # =========================
    # EXECUTE (เริ่ม flow)
    # =========================
    def execute(self):
        outputs = []

        for flow in self.flows:
            # เริ่มใหม่เสมอ
            flow["current"] = 0
            flow["results"] = []
            flow["status"] = "RUNNING"

            result = self._run_flow(flow)
            outputs.append(result)

        return outputs

    # =========================
    # RESUME (ทำต่อจาก WAIT)
    # =========================
    def resume(self):
        outputs = []

        for flow in self.flows:
            if flow["status"] != "WAIT":
                continue

            result = self._run_flow(flow)
            outputs.append(result)

        return outputs

    # =========================
    # RESET (ล้างทั้งหมด)
    # =========================
    def reset(self):
        for flow in self.flows:
            flow["current"] = 0
            flow["results"] = []
            flow["status"] = "PENDING"

    # =========================
    # CORE FLOW ENGINE
    # =========================
    def _run_flow(self, flow):
        while flow["current"] < len(flow["steps"]):
            task = flow["steps"][flow["current"]]

            result = run(task)

            # -------------------------
            # VALIDATION
            # -------------------------
            if not isinstance(result, dict) or "status" not in result:
                flow["status"] = "STOP"
                return {
                    "flow": flow["name"],
                    "status": "STOP",
                    "error": "invalid executor response",
                    "step": task
                }

            flow["results"].append(result)

            status = result["status"]

            # -------------------------
            # CONTROL
            # -------------------------
            if status == "STOP":
                flow["status"] = "STOP"
                return {
                    "flow": flow["name"],
                    "status": "STOP",
                    "step": task,
                    "results": flow["results"]
                }

            if status == "WAIT":
                flow["status"] = "WAIT"
                return {
                    "flow": flow["name"],
                    "status": "WAIT",
                    "step": task,
                    "results": flow["results"]
                }

            # SUCCESS → ไปต่อ
            flow["current"] += 1

        # -------------------------
        # FLOW COMPLETE
        # -------------------------
        flow["status"] = "SUCCESS"

        return {
            "flow": flow["name"],
            "status": "SUCCESS",
            "results": flow["results"]
        }
