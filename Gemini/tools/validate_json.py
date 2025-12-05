import json
import sys

def validate_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ Valid JSON: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {file_path}\n   Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_json(sys.argv[1])
