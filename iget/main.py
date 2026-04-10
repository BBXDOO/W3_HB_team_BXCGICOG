import os
import json
import requests

def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else []

def extract_metrics(files):
    return {
        "files": len(files),
        "changes": sum(f.get("changes", 0) for f in files),
        "tests": sum(1 for f in files if "test" in f.get("filename", "").lower())
    }

def evaluate(m):
    score = 100
    reasons = []

    if m["files"] > 5:
        score -= 20
        reasons.append("เปลี่ยนหลายไฟล์")

    if m["changes"] > 300:
        score -= 30
        reasons.append("แก้ไขจำนวนมาก")

    if m["tests"] == 0:
        score -= 30
        reasons.append("ไม่มี test")

    state = "green" if score >= 70 else "yellow" if score >= 40 else "red"
    return state, score, reasons

def recommend(m):
    rec = []
    if m["tests"] == 0:
        rec.append("เพิ่ม test")
    if m["files"] > 5:
        rec.append("แยก PR")
    if m["changes"] > 300:
        rec.append("ลดขนาด PR")
    return rec if rec else ["พร้อม merge"]

def build_comments(files):
    out = []
    for f in files:
        name = f.get("filename")
        patch = f.get("patch", "")

        line = 1
        for p in patch.split("\n"):
            if p.startswith("@@"):
                try:
                    line = int(p.split("+")[1].split(",")[0])
                except:
                    pass
                break

        if f.get("changes", 0) > 200:
            out.append({"path": name, "line": line, "body": "🔴 แก้เยอะ"})

        if "test" not in name.lower():
            out.append({"path": name, "line": line, "body": "🟡 ไม่มี test"})

    return out

def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    files = get_pr_files(repo, pr, token)
    m = extract_metrics(files)
    state, score, reasons = evaluate(m)

    result = {
        "summary": {"level": state, "reasons": reasons},
        "score": score,
        "recommend": recommend(m),
        "comments": build_comments(files)
    }

    print(json.dumps(result))

if __name__ == "__main__":
    run()
