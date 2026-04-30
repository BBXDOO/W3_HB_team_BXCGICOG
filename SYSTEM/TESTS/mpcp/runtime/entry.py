from mpcp.runtime.executor import MPCPExecutor


def execute(task: str):
    executor = MPCPExecutor()
    return executor.run(task)


if __name__ == "__main__":
    print(execute("design"))
