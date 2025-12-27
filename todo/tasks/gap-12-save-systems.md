# Gap 12: Save Data Patterns

**Status:** `[x]` Completed
**Priority:** MEDIUM
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

FFI exists for save/load, NO design patterns documented. Games need save systems, but the plugins don't cover save data architecture.

## FFI Functions (from zx.rs)

```rust
/// Saves data to a slot.
/// - slot: Save slot (0-7, 8 slots available)
/// - data_ptr: Pointer to data in WASM memory
/// - data_len: Length of data in bytes (max 64KB)
/// Returns: 0 on success, 1 if invalid slot, 2 if data too large
pub fn save(slot: u32, data_ptr: *const u8, data_len: u32) -> u32;

/// Loads data from a slot.
/// - slot: Save slot (0-7)
/// - data_ptr: Pointer to buffer in WASM memory
/// - max_len: Maximum bytes to read
/// Returns: Bytes read (0 if empty or error)
pub fn load(slot: u32, data_ptr: *mut u8, max_len: u32) -> u32;

/// Deletes a save slot.
/// Returns: 0 on success, 1 if invalid slot
pub fn delete(slot: u32) -> u32;
```

**Note:** There is NO `save_exists()` function. To check if a save exists, call `load()` with a small buffer and check if the return value is > 0.

## What's Missing

- Save data structure design (what to save)
- Serialization patterns (binary format, versioning)
- Multiple save slots UX (8 slots available: 0-7)
- Auto-save timing (when is it safe to save?)
- Save corruption prevention
- Rollback-safe save design (don't save during update())
- Checking if save exists (load returns 0 for empty slots)

## Prompt for Implementation

```
Add skill "save-systems" to nethercore-zx-game-design. Triggers: "save game", "save
data", "load game", "save slot", "persistent storage", "game progress". Cover: what
to save (progress, settings, high scores), save data structure design, binary
serialization (bytemuck), version migration, 8 save slots (0-7) with 64KB limit,
checking if save exists (load returns 0), error handling (save returns error codes),
auto-save patterns, rollback safety (save only in render or between frames). ~1000
words.
```

## Dependencies

- None

## Related Gaps

- Gap 20 (Multiplayer Rendering) for rollback safety rules
