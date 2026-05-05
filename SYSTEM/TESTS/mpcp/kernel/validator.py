# mpcp/kernel/validator.py

from mpcp.kernel.contract import MPCPContract
from mpcp.kernel.system import validate_system_context
from mpcp.kernel.rot import MPCPRot


class MPCPValidator:

    # =========================
    # INPUT VALIDATION
    # =========================
    @staticmethod
    def validate_input(data: dict):
        # system (optional)
        validate_system_context(data)

        # contract (structure)
        MPCPContract.validate_input(data)

        # rot (boundary)
        MPCPRot.validate_boundary(data)

        return True

    # =========================
    # OUTPUT VALIDATION
    # =========================
    @staticmethod
    def validate_output(data: dict, result: dict):
        # contract (result structure)
        MPCPContract.validate_output(result)

        # rot (core law)
        MPCPRot.validate_core(data, result)

        # optional trace (เปิดใช้ทีหลังได้)
        # MPCPRot.validate_trace(result)

        # fail condition
        MPCPRot.validate_fail_condition(data, result)

        return True
