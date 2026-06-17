# Signal System

ระบบสีและสัญญาณของ IGET

## Green

```text
พร้อมตรวจขั้นสุดท้าย / merge ได้เมื่อมนุษย์เห็นว่าเหมาะสม
```

สัญญาณทั่วไป:

- คะแนนสูง
- ไม่มี risky file
- PR ไม่ใหญ่เกินไป
- test หรือ docs สอดคล้องกับประเภทงาน

## Yellow

```text
มีความเสี่ยงบางส่วน ควร review เพิ่ม
```

สัญญาณทั่วไป:

- changes เยอะ
- มี code แต่ไม่มี test
- มีหลายชนิดงานรวมกัน
- PR ใหญ่พอควร

## Red

```text
หยุดก่อน ต้องตรวจละเอียด
```

สัญญาณทั่วไป:

- คะแนนต่ำ
- พบ risky keyword / risky file
- changes หนักมาก
- workflow หรือ permission path ถูกแก้

## Semantic State

IGET มี semantic state เพื่ออธิบายความหมายของสี:

```text
safe     = ปลอดภัยพอสำหรับตรวจขั้นสุดท้าย
caution  = มีจุดควรระวัง
critical = เสี่ยงสูง ต้องตรวจละเอียด
unknown  = ระบบไม่มั่นใจพอ
```

## ตัวอย่าง Visual Flow

```text
🟩🟩🟨🟩 Stable
🟨🟥🟨 Need Review
🟥🟥🟨 Stop Before Merge
```

## ต้องการชี้ให้เห็นอะไร

สีทำให้เห็นภาพเร็ว แต่เหตุผลและ proof trace ยังสำคัญกว่า

สีคือสัญญาณนำทาง ไม่ใช่คำสั่งสุดท้าย

## การนำมาใช้

- ใช้สีเพื่อเลือกความเร็วในการ review
- ใช้เหตุผลเพื่อหาจุดที่ต้องอ่านจริง
- ใช้ proof trace เพื่อตรวจว่าคะแนนมาจากอะไร

## ข้อสังเกต

Green ยังต้องมี human final check เสมอ โดยเฉพาะ PR ที่แตะ workflow, config, secret path หรือ runtime boundary
