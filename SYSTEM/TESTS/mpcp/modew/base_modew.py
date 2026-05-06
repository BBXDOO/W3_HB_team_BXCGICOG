# mpcp/modew/base_modew.py

class BaseModew:
    """
    Base Modew (Pillar)
    Implements A–F execution flow aligned with MPCP + ROT
    """

    def __init__(self):
        self.context = {}
        self.trace = []

    # =========================
    # CONTEXT
    # =========================
    def set_context(self, key, value):
        self.context[key] = value

    # =========================
    # TRACE (ENV PRESERVE)
    # =========================
    def log(self, stage, data):
        self.trace.append({
            "stage": stage,
            "data": data,
            "env": dict(self.context)  # no reduction (ENV LAW)
        })

    # =========================
    # A–F PIPELINE
    # =========================
    def run(self):
        """
        Execute the A–F pillar pipeline.

        Prerequisites: call set_context("TASK", ...) before run() so that
        'cause' is captured correctly for CAUSE→ACTION→RESULT traceability.
        """
        cause = self.context.get("TASK")
        try:
            a = self.stage_A_input()
            self.log("A", a)

            b = self.stage_B_validate(a)
            self.log("B", b)

            c = self.stage_C_route(b)
            self.log("C", c)

            d = self.stage_D_process(c)
            self.log("D", d)

            e = self.stage_E_transition(d)
            self.log("E", e)

            f = self.stage_F_output(e)
            self.log("F", f)

            # CAUSE → ACTION → RESULT: include cause so trace is complete
            return {
                "state": "SUCCESS",
                "cause": cause,
                "result": f,
                "trace": self.trace,
            }

        except Exception as e:
            return {
                "state": "STOP",
                "cause": cause,
                "error": str(e),
                "trace": self.trace,
            }

    # =========================
    # STAGES (OVERRIDE REQUIRED)
    # =========================
    def stage_A_input(self):
        return self.context

    def stage_B_validate(self, data):
        return data

    def stage_C_route(self, data):
        return data

    def stage_D_process(self, data):
        return data

    def stage_E_transition(self, data):
        return data

    def stage_F_output(self, data):
        return data
