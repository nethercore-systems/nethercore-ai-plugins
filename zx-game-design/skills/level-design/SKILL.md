---
name: Level Design Patterns for ZX
description: |
  Use this skill for ZX-SPECIFIC level implementation - data formats, storage, and generation. Trigger phrases: "tile map", "level data format", "procedural level generation", "room templates", "dungeon generator code", "level chunks", "tileset organization", "level streaming".

  This skill provides ZX IMPLEMENTATION - tile storage, ROM constraints, generation algorithms, tileset patterns.

  For CONCEPTUAL DESIGN (flow, pacing, challenge curves): use game-design:level-design instead.
version: 0.1.1
---

# Level Design Patterns

Spatial content design patterns for Nethercore ZX games. Covers tile-based 2D layouts, 3D level flow, procedural generation, and pacing—all within ZX ROM constraints.

## Level Type Overview

| Level Type | Perspective | Storage | Generation |
|------------|-------------|---------|------------|
| Tile Map | 2D/Top-Down | Grid arrays | Hand-crafted or procedural |
| Room-Based | Any | Room + connection data | BSP, graph-based |
| Open World | 3D | Chunked sectors | Streaming, LOD |
| Linear | Any | Sequential segments | Hand-crafted |

---

## Tile-Based Design (2D)

Grid-based levels using tile indices. Efficient storage and collision.

### Tile Map Structure

```rust
const TILE_SIZE: u32 = 16;
const MAP_WIDTH: usize = 64;
const MAP_HEIGHT: usize = 48;

struct TileMap {
    tiles: [u8; MAP_WIDTH * MAP_HEIGHT],  // Tile indices
    collision: [u8; MAP_WIDTH * MAP_HEIGHT],  // Collision flags
}

impl TileMap {
    fn get_tile(&self, x: usize, y: usize) -> u8 {
        if x < MAP_WIDTH && y < MAP_HEIGHT {
            self.tiles[y * MAP_WIDTH + x]
        } else {
            0  // Out of bounds = empty
        }
    }

    fn is_solid(&self, x: usize, y: usize) -> bool {
        if x < MAP_WIDTH && y < MAP_HEIGHT {
            self.collision[y * MAP_WIDTH + x] != 0
        } else {
            true  // Out of bounds = solid
        }
    }

    fn world_to_tile(&self, world_x: f32, world_y: f32) -> (usize, usize) {
        ((world_x / TILE_SIZE as f32) as usize,
         (world_y / TILE_SIZE as f32) as usize)
    }
}
```

### Collision Layers

Use bitflags for multi-layer collision:

```rust
const COLLISION_NONE: u8 = 0b0000_0000;
const COLLISION_SOLID: u8 = 0b0000_0001;
const COLLISION_PLATFORM: u8 = 0b0000_0010;  // One-way
const COLLISION_HAZARD: u8 = 0b0000_0100;
const COLLISION_WATER: u8 = 0b0000_1000;
const COLLISION_LADDER: u8 = 0b0001_0000;

fn check_collision(flags: u8, mask: u8) -> bool {
    (flags & mask) != 0
}
```

### Tile Types (Platformer)

| Category | Tiles | Purpose |
|----------|-------|---------|
| Terrain | Ground, walls, slopes | Core geometry |
| Platforms | Solid, one-way, moving | Traversal |
| Hazards | Spikes, lava, pits | Obstacles |
| Interactables | Doors, switches, chests | Progression |
| Decorative | Background, foreground | Visual only |

See **`references/tile-map-patterns.md`** for chunk streaming and large map handling.

---

## 3D Level Layout

Spatial flow principles for third-person and first-person games.

### Layout Principles

**Landmarks**: Place distinct visual features for orientation. Players navigate by memorable geometry, not minimaps.

**Sight Lines**: Control what players see. Long sight lines build anticipation; blocked views create surprise.

**Verticality**: Use height changes for:
- Pacing variation (climb = slow, drop = fast)
- Combat advantage (high ground)
- Exploration reward (hidden areas above/below)

**Flow Loops**: Design levels as interconnected loops, not dead-ends. Players should return to familiar areas with new access.

### Critical Path vs Exploration

```
Level Structure:
├── Critical Path (required)
│   ├── Clear signposting
│   ├── Moderate challenge
│   └── Story beats
└── Optional Areas (reward exploration)
    ├── Collectibles
    ├── Shortcuts
    └── Harder challenges
```

### Space Budgeting

| Area Type | Size (units) | Purpose |
|-----------|--------------|---------|
| Combat Arena | 30×30 minimum | Room to maneuver |
| Corridor | 4-6 wide | Transition, tension |
| Hub Room | 50×50+ | Orientation, choices |
| Boss Arena | 60×60+ | Epic encounters |

---

## Procedural Generation

Deterministic algorithms for rollback-safe level creation.

### Room-Based Generation (BSP)

Binary Space Partitioning creates dungeon-like layouts:

```rust
struct Room {
    x: u16, y: u16,
    width: u16, height: u16,
}

struct Dungeon {
    rooms: Vec<Room>,
    corridors: Vec<(usize, usize)>,  // Room index pairs
}

fn generate_dungeon(seed: u32, width: u16, height: u16,
                    min_room: u16, max_room: u16) -> Dungeon {
    // Seed the deterministic RNG
    seed_random(seed);

    let mut rooms = Vec::new();
    let mut areas = vec![(0u16, 0u16, width, height)];

    // Recursively split areas
    while let Some((x, y, w, h)) = areas.pop() {
        if w < min_room * 2 || h < min_room * 2 {
            // Area too small to split, create room
            let room_w = random_range(min_room as i32, w.min(max_room) as i32) as u16;
            let room_h = random_range(min_room as i32, h.min(max_room) as i32) as u16;
            let room_x = x + random_range(0, (w - room_w) as i32) as u16;
            let room_y = y + random_range(0, (h - room_h) as i32) as u16;
            rooms.push(Room { x: room_x, y: room_y, width: room_w, height: room_h });
        } else {
            // Split horizontally or vertically
            if random() % 2 == 0 && w > min_room * 2 {
                let split = random_range(min_room as i32, (w - min_room) as i32) as u16;
                areas.push((x, y, split, h));
                areas.push((x + split, y, w - split, h));
            } else if h > min_room * 2 {
                let split = random_range(min_room as i32, (h - min_room) as i32) as u16;
                areas.push((x, y, w, split));
                areas.push((x, y + split, w, h - split));
            }
        }
    }

    // Connect adjacent rooms with corridors
    let corridors = connect_rooms(&rooms);

    Dungeon { rooms, corridors }
}
```

### Determinism Requirements

All procedural generation MUST use ZX FFI random functions:

| Use | Correct | Incorrect |
|-----|---------|-----------|
| Seed | `seed_random(seed)` | `srand()`, system time |
| Values | `random()`, `random_range()` | `rand()`, external RNG |

Same seed = identical level across all clients (rollback-safe).

See **`references/procedural-generation.md`** for noise-based terrain and room templates.

---

## Pacing and Difficulty

Control player experience through intentional rhythm.

### Difficulty Curve Patterns

| Pattern | Shape | Use Case |
|---------|-------|----------|
| Linear | `/` | Tutorial → mastery |
| Sawtooth | `/\/\/\` | Tension/release cycles |
| Plateau | `_/‾‾‾` | Skill gates then mastery zone |
| Inverse | `\` | Power fantasy, late-game ease |

### Intensity Graph

Map sections by intensity (0-10):

```
Level Flow:
Start [2] → Combat [6] → Puzzle [3] → Miniboss [8] → Rest [2] → Boss [10]

Visualized:
10 |                                              ████
 8 |              ████                            ████
 6 |    ████      ████                            ████
 4 |    ████      ████      ████                  ████
 2 | ████████     ████      ████████    ████████  ████
   └──────────────────────────────────────────────────
     Start    Combat   Puzzle   Mini   Rest    Boss
```

### Checkpoint Placement

- Every 30-60 seconds of gameplay
- Before difficulty spikes (not after)
- After learning new mechanics
- Never mid-combat or mid-puzzle

---

## ZX Constraints

ROM budget considerations for level data.

### Storage Estimates

| Data Type | Size | Notes |
|-----------|------|-------|
| Tile index | 1 byte | 256 tile types |
| 64×48 map | 3 KB | Single screen |
| 256×256 map | 64 KB | Large area |
| Room template | 200-500 bytes | Procedural building block |
| Collision layer | Same as tile layer | Can compress with RLE |

### Streaming Strategy

For large worlds, stream chunks:

```rust
const CHUNK_SIZE: usize = 32;  // 32×32 tiles per chunk
const LOADED_RADIUS: usize = 2;  // Load chunks within 2 of player

struct WorldStreamer {
    loaded_chunks: HashMap<(i32, i32), Chunk>,
    player_chunk: (i32, i32),
}

fn update_streaming(streamer: &mut WorldStreamer, player_x: f32, player_y: f32) {
    let new_chunk = (
        (player_x / (CHUNK_SIZE * TILE_SIZE) as f32) as i32,
        (player_y / (CHUNK_SIZE * TILE_SIZE) as f32) as i32,
    );

    if new_chunk != streamer.player_chunk {
        // Unload distant chunks, load nearby chunks
        // Keep within ROM streaming budget
    }
}
```

### Compression Tips

- Use RLE for repetitive tile runs
- Store room templates, instantiate at runtime
- Procedural generation trades CPU for storage

---

## Additional Resources

### Reference Files

- **`references/tile-map-patterns.md`** — Complete tile systems, chunk loading, editor integration
- **`references/procedural-generation.md`** — BSP, cellular automata, wave function collapse basics

### Related Skills

- **`gameplay-mechanics`** — Player movement and interaction patterns
- **`physics-collision`** — Collision detection for level geometry

### Conceptual Design

For flow, pacing, and challenge curves (without code): use **`game-design:level-design`**.
