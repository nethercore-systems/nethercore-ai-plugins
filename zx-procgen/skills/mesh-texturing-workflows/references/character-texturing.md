# Character Texturing

Region-based texturing for humanoid characters.

## Character Regions

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

impl UvRegion {
    fn contains(&self, u: f32, v: f32) -> bool {
        u >= self.min_uv[0] && u <= self.max_uv[0] &&
        v >= self.min_uv[1] && v <= self.max_uv[1]
    }
}
```

## Region-Based Texture Generation

```rust
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
                apply_face_details(skin_color, u, v)
            } else if regions.body.contains(u, v) {
                apply_clothing_pattern(clothing_color, u, v)
            } else if regions.left_arm.contains(u, v) || regions.right_arm.contains(u, v) {
                blend_sleeve(skin_color, clothing_color, u, v)
            } else if regions.left_leg.contains(u, v) || regions.right_leg.contains(u, v) {
                clothing_color
            } else {
                0x00000000  // Transparent
            };

            texture.set(x, y, color);
        }
    }

    texture
}

fn apply_face_details(base: u32, u: f32, v: f32) -> u32 {
    let noise = simplex_noise(u * 20.0, v * 20.0);
    modulate_color(base, 1.0 + noise * 0.05)
}
```

## Skin Tone Variations

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

## Complete Character Workflow

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
        &regions, params.skin_color, params.clothing_color, tex_w,
    );

    // 5. Generate MRE
    let mre = generate_character_mre(&regions, tex_w);

    CharacterAsset { mesh, albedo, mre }
}
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
