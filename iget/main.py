import os
import requests

repo = os.getenv("REPO")
pr = os.getenv("PR")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# ==========================================
# FETCH PR FILES
# ==========================================
url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
res = requests.get(url, headers=headers)

if res.status_code != 200:
    exit()

files = res.json()

# ==========================================
# CONFIG
# ==========================================
MAX_INLINE_COMMENTS = 5

CODE_EXT = (
    ".py", ".js", ".ts", ".tsx",
    ".jsx", ".json", ".yml", ".yaml",
    ".css", ".html"
)

DOC_EXT = (
    ".md", ".txt", ".rst"
)

RISK_WORDS = [
    ".env",
    "secret",
    "token",
    "password",
    "credential",
    "private_key",
    "apikey"
]

# ==========================================
# METRICS
# ==========================================
total_files = len(files)
total_changes = sum(f.get("changes", 0) for f in files)

code_files = []
doc_files = []
test_files = []
risky_files = []

for f in files:
    name = f["filename"].lower()

    if name.endswith(CODE_EXT):
        code_files.append(f)

    if name.endswith(DOC_EXT):
        doc_files.append(f)

    if "test" in name or "spec" in name:
        test_files.append(f)

    if any(word in name for word in RISK_WORDS):
        risky_files.append(f)

# ==========================================
# DETECT MODE
# ==========================================
docs_only = (
    len(doc_files) == total_files and total_files > 0
)

# ==========================================
# SCORE ENGINE
# ==========================================
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

# code but no tests
if not docs_only:
    if len(code_files) > 0 and len(test_files) == 0:
        score -= 20
        issues.append("🟡 มี code change แต่ไม่มี test")

# risky files
if len(risky_files) > 0:
    score -= 30
    issues.append("🔴 พบไฟล์เสี่ยง")

# docs bonus
if docs_only:
    issues.append("🔵 Documentation PR")
    score += 5

if score > 100:
    score = 100

if score < 0:
    score = 0

# ==========================================
# STATE COLOR
# ==========================================
if score >= 85:
    state = "green"
elif score >= 60:
    state = "yellow"
else:
    state = "red"

FLOW = {
    "green": "🟩",
    "yellow": "🟨",
    "red": "🟥"
}

flow = [
    "🟩",
    FLOW[state],
    FLOW[state],
    "🟩",
    FLOW[state],
    "🟩"
]

impact = {
    "green": "🟢 ปลอดภัยระดับดี พร้อม merge",
    "yellow": "🟡 มีความเสี่ยงบางส่วน ควรตรวจเพิ่ม",
    "red": "🔴 เสี่ยงสูง ควร review ก่อน merge"
}[state]

# ==========================================
# SUMMARY
# ==========================================
summary = []
summary.append(f"- ไฟล์ที่เปลี่ยน: {total_files}")
summary.append(f"- บรรทัดที่เปลี่ยน: {total_changes}")
summary.append(f"- ไฟล์โค้ด: {len(code_files)}")
summary.append(f"- ไฟล์เอกสาร: {len(doc_files)}")
summary.append(f"- ไฟล์ทดสอบ: {len(test_files)}")

if docs_only:
    summary.append("- โหมด: Documentation Only")

# ==========================================
# RECOMMEND
# ==========================================
recommend = []

if docs_only:
    recommend.append("ตรวจเนื้อหา/คำสะกดก่อน merge")

if not docs_only and len(code_files) > 0 and len(test_files) == 0:
    recommend.append("เพิ่ม test coverage")

if total_changes > 300:
    recommend.append("ลดขนาด PR")

if total_files > 10:
    recommend.append("แยก PR เป็นงานย่อย")

if len(risky_files) > 0:
    recommend.append("ตรวจไฟล์เสี่ยงทันที")

if not recommend:
    recommend.append("สามารถ merge ได้")

# ==========================================
# INLINE COMMENTS
# ==========================================
comments = []

for f in files:
    name = f["filename"]
    changes = f.get("changes", 0)
    low = name.lower()

    if changes > 250:
        comments.append({
            "path": name,
            "line": 1,
            "body": "🔴 ไฟล์นี้แก้ไขจำนวนมาก ควรตรวจละเอียด"
        })

    if (
        not docs_only
        and low.endswith(CODE_EXT)
        and "test" not in low
        and len(test_files) == 0
    ):
        comments.append({
            "path": name,
            "line": 1,
            "body": "🟡 พิจารณาเพิ่ม test สำหรับส่วนนี้"
        })

# anti spam
comments = comments[:MAX_INLINE_COMMENTS]

# ==========================================
# POST INLINE COMMENTS
# ==========================================
for c in comments:
    requests.post(
        f"https://api.github.com/repos/{repo}/pulls/{pr}/comments",
        headers=headers,
        json=c
    )

# ==========================================
# BUILD COMMENT
# ==========================================
body = "## 🔍 IGET v4\n\n"

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
body += "_Powered by W3 IGET Governance Engine v4_"

# ==========================================
# POST COMMENT
# ==========================================
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
    headers=headers,
    json={"body": body}
)
