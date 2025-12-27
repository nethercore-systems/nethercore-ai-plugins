# Autotile Pattern Reference

Complete neighbor mapping tables for procedural tileset generation.

## Overview

Autotiles automatically select the correct tile graphic based on neighboring tiles of the same type. Three main systems exist with varying complexity.

## Neighbor Bit Flags

Standard bit encoding for neighbor presence:

```rust
const N:  u8 = 0b00000001;  // North
const S:  u8 = 0b00000010;  // South
const E:  u8 = 0b00000100;  // East
const W:  u8 = 0b00001000;  // West
const NE: u8 = 0b00010000;  // North-East
const NW: u8 = 0b00100000;  // North-West
const SE: u8 = 0b01000000;  // South-East
const SW: u8 = 0b10000000;  // South-West
```

---

## 16-Tile System (2-Corner)

Simplest autotile system. Only considers cardinal directions (N, S, E, W). Corners are implied.

### Tile Index Calculation

```rust
fn get_tile_index_16(neighbors: u8) -> usize {
    let n = (neighbors & N) != 0;
    let s = (neighbors & S) != 0;
    let e = (neighbors & E) != 0;
    let w = (neighbors & W) != 0;

    // 4-bit index: NSEW
    ((n as usize) << 3) | ((s as usize) << 2) | ((e as usize) << 1) | (w as usize)
}
```

### 16-Tile Layout

```
Index  NSEW   Description
-----  ----   -----------
0      0000   Isolated (no neighbors)
1      0001   West only
2      0010   East only
3      0011   East-West corridor
4      0100   South only
5      0101   South-West corner (inner)
6      0110   South-East corner (inner)
7      0111   South edge
8      1000   North only
9      1001   North-West corner (inner)
10     1010   North-East corner (inner)
11     1011   North edge
12     1100   North-South corridor
13     1101   West edge
14     1110   East edge
15     1111   Center (all neighbors)
```

### Atlas Layout (4x4)

```
+---+---+---+---+
| 0 | 1 | 2 | 3 |
+---+---+---+---+
| 4 | 5 | 6 | 7 |
+---+---+---+---+
| 8 | 9 |10 |11 |
+---+---+---+---+
|12 |13 |14 |15 |
+---+---+---+---+
```

---

## 47-Tile System (4-Corner Blob)

Standard RPG tileset system. Considers all 8 neighbors but only diagonal neighbors where both adjacent cardinals are present.

### Key Insight

A diagonal neighbor (NE, NW, SE, SW) only affects the tile if BOTH adjacent cardinals are present. Example: NE corner only matters if both N and E are present.

### Tile Mapping Table

The 47-tile system maps 256 possible neighbor combinations to 47 unique tiles:

```rust
/// Maps 8-bit neighbor flags to 47-tile index
const AUTOTILE_47_MAP: [u8; 256] = [
    // Generated from blob rules - each index is the 8-bit neighbor flag
    // Value is the tile index (0-46)
     0,  1,  2,  3,  1,  1,  3,  3,  4,  5,  6,  7,  5,  5,  7,  7,
     8,  9, 10, 11,  9,  9, 11, 11, 12, 13, 14, 15, 13, 13, 15, 15,
     4,  5,  6,  7,  5,  5,  7,  7,  4,  5,  6,  7,  5,  5,  7,  7,
    12, 13, 14, 15, 13, 13, 15, 15, 12, 13, 14, 15, 13, 13, 15, 15,
    16, 17, 18, 19, 17, 17, 19, 19, 20, 21, 22, 23, 21, 21, 23, 23,
    24, 25, 26, 27, 25, 25, 27, 27, 28, 29, 30, 31, 29, 29, 31, 31,
    20, 21, 22, 23, 21, 21, 23, 23, 20, 21, 22, 23, 21, 21, 23, 23,
    28, 29, 30, 31, 29, 29, 31, 31, 28, 29, 30, 31, 29, 29, 31, 31,
    16, 17, 18, 19, 17, 17, 19, 19, 20, 21, 22, 23, 21, 21, 23, 23,
    24, 25, 26, 27, 25, 25, 27, 27, 28, 29, 30, 31, 29, 29, 31, 31,
    20, 21, 22, 23, 21, 21, 23, 23, 20, 21, 22, 23, 21, 21, 23, 23,
    28, 29, 30, 31, 29, 29, 31, 31, 28, 29, 30, 31, 29, 29, 31, 31,
    32, 33, 34, 35, 33, 33, 35, 35, 36, 37, 38, 39, 37, 37, 39, 39,
    40, 41, 42, 43, 41, 41, 43, 43, 44, 45, 46, 46, 45, 45, 46, 46,
    36, 37, 38, 39, 37, 37, 39, 39, 36, 37, 38, 39, 37, 37, 39, 39,
    44, 45, 46, 46, 45, 45, 46, 46, 44, 45, 46, 46, 45, 45, 46, 46,
];

fn get_tile_index_47(neighbors: u8) -> usize {
    AUTOTILE_47_MAP[neighbors as usize] as usize
}
```

### 47-Tile Descriptions

```
Index  Description                      Corners Affected
-----  -----------                      ----------------
0      Isolated                         None
1      West only                        None
2      East only                        None
3      East-West corridor               None
4      South only                       None
5      South-West inner                 None
6      South-East inner                 None
7      South edge                       None
8      North only                       None
9      North-West inner                 None
10     North-East inner                 None
11     North edge                       None
12     North-South corridor             None
13     West edge                        None
14     East edge                        None
15     Center, no corners               None
16     South, SE corner missing         SE
17     South-West, SE missing           SE
18     South-East, SE missing           SE
19     South edge, SE missing           SE
20     NS corridor, SE missing          SE
21     West edge, SE missing            SE
22     East edge, SE missing            SE
23     Center, SE missing               SE
24     South, SW corner missing         SW
25     South-West, SW missing           SW
26     South-East, SW missing           SW
27     South edge, SW missing           SW
28     NS corridor, SW missing          SW
29     West edge, SW missing            SW
30     East edge, SW missing            SW
31     Center, SW missing               SW
32     North, NE corner missing         NE
33     North-West, NE missing           NE
34     North-East, NE missing           NE
35     North edge, NE missing           NE
36     NS corridor, NE missing          NE
37     West edge, NE missing            NE
38     East edge, NE missing            NE
39     Center, NE missing               NE
40     North, NW corner missing         NW
41     North-West, NW missing           NW
42     North-East, NW missing           NW
43     North edge, NW missing           NW
44     NS corridor, NW missing          NW
45     West edge, NW missing            NW
46     Center, NW missing (or any combo) NW+
```

### Atlas Layout (8x6)

```
+---+---+---+---+---+---+---+---+
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
+---+---+---+---+---+---+---+---+
| 8 | 9 |10 |11 |12 |13 |14 |15 |
+---+---+---+---+---+---+---+---+
|16 |17 |18 |19 |20 |21 |22 |23 |
+---+---+---+---+---+---+---+---+
|24 |25 |26 |27 |28 |29 |30 |31 |
+---+---+---+---+---+---+---+---+
|32 |33 |34 |35 |36 |37 |38 |39 |
+---+---+---+---+---+---+---+---+
|40 |41 |42 |43 |44 |45 |46 |   |
+---+---+---+---+---+---+---+---+
```

---

## 256-Tile System (Full Blob)

Complete 8-neighbor system with all 256 unique combinations. Maximum visual quality but largest atlas size.

### Tile Index Calculation

Direct use of 8-bit neighbor flags as index:

```rust
fn get_tile_index_256(neighbors: u8) -> usize {
    neighbors as usize
}
```

### Atlas Layout (16x16)

Tiles arranged by index (0-255) in row-major order:

```rust
fn atlas_position_256(index: usize, tile_size: u32) -> (u32, u32) {
    let col = (index % 16) as u32;
    let row = (index / 16) as u32;
    (col * tile_size, row * tile_size)
}
```

---

## Generation Code

### 47-Tile Generator

```rust
fn generate_autotile_47(
    tile_size: u32,
    fill_color: u32,
    edge_color: u32,
    corner_radius: u32,
) -> TextureBuffer {
    let mut atlas = TextureBuffer::new(tile_size * 8, tile_size * 6);

    for tile_idx in 0..47 {
        let tile = generate_tile_for_index(tile_idx, tile_size, fill_color, edge_color, corner_radius);
        let col = tile_idx % 8;
        let row = tile_idx / 8;
        atlas.blit(&tile, (col * tile_size as usize) as u32, (row * tile_size as usize) as u32);
    }

    atlas
}

fn generate_tile_for_index(
    idx: usize,
    size: u32,
    fill: u32,
    edge: u32,
    radius: u32,
) -> TextureBuffer {
    let mut tile = TextureBuffer::new(size, size);

    // Decode which edges/corners this tile needs
    let (has_n, has_s, has_e, has_w, has_ne, has_nw, has_se, has_sw) = decode_tile_47(idx);

    // Fill base
    tile.solid(fill);

    // Draw edges where no neighbor
    if !has_n { draw_edge(&mut tile, Edge::North, edge, radius); }
    if !has_s { draw_edge(&mut tile, Edge::South, edge, radius); }
    if !has_e { draw_edge(&mut tile, Edge::East, edge, radius); }
    if !has_w { draw_edge(&mut tile, Edge::West, edge, radius); }

    // Draw outer corners (where both adjacent edges exist)
    if !has_n && !has_w { draw_outer_corner(&mut tile, Corner::NW, edge, radius); }
    if !has_n && !has_e { draw_outer_corner(&mut tile, Corner::NE, edge, radius); }
    if !has_s && !has_w { draw_outer_corner(&mut tile, Corner::SW, edge, radius); }
    if !has_s && !has_e { draw_outer_corner(&mut tile, Corner::SE, edge, radius); }

    // Draw inner corners (where diagonal missing but cardinals present)
    if has_n && has_w && !has_nw { draw_inner_corner(&mut tile, Corner::NW, edge, radius); }
    if has_n && has_e && !has_ne { draw_inner_corner(&mut tile, Corner::NE, edge, radius); }
    if has_s && has_w && !has_sw { draw_inner_corner(&mut tile, Corner::SW, edge, radius); }
    if has_s && has_e && !has_se { draw_inner_corner(&mut tile, Corner::SE, edge, radius); }

    tile
}
```

---

## Runtime Usage

### Calculating Neighbors at Runtime

```rust
fn get_neighbor_flags(map: &Tilemap, x: i32, y: i32, tile_type: u8) -> u8 {
    let mut flags = 0u8;

    let same = |dx: i32, dy: i32| -> bool {
        map.get(x + dx, y + dy).map_or(false, |t| t == tile_type)
    };

    if same(0, -1) { flags |= N; }
    if same(0, 1)  { flags |= S; }
    if same(1, 0)  { flags |= E; }
    if same(-1, 0) { flags |= W; }
    if same(1, -1) { flags |= NE; }
    if same(-1, -1) { flags |= NW; }
    if same(1, 1)  { flags |= SE; }
    if same(-1, 1) { flags |= SW; }

    flags
}

fn draw_autotile(
    map: &Tilemap,
    atlas: u32,
    x: i32, y: i32,
    tile_type: u8,
    tile_size: u32,
    system: AutotileSystem,
) {
    let neighbors = get_neighbor_flags(map, x, y, tile_type);
    let tile_idx = match system {
        AutotileSystem::Tile16 => get_tile_index_16(neighbors),
        AutotileSystem::Tile47 => get_tile_index_47(neighbors),
        AutotileSystem::Tile256 => neighbors as usize,
    };

    let (atlas_cols, _) = match system {
        AutotileSystem::Tile16 => (4, 4),
        AutotileSystem::Tile47 => (8, 6),
        AutotileSystem::Tile256 => (16, 16),
    };

    let src_x = (tile_idx % atlas_cols) as u32 * tile_size;
    let src_y = (tile_idx / atlas_cols) as u32 * tile_size;

    draw_sprite_region(
        atlas,
        x as u32 * tile_size, y as u32 * tile_size,
        src_x, src_y,
        tile_size, tile_size,
    );
}
```

---

## Python Implementation

```python
import numpy as np
from PIL import Image

# Neighbor flags
N, S, E, W = 0x01, 0x02, 0x04, 0x08
NE, NW, SE, SW = 0x10, 0x20, 0x40, 0x80

def generate_autotile_47(tile_size, fill_color, edge_color):
    """Generate 47-tile autotile atlas."""
    atlas = np.zeros((tile_size * 6, tile_size * 8, 4), dtype=np.uint8)

    for idx in range(47):
        tile = generate_single_tile(idx, tile_size, fill_color, edge_color)
        row, col = divmod(idx, 8)
        y, x = row * tile_size, col * tile_size
        atlas[y:y+tile_size, x:x+tile_size] = tile

    return Image.fromarray(atlas)

def decode_tile_47(idx):
    """Decode tile index to neighbor presence flags."""
    # Simplified - in practice use lookup table
    # Returns (has_n, has_s, has_e, has_w, has_ne, has_nw, has_se, has_sw)
    # This requires the inverse of AUTOTILE_47_MAP
    pass

def generate_single_tile(idx, size, fill, edge):
    """Generate a single autotile."""
    tile = np.full((size, size, 4), [
        (fill >> 24) & 0xFF,
        (fill >> 16) & 0xFF,
        (fill >> 8) & 0xFF,
        fill & 0xFF
    ], dtype=np.uint8)

    # Draw edges based on decoded neighbors
    neighbors = decode_tile_47(idx)
    # ... edge and corner drawing logic

    return tile
```

---

## Choosing a System

| System | Pros | Cons | Best For |
|--------|------|------|----------|
| 16-tile | Smallest atlas, simple | No inner corners | Simple games, prototypes |
| 47-tile | Good balance | More complex generation | Most 2D games, RPGs |
| 256-tile | Maximum quality | Large atlas (256 tiles) | High polish, smooth terrain |

**Recommendation:** Start with 47-tile for most projects. It handles all common cases while keeping atlas size manageable.
