    +from core.runtime.agents.copilot_gm import CopilotGmAgent
+
+
+def test_execute_no_doc_text_needs_revision():
+    agent = CopilotGmAgent()
+    out = agent.execute(
+        task="review origin notes alignment",
+        plan={"min_coverage": 0.5, "responsibilities": ["governance check"]},
+        context={"target": "Origin"},
+    )
+    assert out["status"] == "NEEDS_REVISION"
+    assert out["traceable"] is True
+    assert "continuity" in out
+
+
+def test_execute_partial_doc_text_default_threshold_completed():
+    agent = CopilotGmAgent()
+    out = agent.execute(
+        task="review policy doc",
+        plan={},  # default min_coverage = 0.5
+        context={"doc_text": "This proposal improves governance and compliance."},
+    )
+    assert out["status"] == "COMPLETED"
+    assert out["result"]["coverage_ratio"] >= 0.5
+
+
+def test_execute_strict_threshold_needs_revision():
+    agent = CopilotGmAgent()
+    out = agent.execute(
+        task="review structural policy",
+        plan={"min_coverage": 1.0},
+        context={"doc_text": "governance and policy only"},
+    )
+    assert out["status"] == "NEEDS_REVISION"
+    assert out["result"]["min_coverage"] == 1.0
