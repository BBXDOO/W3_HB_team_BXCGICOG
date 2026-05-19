import os
import sys
import json
from github import Github

def main():
# รับ event context จาก GitHub Actions
event_path = os.environ.get("GITHUB_EVENT_PATH")
if not event_path or not os.path.exists(event_path):
print("No event file found; aborting.")
sys.exit(0)
with open(event_path, "r", encoding="utf-8") as f:
event = json.load(f)

# กำหนดประเภทงาน (issue หรือ PR)
if "issue" in event:
issue = event["issue"]
url = issue["url"]
title = issue.get("title", "")
number = issue.get("number")
body = issue.get("body", "")
elif "pull_request" in event:
pr = event["pull_request"]
url = pr["issue_url"]
title = pr.get("title", "")
number = pr.get("number")
body = pr.get("body", "")
else:
print("No issue or PR context found.")
sys.exit(0)

# ตรวจสอบหัวข้อ (Optional: เงื่อนไขเฉพาะ W3 agent trigger)
if "EP-Signal" in title or "W3Lgu" in title or "MPCP" in title:
# เชื่อมต่อ GitHub ด้วย GITHUB_TOKEN
gh = Github(os.environ.get("GITHUB_TOKEN"))
repo_name = os.environ.get("GITHUB_REPOSITORY")
repo = gh.get_repo(repo_name)
issue_obj = repo.get_issue(number=number)

agent_comment = (
"🤖 Hello from W3Agent!\n"
"This issue relates to W3 system modules.\n"
"Automated agent has picked up your topic and will help orchestrate the next steps.\n"
"— W3 Auto-responder\n"
)
# ตอบกลับ (หรือปรับ logic ตาม module ได้)
issue_obj.create_comment(agent_comment)
print(f"Commented on issue/PR #{number}")
else:
print("Job detected, but not an EP-Signal/W3Lgu/MPCP trigger. No action needed.")

if name == "main":
main()
