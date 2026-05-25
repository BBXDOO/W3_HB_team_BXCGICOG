# W3Lgu Event Paper

## Goal
Describe the lifecycle of an event as it moves through parser, layers, runtime, signals, and memory.

## Event lifecycle
1. event enters from human, module, or system source
2. parser normalizes the line
3. layers apply meaning and decision confidence
4. runtime dispatches to Modew or another execution path
5. signal layer reports current state
6. memory stores the minimum needed continuity data

## Event packet shape
```txt
EVENT:<name>,TASK:<task>,STATE:<state>,ENV:<env>,CONF:<confidence>
```

## Modew communication example
```txt
EVENT:request,TASK:sync,STATE:ready
EVENT:modew.run,TASK:sync,STATE:run
EVENT:modew.done,TASK:sync,STATE:done
```

## Condien interaction example
```txt
EVENT:request,TASK:route,CONDIEN:heavy,CONF:0.5
EVENT:decision,ACTION:continue_with_watch
```

## Cross-layer execution example
```txt
EVENT:input,TASK:merge,ENV:mobile
EVENT:parse_ok,TASK:merge,ENV:mobile
EVENT:runtime_run,MODEW:merge,STATE:run
EVENT:signal,STATE:SUCCESS,COLOR:green,SYM:✓
```

## Operational rule
Events should remain compact enough to log, replay, and inspect by eye.
If an event cannot be understood by a human reviewer, the packet is too complex for W3Lgu.
