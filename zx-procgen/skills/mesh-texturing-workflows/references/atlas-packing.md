# Texture Atlas Packing

Combine multiple textures into a single atlas with UV remapping.

## Atlas Data Structures

```python
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image

@dataclass
class AtlasRect:
    x: int
    y: int
    width: int
    height: int

@dataclass
class UvTransform:
    offset: Tuple[float, float]  # (u_offset, v_offset)
    scale: Tuple[float, float]   # (u_scale, v_scale)

@dataclass
class TextureAtlas:
    texture: np.ndarray           # RGBA array
    uv_transforms: List[UvTransform]
    placements: List[AtlasRect]
```

## Shelf Packing Algorithm

```python
import numpy as np
from PIL import Image
from typing import List

def next_power_of_two(n: int) -> int:
    """Return the smallest power of 2 >= n."""
    return 1 << (n - 1).bit_length() if n > 0 else 1

def pack_textures(textures: List[np.ndarray], padding: int = 2) -> TextureAtlas:
    """Pack multiple textures into a single atlas using shelf packing.

    Args:
        textures: List of RGBA texture arrays
        padding: Padding between textures in pixels

    Returns:
        TextureAtlas with packed texture and UV transforms
    """
    # Get texture dimensions
    tex_sizes = [(tex.shape[1], tex.shape[0]) for tex in textures]  # (width, height)

    # Sort by height (descending) for better packing
    indices = sorted(range(len(textures)), key=lambda i: -tex_sizes[i][1])

    # Calculate required atlas size
    total_area = sum((w + padding) * (h + padding) for w, h in tex_sizes)
    min_size = int(np.sqrt(total_area))
    atlas_size = max(256, min(2048, next_power_of_two(min_size)))

    # Initialize atlas and tracking arrays
    atlas = np.zeros((atlas_size, atlas_size, 4), dtype=np.uint8)
    placements = [AtlasRect(0, 0, 0, 0) for _ in textures]
    uv_transforms = [UvTransform((0, 0), (1, 1)) for _ in textures]

    # Shelf packing
    shelf_y = 0
    shelf_height = 0
    x = 0

    for idx in indices:
        tex = textures[idx]
        h, w = tex.shape[:2]
        padded_w = w + padding
        padded_h = h + padding

        # New shelf if doesn't fit
        if x + padded_w > atlas_size:
            x = 0
            shelf_y += shelf_height
            shelf_height = 0

        if shelf_y + padded_h > atlas_size:
            raise ValueError("Atlas too small for textures")

        # Place texture (blit)
        atlas[shelf_y:shelf_y + h, x:x + w] = tex

        placements[idx] = AtlasRect(x=x, y=shelf_y, width=w, height=h)

        uv_transforms[idx] = UvTransform(
            offset=(x / atlas_size, shelf_y / atlas_size),
            scale=(w / atlas_size, h / atlas_size),
        )

        x += padded_w
        shelf_height = max(shelf_height, padded_h)

    return TextureAtlas(texture=atlas, uv_transforms=uv_transforms, placements=placements)

def remap_uvs(uvs: np.ndarray, transform: UvTransform) -> np.ndarray:
    """Remap UV coordinates using atlas transform.

    Args:
        uvs: Array of shape (N, 2) containing UV coordinates
        transform: UvTransform with offset and scale

    Returns:
        Remapped UV coordinates
    """
    remapped = uvs.copy()
    remapped[:, 0] = uvs[:, 0] * transform.scale[0] + transform.offset[0]
    remapped[:, 1] = uvs[:, 1] * transform.scale[1] + transform.offset[1]
    return remapped
```

## Batch Atlasing Multiple Props

```python
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class PropAsset:
    texture: np.ndarray  # RGBA texture array
    uvs: np.ndarray      # UV coordinates (N, 2)

def create_prop_atlas(props: List[PropAsset]) -> Tuple[TextureAtlas, List[np.ndarray]]:
    """Create texture atlas from multiple props and remap their UVs.

    Args:
        props: List of PropAsset with texture and UV data

    Returns:
        Tuple of (TextureAtlas, list of remapped UV arrays)
    """
    textures = [prop.texture for prop in props]
    atlas = pack_textures(textures, padding=2)

    remapped_uvs = [
        remap_uvs(prop.uvs, atlas.uv_transforms[idx])
        for idx, prop in enumerate(props)
    ]

    return atlas, remapped_uvs
```

## Python Implementation

```python
import numpy as np
from PIL import Image

def create_texture_atlas(textures, padding=2):
    """Pack textures into atlas, return atlas and UV transforms."""
    sorted_texs = sorted(enumerate(textures), key=lambda t: -t[1].height)

    total_area = sum((t.width + padding) * (t.height + padding) for t in textures)
    atlas_size = int(np.ceil(np.sqrt(total_area)))
    atlas_size = 2 ** int(np.ceil(np.log2(atlas_size)))
    atlas_size = max(256, min(2048, atlas_size))

    atlas = np.zeros((atlas_size, atlas_size, 4), dtype=np.uint8)
    transforms = [None] * len(textures)

    shelf_y, shelf_h, x = 0, 0, 0

    for orig_idx, tex in sorted_texs:
        w, h = tex.width + padding, tex.height + padding

        if x + w > atlas_size:
            x, shelf_y, shelf_h = 0, shelf_y + shelf_h, 0

        atlas[shelf_y:shelf_y+tex.height, x:x+tex.width] = np.array(tex)

        transforms[orig_idx] = {
            'offset': [x / atlas_size, shelf_y / atlas_size],
            'scale': [tex.width / atlas_size, tex.height / atlas_size],
        }

        x += w
        shelf_h = max(shelf_h, h)

    return Image.fromarray(atlas), transforms
```
