# ติดตั้ง IGET v9 ใน GitHub Repository

คู่มือนี้จัดทำสำหรับผู้เริ่มใช้ GitHub และต้องการนำ IGET ไปช่วยอ่าน Pull Request (PR)

> IGET อ่านข้อมูลการเปลี่ยนแปลงของ PR แล้วสร้างรายงานสรุปเป็นคะแนน สี ความเสี่ยง เหตุผล และคำแนะนำ  
> IGET ไม่แก้ไฟล์ใน PR ไม่รันโค้ดจาก PR และไม่อนุมัติหรือ Merge แทนเจ้าของ Repository

## สิ่งที่จะเกิดขึ้นหลังติดตั้ง

เมื่อเปิดหรืออัปเดต PR ที่ไม่ใช่ Draft:

1. GitHub Actions เรียก IGET
2. IGET อ่านรายการไฟล์และจำนวนบรรทัดที่เปลี่ยนผ่าน GitHub API
3. IGET จำแนกประเภทงานและสัญญาณความเสี่ยง
4. IGET ทดสอบ Runtime ของตัวเองก่อนทำงาน
5. IGET สร้างหรืออัปเดต Summary Comment หนึ่งรายการใน PR
6. มนุษย์ใช้รายงานประกอบการ Review และตัดสินใจ

สีเป็นสัญญาณสำหรับตัดสินใจเร็ว ไม่ใช่คำตัดสินสุดท้าย:

- 🟩 Green — ความเสี่ยงต่ำหรือพร้อมพิจารณาต่อ
- 🟨 Yellow — ควรตรวจเพิ่มเติม
- 🟥 Red — ควรหยุดและตรวจรายละเอียดก่อน

## สิ่งที่ต้องนำไปไว้ใน Repository ปลายทาง

ต้องมีครบสองส่วน:

```text
iget/                         # Runtime, tests และ requirements ของ IGET
.github/workflows/iget.yml    # ตัวเรียก IGET เมื่อเกิด PR
```

ห้ามคัดลอกเฉพาะ `main.py` เพราะ IGET ใช้ไฟล์ประกอบภายในโฟลเดอร์ `iget/`

## วิธี A — ติดตั้งผ่านหน้าเว็บ GitHub

เหมาะกับผู้ที่ยังไม่ถนัดคำสั่ง Git

1. เปิด Repository ต้นทางของ W3 ที่ Branch `refactor/v0.2`
2. ดาวน์โหลด Source code เป็น ZIP แล้วแตกไฟล์
3. เปิด Repository ของตนเองใน GitHub
4. เลือก **Add file → Upload files**
5. อัปโหลดโฟลเดอร์ `iget/` โดยรักษาชื่อและโครงสร้างเดิม
6. สร้างไฟล์ `.github/workflows/iget.yml` แล้วคัดลอกเนื้อหาจากไฟล์เดียวกันใน W3
7. Commit ลง Branch สำหรับติดตั้ง เช่น `setup/iget`
8. เปิด PR เพื่อนำ Branch นี้เข้า Default Branch
9. ตรวจแท็บ **Actions** และ Merge เมื่อพร้อม

ข้อสำคัญ: Workflow ต้องอยู่ใน Default Branch ก่อน จึงจะทำงานกับ PR รุ่นถัดไปอย่างสม่ำเสมอ

## วิธี B — ติดตั้งด้วย Git

ตัวอย่างนี้สมมุติว่า W3 และ Repository ปลายทางอยู่ในเครื่องเดียวกัน

```bash
git clone --branch refactor/v0.2 \
  https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git w3-iget-source

git clone https://github.com/OWNER/TARGET_REPO.git target-repo

cd target-repo
git switch -c setup/iget

cp -R ../w3-iget-source/iget ./iget
mkdir -p .github/workflows
cp ../w3-iget-source/.github/workflows/iget.yml .github/workflows/iget.yml

python -m pip install -r iget/requirements-dev.txt
python -m pytest iget/tests -q

git add iget .github/workflows/iget.yml
git commit -m "ci: install IGET v9 PR assistant"
git push -u origin setup/iget
```

เปลี่ยน `OWNER/TARGET_REPO` ให้เป็นชื่อ Repository จริง แล้วเปิด PR จาก Branch `setup/iget`

## ตั้งค่า GitHub Actions

ไปที่:

```text
Repository → Settings → Actions → General
```

ตรวจว่า:

- Actions สามารถทำงานได้
- Workflow ได้รับสิทธิ์อ่าน Contents
- Workflow สามารถเขียน Pull Request/Issue Comment ตามสิทธิ์ที่ระบุใน `iget.yml`

Workflow ใช้ `github.token` ที่ GitHub สร้างให้ระหว่างการทำงาน จึงไม่ต้องนำ Personal Access Token ไปเขียนไว้ในไฟล์

## ทดลองครั้งแรก

หลัง Merge ชุดติดตั้งเข้า Default Branch:

1. สร้าง Branch ทดลอง
2. แก้ไฟล์เล็กหนึ่งไฟล์
3. Commit และ Push
4. เปิด Pull Request และเอาสถานะ Draft ออก
5. เปิดแท็บ **Actions**
6. เลือก Workflow **IGET v9**
7. รอ Job **Analyze PR with IGET v9**
8. กลับไปดู Summary Comment ในหน้า PR

ถ้า Workflow ผ่านแต่ไม่มี Comment ให้ดูหัวข้อแก้ปัญหาด้านล่าง

## เรียกตรวจ PR ด้วยตนเอง

1. เปิดแท็บ **Actions**
2. เลือก **IGET v9**
3. กด **Run workflow**
4. ใส่หมายเลข PR
5. กดเริ่มทำงาน

Manual Run ต้องระบุหมายเลข PR เสมอ

## ทดสอบโดยยังไม่โพสต์ Comment

รันจาก Root ของ Repository:

```bash
python -m pip install -r iget/requirements-dev.txt

REPO=OWNER/REPO \
PR=1 \
GITHUB_TOKEN=YOUR_TOKEN \
IGET_DRY_RUN=1 \
PYTHONPATH=. python -m iget.main
```

คำสั่งนี้ใช้สำหรับทดสอบในเครื่อง ควรส่ง Token ผ่าน Environment เท่านั้น ห้ามเขียน Token ลง Source code, Commit, Screenshot หรือไฟล์รายงาน

## ความปลอดภัยของ Workflow

IGET ใช้ `pull_request_target` เพื่อให้สามารถรายงานใน PR ได้ แต่ Workflow ถูกออกแบบให้ Checkout เฉพาะโค้ดของ Base Branch ที่เชื่อถือได้

IGET:

- อ่าน Changed-file metadata ผ่าน GitHub API
- ไม่ Checkout และไม่ Execute โค้ดจาก Branch ของผู้ส่ง PR
- ไม่ Merge
- ไม่เปลี่ยน Source code
- ใช้ Summary Comment แบบอัปเดตรายการเดิม เพื่อลด Comment ซ้ำ
- ปิด Inline Comment เป็นค่าเริ่มต้น

หากมีการแก้ Workflow ในอนาคต ต้องรักษาหลักนี้ไว้: **ห้าม Checkout หรือรันโค้ดที่มาจาก PR ซึ่งไม่น่าเชื่อถือภายใต้ `pull_request_target`**

## ปัญหาที่พบบ่อย

### Actions ไม่ทำงาน

ตรวจว่า:

- ไฟล์อยู่ตรง `.github/workflows/iget.yml`
- Workflow อยู่ใน Default Branch แล้ว
- GitHub Actions ไม่ถูกปิดใน Settings
- PR ไม่ได้อยู่ในสถานะ Draft

### Tests ไม่ผ่าน

รัน:

```bash
python -m pip install -r iget/requirements-dev.txt
python -m pytest iget/tests -q
```

อย่าข้ามขั้น **Verify trusted IGET runtime** เพื่อบังคับให้รายงานออกมา เพราะผลที่ถูกต้องสำคัญกว่าการทำให้ Workflow เป็นสีเขียว

### Workflow ผ่านแต่ไม่มี Comment

ตรวจว่า:

- `pull-requests: write` และ `issues: write` ยังอยู่ใน Workflow
- Repository หรือองค์กรไม่ได้จำกัดสิทธิ์ของ GitHub Actions
- หมายเลข PR ถูกต้อง
- Run นั้นมาจาก Event ที่รองรับ
- Summary Marker `<!-- iget:summary -->` ไม่ถูกแก้ไข

### คะแนนไม่ตรงกับบริบท

คะแนนเป็น Signal จากไฟล์ จำนวนการเปลี่ยนแปลง Test และคำเสี่ยง ไม่ใช่คำตัดสินว่าโค้ดถูกหรือผิด

ให้อ่าน:

- เหตุผลที่ถูกหักคะแนน
- ประเภทไฟล์ที่ IGET ตรวจพบ
- ข้อจำกัดของรายงาน
- ผล Test และความเห็นของ Human Reviewer

## ถอนการใช้งาน

หากต้องการหยุดชั่วคราว ให้ Disable Workflow ในแท็บ Actions

หากต้องการถอนออก ให้ทำผ่าน PR โดยลบ:

```text
.github/workflows/iget.yml
iget/
```

การลบ Workflow ไม่ได้ลบ Comment เก่าที่เคยบันทึกใน PR

## ขอบเขตความจริงของผลลัพธ์

IGET ช่วยตอบว่า:

- PR เปลี่ยนไฟล์อะไรและมากน้อยเพียงใด
- มีสัญญาณความเสี่ยงประเภทใด
- มี Test ประกอบหรือไม่
- ควรอ่านหรือตรวจจุดใดต่อ

IGET ไม่ได้พิสูจน์โดยลำพังว่า:

- โค้ดทำงานถูกต้องทุกกรณี
- ไม่มีช่องโหว่
- เจตนาของผู้เขียนถูกต้อง
- PR พร้อม Merge โดยไม่ต้องให้มนุษย์ตรวจ

ดังนั้นผลลัพธ์ที่เหมาะสมคือ:

```text
IGET Report
→ Human reads evidence
→ Human reviews context
→ Human decides
```

## เอกสารอ่านต่อ

- `iget/README.md` — ภาพรวมและขอบเขต
- `iget/docs/HOW_TO_USE.md` — วิธีใช้งาน
- `iget/docs/HOW_IT_WORKS.md` — กลไกภายใน
- `iget/docs/TROUBLESHOOT.md` — แก้ปัญหา
- `iget/docs/PR_EXAMPLES.md` — ตัวอย่างผลจาก PR
- `iget/docs/INDEX.md` — สารบัญเอกสาร

---

สถานะคู่มือนี้: Setup guide สำหรับ IGET v9  
ขอบเขต: Installation / PR reporting / Human review  
Mutation authority: ไม่มี  
Final decision: เจ้าของหรือ Maintainer ของ Repository
