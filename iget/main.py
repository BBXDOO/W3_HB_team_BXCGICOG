```diff
diff --git a/iget/main.py b/iget/main.py
index 531696e..6ca9175 100644
--- a/iget/main.py
+++ b/iget/main.py
@@ -1,179 +1,272 @@
 import os
 import requests
 
-# ----------------------
-# FETCH PR FILES
-# ----------------------
-def get_pr_files(repo, pr_number, token):
-    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
-    headers = {
-        "Authorization": f"Bearer {token}",
-        "Accept": "application/vnd.github+json"
-    }
-
-    res = requests.get(url, headers=headers)
-    if res.status_code != 200:
-        return []
-
-    return res.json()
-
-# ----------------------
-# METRICS
-# ----------------------
-def extract_metrics(files):
-    total_files = len(files)
-    total_changes = 0
-    python_files = 0
-    test_files = 0
-
-    for f in files:
-        changes = f.get("changes", 0)
-        name = f.get("filename", "")
-
-        total_changes += changes
-
-        if name.endswith(".py"):
-            python_files += 1
-
-        if "test" in name.lower():
-            test_files += 1
-
-    return {
-        "total_files": total_files,
-        "total_changes": total_changes,
-        "python_files": python_files,
-        "test_files": test_files
-    }
-
-# ----------------------
-# RULE ENGINE
-# ----------------------
-def evaluate_risk(files, metrics):
-    score = 100
-    reasons = []
-
-    # rule 1: many files
-    if metrics["total_files"] > 5:
-        score -= 20
-        reasons.append("เปลี่ยนหลายไฟล์")
-
-    # rule 2: large change
-    if metrics["total_changes"] > 300:
-        score -= 30
-        reasons.append("แก้ไขจำนวนบรรทัดมาก")
-
-    # rule 3: python heavy
-    if metrics["python_files"] > 3:
-        score -= 20
-        reasons.append("เกี่ยวข้องกับ logic (.py หลายไฟล์)")
-
-    # rule 4: no test
-    if metrics["test_files"] == 0:
-        score -= 30
-        reasons.append("ไม่มี test รองรับ")
-
-    # rule 5: config/db
-    for f in files:
-        name = f.get("filename", "").lower()
-        if "config" in name:
-            score -= 25
-            reasons.append("แก้ไขไฟล์ config")
-            break
-
-        if "db" in name:
-            score -= 25
-            reasons.append("เกี่ยวข้องกับฐานข้อมูล")
-            break
-
-    # rule 6: heavy file
-    if any(f.get("changes", 0) > 300 for f in files):
-        score -= 25
-        reasons.append("มีไฟล์ที่ถูกแก้หนักมาก")
-
-    # state
-    if score >= 70:
-        state = "green"
-    elif score >= 40:
-        state = "yellow"
-    else:
-        state = "red"
-
-    return state, score, reasons
-
-# ----------------------
-# MAIN
-# ----------------------
-def run():
-    repo = os.getenv("GITHUB_REPOSITORY")
-    pr_number = os.getenv("PR_NUMBER")
-    token = os.getenv("GITHUB_TOKEN")
-
-    commit = os.getenv("GITHUB_SHA", "")[:7]
-
-    files = get_pr_files(repo, pr_number, token)
-    metrics = extract_metrics(files)
-    state, score, reasons = evaluate_risk(files, metrics)
-
-    # progress mock (full flow done)
-    progress_bar = "██████████"
-    percent = 100
-
-    emoji = {
-        "green": "🟢",
-        "yellow": "🟡",
-        "red": "🔴"
-    }
-
-    flow_state = "🟩🟩"
-    flow_state += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
-    flow_state += "🟩"
-    flow_state += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
-    flow_state += "🟩"
-
-    output = []
-
-    output.append("# 🔍 IGET PR Analysis")
-    output.append(f"## 🧾 PR: {pr_number}")
-    output.append(f"🧬 Commit: `{commit}`\n")
-
-    output.append("## 📊 Progress")
-    output.append(f"[{progress_bar}] {percent}%\n")
-
-    output.append("## 🔗 Flow")
-    output.append("A → B → C → D → E → F\n")
-
-    output.append("## 🧩 Flow State")
-    output.append(flow_state + "\n")
-
-    output.append("## 📋 Issues")
-    output.append(f"- C → {emoji[state]} {state}")
-    output.append(f"- E → {emoji[state]} {state}\n")
-
-    output.append("## 🎯 Impact")
-    if reasons:
-        for r in reasons:
-            output.append(f"- {r}")
-    else:
-        output.append("ไม่มีผลกระทบ")
-
-    output.append("\n## 🧠 Analysis")
-    output.append(f"Score: {score}/100")
-
-    output.append("\n## 📂 PR Data")
-    output.append(f"- files: {metrics['total_files']}")
-    output.append(f"- changes: {metrics['total_changes']}")
-    output.append(f"- python: {metrics['python_files']}")
-    output.append(f"- tests: {metrics['test_files']}")
-
-    result = "✅ สำเร็จ" if state != "red" else "❌ มีความเสี่ยง"
-
-    output.append("\n## 🏁 Result")
-    output.append(result)
-
-    print("```")
-    print("\n".join(output))
-    print("```")
-
-if __name__ == "__main__":
-    run()
+repo = os.getenv("REPO")
+pr = os.getenv("PR")
+token = os.getenv("GITHUB_TOKEN")
+
+headers = {
+    "Authorization": f"Bearer {token}",
+    "Accept": "application/vnd.github+json"
+}
+
+# ==========================================
+# FETCH PR FILES
+# ==========================================
+url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
+res = requests.get(url, headers=headers)
+
+if res.status_code != 200:
+    exit()
+
+files = res.json()
+
+# ==========================================
+# CONFIG
+# ==========================================
+MAX_INLINE_COMMENTS = 5
+
+CODE_EXT = (
+    ".py", ".js", ".ts", ".tsx",
+    ".jsx", ".json", ".yml", ".yaml",
+    ".css", ".html"
+)
+
+DOC_EXT = (
+    ".md", ".txt", ".rst"
+)
+
+RISK_WORDS = [
+    ".env",
+    "secret",
+    "token",
+    "password",
+    "credential",
+    "private_key",
+    "apikey"
+]
+
+# ==========================================
+# METRICS
+# ==========================================
+total_files = len(files)
+total_changes = sum(f.get("changes", 0) for f in files)
+
+code_files = []
+doc_files = []
+test_files = []
+risky_files = []
+
+for f in files:
+    name = f["filename"].lower()
+
+    if name.endswith(CODE_EXT):
+        code_files.append(f)
+
+    if name.endswith(DOC_EXT):
+        doc_files.append(f)
+
+    if "test" in name or "spec" in name:
+        test_files.append(f)
+
+    if any(word in name for word in RISK_WORDS):
+        risky_files.append(f)
+
+# ==========================================
+# DETECT MODE
+# ==========================================
+docs_only = (
+    len(doc_files) == total_files and total_files > 0
+)
+
+# ==========================================
+# SCORE ENGINE
+# ==========================================
+score = 100
+issues = []
+
+if total_files > 5:
+    score -= 10
+    issues.append("🟡 เปลี่ยนหลายไฟล์")
+
+if total_files > 12:
+    score -= 10
+    issues.append("🔴 PR ใหญ่เกินควร")
+
+if total_changes > 300:
+    score -= 20
+    issues.append("🔴 แก้ไขจำนวนมาก")
+
+if total_changes > 700:
+    score -= 15
+    issues.append("🔴 เปลี่ยนหนักมาก")
+
+# code but no tests
+if not docs_only:
+    if len(code_files) > 0 and len(test_files) == 0:
+        score -= 20
+        issues.append("🟡 มี code change แต่ไม่มี test")
+
+# risky files
+if len(risky_files) > 0:
+    score -= 30
+    issues.append("🔴 พบไฟล์เสี่ยง")
+
+# docs bonus
+if docs_only:
+    issues.append("🔵 Documentation PR")
+    score += 5
+
+if score > 100:
+    score = 100
+
+if score < 0:
+    score = 0
+
+# ==========================================
+# STATE COLOR
+# ==========================================
+if score >= 85:
+    state = "green"
+elif score >= 60:
+    state = "yellow"
+else:
+    state = "red"
+
+FLOW = {
+    "green": "🟩",
+    "yellow": "🟨",
+    "red": "🟥"
+}
+
+flow = [
+    "🟩",
+    FLOW[state],
+    FLOW[state],
+    "🟩",
+    FLOW[state],
+    "🟩"
+]
+
+impact = {
+    "green": "🟢 ปลอดภัยระดับดี พร้อม merge",
+    "yellow": "🟡 มีความเสี่ยงบางส่วน ควรตรวจเพิ่ม",
+    "red": "🔴 เสี่ยงสูง ควร review ก่อน merge"
+}[state]
+
+# ==========================================
+# SUMMARY
+# ==========================================
+summary = []
+summary.append(f"- ไฟล์ที่เปลี่ยน: {total_files}")
+summary.append(f"- บรรทัดที่เปลี่ยน: {total_changes}")
+summary.append(f"- ไฟล์โค้ด: {len(code_files)}")
+summary.append(f"- ไฟล์เอกสาร: {len(doc_files)}")
+summary.append(f"- ไฟล์ทดสอบ: {len(test_files)}")
+
+if docs_only:
+    summary.append("- โหมด: Documentation Only")
+
+# ==========================================
+# RECOMMEND
+# ==========================================
+recommend = []
+
+if docs_only:
+    recommend.append("ตรวจเนื้อหา/คำสะกดก่อน merge")
+
+if not docs_only and len(code_files) > 0 and len(test_files) == 0:
+    recommend.append("เพิ่ม test coverage")
+
+if total_changes > 300:
+    recommend.append("ลดขนาด PR")
+
+if total_files > 10:
+    recommend.append("แยก PR เป็นงานย่อย")
+
+if len(risky_files) > 0:
+    recommend.append("ตรวจไฟล์เสี่ยงทันที")
+
+if not recommend:
+    recommend.append("สามารถ merge ได้")
+
+# ==========================================
+# INLINE COMMENTS
+# ==========================================
+comments = []
+
+for f in files:
+    name = f["filename"]
+    changes = f.get("changes", 0)
+    low = name.lower()
+
+    if changes > 250:
+        comments.append({
+            "path": name,
+            "line": 1,
+            "body": "🔴 ไฟล์นี้แก้ไขจำนวนมาก ควรตรวจละเอียด"
+        })
+
+    if (
+        not docs_only
+        and low.endswith(CODE_EXT)
+        and "test" not in low
+        and len(test_files) == 0
+    ):
+        comments.append({
+            "path": name,
+            "line": 1,
+            "body": "🟡 พิจารณาเพิ่ม test สำหรับส่วนนี้"
+        })
+
+# anti spam
+comments = comments[:MAX_INLINE_COMMENTS]
+
+# ==========================================
+# POST INLINE COMMENTS
+# ==========================================
+for c in comments:
+    requests.post(
+        f"https://api.github.com/repos/{repo}/pulls/{pr}/comments",
+        headers=headers,
+        json=c
+    )
+
+# ==========================================
+# BUILD COMMENT
+# ==========================================
+body = "## 🔍 IGET v4\n\n"
+
+body += "### FLOW\n"
+body += "".join(flow) + f" ({score}%)\n\n"
+
+body += "### SUMMARY\n"
+for s in summary:
+    body += s + "\n"
+
+body += "\n### RISK\n"
+if issues:
+    for i in issues:
+        body += f"- {i}\n"
+else:
+    body += "- 🟢 ไม่พบความเสี่ยงเด่นชัด\n"
+
+body += "\n### IMPACT\n"
+body += impact + "\n"
+
+body += "\n### RECOMMEND\n"
+for r in recommend:
+    body += f"- {r}\n"
+
+body += "\n---\n"
+body += "_Powered by W3 IGET Governance Engine v4_"
+
+# ==========================================
+# POST COMMENT
+# ==========================================
+requests.post(
+    f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
+    headers=headers,
+    json={"body": body}
+)
```
