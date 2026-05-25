COLOR_SYMBOL_PAPER.md

mpcp Color & Symbol System

This paper defines the visual communication layer of mpcp.

The purpose is immediate understanding without reading long text.

Use color and symbols as fast signals for status, priority, risk, and action direction.

---

Core Principle

See first.
Read second.
Act clearly.

---

Color Standard

Green

Meaning:

- safe
- pass
- ready
- stable
- completed

Examples:

Validation passed
Ready to merge
Task completed

---

Yellow

Meaning:

- caution
- review needed
- uncertain
- observe
- pending attention

Examples:

Need review
Possible issue
Check input

---

Red

Meaning:

- blocked
- fail
- critical risk
- stop
- action required now

Examples:

Validation failed
Security issue
Deployment blocked

---

Blue

Meaning:

- information
- external source
- neutral notice
- documentation
- reference state

Examples:

Info update
Linked source
Documentation only

---

Gray

Meaning:

- idle
- inactive
- archived
- no active state

Examples:

No process
Waiting
Disabled Modew

---

Symbol Standard

✓

Success / approved / pass

!

Attention / warning / check now

✕

Failure / rejected / blocked

●

Focus point / item requires attention

▲

Priority / force / top importance

◆

External / network / linked source

→

Flow / next step / transfer

⟳

Running / processing / retry

■

Stable result / fixed state

---

Combined Usage

Green + ✓

Approved / safe complete

Yellow + !

Warning / review required

Red + ✕

Blocked / failure

Blue + ◆

External reference / connected source

Gray + ■

Inactive stable state

---

Modew Example

MODEW:Validation
COLOR:Green
SYM:✓
STATE:ready

MODEW:Review
COLOR:Yellow
SYM:!
STATE:wait

MODEW:Deploy
COLOR:Red
SYM:✕
STATE:block

---

Papet Example

TASK:merge,COLOR:Green,SYM:✓
CHECK:input,COLOR:Yellow,SYM:!
DEPLOY:prod,COLOR:Red,SYM:✕
DOC:read,COLOR:Blue,SYM:◆

---

Usage Rules

- One primary color per item
- One primary symbol per item
- Do not mix meanings
- Use familiar global meanings
- Prefer instant recognition

---

Human Goal

User should understand state in 1 second.

---

System Goal

Machine can parse values directly.

---

Status

mpcp Visual Layer v1

---

Owner

BBX19
