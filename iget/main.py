import os
import json
import requests

# ======================
# FETCH PR FILES
# ======================
def get_pr_files(repo, pr, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else []

# ======================
# METRICS
# ======================
def extract(files):
    return {
        "files": len(files),
        "changes": sum(f.get("changes", 0) for f in files),
        "tests": sum(1 for f in files if "test" in f["filename"].lower())
    }

# ======================
# NODE SYSTEM (A–F)
# ======================
def build_nodes(state):
    return [
        {"id": "A", "state": "green"},
        {"id": "B", "state": "green"},
        {"id": "C", "state": state},     # system check
        {"id": "D", "state": "yellow"},  # decision (uncertain)
        {"id": "E", "state": state},     # decision result
        {"id": "F", "state": "green"}    # merge
    ]

# ======================
# DECISION ENGINE (D)
# ======================
def evaluate(m):
    score = 100
    issues = []

    if m["files"] > 5:
        score -= 20
        issues.append("เปลี่ยนหลายไฟล์")

    if m["changes"] > 300:
        score -= 30
        issues.append("แก้ไขหนัก")

    if m["tests"] == 0:
        score -= 30
        issues.append("ไม่มี test")

    if score >= 70:
        state = "green"
    elif score >= 40:
        state = "yellow"
    else:
        state = "red"

    return state, score, issues

# ======================
# IMPACT ENGINE (G)
# ======================
def impact(state):
    if state == "green":
        return "🟢 ไม่มีผลกระทบ"
    if state == "yellow":
        return "🟡 มีความเสี่ยงบางส่วน"
    return "🔴 กระทบโครงสร้าง"

# ======================
# RECOMMEND (R)
# ======================
def recommend(m):
    rec = []

    if m["tests"] == 0:
        rec.append("เพิ่ม test")

    if m["files"] > 5:
        rec.append("แยก PR")

    if m["changes"] > 300:
        rec.append("ลดขนาด PR")

    if not rec:
        rec.append("สามารถ merge ได้")

    return rec

# ======================
# MEMORY (pattern)
# ======================
def save(pr, state, score):
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

# ======================
# FLOW UI
# ======================
def render_nodes(nodes):
    m = {"green":"🟩","yellow":"🟨","red":"🟥"}
    return "".join([m[n["state"]] for n in nodes])

# ======================
# INLINE INSIGHT (D)
# ======================
def insight(files):
    out = []
    for f in files:
        name = f["filename"]
        if f.get("changes", 0) > 200:
            out.append(f"🔴 {name} แก้ไขหนัก")
        if "test" not in name.lower():
            out.append(f"🟡 {name} ไม่มี test")
    return out

# ======================
# MAIN
# ======================
def run():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    files = get_pr_files(repo, pr, token)
    m = extract(files)

    state, score, issues = evaluate(m)
    nodes = build_nodes(state)

    flow = render_nodes(nodes)
    imp = impact(state)
    rec = recommend(m)
    ins = insight(files)

    save(pr, state, score)

    print("```")
    print(f"IGET PR #{pr}\n")

    print("FLOW")
    print(flow, f"{score}%")

    print("\nSTATE")
    print("A → B → C → D → E → F")

    print("\nSUMMARY")
    for i in issues:
        print("-", i)

    print("\nINSIGHT (D)")
    for i in ins:
        print("-", i)

    print("\nIMPACT (G)")
    print(imp)

    print("\nRECOMMEND (R)")
    for r in rec:
        print("-", r)

    print("\nRESULT")
    print("PASS" if state != "red" else "RISK")

    print("```")

if __name__ == "__main__":
    run()
