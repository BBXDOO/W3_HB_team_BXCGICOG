"""
PSP2 (Pointer Stamp) — สถานีขนส่งพัสดุดิจิทัล

หัวใจ: รับ package -> ประทับตรา PX -> ส่งต่อผ่าน Nodes
ไม่ตรวจสอบเนื้อหา, ไม่แก้ไข payload, ไม่ infer
ออกแบบเผื่อ cross-system และ WHUB ในอนาคต

Event Chain: REDR -> PSP2 -> DTML -> LRC2
"""

from __future__ import annotations

from typing import Any, Dict
from .base import RuntimeAgent
from ..w3lgu_mfc_logic.psp2_mfc_logic import generate_px_stamp, resolve_node


class PSP2Agent(RuntimeAgent):
    module_name = "PSP2"
    action_label = "stamped and forwarded"
    mpcp_role = "pointer_stamp"
    mpcp_concepts = [
        "pointer", "stamp", "forward", "node",
        "dispatch", "px", "no_mutation", "cross_system",
        "ni", "no",
    ]

    # ------------------------------------------------------------------
    # PSP2 specific API
    # ------------------------------------------------------------------

    @staticmethod
    def stamp(package: Dict[str, Any], system_id: str = "") -> str:
        """สร้าง PX stamp จากพิกัด package

        ไม่แก้ไข package เดิม, ไม่ inspect เนื้อหา
        """
        px = package.get("_px", "")
        if not px:
            px = generate_px_stamp(package, system_id)
        return px

    @staticmethod
    def _select_node(package: Dict[str, Any]) -> str:
        """เลือก node ปลายทางจากข้อมูลใน package

        ถ้ามี 'to' ใช้ resolve node ตามนั้น
        ถ้าไม่มี ส่งไป LRC2 ตาม Event Chain ปกติ
        """
        target = package.get("to", "LRC2")
        return resolve_node(target)

    # ------------------------------------------------------------------
    # RuntimeAgent interface
    # ------------------------------------------------------------------

    def run(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        """รับ task -> stamp -> forward -> สรุปผล"""
        package = plan.get("package", {})
        system_id = context.get("system_id", "")
        px_stamp = self.stamp(package, system_id)
        node = self._select_node(package)

        return (
            f"{self.module_name} ({self.mpcp_role}) "
            f"{self.action_label} | "
            f"task: {task} | "
            f"stamp: {px_stamp} | "
            f"via: {node} | "
            f"mutated: False"
        )

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Return structured result สำหรับ cross-system chain"""
        package = plan.get("package", {})
        system_id = context.get("system_id", "")
        px_stamp = self.stamp(package, system_id)
        node = self._select_node(package)

        return {
            "contract_version": "1.0",
            "module": self.module_name,
            "status": "DISPATCHED",
            "task": task,
            "action": "stamp_and_forward",
            "stamp": px_stamp,
            "node": node,
            "mutated": False,
            "traceable": True,
            "package_id": package.get("package_id", "UNKNOWN"),
            "summary": (
                f"PSP2 stamped {px_stamp} and forwarded via {node}"
            ),
            "artifacts": [{"type": "stamp", "value": px_stamp}],
            "review": False,
        }


__all__ = ["PSP2Agent"]
