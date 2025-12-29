# Blender bpy Organic Workflows

Three workflows for creating organic shapes: Metaballs, Skin Modifier, and SDF Pipeline. Choose based on shape complexity and workflow preference.

## Workflow Comparison

| Workflow | Best For | Pros | Cons |
|----------|----------|------|------|
| **Metaballs** | Blobby shapes, slimes, eggs | Simple API, smooth blends | Limited control, no sharp edges |
| **Skin Modifier** | Creatures from skeleton | Intuitive, good topology | Manual radius adjustment |
| **SDF Pipeline** | Complex blends, terrain | Powerful operations, smooth | External library, extra step |

---

## Metaballs

Metaballs (isosurfaces) create smooth, blobby shapes that naturally blend together. Fully supported in bpy — NOT deprecated.

### Element Types

| Type | Shape | Use Case |
|------|-------|----------|
| `BALL` | Sphere | General blobs, limbs |
| `CAPSULE` | Pill/Cylinder | Elongated parts, limbs |
| `PLANE` | Flat disc | Flat organic areas |
| `ELLIPSOID` | Stretched sphere | Eggs, bodies |
| `CUBE` | Rounded cube | Blocky organic shapes |

### Basic Metaball Creation

```python
import bpy

def create_metaball_mesh(name="OrganicShape"):
    """Create a metaball object and convert to mesh."""
    # Create metaball data
    mball = bpy.data.metaballs.new(name)
    mball.resolution = 0.1        # Viewport resolution (lower = denser)
    mball.render_resolution = 0.05  # Final resolution
    mball.threshold = 1.0         # Isosurface threshold

    # Create metaball object
    mball_obj = bpy.data.objects.new(name, mball)
    bpy.context.collection.objects.link(mball_obj)
    bpy.context.view_layer.objects.active = mball_obj

    return mball, mball_obj

def add_element(mball, elem_type='BALL', location=(0, 0, 0), radius=1.0):
    """Add an element to a metaball."""
    elem = mball.elements.new()
    elem.type = elem_type
    elem.co = location
    elem.radius = radius
    return elem
```

### Complete Example: Slime Creature

```python
#!/usr/bin/env python3
"""Generate a slime creature using metaballs."""

import bpy
import math
import random

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_slime(seed=42):
    """Create a blobby slime creature."""
    random.seed(seed)

    # Create metaball
    mball = bpy.data.metaballs.new("Slime")
    mball.resolution = 0.08
    mball.render_resolution = 0.04
    mball.threshold = 1.0

    mball_obj = bpy.data.objects.new("Slime", mball)
    bpy.context.collection.objects.link(mball_obj)
    bpy.context.view_layer.objects.active = mball_obj

    # Main body (large ball)
    body = mball.elements.new()
    body.type = 'BALL'
    body.co = (0, 0, 0.5)
    body.radius = 1.0

    # Add random bumps
    for i in range(5):
        bump = mball.elements.new()
        bump.type = 'BALL'
        angle = random.uniform(0, 2 * math.pi)
        bump.co = (
            math.cos(angle) * 0.6,
            math.sin(angle) * 0.6,
            random.uniform(0.3, 0.8)
        )
        bump.radius = random.uniform(0.3, 0.5)

    # Eyes (small balls)
    for x_offset in [-0.25, 0.25]:
        eye = mball.elements.new()
        eye.type = 'BALL'
        eye.co = (x_offset, -0.5, 0.8)
        eye.radius = 0.15

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')
    mesh_obj = bpy.context.active_object
    mesh_obj.name = "SlimeMesh"

    return mesh_obj

def post_process(obj):
    """Apply UVs and smooth shading."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

def main():
    clear_scene()
    slime = create_slime(seed=12345)
    post_process(slime)
    bpy.ops.export_scene.gltf(filepath="slime.glb", export_format='GLB')

if __name__ == "__main__":
    main()
```

### Metaball Parameters

```python
# Resolution (lower = more triangles)
mball.resolution = 0.1        # 0.05-0.2 typical
mball.render_resolution = 0.05

# Threshold affects blend distance
mball.threshold = 1.0         # Default, higher = tighter blend

# Stiffness per element (how much it blends)
elem.stiffness = 1.0          # 0-10, lower = more blend

# Hide elements for negative space (NOT subtraction, just hidden)
elem.hide = True
```

### Tips for Metaballs

1. **Resolution tradeoff** — Lower resolution = more polys, smoother surface
2. **Blend control** — Use `stiffness` to control how elements merge
3. **Placement matters** — Elements blend based on distance
4. **Convert early** — Convert to mesh before applying modifiers
5. **Decimate after** — Use DECIMATE modifier to reduce poly count

---

## Skin Modifier

Create creatures from vertex "skeletons" — the Skin modifier inflates vertices into a mesh.

### Workflow

1. Create vertices (the skeleton)
2. Connect with edges
3. Add Skin modifier
4. Adjust vertex radii
5. Add Subsurf for smoothing (optional)

### Basic Skin Modifier Setup

```python
import bpy
import bmesh

def create_skin_mesh(name="Creature"):
    """Create a mesh with skin modifier from vertex skeleton."""
    # Create mesh data
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Use bmesh for vertex creation
    bm = bmesh.new()

    # Create skeleton vertices (example: simple biped)
    verts = []
    # Spine
    verts.append(bm.verts.new((0, 0, 0)))      # Hip
    verts.append(bm.verts.new((0, 0, 0.5)))    # Chest
    verts.append(bm.verts.new((0, 0, 0.8)))    # Neck
    verts.append(bm.verts.new((0, 0, 1.0)))    # Head

    # Connect spine
    bm.edges.new((verts[0], verts[1]))
    bm.edges.new((verts[1], verts[2]))
    bm.edges.new((verts[2], verts[3]))

    # Write to mesh
    bm.to_mesh(mesh)
    bm.free()

    # Add skin modifier
    mod = obj.modifiers.new(name="Skin", type='SKIN')

    return obj
```

### Complete Example: Quadruped Creature

```python
#!/usr/bin/env python3
"""Generate a quadruped creature using skin modifier."""

import bpy
import bmesh
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_quadruped():
    """Create a four-legged creature skeleton."""
    mesh = bpy.data.meshes.new("Quadruped")
    obj = bpy.data.objects.new("Quadruped", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()

    # Body spine
    spine = []
    spine.append(bm.verts.new((0, -0.5, 0.5)))   # Tail base
    spine.append(bm.verts.new((0, 0, 0.5)))      # Hip
    spine.append(bm.verts.new((0, 0.5, 0.55)))   # Mid body
    spine.append(bm.verts.new((0, 1.0, 0.5)))    # Chest
    spine.append(bm.verts.new((0, 1.3, 0.6)))    # Neck
    spine.append(bm.verts.new((0, 1.5, 0.7)))    # Head

    # Connect spine
    for i in range(len(spine) - 1):
        bm.edges.new((spine[i], spine[i + 1]))

    # Tail
    tail_base = spine[0]
    tail_tip = bm.verts.new((0, -0.9, 0.4))
    bm.edges.new((tail_base, tail_tip))

    # Back legs (from hip)
    hip = spine[1]
    for x_offset in [-0.2, 0.2]:
        knee = bm.verts.new((x_offset, -0.1, 0.25))
        foot = bm.verts.new((x_offset, -0.05, 0))
        bm.edges.new((hip, knee))
        bm.edges.new((knee, foot))

    # Front legs (from chest)
    chest = spine[3]
    for x_offset in [-0.2, 0.2]:
        elbow = bm.verts.new((x_offset, 0.9, 0.25))
        paw = bm.verts.new((x_offset, 0.95, 0))
        bm.edges.new((chest, elbow))
        bm.edges.new((elbow, paw))

    # Ears (from head)
    head = spine[5]
    for x_offset in [-0.08, 0.08]:
        ear = bm.verts.new((x_offset, 1.45, 0.85))
        bm.edges.new((head, ear))

    bm.to_mesh(mesh)
    bm.free()

    # Add skin modifier
    mod_skin = obj.modifiers.new(name="Skin", type='SKIN')

    # Adjust skin radii
    skin_data = mesh.skin_vertices[0].data
    radii = {
        0: (0.03, 0.03),   # Tail base
        1: (0.12, 0.12),   # Hip
        2: (0.15, 0.15),   # Mid body
        3: (0.12, 0.12),   # Chest
        4: (0.06, 0.06),   # Neck
        5: (0.1, 0.1),     # Head
        6: (0.01, 0.01),   # Tail tip
    }
    for idx, (rx, ry) in radii.items():
        if idx < len(skin_data):
            skin_data[idx].radius = (rx, ry)

    # Mark root vertex
    skin_data[1].use_root = True

    # Add subdivision for smoothing
    mod_subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    mod_subsurf.levels = 1
    mod_subsurf.render_levels = 1

    return obj

def apply_modifiers(obj):
    """Apply all modifiers."""
    bpy.context.view_layer.objects.active = obj
    for mod in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=mod.name)

def post_process(obj):
    """UV unwrap and finalize."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

def main():
    clear_scene()
    creature = create_quadruped()
    apply_modifiers(creature)
    post_process(creature)
    bpy.ops.export_scene.gltf(filepath="quadruped.glb", export_format='GLB')

if __name__ == "__main__":
    main()
```

### Skin Modifier Parameters

```python
# Access skin vertex data
skin_data = mesh.skin_vertices[0].data

# Set radius per vertex
skin_data[vertex_index].radius = (x_radius, y_radius)

# Mark root (important for topology)
skin_data[vertex_index].use_root = True

# Mark as loose (disconnected)
skin_data[vertex_index].use_loose = True
```

### Tips for Skin Modifier

1. **Mark root vertex** — One vertex should be marked as root for proper topology
2. **Adjust radii** — Each vertex can have independent X/Y radius
3. **Add Subsurf** — Usually needed for smooth results
4. **Symmetry** — Use X mirror in edit mode for symmetric creatures
5. **Edge flow** — Skeleton edge layout affects final topology

---

## SDF Pipeline

Use `fogleman/sdf` library for complex smooth blends, then clean up in Blender.

### When to Use SDF

- Complex boolean operations that bpy booleans struggle with
- Smooth blends between many shapes
- Terrain generation
- Abstract organic forms
- When metaballs don't provide enough control

### Workflow

```
1. Generate STL with fogleman/sdf  →  output.stl
2. Import into Blender
3. Remesh for clean topology
4. UV unwrap and export
```

### Step 1: SDF Generation (Python, no Blender)

```python
#!/usr/bin/env python3
"""Generate organic mesh using fogleman/sdf library."""

# pip install sdf
from sdf import *

def generate_creature():
    """Create a blobby creature using SDF operations."""
    # Body (rounded box)
    body = rounded_box([1.0, 0.6, 0.5], 0.1)

    # Head (sphere, offset forward)
    head = sphere(0.3).translate((0.6, 0, 0.1))

    # Smooth blend body and head
    creature = body | head.k(0.2)  # k = blend factor

    # Legs (capsules)
    leg = capsule(-Y * 0.3, Y * 0, 0.08)
    legs = []
    for x in [-0.3, 0.3]:
        for y in [-0.2, 0.2]:
            legs.append(leg.translate((x, y, -0.25)))

    # Add legs with smooth blend
    for leg_sdf in legs:
        creature = creature | leg_sdf.k(0.1)

    # Tail (tapered capsule)
    tail = capsule(Z * 0, -Z * 0.4, 0.05).translate((-0.5, 0, 0))
    creature = creature | tail.k(0.15)

    # Export to STL
    creature.save('creature_sdf.stl', step=0.02)  # step = resolution
    print("Exported creature_sdf.stl")

if __name__ == "__main__":
    generate_creature()
```

### Step 2: Blender Cleanup Script

```python
#!/usr/bin/env python3
"""Import SDF mesh and clean up in Blender."""

import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def import_stl(filepath):
    """Import STL file."""
    bpy.ops.import_mesh.stl(filepath=filepath)
    return bpy.context.active_object

def cleanup_sdf_mesh(obj, target_tris=500):
    """Clean up imported SDF mesh."""
    bpy.context.view_layer.objects.active = obj

    # Remesh for clean topology
    mod_remesh = obj.modifiers.new(name="Remesh", type='REMESH')
    mod_remesh.mode = 'VOXEL'
    mod_remesh.voxel_size = 0.05  # Adjust for detail level
    mod_remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier="Remesh")

    # Decimate to target poly count
    current_tris = len(obj.data.polygons)
    if current_tris > target_tris:
        ratio = target_tris / current_tris
        mod_decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod_decimate.ratio = ratio
        bpy.ops.object.modifier_apply(modifier="Decimate")

    # Smooth shading
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(30)

def post_process(obj):
    """UV unwrap and finalize."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Remove doubles from SDF mesh
    bpy.ops.mesh.remove_doubles(threshold=0.001)

    # UV unwrap
    bpy.ops.uv.smart_project(angle_limit=66.0)

    # Triangulate
    bpy.ops.mesh.quads_convert_to_tris()

    bpy.ops.object.mode_set(mode='OBJECT')

def export_glb(filepath):
    """Export to GLB."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_apply_modifiers=True
    )

def main():
    clear_scene()

    # Import the SDF-generated STL
    obj = import_stl("creature_sdf.stl")
    obj.name = "CreatureSDF"

    # Clean up
    cleanup_sdf_mesh(obj, target_tris=800)
    post_process(obj)

    # Export
    export_glb("creature_final.glb")
    print("Exported creature_final.glb")

if __name__ == "__main__":
    main()
```

### SDF Operations Reference

```python
from sdf import *

# Primitives
sphere(radius)
box(size)                    # size = (x, y, z) tuple
rounded_box(size, radius)
capsule(point_a, point_b, radius)
cylinder(radius)             # Infinite cylinder
capped_cylinder(point_a, point_b, radius)
torus(major_radius, minor_radius)
plane(normal, point)

# Transformations
shape.translate((x, y, z))
shape.rotate(angle, axis)
shape.scale(factor)          # Uniform scale
shape.orient(forward_vector)

# Boolean Operations
a | b                        # Union
a & b                        # Intersection
a - b                        # Difference

# Smooth Blends (the magic of SDF!)
a | b.k(0.2)                 # Smooth union (k = blend radius)
a & b.k(0.2)                 # Smooth intersection
a - b.k(0.2)                 # Smooth difference

# Modifiers
shape.shell(thickness)       # Hollow shell
shape.elongate((x, y, z))   # Stretch
shape.twist(amount)          # Twist around Y
shape.bend(amount)           # Bend
shape.onion(thickness)       # Concentric shells
```

### Tips for SDF Pipeline

1. **Step size matters** — Lower step = more triangles, smoother surface
2. **Use smooth blends** — `.k(value)` is the key advantage of SDF
3. **Remesh is essential** — SDF output has messy topology, always remesh
4. **Decimate after** — SDF often generates too many triangles
5. **Check scale** — SDF uses arbitrary units, scale in Blender as needed
6. **Combine workflows** — Use SDF for base shape, Blender for details

---

## Choosing the Right Workflow

| Shape Type | Recommended Workflow |
|------------|---------------------|
| Simple blobs (slime, egg) | Metaballs |
| Character from pose sketch | Skin Modifier |
| Abstract organic terrain | SDF Pipeline |
| Creature with defined limbs | Skin Modifier or SDF |
| Smooth blend of many shapes | SDF Pipeline |
| Quick prototype | Metaballs |
| Complex carved surface | SDF Pipeline |
| Symmetrical creature | Skin + Mirror modifier |

### Complexity vs Control Tradeoff

```
Simple ←————————————————————————→ Complex
Metaballs → Skin Modifier → SDF Pipeline
Less Control                More Control
Fewer Options              More Operations
Fast Iteration             Precise Results
```
