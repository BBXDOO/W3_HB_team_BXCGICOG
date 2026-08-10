 from .base import RuntimeAgent
 
 
 class CopilotGmAgent(RuntimeAgent):
     module_name = "Copilot-Gm"
     action_label = "completed governance review"
     # W3 ecosystem role: governance / structural consistency (W3LGU_MPCP_ROLE_MAPPING.md §9)
     mpcp_role = "governance"
     mpcp_concepts = ["governance", "policy", "compliance", "structural consistency"]
+
+    def execute(self, task, plan, context):
+        """
+        Governance executor (minimum viable contract):
+        - inspects document text against mpcp_concepts
+        - returns traceable evidence + deterministic status
+        """
+        request = context.get("request") or {}
+        doc_text = (
+            context.get("doc_text")
+            or request.get("doc_text")
+            or context.get("text")
+            or ""
+        )
+        target = context.get("target") or request.get("target") or "W3"
+        responsibilities = self._responsibilities(plan)
+        required_terms = list(self.mpcp_concepts)
+        found_terms = self.inspect_mpcp(doc_text)
+        missing_terms = [t for t in required_terms if t not in found_terms]
+
+        # simple score for quick operational decision
+        coverage_ratio = (len(found_terms) / len(required_terms)) if required_terms else 1.0
+        status = "COMPLETED" if coverage_ratio >= 0.5 else "NEEDS_REVISION"
+
+        summary = (
+            f"{self.module_name} governance review on {target}: "
+            f"{len(found_terms)}/{len(required_terms)} concept coverage "
+            f"({coverage_ratio:.0%})"
+        )
+
+        return {
+            "contract_version": "1.1",
+            "status": status,
+            "module": self.module_name,
+            "task": task,
+            "role": self.mpcp_role,
+            "action": "governance_review",
+            "summary": summary,
+            "target": target,
+            "responsibilities": responsibilities,
+            "result": {
+                "required_terms": required_terms,
+                "found_terms": found_terms,
+                "missing_terms": missing_terms,
+                "coverage_ratio": coverage_ratio,
+            },
+            "artifacts": [
+                {
+                    "type": "governance_review",
+                    "label": f"{self.module_name} concept coverage",
+                    "evidence": {
+                        "terms_scanned": required_terms,
+                        "terms_found": found_terms,
+                        "terms_missing": missing_terms,
+                    },
+                }
+            ],
+            "mutated": False,
+            "traceable": True,
+            "review": True,
+        }
