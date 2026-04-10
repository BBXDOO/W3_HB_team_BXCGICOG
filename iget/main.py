import os
import requests

# ----------------------
# FETCH PR FILES
# ----------------------
def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else []

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
# EVALUATE (G)
# ----------------------
def evaluate(m):
    score = 100
    reasons = []

    if m["files"] > 5:
        score -= 20
        reasons.append("🔴 เปลี่ยนหลายไฟล์")

    if m["changes"] > 300:
        score -= 30
        reasons.append("🔴 แก้ไขจำนวนมาก")

    if m["tests"] == 0:
        score -= 30
        reasons.append("🟡 ไม่มี test")

    state = "green" if score >= 70 else "yellow" if score >= 40 else "red"
    return state, score, reasons

# ----------------------
# RECOMMEND (R)
# ----------------------
def recommend(m):
    rec = []
    if m["tests"] == 0:
        rec.append("เพิ่ม unit test")
    if m["files"] > 5:
        rec.append("แยก PR")
    if m["changes"] > 300:
        rec.append("ลดขนาด PR")
    return rec if rec else ["สามารถ merge ได้"]

# ----------------------
# FLOW (A-F)
# ----------------------
def build_flow(state):
    flow = ["🟩","🟩","🟩","🟩","🟩","🟩"]
    if state == "yellow":
        flow[2] = "🟨"
        flow[4] = "🟨"
    elif state == "red":
        flow[2] = "🟥"
        flow[4] = "🟥"
    return "".join(flow)

# ----------------------
# MAIN
# ----------------------
def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    files = get_pr_files(repo, pr, token)
    m = extract_metrics(files)
    state, score, reasons = evaluate(m)
    rec = recommend(m)
    flow = build_flow(state)

    emoji = {"green":"🟢","yellow":"🟡","red":"🔴"}

    out = []
    out.append(f"# 🔍 IGET PR #{pr}")

    # A + B + C
    out.append("\n## 🔗 FLOW")
    out.append(f"{flow}  ({score}%)")

    # D
    out.append("\n## ⚙️ STATUS")
    out.append("A → B → C → D → E → F")

    # E
    out.append("\n## 📋 SUMMARY")
    out.append(f"สถานะ: {emoji[state]} {state}")
    if reasons:
        for r in reasons:
            out.append(f"- {r}")
    else:
        out.append("- ไม่มีปัญหา")

    # G
    out.append("\n## 🎯 IMPACT")
    if state == "green":
        out.append("ไม่มีผลกระทบ")
    elif state == "yellow":
        out.append("มีผลกระทบบางส่วน")
    else:
        out.append("เสี่ยงต่อระบบ")

    # R
    out.append("\n## 🧠 RECOMMEND")
    for r in rec:
        out.append(f"- {r}")

    print("\n".join(out))

if __name__ == "__main__":
    run()
