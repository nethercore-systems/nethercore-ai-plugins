---
name: Procedural Mesh Generation (Blender bpy)
description: This skill should be used when the user asks to "generate mesh", "create 3D model", "procedural geometry", "low-poly model", "blender script", "bpy mesh", "hard surface model", "organic mesh", "metaballs", "skin modifier", "SDF mesh", "mesh modifiers", "UV unwrap", "export glb", "export gltf", or mentions mesh generation, geometry synthesis, Blender scripting, or procedural 3D modeling for game assets.
---

# Procedural Mesh Generation with Blender bpy

Generate game-ready 3D meshes procedurally using Blender in headless mode. All output includes proper UVs and normals for Nethercore ZX.

## Prerequisites: System Blender

This skill requires Blender installed and accessible via the system PATH.

**Check if Blender is available:**
```bash
blender --version
```

**If Blender is not installed:**

| Platform | Installation |
|----------|--------------|
| Windows | Download from [blender.org](https://www.blender.org/download/), install, add to PATH |
| macOS | `brew install --cask blender` or download from blender.org |
| Linux | `sudo apt install blender` or `sudo dnf install blender` or download from blender.org |

**Required version:** Blender 3.0+ (for modern bpy API and glTF 2.0 export)

**Why system Blender?** Headless scripting with `blender --background --python script.py` is the most reliable way to generate production-quality meshes with proper UVs and normals. Python's bpy module is only available within Blender's embedded Python environment.

## Runtime

Execute scripts via headless Blender:

```bash
blender --background --python generator.py
```

## Output Format

- **Primary:** `.glb` (GLTF binary) with embedded UVs and normals
- **Alternative:** `.gltf`, `.obj`, `.fbx` when specified
- **Target aesthetic:** Low-poly/N64/PS1/PS2 era (500-2000 tris typical)

---

## Workflow Decision Tree

Choose the appropriate workflow based on what is being modeled:

```
┌─ What type of mesh?
│
├─► HARD SURFACE (weapons, vehicles, architecture, props, mechanical)
│   └─► Use: Polygon Modeling with bpy primitives + modifiers
│       See: references/bpy-hard-surface.md
│
└─► ORGANIC (characters, creatures, rocks, foliage, blobby shapes)
    │
    ├─► Simple blobby shapes (slimes, eggs, bulbous forms)
    │   └─► Use: Metaballs → convert to mesh
    │       See: references/bpy-organic-workflows.md#metaballs
    │
    ├─► Creatures from stick-figure skeleton
    │   └─► Use: Skin Modifier workflow
    │       See: references/bpy-organic-workflows.md#skin-modifier
    │
    └─► Complex smooth blends (terrain, abstract shapes)
        └─► Use: SDF Pipeline (fogleman/sdf → Blender cleanup)
            See: references/bpy-organic-workflows.md#sdf-pipeline
```

---

## Hard Surface Workflow (Polygon Modeling)

Build mechanical objects from bpy primitives combined with modifiers.

### Core Primitives

| Primitive | bpy Function | Common Use |
|-----------|--------------|------------|
| Cube | `bpy.ops.mesh.primitive_cube_add()` | Crates, buildings, boxes |
| Cylinder | `bpy.ops.mesh.primitive_cylinder_add()` | Barrels, pillars, tubes |
| UV Sphere | `bpy.ops.mesh.primitive_uv_sphere_add()` | Spheres, domes, orbs |
| Cone | `bpy.ops.mesh.primitive_cone_add()` | Spikes, roofs, cones |
| Torus | `bpy.ops.mesh.primitive_torus_add()` | Rings, donuts, wheels |
| Plane | `bpy.ops.mesh.primitive_plane_add()` | Floors, walls, panels |

### Essential Modifiers

| Modifier | Type Constant | Purpose |
|----------|---------------|---------|
| MIRROR | `'MIRROR'` | Symmetric objects (characters, vehicles) |
| BEVEL | `'BEVEL'` | Chamfered edges, rounded corners |
| SOLIDIFY | `'SOLIDIFY'` | Add thickness to flat surfaces |
| ARRAY | `'ARRAY'` | Repeated elements (stairs, chains) |
| BOOLEAN | `'BOOLEAN'` | Combine/subtract shapes (carving) |
| SUBSURF | `'SUBSURF'` | Smoothing (use sparingly for low-poly) |
| DECIMATE | `'DECIMATE'` | Reduce poly count |
| REMESH | `'REMESH'` | Clean up topology |

See `references/bpy-modifiers.md` for detailed modifier usage and parameters.

---

## Organic Workflows

Three approaches for organic shapes, each with specific strengths:

### Metaballs

For blobby, smooth-blending shapes. Fully supported in bpy scripting.

**Element types:** `BALL`, `CAPSULE`, `PLANE`, `ELLIPSOID`, `CUBE`

```python
# Create metaball
mball = bpy.data.metaballs.new("OrganicShape")
mball.resolution = 0.1
mball.render_resolution = 0.05

# Add elements
elem = mball.elements.new()
elem.type = 'BALL'
elem.radius = 1.0

# Convert to mesh when done
bpy.ops.object.convert(target='MESH')
```

### Skin Modifier

Create creatures from vertex skeleton. Ideal for characters defined as stick figures.

```python
# Create armature-like vertex chain
bpy.ops.mesh.primitive_vert_add()
# Extrude to create skeleton shape
bpy.ops.mesh.extrude_region_move(...)

# Apply skin modifier
bpy.ops.object.modifier_add(type='SKIN')
# Adjust skin radii per vertex
```

### SDF Pipeline

For complex smooth blends using `fogleman/sdf` library. Only external dependency.

1. Generate STL with `fogleman/sdf`
2. Import into Blender
3. Clean up with REMESH modifier
4. UV unwrap and export

See `references/bpy-organic-workflows.md` for complete workflow details.

---

## Post-Processing (Required for All Meshes)

Every mesh MUST have these applied before export:

### 1. UV Unwrap

```python
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Choose unwrap method:
bpy.ops.uv.smart_project(angle_limit=66.0)  # General purpose
# OR
bpy.ops.uv.cube_project(cube_size=1.0)      # Box-like objects
# OR
bpy.ops.uv.unwrap(method='ANGLE_BASED')     # Manual seams
```

### 2. Normals

```python
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

# Enable auto-smooth for hard edges
obj.data.use_auto_smooth = True
obj.data.auto_smooth_angle = math.radians(30)

# Fix any inverted normals
bpy.ops.mesh.normals_make_consistent(inside=False)
```

### 3. Cleanup

```python
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Remove doubles
bpy.ops.mesh.remove_doubles(threshold=0.0001)

# Delete loose geometry
bpy.ops.mesh.delete_loose()

# Triangulate for game export
bpy.ops.mesh.quads_convert_to_tris()
```

### 4. Export

```python
bpy.ops.export_scene.gltf(
    filepath="output.glb",
    export_format='GLB',
    export_apply_modifiers=True,
    export_normals=True,
    export_tangents=False,
    export_colors=True
)
```

See `references/bpy-post-processing.md` for complete post-processing patterns.

---

## Console Constraints (Nethercore ZX)

### Triangle Budgets

| Use Case | Triangle Budget |
|----------|-----------------|
| Swarm entities | 50-150 |
| Props | 50-300 |
| Characters | 200-500 |
| Vehicles | 300-800 |
| Hero/close-up | 500-2000 |

### Bone Limits (Animated Meshes)

| Tier | Max Bones |
|------|-----------|
| Simple | 8-12 |
| Standard | 16-24 |
| Complex | 32-48 |

### Texture Resolution

Power-of-2 only: 64, 128, 256, 512

---

## Script Template

```python
#!/usr/bin/env python3
"""
Procedural mesh generator for Nethercore ZX.
Run: blender --background --python generator.py
"""

import bpy
import math
import sys

def clear_scene():
    """Remove default objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def generate_mesh():
    """Generate the mesh - customize this."""
    # Add primitives, apply modifiers
    pass

def post_process(obj):
    """Apply required post-processing."""
    bpy.context.view_layer.objects.active = obj

    # UV unwrap
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0)

    # Cleanup
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.delete_loose()
    bpy.ops.mesh.quads_convert_to_tris()

    # Normals
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(30)

def export(filepath):
    """Export to GLB."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_apply_modifiers=True,
        export_normals=True
    )

def main():
    clear_scene()
    obj = generate_mesh()
    post_process(obj)
    export("output.glb")

if __name__ == "__main__":
    main()
```

---

## nether.toml Integration

```toml
[build]
script = "blender --background --python generator.py && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.meshes]]
id = "barrel"
path = "../assets/meshes/barrel.glb"
```

---

## Reference Files

### Detailed Patterns

- **`references/bpy-primitives.md`** — All bpy primitives with parameters and examples
- **`references/bpy-modifiers.md`** — Complete modifier reference with stacking patterns
- **`references/bpy-organic-workflows.md`** — Metaballs, Skin modifier, SDF pipeline
- **`references/bpy-post-processing.md`** — UV unwrapping, normals, cleanup, export

### Complete Examples

Reference files contain full working scripts for common asset types.

---

## Quality Checklist

Before exporting any mesh:

- [ ] Triangle count within budget for use case
- [ ] UV unwrapped (no overlapping for textured surfaces)
- [ ] Normals consistent (no inverted faces)
- [ ] No loose vertices or edges
- [ ] Triangulated (no quads/ngons)
- [ ] Correct scale (1 unit = 1 meter typical)
- [ ] Origin at logical point (center, base, etc.)
