from typing import Dict, Any, List, Optional
import json
from pathlib import Path

from .base import RuntimeAgent
from .mpcp_reader import scan_terms, MPCP_CORE_TERMS


class DeepSeekAgent(RuntimeAgent):
    module_name = "DeepSeek"
    action_label = "completed structure planning"

    # W3 ecosystem role: scale / long-term planning (module.json role)
    mpcp_role = "planning"
    mpcp_concepts = ["scale", "planning", "long-term", "structure", "logic", "audit"]

    # ------------------------------------------------------------
    # 1. inspect_mpcp — ตรวจจับ concept terms ในเอกสาร (เดิม)
    # ------------------------------------------------------------
    def inspect_mpcp(self, doc_text: str) -> List[str]:
        if not self.mpcp_concepts:
            return []
        terms_set = frozenset(self.mpcp_concepts)
        return scan_terms(doc_text, terms_set)

    # ------------------------------------------------------------
    # 2. run — สรุปงานแบบมนุษย์อ่านเข้าใจ
    # ------------------------------------------------------------
    def run(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        role = plan.get("role", "—")
        responsibilities = self._responsibilities(plan)
        main_duty = responsibilities[0] if responsibilities else "execute assigned task"
        experience = self._experience_summary(task, context)

        target = context.get("target") or context.get("request", {}).get("target") or "W3"

        # เพิ่มข้อมูล BOX / CROLL ถ้ามี
        box_hint = ""
        if "box_suggestion" in context:
            box_hint = f" | box_suggestion: {context['box_suggestion']}"

        return (
            f"{self.module_name} ({role}) {self.action_label}: {task} | "
            f"target: {target} | duty: {main_duty} | experience: {experience}{box_hint}"
        )

    # ------------------------------------------------------------
    # 3. execute — ทำงานแบบ planner‑only ผ่าน BOX + CROLL
    # ------------------------------------------------------------
    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        DeepSeek execute — ใช้ BOX และ CROLL เพื่อสร้างแผนงาน (planner‑only)
        ไม่มีการ execute จริง, ไม่ mutate, ไม่เขียนไฟล์
        """
        # 1. พยายามหา PX จาก task หรือ context
        px = self._extract_px(task, context)

        # 2. ถ้ามี PX → ลองใช้ BOX + CROLL
        if px:
            box_result = self._consult_box(px)
            if box_result:
                return self._build_plan_response(
                    task=task,
                    px=px,
                    box_result=box_result,
                    status="PLANNED",
                    summary=f"Plan created for PX:{px} (planner‑only, no execution)",
                )

        # 3. ถ้าไม่มี PX หรือ BOX ไม่ตอบ → สร้างแผนทั่วไป (fallback)
        return self._build_fallback_response(task, plan, context)

    # ------------------------------------------------------------
    # 4. Helper: แยก PX จาก task / context
    # ------------------------------------------------------------
    def _extract_px(self, task: str, context: Dict[str, Any]) -> Optional[str]:
        # ตรวจจาก context ก่อน
        if "px" in context:
            return str(context["px"])
        if "PX" in context:
            return str(context["PX"])

        # ตรวจจาก task string
        import re
        match = re.search(r"(?:PX:?)?\s*\[?([0-9]+\s*,\s*[0-9]+)\]?", task)
        if match:
            return match.group(1).replace(" ", "")

        return None

    # ------------------------------------------------------------
    # 5. Helper: เรียก BOX / CROLL (planner‑only)
    # ------------------------------------------------------------
    def _consult_box(self, px: str) -> Optional[Dict[str, Any]]:
        """เรียก CROSS‑L Dispatcher แบบ planner‑only (ไม่ execute)"""
        try:
            # พยายามใช้ croll.cross_l_dispatcher
            from croll.cross_l_dispatcher import dispatch_workset
            result = dispatch_workset(px, enable_box_suggestion=True)
            return result
        except ImportError:
            # fallback: ลองอ่าน BOX registry โดยตรง
            return self._read_box_registry(px)
        except Exception as e:
            return {"error": str(e), "px": px}

    def _read_box_registry(self, px: str) -> Optional[Dict[str, Any]]:
        """อ่าน BOX registry โดยตรง (ถ้า CROLL ยังไม่พร้อม)"""
        reg_path = Path("wx/registry/template_registry.json")
        if not reg_path.exists():
            return None
        try:
            with open(reg_path) as f:
                data = json.load(f)
            for tmpl in data.get("templates", []):
                if px in tmpl.get("px", []):
                    return {
                        "found": True,
                        "template_id": tmpl.get("template_id"),
                        "path": tmpl.get("path"),
                        "work_type": tmpl.get("work_type"),
                        "rytm": tmpl.get("rytm"),
                        "boundary": tmpl.get("boundary"),
                        "deny": tmpl.get("deny", []),
                        "source": "box_registry",
                    }
        except Exception:
            pass
        return None

    # ------------------------------------------------------------
    # 6. Helper: สร้าง response แบบ PLANNED
    # ------------------------------------------------------------
    def _build_plan_response(
        self,
        task: str,
        px: str,
        box_result: Dict[str, Any],
        status: str = "PLANNED",
        summary: str = "",
    ) -> Dict[str, Any]:
        """สร้าง response ที่ปลอดภัย (planner‑only, ไม่ mutate)"""
        return {
            "contract_version": "1.0",
            "status": status,
            "module": self.module_name,
            "task": task,
            "px": px,
            "action": "plan_created",
            "summary": summary,
            "plan": box_result,
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,  # ต้อง review ก่อน execute จริง
            "execution_allowed": False,
            "planner_only": True,
        }

    # ------------------------------------------------------------
    # 7. Helper: fallback (เมื่อไม่มี PX หรือ BOX ไม่ตอบ)
    # ------------------------------------------------------------
    def _build_fallback_response(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """fallback เมื่อไม่มี PX หรือ BOX ไม่ตอบ"""
        return {
            "contract_version": "1.0",
            "status": "REVIEW",
            "module": self.module_name,
            "task": task,
            "action": "planning_required",
            "summary": (
                f"{self.module_name} needs a PX to create a structured plan. "
                "Please provide PX (e.g., '1,1') in task or context."
            ),
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,
            "execution_allowed": False,
            "planner_only": True,
        }
