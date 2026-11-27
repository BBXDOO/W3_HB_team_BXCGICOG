---
AM_TYPE: III
ROLE: USAGE_GUIDE
GROUP: CONTINUE
DERIVED_FROM:
  - docs/governance/AMS.md
  - tools/README.md
OWNER: BBX19
---

# Quick Start Guide - File Integrity Check
# คู่มือเริ่มต้นอย่างรวดเร็ว - การตรวจสอบไฟล์

## การใช้งานอย่างรวดเร็ว / Quick Usage

### 1. ตรวจสอบไฟล์ / Check Files

```bash
cd /path/to/W3_HB_team_BXCGICOG
python3 tools/file_integrity_check.py
```

ผลลัพธ์จะแสดงบนหน้าจอและบันทึกไว้ที่ `tools/file_integrity_report.txt`

### 2. ส่งรายงานทางอีเมล / Send Email Report

```bash
# ตั้งค่า / Configure
export SENDER_EMAIL="your-email@gmail.com"
export RECIPIENT_EMAIL="recipient@example.com"
export SENDER_PASSWORD="your-app-password"

# ส่งรายงาน / Send report
python3 tools/send_integrity_report.py
```

## ตัวอย่างผลลัพธ์ / Example Output

```
================================================================================
FILE INTEGRITY CHECK REPORT
================================================================================
Repository: W3_HB_team_BXCGICOG
Check Date: 2025-12-09 06:25:43
================================================================================

⚠️  STATUS: 6 ISSUES DETECTED

📁 MISSING DIRECTORIES:
----------------------------------------
  • modules/ChatGPT/flows/
  • modules/ChatGPT/requests/
  • modules/ChatGPT/scenarios/
  • modules/Gemini/reports/
  • modules/Gemini/requests/
  • workflows/orchestration/

================================================================================
SUMMARY:
----------------------------------------
Missing Directories:     6
Missing Files:           0
Corrupted JSON Files:    0
Suspicious Empty Files:  0
Broken Symbolic Links:   0
TOTAL ISSUES:            6
================================================================================
```

## การแก้ไขปัญหา / Fix Issues

### สร้างโฟลเดอร์ที่หายไป / Create Missing Directories

```bash
# สร้างทั้งหมดในคำสั่งเดียว / Create all at once
mkdir -p modules/ChatGPT/{flows,requests,scenarios}
mkdir -p modules/Gemini/{reports,requests}
mkdir -p workflows/orchestration

# หรือสร้างทีละอัน / Or create one by one
mkdir -p modules/ChatGPT/flows
mkdir -p modules/ChatGPT/requests
mkdir -p modules/ChatGPT/scenarios
mkdir -p modules/Gemini/reports
mkdir -p modules/Gemini/requests
mkdir -p workflows/orchestration
```

## การรันอัตโนมัติ / Automation

### ใช้ Cron (Linux/Mac)

```bash
# แก้ไข crontab
crontab -e

# เพิ่มบรรทัดนี้เพื่อรันทุกวันเวลา 9:00 น.
0 9 * * * cd /path/to/W3_HB_team_BXCGICOG && python3 tools/file_integrity_check.py
```

### ใช้ GitHub Actions

ดูตัวอย่างใน `tools/README.md`

## คำถามที่พบบ่อย / FAQ

**Q: โฟลเดอร์ที่หายไปจำเป็นต้องสร้างหรือไม่?**
A: ขึ้นอยู่กับว่าคุณจะใช้ฟีเจอร์นั้นหรือไม่ หากไม่ใช้ ก็ไม่จำเป็นต้องสร้างทันที

**Q: ทำไมต้องใช้ App Password สำหรับ Gmail?**
A: เพื่อความปลอดภัย Gmail ไม่อนุญาตให้ใช้รหัสผ่านธรรมดาสำหรับแอป

**Q: รายงานจะส่งในรูปแบบใด?**
A: ทั้ง plain text และ HTML (สวยงามมีสี)

**Q: สามารถใช้กับ email service อื่นได้หรือไม่?**
A: ได้ แค่ตั้งค่า SMTP_SERVER และ SMTP_PORT ให้ถูกต้อง

## ข้อมูลเพิ่มเติม / More Information

- รายงานฉบับสมบูรณ์ (ไทย): `INTEGRITY_REPORT_TH.md`
- เอกสารเต็ม (อังกฤษ): `tools/README.md`
- รายงานล่าสุด: `tools/file_integrity_report.txt`

---

**สร้างโดย / Created by:** GitHub Copilot  
**วันที่ / Date:** 2025-12-09
