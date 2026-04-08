import os
import requests

# ----------------------
# FETCH PR FILES
# ----------------------
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

# ----------------------
# METRICS
# ----------------------
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

# ----------------------
# RULE ENGINE
# ----------------------
def evaluate_risk(files, metrics):
    score = 100
    reasons = []

    # rule 1: many files
    if metrics["total_files"] > 5:
        score -= 20
        reasons.append("เปลี่ยนหลายไฟล์")

    # rule 2: large change
    if metrics["total_changes"] > 300:
        score -= 30
        reasons.append("แก้ไขจำนวนบรรทัดมาก")

    # rule 3: python heavy
    if metrics["python_files"] > 3:
        score -= 20
        reasons.append("เกี่ยวข้องกับ logic (.py หลายไฟล์)")

    # rule 4: no test
    if metrics["test_files"] == 0:
        score -= 30
        reasons.append("ไม่มี test รองรับ")

    # rule 5: config/db
    for f in files:
        name = f.get("filename", "").lower()
        if "config" in name:
            score -= 25
            reasons.append("แก้ไขไฟล์ config")
            break

        if "db" in name:
            score -= 25
            reasons.append("เกี่ยวข้องกับฐานข้อมูล")
            break

    # rule 6: heavy file
    if any(f.get("changes", 0) > 300 for f in files):
        score -= 25
        reasons.append("มีไฟล์ที่ถูกแก้หนักมาก")

    # state
    if score >= 70:
        state = "green"
    elif score >= 40:
        state = "yellow"
    else:
        state = "red"

    return state, score, reasons

# ----------------------
# MAIN
# ----------------------
def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    commit = os.getenv("GITHUB_SHA", "")[:7]

    files = get_pr_files(repo, pr_number, token)
    metrics = extract_metrics(files)
    state, score, reasons = evaluate_risk(files, metrics)

    # progress mock (full flow done)
    progress_bar = "██████████"
    percent = 100

    emoji = {
        "green": "🟢",
        "yellow": "🟡",
        "red": "🔴"
    }

    flow_state = "🟩🟩"
    flow_state += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
    flow_state += "🟩"
    flow_state += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
    flow_state += "🟩"

    output = []

    output.append("# 🔍 IGET PR Analysis")
    output.append(f"## 🧾 PR: {pr_number}")
    output.append(f"🧬 Commit: `{commit}`\n")

    output.append("## 📊 Progress")
    output.append(f"[{progress_bar}] {percent}%\n")

    output.append("## 🔗 Flow")
    output.append("A → B → C → D → E → F\n")

    output.append("## 🧩 Flow State")
    output.append(flow_state + "\n")

    output.append("## 📋 Issues")
    output.append(f"- C → {emoji[state]} {state}")
    output.append(f"- E → {emoji[state]} {state}\n")

    output.append("## 🎯 Impact")
    if reasons:
        for r in reasons:
            output.append(f"- {r}")
    else:
        output.append("ไม่มีผลกระทบ")

    output.append("\n## 🧠 Analysis")
    output.append(f"Score: {score}/100")

    output.append("\n## 📂 PR Data")
    output.append(f"- files: {metrics['total_files']}")
    output.append(f"- changes: {metrics['total_changes']}")
    output.append(f"- python: {metrics['python_files']}")
    output.append(f"- tests: {metrics['test_files']}")

    result = "✅ สำเร็จ" if state != "red" else "❌ มีความเสี่ยง"

    output.append("\n## 🏁 Result")
    output.append(result)

    print("```")
    print("\n".join(output))
    print("```")

if __name__ == "__main__":
    run()
