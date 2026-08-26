    @@
 from .base import RuntimeAgent
 
 
 class CopilotGmAgent(RuntimeAgent):
@@
     action_label = "completed governance review"
@@
     mpcp_role = "governance"
     mpcp_concepts = ["governance", "policy", "compliance", "structural consistency"]
+
+    def execute(self, task, plan, context):
+        """
+        Governance executor (MVP):
+        - checks concept coverage in doc_text
+        - returns traceable, non-fabricated status
+        - includes reflection + continuity packet
+        """
+        preload = self.preload_context(task, plan, context)
+        request = context.get("request") or {}
+        doc_text = (
+            context.get("doc_text")
+            or request.get("doc_text")
+            or context.get("text")
+            or ""
+        )
+        target = context.get("target") or request.get("target") or "W3"
+        responsibilities = self._responsibilities(plan)
+
+        required_terms = list(self.mpcp_concepts)
+        found_terms = self.inspect_mpcp(doc_text)
+        missing_terms = [t for t in required_terms if t not in found_terms]
+
+        min_coverage = float(plan.get("min_coverage", 0.5))
+        coverage_ratio = (len(found_terms) / len(required_terms)) if required_terms else 1.0
+        status = "COMPLETED" if coverage_ratio >= min_coverage else "NEEDS_REVISION"
+
+        summary = (
+            f"{self.module_name} governance review on {target}: "
+            f"{len(found_terms)}/{len(required_terms)} concept coverage "
+            f"({coverage_ratio:.0%}, threshold={min_coverage:.0%})"
+        )
+
+        result = {
+            "contract_version": "1.2",
+            "status": status,
+            "module": self.module_name,
+            "task": task,
+            "role": self.mpcp_role,
+            "action": "governance_review",
+            "summary": summary,
+            "target": target,
+            "responsibilities": responsibilities,
+            "preload": preload,
+            "result": {
+                "required_terms": required_terms,
+                "found_terms": found_terms,
+                "missing_terms": missing_terms,
+                "coverage_ratio": coverage_ratio,
+                "min_coverage": min_coverage,
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
+
+        evidence = self.collect_evidence(task, plan, context, result)
+        reflection = self.reflect(task, plan, context, result)
+        continuity = self.persist_continuity(task, plan, context, result, reflection)
+
+        result["evidence"] = evidence
+        result["reflection"] = reflection
+        result["continuity"] = continuity
+        return result
