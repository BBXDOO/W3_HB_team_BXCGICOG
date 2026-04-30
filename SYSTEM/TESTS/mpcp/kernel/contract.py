class MPCPContract:

    @staticmethod
    def validate_input(task):
        if not isinstance(task, str):
            raise ValueError("Task must be string")

    @staticmethod
    def validate_output(result):
        if result is None:
            raise ValueError("Empty result")
