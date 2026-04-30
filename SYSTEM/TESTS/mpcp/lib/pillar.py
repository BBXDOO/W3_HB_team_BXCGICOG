class Pillar:
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

    def set_stage(self, stage, fn):
        if stage in self.stages:
            self.stages[stage] = fn

    def run(self):
        result = None

        for stage_name in ["A", "B", "C", "D", "E", "F"]:
            fn = self.stages.get(stage_name)

            if callable(fn):
                result = fn(result, self.context)

                # 🔥 control inside engine
                if isinstance(result, dict):
                    state = result.get("state")

                    if state == "STOP":
                        return result

                    if state == "WAIT":
                        return result

        self.output = result
        return result
