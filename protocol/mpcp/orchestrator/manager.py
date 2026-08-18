from ..runtime.executor import run
from ..kernel.contract import VALID_STATES


# States that mean "continue to next step"
_CONTINUE_STATES = frozenset({"SUCCESS", "done"})
# States that mean "pause / suspend flow"
_WAIT_STATES = frozenset({"WAIT", "wait"})
# States that mean "warn but keep going"
_WARN_STATES = frozenset({"warn"})
# States that mean "halt the flow"
_HALT_STATES = frozenset({"STOP", "fail", "block"})


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

            if state not in VALID_STATES:
                return self._stop(flow, step, f"invalid state: {state}")

            # -------------------------
            # CONTROL FLOW
            # -------------------------
            if state in _HALT_STATES:
                return self._response(flow, step, state)

            if state in _WAIT_STATES:
                return self._response(flow, step, "WAIT")

            if state in _WARN_STATES:
                # continue but propagate warning flag
                flow["current"] += 1
                continue

            if state in _CONTINUE_STATES:
                flow["current"] += 1
                continue

            # Lifecycle states (idle, ready, run) are Modew *internal* states
            # and must not appear as a final step result — treat as unexpected
            # STOP so the flow halts with a traceable error rather than silently
            # continuing or looping.
            return self._stop(flow, step, f"unexpected lifecycle state: {state}")

        # -------------------------
        # DONE
        # -------------------------
        return {
            "flow": flow["name"],
            "state": "SUCCESS",
            "cause": flow["steps"][0] if flow["steps"] else None,
            "results": flow["results"],
        }

    # =========================
    # INTERNAL HELPERS
    # =========================
    def _stop(self, flow, step, error):
        return {
            "flow": flow["name"],
            "state": "STOP",
            "cause": step,
            "step": step,
            "error": error,
            "results": flow["results"],
        }

    def _response(self, flow, step, state):
        return {
            "flow": flow["name"],
            "state": state,
            "cause": step,
            "step": step,
            "results": flow["results"],
        }
