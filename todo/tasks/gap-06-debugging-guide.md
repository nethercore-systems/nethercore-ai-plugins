# Gap 6: Testing & Debug

**Status:** `[x]` Completed
**Priority:** MEDIUM
**Plugin:** nethercore-zx-dev
**Type:** Skill

---

## Problem

Debug FFI exists, minimal plugin guidance. ZX has a debug inspection system (F3 panel, `debug_register_*`) but no skill teaches its use.

## What's Missing

- Debug panel usage (F3, registering values, grouping)
- Sync testing for multiplayer (`--sync-test`, `--p2p-test`)
- Common debugging patterns
- Performance profiling basics

## Prompt for Implementation

```
Add skill "debugging-guide" to nethercore-zx-dev. Triggers: "debug", "F3",
"debug_register", "sync test", "desync", "profiling". Cover: F3 panel usage,
debug_register_*/debug_watch_* FFI, debug_group organization, frame stepping
(F5/F6/F7/F8), --sync-test and --p2p-test flags. Reference include/zx.rs debug
section. ~1000 words.
```

## Dependencies

- None

## Related Gaps

- Gap 20 (Multiplayer Rendering) for sync testing context
