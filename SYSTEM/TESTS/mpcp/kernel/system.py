SYSTEM_NAME = "mpcp"

def assert_system(name: str):
    if name != SYSTEM_NAME:
        raise ValueError(f"Invalid system name: {name}")
