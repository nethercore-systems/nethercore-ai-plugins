# Mesh Modifiers Reference

Modifiers transform meshes procedurally. Apply them in sequence to build complex geometry from simple primitives.

## Transform Modifiers

### Translate
Move mesh in 3D space.
- **Parameters:** x, y, z offset
- **Use for:** Positioning parts before combining

### Rotate
Rotate mesh around an axis.
- **Parameters:** axis (X/Y/Z), angle in radians
- **Use for:** Orienting parts, creating variations

### Scale
Resize mesh uniformly or per-axis.
- **Parameters:** x, y, z scale factors
- **Use for:** Proportions, squash and stretch

---

## Subdivision Modifiers

### Subdivide (Midpoint)
Split each triangle into 4 smaller triangles.
- **Parameters:** iterations (1-3 typical)
- **Effect:** Each iteration quadruples triangle count
- **Use for:** Smoothing low-poly shapes, adding detail

**Triangle count growth:**
| Iterations | Multiplier |
|------------|------------|
| 1 | 4x |
| 2 | 16x |
| 3 | 64x |

### Catmull-Clark (if available)
Smooth subdivision with proper edge weighting.
- **Use for:** Organic shapes, character bodies

---

## Displacement Modifiers

### Noise Displacement

Add organic surface variation using noise functions.

**Parameters:**
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Amplitude | How far vertices move | 0.01-0.1 |
| Frequency | Noise detail scale | 1.0-5.0 |
| Octaves | Noise complexity | 1-4 |
| Seed | Reproducibility | Any integer |
| Direction | Normal, Radial, or Axis | Normal (default) |

**Presets:**
- **Subtle:** amplitude=0.02, frequency=2.0, octaves=2 (slight wear)
- **Weathered:** amplitude=0.05, frequency=3.0, octaves=3 (heavy damage)
- **Organic:** amplitude=0.08, frequency=1.5, octaves=4 (natural forms)

**Algorithm (pseudocode):**
```
for each vertex:
    noise_value = perlin_noise(vertex.position * frequency, octaves, seed)
    offset = vertex.normal * noise_value * amplitude
    vertex.position += offset
```

### Twist
Rotate vertices progressively along an axis.
- **Parameters:** axis, angle, center position
- **Use for:** Spiral shapes, organic twisting

### Taper
Scale progressively along an axis.
- **Parameters:** axis, factor (0=point, 1=unchanged), center
- **Use for:** Cones, tapered cylinders, carrots

### Bulge
Inflate or deflate radially.
- **Parameters:** amount, axis, falloff
- **Use for:** Barrel shapes, organic swelling

---

## Symmetry Modifiers

### Mirror
Duplicate mesh reflected across a plane.
- **Parameters:** axis (X/Y/Z), merge threshold
- **Use for:** Symmetric models (characters, vehicles)

**Workflow:**
1. Model one half
2. Apply mirror
3. Weld vertices at the seam

---

## Detail Generators (Industrial/Sci-Fi)

### Rivets
Add rivet/bolt details to flat surfaces.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Density | Rivets per unit area (0.05-0.2) |
| Radius | Rivet head size |
| Height | Protrusion amount |
| Pattern | Grid, Hexagonal, Random, EdgeOnly |

**Algorithm:**
1. Find flat faces (normal pointing outward)
2. Distribute points on face using pattern
3. Add small sphere/cylinder at each point

### Panel Lines
Create recessed panel seams.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Spacing | Distance between lines |
| Depth | How deep the groove cuts |
| Width | Line thickness |
| Direction | Horizontal, Vertical, or Both |

**Algorithm:**
1. Create grid of line positions
2. For each line, push nearby vertices inward
3. Optionally add edge loops for sharper definition

### Greebles
Add small tech details (boxes, cylinders, vents).

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Density | Coverage amount (0.1-0.5) |
| Size range | Min/max greeble size |
| Types | Box, Cylinder, Vent, Antenna |

**Use for:** Sci-fi surfaces, machinery, space ships

### Bolts
Add bolt head details.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Density | Bolts per unit area |
| Radius | Bolt head size |
| Head type | Hex, Phillips, Slotted, Allen |

---

## Normal Modifiers

### Smooth Normals
Average normals across shared vertices for smooth shading.
- **Use for:** Organic shapes, curved surfaces

### Flat Normals
Use face normal for all vertices in each face.
- **Use for:** Faceted look, low-poly style, hard surface

### Recalculate Normals
Recompute all normals from geometry (fixes inverted faces).
- **Use for:** After combining meshes, fixing import issues

---

## UV Modifiers

### Pixel Snap UVs
Align UV coordinates to texture pixel boundaries.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Resolution | Texture size (64, 128, 256, 512) |
| Half-pixel offset | Center UVs on pixels (true/false) |

**Why it matters:**
- Prevents texture bleeding at edges
- Cleaner pixel art look
- Required for retro aesthetic

**Algorithm:**
```
for each uv:
    uv.x = round(uv.x * resolution) / resolution
    uv.y = round(uv.y * resolution) / resolution
    if half_pixel_offset:
        uv.x += 0.5 / resolution
        uv.y += 0.5 / resolution
```

### Normalize Texel Density
Make texture density consistent across the mesh.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Target density | Texels per world unit (128-512) |

**Why it matters:**
- Large faces don't look blurry
- Small faces don't waste texture space
- Professional, consistent look

---

## Cleanup Modifiers

### Weld Vertices
Merge vertices within a threshold distance.
- **Parameters:** threshold (0.001 typical)
- **Use for:** Closing seams after combine/mirror

### Remove Doubles
Eliminate duplicate vertices.
- **Use for:** Cleaning imported meshes

### Triangulate
Convert quads/n-gons to triangles.
- **Required for:** ZX export (triangles only)

---

## Modifier Order (Best Practice)

Apply modifiers in this order for best results:

```
1. Subdivision (if needed)
2. Displacement/deformation
3. Detail generators (rivets, greebles)
4. Vertex color baking (AO, curvature, lighting)
5. Normal recalculation
6. UV pixel snapping
7. Weld/cleanup
```

---

## Language Examples

### Rust (proc-gen)

```rust
use proc_gen::mesh::*;

let mut mesh = generate_cube_uv(1.0, 1.0, 1.0);
mesh.apply(Subdivide { iterations: 1 });
mesh.apply(NoiseDisplace::subtle(42));
mesh.apply(AddRivets { pattern: RivetPattern::EdgeOnly, ..Default::default() });
mesh.apply(BakeVertexAO::default());
mesh.apply(SmoothNormals);
mesh.apply(PixelSnapUVs { resolution: 256, half_pixel_offset: true });
```

### Python (trimesh + custom)

```python
import trimesh
import numpy as np

mesh = trimesh.primitives.Box()

# Subdivision
mesh = mesh.subdivide()

# Noise displacement
noise = perlin_3d(mesh.vertices, frequency=3.0, seed=42)
mesh.vertices += mesh.vertex_normals * noise[:, np.newaxis] * 0.02

# Smooth normals
mesh.fix_normals()
```

### Conceptual (any language)

```
mesh = generate_cube(1.0, 1.0, 1.0)
mesh = subdivide(mesh, iterations=1)
mesh = noise_displace(mesh, amplitude=0.02, frequency=3.0)
mesh = add_rivets(mesh, density=0.1, pattern="edge_only")
mesh = bake_vertex_ao(mesh, ray_count=32)
mesh = recalculate_normals(mesh, smooth=true)
mesh = snap_uvs_to_pixels(mesh, resolution=256)
```

---

## Complete Industrial Asset Example

```
# Create a sci-fi crate
mesh = generate_cube(1.0, 0.8, 1.0)

# Subdivide for detail
mesh = subdivide(mesh, iterations=1)

# Add surface wear
mesh = noise_displace(mesh, amplitude=0.015, frequency=3.0, seed=42)

# Industrial details
mesh = add_panel_lines(mesh, spacing=0.3, depth=0.005)
mesh = add_rivets(mesh, pattern="edge_only", density=0.15)

# Bake vertex colors for PS1/N64 quality
mesh = bake_vertex_ao(mesh, ray_count=32)
mesh = bake_directional_light(mesh,
    direction=[0.5, -0.8, 0.3],
    light_color=[255, 250, 240],
    shadow_color=[80, 70, 90])

# Finalize
mesh = smooth_normals(mesh)
mesh = snap_uvs_to_pixels(mesh, resolution=256)
```
