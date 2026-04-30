from mpcp.runtime.executor import run


class MPCPManager:
    def __init__(self):
        self.flows = []

    def add_flow(self, flow_name, steps):
        self.flows.append({
            "name": flow_name,
            "steps": steps,
            "current": 0,
            "results": []
        })

    def execute(self):
        outputs = []

        for flow in self.flows:
            result = self._run_flow(flow)
            outputs.append(result)

        return outputs

    # =========================
    # CORE FLOW ENGINE
    # =========================
    def _run_flow(self, flow):
        while flow["current"] < len(flow["steps"]):

            step = flow["steps"][flow["current"]]

            result = run(step)
            flow["results"].append(result)

            # -------------------------
            # VALIDATION (MPCP format)
            # -------------------------
            if not isinstance(result, dict):
                return self._stop(flow, step, "invalid result type")

            state = result.get("state")

            if state not in ["SUCCESS", "WAIT", "STOP"]:
                return self._stop(flow, step, f"invalid state: {state}")

            # -------------------------
            # CONTROL FLOW
            # -------------------------
            if state == "STOP":
                return self._response(flow, step, "STOP")

            if state == "WAIT":
                return self._response(flow, step, "WAIT")

            # SUCCESS → next step
            flow["current"] += 1

        # -------------------------
        # DONE
        # -------------------------
        return {
            "flow": flow["name"],
            "state": "SUCCESS",
            "results": flow["results"]
        }

    # =========================
    # INTERNAL HELPERS
    # =========================
    def _stop(self, flow, step, error):
        return {
            "flow": flow["name"],
            "state": "STOP",
            "step": step,
            "error": error,
            "results": flow["results"]
        }

    def _response(self, flow, step, state):
        return {
            "flow": flow["name"],
            "state": state,
            "step": step,
            "results": flow["results"]
        }
