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
res = requests.get(url, headers=headers)

if res.status_code != 200:
    exit()

files = res.json()

# =====================
# METRICS
# =====================
total_files = len(files)
total_changes = sum(f.get("changes", 0) for f in files)

code_files = [f for f in files if f["filename"].endswith(
    (".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cpp")
)]

test_files = [f for f in files if "test" in f["filename"].lower()]

# =====================
# SCORE SYSTEM
# =====================
score = 100
issues = []

if total_files > 5:
    score -= 15
    issues.append("🟡 เปลี่ยนหลายไฟล์ เสี่ยงกระทบหลายจุด")

if total_files > 10:
    score -= 10
    issues.append("🔴 PR ใหญ่เกินควร")

if total_changes > 300:
    score -= 25
    issues.append("🔴 แก้ไขจำนวนมาก ตรวจสอบยาก")

if total_changes > 600:
    score -= 15
    issues.append("🔴 เปลี่ยนหนักมาก เสี่ยงพลาด")

if len(code_files) > 0 and len(test_files) == 0:
    score -= 25
    issues.append("🟡 มี code change แต่ไม่มี test")

if score < 0:
    score = 0

# =====================
# STATE COLOR
# =====================
if score >= 75:
    state = "green"
    color = "🟩"
elif score >= 45:
    state = "yellow"
    color = "🟨"
else:
    state = "red"
    color = "🟥"

# =====================
# FLOW VISUAL
# =====================
flow = ["🟩", color, "🟩", color, "🟩", color]

# =====================
# IMPACT
# =====================
impact = {
    "green": "🟢 ปลอดภัยระดับดี พร้อมพิจารณา merge",
    "yellow": "🟡 มีจุดเสี่ยง ควรตรวจเพิ่ม",
    "red": "🔴 ความเสี่ยงสูง ควร review ละเอียด"
}[state]

# =====================
# SUMMARY
# =====================
summary = []

summary.append(f"ไฟล์ที่เปลี่ยน: {total_files}")
summary.append(f"บรรทัดที่เปลี่ยน: {total_changes}")
summary.append(f"ไฟล์โค้ด: {len(code_files)}")
summary.append(f"ไฟล์ทดสอบ: {len(test_files)}")

# =====================
# RECOMMEND
# =====================
recommend = []

if total_files > 5:
    recommend.append("แยก PR ให้เล็กลง")

if total_changes > 300:
    recommend.append("ลดขนาดงานต่อ PR")

if len(code_files) > 0 and len(test_files) == 0:
    recommend.append("เพิ่ม test ก่อน merge")

if not recommend:
    recommend.append("สามารถ merge ได้")

# =====================
# INLINE COMMENTS
# =====================
comments = []

for f in files:
    filename = f["filename"]
    changes = f.get("changes", 0)

    if changes > 200:
        comments.append({
            "path": filename,
            "body": "🔴 ไฟล์นี้เปลี่ยนจำนวนมาก ควรตรวจละเอียด",
            "side": "RIGHT",
            "line": 1
        })

# =====================
# POST INLINE
# =====================
for c in comments:
    try:
        requests.post(
            f"https://api.github.com/repos/{repo}/pulls/{pr}/comments",
            headers=headers,
            json=c
        )
    except:
        pass

# =====================
# BUILD COMMENT UI
# =====================
body = "## 🔍 IGET v2\\n\\n"

body += "### FLOW\\n"
body += "".join(flow) + f" ({score}%)\\n\\n"

body += "### SUMMARY\\n"
for s in summary:
    body += f"- {s}\\n"

body += "\\n### RISK\\n"
if issues:
    for i in issues:
        body += f"- {i}\\n"
else:
    body += "- 🟢 ไม่พบความเสี่ยงเด่นชัด\\n"

body += "\\n### IMPACT\\n"
body += impact + "\\n"

body += "\\n### RECOMMEND\\n"
for r in recommend:
    body += f"- {r}\\n"

# =====================
# POST MAIN COMMENT
# =====================
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
    headers=headers,
    json={"body": body}
)
