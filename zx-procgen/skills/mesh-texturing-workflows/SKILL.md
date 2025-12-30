---
name: UV-Aware Texturing and Atlasing Workflows
description: |
  Use this skill for texturing meshes with UV awareness, atlas creation, and UV remapping.

  **Triggers:** "texture character", "UV texture", "texture atlas", "atlas packing", "decal projection", "multi-material mesh", "bake texture", "UV mapping", "texel density"

  **Load references when:**
  - UV bounds/island detection → `references/uv-mapping.md`
  - Character texturing → `references/character-texturing.md`
  - Atlas packing → `references/atlas-packing.md`
  - Decals/wear overlays → `references/decal-projection.md`

  For base texture generation: use `procedural-textures` skill.
  For mesh generation: use `procedural-meshes` skill.
version: 2.0.0
---

# UV-Aware Texturing and Atlasing

Bridge procedural mesh and texture generation with UV-aware workflows.

## Overview

**This skill covers:**
- Reading UV bounds from meshes
- Generating textures mapped to UV regions
- Texture atlas creation and UV remapping
- Character texturing workflows
- Decal and detail projection

**Key principle:** All generation is BUILD-TIME tooling. Output files are bundled into ROM.

## Quick Decision Guide

| Task | Approach | Reference |
|------|----------|-----------|
| Single mesh texture | UV-aware generation | `references/uv-mapping.md` |
| Multiple meshes | Atlas packing | `references/atlas-packing.md` |
| Character skins | Region-based | `references/character-texturing.md` |
| Damage/wear | Decal projection | `references/decal-projection.md` |

## ZX Texture Resolution Guidelines

| Use Case | Resolution | Texel Density |
|----------|------------|---------------|
| Character main | 256x256 | ~64 texels/unit |
| Character detail | 128x128 | ~32 texels/unit |
| Props | 64-128 | ~24-32 texels/unit |
| Terrain tiles | 128x128 | Varies |

## Basic UV Bounds Reading

```rust
struct UvBounds { min_u: f32, max_u: f32, min_v: f32, max_v: f32 }

fn get_uv_bounds(mesh: &MeshUV) -> UvBounds {
    let mut bounds = UvBounds { /* infinity defaults */ };
    for uv in &mesh.uvs {
        bounds.min_u = bounds.min_u.min(uv[0]);
        bounds.max_u = bounds.max_u.max(uv[0]);
        // ... etc
    }
    bounds
}
```

For detailed implementation, see `references/uv-mapping.md`.

## Texture Resolution Calculation

Match texture resolution to mesh detail:

```rust
fn calculate_texture_resolution(mesh: &MeshUV, target_density: f32) -> (u32, u32) {
    let total_area = calculate_surface_area(mesh);
    let uv_coverage = get_uv_bounds(mesh);
    let desired_texels = (total_area * target_density.powi(2)).sqrt();
    let size = (desired_texels / uv_coverage.sqrt()).next_power_of_two().clamp(64, 512);
    (size, size)
}
```

## Character Workflow Summary

```
1. Generate mesh with UVs (procedural-meshes)
2. Calculate texture resolution (64 texels/unit)
3. Identify UV regions (body, head, limbs)
4. Generate albedo (skin + clothing)
5. Generate MRE/SSE (per-region roughness)
6. Export coordinated set
```

See `references/character-texturing.md` for complete workflow.

## Atlas Workflow Summary

```
1. Generate individual textures for props
2. Pack into atlas using shelf algorithm
3. Remap mesh UVs to atlas coordinates
4. Export single atlas + remapped meshes
```

See `references/atlas-packing.md` for packing algorithms.

## nether.toml Integration

```toml
# Character with coordinated textures
[[assets.meshes]]
id = "player"
path = "assets/meshes/player.gltf"

[[assets.textures]]
id = "player_albedo"
path = "assets/textures/player_albedo.png"

# Atlased props (single texture for multiple meshes)
[[assets.textures]]
id = "props_atlas"
path = "assets/textures/props_atlas.png"

[[assets.meshes]]
id = "crate"
path = "assets/meshes/crate.gltf"  # UVs remapped to atlas
```

## References

- `references/uv-mapping.md` - UV bounds, islands, per-island texturing
- `references/character-texturing.md` - Character regions, skin tones
- `references/atlas-packing.md` - Shelf packing, UV remapping
- `references/decal-projection.md` - Decals, wear overlays

## Related Skills

- `procedural-meshes` - Generating meshes with UVs
- `procedural-textures` - Base texture generation
