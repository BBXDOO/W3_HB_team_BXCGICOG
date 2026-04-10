import os
import json
import requests

# ======================
# CONFIG
# ======================
IMPACT_MAP = {
    "green": "ไม่มีผลกระทบ",
    "yellow": "มีผลกระทบบางส่วน",
    "red": "เสี่ยงต่อระบบ"
}

MEMORY_FILE = "iget_memory.json"

# ======================
# FETCH PR FILES
# ======================
def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return []

    return res.json()

# ======================
# METRICS
# ======================
def extract_metrics(files):
    total_files = len(files)
    total_changes = 0
    python_files = 0
    test_files = 0

    for f in files:
        changes = f.get("changes", 0)
        name = f.get("filename", "")

        total_changes += changes

        if name.endswith(".py"):
            python_files += 1

        if "test" in name.lower():
            test_files += 1

    return {
        "total_files": total_files,
        "total_changes": total_changes,
        "python_files": python_files,
        "test_files": test_files
    }

# ======================
# RULE ENGINE
# ======================
def evaluate_risk(files, metrics):
    score = 100
    reasons = []

    if metrics["total_files"] > 5:
        score -= 20
        reasons.append("เปลี่ยนหลายไฟล์")

    if metrics["total_changes"] > 300:
        score -= 30
        reasons.append("แก้ไขจำนวนบรรทัดมาก")

    if metrics["python_files"] > 3:
        score -= 20
        reasons.append("เกี่ยวข้องกับ logic หลายไฟล์")

    if metrics["test_files"] == 0:
        score -= 30
        reasons.append("ไม่มี test รองรับ")

    for f in files:
        name = f.get("filename", "").lower()

        if "config" in name:
            score -= 25
            reasons.append("แก้ไข config")
            break

        if "db" in name:
            score -= 25
            reasons.append("เกี่ยวข้องกับฐานข้อมูล")
            break

    if any(f.get("changes", 0) > 300 for f in files):
        score -= 25
        reasons.append("มีไฟล์แก้ไขหนัก")

    if score >= 70:
        state = "green"
    elif score >= 40:
        state = "yellow"
    else:
        state = "red"

    return state, score, reasons

# ======================
# SUMMARY (E + G)
# ======================
def build_summary(state, reasons):
    level = state
    impact = IMPACT_MAP[state]

    summary = []
    if reasons:
        for r in reasons:
            summary.append(r)
    else:
        summary.append("ไม่มีปัญหาที่ตรวจพบ")

    return summary, level, impact

# ======================
# RECOMMEND (R)
# ======================
def build_recommendation(metrics):
    rec = []

    if metrics["total_files"] > 5:
        rec.append("แนะนำให้แยก PR เป็นส่วนย่อย")

    if metrics["test_files"] == 0:
        rec.append("ควรเพิ่ม test")

    if metrics["total_changes"] > 300:
        rec.append("ลดขนาด PR")

    if not rec:
        rec.append("โครงสร้างดีแล้ว สามารถ merge ได้")

    return rec

# ======================
# MEMORY
# ======================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    mem = load_memory()
    mem.append(data)

    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

# ======================
# RENDER (Markdown)
# ======================
def render(pr, state, score, metrics, summary, level, impact, rec):
    emoji = {
        "green": "🟢",
        "yellow": "🟡",
        "red": "🔴"
    }

    flow = "🟩🟩"
    flow += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
    flow += "🟩"
    flow += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
    flow += "🟩"

    output = []

    output.append("# 🔍 IGET PR Analysis")
    output.append(f"## 🧾 PR: {pr}\n")

    # B + C
    output.append("## 📊 Progress")
    output.append("[██████████] 100%\n")

    # Flow
    output.append("## 🔗 Flow")
    output.append("A → B → C → D → E → F\n")

    output.append("## 🧩 Flow State")
    output.append(flow + "\n")

    # SUMMARY
    output.append("## 📋 SUMMARY")
    for s in summary:
        output.append(f"- {s}")

    # LEVEL
    output.append("\n## 🎚 LEVEL")
    output.append(f"{emoji[level]} {level}")

    # IMPACT
    output.append("\n## 🎯 IMPACT")
    output.append(impact)

    # METRICS
    output.append("\n## 📂 DATA")
    output.append(f"- files: {metrics['total_files']}")
    output.append(f"- changes: {metrics['total_changes']}")
    output.append(f"- python: {metrics['python_files']}")
    output.append(f"- tests: {metrics['test_files']}")

    # SCORE
    output.append(f"\n## 🧠 SCORE: {score}/100")

    # RECOMMEND
    output.append("\n## 🧠 RECOMMEND")
    for r in rec:
        output.append(f"- {r}")

    # RESULT
    result = "✅ ผ่าน" if state != "red" else "❌ เสี่ยง"
    output.append("\n## 🏁 RESULT")
    output.append(result)

    print("```")
    print("\n".join(output))
    print("```")

# ======================
# MAIN
# ======================
def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    files = get_pr_files(repo, pr_number, token)
    metrics = extract_metrics(files)
    state, score, reasons = evaluate_risk(files, metrics)

    summary, level, impact = build_summary(state, reasons)
    rec = build_recommendation(metrics)

    # save memory
    save_memory({
        "pr": pr_number,
        "state": state,
        "score": score,
        "metrics": metrics,
        "reasons": reasons
    })

    render(pr_number, state, score, metrics, summary, level, impact, rec)

if __name__ == "__main__":
    run()
