↩️ [กลับไป Apps Manual Hub](../INDEX.md)

# 📱 คู่มือ Termux + GitHub (ภาษาไทย)

> **สำหรับมือใหม่** — ใช้งานได้จริงบนมือถือ Android ทุกขั้นตอน

---

## 1) ติดตั้ง Termux

### ดาวน์โหลด
- ❌ **อย่าใช้ Play Store** (เวอร์ชันเก่า ไม่ได้รับการอัปเดต)
- ✅ ดาวน์โหลดจาก **F-Droid** หรือ **GitHub Releases** เท่านั้น:
  - F-Droid: [https://f-droid.org/packages/com.termux/](https://f-droid.org/packages/com.termux/)
  - GitHub: [https://github.com/termux/termux-app/releases](https://github.com/termux/termux-app/releases)

### อัปเดต package แรกที่ต้องทำ
เปิด Termux แล้วพิมพ์คำสั่งตามลำดับ:

```bash
pkg update && pkg upgrade -y
```

> รอให้เสร็จ (อาจใช้เวลา 2–5 นาที)

---

## 2) ติดตั้ง Git และตั้งค่าเบื้องต้น

### ติดตั้ง git

```bash
pkg install git -y
```

### ตั้งชื่อและอีเมล (บังคับก่อน commit)

```bash
git config --global user.name "ชื่อของคุณ"
git config --global user.email "email@example.com"
```

### ตรวจสอบว่าตั้งค่าถูกต้อง

```bash
git config --list
```

> ควรเห็น `user.name` และ `user.email` ที่ตั้งไว้

---

## 3) Clone Repository

### วิธีที่ 1 — ผ่าน HTTPS (ง่าย แต่ต้องใส่ token ทุกครั้ง)

```bash
git clone https://github.com/USERNAME/REPO_NAME.git
```

ตัวอย่าง:

```bash
git clone https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
```

### วิธีที่ 2 — ผ่าน SSH (แนะนำ ไม่ต้องใส่รหัสซ้ำ)

```bash
git clone git@github.com:USERNAME/REPO_NAME.git
```

ตัวอย่าง:

```bash
git clone git@github.com:BBXDOO/W3_HB_team_BXCGICOG.git
```

> ⚠️ ต้องตั้งค่า SSH key ก่อน (ดูหัวข้อ 5)

### เข้าไปในโฟลเดอร์ repo

```bash
cd REPO_NAME
```

---

## 4) Commit และ Push

### ขั้นตอนมาตรฐาน

```bash
# 1. ดูสถานะไฟล์ที่เปลี่ยนแปลง
git status

# 2. เพิ่มไฟล์ที่ต้องการ commit (หรือทั้งหมด)
git add ชื่อไฟล์.md
# หรือเพิ่มทุกไฟล์:
git add .

# 3. Commit พร้อมข้อความ
git commit -m "feat: เพิ่มไฟล์ใหม่"

# 4. Push ขึ้น GitHub
git push origin ชื่อ-branch
```

### ตัวอย่างจริง

```bash
git status
git add knowledge/apps_manual/android/termux_github.md
git commit -m "docs: add termux github guide"
git push origin main
```

### เช็ค log commit ที่ผ่านมา

```bash
git log --oneline -5
```

---

## 5) ตั้งค่า SSH Key (แนะนำ)

### สร้าง SSH Key ใหม่

```bash
ssh-keygen -t ed25519 -C "email@example.com"
```

> กด Enter ผ่านทุก prompt (หรือตั้ง passphrase ก็ได้)

### ดู Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

> คัดลอกทั้งหมด (ขึ้นต้นด้วย `ssh-ed25519 ...`)

### เพิ่ม Key บน GitHub
1. เปิด [https://github.com/settings/ssh/new](https://github.com/settings/ssh/new)
2. ตั้งชื่อ (เช่น `Termux Android`)
3. วาง Public Key ลงช่อง **Key**
4. กด **Add SSH key**

### ทดสอบการเชื่อมต่อ

```bash
ssh -T git@github.com
```

> ถ้าสำเร็จจะขึ้นว่า: `Hi USERNAME! You've successfully authenticated...`

---

## 6) ใช้ Personal Access Token (HTTPS แทน SSH)

เหมาะสำหรับกรณีที่ไม่ต้องการใช้ SSH

### สร้าง Token บน GitHub
1. ไปที่ [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)
2. ตั้งชื่อ token (เช่น `Termux`)
3. เลือกสิทธิ์: ✅ `repo` (อย่างน้อย)
4. กด **Generate token**
5. **คัดลอก token ทันที** — จะดูได้ครั้งเดียว!

### ใช้ Token แทนรหัสผ่าน

เมื่อ git ถาม password ให้วาง token แทน:

```bash
git push origin main
# Username: your_github_username
# Password: <วาง token ที่นี่>
```

### บันทึก Credential (ไม่ต้องพิมพ์ซ้ำ)

```bash
git config --global credential.helper store
```

> ครั้งต่อไป git จะจำ token ให้อัตโนมัติ

---

## 7) คำสั่งที่ใช้บ่อย (Quick Reference)

| คำสั่ง | ความหมาย |
|---|---|
| `git status` | ดูสถานะไฟล์ |
| `git add .` | เตรียมไฟล์ทั้งหมด |
| `git commit -m "..."` | บันทึก commit |
| `git push origin main` | ส่งขึ้น GitHub |
| `git pull` | ดึงอัปเดตล่าสุด |
| `git branch` | ดู branch ทั้งหมด |
| `git checkout -b ชื่อ` | สร้าง branch ใหม่ |
| `git log --oneline` | ดูประวัติ commit |
| `git diff` | ดูการเปลี่ยนแปลง |

---

## 8) ปัญหาที่พบบ่อย + วิธีแก้

- **อาการ:** `Permission denied (publickey)`
  **วิธีแก้:** ยังไม่ได้เพิ่ม SSH key บน GitHub → ทำตามหัวข้อ 5

- **อาการ:** `remote: Support for password authentication was removed`
  **วิธีแก้:** GitHub ไม่รับ password แล้ว ต้องใช้ Token (หัวข้อ 6) หรือ SSH (หัวข้อ 5)

- **อาการ:** `error: src refspec main does not match any`
  **วิธีแก้:** ยังไม่มี commit ให้ทำ `git add . && git commit -m "init"` ก่อน push

- **อาการ:** `Please tell me who you are` / ขอชื่อและอีเมล
  **วิธีแก้:** ตั้งค่าตามหัวข้อ 2 (`git config --global user.name / user.email`)

- **อาการ:** `Updates were rejected` (push ไม่ผ่าน)
  **วิธีแก้:** ดึงอัปเดตก่อน: `git pull origin main --rebase` แล้วค่อย push

---

## Quick Link
- Apps Manual Hub: `knowledge/apps_manual/INDEX.md`
- Template: `knowledge/apps_manual/templates/app_manual_template.md`
- GitHub SSH Keys: [https://github.com/settings/keys](https://github.com/settings/keys)
- GitHub Tokens: [https://github.com/settings/tokens](https://github.com/settings/tokens)
