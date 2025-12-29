# Texture Atlas Packing

Nethercore ZX binds one texture per slot. For meshes with multiple materials, pack textures into atlases.

## Atlas Workflow

1. Generate individual material textures
2. Pack into grid atlas (2x2, 4x4)
3. Generate matching atlas for each required slot
4. Remap mesh UVs to atlas quadrants

---

## Atlas Packing Utility

```python
import numpy as np
from PIL import Image
from pathlib import Path

def pack_atlas_2x2(textures: list[str], output: str, size: int = 512):
    """Pack 4 textures into a 2x2 atlas.

    Args:
        textures: List of 4 texture paths [TL, TR, BL, BR]
        output: Output atlas path
        size: Total atlas size (each texture is size/2)
    """
    assert len(textures) == 4, "Need exactly 4 textures for 2x2 atlas"

    half = size // 2
    atlas = np.zeros((size, size, 4), dtype=np.uint8)

    positions = [
        (0, 0),      # Top-left
        (half, 0),   # Top-right
        (0, half),   # Bottom-left
        (half, half) # Bottom-right
    ]

    for i, tex_path in enumerate(textures):
        if tex_path is None:
            continue

        img = Image.open(tex_path).convert('RGBA').resize((half, half))
        tex_data = np.array(img)

        x, y = positions[i]
        atlas[y:y+half, x:x+half] = tex_data

    Image.fromarray(atlas, 'RGBA').save(output)


def pack_atlas_4x4(textures: list[str], output: str, size: int = 512):
    """Pack up to 16 textures into a 4x4 atlas."""
    assert len(textures) <= 16, "Max 16 textures for 4x4 atlas"

    quarter = size // 4
    atlas = np.zeros((size, size, 4), dtype=np.uint8)

    for i, tex_path in enumerate(textures):
        if tex_path is None:
            continue

        row = i // 4
        col = i % 4

        img = Image.open(tex_path).convert('RGBA').resize((quarter, quarter))
        tex_data = np.array(img)

        x = col * quarter
        y = row * quarter
        atlas[y:y+quarter, x:x+quarter] = tex_data

    Image.fromarray(atlas, 'RGBA').save(output)
```

---

## Complete Material Set Atlas

```python
def pack_material_atlas_2x2(materials: list[dict], output_prefix: str,
                            mode: int = 2, size: int = 512):
    """Pack material sets into corresponding atlases.

    Args:
        materials: List of 4 material dicts with texture paths
                   [{"albedo": "...", "mre": "..."}, ...]
        output_prefix: Prefix for output files
        mode: Render mode (determines which maps to pack)
        size: Atlas size
    """
    half = size // 2
    positions = [(0, 0), (half, 0), (0, half), (half, half)]

    # Initialize atlases based on mode
    albedo_atlas = np.zeros((size, size, 4), dtype=np.uint8)

    if mode == 2:
        mre_atlas = np.zeros((size, size, 4), dtype=np.uint8)
    elif mode == 3:
        sse_atlas = np.zeros((size, size, 4), dtype=np.uint8)
        spec_atlas = np.zeros((size, size, 4), dtype=np.uint8)

    for i, mat in enumerate(materials):
        if mat is None:
            continue

        x, y = positions[i]

        # Pack albedo
        if "albedo" in mat:
            img = Image.open(mat["albedo"]).convert('RGBA').resize((half, half))
            albedo_atlas[y:y+half, x:x+half] = np.array(img)

        # Pack mode-specific maps
        if mode == 2 and "mre" in mat:
            img = Image.open(mat["mre"]).convert('RGBA').resize((half, half))
            mre_atlas[y:y+half, x:x+half] = np.array(img)

        elif mode == 3:
            if "sse" in mat:
                img = Image.open(mat["sse"]).convert('RGBA').resize((half, half))
                sse_atlas[y:y+half, x:x+half] = np.array(img)
            if "specular" in mat:
                img = Image.open(mat["specular"]).convert('RGBA').resize((half, half))
                spec_atlas[y:y+half, x:x+half] = np.array(img)

    # Save atlases
    Image.fromarray(albedo_atlas, 'RGBA').save(f"{output_prefix}_albedo.png")

    if mode == 2:
        Image.fromarray(mre_atlas, 'RGBA').save(f"{output_prefix}_mre.png")
    elif mode == 3:
        Image.fromarray(sse_atlas, 'RGBA').save(f"{output_prefix}_sse.png")
        Image.fromarray(spec_atlas, 'RGBA').save(f"{output_prefix}_specular.png")


# Example usage
materials = [
    {"albedo": "metal_albedo.png", "mre": "metal_mre.png"},
    {"albedo": "rubber_albedo.png", "mre": "rubber_mre.png"},
    {"albedo": "plastic_albedo.png", "mre": "plastic_mre.png"},
    {"albedo": "glass_albedo.png", "mre": "glass_mre.png"},
]
pack_material_atlas_2x2(materials, "vehicle_materials", mode=2)
```

---

## UV Region Reference

### 2x2 Atlas

| Quadrant | Position | UV Range |
|----------|----------|----------|
| Top-left (0) | (0, 0) | U: 0.0-0.5, V: 0.5-1.0 |
| Top-right (1) | (half, 0) | U: 0.5-1.0, V: 0.5-1.0 |
| Bottom-left (2) | (0, half) | U: 0.0-0.5, V: 0.0-0.5 |
| Bottom-right (3) | (half, half) | U: 0.5-1.0, V: 0.0-0.5 |

### 4x4 Atlas

Each cell is 0.25 x 0.25 UV units.

| Cell | U Range | V Range |
|------|---------|---------|
| 0 | 0.00-0.25 | 0.75-1.00 |
| 1 | 0.25-0.50 | 0.75-1.00 |
| 2 | 0.50-0.75 | 0.75-1.00 |
| 3 | 0.75-1.00 | 0.75-1.00 |
| 4 | 0.00-0.25 | 0.50-0.75 |
| ... | ... | ... |
| 15 | 0.75-1.00 | 0.00-0.25 |

---

## UV Remapping Helper

```python
def remap_uv_to_atlas_2x2(u: float, v: float, quadrant: int) -> tuple[float, float]:
    """Remap UV coordinates to a 2x2 atlas quadrant.

    Args:
        u, v: Original UV coordinates [0, 1]
        quadrant: 0=TL, 1=TR, 2=BL, 3=BR

    Returns:
        New (u, v) coordinates
    """
    offsets = [
        (0.0, 0.5),   # Top-left
        (0.5, 0.5),   # Top-right
        (0.0, 0.0),   # Bottom-left
        (0.5, 0.0),   # Bottom-right
    ]

    ox, oy = offsets[quadrant]
    new_u = ox + u * 0.5
    new_v = oy + v * 0.5

    return new_u, new_v


def remap_uv_to_atlas_4x4(u: float, v: float, cell: int) -> tuple[float, float]:
    """Remap UV coordinates to a 4x4 atlas cell.

    Args:
        u, v: Original UV coordinates [0, 1]
        cell: Cell index 0-15 (row-major)

    Returns:
        New (u, v) coordinates
    """
    row = cell // 4
    col = cell % 4

    ox = col * 0.25
    oy = (3 - row) * 0.25  # Flip Y for texture coordinates

    new_u = ox + u * 0.25
    new_v = oy + v * 0.25

    return new_u, new_v
```

---

## Atlas Size Considerations

| Atlas Size | Cell Size (2x2) | Cell Size (4x4) | Best For |
|------------|-----------------|-----------------|----------|
| 256 | 128 | 64 | Low-res props, UI |
| 512 | 256 | 128 | Standard props |
| 1024 | 512 | 256 | Hero assets (use sparingly) |

**VRAM Budget:** ZX has 4MB total VRAM. A 512x512 RGBA atlas uses 1MB.

---

## Multi-Material Mesh Workflow

1. **Design phase:** Assign material IDs to mesh faces
2. **UV mapping:** Map each material region to atlas cell
3. **Generate textures:** Create individual material textures
4. **Pack atlas:** Combine into single atlas per slot
5. **Export:** Save atlas files for nether.toml

```python
# Example workflow for a vehicle with 4 materials
# 1. Generate individual materials
generate_mode2_material("body", (200, 50, 50, 255), 1.0, 0.3)
generate_mode2_material("chrome", (220, 220, 220, 255), 1.0, 0.1)
generate_mode2_material("rubber", (30, 30, 30, 255), 0.0, 0.9)
generate_mode2_material("glass", (200, 220, 255, 255), 0.0, 0.05)

# 2. Pack into atlas
materials = [
    {"albedo": "body_albedo.png", "mre": "body_mre.png"},
    {"albedo": "chrome_albedo.png", "mre": "chrome_mre.png"},
    {"albedo": "rubber_albedo.png", "mre": "rubber_mre.png"},
    {"albedo": "glass_albedo.png", "mre": "glass_mre.png"},
]
pack_material_atlas_2x2(materials, "vehicle", mode=2)

# Results: vehicle_albedo.png, vehicle_mre.png
```
