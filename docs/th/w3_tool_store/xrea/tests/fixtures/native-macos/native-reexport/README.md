# load command แบบ re-export ที่สร้างจากซอร์ส

ต้นฉบับ: [Source-built re-export load command](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/native-reexport/README.md)

เก็บข้อมูลจากซอร์ส C ที่อยู่ข้างกันโดยใช้เครื่องมือ Xcode ของเครื่อง macOS arm64:

```sh
xcrun clang -dynamiclib leaf.c -Wl,-install_name,@rpath/libLeaf.dylib -o libLeaf.dylib
xcrun clang -dynamiclib outer.c -Wl,-reexport_library,libLeaf.dylib -o libOuter.dylib
xcrun otool -l libOuter.dylib > otool-load.txt
```

แทนที่พาธชั่วคราวของไลบรารีชั้นนอกด้วย `/owned/libOuter.dylib` นอกนั้นฟิลด์
load command ไม่ถูกแก้ไข ข้อมูลที่เก็บไว้ยังคง re-export, ID และ dependency ปกติของ
libSystem ที่เกิดขึ้นจริงไว้ โดยใช้พิสูจน์การแยกวิเคราะห์รูปแบบ ไม่ใช่พฤติกรรมของ
Hopper หรือ Ghidra
