"""
Mesh Parser - Interprets .spec.py files and generates meshes in Blender.

Usage (via unified generator):
    blender --background --python .studio/generate.py -- --only meshes

Specs:
    .studio/specs/meshes/*.spec.py

Outputs:
    generated/meshes/*.glb
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def load_spec(spec_path: str) -> Dict[str, Any]:
    """Load MESH spec from .spec.py file via exec()."""
    code = Path(spec_path).read_text(encoding="utf-8")
    namespace: Dict[str, Any] = {}
    exec(code, namespace)
    if "MESH" not in namespace:
        raise ValueError(f"No MESH dict found in {spec_path}")
    return namespace["MESH"]


def clear_scene() -> None:
    import bpy  # type: ignore

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def _add_primitive(mesh: Dict[str, Any]) -> None:
    import bpy  # type: ignore

    prim = mesh.get("primitive", "cube")
    params = mesh.get("params", {})

    if prim == "cube":
        bpy.ops.mesh.primitive_cube_add(size=float(params.get("size", 1.0)))
        return

    if prim == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(
            radius=float(params.get("radius", 0.5)),
            depth=float(params.get("depth", 1.0)),
            vertices=int(params.get("vertices", 24)),
        )
        return

    if prim == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=float(params.get("radius", 0.5)),
            segments=int(params.get("segments", 32)),
            ring_count=int(params.get("rings", 16)),
        )
        return

    if prim == "icosphere":
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=float(params.get("radius", 0.5)),
            subdivisions=int(params.get("subdivisions", 2)),
        )
        return

    if prim == "cone":
        bpy.ops.mesh.primitive_cone_add(
            radius1=float(params.get("radius1", 0.5)),
            radius2=float(params.get("radius2", 0.0)),
            depth=float(params.get("depth", 1.0)),
            vertices=int(params.get("vertices", 24)),
        )
        return

    if prim == "torus":
        bpy.ops.mesh.primitive_torus_add(
            major_radius=float(params.get("major_radius", 0.75)),
            minor_radius=float(params.get("minor_radius", 0.25)),
            major_segments=int(params.get("major_segments", 48)),
            minor_segments=int(params.get("minor_segments", 16)),
        )
        return

    raise ValueError(f"Unknown mesh primitive '{prim}'")


def _apply_modifiers(obj, modifiers: list[Dict[str, Any]]) -> None:
    import bpy  # type: ignore

    for mod in modifiers:
        mod_type = mod.get("type")
        if mod_type == "bevel":
            m = obj.modifiers.new(name="Bevel", type="BEVEL")
            m.width = float(mod.get("width", 0.02))
            m.segments = int(mod.get("segments", 2))
            m.limit_method = "ANGLE"
            m.angle_limit = float(mod.get("angle_limit", 0.785398))  # ~45deg
            continue

        if mod_type == "decimate":
            m = obj.modifiers.new(name="Decimate", type="DECIMATE")
            m.ratio = float(mod.get("ratio", 0.5))
            continue

        if mod_type == "triangulate":
            obj.modifiers.new(name="Triangulate", type="TRIANGULATE")
            continue

        raise ValueError(f"Unknown modifier type '{mod_type}'")

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target="MESH")


def _uv_unwrap(obj, uv: Dict[str, Any]) -> None:
    import bpy  # type: ignore

    mode = uv.get("mode", "smart_project")
    if not mode:
        return

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")

    if mode == "smart_project":
        bpy.ops.uv.smart_project(angle_limit=float(uv.get("angle_limit", 66.0)))
    elif mode == "cube_project":
        bpy.ops.uv.cube_project(cube_size=float(uv.get("cube_size", 1.0)))
    else:
        bpy.ops.object.mode_set(mode="OBJECT")
        raise ValueError(f"Unknown UV mode '{mode}'")

    bpy.ops.object.mode_set(mode="OBJECT")


def generate_mesh(spec: Dict[str, Any], output_path: str) -> None:
    import bpy  # type: ignore

    mesh = spec.get("mesh", spec)
    if not isinstance(mesh, dict):
        raise ValueError("MESH spec must contain a 'mesh' dict")

    name = mesh.get("name")
    if not name:
        raise ValueError("MESH spec is missing required mesh.name")

    clear_scene()
    _add_primitive(mesh)

    obj = bpy.context.active_object
    if obj is None:
        raise RuntimeError("Failed to create primitive mesh")

    obj.name = str(name)

    if "location" in mesh:
        obj.location = mesh["location"]
    if "rotation" in mesh:
        obj.rotation_euler = mesh["rotation"]
    if "scale" in mesh:
        obj.scale = mesh["scale"]

    shade = mesh.get("shade", "smooth")
    if shade == "smooth":
        bpy.ops.object.shade_smooth()
    elif shade == "flat":
        bpy.ops.object.shade_flat()
    elif shade:
        raise ValueError(f"Unknown shade mode '{shade}'")

    modifiers = list(mesh.get("modifiers", []))
    if modifiers:
        _apply_modifiers(obj, modifiers)

    uv = dict(mesh.get("uv", {}))
    if uv:
        _uv_unwrap(obj, uv)

    export = dict(mesh.get("export", {}))
    export_tangents = bool(export.get("tangents", False))

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.export_scene.gltf(
        filepath=str(out),
        export_format="GLB",
        export_apply=True,
        export_normals=True,
        export_tangents=export_tangents,
    )
