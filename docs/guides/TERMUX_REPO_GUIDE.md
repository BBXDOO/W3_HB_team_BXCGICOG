# 📱 คู่มือใช้งาน Repository นี้ด้วย Termux (Android)

> สำหรับผู้เริ่มต้นจนถึงใช้งานจริง: clone repo, แก้ไฟล์, รัน `.json/.py/.java/.yaml/.html` และตัวอย่างเชื่อมต่อฐานข้อมูลภายนอก

---

## 0) สิ่งที่ต้องรู้ก่อนเริ่ม

- Termux = Linux terminal บน Android
- แนะนำติดตั้ง Termux จาก **F-Droid** (ไม่ใช่ Play Store)
- คู่มือนี้ “โฟกัสเฉพาะ repo นี้” และใช้คำสั่งที่รันได้จริงบน Termux

ถ้าต้องการคู่มือพื้นฐาน Termux + GitHub แบบยาว: `knowledge/apps_manual/android/termux_github.md`

---

## 1) ติดตั้งแพ็กเกจที่จำเป็น

เปิด Termux แล้วรัน:

```bash
pkg update && pkg upgrade -y

# เครื่องมือพื้นฐาน
pkg install -y git openssh nano vim jq curl ca-certificates

# ภาษา/รันไทม์ (เลือกใช้ตามงาน)
pkg install -y python openjdk-17 nodejs
```

ตรวจสอบเวอร์ชัน:

```bash
git --version
python --version
java -version
node -v
```

---

## 2) Clone และเข้าโฟลเดอร์ repo

### Clone ผ่าน HTTPS

```bash
git clone https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
cd W3_HB_team_BXCGICOG
```

> ถ้า push ไม่ได้เพราะ GitHub ไม่รับ password แล้ว ให้ใช้ Token หรือ SSH (ดู `knowledge/apps_manual/android/termux_github.md`)

---

## 3) โครงสร้างไฟล์สำคัญใน repo (อ่านเร็ว)

- `README.md` ภาพรวม repo / ลิงก์เอกสาร
- `docs/guides/QUICK_START.md` คู่มือรันสคริปต์ตรวจ integrity
- `tools/file_integrity_check.py` ตัวอย่างสคริปต์ที่รันได้ทันที
- `requirements.txt` dependency ฝั่ง Python (ใน repo นี้มีแค่ `jsonschema`)

---

## 4) งานที่เจอบ่อย: เปิด/แก้ไฟล์บนมือถือ

### เปิดไฟล์

```bash
ls
pwd
```

### แก้ไฟล์แบบเร็ว

```bash
nano README.md
# หรือ
vim README.md
```

---

## 5) รองรับไฟล์ .json: ตรวจ/จัดรูปแบบ/อ่านค่า

### ตรวจว่า JSON ถูกต้อง (parse ได้)

```bash
python -m json.tool docs/meta/ACKNOWLEDGMENTS.md >/dev/null 2>&1 || true
python -m json.tool resume_header.json
```

### ใช้ `jq` อ่านค่า

```bash
jq '.' resume_header.json
jq -r '.keyword' resume_header.json
```

### แก้ค่าแบบไม่เปิด editor

```bash
jq '.timestamp = "2026-01-01T00:00:00Z"' resume_header.json > /tmp/resume_header.json && mv /tmp/resume_header.json resume_header.json
```

---

## 6) รองรับไฟล์ .py: รันสคริปต์จริงของ repo

### ติดตั้ง dependency ของ repo

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### รัน quick start ของ repo

```bash
python tools/file_integrity_check.py
```

เอกสารเพิ่มเติม: `docs/guides/QUICK_START.md`

---

## 7) รองรับไฟล์ .yaml: ตรวจ syntax แบบเร็ว

Termux ไม่มี YAML validator ติดมาทุกเครื่อง แนะนำใช้ Python module `pyyaml` แบบเบา:

```bash
python -m pip install pyyaml
python - <<'PY'
import sys, yaml
path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
  yaml.safe_load(f)
print('OK:', path)
PY .github/workflows/check_test.ts
```

หมายเหตุ: ใน repo นี้บางไฟล์ใน `.github/workflows/` อาจเป็น `.ts` ไม่ใช่ `.yaml` ให้เปลี่ยน path เป็นไฟล์ `.yml/.yaml` ที่ต้องการตรวจจริง

---

## 8) รองรับไฟล์ .java: คอมไพล์/รันแบบง่าย

ตัวอย่าง “Hello” แบบไฟล์เดียว:

```bash
cat > /tmp/Hello.java <<'JAVA'
public class Hello {
  public static void main(String[] args) {
    System.out.println("Hello from Termux");
  }
}
JAVA

javac /tmp/Hello.java
java -cp /tmp Hello
```

> ถ้า repo มีไฟล์ Java จริง ให้ใช้ `javac path/to/File.java` ตามตำแหน่งไฟล์

---

## 9) รองรับไฟล์ .html: เปิดดูบนมือถือ

### วิธีง่ายที่สุด

- เปิดไฟล์ผ่าน File Manager แล้วเลือกเปิดด้วย Browser
- ตัวอย่างไฟล์ใน repo: `portal.html`

### เสิร์ฟผ่าน local server (สำหรับทดสอบเร็ว)

```bash
python -m http.server 8000
```

แล้วเปิดบนมือถือ: `http://127.0.0.1:8000/portal.html`

---

## 10) เชื่อมต่อฐานข้อมูลภายนอก (ตัวอย่าง)

แนวทางที่ปลอดภัยคือ “อย่าใส่รหัสผ่านลง git” ให้ใช้ environment variables แทน

### ตัวอย่าง PostgreSQL (Python)

1) ติดตั้ง driver

```bash
python -m pip install psycopg2-binary
```

2) ตั้งค่า env (ตัวอย่าง)

```bash
export DB_HOST="your-host"
export DB_PORT="5432"
export DB_NAME="your-db"
export DB_USER="your-user"
export DB_PASSWORD="your-password"
```

3) รันทดสอบการเชื่อมต่อ

```bash
python - <<'PY'
import os
import psycopg2

conn = psycopg2.connect(
  host=os.environ['DB_HOST'],
  port=int(os.environ.get('DB_PORT', '5432')),
  dbname=os.environ['DB_NAME'],
  user=os.environ['DB_USER'],
  password=os.environ['DB_PASSWORD'],
)

with conn.cursor() as cur:
  cur.execute('select 1')
  print('DB OK:', cur.fetchone()[0])

conn.close()
PY
```

> ถ้าใช้ MySQL/MariaDB: `python -m pip install pymysql` แล้วเชื่อมด้วย `pymysql.connect(...)`

---

## 11) Workflow Git ที่ใช้บ่อยบนมือถือ

```bash
git status
git pull --rebase

# แก้ไฟล์เสร็จ
git add .
git commit -m "docs: update termux guide"
git push
```

---

## 12) Troubleshooting (ที่เจอบ่อยบน Termux)

- `Permission denied (publickey)` → ตั้งค่า SSH key ให้ครบ (ดู `knowledge/apps_manual/android/termux_github.md`)
- `No module named pip` → `pkg install python` แล้ว `python -m ensurepip --upgrade`
- `pip install ...` ช้ามาก/ติด → ลอง `python -m pip install -U pip` และเช็ค network

