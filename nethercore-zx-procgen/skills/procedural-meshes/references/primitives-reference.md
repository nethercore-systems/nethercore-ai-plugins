# Mesh Primitives Reference

Procedural mesh primitives for 3D asset generation. All primitives are language-agnostic and can be implemented in any language.

## Core Primitives

### Cube / Box

Axis-aligned box with configurable dimensions.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| size_x | Width (X axis) |
| size_y | Height (Y axis) |
| size_z | Depth (Z axis) |

**Triangle count:** 12 (fixed)

**Algorithm:**
- 8 vertices at corners
- 6 faces with 2 triangles each
- For UV mapping: unwrap each face independently

---

### Sphere

Latitude/longitude sphere (UV sphere).

**Parameters:**
| Parameter | Description | Range |
|-----------|-------------|-------|
| radius | Sphere size | Any positive |
| segments | Horizontal divisions | 8-32 |
| rings | Vertical divisions | 4-16 |

**Triangle count:** `segments × rings × 2` (approximately)

**Algorithm (pseudocode):**
```
for ring in range(rings + 1):
    phi = PI * ring / rings  # 0 to PI

    for segment in range(segments):
        theta = 2 * PI * segment / segments  # 0 to 2*PI

        x = radius * sin(phi) * cos(theta)
        y = radius * cos(phi)
        z = radius * sin(phi) * sin(theta)

        add_vertex(x, y, z)

        # UV coordinates
        u = segment / segments
        v = ring / rings
```

---

### Cylinder

Cylinder with configurable top and bottom radii.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| radius_bottom | Bottom cap radius |
| radius_top | Top cap radius |
| height | Height |
| segments | Circumference divisions (8-24) |

**Triangle count:** `segments × 4 + segments × 2` (sides + caps)

**Variations:**
- Cone: `radius_top = 0`
- Tube: No caps (open ends)
- Tapered: Different top/bottom radii

---

### Capsule

Cylinder with hemispherical caps.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| radius | Hemisphere and cylinder radius |
| height | Total height (including caps) |
| segments | Circumference divisions |
| rings | Hemisphere ring count |

**Triangle count:** Complex (hemisphere + cylinder)

**Use for:** Characters, projectiles, collision primitives

---

### Torus

Donut shape.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| major_radius | Distance from center to tube center |
| minor_radius | Tube radius |
| major_segments | Divisions around major circle |
| minor_segments | Divisions around tube |

**Triangle count:** `major_segments × minor_segments × 2`

**Algorithm (pseudocode):**
```
for i in range(major_segments):
    theta = 2 * PI * i / major_segments

    for j in range(minor_segments):
        phi = 2 * PI * j / minor_segments

        x = (major_radius + minor_radius * cos(phi)) * cos(theta)
        y = minor_radius * sin(phi)
        z = (major_radius + minor_radius * cos(phi)) * sin(theta)

        add_vertex(x, y, z)
```

---

### Plane / Quad

Flat rectangular surface.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| size_x | Width |
| size_z | Depth |
| subdivisions_x | X axis divisions |
| subdivisions_z | Z axis divisions |

**Triangle count:** `subdivisions_x × subdivisions_z × 2`

**Use for:** Floors, walls, terrains, UI elements

---

## Triangle Count Reference

| Primitive | Low Poly | Medium | High Poly | Use Case |
|-----------|----------|--------|-----------|----------|
| Cube | 12 | 12 | 12 | Crates, buildings |
| Sphere (8×4) | 64 | - | - | Particles, distant |
| Sphere (12×8) | - | 192 | - | Props, NPCs |
| Sphere (24×12) | - | - | 576 | Hero objects |
| Cylinder (8) | 28 | - | - | Simple props |
| Cylinder (16) | - | 60 | - | Standard props |
| Capsule (8×2) | 48 | - | - | Crowds |
| Capsule (12×4) | - | 160 | - | Characters |
| Torus (12×6) | 144 | - | - | Rings, wheels |
| Torus (24×12) | - | - | 576 | Detailed torus |

---

## Recommended Parameters by Use Case

### Low Poly (Swarm/Crowd objects: 50-100 tris)
```
sphere(radius, segments=8, rings=4)       # 64 tris
cube(size)                                 # 12 tris
capsule(radius, height, segments=6, rings=2)  # ~48 tris
```

### Medium Poly (Characters/Props: 150-300 tris)
```
sphere(radius, segments=12, rings=8)      # ~192 tris
cylinder(r, r, height, segments=12)       # ~60 tris
capsule(radius, height, segments=12, rings=4)  # ~160 tris
```

### High Poly (Hero Objects: 400-800 tris)
```
sphere(radius, segments=24, rings=12)     # ~576 tris
torus(major, minor, major_segs=24, minor_segs=12)  # ~576 tris
capsule(radius, height, segments=24, rings=8)  # ~576 tris
```

---

## UV Mapping

All primitives should support UV-mapped variants for texturing.

### Cube UV Layout
- 6 separate faces, each occupying 1/6 of texture space
- Or: cross/T layout for connected unwrap

### Sphere UV Layout
- Equirectangular projection
- Poles may have UV distortion (expected)

### Cylinder UV Layout
- Side: rectangular unwrap
- Caps: circular projection

---

## Coordinate System

**Standard (Y-up, right-handed):**
- Y is up
- X is right
- Z is forward (toward viewer)

**Primitive origins:**
| Primitive | Origin |
|-----------|--------|
| Cube | Center |
| Sphere | Center |
| Cylinder | Bottom center (Y=0 to Y=height) |
| Capsule | Center |
| Torus | Center |
| Plane | Center (in XZ plane, Y=0) |

---

## Language Examples

### Rust (proc-gen)

```rust
use proc_gen::mesh::*;

// Basic primitives
let cube: UnpackedMesh = generate_cube(1.0, 1.0, 1.0);
let sphere: UnpackedMesh = generate_sphere(1.0, 16, 8);
let cylinder: UnpackedMesh = generate_cylinder(0.5, 0.5, 2.0, 12);

// UV-mapped variants
let cube_uv: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);
let sphere_uv: UnpackedMeshUV = generate_sphere_uv(1.0, 16, 8);
```

### Python (trimesh)

```python
import trimesh
import numpy as np

# Primitives via trimesh
cube = trimesh.primitives.Box(extents=[1.0, 1.0, 1.0])
sphere = trimesh.primitives.Sphere(radius=1.0, subdivisions=2)
cylinder = trimesh.primitives.Cylinder(radius=0.5, height=2.0)
capsule = trimesh.primitives.Capsule(radius=0.5, height=1.0)

# Custom sphere with specific segment count
def generate_sphere(radius, segments, rings):
    vertices = []
    faces = []

    for ring in range(rings + 1):
        phi = np.pi * ring / rings
        for seg in range(segments):
            theta = 2 * np.pi * seg / segments
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.cos(phi)
            z = radius * np.sin(phi) * np.sin(theta)
            vertices.append([x, y, z])

    # Generate faces...
    return trimesh.Trimesh(vertices=vertices, faces=faces)
```

### JavaScript (Three.js)

```javascript
import * as THREE from 'three';

// Built-in geometries
const cube = new THREE.BoxGeometry(1, 1, 1);
const sphere = new THREE.SphereGeometry(1, 16, 8);
const cylinder = new THREE.CylinderGeometry(0.5, 0.5, 2, 12);
const torus = new THREE.TorusGeometry(1, 0.3, 12, 24);
const plane = new THREE.PlaneGeometry(2, 2, 4, 4);
const capsule = new THREE.CapsuleGeometry(0.5, 1, 4, 12);
```

### Conceptual (any language)

```
cube = generate_cube(width=1, height=1, depth=1)
sphere = generate_sphere(radius=1, segments=16, rings=8)
cylinder = generate_cylinder(radius_bottom=0.5, radius_top=0.5, height=2, segments=12)
capsule = generate_capsule(radius=0.5, height=1, segments=12, rings=4)
torus = generate_torus(major_radius=1, minor_radius=0.3, major_segs=24, minor_segs=12)
plane = generate_plane(width=2, depth=2, subdiv_x=4, subdiv_z=4)
```
