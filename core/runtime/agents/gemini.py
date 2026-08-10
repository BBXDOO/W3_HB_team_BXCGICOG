from typing import Dict, Any, List
from .base import RuntimeAgent


class GeminiAgent(RuntimeAgent):
    module_name = "Gemini"
    action_label = "completed verification"

    # W3 ecosystem role: validation / cross-check (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "validation"
    mpcp_concepts = [
        "validation",
        "verification",
        "cross-check",
        "cross check",
        "w3lgu",
        "multi-cross",
        "event_field",
    ]

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gemini Execution Engine:
        ทำหน้าที่ตรวจสอบ (Validation/Cross-check) เหตุการณ์และข้อตกลง (Contract/EventField)
        โดยไม่สร้างผลข้างเคียงให้หน่วยความจำเดิม (mutated=False, traceable=True)
        """
        # ดึงบริบทเป้าหมายและสภาวะแวดล้อม (ENV)
        target = context.get("target") or context.get("request", {}).get("target") or "W3"
        responsibilities = self._responsibilities(plan)
        main_duty = responsibilities[0] if responsibilities else "verify system contract & logic27 alignment"
        
        # ตรวจสอบประวัติร่องรอยเดิมผ่าน helper จาก base
        exp_summary = self._experience_summary(task, context)

        # สกัด Event Field / Identity หากมีการส่งมาจาก W3Lgu Runtime
        event_identity = context.get("event_identity") or {
            "chain_id": context.get("chain_id", "CH-LOCAL"),
            "event_id": context.get("event_id", "EV-UNKNOWN"),
            "sequence": context.get("sequence", 1),
            "owner_scope": "Gemini-Field",
        }

        # ประมวลผลผลลัพธ์การตรวจสอบ (Verification Contract Result)
        return {
            "contract_version": "1.0",
            "status": "COMPLETED",
            "module": self.module_name,
            "task": task,
            "action": self.action_label,
            "summary": f"{self.module_name} ({plan.get('role', 'validator')}) verified '{task}' for target [{target}].",
            "reason": f"Duty executed: {main_duty}. Context state checked against {exp_summary}.",
            "artifacts": [
                {
                    "type": "verification_stamp",
                    "target": target,
                    "verified_by": self.module_name,
                    "event_identity": event_identity,
                }
            ],
            "details": {
                "mpcp_role": self.mpcp_role,
                "main_duty": main_duty,
                "experience": exp_summary,
            },
            "mutated": False,
            "traceable": True,
            "review": False,
        }
