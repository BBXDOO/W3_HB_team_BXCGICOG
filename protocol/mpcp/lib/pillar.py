class Pillar:
    VALID_STATES = {"SUCCESS", "WAIT", "STOP"}

    def __init__(self, name):
        self.name = name

        self.stages = {
            "A": None,
            "B": None,
            "C": None,
            "D": None,
            "E": None,
            "F": None,
        }

        self.context = {}
        self.output = None

    # =========================
    # Stage Registration
    # =========================
    def set_stage(self, stage, fn):
        if stage not in self.stages:
            raise ValueError(f"Invalid stage: {stage}")

        if not callable(fn):
            raise TypeError(f"Stage {stage} must be callable")

        self.stages[stage] = fn

    # =========================
    # Context
    # =========================
    def set_context(self, key, value):
        self.context[key] = value

    def get_context(self, key, default=None):
        return self.context.get(key, default)

    # =========================
    # Core Execution
    # =========================
    def run(self):
        result = None

        for stage_name in ["A", "B", "C", "D", "E", "F"]:
            fn = self.stages.get(stage_name)

            if not callable(fn):
                continue

            try:
                result = fn(result, self.context)

            except Exception as e:
                return self._stop(stage_name, f"exception: {str(e)}")

            # -------------------------
            # VALIDATION
            # -------------------------
            if not isinstance(result, dict):
                return self._stop(stage_name, "invalid result type")

            state = result.get("state")

            if state not in self.VALID_STATES:
                return self._stop(stage_name, f"invalid state: {state}")

            # -------------------------
            # TRACE (mpcp format)
            # -------------------------
            print(f"MODEW:{self.name},STAGE:{stage_name},STATE:{state}")

            # -------------------------
            # CONTROL FLOW
            # -------------------------
            if state in ["STOP", "WAIT"]:
                self.output = result
                return result

        # -------------------------
        # FINAL
        # -------------------------
        if result is None:
            return self._stop("F", "empty result")

        self.output = result
        return result

    # =========================
    # INTERNAL
    # =========================
    def _stop(self, stage, error):
        return {
            "state": "STOP",
            "stage": stage,
            "error": error
        }
