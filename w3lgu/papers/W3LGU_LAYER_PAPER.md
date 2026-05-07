# W3Lgu Layer Paper

## Goal
Map W3Lgu into explicit layers so cross-layer execution stays understandable and debuggable.

## Draft layer stack
| Layer | Role |
|---|---|
| L0 Input | receive human, module, or system events |
| L1 Parser | tokenize and normalize lines |
| L2 Meaning | apply Condien and symbolic interpretation |
| L2.5 Decision | hold the 0.5 decision layer before hard commit |
| L3 Runtime | dispatch to Modew or internal execution path |
| L4 Signal | emit readable state packets |
| L5 Memory | store compact continuity state |

## Layer law
Structure serves truth.
A layer boundary exists to make execution observable, not to add ceremony.

## Cross-layer example
```txt
L0  INPUT  : TASK:scan MODE:auto ENV:mobile
L1  PARSE  : TASK:scan,MODE:auto,ENV:mobile
L2  MEAN   : TASK:scan,MODE:auto,ENV:mobile,CONDIEN:light
L2.5 CHECK : CONF:0.5,ACTION:continue_with_watch
L3  RUN    : MODEW:scan,STATE:run
L4  SIGNAL : STATE:done,COLOR:green,SYM:■
L5  STORE  : LAST_TASK:scan,LAST_STATE:done
```

## Line C support
Line C lives across L1-L3.
It keeps enough structure for reliable execution while allowing adaptive interpretation when input is incomplete or situational.
