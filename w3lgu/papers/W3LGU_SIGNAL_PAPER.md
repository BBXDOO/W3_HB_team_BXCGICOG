# W3Lgu Signal Paper

## Goal
Standardize the signal layer for state communication, color mapping, and readable output.

## Signal model
A signal packet should answer four questions:
- what happened
- what state is active
- how urgent it is
- whether action should continue, pause, or stop

## Color / state mapping
| State | Color | Symbol | Meaning |
|---|---|---|---|
| idle | gray | · | standing by |
| ready | blue | ◆ | prepared / external handoff possible |
| run | blue | ⟳ | active execution |
| WAIT / wait | yellow | ◌ | pending dependency |
| done | green | ■ | completed |
| warn | yellow | ● | caution / review |
| block | orange | ■! | blocked by rule or dependency |
| fail | red | ▲ | failed |
| STOP | red | ⛔ | hard stop |
| SUCCESS | green | ✓ | confirmed success |

## 0.5 decision layer mapping
`CONF:0.5` means uncertainty is active.
It should usually pair with `STATE:warn` or `STATE:wait`, not with `SUCCESS`.

Example:
```txt
EVENT:signal,STATE:warn,CONF:0.5,COLOR:yellow,SYM:●
```

## Mobile-first rule
Signals should stay short enough for mobile views.
Preferred order:
`STATE -> COLOR -> SYM -> CONF -> NOTE`

## Cross-layer contract
Signals are not only UI output.
They are the shared state communication layer between parser, runtime, Modew, Condien, and external observers.
