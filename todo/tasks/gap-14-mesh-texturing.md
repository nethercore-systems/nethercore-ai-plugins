# Gap 14: UV-Aware Texturing & Atlasing

**Status:** `[x]` COMPLETED
**Priority:** MEDIUM
**Plugin:** nethercore-zx-procgen
**Type:** Skill

---

## Problem

Textures and meshes documented separately, integration workflow MISSING. Current skills treat texture generation and mesh generation as independent concerns.

Real workflows need them connected:
- "I generated a character mesh, how do I procedurally texture it?"
- "How do I create a texture atlas for my 10 props?"
- "How do I place a logo on my vehicle's UV layout?"

## What's Missing

### UV-Aware Texture Generation
- Reading mesh UV bounds to size textures correctly
- Generating textures that match specific UV islands (body, face, clothing)
- Painting texture regions based on UV layout
- Seamless tiling across UV seams

### Texture Atlasing
- Combining multiple textures into single atlas
- UV remapping after atlas packing
- Atlas layout optimization (bin packing)
- Shared atlas for multiple meshes (batching)

### Character Texturing Workflows
- Body region texturing (skin gradients, clothing zones)
- Face detail placement (eyes, mouth regions in UV space)
- Procedural clothing patterns on UV islands
- Variation generation (skin tones, outfit colors)

### Decal/Detail Projection
- Projecting details onto UV space
- Logo/emblem placement on vehicles/armor
- Damage/wear overlay generation
- Baked mesh data (AO, curvature, thickness from geometry)

### Multi-Material Workflows
- Different materials for mesh regions (metal armor + cloth + skin)
- Material ID masks from UV regions
- Coordinated MRE/SSE generation per region

## Code Examples

### UV-to-Texture Coordinate Mapping

```rust
/// Read UV bounds from mesh to size texture correctly
pub fn get_uv_bounds(mesh: &Mesh) -> UvBounds {
    let mut min_u = f32::INFINITY;
    let mut max_u = f32::NEG_INFINITY;
    let mut min_v = f32::INFINITY;
    let mut max_v = f32::NEG_INFINITY;

    for uv in &mesh.uvs {
        min_u = min_u.min(uv[0]);
        max_u = max_u.max(uv[0]);
        min_v = min_v.min(uv[1]);
        max_v = max_v.max(uv[1]);
    }

    UvBounds { min_u, max_u, min_v, max_v }
}

/// Calculate optimal texture resolution based on UV space usage and texel density
pub fn calculate_texture_resolution(
    mesh: &Mesh,
    target_texel_density: f32,  // Texels per world unit
) -> (u32, u32) {
    // Calculate world-space surface area
    let mut total_area = 0.0;
    for tri in mesh.triangles() {
        total_area += triangle_area_3d(
            mesh.vertices[tri.0],
            mesh.vertices[tri.1],
            mesh.vertices[tri.2],
        );
    }

    // Calculate UV-space coverage (0-1 range)
    let bounds = get_uv_bounds(mesh);
    let uv_width = bounds.max_u - bounds.min_u;
    let uv_height = bounds.max_v - bounds.min_v;

    // Desired texture size based on target density
    let desired_texels = (total_area * target_texel_density * target_texel_density).sqrt();

    // Account for UV coverage efficiency
    let coverage = uv_width * uv_height;
    let raw_size = (desired_texels / coverage.sqrt()) as u32;

    // Snap to power of 2
    let size = raw_size.next_power_of_two().min(2048);

    (size, size)
}
```

### UV Island Mapping

```rust
/// Map texture coordinates to UV islands
pub struct UvIslandMapper {
    islands: Vec<UvIsland>,
}

impl UvIslandMapper {
    /// Extract UV islands from mesh (connected UV regions)
    pub fn from_mesh(mesh: &Mesh) -> Self {
        let mut visited = vec![false; mesh.triangles().len()];
        let mut islands = vec![];

        for tri_idx in 0..mesh.triangles().len() {
            if visited[tri_idx] { continue; }

            // Flood-fill to find connected island
            let island = flood_fill_island(mesh, tri_idx, &mut visited);
            islands.push(island);
        }

        Self { islands }
    }

    /// Get island containing a UV coordinate
    pub fn island_at(&self, u: f32, v: f32) -> Option<usize> {
        for (idx, island) in self.islands.iter().enumerate() {
            if island.contains(u, v) {
                return Some(idx);
            }
        }
        None
    }

    /// Generate texture with per-island materials
    pub fn generate_textured(
        &self,
        width: u32,
        height: u32,
        island_materials: &[MaterialGenerator],
    ) -> Texture {
        let mut texture = Texture::new(width, height);

        for y in 0..height {
            for x in 0..width {
                let u = x as f32 / width as f32;
                let v = y as f32 / height as f32;

                if let Some(island_idx) = self.island_at(u, v) {
                    let color = island_materials[island_idx].sample(u, v);
                    texture.set_pixel(x, y, color);
                }
            }
        }

        texture
    }
}
```

### Texture Atlas with UV Remapping

```rust
/// Texture atlas with UV remapping
pub struct TextureAtlas {
    pub texture: Texture,
    pub uv_transforms: Vec<UvTransform>,  // Per-source-mesh UV remapping
}

pub struct UvTransform {
    pub offset: [f32; 2],
    pub scale: [f32; 2],
}

impl TextureAtlas {
    /// Create atlas from multiple textures, returning UV transforms
    pub fn pack(textures: &[&Texture], padding: u32) -> Self {
        // Bin packing to arrange textures
        let layout = pack_rectangles(
            textures.iter().map(|t| (t.width + padding, t.height + padding)).collect()
        );

        // Calculate atlas size (power of 2)
        let atlas_width = layout.total_width.next_power_of_two();
        let atlas_height = layout.total_height.next_power_of_two();

        let mut atlas = Texture::new(atlas_width, atlas_height);
        let mut uv_transforms = vec![];

        for (idx, placement) in layout.placements.iter().enumerate() {
            // Copy texture to atlas
            atlas.blit(textures[idx], placement.x, placement.y);

            // Calculate UV transform for this texture
            uv_transforms.push(UvTransform {
                offset: [
                    placement.x as f32 / atlas_width as f32,
                    placement.y as f32 / atlas_height as f32,
                ],
                scale: [
                    textures[idx].width as f32 / atlas_width as f32,
                    textures[idx].height as f32 / atlas_height as f32,
                ],
            });
        }

        Self { texture: atlas, uv_transforms }
    }

    /// Remap mesh UVs to atlas coordinates
    pub fn remap_uvs(&self, mesh: &mut Mesh, atlas_index: usize) {
        let transform = &self.uv_transforms[atlas_index];

        for uv in &mut mesh.uvs {
            uv[0] = uv[0] * transform.scale[0] + transform.offset[0];
            uv[1] = uv[1] * transform.scale[1] + transform.offset[1];
        }
    }
}
```

### Example Workflow (Character)

```
1. Generate character mesh with UVs (procedural-meshes)
   → Body UV island, Head UV island, Clothing UV island

2. Generate UV-aware textures (NEW skill)
   → Skin gradient mapped to body island bounds
   → Face details at head island coordinates
   → Fabric pattern on clothing island

3. Generate material maps (procedural-textures)
   → MRE with skin roughness, cloth roughness, metal armor

4. Export coordinated set
   → character_albedo.png (all regions)
   → character_mre.png (material properties per region)
```

## Prompt for Implementation

```
Add skill "mesh-texturing-workflows" to nethercore-zx-procgen. Triggers: "texture
character", "UV texture", "texture atlas", "atlas packing", "UV-aware texture",
"procedural character texture", "decal projection", "multi-material mesh", "bake
texture". Cover: UV-aware generation (reading UV bounds, painting UV regions),
atlasing (bin packing, UV remapping), character workflows (body zones, face regions,
clothing), decal projection, baked maps (AO from geometry). Integration: uses
procedural-meshes for UV data, procedural-textures for generation.

IMPORTANT: ZX is WASM-based. Procedural generation is BUILD-TIME tooling that
outputs to Nethercore formats (.nczmesh, .ncztex). Include examples using Rust
CLI tools or any language that can output PNG/OBJ files, which are then converted
via nether-export. NOT runtime Python. ~1500 words.
```

## Technical Notes

**Build-time vs Runtime:** All procedural asset generation happens BEFORE the game
runs. The output files (.nczmesh, .ncztex, .nczsnd) are bundled into the ROM via
nether.toml. Games do NOT generate meshes/textures at runtime - they load pre-built
assets via `rom_texture()`, `rom_mesh()`, etc.

**FFI Reference:** See `nethercore/include/zx.rs` for asset loading functions:
- `rom_texture(id_ptr, id_len)` - Load texture from ROM data pack
- `rom_mesh(id_ptr, id_len)` - Load mesh from ROM data pack
- `load_texture(width, height, pixels_ptr)` - Load from WASM memory (embedded assets)

## Dependencies

- None (uses existing procedural-meshes and procedural-textures)

## Related Gaps

- Gap 15 (Character Pipeline) uses this for character texturing
- Gap 24 (2D Sprites) for 2D atlas workflows
