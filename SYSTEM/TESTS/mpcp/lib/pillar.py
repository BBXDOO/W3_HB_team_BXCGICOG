class Pillar:
    def __init__(self, name):
        self.name = name
        self.stages = {k: None for k in ["A", "B", "C", "D", "E", "F"]}
        self.context = {}
        self.output = None

    def set_stage(self, stage, fn):
        if stage not in self.stages:
            raise ValueError(f"Invalid stage: {stage}")
        self.stages[stage] = fn

    def set_context(self, key, value):
        self.context[key] = value

    def run(self):
        result = None

        for stage in ["A", "B", "C", "D", "E", "F"]:
            fn = self.stages.get(stage)

            if fn:
                result = fn(result, self.context)

        self.output = result
        return result
