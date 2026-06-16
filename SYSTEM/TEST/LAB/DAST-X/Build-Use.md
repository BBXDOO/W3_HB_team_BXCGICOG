# Build-Use — คู่มือสร้างและใช้งาน DAST-X

เอกสารนี้เป็นคู่มือภาษาไทยสำหรับติดตั้งและรันแอป **DAST-X** ใน Termux

DAST-X คือ local web app สำหรับดู repo ที่ clone มาแล้วใน Termux โดยเปิดผ่าน Chrome ที่:

```text
http://127.0.0.1:8080/
```

---

## 0. ตำแหน่งไฟล์

ใน repo ให้เข้าโฟลเดอร์นี้:

```bash
cd SYSTEM/TEST/LAB/DAST-X
```

ไฟล์ที่เกี่ยวข้อง:

```text
README.md              # อธิบายแนวคิด
Build-Use.md           # คู่มือสร้างและใช้งานภาษาไทย
requirements.txt       # Python packages ที่ต้องใช้
dast_x_app.py          # โค้ดแอปหลัก
run_dast_x.sh          # สคริปต์ช่วยรัน
commands.example.json  # ตัวอย่าง command library
```

---

## 1. ติดตั้งเครื่องมือใน Termux

ติดตั้ง package พื้นฐาน:

```bash
pkg update
pkg install python git tree ripgrep jq
```

ติดตั้ง Python library:

```bash
pip install -r requirements.txt
```

หรือถ้าต้องติดตั้งเองทีละชื่อ:

```bash
pip install fastapi uvicorn jinja2 markdown pygments psutil
```

---

## 2. เข้า repo ที่ clone ไว้

ตัวอย่าง ถ้า repo อยู่ที่ home:

```bash
cd ~/W3_HB_team_BXCGICOG
```

จากนั้นเข้าโฟลเดอร์ DAST-X:

```bash
cd SYSTEM/TEST/LAB/DAST-X
```

ตรวจว่าตอนนี้อยู่ใน repo จริง:

```bash
git rev-parse --show-toplevel
```

ถ้าคำสั่งนี้แสดง path ของ repo แปลว่าใช้ได้

---

## 3. รันแอปด้วย run_dast_x.sh

ให้สิทธิ์รันไฟล์:

```bash
chmod +x run_dast_x.sh
```

รันแอป:

```bash
./run_dast_x.sh
```

เมื่อรันสำเร็จ จะเห็น server เปิดที่:

```text
http://127.0.0.1:8080/
```

เปิด Chrome แล้วเข้า URL นี้

---

## 4. รันแบบกำหนด repo root เอง

ถ้าต้องการระบุ repo root เอง ให้ใช้ environment variable:

```bash
DASTX_REPO_ROOT="$HOME/W3_HB_team_BXCGICOG" ./run_dast_x.sh
```

หรือรัน Python โดยตรง:

```bash
DASTX_REPO_ROOT="$HOME/W3_HB_team_BXCGICOG" python dast_x_app.py
```

---

## 5. หน้าจอหลัก

หน้าจอหลักมี 3 ส่วนสำคัญ

### 5.1 Header

แสดงข้อมูลรวม:

```text
DAST-X
repo name
branch
Termux / Python / Git
server URL
```

### 5.2 WINDOW A — Repo Tree

ใช้ดูโครงสร้าง repo:

- แตะ folder เพื่อดูรายการด้านใน
- แตะ file เพื่อเปิด viewer
- มีปุ่ม reload tree
- มีช่องกรอก path ภายใน repo

### 5.3 WINDOW B — Termux / Tools / Commands

ใช้ดูข้อมูล Termux และคำสั่ง:

- package count
- command path
- python/git/node/gh
- termux-info ถ้ามี
- saved commands จาก `data/commands.json`
- command พื้นฐานจาก `commands.example.json`

### 5.4 Viewer

ใช้ดูไฟล์:

- `.md` แสดงเป็น Markdown
- `.py`, `.js`, `.json`, `.sh`, `.html`, `.css` แสดงเป็น code พร้อมสี
- `.txt` แสดงเป็น text
- ไฟล์ที่เสี่ยง เช่น `.env`, key, token จะถูก redact บางส่วน

---

## 6. การบันทึก command

DAST-X มี command library สำหรับบันทึกคำสั่งที่ใช้บ่อย แต่ v0.1 ยังไม่รันคำสั่งจากหน้าเว็บ

ตัวอย่าง command ที่ควรบันทึก:

```bash
git status
python --version
tree -L 2
rg "TODO" .
python -m pytest
```

ตำแหน่งไฟล์ข้อมูล runtime:

```text
SYSTEM/TEST/LAB/DAST-X/data/commands.json
```

ถ้าไม่มีไฟล์นี้ แอปจะสร้างให้เองจาก `commands.example.json`

---

## 7. ขอบเขตความปลอดภัยใน v0.1

เพื่อความปลอดภัย v0.1 ไม่ใช่ terminal เต็มรูปแบบ

หลักการคือ:

```text
ใช้ดูและติดตามงานก่อน
ยังไม่ใช้สั่งแก้ระบบโดยตรง
คำสั่งที่กระทบไฟล์หรือ git history ต้องทำเองใน Termux หลังตรวจแล้วเท่านั้น
```

---

## 8. คำสั่งตรวจสอบเมื่อมีปัญหา

ดูว่า server ยังรันอยู่ไหม:

```bash
ps aux | grep dast_x_app
```

หยุด server ด้วย `CTRL + C`

ถ้า port 8080 ถูกใช้แล้ว ให้เปลี่ยน port:

```bash
DASTX_PORT=8090 ./run_dast_x.sh
```

แล้วเปิด:

```text
http://127.0.0.1:8090/
```

---

## 9. วิธีเปิดจาก Termux ไป Chrome

ถ้ามีคำสั่ง `termux-open-url`:

```bash
termux-open-url http://127.0.0.1:8080/
```

ถ้าไม่มี ให้เปิด Chrome เองแล้วพิมพ์:

```text
http://127.0.0.1:8080/
```

---

## 10. สรุปขั้นตอนรวดเดียว

```bash
cd ~/W3_HB_team_BXCGICOG/SYSTEM/TEST/LAB/DAST-X
pkg install python git tree ripgrep jq
pip install -r requirements.txt
chmod +x run_dast_x.sh
./run_dast_x.sh
```

จากนั้นเปิด:

```text
http://127.0.0.1:8080/
```

---

## 11. เป้าหมายของเอกสารนี้

เอกสารนี้เขียนเพื่อให้เจ้าของเครื่องสามารถ:

1. ติดตั้งได้เองใน Termux
2. รันแอปได้เอง
3. เปิดดู repo ได้โดยไม่ต้องพิมพ์คำสั่งมั่ว
4. อ่านไฟล์/Markdown/code ได้ในหน้าเดียว
5. เก็บคำสั่งที่ใช้บ่อยไว้เป็นระบบ
