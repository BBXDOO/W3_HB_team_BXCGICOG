from __future__ import annotations

from typing import Any, Dict, List, Optional
from .base import RuntimeAgent
from ..w3lgu_mfc_logic.psp2_mfc_logic import route_package

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
        payload = dict(package)
        payload["next"] = list(route_plan or payload.get("next") or [])

        routed = route_package(payload).as_dict()
        details = routed.get("details", {})
        if routed.get("status") == "REVIEW_REQUIRED":
            return {
                "status": "REVIEW_REQUIRED",
                "reason": routed.get("reason", "route requires review"),
                "package": package,
                "next_stops": routed.get("next", []),
                "stamped": False,
                "review": True,
                "details": details,
            }

        if routed.get("status") != "ACTIVE":
            return {"status": "FAILED", "reason": "INVALID_ROUTE", "details": details}

        # ประทับตราการขนส่ง (Non-mutation of payload content; wrapper metadata only)
        package["_psp2_stamp"] = self._generate_stamp(package_id)
        package["_last_hop"] = self.module_name

        return {
            "status": "DISPATCHED",
            "package": package,
            "next_stops": routed.get("next", route_plan),
            "stamped": True,
            "review": False,
            "details": details,
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
