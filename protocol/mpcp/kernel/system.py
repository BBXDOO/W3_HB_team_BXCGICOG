# mpcp/kernel/system.py

SYSTEM_NAME = "mpcp"


def assert_system(name: str):
    """
    ตรวจว่าเป็นระบบ MPCP จริง
    ใช้กันของแปลก / cross-system input
    """
    if not isinstance(name, str):
        raise ValueError("System name must be string")

    if name.strip().lower() != SYSTEM_NAME:
        raise ValueError(f"Invalid system name: {name}")

    return True


def validate_system_context(data: dict):
    """
    ตรวจ context ระดับระบบ
    - ไม่บังคับว่าต้องมี SYSTEM
    - แต่ถ้ามี ต้องถูกต้อง
    """

    if not isinstance(data, dict):
        raise ValueError("System context must be dict")

    # optional field
    system_name = data.get("SYSTEM")

    if system_name:
        assert_system(system_name)

    return True
