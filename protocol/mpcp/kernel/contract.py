# mpcp/kernel/contract.py

from .system import SYSTEM_NAME


# All runtime states allowed by spec (MODEW_PAPER + MPCP_RUNTIME_SANITY_SWEEP_v2)
VALID_STATES = frozenset({
    # Terminal / execution-result states
    "SUCCESS", "STOP",
    # Suspension state
    "WAIT", "wait",
    # Modew lifecycle states
    "idle", "ready", "run", "done", "warn", "block", "fail",
})


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
        - ต้องมี state ที่อยู่ใน VALID_STATES
        - state 'fail' ต้องมี error field
        """
        if not isinstance(result, dict):
            raise ValueError("Result must be dict")

        if "state" not in result:
            raise ValueError("Missing state in result")

        if result["state"] not in VALID_STATES:
            raise ValueError(f"Invalid state: {result['state']}")

        # fail state ต้องมี error ระบุเหตุ
        if result["state"] == "fail" and "error" not in result:
            raise ValueError("State 'fail' requires 'error' field")

        return True
