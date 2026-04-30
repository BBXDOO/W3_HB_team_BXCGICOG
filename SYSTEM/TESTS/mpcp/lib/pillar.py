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
    # Context Management
    # =========================
    def set_context(self, key, value):
        self.context[key] = value

    def get_context(self, key, default=None):
        return self.context.get(key, default)

    # =========================
    # Core Execution Engine
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
                return {
                    "state": "STOP",
                    "color": "🔴",
                    "error": f"Stage {stage_name} exception: {str(e)}"
                }

            # -------------------------
            # Validation Layer
            # -------------------------
            if not isinstance(result, dict):
                return {
                    "state": "STOP",
                    "color": "🔴",
                    "error": f"Stage {stage_name} returned invalid type"
                }

            state = result.get("state")

            if state not in self.VALID_STATES:
                return {
                    "state": "STOP",
                    "color": "🔴",
                    "error": f"Invalid state: {state} (Stage {stage_name})"
                }

            # -------------------------
            # Trace (lightweight)
            # -------------------------
            print(f"[MPCP] {self.name} | Stage {stage_name} → {state}")

            # -------------------------
            # Control Flow
            # -------------------------
            if state == "STOP":
                self.output = result
                return result

            if state == "WAIT":
                self.output = result
                return result

        # -------------------------
        # Final Safeguard
        # -------------------------
        if result is None:
            return {
                "state": "STOP",
                "color": "🔴",
                "error": "Empty result"
            }

        self.output = result
        return result
