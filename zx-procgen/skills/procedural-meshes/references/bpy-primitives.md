# Blender bpy Primitives Reference

Complete reference for creating mesh primitives with Blender's Python API.

## Scene Setup

```python
import bpy
import math

def clear_scene():
    """Remove all objects from scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def get_active_object():
    """Return the active object after creation."""
    return bpy.context.active_object
```

---

## Cube / Box

```python
bpy.ops.mesh.primitive_cube_add(
    size=2.0,              # Total size (not half-size)
    location=(0, 0, 0),    # World position
    rotation=(0, 0, 0),    # Rotation in radians
    scale=(1, 1, 1)        # Non-uniform scaling
)
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| size | 2.0 | Cube edge length |
| location | (0,0,0) | World position |
| rotation | (0,0,0) | Euler rotation (radians) |
| scale | (1,1,1) | Per-axis scale |

**Triangle count:** 12 (fixed)

**Example: Rectangular Box**
```python
def create_box(width, height, depth, location=(0, 0, 0)):
    """Create a rectangular box with custom dimensions."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.scale = (width, depth, height)
    bpy.ops.object.transform_apply(scale=True)
    return obj

# Create a 2x1x3 crate
crate = create_box(2.0, 3.0, 1.0, location=(0, 0, 1.5))
```

---

## Cylinder

```python
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,           # Circumference segments
    radius=1.0,            # Cylinder radius
    depth=2.0,             # Height
    end_fill_type='NGON',  # 'NOTHING', 'NGON', 'TRIFAN'
    location=(0, 0, 0),
    rotation=(0, 0, 0)
)
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| vertices | 32 | Segments around circumference |
| radius | 1.0 | Cylinder radius |
| depth | 2.0 | Height |
| end_fill_type | 'NGON' | Cap style |

**Triangle count:** `vertices × 4 + cap_tris`

**Recommended segments for low-poly:**
- Distant: 6-8
- Standard: 12-16
- Close-up: 24-32

**Example: Barrel**
```python
def create_barrel(radius=0.5, height=1.2, segments=12):
    """Create a low-poly barrel."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=segments,
        radius=radius,
        depth=height,
        end_fill_type='TRIFAN',
        location=(0, 0, height / 2)
    )
    obj = bpy.context.active_object
    obj.name = "Barrel"
    return obj
```

---

## UV Sphere

```python
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=32,           # Horizontal segments
    ring_count=16,         # Vertical rings
    radius=1.0,
    location=(0, 0, 0),
    rotation=(0, 0, 0)
)
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| segments | 32 | Longitude divisions |
| ring_count | 16 | Latitude divisions |
| radius | 1.0 | Sphere radius |

**Triangle count:** `segments × ring_count × 2` (approximately)

**Recommended for low-poly:**
| Quality | Segments | Rings | Tris |
|---------|----------|-------|------|
| Distant | 8 | 4 | ~64 |
| Standard | 12 | 8 | ~192 |
| Close-up | 24 | 12 | ~576 |

**Example: Low-poly Sphere**
```python
def create_sphere(radius=1.0, detail='standard', location=(0, 0, 0)):
    """Create sphere with preset detail levels."""
    presets = {
        'distant': (8, 4),
        'standard': (12, 8),
        'closeup': (24, 12)
    }
    segs, rings = presets.get(detail, (12, 8))

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segs,
        ring_count=rings,
        radius=radius,
        location=location
    )
    return bpy.context.active_object
```

---

## Ico Sphere

Alternative sphere with more uniform triangle distribution.

```python
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=2,        # Subdivision level (1-10)
    radius=1.0,
    location=(0, 0, 0)
)
```

**Triangle count by subdivision:**
| Subdivisions | Triangles |
|--------------|-----------|
| 1 | 20 |
| 2 | 80 |
| 3 | 320 |
| 4 | 1280 |

**Best for:** Game assets where uniform triangle distribution matters (physics spheres, planets).

---

## Cone

```python
bpy.ops.mesh.primitive_cone_add(
    vertices=32,           # Base segments
    radius1=1.0,           # Bottom radius
    radius2=0.0,           # Top radius (0 = point)
    depth=2.0,             # Height
    end_fill_type='NGON',  # Base fill type
    location=(0, 0, 0)
)
```

**Variations:**
- **Cone:** `radius2=0`
- **Truncated cone:** `radius2 > 0`
- **Cylinder:** `radius1 == radius2`

**Example: Spike**
```python
def create_spike(radius=0.2, height=1.0, segments=6):
    """Create a pointed spike for traps, fences, etc."""
    bpy.ops.mesh.primitive_cone_add(
        vertices=segments,
        radius1=radius,
        radius2=0.0,
        depth=height,
        location=(0, 0, height / 2)
    )
    return bpy.context.active_object
```

---

## Torus

```python
bpy.ops.mesh.primitive_torus_add(
    major_segments=48,     # Ring segments
    minor_segments=12,     # Tube segments
    major_radius=1.0,      # Distance from center to tube center
    minor_radius=0.25,     # Tube radius
    location=(0, 0, 0)
)
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| major_segments | 48 | Segments around ring |
| minor_segments | 12 | Segments around tube |
| major_radius | 1.0 | Ring radius |
| minor_radius | 0.25 | Tube thickness |

**Triangle count:** `major_segments × minor_segments × 2`

**Low-poly settings:**
| Quality | Major | Minor | Tris |
|---------|-------|-------|------|
| Distant | 12 | 4 | ~96 |
| Standard | 24 | 8 | ~384 |
| Close-up | 48 | 12 | ~1152 |

**Example: Wheel/Ring**
```python
def create_wheel(outer_radius=0.5, thickness=0.1, segments=16):
    """Create a low-poly wheel or ring."""
    bpy.ops.mesh.primitive_torus_add(
        major_segments=segments,
        minor_segments=6,
        major_radius=outer_radius - thickness,
        minor_radius=thickness,
        location=(0, 0, 0)
    )
    return bpy.context.active_object
```

---

## Plane

```python
bpy.ops.mesh.primitive_plane_add(
    size=2.0,              # Total width/height
    location=(0, 0, 0),
    rotation=(0, 0, 0)
)
```

**Triangle count:** 2 (single quad triangulated)

**Example: Subdivided Ground Plane**
```python
def create_ground_plane(size=10.0, subdivisions=4):
    """Create subdivided ground plane for terrain."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    obj = bpy.context.active_object

    # Add subdivision
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=subdivisions)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj
```

---

## Circle (Edge Ring)

```python
bpy.ops.mesh.primitive_circle_add(
    vertices=32,           # Number of vertices
    radius=1.0,
    fill_type='NOTHING',   # 'NOTHING', 'NGON', 'TRIFAN'
    location=(0, 0, 0)
)
```

**Use for:** Creating custom shapes by extruding edges, path outlines.

---

## Grid

```python
bpy.ops.mesh.primitive_grid_add(
    x_subdivisions=10,     # Subdivisions in X
    y_subdivisions=10,     # Subdivisions in Y
    size=2.0,              # Total size
    location=(0, 0, 0)
)
```

**Triangle count:** `x_subdivisions × y_subdivisions × 2`

**Use for:** Terrain, deformable surfaces, water planes.

---

## Monkey (Suzanne)

Blender's test mesh - useful for testing shaders and workflows.

```python
bpy.ops.mesh.primitive_monkey_add(
    size=2.0,
    location=(0, 0, 0)
)
```

**Triangle count:** ~500 (varies by version)

---

## Complete Example: Props Pack

```python
#!/usr/bin/env python3
"""Generate a pack of game props using bpy primitives."""

import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_crate(size=1.0, location=(0, 0, 0)):
    """Simple wooden crate."""
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = "Crate"
    return obj

def create_barrel(location=(0, 0, 0)):
    """Low-poly barrel."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=0.4,
        depth=1.0,
        location=(location[0], location[1], location[2] + 0.5)
    )
    obj = bpy.context.active_object
    obj.name = "Barrel"

    # Slight bulge in middle
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Scale middle vertices slightly
    for v in obj.data.vertices:
        if 0.2 < v.co.z < 0.8:
            factor = 1.0 + 0.1 * math.sin((v.co.z - 0.2) / 0.6 * math.pi)
            v.co.x *= factor
            v.co.y *= factor

    return obj

def create_pillar(height=3.0, radius=0.3, location=(0, 0, 0)):
    """Stone pillar."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=radius,
        depth=height,
        location=(location[0], location[1], location[2] + height / 2)
    )
    obj = bpy.context.active_object
    obj.name = "Pillar"
    return obj

def create_orb(radius=0.3, location=(0, 0, 0)):
    """Glowing orb / collectible."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12,
        ring_count=8,
        radius=radius,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = "Orb"
    return obj

def post_process(obj):
    """Apply UVs and smooth normals."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

def export_glb(filepath):
    """Export selected objects to GLB."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_apply_modifiers=True
    )

def main():
    clear_scene()

    # Create props
    crate = create_crate(location=(0, 0, 0))
    barrel = create_barrel(location=(2, 0, 0))
    pillar = create_pillar(location=(4, 0, 0))
    orb = create_orb(location=(0, 2, 1))

    # Post-process each
    for obj in [crate, barrel, pillar, orb]:
        post_process(obj)

    # Export all
    bpy.ops.object.select_all(action='SELECT')
    export_glb("props_pack.glb")

if __name__ == "__main__":
    main()
```

---

## Coordinate System Notes

- **Y-up:** Blender uses Z-up internally, but GLTF export converts to Y-up
- **Right-handed:** Standard game engine convention
- **Units:** 1 Blender unit = 1 meter (typical)
- **Origin:** Set at logical center point (base for standing objects, center for thrown objects)

## Performance Tips

1. **Minimize segments** - Use the lowest segment count that looks acceptable
2. **Share primitives** - Create once, duplicate with `obj.copy()` and `obj.data.copy()`
3. **Batch operations** - Process multiple objects in one script run
4. **Apply transforms** - Call `bpy.ops.object.transform_apply()` before export
