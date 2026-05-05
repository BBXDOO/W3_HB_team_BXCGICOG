class BaseModew:
    def __init__(self):
        self.context = {}

    def set_context(self, k, v):
        self.context[k] = v

    def check_scope(self, key):
        scope = self.context.get("INCLUDE", "")
        allowed = set(scope.split(","))
        return key in allowed

    def run(self):
        raise NotImplementedError
