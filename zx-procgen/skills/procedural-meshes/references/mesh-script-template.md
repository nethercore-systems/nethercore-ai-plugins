# Mesh Generation Script Template

Standard template for procedural mesh generators using Blender bpy.

## Basic Template

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

## Template with Arguments

For generators that accept command-line parameters:

```python
#!/usr/bin/env python3
"""
Parameterized mesh generator.
Run: blender --background --python generator.py -- --size 2.0 --segments 8
"""

import bpy
import math
import sys
import argparse

def parse_args():
    """Parse command-line arguments after '--'."""
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=float, default=1.0)
    parser.add_argument("--segments", type=int, default=8)
    parser.add_argument("--output", type=str, default="output.glb")
    return parser.parse_args(argv)

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def generate_mesh(args):
    """Generate mesh with parameters."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=args.size,
        depth=args.size * 2,
        vertices=args.segments
    )
    return bpy.context.active_object

def post_process(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

def export(filepath):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_apply_modifiers=True,
        export_normals=True
    )

def main():
    args = parse_args()
    clear_scene()
    obj = generate_mesh(args)
    post_process(obj)
    export(args.output)

if __name__ == "__main__":
    main()
```

## Template with Shared Library

For projects with multiple mesh generators sharing utilities:

```python
#!/usr/bin/env python3
"""
Mesh generator using shared library.
Run: blender --background --python meshes/barrel.py
"""

import bpy
import math
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from bpy_utils import clear_scene, post_process, export_glb

def generate_barrel():
    """Generate a barrel mesh."""
    # Main body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.5,
        depth=1.2,
        vertices=12
    )
    barrel = bpy.context.active_object

    # Add bevel for barrel bulge
    mod = barrel.modifiers.new("Bevel", 'BEVEL')
    mod.width = 0.1
    mod.segments = 2

    bpy.ops.object.modifier_apply(modifier="Bevel")
    return barrel

def main():
    clear_scene()
    obj = generate_barrel()
    post_process(obj)
    export_glb("../assets/meshes/barrel.glb")

if __name__ == "__main__":
    main()
```

## Post-Processing Utilities

Extract to `lib/bpy_utils.py`:

```python
"""Shared utilities for mesh generation."""

import bpy
import math

def clear_scene():
    """Remove all objects from scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def post_process(obj, smooth_angle=30):
    """Apply standard post-processing to mesh."""
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # UV unwrap
    bpy.ops.uv.smart_project(angle_limit=66.0)

    # Cleanup
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.delete_loose()
    bpy.ops.mesh.quads_convert_to_tris()

    # Normals
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(smooth_angle)

def export_glb(filepath, tangents=False):
    """Export scene to GLB."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_apply_modifiers=True,
        export_normals=True,
        export_tangents=tangents,
        export_colors=True
    )
```

## Usage

```bash
# Basic generation
blender --background --python meshes/barrel.py

# With arguments
blender --background --python meshes/crate.py -- --size 2.0 --output crate_large.glb

# Batch generation
python generate_all.py
```
