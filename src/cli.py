import argparse

def submit_task(name, desc):
    # สามารถปรับฟังก์ชันนี้ให้บันทึกหรือส่งงานไปยังระบบจริง
    print(f"Submit task: {name}")
    print(f"Description: {desc}")

def main():
    parser = argparse.ArgumentParser(description="Task CLI Entrypoint")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser("submit-task", help="ส่ง task ใหม่")
    submit_parser.add_argument("--name", required=True, help="ชื่อของ task")
    submit_parser.add_argument("--desc", required=True, help="รายละเอียดของ task")

    args = parser.parse_args()
    if args.command == "submit-task":
        submit_task(args.name, args.desc)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
