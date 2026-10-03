---
AM_TYPE: II
ROLE: ADAPTATION
GROUP: LEARN
DERIVED_FROM:
  - "requests/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001.md"
OWNER: "BBX19"
MAKER: "Copilot-Gm"
STATUS: "waiting_human"
REQUEST_ID: "RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001"
CREATED_AT: "2026-10-03T10:08:04Z"
---

# คู่มือการใช้ Markdown ฉบับภาษาไทย

## Head line

1. Name: คู่มือการใช้ Markdown ฉบับภาษาไทย
2. AM II - LEARN: ADAPTATION
3. ID: RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001
4. Note: Copilot-Gm draft; Gemini validated; BBX19 sign-off required

## Body line

คู่มือนี้อธิบาย Markdown สำหรับผู้เริ่มต้น โดยแยกสิ่งที่เป็น Markdown
มาตรฐาน, GitHub Flavored Markdown (GFM), HTML/CSS และความสามารถที่ขึ้นกับ renderer
อย่างชัดเจน

> **หลักสำคัญ:** Markdown เน้นโครงสร้างของเนื้อหา ไม่ได้กำหนดสี ขนาด หรือเส้นขอบ
> แบบระบบจัดหน้าเต็มรูปแบบ ความสามารถด้านรูปลักษณ์จึงต้องตรวจ renderer ที่ใช้งานเสมอ

## 1. รูปแบบพื้นฐาน

### หัวข้อและย่อหน้า

```md
# หัวข้อระดับ 1
## หัวข้อระดับ 2
### หัวข้อระดับ 3

ย่อหน้าแรก

ย่อหน้าที่สอง แยกด้วยบรรทัดว่าง
```

### รายการและลำดับเลข

```md
- รายการแบบจุด
  - รายการย่อย

1. ขั้นตอนแรก
2. ขั้นตอนถัดไป
```

### โค้ด

ใช้ backtick ครอบโค้ดสั้น เช่น `` `print("W3")` `` และใช้รั้วสาม backticks
สำหรับ code block:

````md
```python
print("Build. Observe. Learn. Continue.")
```
````

## 2. การสร้างตาราง

```md
| ชื่อ | สถานะ | หมายเหตุ |
|:---|:---:|---:|
| W3 | พร้อม | ขวา |
| BOX | ตรวจสอบ | ขวา |
```

- `:---` จัดซ้าย, `:---:` จัดกึ่งกลาง และ `---:` จัดขวา
- ตารางเป็นความสามารถเด่นของ GFM ไม่ใช่ CommonMark ขั้นต่ำทุกตัว
- ตาราง Markdown ไม่รองรับการรวมเซลล์ สีพื้นหลัง หรือเส้นขอบแบบละเอียดโดยตรง
- หากข้อความมี `|` ให้ escape เป็น `\|` หรือใช้ HTML ตาม renderer

## 3. สีพื้นหลังของตาราง

Markdown มาตรฐานไม่มีไวยากรณ์กำหนดสีพื้นหลัง ตารางที่ต้องการสีต้องพึ่ง HTML/CSS:

```html
<table>
  <tr style="background-color: #fff3cd;">
    <th>สถานะ</th><th>ความหมาย</th>
  </tr>
  <tr><td>รอตรวจ</td><td>WAITING_HUMAN</td></tr>
</table>
```

ตัวอย่างนี้ **ขึ้นกับ renderer** โดย GitHub อาจกรองแอตทริบิวต์ `style` จึงไม่ควรใช้สี
เป็นหลักฐานสถานะเพียงอย่างเดียว ควรมีข้อความกำกับเสมอ

## 4. สีและข้อความ

Markdown ไม่มีคำสั่งสีข้อความมาตรฐาน ตัวอย่าง fallback:

```html
<span style="color: #c62828;">ข้อความสีแดง</span>
```

HTML/CSS อาจใช้ได้ใน Obsidian หรือ renderer ที่อนุญาต แต่ GitHub อาจตัด style ออก
และ Pure Writer ขึ้นกับโหมด preview/renderer ที่เลือก จึงต้องทดลองกับปลายทางจริง

## 5. การสร้างลิงก์

```md
[ข้อความลิงก์](https://example.com)
<https://example.com>
![คำอธิบายภาพ](images/example.png)
[ไปยังหัวข้อการสร้างตาราง](#2-การสร้างตาราง)
[อ่านไฟล์ใกล้เคียง](./README.md)
[ย้อนขึ้นหนึ่งระดับ](../README.md)
```

- ใช้ relative path เมื่อไฟล์อยู่ใน repository เดียวกัน
- anchor ถูกสร้างต่างกันได้ตาม renderer โดยเฉพาะภาษาไทยและหัวข้อที่มีสัญลักษณ์
- หลีกเลี่ยง URL ติดตามและตรวจว่าไฟล์ปลายทางมีอยู่จริงก่อนเผยแพร่

## 6. ตัวหนา ตัวเอียง ขีดฆ่า และขีดเส้นใต้

```md
**ตัวหนา**
*ตัวเอียง*
***หนาและเอียง***
~~ขีดฆ่า~~
<u>ขีดเส้นใต้</u>
```

ตัวหนาและตัวเอียงเป็น Markdown ทั่วไป ส่วนขีดฆ่าเป็น GFM และ `<u>` เป็น HTML
ซึ่งขึ้นกับ renderer

## 7. เส้นแนวนอนและเส้นแนวตั้ง

เส้นแนวนอนมาตรฐานเขียนได้ดังนี้:

```md
---
```

ควรมีบรรทัดว่างก่อนเส้น เพื่อไม่ให้ `---` ถูกตีความเป็นหัวข้อแบบ Setext
Markdown ไม่มีเส้นแนวตั้งอิสระ เครื่องหมาย `|` เป็นเพียงตัวแบ่งคอลัมน์ในตาราง
หากต้องการเส้นตกแต่งให้ใช้ HTML/CSS และยอมรับว่าอาจไม่ทำงานทุก renderer:

```html
<div style="border-left: 4px solid #4a90e2; padding-left: 12px;">
  ข้อความข้างเส้นแนวตั้ง
</div>
```

## 8. การเพิ่มความหนาของเส้น

ความหนาเส้นไม่ใช่ความสามารถของ Markdown ต้องใช้ CSS เช่น:

```html
<hr style="border: 0; border-top: 6px solid #333;">
```

บน GitHub อาจถูกกรอง style ออก ทางเลือกที่เข้ากันได้ดีกว่าคือใช้ `---` แล้วปล่อยให้
ธีมหรือ renderer เป็นผู้กำหนดรูปแบบ

## 9. เทคนิคเพิ่มเติม

### Blockquote และ checklist

```md
> ข้อความอ้างอิง

- [x] ทำแล้ว
- [ ] ยังไม่ทำ
```

Checklist เป็น GFM และอาจแสดงเป็นกล่องที่คลิกไม่ได้ในบางโปรแกรม

### Details/summary

```html
<details>
<summary>แตะเพื่อดูรายละเอียด</summary>

เนื้อหาที่ซ่อนไว้
</details>
```

นี่คือ HTML fallback และขึ้นกับ renderer

### Escaping และการขึ้นบรรทัดใหม่

```md
\*ไม่ให้เป็นตัวเอียง\*
บรรทัดแรก\
บรรทัดที่สอง
```

ใช้ backslash หน้าสัญลักษณ์เพื่อแสดงตัวอักษรตามจริง การเว้นสองช่องท้ายบรรทัดสร้าง
line break ใน Markdown หลายแบบ แต่บรรทัดว่างมักอ่านและบำรุงรักษาง่ายกว่า

## 10. ตารางความเข้ากันได้

| รูปแบบ | ประเภท | GitHub | หมายเหตุ |
|:---|:---|:---:|:---|
| หัวข้อ รายการ ลิงก์ ตัวหนา ตัวเอียง | Markdown ทั่วไป | ✅ | ใช้ได้กว้าง |
| ตาราง ขีดฆ่า checklist | GFM | ✅ | renderer อื่นอาจต่างกัน |
| `<u>` และ `<details>` | HTML fallback | บางส่วน | ขึ้นกับ renderer |
| สีข้อความ/พื้นหลังผ่าน `style` | HTML/CSS | ⚠️ | GitHub อาจกรอง style |
| เส้นแนวตั้ง/ความหนาเส้นผ่าน CSS | HTML/CSS | ⚠️ | ไม่ใช่ Markdown มาตรฐาน |
| anchor ภาษาไทย | ขึ้นกับ renderer | ⚠️ | ตรวจลิงก์กับปลายทางจริง |

## แนวทางใช้งานที่ปลอดภัย

1. เริ่มจาก Markdown/GFM ที่เรียบง่ายก่อน
2. ใช้ HTML/CSS เฉพาะเมื่อทราบ renderer ปลายทาง
3. อย่าใช้สีเพียงอย่างเดียวเพื่อสื่อสถานะ
4. เปิด preview และทดสอบลิงก์ relative path ก่อน commit
5. เมื่อไม่ทราบผล ให้บันทึกว่า “ขึ้นกับ renderer” แทนการคาดเดา

## Movement line

- [requests/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001.md](../../requests/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001.md)

## Owner line

- Owner: BBX19
- Maker: Copilot-Gm
- Log: 2026-10-03T10:08:04Z; status=waiting_human; request=RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001
