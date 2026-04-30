from mpcp.runtime.executor import run


class MPCPManager:
    def __init__(self):
        self.jobs = []

    def add_job(self, task_name):
        self.jobs.append(task_name)

    def execute_all(self):
        results = []

        for task in self.jobs:
            result = run(task)
            results.append({
                "task": task,
                "result": result
            })

        return results
