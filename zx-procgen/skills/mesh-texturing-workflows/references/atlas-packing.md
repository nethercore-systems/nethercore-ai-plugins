# Texture Atlas Packing

Combine multiple textures into a single atlas with UV remapping.

## Atlas Data Structures

```rust
struct AtlasRect {
    x: u32, y: u32,
    width: u32, height: u32,
}

struct TextureAtlas {
    texture: TextureBuffer,
    uv_transforms: Vec<UvTransform>,
    placements: Vec<AtlasRect>,
}

struct UvTransform {
    offset: [f32; 2],
    scale: [f32; 2],
}
```

## Shelf Packing Algorithm

```rust
impl TextureAtlas {
    fn pack(textures: &[&TextureBuffer], padding: u32) -> Self {
        // Sort by height (descending) for better packing
        let mut indices: Vec<usize> = (0..textures.len()).collect();
        indices.sort_by(|&a, &b| textures[b].height.cmp(&textures[a].height));

        // Calculate required atlas size
        let total_area: u32 = textures.iter()
            .map(|t| (t.width + padding) * (t.height + padding))
            .sum();
        let min_size = (total_area as f32).sqrt() as u32;
        let atlas_size = min_size.next_power_of_two().max(256).min(2048);

        let mut atlas = TextureBuffer::new(atlas_size, atlas_size);
        let mut placements = vec![AtlasRect::default(); textures.len()];
        let mut uv_transforms = vec![UvTransform::default(); textures.len()];

        // Shelf packing
        let mut shelf_y = 0u32;
        let mut shelf_height = 0u32;
        let mut x = 0u32;

        for &idx in &indices {
            let tex = textures[idx];
            let w = tex.width + padding;
            let h = tex.height + padding;

            // New shelf if doesn't fit
            if x + w > atlas_size {
                x = 0;
                shelf_y += shelf_height;
                shelf_height = 0;
            }

            if shelf_y + h > atlas_size {
                panic!("Atlas too small for textures");
            }

            // Place texture
            atlas.blit(tex, x, shelf_y);

            placements[idx] = AtlasRect {
                x, y: shelf_y,
                width: tex.width, height: tex.height,
            };

            uv_transforms[idx] = UvTransform {
                offset: [x as f32 / atlas_size as f32, shelf_y as f32 / atlas_size as f32],
                scale: [tex.width as f32 / atlas_size as f32, tex.height as f32 / atlas_size as f32],
            };

            x += w;
            shelf_height = shelf_height.max(h);
        }

        Self { texture: atlas, uv_transforms, placements }
    }

    fn remap_uvs(&self, mesh: &mut MeshUV, atlas_index: usize) {
        let transform = &self.uv_transforms[atlas_index];

        for uv in &mut mesh.uvs {
            uv[0] = uv[0] * transform.scale[0] + transform.offset[0];
            uv[1] = uv[1] * transform.scale[1] + transform.offset[1];
        }
    }
}
```

## Batch Atlasing Multiple Props

```rust
fn create_prop_atlas(props: &[PropAsset]) -> (TextureAtlas, Vec<MeshUV>) {
    let textures: Vec<&TextureBuffer> = props.iter().map(|p| &p.texture).collect();
    let atlas = TextureAtlas::pack(&textures, 2);

    let remapped_meshes: Vec<MeshUV> = props.iter()
        .enumerate()
        .map(|(idx, prop)| {
            let mut mesh = prop.mesh.clone();
            atlas.remap_uvs(&mut mesh, idx);
            mesh
        })
        .collect();

    (atlas, remapped_meshes)
}
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
