import os
import json
import requests

# =========================
# FETCH PR FILES
# =========================
def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else []

# =========================
# METRICS
# =========================
def extract_metrics(files):
    return {
        "files": len(files),
        "changes": sum(f.get("changes", 0) for f in files),
        "python": sum(1 for f in files if f["filename"].endswith(".py")),
        "tests": sum(1 for f in files if "test" in f["filename"].lower())
    }

# =========================
# RISK ENGINE (C, E node)
# =========================
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

# =========================
# FLOW (A–F)
# =========================
def build_flow(state):
    return ["green", "green", state, "green", state, "green"]

# =========================
# INLINE COMMENT (D node)
# =========================
def build_comments(files):
    comments = []

    for f in files:
        name = f["filename"]
        changes = f.get("changes", 0)

        if changes > 200:
            comments.append(f"🔴 {name} → แก้ไขหนัก")

        if "test" not in name.lower():
            comments.append(f"🟡 {name} → ไม่มี test")

        if name.endswith(".py"):
            comments.append(f"🧠 {name} → logic สำคัญ")

    return comments

# =========================
# RECOMMEND
# =========================
def recommend(metrics):
    if metrics["tests"] == 0:
        return "เพิ่ม unit test"
    if metrics["changes"] > 300:
        return "แยก PR"
    return "สามารถ merge ได้"

# =========================
# MEMORY
# =========================
def save_memory(pr, state, score):
    try:
        with open("iget_memory.json", "r") as f:
            mem = json.load(f)
    except:
        mem = []

    mem.append({
        "pr": pr,
        "state": state,
        "score": score
    })

    with open("iget_memory.json", "w") as f:
        json.dump(mem, f, indent=2)

# =========================
# RENDER (UI ทั้งหมด)
# =========================
def render(pr, flow, progress, state, reasons, comments, rec, score):
    emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}

    bar = "".join(["🟩" if s=="green" else "🟨" if s=="yellow" else "🟥" for s in flow])

    print("```")
    print(f"PR: #{pr}\n")

    # B + C
    print(f"Progress: {progress}%")
    print(bar)

    # D
    print("\n📍 Inline Insight")
    for c in comments:
        print("-", c)

    # E
    print("\n📋 SUMMARY")
    for r in reasons:
        print("-", r)

    # G
    print("\n🎯 IMPACT")
    print(emoji[state], state)

    # R
    print("\n💡 RECOMMEND")
    print("-", rec)

    # RESULT
    print("\n🏁 RESULT")
    print("✅ PASS" if state != "red" else "❌ RISK")

    print("\nScore:", score)
    print("```")

# =========================
# MAIN
# =========================
def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    files = get_pr_files(repo, pr, token)
    metrics = extract_metrics(files)
    state, score, reasons = evaluate(metrics)

    flow = build_flow(state)
    comments = build_comments(files)
    rec = recommend(metrics)

    progress = int((len(flow) / 6) * 100)

    save_memory(pr, state, score)

    render(pr, flow, progress, state, reasons, comments, rec, score)

if __name__ == "__main__":
    run()
