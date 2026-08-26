    @@
 from typing import Dict, Any, List
 
 from .mpcp_reader import scan_terms, MPCP_CORE_TERMS
 
 
 class RuntimeAgent:
@@
     def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
@@
         return {
             "contract_version": "1.0",
@@
             "review": True,
         }
+
+    # -----------------------------
+    # Continuity hooks (MVP)
+    # -----------------------------
+    def preload_context(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
+        """
+        Read-before-guess hook:
+        Pull lightweight memory from context if available.
+        Runtime/dispatcher can inject these fields from notes/progress later.
+        """
+        notes = context.get("notes") or []
+        decisions = context.get("decisions") or []
+        expectations = context.get("expectations") or []
+        progress = context.get("progress") or {}
+        return {
+            "notes_count": len(notes),
+            "decisions_count": len(decisions),
+            "expectations_count": len(expectations),
+            "has_progress": bool(progress),
+        }
+
+    def collect_evidence(
+        self,
+        task: str,
+        plan: Dict[str, Any],
+        context: Dict[str, Any],
+        result: Dict[str, Any],
+    ) -> List[Dict[str, Any]]:
+        """
+        Evidence-first hook:
+        Gather minimal trace evidence from execution result.
+        """
+        evidence = []
+        if result.get("summary"):
+            evidence.append(
+                {
+                    "type": "summary",
+                    "label": f"{self.module_name} summary",
+                    "value": result["summary"],
+                }
+            )
+        if result.get("status"):
+            evidence.append(
+                {
+                    "type": "status",
+                    "label": f"{self.module_name} status",
+                    "value": result["status"],
+                }
+            )
+        return evidence
+
+    def reflect(
+        self,
+        task: str,
+        plan: Dict[str, Any],
+        context: Dict[str, Any],
+        result: Dict[str, Any],
+    ) -> Dict[str, Any]:
+        """
+        Learn hook:
+        Produce compact reflection payload for notes/reflections.
+        """
+        return {
+            "module": self.module_name,
+            "task": task,
+            "status": result.get("status"),
+            "insight": result.get("summary", "no summary"),
+            "next_attention": "verify missing evidence and continue iteration",
+        }
+
+    def persist_continuity(
+        self,
+        task: str,
+        plan: Dict[str, Any],
+        context: Dict[str, Any],
+        result: Dict[str, Any],
+        reflection: Dict[str, Any],
+    ) -> Dict[str, Any]:
+        """
+        Continue hook:
+        Return a normalized continuity packet for runtime to persist.
+        (File I/O can be added by dispatcher/storage layer.)
+        """
+        return {
+            "progress_entry": {
+                "module": self.module_name,
+                "task": task,
+                "status": result.get("status"),
+                "mutated": result.get("mutated", False),
+            },
+            "reflection_entry": reflection,
+            "next_step": result.get("reason") or "continue with next controlled iteration",
+        }
