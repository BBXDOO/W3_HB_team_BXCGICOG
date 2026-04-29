SYSTEM_NAME = "MPCP"

def assert_system(name: str):
    if name != SYSTEM_NAME:
        raise ValueError(f"Invalid system name: {name}")
