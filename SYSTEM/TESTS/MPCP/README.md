MPCP Protocol Specification v1.0

Project: MPCP
Owner: BBX19
Status: Experimental → Usable Core
License: Define per repository policy

---

Overview

MPCP (Multi Purpose Context Protocol) is a lightweight structured text protocol designed for:

- Environment blueprints
- Runtime configuration
- Cross-platform messaging
- Data serialization
- Embedded/mobile systems
- Human-readable machine parsing

MPCP uses symbolic grammar with predictable separators.

---

Design Goals

- Single grammar system
- Low memory parsing
- Easy manual writing
- Easy debugging from logs
- Cross-platform compatible
- Deterministic parsing
- Expandable version path

---

Core Symbols

Symbol| Meaning| Scope
":"| Key / Value separator| Namespace split
","| Independent item separator| Record level
"'"| Shared field separator| Internal group fields
"* *"| Block wrapper| Structured value
";"| Optional packet terminator| End marker

---

Semantic Rules

"," Item Separator

Separates independent values or records.

Example:

USER:john,ROLE:admin,AGE:25

---

"'" Field Separator

Separates values sharing the same context.

Example:

*23'15'11'40*

Means:

[23,15,11,40]

---

"* *" Block Wrapper

Defines grouped structured data.

Example:

PKG:*10'15'3*

---

Packet Format

HEADER:VALUE,HEADER:VALUE,...

---

Formal Grammar

PACKET := ITEM ( , ITEM )*
ITEM   := KEY : VALUE
VALUE  := RAW | BLOCK
BLOCK  := * FIELD ( ' FIELD )* *
FIELD  := TEXT | NUMBER
KEY    := ALPHA+

---

Data Types

Raw String

MODE:debug

Integer

RAM:256

Block List

PKG:*10'22'31*

---

Examples

Runtime Config

SYS:core,RUN:python,RAM:256

Package Blueprint

PKG:*10'15'3*

User Record

USER:john,ROLE:admin,AGE:25

Mixed Packet

APP:calc,LIB:*12'15*,MODE:fast

---

Parsing Result Example

Input:

SYS:core,RUN:python,PKG:*10'15'3*

Output:

{
  "SYS": "core",
  "RUN": "python",
  "PKG": [10,15,3]
}

---

Validation Rules

Parser must reject:

- Missing ":"
- Unclosed "*"
- Empty key
- Illegal separators
- Invalid block structure

---

Recommended Implementation Layers

Module Flow

Input -> Parse -> Validate -> Execute -> Output

Memory Role

Log only:

- raw packet
- parsed object
- status
- timestamp

---

Cross Platform Targets

Compatible with:

- 
- 
- 
- Embedded runtimes
- CLI systems

---

Python Reference Parser

def parse(packet):
    ...

(see "/reference/python/")

---

Roadmap

v1

- Core grammar
- Flat packets
- Block lists
- Validation

v2

- Nested objects
- Type prefixes
- Packet checksum
- Length fields

v3

- Binary transport mode
- Streaming parser
- Runtime native integration

---

Repository Structure

/
├── README.md
├── SPEC.md
├── examples/
├── reference/
│   └── python/
├── tests/
└── docs/

---

Recommended README Short Intro

MPCP is a lightweight symbolic protocol for portable systems, blueprints, and runtime messaging.

---

Maintainer Notes

All future revisions should preserve:

- deterministic parsing
- backward compatibility where possible
- human readability
- reversible structured values
- low resource execution

---

Version

MPCP Protocol Specification v1.0
