# Vertex Colors

Per-vertex colors multiply with material/texture colors. This is THE signature technique for achieving PS1/PS2/N64 quality assets - professional retro games used extensively baked vertex lighting.

## Why Vertex Colors Matter

Vertex colors were the primary shading technique for 5th-gen consoles because:
- No per-pixel lighting calculations needed
- Baked lighting looks consistent across hardware
- Adds depth and visual interest without texture complexity
- Creates the characteristic "warm shadows" look of the era

## Core Techniques

### 1. Ambient Occlusion Baking

**What it does:** Darkens vertices in crevices and corners where ambient light can't reach.

**How it works:**
1. For each vertex, cast rays in a hemisphere aligned to the vertex normal
2. Count how many rays hit nearby geometry
3. More hits = darker (less ambient light reaches the vertex)

**Parameters:**
| Parameter | Typical Value | Effect |
|-----------|---------------|--------|
| Ray count | 32-64 | Quality vs speed tradeoff |
| Max distance | 0.3-1.0 | How far to check for occlusion |
| Falloff | Linear/Quadratic | How darkness fades with distance |

**Algorithm (pseudocode):**
```
for each vertex:
    ao_value = 0
    for i in range(ray_count):
        direction = random_hemisphere_direction(vertex.normal)
        if ray_hits_geometry(vertex.position, direction, max_distance):
            ao_value += 1

    vertex.color.r = 255 - (ao_value / ray_count * 255)
```

### 2. Curvature-Based Coloring

**What it does:** Detects edges (convex) and corners (concave) for wear effects.

**Why it's important:**
- Edges wear first in real life (paint chips, metal scratches)
- Corners collect dirt and grime
- Creates realistic weathering distribution

**How it works:**
1. Calculate average normal of neighboring vertices
2. Compare to current vertex normal
3. Large difference = edge (convex) or corner (concave)

**Algorithm (pseudocode):**
```
for each vertex:
    neighbor_normal = average(neighbors.normals)
    curvature = dot(vertex.normal, neighbor_normal)

    if curvature < 0:  # Concave (corner)
        vertex.color.g = map(curvature, -1, 0, 0, 128)
    else:  # Convex (edge)
        vertex.color.g = map(curvature, 0, 1, 128, 255)
```

### 3. Directional Light Baking

**What it does:** Pre-calculates lighting from a key light direction.

**Why it's important:**
- Creates dramatic shading without runtime cost
- Consistent look across all view angles
- Classic "hand-painted" quality of retro games

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Direction | Light direction vector (e.g., [0.5, -0.8, 0.3]) |
| Light color | Color for lit areas |
| Shadow color | Color for shadowed areas |
| Ambient | Base lighting contribution (0.2-0.4) |
| Wrap | Soft shadow wrap amount (0-0.5) |

**Algorithm (pseudocode):**
```
for each vertex:
    ndotl = dot(vertex.normal, -light_direction)
    ndotl = (ndotl + wrap) / (1 + wrap)  # Wrap lighting
    ndotl = clamp(ndotl, 0, 1)

    lit = ndotl * (1 - ambient) + ambient
    vertex.color = lerp(shadow_color, light_color, lit)
```

## The Complete PS1/N64 Quality Pipeline

For professional retro-quality assets, apply these techniques in order:

```
1. Generate base mesh
2. Apply displacement for organic feel
3. Bake ambient occlusion → Red channel
4. Bake curvature → Green channel
5. Bake directional light → Multiply with existing
6. Snap UVs to pixel grid
```

## Channel Usage Convention

| Channel | Data | Range |
|---------|------|-------|
| R | Ambient Occlusion | 0 (dark) - 255 (lit) |
| G | Curvature | 0 (concave) - 128 (flat) - 255 (convex) |
| B | Custom/Reserved | User-defined |
| A | Opacity or mask | 0 (transparent) - 255 (opaque) |

## Language Examples

### Rust (proc-gen)

```rust
use proc_gen::mesh::*;

let mut mesh = generate_cube_uv(1.0, 1.0, 1.0);
mesh.apply(BakeVertexAO::default());
mesh.apply(BakeVertexCurvature::default());
mesh.apply(BakeDirectionalLight {
    direction: [0.5, -0.8, 0.3],
    light_color: [255, 250, 240, 255],
    shadow_color: [80, 70, 90, 255],
    ..Default::default()
});
```

### Python (custom)

```python
import numpy as np

def bake_ao(mesh, ray_count=32, max_dist=0.5):
    colors = np.ones((len(mesh.vertices), 4), dtype=np.uint8) * 255

    for i, (pos, normal) in enumerate(zip(mesh.vertices, mesh.normals)):
        hits = 0
        for _ in range(ray_count):
            direction = random_hemisphere(normal)
            if mesh.ray_intersects(pos + normal * 0.001, direction, max_dist):
                hits += 1

        ao = 1.0 - (hits / ray_count)
        colors[i, 0] = int(ao * 255)

    return colors
```

### Conceptual (any language)

```
function bake_vertex_ao(mesh):
    for each vertex in mesh:
        occlusion = calculate_hemisphere_occlusion(vertex, ray_count=32)
        vertex.color.red = (1 - occlusion) * 255
    return mesh

function bake_curvature(mesh):
    for each vertex in mesh:
        curvature = calculate_local_curvature(vertex, neighbors)
        vertex.color.green = map_to_byte(curvature)
    return mesh
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too few AO rays | Noisy, spotty results | Use at least 32 rays |
| Wrong max distance | Either no effect or everything dark | Scale to mesh size (~0.3-1.0 world units) |
| Baking after UV snap | UVs get messed up | Always bake colors first, snap UVs last |
| Ignoring curvature | Missing edge wear | Always bake curvature for weathered assets |
| Single color channel | Can't combine effects | Use different channels for different data |

## Integration with Textures

Vertex colors multiply with textures in the shader:

```
final_color = texture_color * vertex_color * material_tint
```

This means:
- White vertex (255,255,255) = texture unchanged
- Gray vertex (128,128,128) = texture at 50% brightness
- Black vertex (0,0,0) = completely dark

Use this to your advantage - paint AO in vertex colors and let the texture provide the detail.
