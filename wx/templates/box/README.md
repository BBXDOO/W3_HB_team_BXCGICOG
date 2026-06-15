# wx:BOX Template Family

> Status: draft / observe  
> Runtime: none  
> Mutation: false  
> Owner approval: BBX19  
> Source truth: GitHub

`wx:BOX` คือรูปแบบกล่องอ้างอิงแบบเบาใน BOX / Library-WX
ใช้รวมแนวคิดของ CN-Fold เข้ามาเป็นพฤติกรรมของ folder/node โดยไม่สร้าง runtime ใหม่และไม่ล็อกไฟล์หนักเกินจำเป็น

```text
wx:BOX = manifest + reference container + folder/node context
CN-Fold concept = host + relation + boundary + status behavior inside BOX
```

## บทบาท

`wx:BOX` มีหน้าที่:

- บอกว่ากล่องนี้คืออะไร
- ชี้ไปหา identity, registry, template, blueprint หรือ source truth
- บอก host / parent / child relation
- บอก boundary และ status เบื้องต้น
- ทำให้ folder หรือกลุ่มเอกสารกลายเป็น node ที่ระบบอื่นอ่านบริบทได้

`wx:BOX` ไม่ทำหน้าที่:

- execute runtime
- แก้ source truth
- copy template ไป workspace เอง
- กลายเป็น identity เอง
- บังคับ implementation ของระบบอื่น

## หลักสำคัญ

```text
อะไรที่ไม่จำเป็นต้องล็อก → ใช้ reference
อะไรที่เป็น source truth → ชี้ไปหา source truth
อะไรที่เป็น identity → ชี้ไปหา IDP หรือ registry
อะไรที่เปลี่ยนตามงาน → อยู่ใน Paper หรือ workspace copy
```

## ไฟล์ในชุดนี้

- `wx_box_minimum.md` — template ขั้นต่ำของ wx:BOX
- `USAGE_TH.md` — คู่มือใช้งาน wx:BOX ภาษาไทย

## ความสัมพันธ์กับ CN-Fold

CN-Fold ไม่ต้องเป็น protocol แยกในรอบนี้ แต่ใช้เป็นแนวคิดภายใน `wx:BOX`:

```text
CN-Fold identity      → BOX.identity / box_id
CN-Fold host scope    → BOX.host
CN-Fold parent/child  → BOX.relations
CN-Fold boundary      → BOX.boundary
CN-Fold status        → BOX.status
CN-Fold index         → BOX.index
CN-Fold source_truth  → BOX.refs.source_truth
CN-Fold registry      → BOX.refs.registry
```

## Minimum rule

```text
BOX รู้ว่า “จะไปดูอะไรที่ไหน”
BOX ไม่ควรกลายเป็นทุกสิ่งเอง
```
