คู่มือการใช้งาน Markdown และสมุดรวมไวยากรณ์ฉบับสมบูรณ์ (Comprehensive Markdown User Guide & Syntax Reference)1. บทนำและภาพรวมมาตรฐาน Markdown (Introduction & Overview)1.1 นิยามและความแตกต่างของ Markdown ParsersMarkdown คือภาษาทำเครื่องหมายแบบเบา (Lightweight Markup Language) ที่ออกแบบมาเพื่อกำหนดโครงสร้างเอกสารให้อยู่ในรูปแบบที่อ่านง่ายด้วยตาเปล่าตั้งแต่ซอร์สโค้ด การประมวลผลข้อความ Markdown จำเป็นต้องพึ่งพาตัวแปลงผล (Markdown Processors) หรือตัววิเคราะห์ภาษา (Parsers) ซึ่งแบ่งออกเป็น 2 กลุ่มหลัก ได้แก่ ไวยากรณ์พื้นฐาน (Basic Syntax) และส่วนขยาย (Extended Syntax)• ไวยากรณ์พื้นฐาน (Basic Syntax): ครอบคลุมองค์ประกอบหลักตามข้อกำหนดดั้งเดิม เช่น หัวข้อ (Headings), รายการ (Lists), ข้อความอ้างอิง (Blockquotes), ลิงก์, รูปภาพ และการเน้นตัวหนังสือพื้นฐาน• ส่วนขยาย (Extended Syntax): เพิ่มเติมความสามารถ นอกเหนือจากมาตรฐานดั้งเดิม เพื่อรองรับเอกสารทางเทคนิคและงานสิ่งพิมพ์ เช่น ตาราง, บล็อกโค้ดแบบ Fenced, การเน้นสีไวยากรณ์ (Syntax Highlighting), ลิงก์ URL อัตโนมัติ, เชิงอรรถ (Footnotes), เช็คลิสต์ และสมการคณิตศาสตร์• ภาษาทำเครื่องหมายแบบเบาและตัวประมวลผลยอดนิยม (Lightweight Markup Languages & Processors):◦ CommonMark: มาตรฐานกลางของ Markdown ที่ถูกกำหนดสเปกไว้อย่างเป็นทางการ เน้นความถูกต้อง ถูกต้องแม่นยำ และเป็นเอกภาพข้ามแพลตฟอร์ม◦ GitHub Flavored Markdown (GFM): ส่วนขยายสเปกของ CommonMark ที่เพิ่มคุณสมบัติสำหรับการพัฒนาซอฟต์แวร์ เช่น ตาราง, Task lists, Auto-linking และการแสดงผลเฉพาะบน GitHub◦ Markdown Extra: ส่วนขยายที่เพิ่มฟีเจอร์ระดับสูง เช่น Definition Lists, Custom Attribute และ Footnotes◦ MultiMarkdown: ภาษาที่เป็นซูเปอร์เซ็ต (Superset) ของ Markdown ที่เน้นเพิ่มไวยากรณ์สำหรับการจัดทำเอกสารวิชาการ รูปแบบบรรณานุกรม และการแปลงเป็น PDF/LaTeX◦ R Markdown: ส่วนขยายที่นิยมใช้ในงานประมวลผลข้อมูล การวิเคราะห์ทางสถิติ และการสร้างรายงานเชิงคำนวณ (Data Science)ข้อสังเกตเรื่องความพร้อมใช้งาน (Availability): แอปพลิเคชัน Markdown แต่ละตัวอาจรองรับส่วนขยายไม่เท่ากัน ผู้ใช้จำเป็นต้องตรวจสอบว่าตัวประมวลผล (Processor) หรือเอนจินการแสดงผล (Renderer) ในโปรแกรมนั้นๆ รองรับ Extended Syntax ตัวใดบ้าง หากไม่รองรับโดยตรง อาจต้องเปิดใช้งานตัวขยายเพิ่มเติม (Extensions) ในการตั้งค่าของระบบ1.2 กฎพื้นฐานและข้อจำกัดการประมวลผลหลักการสำคัญของ Markdown คือ "แยกโครงสร้างเอกสาร (Structure) ออกจากการตกแต่งรูปแบบ (Appearance)"Markdown มีหน้าที่ระบุเชิง semantics ว่าข้อความส่วนใดคือหัวข้อ รายการ หรือโค้ด ส่วนการแสดงผลเรื่องสี ฟอนต์ ระยะห่าง หรือขนาดข้อความที่แน่นอน จะเป็นหน้าที่ของ Style Sheet (CSS) และตัวแปลงผล (Renderers) ด้วยเหตุนี้ สัญลักษณ์การตกแต่งเฉพาะทาง เช่น การจัดข้อความชิดขวาแบบละเอียด หรือการใส่สีตัวหนังสือ จึงไม่มีระบุอยู่ในไวยากรณ์มาตรฐานของ Markdown แต่ต้องพึ่งพาการใช้ HTML ร่วม หรืออาศัยความสามารถขยายของตัวแปลงผลในแต่ละแพลตฟอร์ม2. ไวยากรณ์การจัดข้อความและโครงสร้างพื้นฐาน (Basic Syntax & Formatting)2.1 หัวข้อ (Headings) และ Custom Heading IDsการกำหนดระดับหัวข้อใช้เครื่องหมาย # (Hashtag) นำหน้าข้อความ ตั้งแต่ 1 ถึง 6 ตัวตามระดับความสำคัญ นอกจากนี้ ตัวแปลงผลบางระบบรองรับการใส่ Custom Heading IDs เพื่อสร้างจุดเชื่อมโยงภายในเอกสาร (Anchor Links)ตารางเปรียบเทียบไวยากรณ์หัวข้อและการเชื่อมโยงระดับ / รูปแบบไวยากรณ์ Markdownผลลัพธ์การแสดงผล (Rendered Output)Heading 1# หัวข้อระดับ 1<h1>หัวข้อระดับ 1</h1>Heading 2## หัวข้อระดับ 2<h2>หัวข้อระดับ 2</h2>Heading 3### หัวข้อระดับ 3<h3>หัวข้อระดับ 3</h3>Heading 4#### หัวข้อระดับ 4<h4>หัวข้อระดับ 4</h4>Heading 5##### หัวข้อระดับ 5<h5>หัวข้อระดับ 5</h5>Heading 6###### หัวข้อระดับ 6<h6>หัวข้อระดับ 6</h6>Custom ID##### หัวข้อของฉัน {#custom-id}<h5 id="custom-id">หัวข้อของฉัน</h5>Anchor Link[ไปยังหัวข้อ](#custom-id)ไปยังหัวข้อ (สร้างลิงก์กระโดดไปยังเป้าหมาย)2.2 การจัดรูปแบบตัวหนังสือ (Text Formatting)การเน้นข้อความในรูปแบบต่างๆ สามารถใช้สัญลักษณ์ Markdown หรือแท็ก HTML ในกรณีที่ตัวแปลงผลรองรับตารางเปรียบเทียบการจัดรูปแบบตัวหนังสือรูปแบบการตกแต่งไวยากรณ์ Markdown / HTMLตัวอย่างโค้ดผลลัพธ์การแสดงผล (Rendered Output)ตัวหนา (Bold)** หรือ __**ข้อความหนา**ข้อความหนาตัวเอียง (Italic)* หรือ _*ข้อความเอียง*ข้อความเอียงตัวหนาและตัวเอียง*** หรือ ___***ข้อความหนาเอียง***ข้อความหนาเอียงตัวขีดฆ่า (Strikethrough)~~~~ข้อความขีดฆ่า~~ข้อความขีดฆ่าการไฮไลต์ข้อความ== หรือ <mark>==ข้อความสำคัญ== หรือ <mark>ข้อความสำคัญ</mark><mark>ข้อความสำคัญ</mark>ตัวสับสคริปต์ (Subscript)~ หรือ <sub>H~2~O หรือ H<sub>2</sub>OH<sub>2</sub>Oตัวยก (Superscript)^ หรือ <sup>X^2^ หรือ X<sup>2</sup>X<sup>2</sup>2.3 รายการ (Lists)1. รายการแบบไม่มีลำดับ (Unordered List)ใช้เครื่องหมาย -, *, หรือ + นำหน้าข้อความ และสร้างรายการย่อยด้วยการเว้นวรรค (Space) ด้านหน้า 2–4 ช่อง- รายการหลัก A
* รายการหลัก B
+ รายการหลัก C
  - รายการย่อย C.1 (เว้นวรรคด้านหน้า)
  - รายการย่อย C.2
ผลลัพธ์การแสดงผล:• รายการหลัก A• รายการหลัก B• รายการหลัก C◦ รายการย่อย C.1◦ รายการย่อย C.22. รายการแบบมีลำดับ (Ordered List)ใช้ตัวเลขตามด้วยจุด 1., 2. นำหน้าข้อความ1. ขั้นตอนที่หนึ่ง
2. ขั้นตอนที่สอง
3. ขั้นตอนที่สาม
ผลลัพธ์การแสดงผล:1. ขั้นตอนที่หนึ่ง2. ขั้นตอนที่สอง3. ขั้นตอนที่สาม3. รายการงาน / เช็คลิสต์ (Task Lists / Checkbox)ใช้เครื่องหมายขีด - ตามด้วยวงเล็บเหลี่ยม [ ] สำหรับรายการที่ยังไม่เสร็จ และ [x] สำหรับรายการที่เสร็จแล้ว- [x] เขียนเนื้อหาบทนำ
- [ ] ตรวจทานไวยากรณ์
- [ ] เผยแพร่ออกสู่ระบบ
ผลลัพธ์การแสดงผล:• [x] เขียนเนื้อหาบทนำ• [ ] ตรวจทานไวยากรณ์• [ ] เผยแพร่ออกสู่ระบบ4. รายการคำนิยาม (Definition Lists)พิมพ์คำศัพท์ในบรรทัดแรก จากนั้นขึ้นบรรทัดใหม่แล้วพิมพ์เครื่องหมายโคลอน : ตามด้วยช่องว่างและคำนิยามTerm First
: คำนิยามของศัพท์คำแรก

Term Second
: คำนิยามแบบที่หนึ่งของศัพท์คำที่สอง
: คำนิยามแบบที่สองของศัพท์คำที่สอง
ผลลัพธ์การแสดงผล:2.4 การอ้างอิงข้อความ (Blockquotes)ใช้เครื่องหมายมากกว่า > นำหน้าบรรทัด และสามารถซ้อนสัญลักษณ์ >> เพื่อสร้างอ้างอิงย่อย (Nested Blockquotes)> นี่คือข้อความอ้างอิงระดับที่หนึ่ง
>> นี่คือข้อความอ้างอิงซ้อนภายในระดับที่สอง
ผลลัพธ์การแสดงผล:นี่คือข้อความอ้างอิงระดับที่หนึ่งนี่คือข้อความอ้างอิงซ้อนภายในระดับที่สอง2.5 ลิงก์ รูปภาพ และลิงก์อัตโนมัติ (Links, Images & Auto-linking)ลิงก์ (Links) และรูปภาพ (Images)[ข้อความลิงก์](https://example.com)
![ข้อความอธิบายรูปภาพ (Alt Text)](https://example.com/image.jpg)
[![รูปภาพที่เป็นลิงก์](https://example.com/image.jpg)](https://example.com)
ผลลัพธ์การแสดงผล:• ข้อความลิงก์• การใส่รูปภาพจะดึงรูปจาก URL มาแสดงผลตาม Alt Text ที่ระบุ• การคลิกที่รูปภาพจะนำทางไปยัง URL ที่ครอบอยู่ลิงก์อัตโนมัติ (Auto-linking) และการยกเลิกตัวแปลงผลส่วนใหญ่จะแปลง URL ที่พิมพ์ลงไปตรงๆ ให้กลายเป็นลิงก์โดยอัตโนมัติ หากต้องการยกเลิก ให้ครอบ URL ด้วย Inline Backtick (`)URL อัตโนมัติ: http://www.example.com
ยกเลิก URL อัตโนมัติ: `http://www.example.com`
ผลลัพธ์การแสดงผล:• URL อัตโนมัติ: http://www.example.com• ยกเลิก URL อัตโนมัติ: http://www.example.com2.6 เส้นคั่นแนวนอน (Horizontal Rules)สามารถสร้างเส้นคั่นแนวนอนได้ด้วยการใช้สัญลักษณ์ Hyphens (---), Asterisks (***), หรือ Underscores (___) จำนวน 3 ตัวขึ้นไปในบรรทัดเปล่า---
***
___
ผลลัพธ์การแสดงผล: (แสดงเส้นคั่นแนวนอน 3 เส้นแยกส่วนเนื้อหาออกจากกัน)3. บล็อกโค้ดและการเน้นไวยากรณ์โค้ด (Code Blocks & Syntax Highlighting)3.1 โค้ดอินไลน์ (Inline Code) และการหลบสัญลักษณ์ Backticksโค้ดอินไลน์ใช้สำหรับเน้นข้อความคำสั่งสั้นๆ ในบรรทัด โดยครอบด้วยเครื่องหมาย Backtick บรรทัดเดียว (`)ใช้คำสั่ง `const x = 10;` เพื่อประกาศตัวแปร
การ Escape สัญลักษณ์ Backtick ภายในโค้ดอินไลน์หากในข้อความโค้ดมีเครื่องหมาย Backtick อยู่แล้ว ให้ครอบด้วย Double Backticks หรือ Triple Backticks ด้านนอกแสดงสัญลักษณ์ backtick: ``` ` ``` หรือ `` ` code ` ``
3.2 บล็อกโค้ดแบบ Fenced Code Blocksการสร้างบล็อกโค้ดหลายบรรทัดทำได้โดยใช้ Triple Backticks (```) หรือ Triple Tildes (~~~) ปิดหัวและท้ายบล็อก โดยไม่จำเป็นต้องเว้นวรรค 4 Space ด้านหน้า```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
3.3 การระบุภาษาเพื่อทำ Syntax Highlightingการระบุชื่อภาษาหรือชื่อย่อ (Aliases) ต่อท้าย Triple Backticks บรรทัดแรก จะช่วยเปิดการเน้นสีไวยากรณ์ (Syntax Highlighting) ตามกฎของภาษานั้นๆ1. Web Developmentใช้ชื่อเต็มหรือชื่อย่อ เช่น html, css, javascript (หรือ js), typescript (หรือ ts), jsx, vue```html
<div class="container"><h1>Hello World</h1></div>
```

```css
.container { display: flex; background: #ff6b6b; }
```

```javascript
// ใช้ชื่อภาษาแบบเต็ม: javascript
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    return await response.json();
}
```

```js
// ใช้ชื่อภาษาย่อ (Alias): js
const greet = (name) => `Hello, ${name}!`;
```

```typescript
// ใช้ชื่อภาษาแบบเต็ม: typescript
interface User { id: number; name: string; }
```

```ts
// ใช้ชื่อภาษาย่อ (Alias): ts
type ID = string | number;
```

```jsx
const UserProfile = ({ name }) => <div><h2>{name}</h2></div>;
```

```vue
<template><div class="user">{{ name }}</div></template>
```
2. Backend & Systemsใช้ชื่อเต็มหรือชื่อย่อ เช่น python (หรือ py), java, go, rust```python
# ใช้ชื่อภาษาแบบเต็ม: python
def calculate_sum(a, b):
    return a + b
```

```py
# ใช้ชื่อภาษาย่อ (Alias): py
print("Hello from py alias")
```

```java
public class ApiController {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

```go
package main
import "fmt"
func main() { fmt.Println("Hello, World!") }
```

```rust
fn main() { println!("Hello, World!"); }
```
3. Databases & Queriesใช้ชื่อระบุ เช่น sql, graphql, mongodb```sql
SELECT id, name FROM users WHERE created_at >= '2024-01-01';
```

```graphql
query GetUser($userId: ID!) { user(id: $userId) { name } }
```

```mongodb
db.users.aggregate([{ $match: { status: "active" } }]);
```
4. Configuration & Dataใช้ชื่อระบุ เช่น yaml, json, xml```yaml
version: '3.8'
services:
  web:
    image: node:16
```

```json
{ "name": "my-project", "version": "1.0.0" }
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration><root level="INFO" /></configuration>
```
5. Shell & Terminalใช้ชื่อระบุ เช่น bash, console```bash
# ติดตั้งแพ็กเกจ
npm install express dotenv
```

```console
$ docker build -t myapp .
Successfully built 4a6b7c8d9e0f
```
3.4 เทคนิคการแสดงโค้ดขั้นสูงและคุณสมบัติเฉพาะแพลตฟอร์มDiff Code Blocksแสดงการเปลี่ยนแปลงของโค้ด โดยบรรทัดที่เริ่มต้นด้วย + จะแสดงเป็นสีเขียว (เพิ่มเข้ามา) และ - จะแสดงเป็นสีแดง (ถูกลบออก)```diff
function calculateTotal(items) {
-   let total = 0;
+   let total = 0.0;
    return total;
}
```
คุณสมบัติเฉพาะแพลตฟอร์ม (Platform-Specific Features)• การใส่เลขบรรทัดและไฮไลต์บรรทัด (Line Numbers / Highlighting): Static site generators หรือตัวแปลงผลเฉพาะทางรองรับพารามิเตอร์เสริม เช่น {.line-numbers} หรือไวยากรณ์เฉพาะของ Jekyll/Hugo เช่น {% highlight javascript linenos %} หรือ {{< highlight go "linenos=table,hl_lines=3" >}}3.5 การแก้ไขปัญหาบล็อกโค้ด (Troubleshooting Code Blocks)1. ภาษาไม่แสดงผลสี (Unrecognized languages): ตรวจสอบการสะกดชื่อภาษา หรือเปลี่ยนไปใช้ชื่อย่อมาตรฐาน (Aliases) เช่น js แทน javascript หรือ py แทน python2. การสะกดชื่อภาษาผิด: หากพิมพ์ชื่อภาษาผิด ตัวแปลงผลจะไม่สามารถแมปกฎการไฮไลต์สีได้ และจะถอยกลับไปแสดงผลเป็นบล็อกข้อความธรรมดา (Plain Text)3. การซ้อนบล็อกโค้ดใน Markdown: หากต้องการแสดงบล็อกโค้ด Markdown ไว้ภายในเอกสาร Markdown ให้ใช้นอกสุดด้วย Quadruple Backticks (  ````)````markdown
```python
print("Nested code block")
```
````
4. การสร้างและการจัดรูปแบบตาราง (Tables - GFM Syntax)4.1 โครงสร้างตารางพื้นฐานการสร้างตารางใช้เครื่องหมาย Pipe (|) แบ่งคอลัมน์ และใช้ Hyphen (-) อย่างน้อย 3 ตัวในบรรทัดคั่นหัวข้อ (Header Row)| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
ผลลัพธ์การแสดงผล:SyntaxDescriptionHeaderTitleParagraphText4.2 การจัดตำแหน่งข้อความในคอลัมน์ (Column Alignment)ใส่เครื่องหมาย Colon (:) ที่ส่วนคั่นหัวข้อเพื่อกำหนดการจัดวาง:• :--- จัดชิดซ้าย (Left-aligned)• :---: จัดกึ่งกลาง (Center-aligned)• ---: จัดชิดขวา (Right-aligned)| ชิดซ้าย (Left) | จัดกลาง (Center) | ชิดขวา (Right) |
| :--- | :---: | ---: |
| ข้อมูล A | ข้อมูล B | ข้อมูล C |
| Item 1 | Item 2 | Item 3 |
ผลลัพธ์การแสดงผล:ชิดซ้าย (Left)จัดกลาง (Center)ชิดขวา (Right)ข้อมูล Aข้อมูล Bข้อมูล CItem 1Item 2Item 34.3 ข้อจำกัดและการจัดรูปแบบเนื้อหาภายในตารางองค์ประกอบที่ "สามารถใช้ได้" และ "ห้ามใช้" ภายในเซลล์ตารางประเภทองค์ประกอบรายการองค์ประกอบสามารถใช้ได้ (Allowed)ตัวหนา, ตัวเอียง, ลิงก์, Inline Code (code), ตัวขีดฆ่าห้ามใช้ในไวยากรณ์ Markdown ปกติ (Forbidden)Headings, Blockquotes, Native Lists (- หรือ 1.), Horizontal rules, Images, Fenced Code Blocksทางออกและการแก้ไขปัญหา (Workarounds)1. การขึ้นบรรทัดใหม่ในเซลล์: ใช้แท็ก HTML <br> สำหรับแบ่งบรรทัดภายในเซลล์เดียวกัน2. การหลบสัญลักษณ์ Pipe (|): หากต้องการใส่ตัวอักษร Pipe ในเนื้อหาตาราง ให้ใช้ HTML Entity &#124; แทน3. การใส่รายการ (Lists) ภายในเซลล์ตาราง: แม้รายการมาตรฐาน Markdown จะใช้งานในตารางไม่ได้ แต่สามารถใช้แท็ก HTML List (<ul><li>...</li></ul> หรือ <ol><li>...</li></ol>) เป็นทางออกในการแสดงผลรายการภายในเซลล์ได้| สัญลักษณ์ / โครงสร้าง | ทางออกและคำอธิบาย |
| :---: | :--- |
| &#124; | แสดงตัวอักษร Pipe โดยไม่ทำให้โครงสร้างตารางพัง <br> (พร้อมขึ้นบรรทัดใหม่ด้วย `<br>`) |
| รายการในเซลล์ | <ul><li>รายการย่อยที่ 1</li><li>รายการย่อยที่ 2</li></ul> |
5. การจัดการสีข้อความ สีพื้นหลัง และสีเส้น (Colored Text & Elements across Platforms)5.1 กฎเบื้องต้นและปัญหาความเข้ากันได้มาตรฐาน CommonMark และ GitHub Flavored Markdown ไม่มีไวยากรณ์สำหรับใส่สีข้อความโดยตรง เนื่องจาก Markdown มุ่งเน้นการกำหนดโครงสร้าง แล้วปล่อยให้ CSS ของระบบจัดการเรื่องสีนอกจากนี้ ระบบความปลอดภัยของตัวแปลงผลบนหลายแพลตฟอร์ม (เช่น GitHub/GitLab) จะทำการลบคุณลักษณะ style="..." หรือแท็ก <font> ออก (Stripping style) เพื่อความปลอดภัย ทำให้การใส่สีต้องเลือกใช้วิธีที่รองรับเฉพาะในแต่ละแพลตฟอร์ม5.2 ตารางเปรียบเทียบวิธีใส่สีบนแพลตฟอร์มต่างๆ (Platform Compatibility Matrix)วิธีการ (Method)ไวยากรณ์ตัวอย่าง (Syntax Example)GitHubGitLabObsidianDiscordSlackNotionVS Code PreviewInline style<span style="color:red">text</span>No (Stripped)NoYesNoNoNoYesMath color${\color{red}\textsf{text}}$YesYesYesNoNoNoต้องมี Math ExtensionDiff code blockบล็อก diff บรรทัด + หรือ -Yes (เขียว/แดง)YesPartlyYes (เขียว/แดง)NoNoYesANSI code blockบล็อก ansi พร้อม Escape codesNoNoNoYes (Desktop/Web)NoNoNoColor swatch#ff0000Yes (Issues/PRs)YesNoNoNoNoNoMenu / Slash commandเมนูเลือกสีข้อความ หรือ /redN/AN/AN/AN/AN/AYesN/A5.3 เจาะลึกรายละเอียดการใช้งานแต่ละวิธี1. HTML Inline CSSใช้แท็ก <span> ร่วมกับแอตทริบิวต์ style เพื่อกำหนดสีข้อความหรือสีพื้นหลัง<span style="color:red">ข้อความสีแดง</span>
<span style="color:#d93025">Error:</span> การทำงานล้มเหลว
<span style="background:yellow">ข้อความไฮไลต์พื้นหลังสีเหลือง</span>
• แพลตฟอร์มที่รองรับ: Obsidian (Reading view และ Live Preview), Typora, Jekyll, Hugo, Docusaurus, MkDocs, VS Code Preview• ข้อจำกัด: ไม่รองรับบน GitHub, GitLab, Discord และ Slack (เนื่องจากแท็ก HTML/Style จะถูกลบหรือเมินเฉย)2. GitHub Math Trick (LaTeX)อาศัยไวยากรณ์สมการคณิตศาสตร์แทรกคำสั่ง \color และ \textsf เพื่อคงฟอนต์ตัวหนังสือปกติไว้${\color{red}\textsf{ข้อความสีแดง}}$ และ ${\color{#0969da}\textsf{ข้อความสีฟ้า}}$
• ข้อจำกัด: ข้อความจะแสดงผลในรูปแบบฟอนต์คณิตศาสตร์, ไม่รองรับการตัดคำขึ้นบรรทัดใหม่ (Line wrapping poor) และไม่แสดงผลบนระบบที่ไม่รองรับ Math (เช่น หน้า npm หรือระบบอื่นที่ไม่มีตัวประมวลผล KaTeX/LaTeX)3. Discord Color Workarounds & ANSI Code BlockDiscord ไม่รองรับการใส่ HTML แท็ก แต่สามารถแสดงสีข้อความได้ผ่านเทคนิคบล็อกโค้ด 3 รูปแบบหลัก:ก. บล็อกโค้ด ANSI (ANSI Escape Sequences)กำหนดสีข้อความในบล็อกโค้ด ansi โดยใช้รหัส ANSI Escape Sequence ([31m สีแดง, [32m สีเขียว, [33m สีเหลือง, [34m สีฟ้า, และ [0m เพื่อรีเซ็ตสี)```ansi
[31mข้อความสีแดง[0m [32mข้อความสีเขียว[0m [34mข้อความสีน้ำเงิน[0m

*   **ข้อจำกัด:** ต้องใช้ตัวอักษรพิเศษ ESC (Invisible Escape Character) นำหน้ารหัส ซึ่งพิมพ์ไม่ได้จากคีย์บอร์ดทั่วไป ต้องคัดลอกจากเครื่องมือสร้าง ANSI และอาจแสดงผลไม่สมบูรณ์บน Discord Mobile Apps (iOS/Android)

##### ข. บล็อกโค้ด Diff (Diff Code Block)
การใช้บล็อกโค้ด `diff` ร่วมกับเครื่องหมาย `+` และ `-` นำหน้าบรรทัด เพื่อสร้างสีเขียวและสีแดงโดยไม่ต้องพึ่งพาตัวอักษร ESC ซ่อนอยู่

```markdown
```diff
+ ข้อความนี้จะแสดงเป็นสีเขียว
- ข้อความนี้จะแสดงเป็นสีแดง

*   **ข้อดี:** แสดงผลสีได้อย่างสมบูรณ์และสม่ำเสมอในทุก Client ของ Discord (ทั้ง Desktop, Web และ Mobile)

##### ค. บล็อกโค้ด Syntax Highlighting เฉพาะทาง
การใช้บล็อกโค้ดภาษาเช่น `fix` (แสดงสีเหลือง/ส้ม), `css` (แสดงสีฟ้า/เขียวมิ้นต์) หรือ `yaml` (แสดงสีฟ้า) เพื่อทำไฮไลต์สีบางส่วนของข้อความในบรรทัดโดยไม่ต้องใช้ Escape Character

#### 4. Colored Lines
การสร้างเส้นคั่นสีด้วย HTML Inline CSS:

```html
<hr style="border: 2px solid red;">
<hr style="border: 1px dashed blue;">
5.4 ข้อควรระวังและข้อปฏิบัติต่างๆ (Best Practices & Troubleshooting)5 สาเหตุหลักที่ทำให้การใส่สีไม่แสดงผลและการแก้ไขปัญหา1. การถูก Sanitizer ลบหรือตัด Style/HTML Tag (GitHub / GitLab / Discord / Slack): ระบบความปลอดภัยจะลบแอตทริบิวต์ style หรือมองข้ามแท็ก HTML ทั้งหมด ให้เปลี่ยนไปใช้วิธี Math Trick หรือ Diff Block สำหรับ GitHub/GitLab และใช้ ANSI หรือ Diff/Syntax Block สำหรับ Discord2. การใช้ HTML Tag ที่ล้าสมัย หรือการซ้อนไวยากรณ์ Markdown ผิดวิธี: แท็กเก่าอย่าง <font color="..."> มักถูกลบโดยตัวแปลงสมัยใหม่ ควรเปลี่ยนไปใช้ <span style="..."> นอกจากนี้ ไวยากรณ์ Markdown ด้านในแท็ก Span เช่น <span>**ข้อความหนา**</span> มักไม่ถูกประมวลผล ให้ย้าย Markdown ไว้ด้านนอก **<span style="...">ข้อความ</span>** หรือใช้แท็ก HTML ตรงๆ เช่น <b>3. โครงสร้าง ANSI / Escape Sequence ผิดพลาด: เกิดจากการคัดลอกรหัส ANSI มาไม่สมบูรณ์ (ขาดตัวอักษรซ่อน ESC Byte) ทำให้ข้อความแสดงผลเป็นตัวหนังสือ [31m ตรงๆ ให้คัดลอกจากเครื่องมือสร้าง ANSI Generator โดยตรง4. ความไม่เข้ากันของตัวแปลงผลเฉพาะทาง (Math Engine / Export PDF): การใช้ Math Color จะล้มเหลวหากระบบปลายทางไม่มีเอนจิน KaTeX/LaTeX หรือตัวแปลงไฟล์ PDF ตัด Inline CSS ออกขณะทำการ Export5. การขัดต่อหลักการเข้าถึง (Accessibility) และ Dark Mode: การสื่อสารด้วยสีเพียงอย่างเดียวทำให้ผู้พิการทางสายตา (Color-blindness) หรือโปรแกรมอ่านหน้าจอ (Screen readers) ขาดข้อมูลสำคัญ ควรใส่ข้อความกำกับเสมอ เช่น Error: นำหน้าข้อความสีแดง และหลีกเลี่ยงการ Hard-code สีเข้มสนิทเพื่อป้องกันปัญหาอ่านไม่ได้ใน Dark Mode6. ส่วนขยายพิเศษ ภาษาจัดรูปแบบ HTML และคณิตศาสตร์ (Extensions, HTML & Math)6.1 เชิงอรรถ (Footnotes)ใช้ไวยากรณ์ [^1] ในการสร้างตัวยกอ้างอิง และระบุคำอธิบายด้านล่างเอกสารด้วย [^1]:เนื้อหาหลักในเอกสารที่มีการอ้างอิงอธิบายเพิ่มเติม[^1] และข้อความที่มีเชิงอรรถแบบยาว[^bignote]

[^1]: นี่คือคำอธิบายเชิงอรรถข้อที่หนึ่ง
[^bignote]: นี่คือคำอธิบายเชิงอรรถแบบยาว
    สามารถเว้นวรรคเข้าด้านในเพื่อใส่โค้ดหรือขึ้นย่อหน้าใหม่ได้
    `{ my code }`
ผลลัพธ์การแสดงผล: ข้อความจะถูกใส่ตัวเลขเชิงอรรถกำกับแบบอัตโนมัติ <sup>[1]</sup> <sup>[2]</sup> และสร้างลิงก์เชื่อมโยงไปยังรายการคำอธิบายท้ายเอกสาร6.2 อีโมจิ (Emoji Integration)สามารถใส่อีโมจิใน Markdown ได้ 2 วิธี:1. การคัดลอก-วาง สัญลักษณ์ Unicodeวางตัวอักษรอีโมจิลงในเอกสารตรงๆ โดยระบบจะแสดงผลสมบูรณ์เมื่อใช้การเข้ารหัสไฟล์แบบ UTF-8เปิดบริการตั้งแคมป์แล้ว! ⛺ แล้วพบกันเร็วๆ นี้ 😂
2. การใช้ Emoji Shortcodesพิมพ์ข้อความรหัสสั้นที่ล้อมรอบด้วยโคลอน : (ขึ้นอยู่กับการรองรับของแต่ละแอปพลิเคชัน)Gone camping! :tent: Be back soon.
That is so funny! :joy:
ผลลัพธ์การแสดงผล: Gone camping! ⛺ Be back soon.That is so funny! 😂6.3 สมการคณิตศาสตร์ (Math Equations - LaTeX/KaTeX)การเขียนสมการคณิตศาสตร์ใช้สัญลักษณ์ Dollar Sign ($)Inline Mathครอบข้อความสมการในบรรทัดด้วยสัญลักษณ์ Dollar Sign หนึ่งตัว ($...$)สมการของไอน์สไตน์คือ $E = mc^2$
ผลลัพธ์การแสดงผล: สมการของไอน์สไตน์คือ E = mc^2Block Mathครอบสมการด้วย Dollar Sign สองตัว ($$...$$) เพื่อแสดงผลสมการกึ่งกลางบล็อก$$
\int_{a}^{b} f(x) \, dx = F(b) - F(a)
$$
ผลลัพธ์การแสดงผล:  \int_{a}^{b} f(x) , dx = F(b) - F(a) 6.4 การซ่อน/ขยายเนื้อหา (Collapsible Content)ใช้แท็ก HTML <details> และ <summary> เพื่อสร้างส่วนเปิด-ปิดเนื้อหาแบบพับเก็บได้<details>
<summary>คลิกเพื่อขยายดูเนื้อหาเพิ่มเติม</summary>

ข้อความหรือรายละเอียดภายในที่ต้องการซ่อนไว้ จะแสดงผลเมื่อกดขยายเท่านั้น
</details>
ผลลัพธ์การแสดงผล:
ข้อความหรือรายละเอียดภายในที่ต้องการซ่อนไว้ จะแสดงผลเมื่อกดขยายเท่านั้น
