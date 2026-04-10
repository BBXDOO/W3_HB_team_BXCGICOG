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
# EVALUATE (G node)
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

    if score >= 70:
        state = "green"
    elif score >= 40:
        state = "yellow"
    else:
        state = "red"

    return state, score, reasons

# ----------------------
# RECOMMEND (R node)
# ----------------------
def recommend(m):
    rec = []

    if m["tests"] == 0:
        rec.append("เพิ่ม unit test")

    if m["files"] > 5:
        rec.append("แยก PR เป็นส่วนย่อย")

    if m["changes"] > 300:
        rec.append("ลดขนาด PR")

    if not rec:
        rec.append("สามารถ merge ได้")

    return rec

# ----------------------
# INLINE COMMENT (D node จริง)
# ----------------------
def build_comments(files):
    comments = []

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
            comments.append({
                "path": name,
                "line": line,
                "body": "🔴 แก้ไขหนัก อาจกระทบระบบ"
            })

        if "test" not in name.lower():
            comments.append({
                "path": name,
                "line": line,
                "body": "🟡 ยังไม่มี test รองรับ"
            })

    return comments

# ----------------------
# FLOW (A-F visualization)
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
    comments = build_comments(files)
    flow = build_flow(state)

    emoji = {
        "green": "🟢",
        "yellow": "🟡",
        "red": "🔴"
    }

    # ----------------------
    # OUTPUT (สำหรับ PR comment)
    # ----------------------
    out = []

    out.append(f"# 🔍 IGET PR #{pr}")
    out.append("\n## 🔗 FLOW")
    out.append(f"{flow}  ({score}%)")

    out.append("\n## 📊 SUMMARY")
    out.append(f"สถานะ: {emoji[state]} {state}")

    if reasons:
        for r in reasons:
            out.append(f"- {r}")
    else:
        out.append("- ไม่มีปัญหา")

    out.append("\n## 🎯 IMPACT")
    if state == "green":
        out.append("ไม่มีผลกระทบ")
    elif state == "yellow":
        out.append("มีผลกระทบบางส่วน")
    else:
        out.append("เสี่ยงต่อระบบ")

    out.append("\n## 🧠 RECOMMEND")
    for r in rec:
        out.append(f"- {r}")

    print("\n".join(out))

    # ----------------------
    # DEBUG (optional json)
    # ----------------------
    # print(comments)

if __name__ == "__main__":
    run()
