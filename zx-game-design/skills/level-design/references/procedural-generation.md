# Procedural Level Generation Reference

Deterministic algorithms for Nethercore ZX. All algorithms use ZX FFI random for rollback safety.

## Determinism (Critical)

```rust
seed_random(level_seed);  // At level start
let value = random();                // 0 to i32::MAX
let range = random_range(min, max);  // Inclusive
```

**Same seed = identical level for all players.**

---

## BSP Dungeon Generation

Binary Space Partitioning for room-based dungeons.

### Algorithm

1. Start with full map as root node
2. Recursively split nodes until below minimum size
3. Create room within each leaf node
4. Connect rooms with corridors

### Core Pattern

```rust
struct Rect { x: u16, y: u16, w: u16, h: u16 }

struct BSPNode {
    bounds: Rect,
    room: Option<Rect>,
    left: Option<Box<BSPNode>>,
    right: Option<Box<BSPNode>>,
}

fn split(node: &mut BSPNode, min_size: u16) -> bool {
    if node.bounds.w < min_size * 2 && node.bounds.h < min_size * 2 {
        return false;  // Too small
    }
    let split_h = if node.bounds.w > node.bounds.h * 1.25 { false }
                  else if node.bounds.h > node.bounds.w * 1.25 { true }
                  else { random() % 2 == 0 };
    // Split at random point, create left/right children
    true
}
```

### Room Creation

After splitting, create room inside each leaf:
```rust
fn create_room(node: &mut BSPNode, min: u16, max: u16) {
    let w = random_range(min as i32, node.bounds.w.min(max) as i32) as u16;
    let h = random_range(min as i32, node.bounds.h.min(max) as i32) as u16;
    let x = node.bounds.x + random_range(0, (node.bounds.w - w) as i32) as u16;
    let y = node.bounds.y + random_range(0, (node.bounds.h - h) as i32) as u16;
    node.room = Some(Rect { x, y, w, h });
}
```

### Corridor Connection

Connect sibling rooms with L-shaped corridors from center to center.

---

## Cellular Automata (Caves)

Organic cave generation.

### Algorithm

1. Fill grid randomly (~45% wall)
2. Apply smoothing rules multiple times
3. Rule: Cell becomes wall if ≥5 neighbors are walls

```rust
fn smooth_caves(map: &mut [bool], width: usize, height: usize) {
    for _ in 0..5 {  // 5 iterations
        let snapshot = map.to_vec();
        for y in 1..height-1 {
            for x in 1..width-1 {
                let walls = count_neighbors(&snapshot, x, y, width);
                map[y * width + x] = walls >= 5;
            }
        }
    }
}
```

---

## Noise-Based Terrain

For open-world heightmaps.

### Value Noise Pattern

```rust
fn value_noise(x: i32, y: i32, seed: u32) -> f32 {
    seed_random(hash(x, y, seed));
    random() as f32 / i32::MAX as f32
}

fn terrain_height(x: f32, y: f32) -> f32 {
    // Octave layering
    let n1 = noise(x * 0.1, y * 0.1) * 1.0;    // Large features
    let n2 = noise(x * 0.3, y * 0.3) * 0.5;    // Medium
    let n3 = noise(x * 0.9, y * 0.9) * 0.25;   // Detail
    n1 + n2 + n3
}
```

---

## Room Templates

Pre-designed room layouts for variety.

### Pattern

```rust
const ROOM_TEMPLATES: &[&[u8]] = &[
    // 8x6 room with pillars
    b"########\
      #......#\
      #.#..#.#\
      #.#..#.#\
      #......#\
      ########",
    // More templates...
];

fn place_template(map: &mut TileMap, template: &[u8], x: u16, y: u16) {
    // Copy template tiles into map at position
}
```

---

## Best Practices

1. **Seed consistently** — Use level number or hash of coordinates
2. **Validate connectivity** — Flood-fill to ensure all rooms reachable
3. **Cache expensive generation** — Store in rollback state only if needed
4. **Profile memory** — Large procedural maps can exceed ZX limits
