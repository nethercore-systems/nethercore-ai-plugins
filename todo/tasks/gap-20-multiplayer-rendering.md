# Gap 20: Multiplayer Rendering Patterns

**Status:** `[x]` Completed
**Priority:** HIGH (CRITICAL)
**Plugin:** nethercore-zx-game-design
**Type:** Skill
**Completed:** 2025-12-28

## Implementation Summary

Created new skill `multiplayer-rendering` in `nethercore-zx-game-design/skills/multiplayer-rendering/`:

- **SKILL.md** (~1500 words) - Core skill covering:
  - Critical update() vs render() determinism rule
  - `player_count()` and `local_player_mask()` FFI documentation
  - Pattern 1: Split-Screen (Local Multiplayer) with viewport per local player
  - Pattern 2: Same-Screen (Shared Camera) with dynamic zoom
  - Pattern 3: Asymmetric (Role-Based Views)
  - Correct input handling in update()
  - Common mistakes section with WRONG/CORRECT examples
  - Integration notes with multiplayer-design skill

- **references/viewport-layouts.md** - Complete viewport configurations for:
  - 2-player horizontal and vertical splits
  - 3-player layouts (one+two, columns)
  - 4-player quadrants
  - Dynamic layout function
  - Mixed local/remote examples
  - Aspect ratio considerations

---

---

## Problem

multiplayer-design skill covers THEORY but not IMPLEMENTATION patterns.

**Critical Issue:** The skill never mentions `player_count()` or `local_player_mask()` FFI functions, and doesn't explain how to use them without breaking determinism.

## The Determinism Rule for Multiplayer Rendering

```
update() - DETERMINISTIC
  - Called on ALL clients with SAME synchronized inputs
  - Must produce IDENTICAL results everywhere
  - OK: player_count() - same on all clients
  - OK: button_pressed(player_id, ...) - for ALL players
  - NEVER: local_player_mask() - different per client!

render() - LOCAL ONLY
  - Called only on THIS client
  - Can differ between clients (that's fine!)
  - OK: local_player_mask() - to know YOUR players
  - OK: viewport() - for split-screen rendering
```

## FFI Functions for Multiplayer

```rust
fn player_count() -> u32;           // 1-4, SAME on all clients
fn local_player_mask() -> u32;      // Bitmask, DIFFERENT per client!

// Example: 2 players, P1 local on Client A, P2 local on Client B
// Client A: player_count() = 2, local_player_mask() = 0b01 (bit 0 = P1)
// Client B: player_count() = 2, local_player_mask() = 0b10 (bit 1 = P2)
```

## Missing Multiplayer Mode Implementations

1. **Split-Screen (Local Multiplayer)** - viewport per local player
2. **Same-Screen (Shared Camera)** - camera follows center of all players
3. **Asymmetric Multiplayer** - different views for different roles
4. **Online with Rollback** - correct pattern avoiding desync

## What's Missing from Current Skill

| Topic | Status | Impact |
|-------|--------|--------|
| `player_count()` FFI | Not mentioned | Can't iterate players |
| `local_player_mask()` FFI | Not mentioned | Can't identify local players |
| update() vs render() safety | Implied but not explicit | Desync risk |
| Split-screen patterns | Not covered | Local MP broken |
| Same-screen patterns | Not covered | Shared camera missing |
| Asymmetric patterns | Not covered | Role-based games broken |
| Viewport FFI integration | Not linked to Gap 9 | No split-screen code |

## Prompt for Implementation

```
Add skill "multiplayer-rendering" to nethercore-zx-game-design OR expand
multiplayer-design skill. Triggers: "split screen", "local multiplayer",
"player_count", "local_player_mask", "multiplayer camera", "same screen
multiplayer", "asymmetric multiplayer", "couch co-op".

CRITICAL: Emphasize the update() vs render() determinism rule. local_player_mask()
is RENDER ONLY, never in update().

Cover:
1. player_count() and local_player_mask() FFI usage
2. Split-screen rendering (viewport per local player)
3. Same-screen rendering (shared camera, player indicators)
4. Asymmetric rendering (role-based views)
5. The determinism rule with code examples
6. Integration with viewport FFI

Include complete Rust code examples showing correct patterns.
~1500 words.
```

## Dependencies

- None

## Related Gaps

- Gap 9 (Split-Screen/Viewport) - viewport FFI usage
- Gap 17 (Camera Implementation) - camera code patterns
