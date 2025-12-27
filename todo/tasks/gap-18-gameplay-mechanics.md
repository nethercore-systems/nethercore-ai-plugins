# Gap 18: Gameplay Mechanics Library

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

NOT covered. Common gameplay patterns must be implemented but aren't taught. Every game type has common mechanics that every developer reimplements. This skill would provide tested, rollback-safe implementations.

## What's Missing

### Platformer Mechanics
- Variable-height jumping (hold to jump higher)
- Coyote time (grace period after leaving edge)
- Jump buffering (press before landing)
- Wall sliding / wall jumping
- Moving platforms
- One-way platforms

### Combat Mechanics
- Hitbox/hurtbox systems
- Damage calculation
- Knockback/hitstun
- Invincibility frames (i-frames)
- Combo systems

### Movement Mechanics
- 8-directional movement (top-down)
- Tank controls
- Acceleration/deceleration curves
- Dash/dodge mechanics

### Inventory & Items
- Item pickup/drop
- Inventory slots
- Equipment system
- Consumables

### Dialogue & Text
- Text box rendering
- Typewriter effect
- Choice selection
- Branching dialogue state

## Prompt for Implementation

```
Add skill "gameplay-mechanics" to nethercore-zx-game-design. Triggers: "platformer
physics", "jump", "coyote time", "hitbox", "combat", "inventory", "dialogue",
"movement", "knockback". Cover: platformer (variable jump, coyote, buffer, wall
jump), combat (hitbox/hurtbox, damage, knockback, i-frames), movement (8-dir,
acceleration), items (pickup, inventory). Focus on rollback-safe patterns. Include
Rust code. ~2000 words.
```

## Dependencies

- Gap 16 (Physics & Collision) for underlying collision

## Related Gaps

- Gap 16 (Physics) for collision foundation
- Gap 19 (AI Patterns) for enemy behavior
