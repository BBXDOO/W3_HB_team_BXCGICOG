import os
import json
import requests

----------------------

FETCH PR FILES

----------------------

def get_pr_files(repo, pr_number, token):
url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
headers = {"Authorization": f"Bearer {token}"}
return requests.get(url, headers=headers).json()

----------------------

FETCH PATCH (diff จริง)

----------------------

def get_patch(repo, pr_number, token):
url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
headers = {
"Authorization": f"Bearer {token}",
"Accept": "application/vnd.github.v3.patch"
}
return requests.get(url, headers=headers).text

----------------------

METRICS

----------------------

def extract_metrics(files):
return {
"files": len(files),
"changes": sum(f.get("changes", 0) for f in files),
"python": sum(1 for f in files if f["filename"].endswith(".py")),
"tests": sum(1 for f in files if "test" in f["filename"].lower())
}

----------------------

RISK

----------------------

def evaluate(metrics):
score = 100
reasons = []

if metrics["files"] > 5:
    score -= 20
    reasons.append("เปลี่ยนหลายไฟล์")

if metrics["changes"] > 300:
    score -= 30
    reasons.append("แก้ไขหนัก")

if metrics["tests"] == 0:
    score -= 30
    reasons.append("ไม่มี test")

if score >= 70:
    state = "green"
elif score >= 40:
    state = "yellow"
else:
    state = "red"

return state, score, reasons

----------------------

INLINE COMMENT (D NODE จริง)

----------------------

def build_comments(files):
comments = []

for f in files:
    filename = f["filename"]
    patch = f.get("patch", "")

    # หา line จริงจาก diff
    line = 1
    for p in patch.split("\n"):
        if p.startswith("@@"):
            try:
                line = int(p.split("+")[1].split(",")[0])
            except:
                line = 1
            break

    # rules
    if f.get("changes", 0) > 200:
        comments.append({
            "path": filename,
            "line": line,
            "body": "🔴 แก้ไขจำนวนมาก เสี่ยงต่อระบบ"
        })

    if "test" not in filename.lower():
        comments.append({
            "path": filename,
            "line": line,
            "body": "🟡 ยังไม่มี test"
        })

    if filename.endswith(".py"):
        comments.append({
            "path": filename,
            "line": line,
            "body": "🧠 logic สำคัญ ควร review เพิ่ม"
        })

return comments

----------------------

AI SUGGESTION (พื้นฐาน)

----------------------

def suggest(metrics):
if metrics["tests"] == 0:
return "แนะนำ: เพิ่ม unit test เพื่อความปลอดภัย"
if metrics["changes"] > 300:
return "แนะนำ: แยก PR เป็นหลายส่วน"
return "โครงสร้างเหมาะสม สามารถ merge ได้"

----------------------

SUMMARY

----------------------

def summary(state, reasons):
return {
"level": state,
"impact": reasons if reasons else ["ไม่มีผลกระทบ"]
}

----------------------

MAIN

----------------------

def run():
repo = os.getenv("REPO")
pr = os.getenv("PR_NUMBER")
token = os.getenv("GITHUB_TOKEN")

files = get_pr_files(repo, pr, token)
metrics = extract_metrics(files)
state, score, reasons = evaluate(metrics)

comments = build_comments(files)
rec = suggest(metrics)
sum_data = summary(state, reasons)

output = {
    "summary": sum_data,
    "score": score,
    "recommend": rec,
    "comments": comments
}

print(json.dumps(output))

if name == "main":
run()
