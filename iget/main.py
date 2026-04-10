import os
import requests

repo = os.getenv("REPO")
pr = os.getenv("PR")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# =====================
# FETCH PR FILES
# =====================
url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
files = requests.get(url, headers=headers).json()

# =====================
# METRICS
# =====================
total_files = len(files)
total_changes = sum(f.get("changes", 0) for f in files)
tests = sum(1 for f in files if "test" in f["filename"].lower())

# =====================
# LOGIC (D)
# =====================
score = 100
issues = []

if total_files > 5:
    score -= 20
    issues.append("🔴 เปลี่ยนหลายไฟล์")

if total_changes > 300:
    score -= 30
    issues.append("🔴 แก้ไขหนัก")

if tests == 0:
    score -= 30
    issues.append("🟡 ไม่มี test")

if score >= 70:
    state = "green"
elif score >= 40:
    state = "yellow"
else:
    state = "red"

# =====================
# FLOW (A–F)
# =====================
flow_map = {
    "green": "🟩",
    "yellow": "🟨",
    "red": "🟥"
}

flow = ["🟩","🟩",flow_map[state],"🟩",flow_map[state],"🟩"]

# =====================
# IMPACT (G)
# =====================
impact = {
    "green": "🟢 ไม่มีผลกระทบ",
    "yellow": "🟡 มีความเสี่ยงบางส่วน",
    "red": "🔴 กระทบระบบ"
}[state]

# =====================
# RECOMMEND (R)
# =====================
recommend = []

if tests == 0:
    recommend.append("เพิ่ม test")

if total_files > 5:
    recommend.append("แยก PR")

if total_changes > 300:
    recommend.append("ลดขนาด PR")

if not recommend:
    recommend.append("สามารถ merge ได้")

# =====================
# INLINE COMMENTS (D จริง)
# =====================
comments = []

for f in files:
    filename = f["filename"]
    if f.get("changes", 0) > 200:
        comments.append({
            "path": filename,
            "line": 1,
            "body": "🔴 แก้ไขหนัก"
        })

    if "test" not in filename.lower():
        comments.append({
            "path": filename,
            "line": 1,
            "body": "🟡 ไม่มี test"
        })

# =====================
# POST INLINE COMMENTS
# =====================
for c in comments:
    requests.post(
        f"https://api.github.com/repos/{repo}/pulls/{pr}/comments",
        headers=headers,
        json=c
    )

# =====================
# BUILD UI (COMMENT)
# =====================
body = "## 🔍 IGET\n\n"

body += "### FLOW\n"
body += "".join(flow) + f" ({score}%)\n\n"

body += "### SUMMARY\n"
for i in issues:
    body += f"- {i}\n"

body += "\n### IMPACT\n"
body += impact + "\n"

body += "\n### RECOMMEND\n"
for r in recommend:
    body += f"- {r}\n"

# =====================
# POST COMMENT
# =====================
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
    headers=headers,
    json={"body": body}
)
