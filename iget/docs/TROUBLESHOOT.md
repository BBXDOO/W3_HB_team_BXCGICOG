# Troubleshoot

แนวทางตรวจปัญหา IGET

## No Comment Posted

### อาการ

IGET workflow run ผ่านหรือเริ่มทำงาน แต่ไม่มี comment ใน PR

### ตรวจอะไร

```text
- GITHUB_TOKEN มีสิทธิ์เขียน issue comment หรือไม่
- workflow permission เปิด write หรือไม่
- PR number resolve ถูกหรือไม่
- ใช้ fork PR หรือไม่
- pull_request_target ใช้ trusted base code ถูกหรือไม่
```

### คำสั่งช่วยตรวจ

```bash
PYTHONPATH=. python -m pytest iget/tests -q
```

ใช้ dry-run เพื่อตรวจว่าระบบสร้าง comment body ได้ไหม:

```bash
REPO=OWNER/REPO PR=1 GITHUB_TOKEN=xxx IGET_DRY_RUN=1 \
PYTHONPATH=. python -m iget.main
```

---

## Wrong Score

### อาการ

คะแนนดูไม่ตรงกับความรู้สึกหรือสถานการณ์จริง

### ตรวจอะไร

```text
- classify_files แยก code/doc/test/risky ถูกไหม
- changes จาก GitHub API ถูกไหม
- threshold ใน config.py เหมาะไหม
- risky keyword ตรงเกินไปหรือกว้างเกินไปไหม
- PR รวมหลายงานเกินไปไหม
```

### ข้อสังเกต

คะแนนเป็น signal ไม่ใช่ judgment สุดท้าย ถ้า PR มีบริบทพิเศษ human reviewer ต้องพิจารณาเพิ่ม

---

## Too Many Alerts

### อาการ

IGET แจ้งเตือนเยอะเกินหรือ comment ซ้ำ

### ตรวจอะไร

```text
- summary marker <!-- iget:summary --> ยังอยู่ไหม
- มี legacy comment หลายชุดหรือไม่
- inline comments เปิดอยู่หรือไม่
- threshold ต่ำเกินไปหรือไม่
```

### แนวทางแก้

- ใช้ summary comment เป็น default
- เปิด inline comments เฉพาะเคสที่ต้องการ
- tune threshold อย่างระวัง
- ลด duplicate comment ด้วย idempotent marker

---

## Runtime Context Missing

### อาการ

ระบบแจ้งว่า missing runtime values

### ต้องมีค่าอย่างน้อย

```text
REPO หรือ GITHUB_REPOSITORY
PR หรือ PR_NUMBER หรือ INPUT_PR_NUMBER
GITHUB_TOKEN หรือ GH_TOKEN
```

---

## สรุป

ปัญหา IGET ส่วนใหญ่แยกได้เป็น 3 กลุ่ม:

```text
1. context ไม่ครบ
2. permission ไม่พอ
3. scoring/classification ไม่ตรงสถานการณ์
```
