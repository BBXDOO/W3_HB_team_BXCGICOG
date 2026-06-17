# How To Use IGET

คู่มือใช้งาน IGET สำหรับ Pull Request governance

## เทสนี้ / ระบบนี้คืออะไร

IGET เป็น runtime ช่วยประเมิน Pull Request โดยอ่านไฟล์ที่เปลี่ยน จำนวนบรรทัด ความเสี่ยง ประเภทงาน และ test ที่เกี่ยวข้อง แล้วสรุปเป็นคะแนน สี และคำแนะนำ

## วิธีใช้งานหลัก

### 1. ใช้งานผ่าน GitHub Workflow

ระบบทำงานเมื่อมี Pull Request หรือ manual dispatch ที่ระบุ PR number

```text
PR Open / Update
→ GitHub workflow
→ IGET runtime
→ Summary comment
```

### 2. ใช้งานแบบ manual dispatch

ใช้เมื่ออยากตรวจ PR เฉพาะหมายเลข หรือ rerun แบบควบคุมได้

ต้องมี:

```text
REPO = owner/repository
PR = pull request number
GITHUB_TOKEN = token ที่มีสิทธิ์อ่าน PR และเขียน comment
```

### 3. ใช้งานแบบ dry-run

ใช้ทดสอบก่อนโพสต์ comment จริง

```bash
REPO=OWNER/REPO PR=1 GITHUB_TOKEN=xxx IGET_DRY_RUN=1 \
PYTHONPATH=. python -m iget.main
```

## ขั้นตอนที่ระบบทำ

```text
resolve runtime context
→ fetch PR files
→ classify files
→ build numeric stats
→ detect PR mode
→ compute score
→ map state
→ build semantic state
→ build comment
→ upsert comment
```

## Human Action

หลัง IGET โพสต์ผล:

1. อ่านคะแนนและสี
2. ตรวจเหตุผลที่ถูกหักคะแนน
3. ดู semantic state
4. ตรวจคำแนะนำ
5. ตัดสินใจ merge / request change / review เพิ่ม

## Best Practice

- ทำ PR ให้เล็ก
- แยก docs / code / workflow ออกจากกันเมื่อทำได้
- มี test เมื่อแก้ code
- หลีกเลี่ยง secret หรือไฟล์เสี่ยง
- ไม่รวมหลาย feature ใน PR เดียว

## สิ่งที่คาดหวัง

IGET ควรช่วยให้เห็นว่า PR นี้:

```text
พร้อม merge
ต้อง review เพิ่ม
หรือควรหยุดตรวจละเอียด
```

## ข้อสังเกต

IGET เป็นตัวช่วย ไม่ใช่ authority สุดท้าย Maintainer ยังต้องตัดสินใจเองเสมอ
