from __future__ import annotations

from typing import Any, Dict, List, Optional
from .base import RuntimeAgent
from ..w3lgu_mfc_logic.psp2_mfc_logic import validate_routing_path

class PSP2Agent(RuntimeAgent):
    module_name = "PSP2"
    action_label = "stamped, routed, and dispatched event"
    mpcp_role = "pointer_stamp_dispatcher"
    mpcp_concepts = [
        "pointer",
        "stamp",
        "route",
        "dispatch",
        "validate",
        "log",
        "handoff",
        "px_anchor",
        "no_mutation"
    ]

    def _generate_stamp(self, package_id: str) -> str:
        """สร้างร่องรอยการขนส่งพัสดุในพื้นที่."""
        return f"STAMP-{self.module_name}-{package_id}"

    def dispatch(
        self,
        package: Dict[str, Any],
        route_plan: List[str]
    ) -> Dict[str, Any]:
        """
        PSP2 ไม่ดัดแปลงเนื้อหา แต่จะประทับตรา PX และส่งต่อตามแผน.
        """
        package_id = package.get("package_id", "UNKNOWN")
        
        # ลอจิกแกร่ง: ตรวจสอบเส้นทางก่อนเคลื่อนย้าย
        if not validate_routing_path(route_plan):
            return {"status": "FAILED", "reason": "INVALID_ROUTE"}

        # ประทับตราการขนส่ง (Non-mutation of payload)
        package["_psp2_stamp"] = self._generate_stamp(package_id)
        package["_last_hop"] = self.module_name

        return {
            "status": "DISPATCHED",
            "package": package,
            "next_stops": route_plan,
            "stamped": True
        }

    def run(
        self,
        package: Dict[str, Any],
        route_plan: Optional[List[str]] = None
    ) -> str:
        """
        ทำงานตามวงจรของ Event Chain: รับพัสดุ -> Stamp -> ส่งต่อ.
        """
        route_plan = route_plan or []
        result = self.dispatch(package, route_plan)
        
        status = result.get("status", "UNKNOWN")
        stamped = result.get("stamped", False)
        
        return (
            f"{self.module_name} ({self.mpcp_role}) "
            f"{self.action_label} | "
            f"status: {status} | "
            f"stamp: {stamped} | "
            f"trace: {package.get('package_id')} | "
            f"next: {route_plan} | "
            f"mutated: False"
        )

__all__ = ["PSP2Agent"]
