# Scoring Rules

กติกาคะแนนของ IGET v9.0

## Base Score

```text
เริ่มต้น = 100
```

จากนั้นระบบจะหักคะแนนหรือเพิ่มคะแนนตามสัญญาณของ PR

## Penalty

| เงื่อนไข | ผล |
|---|---|
| ไฟล์มากกว่า `FILES_WARN` | หักคะแนนระดับเตือน |
| ไฟล์มากกว่า `FILES_LARGE` | หักคะแนนระดับใหญ่ |
| changes มากกว่า `CHANGES_WARN` | หักคะแนนระดับแก้เยอะ |
| changes มากกว่า `CHANGES_LARGE` | หักคะแนนระดับหนักมาก |
| มี code change แต่ไม่มี test | หักตามจำนวน code files |
| พบ risky file | หักหนัก |
| มี workflow change | หักเพราะกระทบ CI / permission / runtime |

## Bonus

| เงื่อนไข | ผล |
|---|---|
| docs only | เพิ่มคะแนนเล็กน้อย |
| PR เล็กและ changes ต่ำ | เพิ่มคะแนน |
| มี code และ test คู่กัน | เพิ่มคะแนน |

## State Mapping

```text
85 - 100 = Green
60 - 84  = Yellow
0 - 59   = Red
```

## Semantic State

| state | ความหมาย |
|---|---|
| safe | PR ผ่านเกณฑ์ ไม่มีความเสี่ยงสำคัญ |
| caution | PR มีจุดควรตรวจสอบ |
| critical | PR เสี่ยงสูง หรือต่ำกว่าเกณฑ์ |
| unknown | ระบบจำแนกไม่ได้ |

## ต้องการชี้ให้เห็นอะไร

คะแนนไม่ใช่คำสั่ง merge แต่เป็นตัวบอกแรงกดดันของ PR

ตัวอย่าง:

```text
PR เล็ก + docs only
= มีแนวโน้ม Green

PR ใหญ่ + code เยอะ + ไม่มี test
= มีแนวโน้ม Yellow / Red

PR แก้ workflow หรือมี secret keyword
= ต้องตรวจละเอียด
```

## การนำมาใช้

ใช้ประกอบการ review:

```text
Green  → ตรวจขั้นสุดท้ายได้เร็ว
Yellow → review เพิ่มตามเหตุผลที่ระบบบอก
Red    → หยุดก่อน ตรวจละเอียด
```

## ข้อสังเกต

Threshold อยู่ใน `iget/config.py` และควรแก้ด้วยความระวัง เพราะมีผลต่อ PR ทั้งระบบ
