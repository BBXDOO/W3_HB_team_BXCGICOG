# EP_SIGNAL Integration Guide (W3Lgu / mpcp)

## Overview

ชุดเครื่องมือ EP_SIGNAL นี้ออกแบบให้เชื่อมต่อข้อมูลกับระบบภายนอกทั้ง W3Lgu และ mpcp ได้โดยตรง  
- สามารถรับข้อมูล binary/raw มา encode เป็นรูปแบบ EP-SIGNAL ทันที  
- สามารถถอดกลับ binary เพื่อนำไปใช้ใน logic logic หรือ hardware interface ปลายทาง

## Example

### Connect with W3Lgu

```python
from ep_signal_adapter import interop_with_w3lgu

w3lgu_payload = bytes([0b11001100, 0b10101010])
epencoded = interop_with_w3lgu(w3lgu_payload)
print("EP Signal format:", epencoded)
# สามารถ decode คืนค่าเดิมได้
```

### ใช้กับ mpcp

```python
from ep_signal_adapter import interop_with_mpcp

mp_payload = "110100110101"
epencoded = interop_with_mpcp(mp_payload)
```

## Benchmark

งาน encode/decode ข้อมูลที่ payload ขนาด 128 bytes:  
- encode ≈ 1-3 ms  
- decode ≈ 1-3 ms

## Attention

หากต้องใช้กับระบบที่ต้องการ performance สูง ให้ batch encode/decode เป็น block เพื่อประหยัดเวลา

---
