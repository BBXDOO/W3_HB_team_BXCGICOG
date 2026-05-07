# W3Lgu Runtime Paper

## Goal
Describe how W3Lgu packets move through runtime with low overhead and predictable state reporting.

## Runtime stages
1. receive
2. parse
3. interpret
4. route
5. execute
6. signal
7. commit memory

## ENV-aware execution
Runtime should adapt execution behavior to environment hints without changing the packet meaning.
Examples: mobile, offline, low-power, debug, batch.

```txt
TASK:sync,ENV:mobile,MODE:auto
```

Runtime action:
- keep packet shape unchanged
- reduce payload size
- prefer short signal output
- postpone non-critical secondary work

## Modew communication
Modew receives the normalized packet and returns a stateful result packet.

```txt
IN : TASK:sync,MODEW:queue,STATE:ready
OUT: TASK:sync,MODEW:queue,STATE:done,COLOR:green
```

## Condien interaction
Condien provides contextual meaning pressure such as urgency, ambiguity, or situational bias.
Runtime may use Condien to pick a safer interpretation path, but it must log the adjustment in output state.

## MPCP compatibility
W3Lgu runtime should preserve MPCP-valid states and emit them directly when possible:
- idle
- ready
- run
- WAIT
- wait
- done
- warn
- block
- fail
- STOP
- SUCCESS

## 0.5 decision layer
A decision confidence of `0.5` means the runtime should not treat the packet as failed or final truth.
Instead it should keep execution observable and request the next best resolving step.

## Pseudo-runtime example
```txt
INPUT  : TASK:route,ENV:mobile,STATE:ready
PARSE  : EVENT:parse_ok,TASK:route,ENV:mobile,STATE:ready
MODEW  : EVENT:modew.run,TASK:route,STATE:run
SIGNAL : EVENT:signal,STATE:done,COLOR:green,SYM:■
MEMORY : EVENT:commit,LAST_STATE:done
```
