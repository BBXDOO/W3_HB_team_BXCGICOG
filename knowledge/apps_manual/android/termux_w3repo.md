↩️ [กลับไป Apps Manual Hub](../INDEX.md)

# 🛠️ คู่มือใช้งานและสั่งงาน Repository BBXDOO/W3_HB_team_BXCGICOG ด้วย Termux

> **สำหรับผู้เริ่มต้นจนถึงขั้นใช้งานจริง** — รองรับ `.json` `.py` `.java` `.yaml` `.html`
> ทั้งเพื่อเก็บเอกสาร, รันโค้ด และเชื่อมต่อฐานข้อมูลภายนอก

---

## 1) ติดตั้ง Termux และเครื่องมือพื้นฐาน

### ดาวน์โหลด Termux
- ❌ อย่าดาวน์โหลดจาก Play Store (เวอร์ชันเก่า)
- ✅ ดาวน์โหลดจาก **F-Droid** หรือ **GitHub Releases**:
  - F-Droid: [https://f-droid.org/packages/com.termux/](https://f-droid.org/packages/com.termux/)
  - GitHub: [https://github.com/termux/termux-app/releases](https://github.com/termux/termux-app/releases)

### อัปเดตและติดตั้งเครื่องมือพื้นฐาน

```bash
pkg update && pkg upgrade -y
pkg install git python python-pip nano curl wget -y
```

> ใช้เวลาประมาณ 3–10 นาที ขึ้นอยู่กับความเร็วอินเทอร์เน็ต

---

## 2) Clone Repository

### ผ่าน HTTPS

```bash
git clone https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
cd W3_HB_team_BXCGICOG
```

### ผ่าน SSH (แนะนำ ถ้าตั้งค่า SSH key แล้ว)

```bash
git clone git@github.com:BBXDOO/W3_HB_team_BXCGICOG.git
cd W3_HB_team_BXCGICOG
```

> ดูวิธีตั้งค่า SSH Key ได้ที่ [termux_github.md](termux_github.md) หัวข้อ 5

### ดูโครงสร้างโฟลเดอร์หลัก

```bash
ls
```

โครงสร้างที่สำคัญ:

```
W3_HB_team_BXCGICOG/
├── src/          ← Python engine หลัก
├── core/         ← module loader, memory, runtime
├── tools/        ← สคริปต์เครื่องมือ (.py)
├── docs/         ← เอกสาร JSON
├── config/       ← ค่าตั้งต้นระบบ (.json)
├── knowledge/    ← คลังความรู้ (.md, .json)
├── modules/      ← ทะเบียน AI modules (.json)
├── requirements.txt
└── portal.html
```

---

## 3) ตั้งค่า Python Environment และรันไฟล์ .py

### ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

> ตรวจสอบ `requirements.txt` เสมอเพื่อดู dependencies ล่าสุด ก่อนติดตั้ง

### รัน W3 Hybrid Engine (ไฟล์หลัก)

```bash
python src/main.py
```

> Engine จะบูตโมดูล → เข้า heartbeat loop → กด `Ctrl+C` เพื่อหยุด

### รันสคริปต์เครื่องมือ

```bash
# ตรวจสอบ JSON schemas
python tools/validate_json_schemas.py

# ตรวจสอบความสมบูรณ์ของไฟล์
python tools/file_integrity_check.py

# รัน audit ทั้งระบบ
python tools/run_audit.py
```

### รัน iget module

```bash
python iget/main.py
```

### ทดสอบ (unit tests)

```bash
python -m pytest iget/tests/ -v
```

> ถ้ายังไม่มี pytest: `pip install pytest`

---

## 4) จัดการไฟล์ .json

ไฟล์ JSON ในโปรเจกต์นี้ใช้เก็บ: config, module registry, schema, memory และ log

### อ่านไฟล์ JSON

```bash
# ดูไฟล์ config หลัก
cat config/environment.json

# ดู module registry
cat modules/registry.json

# ดู memory store
cat core/memory/memory_store.json
```

### แก้ไขไฟล์ JSON ด้วย nano

```bash
nano config/environment.json
```

> ใน nano: `Ctrl+O` บันทึก → `Ctrl+X` ออก

### ตรวจสอบ JSON syntax ด้วย Python

```bash
python -c "import json; json.load(open('config/environment.json')); print('JSON valid')"
```

### ตรวจสอบ JSON ตาม schema

```bash
python tools/validate_json_schemas.py
```

### สร้างไฟล์ JSON ใหม่ด้วย Python

```bash
python3 << 'EOF'
import json

data = {
  "name": "my_module",
  "version": "0.1",
  "status": "active"
}

with open("my_module.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("สร้างไฟล์สำเร็จ")
EOF
```

---

## 5) จัดการไฟล์ .yaml

ไฟล์ .yaml ใช้สำหรับ workflow และ CI/CD configuration

### ติดตั้ง PyYAML

```bash
pip install pyyaml
```

### อ่านไฟล์ YAML ด้วย Python

```bash
python3 << 'EOF'
import yaml

with open("my_config.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print(data)
EOF
```

### สร้างไฟล์ .yaml ใหม่

```bash
python3 << 'EOF'
import yaml

config = {
  "name": "w3-workflow",
  "version": "1.0",
  "steps": ["clone", "install", "run"]
}

with open("workflow.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

print("สร้างไฟล์ YAML สำเร็จ")
EOF
```

### แก้ไข YAML ด้วย nano

```bash
nano workflow.yaml
```

---

## 6) เปิดและทำงานกับไฟล์ .html

### ดูเนื้อหาไฟล์ portal.html

```bash
cat portal.html
```

### แก้ไขด้วย nano

```bash
nano portal.html
```

### เปิดในเบราว์เซอร์บน Android

ติดตั้ง `termux-open-url`:

```bash
pkg install termux-tools -y
```

แล้วเปิดไฟล์:

```bash
termux-open portal.html
```

> ระบบจะเปิดไฟล์ใน Chrome หรือเบราว์เซอร์เริ่มต้นบน Android

### รัน HTTP server เพื่อดู HTML ในเบราว์เซอร์

```bash
python -m http.server 8080
```

> จากนั้นเปิด Chrome แล้วไปที่ `http://localhost:8080/portal.html`

---

## 7) ทำงานกับไฟล์ .java

### ติดตั้ง Java บน Termux

```bash
pkg install openjdk-21 -y
```

> ตรวจสอบ: `java -version`

### สร้างและรันไฟล์ .java

สร้างไฟล์ทดสอบ:

```bash
cat > Hello.java << 'EOF'
public class Hello {
    public static void main(String[] args) {
        System.out.println("W3 Engine - Java OK");
    }
}
EOF
```

คอมไพล์และรัน:

```bash
javac Hello.java
java Hello
```

### ทำงานกับ Java ใน repo

ถ้ามีไฟล์ .java ใน repo ให้เข้าไปในโฟลเดอร์นั้นแล้ว:

```bash
# คอมไพล์
javac ชื่อไฟล์.java

# รัน
java ชื่อคลาส
```

### ใช้ Maven (ถ้า repo มี pom.xml)

```bash
pkg install maven -y
mvn compile
mvn exec:java -Dexec.mainClass="MainClass"
```

---

## 8) เชื่อมต่อฐานข้อมูลภายนอก

### SQLite (ในตัว ไม่ต้องติดตั้งเพิ่ม)

```bash
pkg install sqlite -y
```

ใช้งานใน Python:

```python
import sqlite3

conn = sqlite3.connect("w3_local.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY,
        name TEXT,
        status TEXT
    )
""")

cursor.execute("INSERT INTO modules (name, status) VALUES (?, ?)", ("BBX19", "READY"))
conn.commit()

for row in cursor.execute("SELECT * FROM modules"):
    print(row)

conn.close()
```

รันสคริปต์:

```bash
python3 db_test.py
```

---

### PostgreSQL

ติดตั้ง client:

```bash
pkg install postgresql -y
pip install psycopg2-binary
```

เชื่อมต่อใน Python:

```python
import psycopg2

conn = psycopg2.connect(
    host="your-host",
    port=5432,
    database="your_db",
    user="your_user",
    password="your_password"
)
cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

---

### MySQL / MariaDB

ติดตั้ง:

```bash
pip install mysql-connector-python
```

เชื่อมต่อใน Python:

```python
import mysql.connector

conn = mysql.connector.connect(
    host="your-host",
    user="your_user",
    password="your_password",
    database="your_db"
)
cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
for table in cursor:
    print(table)
conn.close()
```

---

## 9) คำสั่งที่ใช้บ่อยในโปรเจกต์นี้

| คำสั่ง | ความหมาย |
|---|---|
| `python src/main.py` | รัน W3 Hybrid Engine |
| `python tools/run_audit.py` | ตรวจสอบระบบทั้งหมด |
| `python tools/validate_json_schemas.py` | ตรวจ JSON schemas |
| `python tools/file_integrity_check.py` | ตรวจความสมบูรณ์ไฟล์ |
| `python iget/main.py` | รัน iget module |
| `python -m pytest iget/tests/ -v` | รัน unit tests |
| `cat config/environment.json` | ดู config หลัก |
| `cat modules/registry.json` | ดู module registry |
| `python -m http.server 8080` | เปิด HTTP server |
| `git pull origin main` | ดึงอัปเดตล่าสุด |
| `git log --oneline -10` | ดู commit ล่าสุด 10 รายการ |

---

## 10) workflow ทั่วไป (ตัวอย่างการทำงานจริง)

### อัปเดตไฟล์และ push ขึ้น GitHub

```bash
# 1. ดึงอัปเดตล่าสุด
git pull origin main

# 2. แก้ไขไฟล์ที่ต้องการ
nano config/environment.json

# 3. ตรวจสอบ JSON ก่อน commit
python -c "import json; json.load(open('config/environment.json')); print('OK')"

# 4. Commit และ push
git add config/environment.json
git commit -m "config: อัปเดตค่า environment"
git push origin main
```

### เพิ่ม module ใหม่

```bash
# 1. สร้างไฟล์ module config
nano modules/MyModule.json

# 2. อัปเดต registry
nano modules/registry.json

# 3. รัน audit เพื่อตรวจสอบ
python tools/run_audit.py

# 4. Commit
git add modules/
git commit -m "feat: เพิ่ม MyModule"
git push origin main
```

---

## 11) ปัญหาที่พบบ่อย + วิธีแก้

- **อาการ:** `ModuleNotFoundError: No module named 'jsonschema'`
  **วิธีแก้:** `pip install -r requirements.txt`

- **อาการ:** `pip: command not found`
  **วิธีแก้:** `pkg install python python-pip -y`

- **อาการ:** `java: command not found`
  **วิธีแก้:** `pkg install openjdk-21 -y`

- **อาการ:** `json.decoder.JSONDecodeError`
  **วิธีแก้:** ตรวจ syntax ใน JSON ด้วย `python -m json.tool ชื่อไฟล์.json`

- **อาการ:** `Permission denied` เมื่อรันสคริปต์
  **วิธีแก้:** `chmod +x สคริปต์.py` หรือรันด้วย `python สคริปต์.py`

- **อาการ:** `git push` ไม่ผ่าน (authentication failed)
  **วิธีแก้:** ใช้ Personal Access Token หรือตั้งค่า SSH Key (ดู [termux_github.md](termux_github.md) หัวข้อ 5–6)

- **อาการ:** `python -m http.server` แล้วเปิด HTML ไม่ได้
  **วิธีแก้:** ตรวจว่าอยู่ในโฟลเดอร์ที่มี `portal.html` แล้วเปิด `http://localhost:8080`

---

## Quick Link
- Apps Manual Hub: [`knowledge/apps_manual/INDEX.md`](../INDEX.md)
- Termux + GitHub: [`termux_github.md`](termux_github.md)
- GitHub SSH Keys: [https://github.com/settings/keys](https://github.com/settings/keys)
- GitHub Tokens: [https://github.com/settings/tokens](https://github.com/settings/tokens)
- Termux App: [https://github.com/termux/termux-app/releases](https://github.com/termux/termux-app/releases)
