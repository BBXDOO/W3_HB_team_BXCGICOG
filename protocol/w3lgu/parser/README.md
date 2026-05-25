# W3Lgu Parser

Purpose: parse human-readable W3Lgu lines into stable runtime packets.

## Scope
- line scanning
- token split
- symbol normalization
- recovery when syntax is incomplete
- handoff to runtime and adapters

## Draft flow
1. read line
2. detect command / state / signal tokens
3. normalize into packet form
4. recover missing separators when safe
5. emit `parse_ok` or `parse_warn`

## Example
Input:
`TASK:sync MODE:fast STATE:ready`

Output packet:
`EVENT:parse_ok,TASK:sync,MODE:fast,STATE:ready`
