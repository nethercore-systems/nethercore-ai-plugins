# Tile Map Patterns Reference

Complete tile-based level system implementations for Nethercore ZX.

## Full Tile Map Implementation

### Core Data Structures

```rust
use crate::ffi::*;

const TILE_SIZE: u32 = 16;
const MAX_TILES: usize = 256;

/// Tile definition with rendering and collision info
#[derive(Clone, Copy)]
struct TileDef {
    sprite_id: u16,       // Asset ID for rendering
    collision: u8,        // Collision flags
    frame_count: u8,      // Animation frames (1 = static)
    frame_rate: u8,       // Ticks per frame
}

/// Tile map layer
struct TileLayer {
    width: u16,
    height: u16,
    tiles: Vec<u8>,       // Tile indices
    offset_x: f32,        // Parallax offset
    offset_y: f32,
    scroll_factor: f32,   // 1.0 = foreground, <1.0 = parallax
}

/// Complete map with multiple layers
struct TileMap {
    tile_defs: [TileDef; MAX_TILES],
    layers: Vec<TileLayer>,
    collision_layer: usize,  // Which layer has collision
}

impl TileLayer {
    fn get(&self, x: u16, y: u16) -> u8 {
        if x < self.width && y < self.height {
            self.tiles[(y as usize) * (self.width as usize) + (x as usize)]
        } else {
            0
        }
    }

    fn set(&mut self, x: u16, y: u16, tile: u8) {
        if x < self.width && y < self.height {
            self.tiles[(y as usize) * (self.width as usize) + (x as usize)] = tile;
        }
    }
}
```

### Rendering with Camera

```rust
fn render_tile_layer(map: &TileMap, layer: &TileLayer, camera_x: f32, camera_y: f32) {
    let scroll_x = camera_x * layer.scroll_factor + layer.offset_x;
    let scroll_y = camera_y * layer.scroll_factor + layer.offset_y;

    // Calculate visible tile range
    let start_x = (scroll_x / TILE_SIZE as f32).floor() as i32;
    let start_y = (scroll_y / TILE_SIZE as f32).floor() as i32;
    let end_x = start_x + (960 / TILE_SIZE as i32) + 2;
    let end_y = start_y + (540 / TILE_SIZE as i32) + 2;

    for ty in start_y..end_y {
        for tx in start_x..end_x {
            if tx < 0 || ty < 0 { continue; }

            let tile_idx = layer.get(tx as u16, ty as u16);
            if tile_idx == 0 { continue; }  // Skip empty tiles

            let def = &map.tile_defs[tile_idx as usize];
            let screen_x = (tx as f32 * TILE_SIZE as f32) - scroll_x;
            let screen_y = (ty as f32 * TILE_SIZE as f32) - scroll_y;

            // Handle animation
            let frame = if def.frame_count > 1 {
                ((tick_count() / def.frame_rate as u64) % def.frame_count as u64) as u16
            } else {
                0
            };

            draw_sprite(def.sprite_id + frame, screen_x, screen_y);
        }
    }
}

fn render_map(map: &TileMap, camera_x: f32, camera_y: f32) {
    // Render back to front
    for layer in &map.layers {
        render_tile_layer(map, layer, camera_x, camera_y);
    }
}
```

---

## Collision Detection

### Point Collision

```rust
fn tile_at_point(map: &TileMap, x: f32, y: f32) -> Option<&TileDef> {
    let layer = &map.layers[map.collision_layer];
    let tx = (x / TILE_SIZE as f32) as u16;
    let ty = (y / TILE_SIZE as f32) as u16;
    let idx = layer.get(tx, ty);
    if idx > 0 {
        Some(&map.tile_defs[idx as usize])
    } else {
        None
    }
}

fn is_solid_at(map: &TileMap, x: f32, y: f32) -> bool {
    tile_at_point(map, x, y)
        .map(|t| (t.collision & COLLISION_SOLID) != 0)
        .unwrap_or(false)
}
```

### AABB vs Tile Grid

```rust
fn check_tile_collision(map: &TileMap, x: f32, y: f32, w: f32, h: f32, mask: u8) -> bool {
    let layer = &map.layers[map.collision_layer];

    // Get tile range overlapping AABB
    let left = (x / TILE_SIZE as f32).floor() as i32;
    let right = ((x + w) / TILE_SIZE as f32).floor() as i32;
    let top = (y / TILE_SIZE as f32).floor() as i32;
    let bottom = ((y + h) / TILE_SIZE as f32).floor() as i32;

    for ty in top..=bottom {
        for tx in left..=right {
            if tx < 0 || ty < 0 { continue; }
            let idx = layer.get(tx as u16, ty as u16);
            if idx > 0 {
                let def = &map.tile_defs[idx as usize];
                if (def.collision & mask) != 0 {
                    return true;
                }
            }
        }
    }
    false
}

fn resolve_horizontal(map: &TileMap, x: &mut f32, y: f32, w: f32, h: f32, vel_x: f32) {
    let new_x = *x + vel_x;

    if vel_x > 0.0 {
        // Moving right - check right edge
        if check_tile_collision(map, new_x, y, w, h, COLLISION_SOLID) {
            // Snap to tile boundary
            *x = ((new_x + w) / TILE_SIZE as f32).floor() * TILE_SIZE as f32 - w - 0.01;
        } else {
            *x = new_x;
        }
    } else if vel_x < 0.0 {
        // Moving left - check left edge
        if check_tile_collision(map, new_x, y, w, h, COLLISION_SOLID) {
            *x = (new_x / TILE_SIZE as f32).ceil() * TILE_SIZE as f32 + 0.01;
        } else {
            *x = new_x;
        }
    }
}

fn resolve_vertical(map: &TileMap, x: f32, y: &mut f32, w: f32, h: f32,
                    vel_y: f32, grounded: &mut bool) {
    let new_y = *y + vel_y;

    if vel_y > 0.0 {
        // Falling - check bottom edge
        if check_tile_collision(map, x, new_y, w, h, COLLISION_SOLID) {
            *y = ((new_y + h) / TILE_SIZE as f32).floor() * TILE_SIZE as f32 - h - 0.01;
            *grounded = true;
        } else {
            *y = new_y;
            *grounded = false;
        }
    } else if vel_y < 0.0 {
        // Rising - check top edge
        if check_tile_collision(map, x, new_y, w, h, COLLISION_SOLID) {
            *y = (new_y / TILE_SIZE as f32).ceil() * TILE_SIZE as f32 + 0.01;
        } else {
            *y = new_y;
        }
    }
}
```

---

## Slope Handling

### 45-Degree Slopes

```rust
const SLOPE_UP_RIGHT: u8 = 1;   // / shape
const SLOPE_UP_LEFT: u8 = 2;    // \ shape

fn get_slope_height(slope_type: u8, x_in_tile: f32) -> f32 {
    let normalized = x_in_tile / TILE_SIZE as f32;  // 0.0 to 1.0

    match slope_type {
        SLOPE_UP_RIGHT => (1.0 - normalized) * TILE_SIZE as f32,
        SLOPE_UP_LEFT => normalized * TILE_SIZE as f32,
        _ => 0.0,
    }
}

fn check_slope_collision(map: &TileMap, x: f32, y: f32, w: f32, h: f32) -> Option<f32> {
    let layer = &map.layers[map.collision_layer];

    // Check tile at player's feet center
    let foot_x = x + w / 2.0;
    let foot_y = y + h;
    let tx = (foot_x / TILE_SIZE as f32) as u16;
    let ty = (foot_y / TILE_SIZE as f32) as u16;

    let idx = layer.get(tx, ty);
    if idx == 0 { return None; }

    let def = &map.tile_defs[idx as usize];
    if def.collision != SLOPE_UP_RIGHT && def.collision != SLOPE_UP_LEFT {
        return None;
    }

    // Calculate height at this x position
    let tile_base_y = ty as f32 * TILE_SIZE as f32;
    let x_in_tile = foot_x - (tx as f32 * TILE_SIZE as f32);
    let slope_height = get_slope_height(def.collision, x_in_tile);
    let ground_y = tile_base_y + TILE_SIZE as f32 - slope_height;

    if foot_y >= ground_y {
        Some(ground_y - h)
    } else {
        None
    }
}
```

---

## Chunk Streaming

For large worlds that exceed ROM budget.

### Chunk Manager

```rust
const CHUNK_SIZE: usize = 32;  // 32x32 tiles
const CHUNK_BYTES: usize = CHUNK_SIZE * CHUNK_SIZE;

struct Chunk {
    tiles: [u8; CHUNK_BYTES],
    loaded: bool,
}

struct ChunkManager {
    chunks: HashMap<(i32, i32), Chunk>,
    world_seed: u32,
    loaded_radius: i32,
}

impl ChunkManager {
    fn get_chunk_coord(world_x: f32, world_y: f32) -> (i32, i32) {
        let chunk_world_size = (CHUNK_SIZE * TILE_SIZE as usize) as f32;
        (
            (world_x / chunk_world_size).floor() as i32,
            (world_y / chunk_world_size).floor() as i32,
        )
    }

    fn update(&mut self, player_x: f32, player_y: f32) {
        let (cx, cy) = Self::get_chunk_coord(player_x, player_y);

        // Load chunks in radius
        for dy in -self.loaded_radius..=self.loaded_radius {
            for dx in -self.loaded_radius..=self.loaded_radius {
                let coord = (cx + dx, cy + dy);
                if !self.chunks.contains_key(&coord) {
                    self.load_chunk(coord);
                }
            }
        }

        // Unload distant chunks
        let to_unload: Vec<_> = self.chunks.keys()
            .filter(|(x, y)| (x - cx).abs() > self.loaded_radius + 1 ||
                            (y - cy).abs() > self.loaded_radius + 1)
            .cloned()
            .collect();

        for coord in to_unload {
            self.chunks.remove(&coord);
        }
    }

    fn load_chunk(&mut self, coord: (i32, i32)) {
        // Generate chunk deterministically from world seed + position
        let chunk_seed = self.world_seed
            .wrapping_add(coord.0 as u32 * 73856093)
            .wrapping_add(coord.1 as u32 * 19349663);
        seed_random(chunk_seed);

        let mut chunk = Chunk {
            tiles: [0; CHUNK_BYTES],
            loaded: true,
        };

        // Generate tiles (example: noise-based terrain)
        for y in 0..CHUNK_SIZE {
            for x in 0..CHUNK_SIZE {
                let world_x = coord.0 * CHUNK_SIZE as i32 + x as i32;
                let world_y = coord.1 * CHUNK_SIZE as i32 + y as i32;
                chunk.tiles[y * CHUNK_SIZE + x] = generate_tile(world_x, world_y);
            }
        }

        self.chunks.insert(coord, chunk);
    }

    fn get_tile(&self, world_x: i32, world_y: i32) -> u8 {
        let chunk_x = world_x.div_euclid(CHUNK_SIZE as i32);
        let chunk_y = world_y.div_euclid(CHUNK_SIZE as i32);
        let local_x = world_x.rem_euclid(CHUNK_SIZE as i32) as usize;
        let local_y = world_y.rem_euclid(CHUNK_SIZE as i32) as usize;

        self.chunks.get(&(chunk_x, chunk_y))
            .map(|c| c.tiles[local_y * CHUNK_SIZE + local_x])
            .unwrap_or(0)
    }
}
```

---

## Autotiling

Automatic tile selection based on neighbors.

### 4-Bit Autotile (Simple)

```rust
/// Check 4 neighbors, create 4-bit mask
fn get_autotile_mask_4(layer: &TileLayer, x: u16, y: u16, base_tile: u8) -> u8 {
    let mut mask = 0u8;

    // Check if neighbor is same tile type
    let check = |dx: i32, dy: i32| -> bool {
        let nx = x as i32 + dx;
        let ny = y as i32 + dy;
        if nx < 0 || ny < 0 { return true; }  // Edges count as same
        layer.get(nx as u16, ny as u16) == base_tile
    };

    if check(0, -1) { mask |= 0b0001; }  // Top
    if check(1, 0)  { mask |= 0b0010; }  // Right
    if check(0, 1)  { mask |= 0b0100; }  // Bottom
    if check(-1, 0) { mask |= 0b1000; }  // Left

    mask
}

/// Get sprite for 4-bit mask (16 variants)
fn autotile_sprite_4(base_sprite: u16, mask: u8) -> u16 {
    // Sprite sheet layout: 4x4 grid of variants
    base_sprite + mask as u16
}
```

### 8-Bit Autotile (Full)

For smooth corners, check all 8 neighbors:

```rust
/// 8-neighbor mask for 47-tile sets (or 256 with full corners)
fn get_autotile_mask_8(layer: &TileLayer, x: u16, y: u16, base_tile: u8) -> u8 {
    let mut mask = 0u8;

    let check = |dx: i32, dy: i32| -> bool {
        let nx = x as i32 + dx;
        let ny = y as i32 + dy;
        if nx < 0 || ny < 0 { return true; }
        layer.get(nx as u16, ny as u16) == base_tile
    };

    // Cardinal directions
    if check(0, -1) { mask |= 0b0000_0001; }  // N
    if check(1, 0)  { mask |= 0b0000_0010; }  // E
    if check(0, 1)  { mask |= 0b0000_0100; }  // S
    if check(-1, 0) { mask |= 0b0000_1000; }  // W

    // Diagonals (only matter if adjacent cardinals are same)
    if check(-1, -1) && (mask & 0b1001) == 0b1001 { mask |= 0b0001_0000; }  // NW
    if check(1, -1)  && (mask & 0b0011) == 0b0011 { mask |= 0b0010_0000; }  // NE
    if check(1, 1)   && (mask & 0b0110) == 0b0110 { mask |= 0b0100_0000; }  // SE
    if check(-1, 1)  && (mask & 0b1100) == 0b1100 { mask |= 0b1000_0000; }  // SW

    mask
}
```

---

## RLE Compression

Reduce ROM usage for large maps.

```rust
/// Run-length encode tile data
fn rle_encode(tiles: &[u8]) -> Vec<u8> {
    let mut encoded = Vec::new();
    let mut i = 0;

    while i < tiles.len() {
        let tile = tiles[i];
        let mut run = 1u8;

        // Count consecutive same tiles (max 255)
        while i + run as usize < tiles.len() &&
              tiles[i + run as usize] == tile &&
              run < 255 {
            run += 1;
        }

        encoded.push(run);
        encoded.push(tile);
        i += run as usize;
    }

    encoded
}

/// Decode RLE data
fn rle_decode(encoded: &[u8], out: &mut [u8]) {
    let mut read = 0;
    let mut write = 0;

    while read < encoded.len() && write < out.len() {
        let run = encoded[read] as usize;
        let tile = encoded[read + 1];
        read += 2;

        for _ in 0..run {
            if write < out.len() {
                out[write] = tile;
                write += 1;
            }
        }
    }
}
```

---

## Editor Integration

Tile map format for external editors (Tiled, LDtk).

### Tiled JSON Import

```rust
/// Minimal Tiled layer import
fn load_tiled_layer(json: &str) -> TileLayer {
    // Parse JSON (simplified)
    let width = parse_field::<u16>(json, "width");
    let height = parse_field::<u16>(json, "height");
    let data = parse_array::<u8>(json, "data");

    TileLayer {
        width,
        height,
        tiles: data,
        offset_x: 0.0,
        offset_y: 0.0,
        scroll_factor: 1.0,
    }
}
```

### Recommended Format

For ZX ROMs, use binary format:

```
Header (8 bytes):
  u16 width
  u16 height
  u16 tile_count
  u8  layer_count
  u8  flags (RLE compressed, etc.)

Tile Definitions (tile_count * 4 bytes each):
  u16 sprite_id
  u8  collision
  u8  animation_frames

Layer Data (per layer):
  If RLE: encoded bytes
  Else: width * height bytes
```
