# Cross-L / CrossLgu Language Tag Table

**Document Path:** `croll/CROSS_L_LANGUAGE_TAG_TABLE.md`  
**Status:** ACTIVE DRAFT  
**System Relation:** W3 / CROLL / Cross-L / CrossLgu / Modew / MPCP  
**Owner:** BBX19  
**Purpose:** ตารางอ้างอิงชื่อภาษา / ตัวย่อ / ประเภทงาน สำหรับใช้สร้าง Tag, Logic, Blueprint, Paper และ Cross-Lgu Unit

---

# 1. Core Statement

เอกสารนี้คือรายชื่อภาษา สคริปต์ คอนฟิก และรูปแบบเอกสารที่อาจถูกใช้ใน Cross-L / CrossLgu

เป้าหมายไม่ใช่จำทุกภาษา แต่เพื่อให้ W3 มีตารางอ้างอิงว่า:

```text
ภาษา / รูปแบบนี้
เหมาะกับงานแบบไหน
ควรใช้ tag อะไร
และอธิบายสั้น ๆ อย่างไร
```

ในแนวคิด Cross-Lgu ภาษาไม่ได้ถูกเลือกเพราะนิยม แต่ถูกเลือกเพราะเหมาะกับหน้าที่ของงาน

---

# 2. Tag Rule

รูปแบบ tag แนะนำ:

```text
TYPE:ABBR
```

ตัวอย่าง:

```text
GEN:PY
SCRIPT:BASH
CONFIG:JSON
DOC:MD
LOW:CPP
QUERY:SQL
```

---

# 3. Core Cross-Lgu Starter Set

| Type | Name | Short | Use |
|---|---|---:|---|
| Host / Glue | Python | PY | คุม flow, glue, orchestration, script หน้างาน |
| Embedded Logic | Lua | LUA | logic เบา ฝังตัว แก้ rule เร็ว |
| Fast Engine | C++ | CPP | งานเร็ว engine compute หนัก |
| Packet / Config | JSON | JSON | packet, config, data contract |
| ENV Config | YAML | YML | env, workflow, deployment config |
| Human Law | Markdown | MD | paper, law, report, docs ให้คนอ่าน |
| Trace | TXT | TXT | trace, state, note เบา ๆ |
| Command Runner | Bash | BASH | สั่งงานใน Termux / Linux / ENV |
| Storage Query | SQL | SQL | query, storage, report data |
| Portable Runtime | WebAssembly | WASM | runtime พกพาข้าม platform |
| ENV Package | Dockerfile | DOCKER | package สภาพแวดล้อม |
| Boundary Config | ENV | ENV | ค่าระบบ, secret placeholder, runtime variable |

---

# 4. General Purpose / ภาษาหลักทั่วไป

| Name | Short | Use |
|---|---:|---|
| Python | PY | เขียนง่าย ใช้คุมระบบ glue automation AI data |
| JavaScript | JS | เว็บ frontend/backend runtime กว้าง |
| TypeScript | TS | JavaScript แบบมี type เหมาะกับระบบใหญ่ |
| Java | JAVA | enterprise, backend, Android legacy |
| C# | CS | .NET, enterprise, game Unity |
| C | C | low-level, embedded, system library |
| C++ | CPP | engine, performance, native app |
| Go | GO | server, tooling, concurrency, cloud |
| Rust | RS | safe systems, performance, CLI, WASM |
| Ruby | RB | scripting, web, automation |
| PHP | PHP | web backend, CMS, server rendering |
| Swift | SWIFT | iOS/macOS app |
| Kotlin | KT | Android, JVM backend |
| Dart | DART | Flutter app, cross-platform UI |
| Scala | SCALA | JVM, big data, functional/OOP mix |
| Perl | PL | text processing, legacy scripting |
| Lua | LUA | embedded logic, game scripting, lightweight rule |
| Raku | RAKU | scripting, text, experimental language |
| Nim | NIM | compiled language, Python-like syntax |
| Zig | ZIG | systems programming, C alternative |
| Crystal | CR | Ruby-like compiled language |
| D | D | systems / native programming |
| V | V | simple compiled language |
| Mojo | MOJO | AI/performance-oriented Python-like language |
| Carbon | CARBON | experimental C++ successor direction |

---

# 5. Scripting / Automation

| Name | Short | Use |
|---|---:|---|
| Bash | BASH | Linux/Termux command automation |
| Shell | SHL | generic shell script family |
| sh | SH | POSIX-style shell script |
| Zsh | ZSH | interactive shell, scripting |
| Fish | FISH | user-friendly shell |
| PowerShell | PS1 | Windows / cross-platform automation |
| Batch | BAT | Windows command script |
| Python | PY | automation script, CLI helper |
| Perl | PL | text-heavy automation |
| Ruby | RB | developer automation / scripting |
| Lua | LUA | embedded automation / config logic |
| Tcl | TCL | scripting, embedding, test tools |
| Awk | AWK | line/text processing |
| Sed | SED | stream editing |
| AutoHotkey | AHK | Windows automation / hotkey |
| AutoIt | AU3 | Windows GUI automation |
| AppleScript | APPLESCRIPT | macOS automation |
| VBA | VBA | Microsoft Office automation |

---

# 6. Web Frontend / UI

| Name | Short | Use |
|---|---:|---|
| HTML | HTML | document structure for web |
| CSS | CSS | style/layout for web |
| JavaScript | JS | browser logic |
| TypeScript | TS | typed browser/app logic |
| JSX | JSX | React component syntax |
| TSX | TSX | React component with TypeScript |
| Vue | VUE | Vue component file |
| Svelte | SVELTE | Svelte component file |
| Astro | ASTRO | content/site component framework |
| MDX | MDX | Markdown + JSX documentation/content |
| SCSS | SCSS | CSS preprocessor syntax |
| Sass | SASS | CSS preprocessor |
| Less | LESS | CSS preprocessor |
| Stylus | STYL | CSS preprocessor |
| PostCSS | POSTCSS | CSS transform pipeline |

---

# 7. Web Backend / Server

| Name | Short | Use |
|---|---:|---|
| Python | PY | FastAPI, Flask, backend API |
| JavaScript | JS | Node.js backend |
| TypeScript | TS | typed Node.js backend |
| PHP | PHP | web server backend |
| Ruby | RB | Rails/Sinatra backend |
| Java | JAVA | enterprise backend |
| C# | CS | .NET backend |
| Go | GO | fast API/server |
| Rust | RS | high-performance backend |
| Kotlin | KT | JVM backend |
| Scala | SCALA | JVM backend/big data |
| Elixir | EX | fault-tolerant web/backend |
| Erlang | ERL | telecom/fault-tolerant runtime |
| Perl | PL | legacy web/backend scripts |
| Lua | LUA | embedded server logic, Nginx/OpenResty style |

---

# 8. Config / Settings / Environment

| Name | Short | Use |
|---|---:|---|
| JSON | JSON | structured data/config packet |
| YAML | YML | workflow/env/deploy config |
| TOML | TOML | project/app config |
| XML | XML | structured document/config legacy |
| INI | INI | simple key-value config |
| ENV | ENV | environment variable file |
| Properties | PROP | Java/app config key-value |
| HCL | HCL | Terraform-style infrastructure config |
| Dockerfile | DOCKER | container build recipe |
| Docker Compose | COMPOSE | multi-container config |
| Nginx Config | NGINX | Nginx server config |
| Apache Config | APACHE | Apache server config |
| EditorConfig | EDITORCFG | editor formatting rules |
| Gitignore | GITIGNORE | ignored files rule |
| Gitattributes | GITATTR | git file behavior rules |
| Procfile | PROC | process declaration for deployment |

---

# 9. Data / Schema / API Contract

| Name | Short | Use |
|---|---:|---|
| JSON | JSON | data packet / API body |
| XML | XML | structured exchange format |
| CSV | CSV | table-like data exchange |
| SQL | SQL | database query / schema |
| GraphQL | GQL | API query contract |
| Protocol Buffers | PROTO | compact typed message contract |
| Thrift | THRIFT | cross-language RPC schema |
| Avro | AVRO | data serialization schema |
| OpenAPI | OAPI | REST API contract |
| Swagger | SWAGGER | REST API documentation/contract |
| JSON Schema | JSCHEMA | JSON validation/schema |
| RDF | RDF | semantic web data model |
| Turtle | TTL | RDF text syntax |
| SPARQL | SPARQL | RDF query language |
| XPath | XPATH | XML path query |
| XSLT | XSLT | XML transform |

---

# 10. Database / Query

| Name | Short | Use |
|---|---:|---|
| SQL | SQL | relational query language |
| PL/SQL | PLSQL | Oracle database procedure language |
| T-SQL | TSQL | Microsoft SQL Server procedure/query |
| Cypher | CYPHER | graph database query |
| Gremlin | GREMLIN | graph traversal query |
| SPARQL | SPARQL | semantic/RDF query |
| Datalog | DATALOG | logic database/query language |
| PromQL | PROMQL | Prometheus metrics query |
| LogQL | LOGQL | Loki log query |
| KQL | KQL | Kusto/Azure query language |

---

# 11. DevOps / Infrastructure

| Name | Short | Use |
|---|---:|---|
| Bash | BASH | Linux automation |
| PowerShell | PS1 | Windows/cloud automation |
| Dockerfile | DOCKER | container image build |
| Docker Compose | COMPOSE | local multi-service runtime |
| Terraform | TF | infrastructure provisioning |
| HCL | HCL | Terraform config syntax |
| Ansible | ANSIBLE | configuration automation |
| Puppet | PUPPET | infrastructure configuration |
| Chef | CHEF | infrastructure automation |
| Helm | HELM | Kubernetes package template |
| Kubernetes YAML | K8S | Kubernetes resource config |
| Nix | NIX | reproducible environment/package config |
| Dhall | DHALL | typed configuration language |
| Starlark | STAR | Bazel config/script language |
| Bazel | BAZEL | build system config |
| Buck | BUCK | build system config |
| Earthly | EARTHLY | build pipeline file |
| Justfile | JUST | command recipe file |
| Taskfile | TASK | task runner config |
| Makefile | MAKE | build/task automation |
| CMake | CMAKE | C/C++ build config |
| Meson | MESON | native build config |
| Gradle | GRADLE | JVM/Android build config |
| Maven POM | POM | Java project build XML |

---

# 12. Documentation / Human Meaning

| Name | Short | Use |
|---|---:|---|
| Markdown | MD | docs, paper, report, law |
| TXT | TXT | plain note, simple trace |
| reStructuredText | RST | Python docs / technical docs |
| AsciiDoc | ADOC | structured technical docs |
| Org Mode | ORG | notes, planning, literate config |
| LaTeX | TEX | academic/math documents |
| BibTeX | BIB | bibliography metadata |
| MDX | MDX | docs with components |
| Mermaid | MMD | text-based diagrams |
| PlantUML | PUML | UML diagrams by text |
| Graphviz DOT | DOT | graph diagrams |

---

# 13. Game / Interactive / Creative

| Name | Short | Use |
|---|---:|---|
| Lua | LUA | game scripting / embedded rule |
| GDScript | GDS | Godot game scripting |
| C# | CS | Unity / Godot / game logic |
| C++ | CPP | game engine performance |
| JavaScript | JS | browser game / interactive logic |
| TypeScript | TS | typed browser game logic |
| Ren'Py | RENPY | visual novel scripting |
| Ink | INK | interactive narrative scripting |
| Yarn Spinner | YARN | dialogue / narrative scripting |
| Scratch | SCRATCH | visual beginner programming |
| Blockly | BLOCKLY | block-based programming |
| Processing | P5 | creative coding / visual sketch |
| OpenSCAD | SCAD | parametric 3D model scripting |

---

# 14. Mobile / App

| Name | Short | Use |
|---|---:|---|
| Kotlin | KT | Android app |
| Swift | SWIFT | iOS app |
| Objective-C | OBJC | legacy iOS/macOS app |
| Java | JAVA | Android/JVM app |
| Dart | DART | Flutter app |
| JavaScript | JS | React Native / hybrid app |
| TypeScript | TS | typed React Native / hybrid app |
| C# | CS | Xamarin/MAUI/Unity app |
| C++ | CPP | native mobile engine/library |
| QML | QML | Qt UI app syntax |

---

# 15. Embedded / Hardware / Low-Level

| Name | Short | Use |
|---|---:|---|
| C | C | embedded/system programming |
| C++ | CPP | embedded/native engine |
| Assembly | ASM | instruction-level / hardware-close patch |
| Rust | RS | safer low-level systems |
| Zig | ZIG | modern low-level systems |
| Ada | ADA | safety-critical systems |
| Forth | FORTH | tiny embedded stack language |
| Arduino | ARDUINO | microcontroller sketch environment |
| MicroPython | MPY | Python-like microcontroller runtime |
| CircuitPython | CPY | beginner-friendly microcontroller Python |
| Verilog | VERILOG | hardware description |
| VHDL | VHDL | hardware description |
| SystemVerilog | SV | hardware verification/design |
| G-code | GCODE | CNC/3D printer machine command |

---

# 16. High Performance / Engine / Native

| Name | Short | Use |
|---|---:|---|
| C | C | low-level fast library |
| C++ | CPP | engine / performance core |
| Rust | RS | safe performance / native tool |
| Go | GO | network/server performance |
| Zig | ZIG | systems/performance build |
| D | D | native performance language |
| Fortran | FORT | scientific/high-performance legacy |
| CUDA | CUDA | NVIDIA GPU compute |
| OpenCL | OCL | cross-vendor GPU/parallel compute |
| Assembly | ASM | lowest-level optimization/patch |

---

# 17. AI / Data Science / Math

| Name | Short | Use |
|---|---:|---|
| Python | PY | AI/data tooling, notebooks, scripts |
| R | R | statistics/data analysis |
| Julia | JL | numerical/scientific computing |
| MATLAB | MATLAB | engineering/math simulation |
| SQL | SQL | data query/report |
| Scala | SCALA | big data / Spark |
| Java | JAVA | enterprise data platform |
| C++ | CPP | high-performance AI/data engine |
| CUDA | CUDA | GPU AI compute |
| OpenCL | OCL | portable GPU compute |
| SAS | SAS | enterprise statistics |
| Stata | STATA | statistical analysis |
| SPSS Syntax | SPSS | statistical package scripting |

---

# 18. Functional / Academic / Formal

| Name | Short | Use |
|---|---:|---|
| Haskell | HS | pure functional programming |
| OCaml | ML | functional/systems language |
| F# | FS | .NET functional language |
| Clojure | CLJ | Lisp on JVM |
| Erlang | ERL | actor/fault-tolerant systems |
| Elixir | EX | Erlang VM, fault-tolerant apps |
| Scheme | SCM | Lisp dialect / education |
| Common Lisp | CL | Lisp system language |
| Lean | LEAN | theorem proving / formal proof |
| Coq | COQ | proof assistant |
| Agda | AGDA | dependently typed proof language |
| Idris | IDRIS | dependently typed functional language |
| Prolog | PROLOG | logic programming |
| Datalog | DATALOG | logic query/rules |

---

# 19. Blockchain / Smart Contract

| Name | Short | Use |
|---|---:|---|
| Solidity | SOL | Ethereum smart contract |
| Vyper | VYPER | Python-like Ethereum contract |
| Move | MOVE | smart contract/resource language |
| Sway | SWAY | Fuel smart contract language |
| Tact | TACT | TON smart contract language |
| Cadence | CADENCE | Flow blockchain contract |
| Clarity | CLARITY | Stacks smart contract |
| Scilla | SCILLA | smart contract language |
| Rust | RS | Solana/Near/Substrate contracts |
| Go | GO | blockchain clients/tools |
| JavaScript | JS | blockchain scripts/tools |
| TypeScript | TS | typed blockchain tooling |

---

# 20. Graphics / Shader / GPU

| Name | Short | Use |
|---|---:|---|
| GLSL | GLSL | OpenGL/WebGL shader |
| HLSL | HLSL | DirectX shader |
| WGSL | WGSL | WebGPU shader |
| Metal Shading Language | MSL | Apple Metal shader |
| CUDA | CUDA | NVIDIA GPU compute |
| OpenCL | OCL | GPU/parallel compute |
| C++ | CPP | graphics engine |
| Processing | P5 | creative visual coding |

---

# 21. Enterprise / Legacy / Business

| Name | Short | Use |
|---|---:|---|
| COBOL | COBOL | legacy finance/business systems |
| Fortran | FORT | scientific/legacy compute |
| ABAP | ABAP | SAP business programming |
| Apex | APEX | Salesforce backend logic |
| PeopleCode | PPLCODE | PeopleSoft scripting |
| Java | JAVA | enterprise backend |
| C# | CS | Microsoft enterprise stack |
| VB.NET | VBNET | .NET legacy/business apps |
| VBA | VBA | Office automation/business tools |
| FoxPro | FOX | legacy database/business apps |
| xBase | XBASE | dBase-style database language |
| Clipper | CLIPPER | xBase compiler legacy |
| Delphi | DELPHI | Pascal-based desktop apps |
| Pascal | PAS | education/legacy language |

---

# 22. Build / Package / Project Control

| Name | Short | Use |
|---|---:|---|
| Makefile | MAKE | command/build recipes |
| CMake | CMAKE | native build generation |
| Meson | MESON | modern native build system |
| Gradle | GRADLE | JVM/Android build |
| Maven POM | POM | Java XML project build |
| Bazel | BAZEL | large build system |
| Buck | BUCK | build system |
| Nix | NIX | reproducible package/env |
| Dune | DUNE | OCaml build/project |
| Earthly | EARTHLY | container-like build pipeline |
| Justfile | JUST | task commands |
| Taskfile | TASK | task runner config |
| package.json | PKGJSON | Node project metadata/scripts |
| requirements.txt | REQ | Python dependency list |
| pyproject.toml | PYPROJ | Python project config |
| Cargo.toml | CARGO | Rust project config |
| go.mod | GOMOD | Go module config |

---

# 23. Text Processing / Pattern / Transform

| Name | Short | Use |
|---|---:|---|
| Regex | REGEX | pattern matching |
| Awk | AWK | text/table line processing |
| Sed | SED | stream text replacement |
| XPath | XPATH | XML path query |
| XSLT | XSLT | XML transform |
| Jinja | JINJA | template engine |
| Mustache | MUSTACHE | logic-light template |
| Handlebars | HBS | template engine |
| Liquid | LIQUID | template engine |
| ERB | ERB | Ruby embedded template |
| EJS | EJS | JavaScript template |

---

# 24. Rare / Specialized / Experimental

| Name | Short | Use |
|---|---:|---|
| Smalltalk | ST | object-oriented language/history |
| Prolog | PROLOG | logic/rule solving |
| Common Lisp | CL | symbolic/system programming |
| Scheme | SCM | Lisp dialect |
| Emacs Lisp | ELISP | Emacs extension language |
| Hy | HY | Lisp syntax on Python |
| Pony | PONY | actor model language |
| Hack | HACK | typed PHP-like language |
| ReasonML | REASON | OCaml-family syntax |
| ReScript | RES | OCaml-family JS compile target |
| Elm | ELM | functional frontend language |
| PureScript | PSCRIPT | Haskell-like frontend language |
| Q# | QSHARP | quantum programming |
| Ballerina | BAL | integration/service language |
| Bosque | BOSQUE | experimental language |
| Janet | JANET | embeddable Lisp-like language |
| Wren | WREN | small embeddable scripting language |
| Ink | INK | narrative scripting |
| Ren'Py | RENPY | visual novel scripting |
| Yarn Spinner | YARN | dialogue scripting |

---

# 25. Machine / Printer / Geometry / Sound

| Name | Short | Use |
|---|---:|---|
| G-code | GCODE | CNC/3D printer control |
| OpenSCAD | SCAD | parametric 3D model language |
| PostScript | PS | page description language |
| Forth | FORTH | stack language / embedded |
| Logo | LOGO | educational turtle graphics |
| APL | APL | array programming |
| J | J | array programming |
| K | K | array language |
| Q | Q | kdb+ query/array language |
| Max/MSP | MAX | visual audio/interactive programming |
| SuperCollider | SC | sound synthesis language |
| Csound | CSOUND | audio synthesis language |
| Faust | FAUST | audio DSP language |
| LabVIEW | LABVIEW | visual engineering programming |

---

# 26. Suggested Cross-L Tag Families

| Family | Meaning | Example |
|---|---|---|
| `GEN:*` | general language | `GEN:PY`, `GEN:JS` |
| `SCRIPT:*` | automation/script | `SCRIPT:BASH`, `SCRIPT:LUA` |
| `CONFIG:*` | configuration | `CONFIG:JSON`, `CONFIG:YML` |
| `DOC:*` | human-readable document | `DOC:MD`, `DOC:TXT` |
| `QUERY:*` | database/query | `QUERY:SQL`, `QUERY:GQL` |
| `LOW:*` | low-level/native | `LOW:C`, `LOW:ASM` |
| `FAST:*` | performance/engine | `FAST:CPP`, `FAST:RS` |
| `WEB:*` | web/frontend/backend | `WEB:JS`, `WEB:HTML` |
| `MOBILE:*` | mobile/app | `MOBILE:KT`, `MOBILE:SWIFT` |
| `BUILD:*` | build/project control | `BUILD:MAKE`, `BUILD:CMAKE` |
| `ENV:*` | environment/deploy | `ENV:DOCKER`, `ENV:ENV` |
| `AI:*` | AI/data/math | `AI:PY`, `AI:R` |
| `CHAIN:*` | blockchain/smart contract | `CHAIN:SOL` |
| `GPU:*` | shader/GPU | `GPU:GLSL`, `GPU:CUDA` |
| `FORMAL:*` | formal/proof/logic | `FORMAL:LEAN` |

---

# 27. Minimal Modew Selection Rule

Modew ไม่จำเป็นต้องเลือกภาษาที่ “ดีที่สุดของโลก”

Modew ควรเลือกภาษาที่ตรงกับงานที่สุดใน ENV นั้น

ตัวอย่าง:

```text
Need flow control     → Python / Bash
Need embedded rule    → Lua / JSON rule
Need speed            → C++ / Rust / C / WASM
Need config           → JSON / YAML / TOML / ENV
Need human meaning    → Markdown / TXT
Need query            → SQL / GraphQL
Need portable runtime → WASM
Need low-level patch  → Assembly / C
```

---

# 28. Final Note

ตารางนี้เป็น Tag Reference สำหรับ Cross-L / CrossLgu

ไม่ใช่กฎตายตัว

ใช้เพื่อช่วยจำ แยกประเภท สร้าง logic และเป็นฐานให้ Modew เลือกเครื่องมือให้ตรงกับงาน

```text
Language is not authority.
Language is a role inside a governed work unit.
```

END
