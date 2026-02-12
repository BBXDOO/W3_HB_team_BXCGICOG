# Consciousness Feed

**Module:** DeepSeek Studio  
**Component:** Core  
**Created:** 2025-12-01

## Purpose
บันทึกสถานะและการตระหนักรู้ของระบบในแต่ละช่วงเวลา

## Feed Format
```json
{
  "timestamp": "ISO 8601",
  "system_state": "string",
  "active_modules": ["array"],
  "insights": "string"
}
```

## Integration
ส่งข้อมูลไปยัง wisdom/learning-loops/ เพื่อการเรียนรู้ต่อเนื่อง
