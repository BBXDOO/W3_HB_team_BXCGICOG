# mpcp/kernel/contract.py

SYSTEM_NAME = "mpcp"


class MPCPContract:
    """
    Contract = ตรวจโครงขั้นต่ำของระบบ (ไม่ใช่ logic)
    - เช็ค input format
    - เช็ค key สำคัญ
    - ไม่ตีความ
    """

    # =========================
    # SYSTEM CHECK
    # =========================
    @staticmethod
    def assert_system(name: str):
        if name != SYSTEM_NAME:
            raise ValueError(f"Invalid system name: {name}")

    # =========================
    # INPUT VALIDATION
    # =========================
    @staticmethod
    def validate_input(data: dict):
        """
        ตรวจ input ระดับ contract
        - ต้องเป็น dict
        - ต้องมี TASK
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be dict (mpcp format required)")

        if "TASK" not in data:
            raise ValueError("Missing TASK")

        if not isinstance(data["TASK"], str):
            raise ValueError("TASK must be string")

        # ห้ามว่าง
        if not data["TASK"].strip():
            raise ValueError("TASK is empty")

        return True

    # =========================
    # OUTPUT VALIDATION
    # =========================
    @staticmethod
    def validate_output(result: dict):
        """
        ตรวจ output ขั้นต่ำ
        - ต้องเป็น dict
        - ต้องมี state
        """
        if not isinstance(result, dict):
            raise ValueError("Result must be dict")

        if "state" not in result:
            raise ValueError("Missing state in result")

        if result["state"] not in ["SUCCESS", "WAIT", "STOP"]:
            raise ValueError(f"Invalid state: {result['state']}")

        return True
