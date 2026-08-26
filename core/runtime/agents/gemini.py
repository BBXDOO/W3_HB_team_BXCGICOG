from typing import Any, Dict, List, Mapping
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

    @staticmethod
    def _context_value(context: Mapping[str, Any], *names: str) -> Any:
        request = context.get("request") if isinstance(context.get("request"), Mapping) else {}
        payload = context.get("payload") if isinstance(context.get("payload"), Mapping) else {}
        if not payload and isinstance(request.get("payload"), Mapping):
            payload = request["payload"]
        for container in (context, payload, request):
            for name in names:
                if name in container:
                    return container[name]
        return None

    @classmethod
    def _normalize_checks(cls, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        raw_checks = cls._context_value(context, "checks", "verification")
        raw_checks = [] if raw_checks is None else raw_checks
        if isinstance(raw_checks, Mapping):
            raw_checks = [raw_checks]
        if not isinstance(raw_checks, list):
            return [{"name": "check_set", "passed": None, "state": "UNRESOLVED"}]

        checks: List[Dict[str, Any]] = []
        for index, item in enumerate(raw_checks, start=1):
            if isinstance(item, bool):
                checks.append({"name": f"check_{index}", "passed": item, "state": "PASS" if item else "FAIL"})
            elif isinstance(item, Mapping):
                passed = item.get("passed", item.get("ok"))
                if isinstance(passed, bool):
                    checks.append({"name": str(item.get("name") or f"check_{index}"), "passed": passed, "state": "PASS" if passed else "FAIL"})
                else:
                    checks.append({"name": str(item.get("name") or f"check_{index}"), "passed": None, "state": "UNRESOLVED"})
            else:
                checks.append({"name": f"check_{index}", "passed": None, "state": "UNRESOLVED"})
        return checks

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

        supplied_identity = context.get("event_identity")
        event_identity = supplied_identity or {
            "chain_id": context.get("chain_id", "CH-LOCAL"),
            "event_id": context.get("event_id", "EV-UNKNOWN"),
            "sequence": context.get("sequence", 1),
            "owner_scope": "Gemini-Field",
        }

        checks = self._normalize_checks(context)
        evidence = self._context_value(context, "evidence", "artifacts") or []
        evidence_supplied = bool(evidence)
        failed = [check["name"] for check in checks if check["state"] == "FAIL"]
        unresolved = [check["name"] for check in checks if check["state"] == "UNRESOLVED"]
        completed = bool(checks) and not failed and not unresolved and evidence_supplied
        status = "COMPLETED" if completed else "REVIEW_REQUIRED"

        # ประมวลผลผลลัพธ์การตรวจสอบ (Verification Contract Result)
        return {
            "contract_version": "1.0",
            "status": status,
            "module": self.module_name,
            "task": task,
            "action": self.action_label,
            "decision": "VERIFIED" if completed else "UNRESOLVED",
            "summary": f"{self.module_name} checked {len(checks)} explicit check(s) for [{target}]; {len(failed)} failed.",
            "reason": (
                f"Explicit checks passed with evidence. Duty: {main_duty}."
                if completed
                else "Verification remains unresolved until explicit checks and supporting evidence are supplied and pass."
            ),
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
                "checks": checks,
                "failed_checks": failed,
                "unresolved_checks": unresolved,
                "evidence_supplied": evidence_supplied,
                "identity_supplied": supplied_identity is not None,
            },
            "mutated": False,
            "traceable": True,
            "review": not completed,
        }
