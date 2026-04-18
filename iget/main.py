import os
import requests

repo = os.getenv("REPO")
pr = os.getenv("PR")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# ==================================
# FETCH PR FILES
# ==================================
url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
res = requests.get(url, headers=headers)

if res.status_code != 200:
    exit()

files = res.json()

# ==================================
# METRICS
# ==================================
total_files = len(files)
total_changes = sum(f.get("changes", 0) for f in files)

code_ext = (
    ".py", ".js", ".ts", ".tsx",
    ".jsx", ".json", ".yml", ".yaml",
    ".md", ".css", ".html"
)

code_files = [
    f for f in files
    if f["filename"].lower().endswith(code_ext)
]

test_files = [
    f for f in files
    if "test" in f["filename"].lower()
]

doc_files = [
    f for f in files
    if f["filename"].lower().endswith(".md")
]

risky_files = [
    f for f in files
    if any(x in f["filename"].lower() for x in [
        ".env", "secret", "token",
        "password", "credential",
        "key"
    ])
]

# ==================================
# SCORE SYSTEM
# ==================================
score = 100
issues = []

if total_files > 5:
    score -= 10
    issues.append("🟡 เปลี่ยนหลายไฟล์")

if total_files > 12:
    score -= 10
    issues.append("🔴 PR ใหญ่เกินควร")

if total_changes > 300:
    score -= 20
    issues.append("🔴 แก้ไขจำนวนมาก")

if total_changes > 700:
    score -= 15
    issues.append("🔴 เปลี่ยนหนักมาก")

if len(code_files) > 0 and len(test_files) == 0:
    score -= 20
    issues.append("🟡 มี code change แต่ไม่มี test")

if len(risky_files) > 0:
    score -= 30
    issues.append("🔴 พบไฟล์เสี่ยง")

if score < 0:
    score = 0

# ==================================
# STATUS COLOR
# ==================================
if score >= 85:
    state = "green"
elif score >= 60:
    state = "yellow"
else:
    state = "red"

flow_map = {
    "green": "🟩",
    "yellow": "🟨",
    "red": "🟥"
}

flow = [
    "🟩",
    flow_map[state],
    flow_map[state],
    "🟩",
    flow_map[state],
    "🟩"
]

impact = {
    "green": "🟢 ปลอดภัยระดับดี พร้อมพิจารณา merge",
    "yellow": "🟡 มีความเสี่ยงบางส่วน ควรตรวจเพิ่ม",
    "red": "🔴 เสี่ยงสูง ควรตรวจละเอียดก่อน merge"
}[state]

# ==================================
# SUMMARY
# ==================================
summary = []
summary.append(f"- ไฟล์ที่เปลี่ยน: {total_files}")
summary.append(f"- บรรทัดที่เปลี่ยน: {total_changes}")
summary.append(f"- ไฟล์โค้ด: {len(code_files)}")
summary.append(f"- ไฟล์ทดสอบ: {len(test_files)}")
summary.append(f"- ไฟล์เอกสาร: {len(doc_files)}")

# ==================================
# RECOMMEND
# ==================================
recommend = []

if len(test_files) == 0 and len(code_files) > 0:
    recommend.append("เพิ่ม test coverage")

if total_changes > 300:
    recommend.append("ลดขนาด PR")

if total_files > 10:
    recommend.append("แยก PR เป็นส่วนย่อย")

if len(risky_files) > 0:
    recommend.append("ตรวจไฟล์เสี่ยงทันที")

if not recommend:
    recommend.append("สามารถ merge ได้")

# ==================================
# INLINE COMMENTS
# ==================================
comments = []

for f in files:
    name = f["filename"]

    if f.get("changes", 0) > 250:
        comments.append({
            "path": name,
            "line": 1,
            "body": "🔴 ไฟล์นี้แก้ไขจำนวนมาก ควรตรวจละเอียด"
        })

    if "test" not in name.lower() and name.lower().endswith((".py",".js",".ts",".tsx")):
        comments.append({
            "path": name,
            "line": 1,
            "body": "🟡 พิจารณาเพิ่ม test สำหรับไฟล์นี้"
        })

# ==================================
# POST INLINE COMMENTS
# ==================================
for c in comments:
    requests.post(
        f"https://api.github.com/repos/{repo}/pulls/{pr}/comments",
        headers=headers,
        json=c
    )

# ==================================
# BUILD COMMENT UI
# ==================================
body = "## 🔍 IGET v3\n\n"

body += "### FLOW\n"
body += "".join(flow) + f" ({score}%)\n\n"

body += "### SUMMARY\n"
for s in summary:
    body += s + "\n"

body += "\n### RISK\n"
if issues:
    for i in issues:
        body += f"- {i}\n"
else:
    body += "- 🟢 ไม่พบความเสี่ยงเด่นชัด\n"

body += "\n### IMPACT\n"
body += impact + "\n"

body += "\n### RECOMMEND\n"
for r in recommend:
    body += f"- {r}\n"

body += "\n---\n"
body += "_Powered by W3 IGET Governance Engine_"

# ==================================
# POST COMMENT
# ==================================
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
    headers=headers,
    json={"body": body}
)
