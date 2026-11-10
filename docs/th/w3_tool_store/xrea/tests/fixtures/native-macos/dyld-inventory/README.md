# ข้อมูล inventory แบบ native ของ Apple ที่บันทึกไว้

ต้นฉบับ: https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/dyld-inventory/README.md

ผลลัพธ์เหล่านี้บันทึกจากเครื่องมือ Apple ที่ติดตั้งบน macOS arm64
ชื่อไฟล์ของไฟล์ปฏิบัติการในผลลัพธ์ของเครื่องมือถูกแทนด้วย `fixture` ดัชนี
เลขฐานสิบหกของ import เป็น binding ordinal ส่วนตาราง export มีออฟเซ็ตของอิมเมจ
export แบบ absolute ไม่สัมพันธ์กับฐานของอิมเมจ `nm` ยังรายงานชื่อที่ export
แต่ละชื่อด้วย เพื่อทดสอบการรวมข้อมูลที่ต้องรักษาข้อเท็จจริงจาก dyld ที่มีรายละเอียดมากกว่า

สร้างไฟล์ปฏิบัติการบนเครื่องของตนเอง อย่าเช็กอินไบนารีลงในที่เก็บ:

```sh
cat > /tmp/rea-inventory.c <<'C'
#include <stdio.h>
__attribute__((weak)) int fixture_weak(void) { return 2; }
int fixture_export(void) { return 1; }
__asm__(".globl _fixture_absolute\n.set _fixture_absolute, 0x42");
int main(void) { puts("fixture"); return fixture_export() + fixture_weak(); }
C
xcrun clang /tmp/rea-inventory.c -o /tmp/rea-inventory
xcrun file -b /tmp/rea-inventory
xcrun lipo -detailed_info /tmp/rea-inventory
xcrun otool -l /tmp/rea-inventory
xcrun nm -gjU /tmp/rea-inventory
xcrun dyld_info -imports /tmp/rea-inventory
xcrun dyld_info -exports /tmp/rea-inventory
xcrun dwarfdump --uuid /tmp/rea-inventory
xcrun vtool -show-build /tmp/rea-inventory
```

ที่อยู่ UUID และเวอร์ชันบิลด์อาจแตกต่างกันตามชุดเครื่องมือที่ติดตั้ง
ข้อมูลที่บันทึกและเช็กอินไว้คืออินพุต golden การทดสอบตรวจสอบที่อยู่เสมือน
ซึ่งสอดคล้องกับออฟเซ็ตและฐานอิมเมจที่บันทึกไว้เหล่านั้น

`../dyld-imports.txt` มีส่วนหัวและแถวตัวอย่าง import แบบปกติและ weak
ตามต้นฉบับทุกประการจาก `xcrun dyld_info -imports /usr/lib/libobjc.A.dylib`
`library-reexports.txt` มีส่วนหัวและแถว reexport หนึ่งแถวจาก
`xcrun dyld_info -exports /usr/lib/libc++.1.dylib` ข้อมูลที่บันทึกจากไลบรารีเหล่านี้
แยกจากกันเพื่อใช้ตรวจสอบรูปแบบแถวของแต่ละรายการ

`renamed-reexports.txt` เป็นผลจาก `xcrun dyld_info -exports` สำหรับ dylib ที่
re-export `_foo` จาก `libfoo` ภายใต้ชื่อ `_foo_renamed`:

```sh
printf 'int foo(void){return 1;}\n' > /tmp/foo.c
printf 'int own(void){return 2;}\n' > /tmp/re.c
xcrun clang -dynamiclib /tmp/foo.c -o /tmp/libfoo.dylib -install_name @rpath/libfoo.dylib
xcrun clang -dynamiclib /tmp/re.c -o /tmp/libre.dylib -install_name @rpath/libre.dylib \
  /tmp/libfoo.dylib -Wl,-alias,_foo,_foo_renamed
xcrun dyld_info -exports /tmp/libre.dylib
xcrun nm -gjU /tmp/libre.dylib
```

`stripped-swift-exports.txt` และ `stripped-swift-nm.txt` เป็นผลจาก `xcrun dyld_info
-exports` และ `xcrun nm -gjU` แบบปริยายสำหรับ Swift dylib ที่ตารางสัญลักษณ์
ถูกตัดออกด้วย `strip -T` export trie ของมันยังคงเก็บทั้งหกชื่อไว้ ขณะที่
`xcrun nm -gjU --no-dyldinfo` ไม่พิมพ์ชื่อใดเลย:

```sh
printf 'public func hello() -> Int { 1 }\npublic struct S { public init() {} ; public func f() -> Int { 2 } }\n' > /tmp/m.swift
xcrun swiftc -emit-library -module-name M /tmp/m.swift -o /tmp/libMT.dylib
xcrun strip -T /tmp/libMT.dylib
xcrun dyld_info -exports /tmp/libMT.dylib
xcrun nm -gjU /tmp/libMT.dylib
xcrun nm -gjU --no-dyldinfo /tmp/libMT.dylib
```

`codesign-missing.txt` คือ stderr จาก `codesign -d --verbose=4` บนพาธที่ไม่มีอยู่
(exit 1) ส่วน `codesign-unsigned.txt` คือ stderr จากคำสั่งเดียวกันบนสำเนา
ของฟิกซ์เจอร์หลังจากใช้ `codesign --remove-signature` (exit 1) มีเพียงกรณีหลังเท่านั้น
ที่เป็นข้อสังเกตว่าอาร์ติแฟกต์ไม่ได้ลงลายเซ็น
