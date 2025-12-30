# UV Mapping and Island Detection

Working with mesh UV coordinates for texture generation.

## UV Bounds

```rust
use glam::Vec2;

struct UvBounds {
    min_u: f32, max_u: f32,
    min_v: f32, max_v: f32,
}

impl UvBounds {
    fn width(&self) -> f32 { self.max_u - self.min_u }
    fn height(&self) -> f32 { self.max_v - self.min_v }
}

fn get_uv_bounds(mesh: &MeshUV) -> UvBounds {
    let mut bounds = UvBounds {
        min_u: f32::INFINITY, max_u: f32::NEG_INFINITY,
        min_v: f32::INFINITY, max_v: f32::NEG_INFINITY,
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

## Texture Resolution Calculation

Match resolution to mesh detail level:

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

## UV Island Detection

Identify connected UV regions:

```rust
struct UvIsland {
    triangle_indices: Vec<usize>,
    min_uv: [f32; 2],
    max_uv: [f32; 2],
    name: Option<String>,  // "body", "head", etc.
}

struct UvIslandMapper {
    islands: Vec<UvIsland>,
}

impl UvIslandMapper {
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

    fn island_at(&self, u: f32, v: f32) -> Option<usize> {
        for (idx, island) in self.islands.iter().enumerate() {
            if u >= island.min_uv[0] && u <= island.max_uv[0] &&
               v >= island.min_uv[1] && v <= island.max_uv[1] {
                if island.contains_uv(u, v) {
                    return Some(idx);
                }
            }
        }
        None
    }
}
```

## Per-Island Texture Generation

```rust
fn generate_island_textured(
    islands: &UvIslandMapper,
    width: u32, height: u32,
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
