# W3Lgu Grammar Paper

## Goal
Define a symbolic grammar that stays human-readable first, but can still be parsed into reliable machine packets.

## Grammar principles
- one line should represent one actionable unit
- keys stay uppercase when they control execution
- values stay compact and readable
- symbols may add meaning, but must not hide state
- missing punctuation may be repaired only when meaning is obvious

## Draft grammar
```ebnf
line        = pair , { separator , pair } ;
pair        = key , ":" , value ;
key         = UPPER , { UPPER | "_" | DIGIT } ;
value       = token , { sub_separator , token } ;
separator   = "," | SPACE ;
sub_separator = "/" | "'" | "-" ;
token       = letter | digit | symbol ;
```

## Symbolic execution notes
Symbols can carry compact intent:
- `■` stable result
- `●` uncertain / watch
- `▲` critical / force
- `◆` external / bridge

## Grammar examples
```txt
TASK:build,MODE:fast,STATE:ready
EVENT:signal,STATE:warn,COLOR:yellow,SYM:●
MODEW:dispatch,CONDIEN:shift,ENV:mobile
```

## Human-readable priority
A line should still be understandable without reading a schema file.
If grammar complexity harms readability, W3Lgu should choose the simpler form.

## Line C grammar rule
Line C support means grammar can accept compact flexible separators, but final normalized output must still be explicit:

Input:
```txt
TASK:build MODE:fast STATE:ready
```

Normalized:
```txt
TASK:build,MODE:fast,STATE:ready
```
