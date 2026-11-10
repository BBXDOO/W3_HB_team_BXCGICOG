# ข้อมูลข้อความ load command แบบ native

ต้นฉบับ: [Native load-command text captures](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/load-command-text-values/README.md)

ข้อมูลเหล่านี้เป็นผลลัพธ์จริงของ `xcrun otool -l` สำหรับ dylib ที่สร้างจาก `fixture.c`
ด้วย Apple clang โดยแทนที่เฉพาะพาธไฟล์ผลลัพธ์ที่เป็นของเราในแต่ละชุดข้อมูลด้วย
`/owned/fixture.dylib` ไม่มีการ commit หรือรันไบนารีของ fixture

สำหรับ install name แต่ละค่า `123 library.dylib`, `0x123 library.dylib`, `123`,
`0x123` และ `ordinary.dylib`:

```sh
xcrun clang -dynamiclib fixture.c "-Wl,-install_name,$INSTALL_NAME" -o fixture.dylib
xcrun otool -l fixture.dylib
```

install name เป็นฟิลด์ข้อความ แม้ token แรกจะดูเหมือนเลขฐานสิบหรือเลขฐานสิบหก
ข้อมูลที่เก็บไว้ยังคงฟิลด์ตัวเลขปกติของช่วงไบต์ สิทธิ์ และขนาดคำสั่งไว้เป็นตัวควบคุมด้วย
