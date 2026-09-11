"""Command-line entry point for adding tasks to the W3 task queue."""

import argparse
import sys
from typing import Any, Dict

from agents_externalagents.task_agent import create_task


def non_empty(value: str) -> str:
    """Return a trimmed CLI value, rejecting empty input."""
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("must not be empty")
    return value


def submit_task(name: str, desc: str, agent: str, module: str) -> int:
    """Create one queued task and return a process exit code."""
    try:
        task: Dict[str, Any] = create_task(
            name,
            desc,
            agent=agent,
            module=module,
        )
        if not isinstance(task, dict) or not task.get("task_id"):
            raise RuntimeError("task agent returned no task_id")
    except Exception as exc:
        print(f"❌ สร้าง task ไม่สำเร็จ: {exc}", file=sys.stderr)
        return 1

    print(f"✅ สร้าง task เข้าคิวแล้ว: {task['task_id']}")
    print(f"   Agent: {task.get('agent', agent)} | Module: {task.get('module', module)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the parser separately so its contract can be tested."""
    parser = argparse.ArgumentParser(description="W3 Task CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser(
        "submit-task",
        help="สร้าง task ใหม่เข้าคิว",
    )
    submit_parser.add_argument("--name", required=True, type=non_empty, help="ชื่อ task")
    submit_parser.add_argument("--desc", required=True, type=non_empty, help="รายละเอียด task")
    submit_parser.add_argument("--agent", default="copilot-gm", type=non_empty)
    submit_parser.add_argument("--module", default="W3Lgu", type=non_empty)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "submit-task":
        return submit_task(args.name, args.desc, args.agent, args.module)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
