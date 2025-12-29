---
name: UV-Aware Texturing and Atlasing Workflows
description: This skill should be used when the user asks to "texture character", "UV texture", "texture atlas", "atlas packing", "UV-aware texture", "procedural character texture", "decal projection", "multi-material mesh", "bake texture", "UV mapping", "texture coordinates", "UV unwrap", "atlas generation", "texture regions", "UV islands", "texel density", or mentions texturing procedural meshes, UV-based texture generation, atlas creation, UV remapping, or coordinating textures with mesh UVs. Provides comprehensive guidance for generating textures that work with specific UV layouts and creating texture atlases with UV remapping.
version: 1.0.0
---

# UV-Aware Texturing and Atlasing

## Overview

This skill bridges procedural mesh generation and texture generation by providing workflows for creating textures that match specific UV layouts. Build-time tooling that outputs to Nethercore asset formats.

**This skill covers:**
- Reading UV bounds from meshes
- Generating textures mapped to UV regions
- Texture atlas creation and UV remapping
- Character texturing workflows
- Decal and detail projection

**Key principle:** All procedural generation is BUILD-TIME tooling. Output files (.nczmesh, .ncztex) are bundled into the ROM. Games load pre-built assets at runtime.

## UV-Aware Texture Generation

### Reading UV Bounds

```rust
use glam::Vec2;

struct UvBounds {
    min_u: f32,
    max_u: f32,
    min_v: f32,
    max_v: f32,
}

impl UvBounds {
    fn width(&self) -> f32 { self.max_u - self.min_u }
    fn height(&self) -> f32 { self.max_v - self.min_v }
}

fn get_uv_bounds(mesh: &MeshUV) -> UvBounds {
    let mut bounds = UvBounds {
        min_u: f32::INFINITY,
        max_u: f32::NEG_INFINITY,
        min_v: f32::INFINITY,
        max_v: f32::NEG_INFINITY,
    };

    for uv in &mesh.uvs {
        bounds.min_u = bounds.min_u.min(uv[0]);
        bounds.max_u = bounds.max_u.max(uv[0]);
        bounds.min_v = bounds.min_v.min(uv[1]);
        bounds.max_v = bounds.max_v.max(uv[1]);
    }

    bounds
}
```

### Calculating Texture Resolution

Match texture resolution to mesh detail level:

```rust
fn calculate_texture_resolution(
    mesh: &MeshUV,
    target_texel_density: f32,  // Texels per world unit
) -> (u32, u32) {
    // Calculate world-space surface area
    let mut total_area = 0.0;
    for tri in mesh.triangles.chunks(3) {
        total_area += triangle_area(
            mesh.positions[tri[0] as usize].into(),
            mesh.positions[tri[1] as usize].into(),
            mesh.positions[tri[2] as usize].into(),
        );
    }

    // Calculate UV-space coverage
    let bounds = get_uv_bounds(mesh);
    let uv_coverage = bounds.width() * bounds.height();

    // Desired size based on density
    let desired_texels = (total_area * target_texel_density.powi(2)).sqrt();
    let raw_size = (desired_texels / uv_coverage.sqrt()) as u32;

    // Snap to power of 2, respect ZX limits
    let size = raw_size.next_power_of_two().clamp(64, 512);
    (size, size)
}

fn triangle_area(a: Vec3, b: Vec3, c: Vec3) -> f32 {
    let ab = b - a;
    let ac = c - a;
    ab.cross(ac).length() * 0.5
}
```

### ZX Texture Resolution Guidelines

| Use Case | Resolution | Texel Density |
|----------|------------|---------------|
| Character main | 256x256 | ~64 texels/unit |
| Character detail | 128x128 | ~32 texels/unit |
| Props | 64-128 | ~24-32 texels/unit |
| Terrain tiles | 128x128 | Varies |
| UI elements | 64-256 | Pixel-perfect |

## UV Island Mapping

Identify and work with UV regions (islands):

```rust
struct UvIsland {
    triangle_indices: Vec<usize>,
    min_uv: [f32; 2],
    max_uv: [f32; 2],
    name: Option<String>,  // "body", "head", "clothing", etc.
}

struct UvIslandMapper {
    islands: Vec<UvIsland>,
}

impl UvIslandMapper {
    /// Extract UV islands from mesh (connected UV regions)
    fn from_mesh(mesh: &MeshUV) -> Self {
        let mut visited = vec![false; mesh.triangles.len() / 3];
        let mut islands = Vec::new();

        for tri_idx in 0..mesh.triangles.len() / 3 {
            if visited[tri_idx] { continue; }

            let island = flood_fill_uv_island(mesh, tri_idx, &mut visited);
            islands.push(island);
        }

        Self { islands }
    }

    /// Check if UV coordinate is within an island
    fn island_at(&self, u: f32, v: f32) -> Option<usize> {
        for (idx, island) in self.islands.iter().enumerate() {
            if u >= island.min_uv[0] && u <= island.max_uv[0] &&
               v >= island.min_uv[1] && v <= island.max_uv[1] {
                // Further check: is point inside any triangle?
                if island.contains_uv(u, v) {
                    return Some(idx);
                }
            }
        }
        None
    }
}
```

### Generating Per-Island Textures

```rust
fn generate_island_textured(
    islands: &UvIslandMapper,
    width: u32,
    height: u32,
    materials: &[MaterialGenerator],
) -> TextureBuffer {
    let mut texture = TextureBuffer::new(width, height);

    for y in 0..height {
        for x in 0..width {
            let u = x as f32 / width as f32;
            let v = y as f32 / height as f32;

            if let Some(island_idx) = islands.island_at(u, v) {
                let color = materials[island_idx].sample(u, v);
                texture.set(x, y, color);
            }
        }
    }

    texture
}
```

## Character Texturing Workflow

### Body Region Texturing

```rust
struct CharacterRegions {
    body: UvRegion,
    head: UvRegion,
    left_arm: UvRegion,
    right_arm: UvRegion,
    left_leg: UvRegion,
    right_leg: UvRegion,
}

struct UvRegion {
    min_uv: [f32; 2],
    max_uv: [f32; 2],
}

fn generate_character_texture(
    regions: &CharacterRegions,
    skin_color: u32,
    clothing_color: u32,
    size: u32,
) -> TextureBuffer {
    let mut texture = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            let u = x as f32 / size as f32;
            let v = y as f32 / size as f32;

            let color = if regions.head.contains(u, v) {
                // Face region - add subtle variation
                apply_face_details(skin_color, u, v)
            } else if regions.body.contains(u, v) {
                // Torso - clothing
                apply_clothing_pattern(clothing_color, u, v)
            } else if regions.left_arm.contains(u, v) || regions.right_arm.contains(u, v) {
                // Arms - blend clothing/skin at sleeves
                blend_sleeve(skin_color, clothing_color, u, v)
            } else if regions.left_leg.contains(u, v) || regions.right_leg.contains(u, v) {
                // Legs - pants
                clothing_color
            } else {
                0x00000000  // Transparent (outside UV)
            };

            texture.set(x, y, color);
        }
    }

    texture
}

fn apply_face_details(base: u32, u: f32, v: f32) -> u32 {
    // Add subtle color variation for face
    let noise = simplex_noise(u * 20.0, v * 20.0);
    modulate_color(base, 1.0 + noise * 0.05)
}
```

### Skin Tone Variations

```rust
fn generate_skin_variations(base_mesh: &MeshUV, count: usize) -> Vec<TextureBuffer> {
    let skin_tones = [
        0xFFE0BDFF,  // Light
        0xD8A67AFF,  // Medium
        0xC68642FF,  // Tan
        0x8D5524FF,  // Brown
        0x614335FF,  // Dark
    ];

    let regions = extract_skin_regions(base_mesh);

    skin_tones.iter()
        .take(count)
        .map(|&tone| generate_skin_texture(&regions, tone))
        .collect()
}
```

## Texture Atlas Creation

### Atlas Packing

Combine multiple textures into a single atlas:

```rust
struct AtlasRect {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
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

impl TextureAtlas {
    /// Pack textures using simple shelf algorithm
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

        // Simple shelf packing
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

            // Check if fits vertically
            if shelf_y + h > atlas_size {
                panic!("Atlas too small for textures");
            }

            // Place texture
            atlas.blit(tex, x, shelf_y);

            placements[idx] = AtlasRect {
                x, y: shelf_y,
                width: tex.width,
                height: tex.height,
            };

            uv_transforms[idx] = UvTransform {
                offset: [
                    x as f32 / atlas_size as f32,
                    shelf_y as f32 / atlas_size as f32,
                ],
                scale: [
                    tex.width as f32 / atlas_size as f32,
                    tex.height as f32 / atlas_size as f32,
                ],
            };

            x += w;
            shelf_height = shelf_height.max(h);
        }

        Self { texture: atlas, uv_transforms, placements }
    }

    /// Remap mesh UVs to atlas coordinates
    fn remap_uvs(&self, mesh: &mut MeshUV, atlas_index: usize) {
        let transform = &self.uv_transforms[atlas_index];

        for uv in &mut mesh.uvs {
            uv[0] = uv[0] * transform.scale[0] + transform.offset[0];
            uv[1] = uv[1] * transform.scale[1] + transform.offset[1];
        }
    }
}
```

### Batch Atlasing Multiple Props

```rust
fn create_prop_atlas(props: &[PropAsset]) -> (TextureAtlas, Vec<MeshUV>) {
    // Collect all textures
    let textures: Vec<&TextureBuffer> = props.iter()
        .map(|p| &p.texture)
        .collect();

    // Create atlas
    let atlas = TextureAtlas::pack(&textures, 2);

    // Remap all mesh UVs
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

## Decal and Detail Projection

### Planar Projection for Decals

```rust
fn project_decal(
    mesh: &MeshUV,
    decal: &TextureBuffer,
    projection_origin: Vec3,
    projection_dir: Vec3,
    projection_size: f32,
    target_texture: &mut TextureBuffer,
) {
    let up = Vec3::Y;
    let right = projection_dir.cross(up).normalize();
    let proj_up = right.cross(projection_dir).normalize();

    for y in 0..target_texture.height {
        for x in 0..target_texture.width {
            let u = x as f32 / target_texture.width as f32;
            let v = y as f32 / target_texture.height as f32;

            // Find world position for this UV
            if let Some(world_pos) = uv_to_world(mesh, u, v) {
                // Project onto decal plane
                let to_point = world_pos - projection_origin;
                let dist = to_point.dot(projection_dir);

                // Check if within projection range
                if dist > 0.0 && dist < projection_size {
                    // Calculate decal UV
                    let proj_u = to_point.dot(right) / projection_size + 0.5;
                    let proj_v = to_point.dot(proj_up) / projection_size + 0.5;

                    if proj_u >= 0.0 && proj_u <= 1.0 && proj_v >= 0.0 && proj_v <= 1.0 {
                        let decal_color = decal.sample(proj_u, proj_v);
                        if (decal_color & 0xFF) > 128 {  // Alpha threshold
                            target_texture.set(x, y, decal_color);
                        }
                    }
                }
            }
        }
    }
}
```

### Damage/Wear Overlay

```rust
fn apply_wear_overlay(
    base_texture: &mut TextureBuffer,
    wear_intensity: f32,
    edge_wear: bool,
    mesh: Option<&MeshUV>,
    seed: u64,
) {
    for y in 0..base_texture.height {
        for x in 0..base_texture.width {
            let u = x as f32 / base_texture.width as f32;
            let v = y as f32 / base_texture.height as f32;

            // Generate wear noise
            let noise = fbm_noise(u * 10.0, v * 10.0, 4, seed);
            let wear = if noise > 1.0 - wear_intensity { 1.0 } else { 0.0 };

            // Optional: more wear at edges (using curvature from mesh)
            let edge_factor = if edge_wear {
                mesh.map(|m| sample_edge_distance(m, u, v)).unwrap_or(1.0)
            } else {
                1.0
            };

            if wear * edge_factor > 0.5 {
                let base = base_texture.get(x, y);
                // Darken and desaturate
                let worn = desaturate(darken(base, 0.3), 0.5);
                base_texture.set(x, y, worn);
            }
        }
    }
}
```

## Complete Character Workflow

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

### Integration Code

```rust
fn generate_character_asset(params: CharacterParams) -> CharacterAsset {
    // 1. Generate mesh
    let mesh = generate_humanoid_mesh_uv(params.height, params.body_type);

    // 2. Calculate resolution
    let (tex_w, tex_h) = calculate_texture_resolution(&mesh, 64.0);

    // 3. Identify regions
    let regions = identify_character_regions(&mesh);

    // 4. Generate albedo
    let albedo = generate_character_texture(
        &regions,
        params.skin_color,
        params.clothing_color,
        tex_w,
    );

    // 5. Generate MRE
    let mre = generate_character_mre(&regions, tex_w);

    CharacterAsset { mesh, albedo, mre }
}
```

## nether.toml Integration

```toml
# Character with coordinated textures
[[assets.meshes]]
id = "player"
path = "assets/meshes/player.gltf"

[[assets.textures]]
id = "player_albedo"
path = "assets/textures/player_albedo.png"

[[assets.textures]]
id = "player_mre"
path = "assets/textures/player_mre.png"

# Atlased props (single texture for multiple meshes)
[[assets.textures]]
id = "props_atlas"
path = "assets/textures/props_atlas.png"

[[assets.meshes]]
id = "crate"
path = "assets/meshes/crate.gltf"  # UVs remapped to atlas

[[assets.meshes]]
id = "barrel"
path = "assets/meshes/barrel.gltf"  # UVs remapped to atlas
```

## Python Implementation

```python
import numpy as np
from PIL import Image

def generate_uv_aware_texture(mesh, regions, size=256):
    """Generate texture respecting UV regions."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            u, v = x / size, y / size

            for region_name, region_bounds in regions.items():
                if region_bounds.contains(u, v):
                    color = sample_region_material(region_name, u, v)
                    img[y, x] = color
                    break

    return Image.fromarray(img)


def create_texture_atlas(textures, padding=2):
    """Pack textures into atlas, return atlas and UV transforms."""
    # Sort by height
    sorted_texs = sorted(enumerate(textures), key=lambda t: -t[1].height)

    # Calculate atlas size
    total_area = sum((t.width + padding) * (t.height + padding) for t in textures)
    atlas_size = int(np.ceil(np.sqrt(total_area)))
    atlas_size = 2 ** int(np.ceil(np.log2(atlas_size)))
    atlas_size = max(256, min(2048, atlas_size))

    atlas = np.zeros((atlas_size, atlas_size, 4), dtype=np.uint8)
    transforms = [None] * len(textures)

    # Shelf packing
    shelf_y, shelf_h, x = 0, 0, 0

    for orig_idx, tex in sorted_texs:
        w, h = tex.width + padding, tex.height + padding

        if x + w > atlas_size:
            x, shelf_y, shelf_h = 0, shelf_y + shelf_h, 0

        # Blit texture
        atlas[shelf_y:shelf_y+tex.height, x:x+tex.width] = np.array(tex)

        # Store transform
        transforms[orig_idx] = {
            'offset': [x / atlas_size, shelf_y / atlas_size],
            'scale': [tex.width / atlas_size, tex.height / atlas_size],
        }

        x += w
        shelf_h = max(shelf_h, h)

    return Image.fromarray(atlas), transforms
```

## Additional Resources

### Reference Files

- **`references/uv-projection-techniques.md`** - Planar, cylindrical, spherical projection

### Related Skills

- **`procedural-meshes`** - Generating meshes with UVs
- **`procedural-textures`** - Base texture generation
- **`character-pipeline`** - Complete character workflow
