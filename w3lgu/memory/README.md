# W3Lgu Memory

Purpose: retain compact execution context needed for parser recovery, signal continuity, and cross-layer communication.

## Store types
- last good packet
- active environment
- signal history
- adapter hints
- recovery notes

Memory should be small, explicit, and disposable when context closes.
