import requests

IMPACT_MAP = {
    "green": "ไม่มีผลกระทบ",
    "yellow": "มีผลกระทบบางส่วน",
    "red": "เสี่ยงต่อระบบ"
}

def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers).json()

def get_pr_patch(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/vnd.github.v3.patch"}
    return requests.get(url, headers=headers).text

def extract_metrics(files):
    total_files = len(files)
    total_changes = sum(f.get("changes", 0) for f in files)
    test_files = sum(1 for f in files if "test" in f.get("filename", "").lower())

    return {
        "files": total_files,
        "changes": total_changes,
        "tests": test_files
    }

def evaluate(metrics):
    score = 100
    reasons = []

    if metrics["files"] > 5:
        score -= 20
        reasons.append("เปลี่ยนหลายไฟล์")

    if metrics["changes"] > 300:
        score -= 30
        reasons.append("diff ขนาดใหญ่")

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

def recommend(metrics, state):
    rec = []

    if metrics["tests"] == 0:
        rec.append("เพิ่ม test เพื่อรองรับ logic")

    if metrics["files"] > 5:
        rec.append("แยก PR ให้เล็กลง")

    if metrics["changes"] > 300:
        rec.append("ลดขนาด diff หรือแบ่ง commit")

    if not rec:
        rec.append("โครงสร้างเหมาะสม สามารถ merge ได้")

    return rec

def build_inline_comments(files, state):
    comments = []

    for f in files:
        if f.get("changes", 0) > 200:
            comments.append({
                "path": f["filename"],
                "body": f"🔴 ไฟล์นี้มีการแก้ไขหนัก ({f['changes']} lines) ควรแยกหรือ review เพิ่ม"
            })

    return comments
