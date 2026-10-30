# คู่มือการใช้งาน Markdown และสมุดรวมไวยากรณ์ฉบับสมบูรณ์

*Comprehensive Markdown User Guide & Syntax Reference*

> เอกสารอ้างอิงเดิม จัดรูปแบบใหม่เพื่อให้อ่านบน GitHub และ Obsidian ได้สะดวก ตัวอย่างบางแบบเป็นส่วนขยายเฉพาะแพลตฟอร์ม

## สารบัญ

- [1. บทนำและภาพรวมมาตรฐาน Markdown (Introduction & Overview)](#chapter-1)
- [2. ไวยากรณ์การจัดข้อความและโครงสร้างพื้นฐาน (Basic Syntax & Formatting)](#chapter-2)
- [3. บล็อกโค้ดและการเน้นไวยากรณ์โค้ด (Code Blocks & Syntax Highlighting)](#chapter-3)
- [4. การสร้างและการจัดรูปแบบตาราง (Tables - GFM Syntax)](#chapter-4)
- [5. การจัดการสีข้อความ สีพื้นหลัง และสีเส้น (Colored Text & Elements across Platforms)](#chapter-5)
- [6. ส่วนขยายพิเศษ ภาษาจัดรูปแบบ HTML และคณิตศาสตร์ (Extensions, HTML & Math)](#chapter-6)

<a id="chapter-1"></a>

## 1. บทนำและภาพรวมมาตรฐาน Markdown (Introduction & Overview)

### 1.1 นิยามและความแตกต่างของ Markdown Parsers

Markdown คือภาษาทำเครื่องหมายแบบเบา (Lightweight Markup Language) ที่ออกแบบมาเพื่อกำหนดโครงสร้างเอกสารให้อยู่ในรูปแบบที่อ่านง่ายด้วยตาเปล่าตั้งแต่ซอร์สโค้ด การประมวลผลข้อความ Markdown จำเป็นต้องพึ่งพาตัวแปลงผล (Markdown Processors) หรือตัววิเคราะห์ภาษา (Parsers) ซึ่งแบ่งออกเป็น 2 กลุ่มหลัก ได้แก่ ไวยากรณ์พื้นฐาน (Basic Syntax) และส่วนขยาย (Extended Syntax)

- ไวยากรณ์พื้นฐาน (Basic Syntax): ครอบคลุมองค์ประกอบหลักตามข้อกำหนดดั้งเดิม เช่น หัวข้อ (Headings), รายการ (Lists), ข้อความอ้างอิง (Blockquotes), ลิงก์, รูปภาพ และการเน้นตัวหนังสือพื้นฐาน
- ส่วนขยาย (Extended Syntax): เพิ่มเติมความสามารถ นอกเหนือจากมาตรฐานดั้งเดิม เพื่อรองรับเอกสารทางเทคนิคและงานสิ่งพิมพ์ เช่น ตาราง, บล็อกโค้ดแบบ Fenced, การเน้นสีไวยากรณ์ (Syntax Highlighting), ลิงก์ URL อัตโนมัติ, เชิงอรรถ (Footnotes), เช็คลิสต์ และสมการคณิตศาสตร์
- ภาษาทำเครื่องหมายแบบเบาและตัวประมวลผลยอดนิยม (Lightweight Markup Languages & Processors):
  - CommonMark: มาตรฐานกลางของ Markdown ที่ถูกกำหนดสเปกไว้อย่างเป็นทางการ เน้นความถูกต้อง ถูกต้องแม่นยำ และเป็นเอกภาพข้ามแพลตฟอร์ม
  - GitHub Flavored Markdown (GFM): ส่วนขยายสเปกของ CommonMark ที่เพิ่มคุณสมบัติสำหรับการพัฒนาซอฟต์แวร์ เช่น ตาราง, Task lists, Auto-linking และการแสดงผลเฉพาะบน GitHub
  - Markdown Extra: ส่วนขยายที่เพิ่มฟีเจอร์ระดับสูง เช่น Definition Lists, Custom Attribute และ Footnotes
  - MultiMarkdown: ภาษาที่เป็นซูเปอร์เซ็ต (Superset) ของ Markdown ที่เน้นเพิ่มไวยากรณ์สำหรับการจัดทำเอกสารวิชาการ รูปแบบบรรณานุกรม และการแปลงเป็น PDF/LaTeX
  - R Markdown: ส่วนขยายที่นิยมใช้ในงานประมวลผลข้อมูล การวิเคราะห์ทางสถิติ และการสร้างรายงานเชิงคำนวณ (Data Science)

**ข้อสังเกตเรื่องความพร้อมใช้งาน (Availability):** แอปพลิเคชัน Markdown แต่ละตัวอาจรองรับส่วนขยายไม่เท่ากัน ผู้ใช้จำเป็นต้องตรวจสอบว่าตัวประมวลผล (Processor) หรือเอนจินการแสดงผล (Renderer) ในโปรแกรมนั้นๆ รองรับ Extended Syntax ตัวใดบ้าง หากไม่รองรับโดยตรง อาจต้องเปิดใช้งานตัวขยายเพิ่มเติม (Extensions) ในการตั้งค่าของระบบ

### 1.2 กฎพื้นฐานและข้อจำกัดการประมวลผล

หลักการสำคัญของ Markdown คือ "แยกโครงสร้างเอกสาร (Structure) ออกจากการตกแต่งรูปแบบ (Appearance)"

Markdown มีหน้าที่ระบุเชิง semantics ว่าข้อความส่วนใดคือหัวข้อ รายการ หรือโค้ด ส่วนการแสดงผลเรื่องสี ฟอนต์ ระยะห่าง หรือขนาดข้อความที่แน่นอน จะเป็นหน้าที่ของ Style Sheet (CSS) และตัวแปลงผล (Renderers) ด้วยเหตุนี้ สัญลักษณ์การตกแต่งเฉพาะทาง เช่น การจัดข้อความชิดขวาแบบละเอียด หรือการใส่สีตัวหนังสือ จึงไม่มีระบุอยู่ในไวยากรณ์มาตรฐานของ Markdown แต่ต้องพึ่งพาการใช้ HTML ร่วม หรืออาศัยความสามารถขยายของตัวแปลงผลในแต่ละแพลตฟอร์ม

<a id="chapter-2"></a>

## 2. ไวยากรณ์การจัดข้อความและโครงสร้างพื้นฐาน (Basic Syntax & Formatting)

### 2.1 หัวข้อ (Headings) และ Custom Heading IDs

การกำหนดระดับหัวข้อใช้เครื่องหมาย # (Hashtag) นำหน้าข้อความ ตั้งแต่ 1 ถึง 6 ตัวตามระดับความสำคัญ นอกจากนี้ ตัวแปลงผลบางระบบรองรับการใส่ Custom Heading IDs เพื่อสร้างจุดเชื่อมโยงภายในเอกสาร (Anchor Links)

**ตารางเปรียบเทียบไวยากรณ์หัวข้อและการเชื่อมโยง**

| ระดับ / รูปแบบ | ไวยากรณ์ Markdown | HTML / ผลลัพธ์ |
| --- | --- | --- |
| Heading 1 | `# หัวข้อระดับ 1` | `<h1>หัวข้อระดับ 1</h1>` |
| Heading 2 | `## หัวข้อระดับ 2` | `<h2>หัวข้อระดับ 2</h2>` |
| Heading 3 | `### หัวข้อระดับ 3` | `<h3>หัวข้อระดับ 3</h3>` |
| Heading 4 | `#### หัวข้อระดับ 4` | `<h4>หัวข้อระดับ 4</h4>` |
| Heading 5 | `##### หัวข้อระดับ 5` | `<h5>หัวข้อระดับ 5</h5>` |
| Heading 6 | `###### หัวข้อระดับ 6` | `<h6>หัวข้อระดับ 6</h6>` |
| Custom ID | `##### หัวข้อของฉัน {#custom-id}` | `<h5 id="custom-id">หัวข้อของฉัน</h5>` |
| Anchor Link | `[ไปยังหัวข้อ](#custom-id)` | ลิงก์กระโดดไปยังเป้าหมาย |

### 2.2 การจัดรูปแบบตัวหนังสือ (Text Formatting)

การเน้นข้อความในรูปแบบต่างๆ สามารถใช้สัญลักษณ์ Markdown หรือแท็ก HTML ในกรณีที่ตัวแปลงผลรองรับ

**ตารางเปรียบเทียบการจัดรูปแบบตัวหนังสือ**

| รูปแบบ | ตัวอย่างไวยากรณ์ | ผลลัพธ์ / หมายเหตุ |
| --- | --- | --- |
| ตัวหนา (Bold) | `**ข้อความหนา**` หรือ `__ข้อความหนา__` | **ข้อความหนา** |
| ตัวเอียง (Italic) | `*ข้อความเอียง*` หรือ `_ข้อความเอียง_` | *ข้อความเอียง* |
| ตัวหนาและตัวเอียง | `***ข้อความหนาเอียง***` | ***ข้อความหนาเอียง*** |
| ตัวขีดฆ่า | `~~ข้อความขีดฆ่า~~` | ~~ข้อความขีดฆ่า~~ |
| ไฮไลต์ | `==ข้อความสำคัญ==` หรือ `<mark>ข้อความสำคัญ</mark>` | ขึ้นอยู่กับตัวแปลงผล |
| ตัวห้อย (Subscript) | `H~2~O` หรือ `H<sub>2</sub>O` | H<sub>2</sub>O; แบบ `~` ต้องมีส่วนขยาย |
| ตัวยก (Superscript) | `X^2^` หรือ `X<sup>2</sup>` | X<sup>2</sup>; แบบ `^` ต้องมีส่วนขยาย |

### 2.3 รายการ (Lists)

#### 1. รายการแบบไม่มีลำดับ (Unordered List)

ใช้เครื่องหมาย `-`, `*` หรือ `+` นำหน้าข้อความ และเยื้องรายการย่อยด้วยช่องว่าง

**ตัวอย่างโค้ด**

```markdown
- รายการหลัก A
- รายการหลัก B
- รายการหลัก C
  - รายการย่อย C.1
  - รายการย่อย C.2
```

**ผลลัพธ์**

- รายการหลัก A
- รายการหลัก B
- รายการหลัก C
  - รายการย่อย C.1
  - รายการย่อย C.2

#### 2. รายการแบบมีลำดับ (Ordered List)

ใช้ตัวเลขตามด้วยจุด เช่น `1.` และ `2.`

```markdown
1. ขั้นตอนที่หนึ่ง
2. ขั้นตอนที่สอง
3. ขั้นตอนที่สาม
```

**ผลลัพธ์**

1. ขั้นตอนที่หนึ่ง
2. ขั้นตอนที่สอง
3. ขั้นตอนที่สาม

#### 3. รายการงาน / เช็คลิสต์ (Task Lists / Checkbox)

ใช้ `- [ ]` สำหรับรายการที่ยังไม่เสร็จ และ `- [x]` สำหรับรายการที่เสร็จแล้ว

```markdown
- [x] เขียนเนื้อหาบทนำ
- [ ] ตรวจทานไวยากรณ์
- [ ] เผยแพร่ออกสู่ระบบ
```

**ผลลัพธ์**

- [x] เขียนเนื้อหาบทนำ
- [ ] ตรวจทานไวยากรณ์
- [ ] เผยแพร่ออกสู่ระบบ

#### 4. รายการคำนิยาม (Definition Lists)

พิมพ์คำศัพท์ในบรรทัดแรก จากนั้นขึ้นบรรทัดใหม่แล้วพิมพ์ `:` ตามด้วยช่องว่างและคำนิยาม ต้องใช้ตัวแปลงผลที่รองรับส่วนขยายนี้

```markdown
Term First
: คำนิยามของศัพท์คำแรก

Term Second
: คำนิยามแบบที่หนึ่งของศัพท์คำที่สอง
: คำนิยามแบบที่สองของศัพท์คำที่สอง
```

### 2.4 การอ้างอิงข้อความ (Blockquotes)

ใช้ `>` นำหน้าบรรทัด และใช้ `>>` เพื่อสร้างอ้างอิงย่อย

```markdown
> นี่คือข้อความอ้างอิงระดับที่หนึ่ง
>
>> นี่คือข้อความอ้างอิงซ้อนภายในระดับที่สอง
```

**ผลลัพธ์**

> นี่คือข้อความอ้างอิงระดับที่หนึ่ง
>
>> นี่คือข้อความอ้างอิงซ้อนภายในระดับที่สอง

### 2.5 ลิงก์ รูปภาพ และลิงก์อัตโนมัติ (Links, Images & Auto-linking)

#### ลิงก์ (Links) และรูปภาพ (Images)

```markdown
[ข้อความลิงก์](https://example.com)
![ข้อความอธิบายรูปภาพ (Alt Text)](https://example.com/image.jpg)
[![รูปภาพที่เป็นลิงก์](https://example.com/image.jpg)](https://example.com)
```

- ลิงก์แสดงข้อความที่กดเปิด URL ได้
- รูปภาพดึงจาก URL โดยมี Alt Text อธิบายภาพ
- รูปภาพที่ครอบด้วยลิงก์จะกดเปิด URL ปลายทางได้

#### ลิงก์อัตโนมัติ (Auto-linking) และการยกเลิก

ตัวแปลงผลที่รองรับจะแปลง URL เป็นลิงก์ หากต้องการแสดงเป็นโค้ด ให้ครอบ URL ด้วย Backtick

```markdown
URL อัตโนมัติ: http://www.example.com
ยกเลิก URL อัตโนมัติ: `http://www.example.com`
```

### 2.6 เส้นคั่นแนวนอน (Horizontal Rules)

ใช้ `---`, `***` หรือ `___` จำนวนอย่างน้อย 3 ตัว โดยเว้นบรรทัดรอบเส้นคั่น

```markdown
ข้อความส่วนแรก

---

ข้อความส่วนถัดไป
```

**ผลลัพธ์**

ข้อความส่วนแรก

---

ข้อความส่วนถัดไป

<a id="chapter-3"></a>

## 3. บล็อกโค้ดและการเน้นไวยากรณ์โค้ด (Code Blocks & Syntax Highlighting)

### 3.1 โค้ดอินไลน์ (Inline Code) และการหลบสัญลักษณ์ Backticks

โค้ดอินไลน์ใช้สำหรับเน้นข้อความคำสั่งสั้นๆ ในบรรทัด โดยครอบด้วยเครื่องหมาย Backtick บรรทัดเดียว (`)

ใช้คำสั่ง `const x = 10;` เพื่อประกาศตัวแปร
**การ Escape สัญลักษณ์ Backtick ภายในโค้ดอินไลน์**

หากในข้อความโค้ดมีเครื่องหมาย Backtick อยู่แล้ว ให้ครอบด้วย Double Backticks หรือ Triple Backticks ด้านนอก

แสดงสัญลักษณ์ backtick: ``` ` ``` หรือ `` ` code ` ``

### 3.2 บล็อกโค้ดแบบ Fenced Code Blocks

การสร้างบล็อกโค้ดหลายบรรทัดทำได้โดยใช้ Triple Backticks (```) หรือ Triple Tildes (~~~) ปิดหัวและท้ายบล็อก โดยไม่จำเป็นต้องเว้นวรรค 4 Space ด้านหน้า

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

### 3.3 การระบุภาษาเพื่อทำ Syntax Highlighting

การระบุชื่อภาษาหรือชื่อย่อ (Aliases) ต่อท้าย Triple Backticks บรรทัดแรก จะช่วยเปิดการเน้นสีไวยากรณ์ (Syntax Highlighting) ตามกฎของภาษานั้นๆ

#### 1. Web Development

ใช้ชื่อเต็มหรือชื่อย่อ เช่น `html`, `css`, `javascript` (หรือ `js`), `typescript` (หรือ `ts`), `jsx`, `vue`

```html
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

#### 2. Backend & Systems

ใช้ชื่อเต็มหรือชื่อย่อ เช่น `python` (หรือ `py`), `java`, `go`, `rust`

```python
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

#### 3. Databases & Queries

ใช้ชื่อระบุ เช่น `sql`, `graphql`, `mongodb`

```sql
SELECT id, name FROM users WHERE created_at >= '2024-01-01';
```

```graphql
query GetUser($userId: ID!) { user(id: $userId) { name } }
```

```mongodb
db.users.aggregate([{ $match: { status: "active" } }]);
```

#### 4. Configuration & Data

ใช้ชื่อระบุ เช่น `yaml`, `json`, `xml`

```yaml
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

#### 5. Shell & Terminal

ใช้ชื่อระบุ เช่น `bash`, `console`

```bash
# ติดตั้งแพ็กเกจ
npm install express dotenv
```

```console
$ docker build -t myapp .
Successfully built 4a6b7c8d9e0f
```

### 3.4 เทคนิคการแสดงโค้ดขั้นสูงและคุณสมบัติเฉพาะแพลตฟอร์ม

#### Diff Code Blocks

แสดงการเปลี่ยนแปลงของโค้ด โดยบรรทัดที่เริ่มต้นด้วย + จะแสดงเป็นสีเขียว (เพิ่มเข้ามา) และ - จะแสดงเป็นสีแดง (ถูกลบออก)

```diff
function calculateTotal(items) {
-   let total = 0;
+   let total = 0.0;
    return total;
}
```

#### คุณสมบัติเฉพาะแพลตฟอร์ม (Platform-Specific Features)

- การใส่เลขบรรทัดและไฮไลต์บรรทัด (Line Numbers / Highlighting): Static site generators หรือตัวแปลงผลเฉพาะทางรองรับพารามิเตอร์เสริม เช่น {.line-numbers} หรือไวยากรณ์เฉพาะของ Jekyll/Hugo เช่น {% highlight javascript linenos %} หรือ {{< highlight go "linenos=table,hl_lines=3" >}}

### 3.5 การแก้ไขปัญหาบล็อกโค้ด (Troubleshooting Code Blocks)

1. ภาษาไม่แสดงผลสี (Unrecognized languages): ตรวจสอบการสะกดชื่อภาษา หรือเปลี่ยนไปใช้ชื่อย่อมาตรฐาน (Aliases) เช่น `js` แทน `javascript` หรือ `py` แทน `python`

2. การสะกดชื่อภาษาผิด: หากพิมพ์ชื่อภาษาผิด ตัวแปลงผลจะไม่สามารถแมปกฎการไฮไลต์สีได้ และจะถอยกลับไปแสดงผลเป็นบล็อกข้อความธรรมดา (Plain Text)

3. การซ้อนบล็อกโค้ดใน Markdown: หากต้องการแสดงบล็อกโค้ด Markdown ไว้ภายในเอกสาร Markdown ให้ใช้นอกสุดด้วย Quadruple Backticks (4 ตัว)

````markdown
```python
print("Nested code block")
```
````

<a id="chapter-4"></a>

## 4. การสร้างและการจัดรูปแบบตาราง (Tables - GFM Syntax)

### 4.1 โครงสร้างตารางพื้นฐาน

ใช้เครื่องหมาย Pipe (`|`) แบ่งคอลัมน์ และ Hyphen (`-`) อย่างน้อย 3 ตัวในบรรทัดคั่นหัวตาราง

**ตัวอย่างโค้ด**

```markdown
| Syntax | Description |
| --- | --- |
| Header | Title |
| Paragraph | Text |
```

**ผลลัพธ์**

| Syntax | Description |
| --- | --- |
| Header | Title |
| Paragraph | Text |

### 4.2 การจัดตำแหน่งข้อความในคอลัมน์ (Column Alignment)

- `:---` จัดชิดซ้าย (Left-aligned)
- `:---:` จัดกึ่งกลาง (Center-aligned)
- `---:` จัดชิดขวา (Right-aligned)

**ตัวอย่างโค้ด**

```markdown
| ชิดซ้าย (Left) | จัดกลาง (Center) | ชิดขวา (Right) |
| :--- | :---: | ---: |
| ข้อมูล A | ข้อมูล B | ข้อมูล C |
| Item 1 | Item 2 | Item 3 |
```

**ผลลัพธ์**

| ชิดซ้าย (Left) | จัดกลาง (Center) | ชิดขวา (Right) |
| :--- | :---: | ---: |
| ข้อมูล A | ข้อมูล B | ข้อมูล C |
| Item 1 | Item 2 | Item 3 |

### 4.3 ข้อจำกัดและการจัดรูปแบบเนื้อหาภายในตาราง

**องค์ประกอบภายในเซลล์ตาราง**

| ประเภท | องค์ประกอบ |
| --- | --- |
| รูปแบบข้อความในบรรทัด | ตัวหนา ตัวเอียง ลิงก์ Inline Code และตัวขีดฆ่า |
| โครงสร้างแบบบล็อกที่ใช้ในเซลล์ GFM โดยตรงไม่ได้ | หัวข้อ Blockquotes รายการแบบบล็อก เส้นคั่น และ Fenced Code Blocks |

**ทางออกและการแก้ไขปัญหา (Workarounds)**

1. การขึ้นบรรทัดใหม่ในเซลล์: ใช้ `<br>` หากตัวแปลงผลรองรับ HTML
2. การแสดง Pipe: ใช้ `&#124;` เพื่อไม่ให้แยกคอลัมน์
3. รายการในเซลล์: ตัวแปลงผลบางตัวรองรับ HTML เช่น `<ul><li>...</li></ul>` หรือ `<ol><li>...</li></ol>` ต้องตรวจผลในแอปปลายทาง

**ตัวอย่างโค้ด**

```markdown
| สัญลักษณ์ / โครงสร้าง | ทางออกและคำอธิบาย |
| :---: | :--- |
| &#124; | แสดง Pipe <br> และขึ้นบรรทัดใหม่ |
| รายการในเซลล์ | <ul><li>รายการย่อยที่ 1</li><li>รายการย่อยที่ 2</li></ul> |
```

**ผลลัพธ์ตัวอย่าง Pipe และการขึ้นบรรทัดใหม่**

| สัญลักษณ์ | คำอธิบาย |
| :---: | :--- |
| &#124; | แสดง Pipe <br> และขึ้นบรรทัดใหม่ |

<a id="chapter-5"></a>

## 5. การจัดการสีข้อความ สีพื้นหลัง และสีเส้น (Colored Text & Elements across Platforms)

### 5.1 กฎเบื้องต้นและปัญหาความเข้ากันได้

มาตรฐาน CommonMark และ GitHub Flavored Markdown ไม่มีไวยากรณ์สำหรับใส่สีข้อความโดยตรง เนื่องจาก Markdown มุ่งเน้นการกำหนดโครงสร้าง แล้วปล่อยให้ CSS ของระบบจัดการเรื่องสี

นอกจากนี้ ระบบความปลอดภัยของตัวแปลงผลบนหลายแพลตฟอร์ม (เช่น GitHub/GitLab) จะทำการลบคุณลักษณะ `style="..."` หรือแท็ก `<font>` ออก (Stripping style) เพื่อความปลอดภัย ทำให้การใส่สีต้องเลือกใช้วิธีที่รองรับเฉพาะในแต่ละแพลตฟอร์ม

### 5.2 ตารางเปรียบเทียบวิธีใส่สีบนแพลตฟอร์มต่างๆ (Platform Compatibility Matrix)

> ตารางนี้จัดรูปจากข้อมูลเดิม ความสามารถจริงอาจต่างกันตามรุ่น ตัวแปลงผล และปลั๊กอิน

| วิธี | ตัวอย่าง |
| --- | --- |
| Inline style | `<span style="color:red">text</span>` |
| Math color | `${\color{red}\textsf{text}}$` |
| Diff code block | บล็อก `diff` ที่มีบรรทัด `+` หรือ `-` |
| ANSI code block | บล็อก `ansi` พร้อม Escape codes |
| Color swatch | `#ff0000` |
| Menu / Slash command | เมนูเลือกสี หรือ `/red` |

แบ่งตารางตามกลุ่มแพลตฟอร์ม เพื่อลดความกว้างบนมือถือ

| วิธี | GitHub | GitLab | Obsidian | VS Code Preview |
| --- | --- | --- | --- |
| Inline style | No (Stripped) | No | Yes | Yes |
| Math color | Yes | Yes | Yes | ต้องมี Math Extension |
| Diff code block | Yes (เขียว/แดง) | Yes | Partly | Yes |
| ANSI code block | No | No | No | No |
| Color swatch | Yes (Issues/PRs) | Yes | No | No |
| Menu / Slash command | N/A | N/A | N/A | N/A |
| วิธี | Discord | Slack | Notion |
| --- | --- | --- | --- |
| Inline style | No | No | No |
| Math color | No | No | No |
| Diff code block | Yes (เขียว/แดง) | No | No |
| ANSI code block | Yes (Desktop/Web) | No | No |
| Color swatch | No | No | No |
| Menu / Slash command | N/A | N/A | Yes |

### 5.3 เจาะลึกรายละเอียดการใช้งานแต่ละวิธี

#### 1. HTML Inline CSS

ใช้แท็ก `<span>` ร่วมกับแอตทริบิวต์ `style` เพื่อกำหนดสีข้อความหรือสีพื้นหลัง

```html<span style="color:red">ข้อความสีแดง</span>
<span style="color:#d93025">Error:</span> การทำงานล้มเหลว
<span style="background:yellow">ข้อความไฮไลต์พื้นหลังสีเหลือง</span>
```

- แพลตฟอร์มที่รองรับ: Obsidian (Reading view และ Live Preview), Typora, Jekyll, Hugo, Docusaurus, MkDocs, VS Code Preview
- ข้อจำกัด: ไม่รองรับบน GitHub, GitLab, Discord และ Slack (เนื่องจากแท็ก HTML/Style จะถูกลบหรือเมินเฉย) 

#### 2. GitHub Math Trick (LaTeX)

อาศัยไวยากรณ์สมการคณิตศาสตร์แทรกคำสั่ง \color และ \textsf เพื่อคงฟอนต์ตัวหนังสือปกติไว้

```latex
${\color{red}\textsf{ข้อความสีแดง}}$ และ ${\color{#0969da}\textsf{ข้อความสีฟ้า}}$
```

- ข้อจำกัด: ข้อความจะแสดงผลในรูปแบบฟอนต์คณิตศาสตร์, ไม่รองรับการตัดคำขึ้นบรรทัดใหม่ (Line wrapping poor) และไม่แสดงผลบนระบบที่ไม่รองรับ Math (เช่น หน้า npm หรือระบบอื่นที่ไม่มีตัวประมวลผล KaTeX/LaTeX) 

#### 3. Discord Color Workarounds & ANSI Code Block

Discord ไม่รองรับการใส่ HTML แท็ก แต่สามารถแสดงสีข้อความได้ผ่านเทคนิคบล็อกโค้ด 3 รูปแบบหลัก:

##### ก. บล็อกโค้ด ANSI (ANSI Escape Sequences)

กำหนดสีข้อความในบล็อกโค้ด ansi โดยใช้รหัส ANSI Escape Sequence ([31m สีแดง, [32m สีเขียว, [33m สีเหลือง, [34m สีฟ้า, และ [0m เพื่อรีเซ็ตสี)

```ansi
[31mข้อความสีแดง[0m [32mข้อความสีเขียว[0m [34mข้อความสีน้ำเงิน[0m
```

*   **ข้อจำกัด:** ต้องใช้ตัวอักษรพิเศษ ESC (Invisible Escape Character) นำหน้ารหัส ซึ่งพิมพ์ไม่ได้จากคีย์บอร์ดทั่วไป ต้องคัดลอกจากเครื่องมือสร้าง ANSI และอาจแสดงผลไม่สมบูรณ์บน Discord Mobile Apps (iOS/Android)

##### ข. บล็อกโค้ด Diff (Diff Code Block)

การใช้บล็อกโค้ด `diff` ร่วมกับเครื่องหมาย `+` และ `-` นำหน้าบรรทัด เพื่อสร้างสีเขียวและสีแดงโดยไม่ต้องพึ่งพาตัวอักษร ESC ซ่อนอยู่

````markdown
```diff
+ ข้อความนี้จะแสดงเป็นสีเขียว
- ข้อความนี้จะแสดงเป็นสีแดง
```
````

*   **ข้อดี:** แสดงผลสีได้อย่างสมบูรณ์และสม่ำเสมอในทุก Client ของ Discord (ทั้ง Desktop, Web และ Mobile)

##### ค. บล็อกโค้ด Syntax Highlighting เฉพาะทาง

การใช้บล็อกโค้ดภาษาเช่น `fix` (แสดงสีเหลือง/ส้ม), `css` (แสดงสีฟ้า/เขียวมิ้นต์) หรือ `yaml` (แสดงสีฟ้า) เพื่อทำไฮไลต์สีบางส่วนของข้อความในบรรทัดโดยไม่ต้องใช้ Escape Character

#### 4. Colored Lines

การสร้างเส้นคั่นสีด้วย HTML Inline CSS:

```html
<hr style="border: 2px solid red;">
<hr style="border: 1px dashed blue;">
```

### 5.4 ข้อควรระวังและข้อปฏิบัติต่างๆ (Best Practices & Troubleshooting)

**5 สาเหตุหลักที่ทำให้การใส่สีไม่แสดงผลและการแก้ไขปัญหา**

1. การถูก Sanitizer ลบหรือตัด Style/HTML Tag (GitHub / GitLab / Discord / Slack): ระบบความปลอดภัยจะลบแอตทริบิวต์ style หรือมองข้ามแท็ก HTML ทั้งหมด ให้เปลี่ยนไปใช้วิธี Math Trick หรือ Diff Block สำหรับ GitHub/GitLab และใช้ ANSI หรือ Diff/Syntax Block สำหรับ Discord

2. การใช้ HTML Tag ที่ล้าสมัย หรือการซ้อนไวยากรณ์ Markdown ผิดวิธี: แท็กเก่าอย่าง `<font color="...">` มักถูกลบโดยตัวแปลงสมัยใหม่ ควรเปลี่ยนไปใช้ `<span style="...">` นอกจากนี้ Markdown ด้านในแท็ก เช่น `<span>**ข้อความหนา**</span>` อาจไม่ถูกประมวลผล ให้ย้าย Markdown ไว้ด้านนอก `**<span style="...">ข้อความ</span>**` หรือใช้ HTML ตรงๆ เช่น `<b>`

3. โครงสร้าง ANSI / Escape Sequence ผิดพลาด: เกิดจากการคัดลอกรหัส ANSI มาไม่สมบูรณ์ (ขาดตัวอักษรซ่อน ESC Byte) ทำให้ข้อความแสดงผลเป็นตัวหนังสือ [31m ตรงๆ ให้คัดลอกจากเครื่องมือสร้าง ANSI Generator โดยตรง

4. ความไม่เข้ากันของตัวแปลงผลเฉพาะทาง (Math Engine / Export PDF): การใช้ Math Color จะล้มเหลวหากระบบปลายทางไม่มีเอนจิน KaTeX/LaTeX หรือตัวแปลงไฟล์ PDF ตัด Inline CSS ออกขณะทำการ Export

5. การขัดต่อหลักการเข้าถึง (Accessibility) และ Dark Mode: การสื่อสารด้วยสีเพียงอย่างเดียวทำให้ผู้พิการทางสายตา (Color-blindness) หรือโปรแกรมอ่านหน้าจอ (Screen readers) ขาดข้อมูลสำคัญ ควรใส่ข้อความกำกับเสมอ เช่น Error: นำหน้าข้อความสีแดง และหลีกเลี่ยงการ Hard-code สีเข้มสนิทเพื่อป้องกันปัญหาอ่านไม่ได้ใน Dark Mode

<a id="chapter-6"></a>

## 6. ส่วนขยายพิเศษ ภาษาจัดรูปแบบ HTML และคณิตศาสตร์ (Extensions, HTML & Math)

### 6.1 เชิงอรรถ (Footnotes)

ใช้ `[^1]` ในข้อความ และระบุคำอธิบายด้วย `[^1]:` ที่บรรทัดแยก

**ตัวอย่างโค้ด**

```markdown
เนื้อหาหลักที่มีการอ้างอิงเพิ่มเติม[^1] และเชิงอรรถแบบยาว[^bignote]

[^1]: นี่คือคำอธิบายเชิงอรรถข้อที่หนึ่ง
[^bignote]: นี่คือคำอธิบายเชิงอรรถแบบยาว
    สามารถเว้นวรรคเข้าด้านในเพื่อใส่โค้ดหรือขึ้นย่อหน้าใหม่ได้
    `{ my code }`
```

**ผลลัพธ์**

เนื้อหาหลักที่มีการอ้างอิงเพิ่มเติม[^1] และเชิงอรรถแบบยาว[^bignote]

[^1]: นี่คือคำอธิบายเชิงอรรถข้อที่หนึ่ง
[^bignote]: นี่คือคำอธิบายเชิงอรรถแบบยาว
    สามารถเว้นวรรคเข้าด้านในเพื่อใส่โค้ดหรือขึ้นย่อหน้าใหม่ได้
    `{ my code }`

### 6.2 อีโมจิ (Emoji Integration)

สามารถใส่อีโมจิใน Markdown ได้ 2 วิธี

#### 1. การคัดลอก-วางสัญลักษณ์ Unicode

วางอีโมจิลงในเอกสารโดยตรง และบันทึกไฟล์เป็น UTF-8

```text
เปิดบริการตั้งแคมป์แล้ว! ⛺ แล้วพบกันเร็วๆ นี้ 😂
```

**ผลลัพธ์**

เปิดบริการตั้งแคมป์แล้ว! ⛺ แล้วพบกันเร็วๆ นี้ 😂

#### 2. การใช้ Emoji Shortcodes

พิมพ์รหัสสั้นที่ล้อมด้วย `:` ทั้งนี้ขึ้นอยู่กับการรองรับของแต่ละแอป

```markdown
Gone camping! :tent: Be back soon.
That is so funny! :joy:
```

**ผลลัพธ์ในระบบที่รองรับ**

Gone camping! ⛺ Be back soon.

That is so funny! 😂

### 6.3 สมการคณิตศาสตร์ (Math Equations - LaTeX/KaTeX)

ใช้สัญลักษณ์ Dollar Sign (`$`) ในตัวแปลงผลที่รองรับคณิตศาสตร์

#### Inline Math — สมการในบรรทัด

ครอบสมการด้วย `$...$`

```markdown
สมการของไอน์สไตน์คือ $E = mc^2$
```

**ผลลัพธ์**

สมการของไอน์สไตน์คือ $E = mc^2$

#### Block Math — สมการแยกบล็อก

ครอบสมการด้วย `$$...$$` โดยวางตัวคั่นในบรรทัดแยก

```latex
$$
\int_{a}^{b} f(x) \, dx = F(b) - F(a)
$$
```

**ผลลัพธ์**

$$
\int_{a}^{b} f(x) \, dx = F(b) - F(a)
$$

### 6.4 การซ่อน/ขยายเนื้อหา (Collapsible Content)

ใช้แท็ก HTML `<details>` และ `<summary>` เพื่อสร้างส่วนเปิด-ปิดในตัวแปลงผลที่รองรับ

**ตัวอย่างโค้ด**

```html
<details>
<summary>คลิกเพื่อขยายดูเนื้อหาเพิ่มเติม</summary>

ข้อความหรือรายละเอียดภายในที่ต้องการซ่อนไว้ จะแสดงผลเมื่อกดขยายเท่านั้น

</details>
```

**ผลลัพธ์**

<details>
<summary>คลิกเพื่อขยายดูเนื้อหาเพิ่มเติม</summary>

ข้อความหรือรายละเอียดภายในที่ต้องการซ่อนไว้ จะแสดงผลเมื่อกดขยายเท่านั้น

</details>

[⬆️ กลับไปสารบัญ](#สารบัญ)
