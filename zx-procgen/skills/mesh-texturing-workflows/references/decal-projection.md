# Decal and Detail Projection

Apply decals, damage, and wear to textures.

## Planar Decal Projection

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

## Damage/Wear Overlay

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

## Wear Intensity Presets

| Intensity | Use Case |
|-----------|----------|
| 0.0-0.1 | New/pristine |
| 0.1-0.3 | Light wear |
| 0.3-0.5 | Moderate use |
| 0.5-0.7 | Heavy wear |
| 0.7-1.0 | Battle-damaged |

## Edge Wear Pattern

Focus wear on convex edges (using mesh curvature):

```rust
fn sample_edge_distance(mesh: &MeshUV, u: f32, v: f32) -> f32 {
    // Find nearest triangle for this UV
    // Calculate curvature at that point
    // Higher curvature = more wear likelihood
    // Returns 0.0 (flat) to 1.0 (sharp edge)
}
```
