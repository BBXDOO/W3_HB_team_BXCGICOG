"""Reusable MPCP flow composition without import-time execution."""

from .manager import MPCPManager


def build_manager(flow_name: str, steps: list[str]) -> MPCPManager:
    manager = MPCPManager()
    manager.add_flow(flow_name, list(steps))
    return manager
