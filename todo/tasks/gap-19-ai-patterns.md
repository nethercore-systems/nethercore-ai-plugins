# Gap 19: AI & Behavior Patterns

**Status:** `[ ]` Not Started
**Priority:** LOW
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

NOT covered. Enemy AI and NPC behavior must be implemented by games. Lower priority than physics/collision but important for games with enemies or NPCs.

## What's Missing

### State Machines
- Finite state machine pattern
- State transitions
- Entry/exit actions
- Hierarchical state machines

### Movement Behaviors
- Patrol (waypoint following)
- Chase (follow target)
- Flee (run from target)
- Wander (random movement)

### Sensing
- Line-of-sight detection
- Hearing (proximity triggers)
- Memory (last known position)

### Pathfinding (Simple)
- Grid-based A* (for tile games)
- Waypoint graphs (for 3D)
- Steering behaviors (seek, flee, arrive)

### Combat AI
- Attack patterns
- Cooldowns
- Aggression levels
- Target selection

## Prompt for Implementation

```
Add skill "ai-patterns" to nethercore-zx-game-design. Triggers: "enemy AI",
"state machine", "patrol", "pathfinding", "NPC behavior", "chase", "AI".
Cover: state machines (FSM pattern, transitions), movement (patrol, chase,
flee, wander), sensing (LOS, proximity), simple pathfinding (grid A*,
waypoints), combat AI (attack patterns, cooldowns). Rollback-safe. Include
Rust code. ~1500 words. Lower priority than physics/collision.
```

## Dependencies

- Gap 16 (Physics & Collision) for LOS raycasting

## Related Gaps

- Gap 16 (Physics) for sensing via raycasting
- Gap 18 (Gameplay Mechanics) for combat integration
