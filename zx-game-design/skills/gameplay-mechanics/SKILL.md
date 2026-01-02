---
name: Gameplay Mechanics Library
description: |
  Use this skill for ZX gameplay patterns: "platformer", "variable jump", "coyote time", "wall jump", "hitbox", "combat", "i-frames", "knockback", "combo", "inventory", "dialogue", "typewriter", "dash", "dodge".

  **Load references when:**
  - Platformer physics, wall jump, moving platforms → `references/platformer-mechanics.md`
  - Combat, combos, attack state machines → `references/combat-mechanics.md`
  - 8-dir movement, acceleration, dash → `references/movement-patterns.md`
  - Items, equipment, stackable inventory → `references/inventory-systems.md`
  - Text boxes, choices, branching dialogue → `references/dialogue-systems.md`

  For CONCEPTUAL game mechanics design (without code): use game-design:core-loop-design instead.
version: 0.2.0
---

# Gameplay Mechanics Library

Tested, rollback-safe implementations for Nethercore ZX. All patterns use deterministic logic compatible with GGRS rollback netcode.

## Rollback Safety (Critical)

All gameplay code MUST be deterministic:

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Time | `delta_time()`, `tick_count()` | System clock, `std::time` |
| Random | `random()`, `random_range()` | `rand()`, external RNG |
| Input | `button_pressed()`, `button_held()` | OS input events |
| State | Fixed-point or consistent floats | Platform-dependent floats |

---

## Platformer Mechanics (Quick Reference)

### Variable-Height Jump
Hold button longer = higher jump. On release while rising, multiply velocity by cut factor (0.5).

### Coyote Time
Grace period (~6 frames) allowing jumps after leaving platform. Track `coyote_timer`, decrement each frame when not grounded.

### Jump Buffering
Queue jump input (~8 frames) before landing. Track `jump_buffer`, execute on ground contact.

**Full implementations**: See **`references/platformer-mechanics.md`**.

---

## Combat Mechanics (Quick Reference)

### Hitbox/Hurtbox System
Separate collision volumes for attacks (hitbox) and vulnerability (hurtbox). Check AABB overlap only when attack is active.

### Invincibility Frames
~45 frames of invulnerability after taking damage. Track `iframes` counter, decrement each frame.

### Knockback + Hitstun
Push entities backward, freeze input for duration proportional to knockback strength.

**Full implementations**: See **`references/combat-mechanics.md`**.

---

## Movement Patterns (Quick Reference)

### 8-Directional (Top-Down)
Read 4 directional inputs, normalize diagonal movement to prevent faster diagonal speed.

### Acceleration Model
Apply acceleration toward input direction, apply friction when no input. Clamp to max speed.

### Dash Mechanic
Burst of speed (~8 frames), cooldown (~30 frames). Lock direction at activation.

**Full implementations**: See **`references/movement-patterns.md`**.

---

## Items and Inventory (Quick Reference)

### Simple Pickup
Check distance to item, deactivate on collection.

### Fixed-Slot Inventory
Array of item IDs, use sentinel value (0xFF) for empty slots.

**Full implementations**: See **`references/inventory-systems.md`**.

---

## Dialogue and Text (Quick Reference)

### Typewriter Effect
Track `chars_shown`, increment each frame. Speed up when button held.

### Choice Selection
Navigate with D-pad, confirm with A. Track `selected` index.

**Full implementations**: See **`references/dialogue-systems.md`**.

---

## Related Skills

- **`multiplayer-patterns`** — Rollback safety and determinism patterns
- **`physics-collision`** — Underlying collision detection
- **`game-design:core-loop-design`** — Conceptual mechanics design
