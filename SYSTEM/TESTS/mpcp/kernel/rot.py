# mpcp/kernel/rot.py

class MPCPRot:
    """
    ROT = กฎกลางของระบบ
    ตรวจความสัมพันธ์ (relation)
    ไม่ใช่แค่ structure
    """

    # =========================
    # CORE LAW
    # =========================
    @staticmethod
    def validate_core(event: dict, result: dict):
        """
        CAUSE → ACTION → RESULT

        event = cause
        result = outcome (must traceable)
        """

        # CAUSE
        if not isinstance(event, dict):
            raise ValueError("Invalid event (not dict)")

        if "TASK" not in event:
            raise ValueError("ROT_FAIL: NO_CAUSE (missing TASK)")

        # RESULT
        if not isinstance(result, dict):
            raise ValueError("ROT_FAIL: INVALID_RESULT")

        # ACTION TRACE (ขั้นต่ำ)
        if "state" not in result:
            raise ValueError("ROT_FAIL: NO_RESULT_STATE")

        return True

    # =========================
    # TRACE LAW (optional strict)
    # =========================
    @staticmethod
    def validate_trace(result: dict):
        """
        ตรวจ trace ลึกขึ้น (ใช้ตอนอยาก strict)
        """

        if "cause" not in result:
            raise ValueError("ROT_FAIL: MISSING_CAUSE_TRACE")

        if "action" not in result:
            raise ValueError("ROT_FAIL: MISSING_ACTION_TRACE")

        return True

    # =========================
    # BOUNDARY LAW (basic)
    # =========================
    @staticmethod
    def validate_boundary(event: dict):
        """
        ต้องมี scope หรือ context บางอย่าง
        (กัน event ลอย)
        """

        # อย่างน้อยต้องมีอะไรนอกจาก TASK
        if len(event.keys()) <= 1:
            raise ValueError("ROT_FAIL: NO_CONTEXT")

        return True

    # =========================
    # FAIL CONDITION CHECK
    # =========================
    @staticmethod
    def validate_fail_condition(event: dict, result: dict):
        """
        ใช้ detect system invalid state
        """

        if not result:
            raise ValueError("ROT_FAIL: EMPTY_RESULT")

        if "state" in result and result["state"] == "STOP":
            return True  # STOP = valid behavior

        return True
