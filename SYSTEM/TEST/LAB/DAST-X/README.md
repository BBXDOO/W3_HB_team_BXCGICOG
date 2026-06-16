# DAST-X — Termux Repo Desk

**สถานะ:** ACTIVE DRAFT / LAB  
**ตำแหน่ง:** `SYSTEM/TEST/LAB/DAST-X/`  
**เจ้าของแนวคิด:** BBX19  
**เป้าหมาย:** สร้างแอป local สำหรับดู repo ที่ clone อยู่ใน Termux โดยลดความเสี่ยงจากการพิมพ์คำสั่งผิดใน terminal

---

## 1. DAST-X คืออะไร

DAST-X คือแอปแบบ **Local Web App ใน Termux** สำหรับเปิดผ่าน Chrome ที่เครื่องเดียวกัน เช่น

```text
http://127.0.0.1:8080/
```

แอปนี้ทำหน้าที่เป็น **Repo Control Desk / Termux Repo Viewer** ไม่ใช่ terminal เต็มรูปแบบ

เป้าหมายหลักคือ:

- ดู repo ที่ clone ไว้ใน Termux
- ดู tree ของ folder/file
- แตะไฟล์แล้วอ่านเนื้อหา
- แสดง Markdown ได้
- แสดง code พร้อม syntax highlight
- ดูข้อมูล Termux, package, tools, path คำสั่งสำคัญ
- บันทึกคำสั่งที่ใช้บ่อยไว้เป็น command library
- ลดการพิมพ์มั่ว ลดความเสี่ยงลบไฟล์หรือสั่งผิด

---

## 2. ภาพรวมหน้าจอ

```text
┌──────────────────────────────────────────────┐
│ DAST-X | repo name | branch | Termux info     │
├─────────────────────┬────────────────────────┤
│ WINDOW A            │ WINDOW B               │
│ Repo Folder Tree    │ Termux / Package / Tool │
│ root-repo           │ Saved Commands          │
├─────────────────────┴────────────────────────┤
│ Long Viewer                                  │
│ - Markdown viewer                            │
│ - Code viewer + syntax highlight             │
│ - Plain text / JSON preview                  │
└──────────────────────────────────────────────┘
```

### WINDOW A — Repo

ใช้แสดง root repo และโครงสร้างโฟลเดอร์ เช่น:

```text
repo-root/
├── protocol/
├── croll/
├── knowledge/
├── SYSTEM/
└── README.md
```

เมื่อแตะ folder จะขยาย tree  
เมื่อแตะ file จะแสดงเนื้อหาใน viewer

### WINDOW B — Termux / Tools

ใช้แสดง:

- Python / Git / Node / gh
- pkg / apt / termux-info
- command path เช่น `command -v python`
- package count
- saved commands
- command พื้นฐาน
- command สำหรับ health check / API check

---

## 3. เครื่องมือจากภาพที่ใช้เป็นแนวอ้างอิง

จากชุดแอปในเครื่อง สามารถใช้เป็นแนวทางออกแบบ workflow ได้ เช่น:

- **GitHub / GitHub Docs / Codespaces** — ดู repo, issue, docs, branch
- **Termux / Termius / Cloud Shell** — terminal, ssh, local server
- **VS Code / Code Studio / Code Inside / TrebEdit** — code editor / viewer
- **Python / Learn Python / Compiler** — runtime และ test scripts
- **YAML / JSON / XML / CSV viewers** — file format viewer
- **API Client / Network tools** — ทดสอบ API และ endpoint
- **SQLite editor** — ดูฐานข้อมูล local
- **Markdown editor / Obsidian / Notion / OneNote** — อ่านและจัดเอกสาร
- **Files / PDF viewer / Gallery** — เปิด output และเอกสาร

DAST-X ไม่ได้บังคับใช้ทุกแอปด้านบน แต่ใช้แนวคิดจากเครื่องมือเหล่านี้เพื่อสร้างหน้ากลางสำหรับดูงานใน repo

---

## 4. ขอบเขตความปลอดภัย

DAST-X v0.1 ตั้งใจให้เป็น **read-only ก่อน**

ทำได้:

- อ่านไฟล์
- ดู folder tree
- ดู Markdown
- ดู code
- ดู git status แบบอ่านอย่างเดียว
- บันทึก command library ลงไฟล์ข้อมูลของ DAST-X

ยังไม่ทำใน v0.1:

- ไม่ลบไฟล์
- ไม่ย้ายไฟล์
- ไม่ push
- ไม่ reset
- ไม่ clean
- ไม่รัน command อิสระแบบ terminal

คำสั่งเสี่ยงที่ต้องกันไว้:

```text
rm
mv
git reset
git clean
git push
chmod -R
pkg uninstall
pip uninstall
```

---

## 5. ไฟล์ในชุดนี้

```text
SYSTEM/TEST/LAB/DAST-X/
├── README.md
├── Build-Use.md
├── requirements.txt
├── run_dast_x.sh
├── dast_x_app.py
└── commands.example.json
```

ไฟล์หลักที่ใช้รันแอปคือ:

```text
dast_x_app.py
```

ไฟล์ช่วยรันคือ:

```text
run_dast_x.sh
```

ขั้นตอนติดตั้งและใช้งานอยู่ใน:

```text
Build-Use.md
```

---

## 6. เป้าหมายระยะต่อไป

v0.1:

- local app เปิดผ่าน Chrome
- repo tree
- file viewer
- markdown/code render
- Termux tools panel
- saved commands

v0.2:

- search file / search text ด้วย ripgrep
- export report เป็น `.md` / `.html`
- API/health panel แบบอ่านอย่างเดียว

v0.3:

- safe command runner แบบ whitelist
- ปุ่ม test เฉพาะรายการที่กำหนด
- trace log สำหรับงาน W3

---

## 7. หลักการของ DAST-X

```text
ดูให้ชัดก่อนสั่ง
อ่านให้ครบก่อนแก้
ลดการพิมพ์มั่ว
ลดความเสี่ยงกับ repo
ให้ Termux เป็นฐานทำงาน แต่ไม่ต้องจำทุกคำสั่งเอง
```
