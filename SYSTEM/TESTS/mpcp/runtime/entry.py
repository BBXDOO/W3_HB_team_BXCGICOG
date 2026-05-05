from mpcp.runtime.executor import run, register


class DesignModew:
    def __init__(self):
        self.ctx = {}

    def set_context(self, k, v):
        self.ctx[k] = v

    def run(self):
        return {
            "state": "SUCCESS",
            "result": "design_done"
        }


# bind TASK -> MODEW
register("design", DesignModew)


if __name__ == "__main__":
    result = run("TASK:design")
    print(result)
