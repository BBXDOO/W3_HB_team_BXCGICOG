import os
import json
import requests

# ----------------------
# FETCH PR FILES
# ----------------------
def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else []

# ----------------------
# METRICS
# ----------------------
def extract_metrics(files):
    return {
        "files": len(files),
        "changes": sum(f.get("changes", 0) for f in files),
        "tests": sum(1 for f in files if "test" in f.get("filename", "").lower())
    }

# ----------------------
# RISK
# ----------------------
def evaluate(metrics):
    score = 100
    reasons = []

    if metrics["files"] > 5:
        score -= 20
        reasons.append("เปลี่ยนหลายไฟล์")

    if metrics["changes"] > 300:
        score -= 30
        reasons.append("แก้ไขจำนวนมาก")

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

# ----------------------
# RECOMMEND
# ----------------------
def recommend(metrics):
    rec = []

    if metrics["tests"] == 0:
        rec.append("เพิ่ม test เพื่อความปลอดภัย")

    if metrics["files"] > 5:
        rec.append("แยก PR ให้เล็กลง")

    if metrics["changes"] > 300:
        rec.append("ลดขนาดการแก้ไข")

    if not rec:
        rec.append("โครงสร้างดี สามารถ merge ได้")

    return rec

# ----------------------
# INLINE COMMENTS (D NODE)
# ----------------------
def build_comments(files):
    comments = []

    for f in files:
        filename = f.get("filename")
        patch = f.get("patch", "")

        line = 1
        for p in patch.split("\n"):
            if p.startswith("@@"):
                try:
                    line = int(p.split("+")[1].split(",")[0])
                except:
                    line = 1
                break

        if f.get("changes", 0) > 200:
            comments.append({
                "path": filename,
                "line": line,
                "body": "🔴 แก้ไขจำนวนมาก อาจเสี่ยงต่อระบบ"
            })

        if "test" not in filename.lower():
            comments.append({
                "path": filename,
                "line": line,
                "body": "🟡 ยังไม่มี test รองรับ"
            })

    return comments

# ----------------------
# MAIN
# ----------------------
def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    files = get_pr_files(repo, pr, token)
    metrics = extract_metrics(files)
    state, score, reasons = evaluate(metrics)
    rec = recommend(metrics)
    comments = build_comments(files)

    output = {
        "summary": {
            "level": state,
            "reasons": reasons
        },
        "score": score,
        "recommend": rec,
        "comments": comments
    }

    print(json.dumps(output))

if __name__ == "__main__":
    run()
