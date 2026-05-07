# W3Lgu Parser Paper

## Goal
Design a parser that is lightweight, readable, and able to recover from common human-written input defects.

## Parser objectives
- accept human-readable syntax
- produce one normalized packet shape
- recover safe formatting issues
- surface ambiguity instead of hiding it

## Parser stages
1. line read
2. token detect
3. separator normalize
4. key/value bind
5. recovery pass
6. confidence emit

## Recovery logic
Safe recovery cases:
- missing commas between obvious `KEY:VALUE` pairs
- repeated spaces
- lowercase keys that clearly map to known commands
- trailing separator at line end

Unsafe recovery cases:
- duplicated keys with conflicting values
- unclear value ownership
- symbol-only line without known context

Unsafe cases should emit a warning packet instead of silent repair.

## Parser examples
### Example 1 — separator recovery
Input:
```txt
TASK:build MODE:fast STATE:ready
```
Output:
```txt
TASK:build,MODE:fast,STATE:ready
```

### Example 2 — confidence downgrade
Input:
```txt
task:build ??? ready
```
Output:
```txt
EVENT:parse_warn,TASK:build,STATE:warn,CONF:0.5,NOTE:ambiguous_tokens
```

### Example 3 — symbolic recovery
Input:
```txt
STATE:warn ●
```
Output:
```txt
STATE:warn,COLOR:yellow,SYM:●
```

## Parser / runtime contract
The parser should not decide final truth.
Its job is to turn readable input into a packet and report how confident that transformation is.
