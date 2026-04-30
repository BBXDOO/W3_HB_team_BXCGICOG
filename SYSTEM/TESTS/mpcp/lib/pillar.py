class Pillar:
    ORDER = ["A", "B", "C", "D", "E", "F"]

    def __init__(self, name):
        self.name = name
        self.stages = {k: None for k in self.ORDER}
        self.context = {}
        self.output = None

    def set_stage(self, stage, fn):
        if stage not in self.stages:
            raise ValueError(f"Invalid stage: {stage}")
        if not callable(fn):
            raise ValueError(f"Stage {stage} must be callable")
        self.stages[stage] = fn

    def run(self, context):
        self.context = context
        result = None

        for s in self.ORDER:
            fn = self.stages[s]

            if fn is None:
                continue

            try:
                result = fn(result, self.context)

            except Exception as e:
                raise RuntimeError(
                    f"[MPCP][{self.name}] Stage {s} failed: {e}"
                )

        self.output = result
        return result
