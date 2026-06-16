# mpcp/kernel/contract.py

from mpcp.kernel.system import SYSTEM_NAME


# All runtime states allowed by spec (MODEW_PAPER + MPCP_RUNTIME_SANITY_SWEEP_v2)
VALID_STATES = frozenset({
    # Terminal / execution-result states
    "SUCCESS", "STOP",
    # Suspension state
    "WAIT", "wait",
    # Modew lifecycle states
    "idle", "ready", "run", "done", "warn", "block", "fail",
})

HALT_STATES = frozenset({"STOP", "fail", "block"})
PAPER_COMMAND_REQUIRED = frozenset({"TASK", "INTENT", "SCOPE", "BOUNDARY"})
RESULT_ENVELOPE_REQUIRED = frozenset({"schema", "state", "cause", "action", "result", "law", "restore", "meta"})


class MPCPContract:
    """
    Contract = ตรวจโครงขั้นต่ำของระบบ (ไม่ใช่ logic)
    - เช็ค input format
    - เช็ค key สำคัญ
    - ไม่ตีความภาษา / synonym / shorthand

    หมายเหตุ:
    - language conversion เป็นหน้าที่ W3Lgu / Paper normalizer
    - ROT เป็นคนตรวจ relation และ boundary ที่ลึกกว่า contract
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
        ตรวจ input ระดับ contract แบบ backward-compatible
        - ต้องเป็น dict
        - ต้องมี TASK
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be dict (mpcp format required)")

        if "TASK" not in data:
            raise ValueError("Missing TASK")

        if not isinstance(data["TASK"], str):
            raise ValueError("TASK must be string")

        if not data["TASK"].strip():
            raise ValueError("TASK is empty")

        return True

    @staticmethod
    def validate_paper_command(data: dict):
        """
        ตรวจคำสั่งงานสั้นจาก Paper หลัง normalize แล้ว

        Required:
        - TASK
        - INTENT
        - SCOPE
        - BOUNDARY

        จุดนี้ไม่แปลภาษาและไม่เดา key ให้ เพื่อกันการตีความผิด
        """
        if not isinstance(data, dict):
            raise ValueError("Paper command must be dict")

        missing = sorted(PAPER_COMMAND_REQUIRED - set(data.keys()))
        if missing:
            raise ValueError(f"Missing paper command keys: {','.join(missing)}")

        for key in PAPER_COMMAND_REQUIRED:
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f"{key} must be non-empty string")

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
        - halt state ต้องมี error field
        """
        if not isinstance(result, dict):
            raise ValueError("Result must be dict")

        if "state" not in result:
            raise ValueError("Missing state in result")

        if result["state"] not in VALID_STATES:
            raise ValueError(f"Invalid state: {result['state']}")

        if result["state"] in HALT_STATES and "error" not in result:
            raise ValueError(f"State '{result['state']}' requires 'error' field")

        return True

    @staticmethod
    def validate_result_envelope(result: dict, *, strict: bool = False):
        """
        ตรวจ canonical MPCP result envelope

        strict=False: ตรวจขั้นต่ำเหมือน validate_output
        strict=True : ต้องมี schema/state/cause/action/result/law/restore/meta
        """
        MPCPContract.validate_output(result)

        if not strict:
            return True

        missing = sorted(RESULT_ENVELOPE_REQUIRED - set(result.keys()))
        if missing:
            raise ValueError(f"Missing result envelope keys: {','.join(missing)}")

        schema = result.get("schema")
        if not isinstance(schema, str) or not schema.startswith("mpcp.result."):
            raise ValueError("Result schema must start with 'mpcp.result.'")

        for key in ("law", "restore", "meta"):
            if not isinstance(result.get(key), dict):
                raise ValueError(f"{key} must be dict")

        return True
