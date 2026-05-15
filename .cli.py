import argparse
# แนะนำให้ import โมดูลของ agent, task manager หรือ handler ที่คุณมีในโปรเจกต์นี้
# เช่น from agents.task_agent import create_task

def submit_task(name, desc):
    # ตัวอย่าง: เรียกใช้เมธอด/ฟังก์ชันจาก agent/module ในโปรเจกต์คุณ
    # create_task(name, desc)
    print(f"ส่ง task: {name}")
    print(f"รายละเอียด: {desc}")
    # สามารถเติมโค้ดติดต่อ agent/module จริง ได้ที่นี่

def main():
    parser = argparse.ArgumentParser(description="Task CLI Entrypoint")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # คำสั่ง submit-task
    submit_parser = subparsers.add_parser("submit-task", help="ส่ง task ใหม")
    submit_parser.add_argument("--name", required=True, help="ชื่อของ task")
    submit_parser.add_argument("--desc", required=True, help="รายละเอียดของ task")

    args = parser.parse_args()

    if args.command == "submit-task":
        try:
            submit_task(args.name, args.desc)
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
