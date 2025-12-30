# Tileset Generation

Generate tilesets including autotiles, variations, and animated tiles.

## Autotile Generation (47-tile)

Generate tiles that automatically connect based on neighbors:

```python
import numpy as np
from PIL import Image
from dataclasses import dataclass
from enum import Enum

class CornerStyle(Enum):
    SQUARE = "square"
    ROUNDED = "rounded"
    BEVELED = "beveled"

@dataclass
class Neighbors:
    """Neighbor flags for autotiling."""
    n: bool = False
    s: bool = False
    e: bool = False
    w: bool = False
    ne: bool = False
    nw: bool = False
    se: bool = False
    sw: bool = False

def generate_autotile_set(
    tile_size: int,
    terrain_color: int,
    edge_color: int,
    corner_style: CornerStyle = CornerStyle.SQUARE
) -> Image.Image:
    """Generate 47-tile autotile set (4-corner blob style)."""
    atlas_width = tile_size * 8   # 8 columns
    atlas_height = tile_size * 6  # 6 rows = 48 slots
    atlas = np.zeros((atlas_height, atlas_width, 4), dtype=np.uint8)

    for tile_id in range(47):
        neighbors = AUTOTILE_47_MAP[tile_id]
        tile = generate_single_autotile(
            tile_size, terrain_color, edge_color, neighbors, corner_style
        )

        col = tile_id % 8
        row = tile_id // 8
        y, x = row * tile_size, col * tile_size
        atlas[y:y + tile_size, x:x + tile_size] = tile

    return Image.fromarray(atlas)
```

## Tile Variations

Add visual interest with randomized variations:

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType

def generate_tile_variations(
    base_tile: Image.Image,
    variation_count: int,
    noise_intensity: float,
    seed: int
) -> Image.Image:
    """Generate tile variations with noise-based brightness changes."""
    tile_array = np.array(base_tile)
    tile_size = base_tile.width
    atlas = np.zeros((tile_size, tile_size * variation_count, 4), dtype=np.uint8)

    for v in range(variation_count):
        variant = tile_array.copy().astype(np.float32)

        # Configure noise generator for this variation
        noise = FastNoiseLite(seed + v)
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2

        # Create noise map (vectorized)
        y_coords, x_coords = np.meshgrid(
            np.arange(tile_size) * 0.1,
            np.arange(tile_size) * 0.1,
            indexing='ij'
        )
        noise_values = np.vectorize(noise.get_noise_2d)(x_coords, y_coords)

        # Apply brightness variation to RGB channels
        brightness_adjust = noise_values[..., np.newaxis] * noise_intensity * 32
        variant[..., :3] = np.clip(variant[..., :3] + brightness_adjust, 0, 255)

        # Blit variant to atlas
        x_offset = v * tile_size
        atlas[:, x_offset:x_offset + tile_size] = variant.astype(np.uint8)

    return Image.fromarray(atlas)
```

## Animated Tiles

Generate animation frames for water, lava, etc.:

```python
import numpy as np
from PIL import Image
from enum import Enum
from pyfastnoiselite import FastNoiseLite, NoiseType

class AnimationType(Enum):
    WATER = "water"
    LAVA = "lava"
    SPARKLE = "sparkle"

def generate_animated_tile(
    tile_size: int,
    frame_count: int,
    base_color: int,
    animation_type: AnimationType,
    seed: int
) -> Image.Image:
    """Generate animation frames for animated tiles (water, lava, etc.)."""
    atlas = np.zeros((tile_size, tile_size * frame_count, 4), dtype=np.uint8)

    # Convert base_color (0xRRGGBBAA) to RGBA array
    base_rgba = np.array([
        (base_color >> 24) & 0xFF,
        (base_color >> 16) & 0xFF,
        (base_color >> 8) & 0xFF,
        base_color & 0xFF
    ], dtype=np.float32)

    for frame in range(frame_count):
        phase = frame / frame_count * 2 * np.pi  # TAU
        tile = np.zeros((tile_size, tile_size, 4), dtype=np.float32)

        # Create coordinate grids
        y_coords, x_coords = np.meshgrid(
            np.arange(tile_size),
            np.arange(tile_size),
            indexing='ij'
        )

        if animation_type == AnimationType.WATER:
            # Scrolling sine wave pattern (vectorized)
            wave = (np.sin(x_coords * 0.3 + phase) * 0.5 + 0.5)
            dark_color = base_rgba.copy()
            dark_color[:3] *= 0.7  # Darken by 30%

            # Blend colors based on wave
            for c in range(4):
                tile[..., c] = base_rgba[c] * wave + dark_color[c] * (1 - wave)

        elif animation_type == AnimationType.LAVA:
            # Bubbling noise
            noise = FastNoiseLite(seed)
            noise.noise_type = NoiseType.NoiseType_OpenSimplex2
            noise_values = np.vectorize(
                lambda x, y: noise.get_noise_3d(x * 0.1, y * 0.1, phase)
            )(x_coords, y_coords)

            # Apply glow where noise > 0.3
            glow_mask = noise_values > 0.3
            tile[..., :3] = base_rgba[:3]
            tile[..., 3] = base_rgba[3]
            # Lighten glowing areas
            tile[glow_mask, :3] = np.clip(
                base_rgba[:3] + noise_values[glow_mask, np.newaxis] * 0.5 * 128, 0, 255
            )

        # Blit tile to atlas
        x_offset = frame * tile_size
        atlas[:, x_offset:x_offset + tile_size] = tile.astype(np.uint8)

    return Image.fromarray(atlas)
```

## Autotile Systems Comparison

| System | Tiles | Bits | Use Case |
|--------|-------|------|----------|
| 2-corner (16) | 16 | 4 | Basic, minimal |
| 4-corner (47) | 47 | 8 | Standard RPG |
| Blob (256) | 256 | 8 | Smooth, complete |

## Data Tables (Keep Separate!)

**Important:** Store autotile neighbor maps in separate data modules:

```python
# data/autotile_47.py - DATA ONLY
from dataclasses import dataclass

@dataclass
class Neighbors:
    n: bool = False
    s: bool = False
    e: bool = False
    w: bool = False
    ne: bool = False
    nw: bool = False
    se: bool = False
    sw: bool = False

AUTOTILE_47_MAP: list[Neighbors] = [
    Neighbors(n=False, s=False, e=False, w=False),
    # ... all 47 entries
]
```

See `references/autotile-patterns.md` for complete neighbor mapping tables.
