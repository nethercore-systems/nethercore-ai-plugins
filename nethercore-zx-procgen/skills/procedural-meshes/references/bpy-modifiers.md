# Blender bpy Modifiers Reference

Complete reference for mesh modifiers in Blender Python scripting. Modifiers transform meshes non-destructively until applied.

## Modifier Workflow

```python
import bpy

# Add modifier
obj = bpy.context.active_object
mod = obj.modifiers.new(name="MyMirror", type='MIRROR')

# Configure modifier
mod.use_axis[0] = True  # Mirror on X

# Apply modifier (makes changes permanent)
bpy.ops.object.modifier_apply(modifier="MyMirror")
```

---

## MIRROR — Symmetric Objects

Create symmetric meshes by modeling half and mirroring.

```python
mod = obj.modifiers.new(name="Mirror", type='MIRROR')
mod.use_axis[0] = True    # X axis (default)
mod.use_axis[1] = False   # Y axis
mod.use_axis[2] = False   # Z axis
mod.use_clip = True       # Prevent vertices crossing center
mod.merge_threshold = 0.001  # Merge distance at seam
```

**Use cases:** Characters, vehicles, weapons, symmetric props

**Complete Example: Symmetric Character Base**
```python
def create_symmetric_torso():
    """Create character torso - model left half only."""
    # Start with half cube
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.5, 0, 1))
    obj = bpy.context.active_object
    obj.name = "Torso"

    # Scale to torso proportions
    obj.scale = (0.5, 0.3, 0.8)
    bpy.ops.object.transform_apply(scale=True)

    # Add mirror on X
    mod = obj.modifiers.new(name="Mirror", type='MIRROR')
    mod.use_axis[0] = True
    mod.use_clip = True
    mod.merge_threshold = 0.001

    return obj
```

---

## BEVEL — Chamfered Edges

Add beveled/chamfered edges for that industrial look.

```python
mod = obj.modifiers.new(name="Bevel", type='BEVEL')
mod.width = 0.05          # Bevel width
mod.segments = 2          # Segments (1-3 for low-poly)
mod.limit_method = 'ANGLE'  # Only bevel sharp edges
mod.angle_limit = math.radians(30)  # Threshold angle
mod.affect = 'EDGES'      # 'EDGES' or 'VERTICES'
mod.profile = 0.5         # 0.0 = concave, 0.5 = flat, 1.0 = convex
```

**Limit methods:**
- `'ANGLE'` — Only edges sharper than threshold
- `'WEIGHT'` — Use edge bevel weights
- `'VGROUP'` — Use vertex group
- `'NONE'` — All edges

**Complete Example: Beveled Crate**
```python
def create_beveled_crate(size=1.0, bevel_width=0.03):
    """Create a crate with beveled edges."""
    bpy.ops.mesh.primitive_cube_add(size=size)
    obj = bpy.context.active_object
    obj.name = "BeveledCrate"

    # Add bevel
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = bevel_width
    mod.segments = 1  # Low-poly friendly
    mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(45)

    return obj
```

---

## SOLIDIFY — Add Thickness

Convert flat surfaces to solid objects with thickness.

```python
mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
mod.thickness = 0.1       # Wall thickness
mod.offset = -1.0         # -1 = inward, 0 = centered, 1 = outward
mod.use_even_offset = True  # Uniform thickness on angled surfaces
mod.use_rim = True        # Fill rim (edges)
mod.use_rim_only = False  # Only create rim, no inner face
```

**Use cases:** Walls, panels, hollow objects, armor plates

**Complete Example: Hollow Box**
```python
def create_hollow_box(outer_size=1.0, wall_thickness=0.05):
    """Create a hollow box (like a container)."""
    bpy.ops.mesh.primitive_cube_add(size=outer_size)
    obj = bpy.context.active_object
    obj.name = "HollowBox"

    # Remove top face to make it open
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Select top face (highest Z vertices)
    for face in obj.data.polygons:
        if face.normal.z > 0.9:
            face.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add solidify for walls
    mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = wall_thickness
    mod.offset = -1.0  # Inward

    return obj
```

---

## ARRAY — Repeated Elements

Create arrays of repeated geometry.

```python
mod = obj.modifiers.new(name="Array", type='ARRAY')
mod.count = 5             # Number of copies
mod.use_relative_offset = True
mod.relative_offset_displace = (1.0, 0.0, 0.0)  # Offset per copy
# OR
mod.use_constant_offset = True
mod.constant_offset_displace = (0.0, 0.0, 1.0)  # Fixed offset
mod.use_merge_vertices = True
mod.merge_threshold = 0.001
```

**Complete Example: Chain Links**
```python
def create_chain(link_count=10):
    """Create a chain of linked rings."""
    # Create single link (torus)
    bpy.ops.mesh.primitive_torus_add(
        major_segments=12,
        minor_segments=4,
        major_radius=0.3,
        minor_radius=0.05
    )
    link = bpy.context.active_object
    link.name = "ChainLink"

    # Rotate to vertical
    link.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    # Array modifier
    mod = link.modifiers.new(name="Array", type='ARRAY')
    mod.count = link_count
    mod.use_relative_offset = True
    mod.relative_offset_displace = (0.0, 0.0, 0.4)

    return link
```

---

## BOOLEAN — Combine/Subtract Shapes

CSG operations: union, difference, intersection.

```python
mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
mod.operation = 'DIFFERENCE'  # 'INTERSECT', 'UNION', 'DIFFERENCE'
mod.object = other_obj        # The object to boolean with
mod.solver = 'FAST'           # 'FAST' or 'EXACT'
```

**Operations:**
- `'UNION'` — Combine volumes
- `'DIFFERENCE'` — Subtract second from first
- `'INTERSECT'` — Keep only overlap

**Complete Example: Carved Stone Block**
```python
def create_carved_block():
    """Create a block with carved details using booleans."""
    # Main block
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 1))
    block = bpy.context.active_object
    block.name = "CarvedBlock"

    # Carving tool (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.4,
        depth=3.0,
        location=(0.6, 0, 1),
        rotation=(0, math.radians(90), 0)
    )
    carver = bpy.context.active_object
    carver.name = "Carver"

    # Boolean difference
    mod = block.modifiers.new(name="Carve", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = carver
    mod.solver = 'FAST'

    # Apply and cleanup
    bpy.context.view_layer.objects.active = block
    bpy.ops.object.modifier_apply(modifier="Carve")

    # Delete carving tool
    bpy.data.objects.remove(carver)

    return block
```

---

## SUBSURF — Subdivision Surface

Smooth mesh by subdivision (use sparingly for low-poly).

```python
mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
mod.subdivision_type = 'CATMULL_CLARK'  # or 'SIMPLE'
mod.levels = 1            # Viewport subdivision level
mod.render_levels = 1     # Render level (same for games)
mod.use_limit_surface = True
```

**Triangle multiplication:**
| Level | Multiplier |
|-------|------------|
| 1 | 4x |
| 2 | 16x |
| 3 | 64x |

**Warning:** Only use level 1 for low-poly, and only on small meshes.

---

## DECIMATE — Reduce Poly Count

Reduce triangle count while preserving shape.

```python
mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
mod.decimate_type = 'COLLAPSE'  # 'COLLAPSE', 'UNSUBDIV', 'DISSOLVE'
mod.ratio = 0.5           # Target ratio (0.5 = half the triangles)
# OR for DISSOLVE:
mod.angle_limit = math.radians(5.0)  # Dissolve angle
```

**Decimate types:**
- `'COLLAPSE'` — Edge collapse (best general purpose)
- `'UNSUBDIV'` — Undo subdivision (if mesh was subdivided)
- `'DISSOLVE'` — Dissolve flat regions

**Complete Example: LOD Generation**
```python
def create_lod_chain(obj, ratios=[1.0, 0.5, 0.25]):
    """Create Level of Detail versions of a mesh."""
    lods = []

    for i, ratio in enumerate(ratios):
        # Duplicate object
        lod = obj.copy()
        lod.data = obj.data.copy()
        lod.name = f"{obj.name}_LOD{i}"
        bpy.context.collection.objects.link(lod)

        if ratio < 1.0:
            # Add decimate
            mod = lod.modifiers.new(name="Decimate", type='DECIMATE')
            mod.decimate_type = 'COLLAPSE'
            mod.ratio = ratio

            # Apply
            bpy.context.view_layer.objects.active = lod
            bpy.ops.object.modifier_apply(modifier="Decimate")

        lods.append(lod)

    return lods
```

---

## REMESH — Clean Topology

Regenerate mesh with clean, uniform topology.

```python
mod = obj.modifiers.new(name="Remesh", type='REMESH')
mod.mode = 'VOXEL'        # 'VOXEL', 'SHARP', 'SMOOTH', 'BLOCKS'
mod.voxel_size = 0.1      # Voxel resolution (VOXEL mode)
mod.octree_depth = 4      # Resolution (other modes, 1-8)
mod.use_smooth_shade = True
mod.use_remove_disconnected = True
```

**Modes:**
- `'VOXEL'` — Best for organic cleanup, size-based resolution
- `'SMOOTH'` — Smooth surface, octree-based
- `'SHARP'` — Preserve sharp edges
- `'BLOCKS'` — Minecraft-style voxels

**Use cases:** Cleaning SDF imports, fixing boolean artifacts, uniform topology.

---

## DISPLACE — Surface Displacement

Offset vertices based on texture or procedural pattern.

```python
mod = obj.modifiers.new(name="Displace", type='DISPLACE')
mod.strength = 0.1        # Displacement amount
mod.mid_level = 0.5       # Neutral height in texture
mod.direction = 'NORMAL'  # 'X', 'Y', 'Z', 'NORMAL', 'RGB_TO_XYZ'

# Create noise texture for displacement
tex = bpy.data.textures.new("NoiseDisplace", type='CLOUDS')
tex.noise_scale = 0.5
mod.texture = tex
```

**Complete Example: Rocky Surface**
```python
def add_rock_surface(obj, strength=0.05, scale=0.5):
    """Add rocky/uneven surface to object."""
    # Create noise texture
    tex = bpy.data.textures.new(f"{obj.name}_RockNoise", type='CLOUDS')
    tex.noise_scale = scale
    tex.noise_depth = 2

    # Add displacement
    mod = obj.modifiers.new(name="RockDisplace", type='DISPLACE')
    mod.texture = tex
    mod.strength = strength
    mod.mid_level = 0.5
    mod.direction = 'NORMAL'

    return mod
```

---

## WEIGHTED NORMAL — Better Normals

Improved normal calculation for hard surface models.

```python
mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
mod.mode = 'FACE_AREA'    # 'FACE_AREA', 'CORNER_ANGLE', 'FACE_AREA_AND_ANGLE'
mod.weight = 50           # Strength
mod.keep_sharp = True     # Respect sharp edges
```

---

## Modifier Stacking Order

Order matters! Apply modifiers in this sequence:

```
1. MIRROR          — Work on half mesh first
2. ARRAY           — Duplicate geometry
3. SUBSURF         — Subdivide if needed
4. DISPLACE        — Add surface detail
5. BOOLEAN         — Carve/combine
6. BEVEL           — Add edge detail
7. SOLIDIFY        — Add thickness
8. DECIMATE        — Reduce poly count
9. REMESH          — Clean topology
10. WEIGHTED_NORMAL — Fix shading
```

---

## Complete Example: Industrial Pipe Section

```python
#!/usr/bin/env python3
"""Generate industrial pipe section using multiple modifiers."""

import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_pipe_section():
    """Create an industrial pipe with flanges and bolts."""
    # Main pipe cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.3,
        depth=2.0,
        location=(0, 0, 1)
    )
    pipe = bpy.context.active_object
    pipe.name = "Pipe"

    # Solidify to make hollow
    mod_solid = pipe.modifiers.new(name="Hollow", type='SOLIDIFY')
    mod_solid.thickness = 0.02
    mod_solid.offset = -1.0

    # Create flange ring
    bpy.ops.mesh.primitive_torus_add(
        major_segments=16,
        minor_segments=4,
        major_radius=0.35,
        minor_radius=0.05,
        location=(0, 0, 0)
    )
    flange = bpy.context.active_object
    flange.name = "Flange"

    # Array the flange at both ends
    mod_array = flange.modifiers.new(name="Ends", type='ARRAY')
    mod_array.count = 2
    mod_array.use_relative_offset = False
    mod_array.use_constant_offset = True
    mod_array.constant_offset_displace = (0.0, 0.0, 2.0)

    # Create bolt (small cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=6,
        radius=0.03,
        depth=0.05,
        location=(0.32, 0, 0)
    )
    bolt = bpy.context.active_object
    bolt.name = "Bolt"

    # Array bolts around flange
    mod_circle = bolt.modifiers.new(name="Circle", type='ARRAY')
    mod_circle.count = 8
    mod_circle.use_relative_offset = False
    mod_circle.use_object_offset = True

    # Create empty for rotation
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    rotator = bpy.context.active_object
    rotator.rotation_euler = (0, 0, math.radians(360 / 8))
    mod_circle.offset_object = rotator

    # Apply all modifiers and join
    for obj in [pipe, flange, bolt]:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        for mod in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.select_set(False)

    # Select all pipe parts
    pipe.select_set(True)
    flange.select_set(True)
    bolt.select_set(True)
    bpy.context.view_layer.objects.active = pipe

    # Join into single mesh
    bpy.ops.object.join()
    pipe.name = "PipeSection"

    # Cleanup empty
    bpy.data.objects.remove(rotator)

    return pipe

def post_process(obj):
    """UV unwrap and finalize."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(30)

def main():
    clear_scene()
    pipe = create_pipe_section()
    post_process(pipe)
    bpy.ops.export_scene.gltf(
        filepath="pipe_section.glb",
        export_format='GLB'
    )

if __name__ == "__main__":
    main()
```

---

## Modifier Tips

1. **Preview before applying** — Modifiers are non-destructive until applied
2. **Order matters** — Experiment with stack order for different results
3. **Keep counts low** — Array counts and subdivision levels add up fast
4. **Use empties for rotation** — Array with object offset enables circular patterns
5. **Boolean cleanup** — Always remesh or remove doubles after booleans
6. **Check normals** — Booleans can flip normals, always recalculate
