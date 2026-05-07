# Data Transport & Memory Log (DT-ML)
from datetime import datetime

def save_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open("../memory/system_logs.txt", "a") as f:
        f.write(log_entry)
    print("Log recorded to Memory Node.")

if __name__ == "__main__":
    save_log("System migration to F-Droid Termux completed.")

