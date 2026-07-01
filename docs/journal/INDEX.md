# Journal Index

Historical record of work completed on this project. Newest first.

## 2026

- [2026-06-30 — GameCopyRepository mutating methods return the updated object](2026-06-30-repository-methods-return-updated-objects.md) — `set_status` and `create` now return the persisted `GameCopy` instead of `None`; convention to apply across the repository layer.
- [2026-06-30 — GameCopyRepository.set_status (renamed from flag_maintenance)](2026-06-30-game-copy-set-status.md) — General status+notes setter for game copies, TDD'd; uncovered an `all()` ordering fragility (no `ORDER BY`).
