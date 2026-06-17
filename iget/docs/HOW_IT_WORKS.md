# How IGET Works

อธิบายการทำงานภายในของ IGET v9.0

## ระบบนี้คืออะไร

IGET เป็น PR governance runtime ที่รับข้อมูล Pull Request จาก GitHub แล้วเปลี่ยนเป็นรายงานสำหรับมนุษย์

## โครงสร้าง runtime

```text
main.py
→ fetcher.py
→ scorer.py
→ reporter.py
→ proof.py
```

## โมดูลหลัก

| ไฟล์ | หน้าที่ |
|---|---|
| main.py | entrypoint, resolve runtime context, run workflow |
| fetcher.py | ติดต่อ GitHub API และดึง PR files |
| scorer.py | classify, stats, mode, score, state, semantic state |
| reporter.py | สร้าง summary comment / recommendations / inline comments |
| proof.py | เก็บ proof trace ว่าคะแนนและผลเกิดจากอะไร |
| config.py | runtime constants, threshold, semantic states |

## สถานการณ์ที่ทดสอบ / ใช้งาน

ตัวอย่าง PR หนึ่งอาจมี:

```text
- ไฟล์ code 3 ไฟล์
- docs 1 ไฟล์
- ไม่มี test
- changes 500 บรรทัด
```

IGET จะอ่านและแปลงเป็น:

```text
classified files
numeric stats
mode=mixed/code/docs_only/test_only
score
state green/yellow/red
semantic_state safe/caution/critical/unknown
```

## ลอจิกหลัก

1. แยกชนิดไฟล์
2. คำนวณจำนวนไฟล์และ changes
3. ตรวจ risky file / workflow file
4. ตรวจว่ามี code แต่ไม่มี test หรือไม่
5. ให้ penalty / bonus
6. map score เป็นสี
7. สร้าง semantic state ภาษาไทย
8. สร้าง proof trace

## สิ่งที่ต้องการชี้ให้เห็น

IGET ไม่ได้ดูแค่จำนวนไฟล์ แต่ดู pattern ความเสี่ยงของ PR เช่น:

```text
ไฟล์เยอะ + changes เยอะ + ไม่มี test
= ต้องระวังมากขึ้น
```

## ข้อสังเกต

- IGET ไม่รัน code จาก PR
- IGET ไม่ merge เอง
- Inline comments เป็น opt-in
- Summary comment ถูก update ด้วย marker เพื่อลด comment ซ้ำ
