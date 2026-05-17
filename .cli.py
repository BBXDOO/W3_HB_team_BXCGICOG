import argparse
from agents.task_agent import create_task   # โมดูลจริงที่คุณต้องมีในโปรเจกต์

def submit_task(name, desc):
    try:
        task_id = create_task(name, desc)   # เรียกใช้ฟังก์ชันจาก agent/module จริง
        print(f"✅ ส่ง task สำเร็จ: {task_id}")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการส่ง task: {e}")

def main():
    parser = argparse.ArgumentParser(description="Task CLI Entrypoint")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # คำสั่ง submit-task
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
