# HybridCross / Hybrid-SynCap / CollorPaper Notes

**Status:** CONCEPT CAPTURE / DRAFT  
**Scope:** W3 / Cross-LGU / Hybrid-SynCap / HybridCross / Cross-index / PS-Pcross / MPCP Hyper / LRC2 / CollorPaper  
**Owner:** BBX19  
**Branch Context:** `refactor/v0.2`  

เอกสารนี้เก็บรายละเอียดแนวคิดเพื่อกันลืมก่อนจัดหมวดเป็นมาตรฐานภายหลัง

หลักสำคัญ:

```text
อย่ารีบทำให้เป็นระบบใหญ่
แต่ต้องนิยามแกนให้ทันก่อนระบบโต
```

---

# 1. Core Naming Lock

## 1.1 Hybrid-SynCap

```text
Hybrid-SynCap
= กล่องความสามารถ
= capability capsule ของ W3
= ความสามารถที่ Module / Modew สร้างเก็บไว้
= ใช้ข้าม OS / ENV / EVENT / App / Agent
= รองรับการประกอบเป็น W3 VM ในอนาคต
```

Hybrid-SynCap ไม่ใช่ plugin ตามระบบภายนอก

W3 ใช้แนวคิดของ plugin / capability pack เป็นวัตถุดิบ แล้วสร้างรูปแบบของตัวเอง

```text
ไม่ใช้ตามแบบ
ใช้รูปแบบ / องค์ประกอบ
แล้วสร้างสิ่งใหม่แบบ W3
```

---

## 1.2 HybridCross : Hub

```text
HybridCross : Hub
= จุดตัดกลาง
= จุดที่ SynCap / Event / App / Module / Agent เข้ามาเจอกัน
= จุดรวมบริบทก่อนเลือก route
= ยังไม่ใช่ executor
```

Hub ไม่ควรทำงานแทนระบบอื่น

Hub ควรทำ:

```text
รับเข้า
จัดหมวด
อ่านสถานะ
ชี้ link
ชี้ SynCap
คืน route / plan
ส่งต่อ
```

Hub ไม่ควรทำโดย default:

```text
execute
mutate
merge
ตัดสิน truth เอง
```

---

## 1.3 Hybrid : Link

```text
Hybrid : Link
= เส้นเชื่อมระหว่าง Hub
= เส้นทางที่ข้อมูล / สัญญาณ / งาน / ความสามารถ เดินทาง
```

ตัวอย่างชนิดของ link:

```text
document_link
signal_link
runtime_link
symptom_link
recovery_link
data_link
route_link
```

---

## 1.4 Cross-index : Highway

```text
Cross-index : Highway
= แผนที่ทางหลวงของ Hub + Link + SynCap
= index กลางที่บอกว่าอะไรเชื่อมไปไหน
= ใช้ลดความพันกันของระบบ
```

ไม่ใช่ให้ทุก module คุยกันมั่ว ๆ
แต่ให้วิ่งผ่าน highway:

```text
App / Module / Agent
→ Hybrid : Link
→ HybridCross : Hub
→ Cross-index route
→ target Hub / SynCap / MPCP
```

---

## 1.5 PS-Pcross

```text
PS-Pcross
= มิติใหม่ของ PSP2
= cross routing / stamp / pointer / path
```

PSP2 เดิม:

```text
stamp + route
```

PS-Pcross:

```text
stamp + cross-route + relation index
```

สั้นที่สุด:

```text
PSP2 ส่งพัสดุ
Pcross รู้ว่าพัสดุนั้นควรข้ามสะพานไหน
```

---

## 1.6 LRC2

```text
LRC2
= log การเข้า-ออก
= memory trace ของ highway
= ทะเบียนการจราจรของ W3 Cross System
```

เมื่อมี Hub / Link แล้ว LRC2 ต้องจำ:

```text
ใครเข้า hub
ออกทาง link ไหน
ใช้ SynCap ใด
color state อะไร
decision อะไร
mutated หรือไม่
review หรือไม่
```

---

# 2. Cross-LGU Coverage

Hybrid-SynCap และ HybridCross ต้องถูกครอบด้วย Cross-LGU

```text
Cross-LGU
= language layer
= contract layer
= cross grammar
= ภาษาครอบที่ทำให้ Hub / Link / Pack / Route / Log เข้าใจร่วมกัน
```

ถ้าไม่มี Cross-LGU ระบบจะเสี่ยงเป็น:

```text
ชื่อเยอะ
node เยอะ
link เยอะ
pack เยอะ
แต่คุยกันไม่เป็นมาตรฐานเดียวกัน
```

เมื่อมี Cross-LGU:

```text
Hub รู้ว่ารับอะไร
Link รู้ว่าเชื่อมแบบไหน
SynCap รู้ว่าตัวเองมี capability อะไร
Pcross รู้ว่าจะ route อย่างไร
LRC2 รู้ว่าต้อง log อะไร
MPCP รู้ว่าจะพาข้าม ENV อย่างไร
```

---

# 3. Avoiding Cross-LGU Bottleneck

Cross-LGU ไม่ควรเป็นคอขวด

Cross-LGU ไม่ควรต้องแบกทุก implementation เอง

บทบาทที่เหมาะ:

```text
Cross-LGU = แสดงความหมาย / grammar / contract
```

สิ่งที่ควรรับแรงต่อ:

```text
MPCP : Hyper Lib
MPCP : Hyper Condien
```

---

## 3.1 MPCP : Hyper Lib

```text
MPCP Hyper Lib
= คลังความสามารถระดับข้าม ENV / OS / platform
= รู้ว่า SynCap หรือ tool ไหนใช้กับสภาพแวดล้อมไหน
= สนับสนุน Cross-LGU และ Hub
```

---

## 3.2 MPCP : Hyper Condien

```text
MPCP Hyper Condien
= ชั้นข้อมูล / สถานะระดับข้ามระบบ
= เก็บ context, state, condition, hub state, link state
= ช่วยไม่ให้ Cross-LGU แบก state เอง
```

Flow ที่ต้องการ:

```text
Cross-LGU อ่าน / ครอบความหมาย
↓
ส่งค่าให้ MPCP
↓
MPCP Hyper Lib เลือกความสามารถที่เกี่ยวข้อง
↓
MPCP Hyper Condien เตรียม state / context / condition
↓
HybridCross Hub ใช้ข้อมูลนี้ตัดสิน route
↓
LRC2 log เข้าออก
```

ประโยคแกน:

```text
Cross-LGU expresses.
MPCP Hyper carries.
Hyper Condien holds state.
HybridCross decides route.
LRC2 remembers.
```

แบบไทย:

```text
Cross-LGU แสดงความหมาย
MPCP Hyper พาข้ามระบบ
Hyper Condien ถือสถานะ
HybridCross เลือกจุดตัด / เส้นทาง
LRC2 จำร่องรอย
```

---

# 4. CollorPaper

เมื่อถึงเวลาจริง Cross-LGU อาจไม่ได้รับ brief เป็น Paper ธรรมดา

แต่จะเป็น:

```text
CollorPaper
```

## 4.1 Meaning

```text
CollorPaper
= Paper + Color State + Rytm + Boundary + Hub/Link Context
```

Paper ธรรมดาบอกว่า:

```text
งานคืออะไร
```

CollorPaper บอกว่า:

```text
งานนี้ควรถูกปฏิบัติต่ออย่างไร
```

CollorPaper ช่วยให้ Cross-LGU อ่าน:

```text
เจตนา
สี / สถานะ
จังหวะ / Rytm
Hub ที่เกี่ยวข้อง
Link ที่ควรวิ่ง
SynCap ที่เป็น candidate
Boundary
Return contract
```

---

## 4.2 Minimal CollorPaper Shape

```text
COLLORPAPER:<id>

COLOR:<red/yellow/green/blue/purple/...>
RYTM:<rock/jazz/edm/ballad/...>
HUB:<HybridCross hub>
LINK:<Hybrid link>
SYNCAP:<Hybrid-SynCap candidate>

INTENT:<เจตนา>
BOUNDARY:<ขอบเขต>
STATE:<observe/review/route/block/ready>
RETURN:<state, reason, trace, mutated, review>
```

---

## 4.3 Color Meaning Draft

```text
GREEN  = stable / pass / ready enough
YELLOW = review / unstable / uncertain
RED    = danger / pressure / block / urgent
BLUE   = signal / monitor / flow / runtime
PURPLE = semantic / relation / meaning layer
BLACK  = deny / stop
WHITE  = unclassified / not yet colored
```

สีไม่ใช่ decoration

```text
Color State = ภาษาสถานะของ Hub / Link / Paper
```

---

# 5. Hub : Color State

งานใหญ่ไม่ควรมีสีเดียวทั้งงาน

งานใหญ่ควรแยกสีตาม Hub ได้

```text
CollorPaper = สีรวมของงาน
Hub Color State = สีของจุดตัดแต่ละจุด
```

ตัวอย่าง:

```text
Project: W3API Gateway Expansion

Main CollorPaper:
COLOR: BLUE
RYTM: EDM
STATE: observe_plan

Hub States:
W3API_GATE_HUB: GREEN
CROSS_LGU_HUB: BLUE
MPCP_HYPER_HUB: YELLOW
HOSPITICATION_HUB: YELLOW
SECURITY_BOUNDARY_HUB: RED
LRC2_TRACE_HUB: BLUE
```

ความหมาย:

```text
งานรวมยังเป็น flow / plan
บาง hub ผ่านแล้ว
บาง hub ต้อง review
บาง hub ห้ามข้ามจนกว่าจะตรวจ
```

สิ่งนี้ช่วยให้ W3 ไม่ต้องตัดสินงานใหญ่แบบหยาบ:

```text
ทั้งงานผ่าน
ทั้งงานล้ม
ทั้งงานรอ
```

แต่ตัดสินแบบละเอียดกว่า:

```text
ส่วนนี้ไปต่อ
ส่วนนี้พัก
ส่วนนี้ review
ส่วนนี้ block
ส่วนนี้ส่ง Hospitication
```

---

# 6. LRC2 Hub Transfer Log

ตัวอย่าง log สำหรับ LRC2:

```json
{
  "event": "hybrid_cross_hub_transfer",
  "hub": "HOSPITICATION_HUB",
  "link": "symptom_link",
  "source": "WE_PAPER",
  "target": "HOSPITICATION",
  "color_state": "YELLOW",
  "decision": "observe",
  "mutated": false,
  "review": true,
  "timestamp": "auto"
}
```

LRC2 ต้องจำ highway trace:

```text
source
hub
link
target
color_state
decision
mutated
review
time
```

---

# 7. Combined Mental Model

```text
Hybrid-SynCap = สิ่งที่ถูกขน / กล่องความสามารถ
HybridCross Hub = จุดที่สิ่งนั้นเข้ามาตัดกัน
Hybrid Link = ทางเชื่อม
Cross-index = แผนที่ถนน
PS-Pcross = คนจัดเส้นทาง
MPCP Hyper = ระบบพาข้าม ENV / OS
Hyper Condien = ชั้นถือสถานะข้ามระบบ
Cross-LGU = ภาษาครอบ
CollorPaper = brief ที่มีสี / สถานะ
LRC2 = คนจำทาง
```

ภาพ flow:

```text
App / Module / Agent / OS Event
↓
CollorPaper / Cross-LGU
↓
Hybrid : Link
↓
HybridCross : Hub
↓
PS-Pcross เลือกทาง
↓
Hybrid-SynCap ถูกเรียกเป็นความสามารถ
↓
MPCP Hyper พาข้าม ENV
↓
LRC2 บันทึกเข้า-ออก
```

---

# 8. Philosophy

เราไม่ได้คิดใหญ่เพื่อให้ดูใหญ่

แต่คิดโครงปลายชั้นเพราะ:

```text
ถ้า Cross ข้าม OS / platform / ENV / EVENT ได้จริง
โครงสร้างต้องชัดเจน
และเปลี่ยนถ่ายได้เร็ว
```

ถ้าไม่มีโครงกลาง:

```text
ส่งต่อผิดทาง
ความสามารถกระจัดกระจาย
แอปภายนอกคุยกับ W3 ยาก
Hospitication รับอาการไม่ตรง format
LRC2 log ไม่เป็นร่องเดียวกัน
MPCP แปลซ้ำทุกครั้ง
Cross-LGU กลายเป็นคอขวด
```

ดังนั้นต้องมี:

```text
Hub
Link
Highway
Capsule
Color State
Log
Route
```

END
