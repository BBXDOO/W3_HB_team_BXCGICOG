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

    def set_stage(self, stage, value):
        if stage in self.stages:
            self.stages[stage] = value

    def set_context(self, key, value):
        self.context[key] = value

    def run(self):
        # simple flow A → F
        result = None
        for s in ["A", "B", "C", "D", "E", "F"]:
            fn = self.stages.get(s)
            if callable(fn):
                result = fn(result, self.context)

        self.output = result
        return result
