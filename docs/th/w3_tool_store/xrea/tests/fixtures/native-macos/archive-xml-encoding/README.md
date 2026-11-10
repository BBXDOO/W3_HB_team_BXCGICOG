# fixture การเข้ารหัส XML archive ของ Foundation

ต้นฉบับ: [Foundation XML archive encoding fixture](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/archive-xml-encoding/README.md)

`producer.swift` สร้างข้อมูล XML จริงจาก NSKeyedArchiver แล้วใช้การเข้ารหัสสตริงของ
Foundation สร้างกราฟ XML เดียวกันในรูป UTF-16 ทั้งแบบ little-endian และ big-endian
ที่มีเครื่องหมาย BOM โดย PropertyListSerialization ของ Foundation อ่านได้ทั้งสองรูปแบบ
และ `plutil -lint` ก็ยอมรับไฟล์ทั้งสามเช่นกัน

```sh
xcrun swiftc producer.swift -o writer
./writer archive.xml little-endian.plist big-endian.plist
plutil -lint archive.xml little-endian.plist big-endian.plist
```

มีการ commit เฉพาะข้อมูล XML ต้นทางแบบ UTF-8 เท่านั้น การทดสอบเข้ารหัสข้อความเดียวกัน
เป็น UTF-16 จึงไม่ต้อง commit ไบนารีที่คอมไพล์แล้วหรือ fixture แบบไบนารี นี่คือการตรวจสอบ
รูปแบบและระบบไฟล์ โดย REA ไม่ได้สร้างอินสแตนซ์ของคลาสใด ๆ จาก archive
