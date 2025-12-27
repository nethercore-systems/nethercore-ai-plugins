# Gap 7: Level Design Patterns

**Status:** `[x]` Completed
**Priority:** LOW
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

Not covered. No guidance for spatial content design beyond procedural asset generation.

## What's Missing

- Tile-based level design for 2D games
- 3D level layout principles
- Procedural level generation patterns
- Pacing and difficulty curves

## Implementation

Created `skills/level-design/` with:

- **SKILL.md** (~1,200 words) - Core level design patterns:
  - Level type overview table
  - Tile-based design (2D) with code examples
  - 3D level layout principles
  - Procedural generation basics (BSP)
  - Pacing and difficulty curves
  - ZX ROM constraints and streaming strategies

- **references/tile-map-patterns.md** - Complete implementations:
  - Full tile map with layers and rendering
  - Collision detection (point, AABB, slopes)
  - Chunk streaming for large worlds
  - Autotiling (4-bit and 8-bit)
  - RLE compression
  - Editor integration (Tiled format)

- **references/procedural-generation.md** - Generation algorithms:
  - Complete BSP dungeon generation
  - Cellular automata caves with connectivity
  - Room templates
  - Noise-based terrain (value noise, fractal)
  - Pacing integration (spawn difficulty by distance)
  - Complete generation pipeline

All code uses ZX FFI random functions for rollback safety.

## Dependencies

- None

## Related Gaps

- Gap 24 (2D Sprites) covers *tileset creation*; this covers *design patterns*
