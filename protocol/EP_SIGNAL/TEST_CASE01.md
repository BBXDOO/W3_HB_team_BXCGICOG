TEST_CASES.md

EP Signal Encoding Protocol โ€” Validation Set v1

---

Purpose

This file defines practical test cases for verifying EP encoder / decoder behavior.

Used for:

- Manual testing
- Parser development
- W3 integration
- Format stability checks

---

Test Group A โ€” Basic Binary

Case| Binary Input| Expected EP
A1| "0"| "0/1-0'BIN"
A2| "1"| "1/1-1'BIN"
A3| "00"| "0/2-0'BIN"
A4| "11"| "1/2-2'BIN"
A5| "01"| "0/11-1'BIN"
A6| "10"| "1/11-1'BIN"

---

Test Group B โ€” Alternating Pattern

Case| Binary Input| Expected EP
B1| "1010"| "1/1111-2'BIN"
B2| "0101"| "0/1111-2'BIN"
B3| "10101010"| "1/11111111-4'BIN"

---

Test Group C โ€” Repeated Blocks

Case| Binary Input| Expected EP
C1| "000111"| "0/33-3'BIN"
C2| "111000"| "1/33-3'BIN"
C3| "00110011"| "0/2222-4'BIN"

---

Test Group D โ€” Original Example

Case| Binary Input| Expected EP
D1| "0011010110111000"| "0/221112133-8'BIN"

---

Decode Validation Steps

For each EP string:

1. Read HEADER
2. Expand PAYLOAD by alternating states
3. Count total logical "1" values
4. Compare with VERIFY field
5. Confirm FORMAT type

---

Manual Decode Example

Input:

0/22-2'BIN

Process:

- Start = "0"
- Run lengths = "2 , 2"
- Output = "00 11"

Final:

0011

Validation:

two logical ones = pass

---

Failure Tests

Case| Input| Reason
F1| "0/22-1'BIN"| Wrong verify count
F2| "2/22-2'BIN"| Invalid header
F3| "0//2'BIN"| Missing payload
F4| "0/22-2'XYZ"| Unknown format

---

Notes

All future EP versions must remain backward-testable against v1 baseline.
