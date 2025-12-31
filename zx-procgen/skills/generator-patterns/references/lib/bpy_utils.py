#!/usr/bin/env python3
"""Blender Python utilities for mesh generation.

Copy this file to your project's generator/lib/ folder.

Requires: Blender 3.0+ (run via `blender --background --python script.py`)
"""
import bpy
from pathlib import Path


def clear_scene():
    """Remove all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


def apply_modifiers(obj):
    """Apply all modifiers to an object."""
    bpy.context.view_layer.objects.active = obj
    for mod in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=mod.name)


def apply_transforms(obj):
    """Apply location, rotation, and scale transforms."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def set_origin_to_bottom(obj):
    """Set object origin to the bottom center."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # Move origin to bottom
    obj.location.z = obj.dimensions.z / 2


def auto_uv_project(obj):
    """Apply automatic UV projection (smart UV project)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')


def box_uv_project(obj):
    """Apply box UV projection."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=1.0)
    bpy.ops.object.mode_set(mode='OBJECT')


def recalculate_normals(obj):
    """Recalculate normals to face outward."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')


def triangulate_mesh(obj):
    """Convert all faces to triangles."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')


def get_poly_count(obj):
    """Get triangle count for an object."""
    return len(obj.data.polygons)


def decimate_to_target(obj, target_tris: int):
    """Add decimate modifier to reduce to target triangle count."""
    current = get_poly_count(obj)
    if current <= target_tris:
        return

    ratio = target_tris / current
    mod = obj.modifiers.new("Decimate", 'DECIMATE')
    mod.ratio = ratio
    apply_modifiers(obj)


def add_bevel(obj, width: float = 0.02, segments: int = 2):
    """Add bevel modifier for rounded edges."""
    mod = obj.modifiers.new("Bevel", 'BEVEL')
    mod.width = width
    mod.segments = segments
    return mod


def add_solidify(obj, thickness: float = 0.1):
    """Add solidify modifier for thickness."""
    mod = obj.modifiers.new("Solidify", 'SOLIDIFY')
    mod.thickness = thickness
    return mod


def add_mirror(obj, axis: str = 'X'):
    """Add mirror modifier."""
    mod = obj.modifiers.new("Mirror", 'MIRROR')
    mod.use_axis = [axis == 'X', axis == 'Y', axis == 'Z']
    return mod


def add_array(obj, count: int, offset: tuple = (1, 0, 0)):
    """Add array modifier."""
    mod = obj.modifiers.new("Array", 'ARRAY')
    mod.count = count
    mod.use_relative_offset = True
    mod.relative_offset_displace = offset
    return mod


def join_objects(objects: list):
    """Join multiple objects into one."""
    if not objects:
        return None

    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    return objects[0]


def export_glb(filepath: str, selected_only: bool = False):
    """Export scene to GLB format."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.export_scene.gltf(
        filepath=str(path),
        export_format='GLB',
        use_selection=selected_only,
        export_apply=True,
        export_yup=True,
    )
    print(f"Exported: {path}")


def export_obj(filepath: str, selected_only: bool = False):
    """Export scene to OBJ format."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.obj_export(
        filepath=str(path),
        export_selected_objects=selected_only,
        apply_modifiers=True,
        export_uv=True,
        export_normals=True,
    )
    print(f"Exported: {path}")


def post_process(obj):
    """Standard post-processing pipeline for game-ready mesh."""
    apply_modifiers(obj)
    apply_transforms(obj)
    recalculate_normals(obj)
    auto_uv_project(obj)
    triangulate_mesh(obj)
