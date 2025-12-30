# Character Texturing

Region-based texturing for humanoid characters.

## Character Regions

```python
import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class UvRegion:
    min_uv: Tuple[float, float]
    max_uv: Tuple[float, float]

    def contains(self, u: float, v: float) -> bool:
        """Check if UV coordinate is within this region."""
        return (self.min_uv[0] <= u <= self.max_uv[0] and
                self.min_uv[1] <= v <= self.max_uv[1])

@dataclass
class CharacterRegions:
    body: UvRegion
    head: UvRegion
    left_arm: UvRegion
    right_arm: UvRegion
    left_leg: UvRegion
    right_leg: UvRegion
```

## Region-Based Texture Generation

```python
import numpy as np
from typing import Tuple

def simplex_noise_2d(x: float, y: float) -> float:
    """Simplified noise function (replace with proper implementation)."""
    np.random.seed(int(x * 1000 + y * 100) % 2**31)
    return np.random.random() * 2 - 1

def hex_to_rgba(color: int) -> np.ndarray:
    """Convert hex color (0xRRGGBBAA) to RGBA array."""
    return np.array([
        (color >> 24) & 0xFF,
        (color >> 16) & 0xFF,
        (color >> 8) & 0xFF,
        color & 0xFF,
    ], dtype=np.uint8)

def modulate_color(color: np.ndarray, factor: float) -> np.ndarray:
    """Modulate color brightness by factor."""
    result = color.astype(np.float32)
    result[:3] = np.clip(result[:3] * factor, 0, 255)
    return result.astype(np.uint8)

def apply_face_details(base: np.ndarray, u: float, v: float) -> np.ndarray:
    """Apply subtle face detail variation."""
    noise = simplex_noise_2d(u * 20.0, v * 20.0)
    return modulate_color(base, 1.0 + noise * 0.05)

def apply_clothing_pattern(base: np.ndarray, u: float, v: float) -> np.ndarray:
    """Apply clothing pattern (placeholder - can add patterns)."""
    return base.copy()

def blend_sleeve(skin: np.ndarray, clothing: np.ndarray, u: float, v: float) -> np.ndarray:
    """Blend skin and clothing for sleeve areas."""
    # Simple blend - can make more sophisticated
    blend_factor = 0.5
    result = skin.astype(np.float32) * blend_factor + clothing.astype(np.float32) * (1 - blend_factor)
    return np.clip(result, 0, 255).astype(np.uint8)

def generate_character_texture(
    regions: CharacterRegions,
    skin_color: int,
    clothing_color: int,
    size: int,
) -> np.ndarray:
    """Generate character texture based on UV regions.

    Args:
        regions: CharacterRegions defining body part UV locations
        skin_color: Hex color for skin (0xRRGGBBAA)
        clothing_color: Hex color for clothing (0xRRGGBBAA)
        size: Texture size (width and height)

    Returns:
        RGBA texture array of shape (size, size, 4)
    """
    texture = np.zeros((size, size, 4), dtype=np.uint8)

    skin_rgba = hex_to_rgba(skin_color)
    clothing_rgba = hex_to_rgba(clothing_color)
    transparent = np.array([0, 0, 0, 0], dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            u = x / size
            v = y / size

            if regions.head.contains(u, v):
                color = apply_face_details(skin_rgba, u, v)
            elif regions.body.contains(u, v):
                color = apply_clothing_pattern(clothing_rgba, u, v)
            elif regions.left_arm.contains(u, v) or regions.right_arm.contains(u, v):
                color = blend_sleeve(skin_rgba, clothing_rgba, u, v)
            elif regions.left_leg.contains(u, v) or regions.right_leg.contains(u, v):
                color = clothing_rgba.copy()
            else:
                color = transparent

            texture[y, x] = color

    return texture
```

## Skin Tone Variations

```python
import numpy as np
from typing import List

# Predefined skin tone palette (RGBA format)
SKIN_TONES = [
    0xFFE0BDFF,  # Light
    0xD8A67AFF,  # Medium
    0xC68642FF,  # Tan
    0x8D5524FF,  # Brown
    0x614335FF,  # Dark
]

def generate_skin_texture(regions: CharacterRegions, skin_tone: int, size: int = 256) -> np.ndarray:
    """Generate a skin-only texture for the given regions and tone."""
    texture = np.zeros((size, size, 4), dtype=np.uint8)
    skin_rgba = hex_to_rgba(skin_tone)

    for y in range(size):
        for x in range(size):
            u = x / size
            v = y / size

            # Apply skin to head and arms
            if regions.head.contains(u, v):
                texture[y, x] = apply_face_details(skin_rgba, u, v)
            elif regions.left_arm.contains(u, v) or regions.right_arm.contains(u, v):
                texture[y, x] = skin_rgba

    return texture

def generate_skin_variations(regions: CharacterRegions, count: int, size: int = 256) -> List[np.ndarray]:
    """Generate skin texture variations for different tones.

    Args:
        regions: CharacterRegions from mesh
        count: Number of variations to generate
        size: Texture size

    Returns:
        List of RGBA texture arrays for each skin tone
    """
    return [
        generate_skin_texture(regions, tone, size)
        for tone in SKIN_TONES[:count]
    ]
```

## Complete Character Workflow

```python
import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class CharacterParams:
    height: float
    body_type: str
    skin_color: int
    clothing_color: int

@dataclass
class CharacterAsset:
    positions: np.ndarray    # Mesh vertex positions
    uvs: np.ndarray          # UV coordinates
    albedo: np.ndarray       # Albedo texture
    mre: np.ndarray          # MRE texture (Metallic, Roughness, Emission)

def generate_character_mre(regions: CharacterRegions, size: int) -> np.ndarray:
    """Generate MRE texture for character.

    - R channel: Metallic (0 for skin/cloth)
    - G channel: Roughness (higher for skin, lower for cloth)
    - B channel: Emission (0 for non-emissive)
    """
    mre = np.zeros((size, size, 4), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            u = x / size
            v = y / size

            if regions.head.contains(u, v):
                # Skin: no metal, medium-high roughness
                mre[y, x] = [0, 180, 0, 255]
            elif regions.body.contains(u, v):
                # Clothing: no metal, lower roughness
                mre[y, x] = [0, 120, 0, 255]
            elif regions.left_arm.contains(u, v) or regions.right_arm.contains(u, v):
                # Mix of skin and clothing
                mre[y, x] = [0, 150, 0, 255]
            elif regions.left_leg.contains(u, v) or regions.right_leg.contains(u, v):
                # Pants/clothing
                mre[y, x] = [0, 120, 0, 255]

    return mre

def generate_character_asset(params: CharacterParams) -> CharacterAsset:
    """Generate complete character asset from parameters.

    Args:
        params: CharacterParams with height, body_type, skin/clothing colors

    Returns:
        CharacterAsset with mesh data and textures
    """
    # 1. Generate mesh (placeholder - use actual mesh generation)
    # In practice, call generate_humanoid_mesh_uv(params.height, params.body_type)
    positions = np.zeros((100, 3), dtype=np.float32)
    uvs = np.zeros((100, 2), dtype=np.float32)

    # 2. Calculate resolution (target 64 texels per unit)
    tex_size = 256  # or calculate from mesh

    # 3. Identify regions (placeholder regions)
    regions = CharacterRegions(
        body=UvRegion((0.25, 0.25), (0.75, 0.6)),
        head=UvRegion((0.35, 0.6), (0.65, 0.9)),
        left_arm=UvRegion((0.0, 0.3), (0.25, 0.6)),
        right_arm=UvRegion((0.75, 0.3), (1.0, 0.6)),
        left_leg=UvRegion((0.25, 0.0), (0.45, 0.25)),
        right_leg=UvRegion((0.55, 0.0), (0.75, 0.25)),
    )

    # 4. Generate albedo
    albedo = generate_character_texture(
        regions, params.skin_color, params.clothing_color, tex_size
    )

    # 5. Generate MRE
    mre = generate_character_mre(regions, tex_size)

    return CharacterAsset(
        positions=positions,
        uvs=uvs,
        albedo=albedo,
        mre=mre,
    )
```

## Workflow Steps

```
1. Generate mesh with UVs (procedural-meshes)
   → Body UV island, Head UV island, Clothing UV island

2. Calculate texture resolution
   → 256x256 for main character

3. Identify UV regions
   → Map semantic regions (body, head, limbs)

4. Generate albedo texture
   → Skin gradient in body regions
   → Face details at head coordinates
   → Clothing pattern on clothing island

5. Generate MRE/SSE texture
   → Skin roughness, cloth roughness per region

6. Export coordinated set
   → character_albedo.png
   → character_mre.png
```
