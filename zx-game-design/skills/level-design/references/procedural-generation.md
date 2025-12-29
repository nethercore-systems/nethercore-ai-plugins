# Procedural Level Generation Reference

Deterministic level generation algorithms for Nethercore ZX. All algorithms use ZX FFI random functions for rollback safety.

## Determinism Requirements

All procedural generation MUST be deterministic:

```rust
// At game start or level load
seed_random(level_seed);  // ZX FFI function

// All random calls after this produce same sequence
let value = random();                    // 0 to i32::MAX
let range = random_range(min, max);      // Inclusive range
```

**Same seed = identical level for all players in netplay.**

---

## BSP Dungeon Generation

Binary Space Partitioning for room-based dungeons.

### Complete BSP Implementation

```rust
use crate::ffi::*;

const MIN_ROOM_SIZE: u16 = 6;
const MAX_ROOM_SIZE: u16 = 15;
const MIN_LEAF_SIZE: u16 = MIN_ROOM_SIZE + 2;

struct Rect {
    x: u16, y: u16,
    w: u16, h: u16,
}

impl Rect {
    fn center(&self) -> (u16, u16) {
        (self.x + self.w / 2, self.y + self.h / 2)
    }
}

struct BSPNode {
    bounds: Rect,
    room: Option<Rect>,
    left: Option<Box<BSPNode>>,
    right: Option<Box<BSPNode>>,
}

impl BSPNode {
    fn new(bounds: Rect) -> Self {
        Self {
            bounds,
            room: None,
            left: None,
            right: None,
        }
    }

    fn split(&mut self) -> bool {
        // Already split
        if self.left.is_some() || self.right.is_some() {
            return false;
        }

        // Determine split direction
        let split_h = if self.bounds.w > self.bounds.h && self.bounds.w / self.bounds.h >= 1.25 {
            false  // Wide: split vertically
        } else if self.bounds.h > self.bounds.w && self.bounds.h / self.bounds.w >= 1.25 {
            true   // Tall: split horizontally
        } else {
            random() % 2 == 0  // Square: random
        };

        let max = if split_h { self.bounds.h } else { self.bounds.w };

        // Too small to split
        if max < MIN_LEAF_SIZE * 2 {
            return false;
        }

        // Random split point
        let split = random_range(
            MIN_LEAF_SIZE as i32,
            (max - MIN_LEAF_SIZE) as i32
        ) as u16;

        if split_h {
            // Horizontal split
            self.left = Some(Box::new(BSPNode::new(Rect {
                x: self.bounds.x,
                y: self.bounds.y,
                w: self.bounds.w,
                h: split,
            })));
            self.right = Some(Box::new(BSPNode::new(Rect {
                x: self.bounds.x,
                y: self.bounds.y + split,
                w: self.bounds.w,
                h: self.bounds.h - split,
            })));
        } else {
            // Vertical split
            self.left = Some(Box::new(BSPNode::new(Rect {
                x: self.bounds.x,
                y: self.bounds.y,
                w: split,
                h: self.bounds.h,
            })));
            self.right = Some(Box::new(BSPNode::new(Rect {
                x: self.bounds.x + split,
                y: self.bounds.y,
                w: self.bounds.w - split,
                h: self.bounds.h,
            })));
        }

        true
    }

    fn create_rooms(&mut self) {
        if let (Some(left), Some(right)) = (&mut self.left, &mut self.right) {
            left.create_rooms();
            right.create_rooms();
        } else {
            // Leaf node: create room
            let room_w = random_range(MIN_ROOM_SIZE as i32, self.bounds.w.min(MAX_ROOM_SIZE) as i32) as u16;
            let room_h = random_range(MIN_ROOM_SIZE as i32, self.bounds.h.min(MAX_ROOM_SIZE) as i32) as u16;
            let room_x = self.bounds.x + random_range(1, (self.bounds.w - room_w) as i32) as u16;
            let room_y = self.bounds.y + random_range(1, (self.bounds.h - room_h) as i32) as u16;

            self.room = Some(Rect {
                x: room_x,
                y: room_y,
                w: room_w,
                h: room_h,
            });
        }
    }

    fn get_room(&self) -> Option<&Rect> {
        if let Some(ref room) = self.room {
            return Some(room);
        }
        // Get room from children
        if let Some(ref left) = self.left {
            if let Some(room) = left.get_room() {
                return Some(room);
            }
        }
        if let Some(ref right) = self.right {
            return right.get_room();
        }
        None
    }
}

fn generate_bsp_dungeon(seed: u32, width: u16, height: u16, iterations: u32) -> Vec<u8> {
    seed_random(seed);

    let mut root = BSPNode::new(Rect { x: 0, y: 0, w: width, h: height });

    // Split tree
    let mut nodes = vec![&mut root as *mut BSPNode];
    for _ in 0..iterations {
        let mut new_nodes = Vec::new();
        for node_ptr in &nodes {
            let node = unsafe { &mut **node_ptr };
            if node.split() {
                if let Some(ref mut left) = node.left {
                    new_nodes.push(left.as_mut() as *mut BSPNode);
                }
                if let Some(ref mut right) = node.right {
                    new_nodes.push(right.as_mut() as *mut BSPNode);
                }
            }
        }
        if new_nodes.is_empty() { break; }
        nodes = new_nodes;
    }

    // Create rooms in leaves
    root.create_rooms();

    // Render to tile grid
    let mut tiles = vec![1u8; (width * height) as usize];  // 1 = wall

    render_bsp_node(&root, &mut tiles, width);
    connect_bsp_rooms(&root, &mut tiles, width);

    tiles
}

fn render_bsp_node(node: &BSPNode, tiles: &mut [u8], map_width: u16) {
    if let Some(ref room) = node.room {
        // Carve out room (0 = floor)
        for y in room.y..(room.y + room.h) {
            for x in room.x..(room.x + room.w) {
                tiles[(y as usize) * (map_width as usize) + (x as usize)] = 0;
            }
        }
    }
    if let Some(ref left) = node.left {
        render_bsp_node(left, tiles, map_width);
    }
    if let Some(ref right) = node.right {
        render_bsp_node(right, tiles, map_width);
    }
}

fn connect_bsp_rooms(node: &BSPNode, tiles: &mut [u8], map_width: u16) {
    if let (Some(ref left), Some(ref right)) = (&node.left, &node.right) {
        // Connect children first
        connect_bsp_rooms(left, tiles, map_width);
        connect_bsp_rooms(right, tiles, map_width);

        // Connect left and right rooms with corridor
        if let (Some(left_room), Some(right_room)) = (left.get_room(), right.get_room()) {
            let (lx, ly) = left_room.center();
            let (rx, ry) = right_room.center();
            create_corridor(tiles, map_width, lx, ly, rx, ry);
        }
    }
}

fn create_corridor(tiles: &mut [u8], map_width: u16, x1: u16, y1: u16, x2: u16, y2: u16) {
    let mut x = x1;
    let mut y = y1;

    // L-shaped corridor
    while x != x2 {
        tiles[(y as usize) * (map_width as usize) + (x as usize)] = 0;
        x = if x < x2 { x + 1 } else { x - 1 };
    }
    while y != y2 {
        tiles[(y as usize) * (map_width as usize) + (x as usize)] = 0;
        y = if y < y2 { y + 1 } else { y - 1 };
    }
}
```

---

## Cellular Automata Caves

Organic cave-like structures.

```rust
fn generate_caves(seed: u32, width: usize, height: usize, fill_percent: u32,
                  iterations: u32) -> Vec<u8> {
    seed_random(seed);

    let mut tiles = vec![0u8; width * height];

    // Initial random fill
    for i in 0..tiles.len() {
        tiles[i] = if (random() as u32 % 100) < fill_percent { 1 } else { 0 };
    }

    // Border walls
    for x in 0..width {
        tiles[x] = 1;
        tiles[(height - 1) * width + x] = 1;
    }
    for y in 0..height {
        tiles[y * width] = 1;
        tiles[y * width + width - 1] = 1;
    }

    // Cellular automata smoothing
    for _ in 0..iterations {
        let mut new_tiles = tiles.clone();

        for y in 1..height - 1 {
            for x in 1..width - 1 {
                let neighbors = count_neighbors(&tiles, width, x, y);

                // 4-5 rule: become wall if >=5 neighbors are walls
                new_tiles[y * width + x] = if neighbors >= 5 { 1 } else { 0 };
            }
        }

        tiles = new_tiles;
    }

    tiles
}

fn count_neighbors(tiles: &[u8], width: usize, x: usize, y: usize) -> u8 {
    let mut count = 0;
    for dy in -1i32..=1 {
        for dx in -1i32..=1 {
            if dx == 0 && dy == 0 { continue; }
            let nx = (x as i32 + dx) as usize;
            let ny = (y as i32 + dy) as usize;
            if tiles[ny * width + nx] == 1 {
                count += 1;
            }
        }
    }
    count
}
```

### Flood Fill for Connectivity

Ensure all floor areas are connected:

```rust
fn ensure_connected(tiles: &mut [u8], width: usize, height: usize) {
    // Find all regions
    let mut visited = vec![false; tiles.len()];
    let mut regions: Vec<Vec<usize>> = Vec::new();

    for i in 0..tiles.len() {
        if tiles[i] == 0 && !visited[i] {
            let region = flood_fill(tiles, &mut visited, width, height, i);
            regions.push(region);
        }
    }

    if regions.len() <= 1 { return; }

    // Keep largest, connect others or fill them
    regions.sort_by(|a, b| b.len().cmp(&a.len()));

    let main_region = &regions[0];

    for region in regions.iter().skip(1) {
        if region.len() < 10 {
            // Too small, fill it
            for &idx in region {
                tiles[idx] = 1;
            }
        } else {
            // Connect to main region
            let (from_idx, to_idx) = find_closest_points(tiles, width, region, main_region);
            carve_tunnel(tiles, width, from_idx, to_idx);
        }
    }
}

fn flood_fill(tiles: &[u8], visited: &mut [bool], width: usize, height: usize,
              start: usize) -> Vec<usize> {
    let mut region = Vec::new();
    let mut stack = vec![start];

    while let Some(idx) = stack.pop() {
        if visited[idx] || tiles[idx] != 0 { continue; }
        visited[idx] = true;
        region.push(idx);

        let x = idx % width;
        let y = idx / width;

        if x > 0 { stack.push(idx - 1); }
        if x < width - 1 { stack.push(idx + 1); }
        if y > 0 { stack.push(idx - width); }
        if y < height - 1 { stack.push(idx + width); }
    }

    region
}
```

---

## Room Templates

Pre-designed rooms for variety.

```rust
const TEMPLATE_EMPTY: &[&[u8]] = &[
    b"........",
    b"........",
    b"........",
    b"........",
];

const TEMPLATE_PILLARS: &[&[u8]] = &[
    b".#..#...",
    b"........",
    b"...#..#.",
    b"........",
];

const TEMPLATE_CENTER: &[&[u8]] = &[
    b"........",
    b"..####..",
    b"..####..",
    b"........",
];

const TEMPLATES: &[&[&[u8]]] = &[
    TEMPLATE_EMPTY,
    TEMPLATE_PILLARS,
    TEMPLATE_CENTER,
];

fn apply_template(tiles: &mut [u8], map_width: usize, room: &Rect) {
    let template_idx = (random() as usize) % TEMPLATES.len();
    let template = TEMPLATES[template_idx];

    let template_h = template.len();
    let template_w = template[0].len();

    for ty in 0..room.h as usize {
        for tx in 0..room.w as usize {
            // Sample template with wrapping
            let src_y = ty % template_h;
            let src_x = tx % template_w;
            let tile = if template[src_y][src_x] == b'#' { 1 } else { 0 };

            let dst_x = room.x as usize + tx;
            let dst_y = room.y as usize + ty;
            tiles[dst_y * map_width + dst_x] = tile;
        }
    }
}
```

---

## Noise-Based Terrain

Height-map terrain using noise.

### Simple Value Noise

```rust
/// Simple hash for noise
fn hash(x: i32, y: i32, seed: u32) -> f32 {
    let n = x.wrapping_mul(374761393)
        .wrapping_add(y.wrapping_mul(668265263))
        .wrapping_add(seed as i32);
    let n = (n ^ (n >> 13)).wrapping_mul(1274126177);
    let n = n ^ (n >> 16);
    (n as u32 as f32) / (u32::MAX as f32)
}

/// Linear interpolation
fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + t * (b - a)
}

/// Smooth step for better interpolation
fn smoothstep(t: f32) -> f32 {
    t * t * (3.0 - 2.0 * t)
}

/// Value noise at point
fn value_noise(x: f32, y: f32, seed: u32) -> f32 {
    let x0 = x.floor() as i32;
    let y0 = y.floor() as i32;
    let x1 = x0 + 1;
    let y1 = y0 + 1;

    let sx = smoothstep(x - x0 as f32);
    let sy = smoothstep(y - y0 as f32);

    let n00 = hash(x0, y0, seed);
    let n10 = hash(x1, y0, seed);
    let n01 = hash(x0, y1, seed);
    let n11 = hash(x1, y1, seed);

    let nx0 = lerp(n00, n10, sx);
    let nx1 = lerp(n01, n11, sx);

    lerp(nx0, nx1, sy)
}

/// Fractal noise (multiple octaves)
fn fractal_noise(x: f32, y: f32, seed: u32, octaves: u32, persistence: f32) -> f32 {
    let mut total = 0.0;
    let mut amplitude = 1.0;
    let mut frequency = 1.0;
    let mut max_value = 0.0;

    for i in 0..octaves {
        total += value_noise(x * frequency, y * frequency, seed + i) * amplitude;
        max_value += amplitude;
        amplitude *= persistence;
        frequency *= 2.0;
    }

    total / max_value
}
```

### Height Map to Tiles

```rust
fn generate_terrain(seed: u32, width: usize, height: usize) -> Vec<u8> {
    let mut tiles = vec![0u8; width * height];

    for y in 0..height {
        for x in 0..width {
            let nx = x as f32 / 10.0;
            let ny = y as f32 / 10.0;

            let height_value = fractal_noise(nx, ny, seed, 4, 0.5);

            // Threshold to tile types
            tiles[y * width + x] = if height_value < 0.3 {
                0  // Water
            } else if height_value < 0.5 {
                1  // Sand
            } else if height_value < 0.7 {
                2  // Grass
            } else {
                3  // Stone
            };
        }
    }

    tiles
}
```

---

## Pacing Integration

Place difficulty elements based on distance from start.

```rust
struct SpawnPoint {
    x: u16,
    y: u16,
    difficulty: u8,  // 0-10
}

fn generate_spawn_points(tiles: &[u8], width: usize, start_x: u16, start_y: u16) -> Vec<SpawnPoint> {
    let mut spawns = Vec::new();
    let mut distance_map = vec![u16::MAX; tiles.len()];

    // BFS to calculate distance from start
    let start_idx = start_y as usize * width + start_x as usize;
    distance_map[start_idx] = 0;

    let mut queue = vec![start_idx];
    while let Some(idx) = queue.pop() {
        if tiles[idx] != 0 { continue; }  // Wall

        let dist = distance_map[idx];
        let x = idx % width;
        let y = idx / width;

        let neighbors = [
            (x.wrapping_sub(1), y),
            (x + 1, y),
            (x, y.wrapping_sub(1)),
            (x, y + 1),
        ];

        for (nx, ny) in neighbors {
            if nx >= width || ny >= tiles.len() / width { continue; }
            let nidx = ny * width + nx;
            if distance_map[nidx] > dist + 1 && tiles[nidx] == 0 {
                distance_map[nidx] = dist + 1;
                queue.push(nidx);
            }
        }
    }

    // Find max distance for normalization
    let max_dist = *distance_map.iter().filter(|&&d| d < u16::MAX).max().unwrap_or(&1);

    // Create spawn points at floor tiles
    for (idx, &tile) in tiles.iter().enumerate() {
        if tile != 0 { continue; }

        let dist = distance_map[idx];
        if dist == u16::MAX { continue; }

        // Spawn probability increases with distance
        let normalized = dist as f32 / max_dist as f32;
        let spawn_chance = normalized * 0.3;  // 0-30% chance

        if (random() as f32 / i32::MAX as f32) < spawn_chance {
            let difficulty = ((normalized * 10.0) as u8).min(10);
            spawns.push(SpawnPoint {
                x: (idx % width) as u16,
                y: (idx / width) as u16,
                difficulty,
            });
        }
    }

    spawns
}
```

---

## Complete Generation Pipeline

```rust
struct LevelConfig {
    seed: u32,
    width: u16,
    height: u16,
    style: LevelStyle,
}

enum LevelStyle {
    Dungeon,
    Caves,
    OpenWorld,
}

struct GeneratedLevel {
    tiles: Vec<u8>,
    spawn_points: Vec<SpawnPoint>,
    player_start: (u16, u16),
    exit_pos: (u16, u16),
}

fn generate_level(config: &LevelConfig) -> GeneratedLevel {
    seed_random(config.seed);

    let tiles = match config.style {
        LevelStyle::Dungeon => generate_bsp_dungeon(
            config.seed, config.width, config.height, 5
        ),
        LevelStyle::Caves => generate_caves(
            config.seed, config.width as usize, config.height as usize, 45, 4
        ),
        LevelStyle::OpenWorld => generate_terrain(
            config.seed, config.width as usize, config.height as usize
        ),
    };

    // Find valid start position (first floor tile)
    let mut player_start = (1, 1);
    for (idx, &tile) in tiles.iter().enumerate() {
        if tile == 0 {
            player_start = ((idx % config.width as usize) as u16,
                           (idx / config.width as usize) as u16);
            break;
        }
    }

    // Find exit (furthest floor from start)
    let spawn_points = generate_spawn_points(&tiles, config.width as usize,
                                              player_start.0, player_start.1);

    let exit_pos = spawn_points.iter()
        .max_by_key(|s| s.difficulty)
        .map(|s| (s.x, s.y))
        .unwrap_or(player_start);

    GeneratedLevel {
        tiles,
        spawn_points,
        player_start,
        exit_pos,
    }
}
```
