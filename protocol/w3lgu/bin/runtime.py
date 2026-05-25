# W3Lgu Runtime Engine v1.0
import os

def boot_system():
    print("--- [G-State: ACTIVE] ---")
    print("W3Lgu Runtime is initializing...")
    # ตรวจสอบการเชื่อมต่อกับ Node อื่นๆ
    nodes = ['adapters', 'signals', 'memory']
    for node in nodes:
        path = f"../{node}"
        status = "FOUND" if os.path.exists(path) else "MISSING"
        print(f"Node {node.upper()}: {status}")

if __name__ == "__main__":
    boot_system()

