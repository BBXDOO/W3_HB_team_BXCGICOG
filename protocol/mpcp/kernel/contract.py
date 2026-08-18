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

HALT_STATES = frozenset({"STOP", "fail", "block"})
PAPER_COMMAND_REQUIRED = frozenset({"TASK", "INTENT", "SCOPE", "BOUNDARY"})
RESULT_ENVELOPE_REQUIRED = frozenset({
    "schema", "state", "cause", "action", "modew", "result", "trace",
    "env", "law", "restore", "meta",
})


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
    def build_result_envelope(
        result: dict,
        *,
        cause=None,
        action: str,
        modew: str,
        role: str = "default",
        env_before: dict | None = None,
    ) -> dict:
        """Normalize a Modew result into the canonical MPCP return envelope."""
        if not isinstance(result, dict):
            raise ValueError("Result must be dict")
        if str(result.get("schema", "")).startswith("mpcp.result."):
            return dict(result)

        state = result.get("state")
        before = dict(env_before or {})
        after_value = result.get("env_after", before)
        after = dict(after_value) if isinstance(after_value, dict) else before
        changed = sorted(
            key for key in set(before) | set(after)
            if before.get(key) != after.get(key)
        )
        source_truth_mutated = bool(result.get("source_truth_mutated", False))
        env_mutated = bool(result.get("env_mutated", bool(changed)))
        event_container_mutated = bool(result.get("event_container_mutated", False))
        mutated = bool(
            result.get("mutated", False)
            or source_truth_mutated
            or env_mutated
            or event_container_mutated
        )
        error = result.get("error")
        envelope = {
            "schema": "mpcp.result.1",
            "state": state,
            "cause": result.get("cause", cause),
            "action": result.get("action", action),
            "modew": result.get("modew", modew),
            "role": result.get("role", role),
            "result": result.get("result"),
            "reason": result.get("reason") or error or "modew_return",
            "trace": list(result.get("trace", [])),
            "mutated": mutated,
            "source_truth_mutated": source_truth_mutated,
            "env_mutated": env_mutated,
            "event_container_mutated": event_container_mutated,
            "review": bool(result.get("review", False)),
            "env": {
                "before": before,
                "after": after,
                "delta_keys": changed,
                "preserved": not changed,
            },
            "law": {
                "validated": False,
                "validator": "ROT:MPCP",
                "blocked_by": None,
            },
            "restore": {
                "required": source_truth_mutated or env_mutated,
                "supported": bool(result.get("restore_token")),
                "token": result.get("restore_token"),
                "state_preserved": not changed,
            },
            "meta": {
                "return_code": 0 if state in {"SUCCESS", "done"} else 1,
                "format": "dict",
                "version": 1,
                "source_result_keys": sorted(str(key) for key in result),
            },
        }
        if error is not None:
            envelope["error"] = error
        if "semantic_layers" in result:
            envelope["semantic_layers"] = dict(result["semantic_layers"])
        return envelope

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

        if not isinstance(result.get("trace"), list):
            raise ValueError("trace must be list")
        if not isinstance(result.get("env"), dict):
            raise ValueError("env must be dict")
        for key in ("action", "modew"):
            if not isinstance(result.get(key), str) or not result[key].strip():
                raise ValueError(f"{key} must be non-empty string")

        return True
