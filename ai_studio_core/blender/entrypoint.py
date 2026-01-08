from __future__ import annotations

# This file is executed *inside Blender* (bpy available).
# It must not depend on non-stdlib Python packages.

import argparse
import json
import math
import random
import sys
from pathlib import Path

import bpy  # type: ignore
import bmesh  # type: ignore
from mathutils import Vector  # type: ignore


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="ai-studio-blender")
    parser.add_argument("--mode", choices=["preview", "validate"], required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out-root", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--generate-placeholder", action="store_true")
    return parser.parse_args(argv)


def _load_json(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("spec JSON must be an object at the top level")
    return raw


def _first_primary_glb_output(spec: dict) -> str:
    outputs = spec.get("outputs", [])
    if not isinstance(outputs, list):
        raise ValueError("spec.outputs must be a list")
    for o in outputs:
        if not isinstance(o, dict):
            continue
        if o.get("kind") == "primary" and o.get("format") == "glb":
            path = o.get("path")
            if isinstance(path, str) and path:
                return path
    raise ValueError("no primary glb output found in spec.outputs")


def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _clear_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _make_material(name: str, base_color=(0.7, 0.7, 0.72, 1.0), emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    assert nt is not None
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)

    if emission is not None:
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = emission
        em.inputs["Strength"].default_value = 1.0
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        return mat

    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = 0.6
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def _assign_material_to_meshes(mat) -> None:
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        mesh = obj.data
        if mesh.materials:
            mesh.materials[0] = mat
        else:
            mesh.materials.append(mat)


def _create_hardsurface_prop(seed: int) -> bpy.types.Object:
    random.seed(seed)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    assert obj is not None

    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = 0.06
    bevel.segments = 2
    bevel.limit_method = "ANGLE"

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=bevel.name)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.inset(thickness=0.08, depth=0.0)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0.0, 0.0, 0.03)})
    bpy.ops.object.mode_set(mode="OBJECT")

    return obj


def _create_lowpoly_character(seed: int) -> bpy.types.Object:
    random.seed(seed)

    parts: list[bpy.types.Object] = []

    def add_cube(name: str, size: tuple[float, float, float], loc: tuple[float, float, float]) -> None:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        obj = bpy.context.active_object
        assert obj is not None
        obj.name = name
        obj.scale = (size[0], size[1], size[2])
        parts.append(obj)

    # Simple, readable proportions (intentionally minimal).
    add_cube("Torso", (0.35, 0.22, 0.55), (0.0, 0.0, 0.55))
    add_cube("Head", (0.22, 0.22, 0.22), (0.0, 0.0, 1.35))
    add_cube("Leg.L", (0.14, 0.14, 0.45), (-0.14, 0.0, 0.15))
    add_cube("Leg.R", (0.14, 0.14, 0.45), (0.14, 0.0, 0.15))
    add_cube("Arm.L", (0.12, 0.12, 0.42), (-0.55, 0.0, 0.75))
    add_cube("Arm.R", (0.12, 0.12, 0.42), (0.55, 0.0, 0.75))

    for p in parts:
        bpy.context.view_layer.objects.active = p
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Join into a single mesh object.
    bpy.context.view_layer.objects.active = parts[0]
    for p in parts:
        p.select_set(True)
    bpy.ops.object.join()
    obj = bpy.context.active_object
    assert obj is not None
    obj.name = "Character"
    return obj


def _smart_uv_unwrap(obj: bpy.types.Object) -> None:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


def _export_glb(path: Path, require_tangents: bool) -> None:
    _ensure_parent_dir(path)
    bpy.ops.export_scene.gltf(
        filepath=str(path),
        export_format="GLB",
        export_apply=True,
        export_normals=True,
        export_tangents=require_tangents,
        export_texcoords=True,
    )


def _import_glb(path: Path) -> None:
    bpy.ops.import_scene.gltf(filepath=str(path))


def _gather_mesh_objects() -> list[bpy.types.Object]:
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def _bounds_world(objs: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    if not objs:
        return Vector((0.0, 0.0, 0.0)), Vector((0.0, 0.0, 0.0))
    mins = Vector((math.inf, math.inf, math.inf))
    maxs = Vector((-math.inf, -math.inf, -math.inf))
    for obj in objs:
        for corner in obj.bound_box:
            v = obj.matrix_world @ Vector(corner)
            mins.x = min(mins.x, v.x)
            mins.y = min(mins.y, v.y)
            mins.z = min(mins.z, v.z)
            maxs.x = max(maxs.x, v.x)
            maxs.y = max(maxs.y, v.y)
            maxs.z = max(maxs.z, v.z)
    return mins, maxs


def _setup_render(res: int = 512) -> None:
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.render.resolution_x = res
    scene.render.resolution_y = res
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False


def _ensure_camera() -> bpy.types.Object:
    scene = bpy.context.scene
    cam = next((o for o in scene.objects if o.type == "CAMERA"), None)
    if cam is not None:
        return cam
    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    assert cam is not None
    return cam


def _ensure_light() -> None:
    scene = bpy.context.scene
    if any(o.type == "LIGHT" for o in scene.objects):
        return
    bpy.ops.object.light_add(type="AREA", location=(2.5, -2.5, 3.0))
    key = bpy.context.active_object
    assert key is not None
    key.data.energy = 900  # type: ignore[attr-defined]
    key.data.size = 3.0  # type: ignore[attr-defined]

    bpy.ops.object.light_add(type="AREA", location=(-2.0, 1.5, 1.2))
    fill = bpy.context.active_object
    assert fill is not None
    fill.data.energy = 250  # type: ignore[attr-defined]
    fill.data.size = 2.0  # type: ignore[attr-defined]


def _point_camera_at(cam: bpy.types.Object, target: Vector) -> None:
    direction = target - cam.location
    rot_quat = direction.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot_quat.to_euler()


def _render_turntable(asset_id: str, out_root: Path, center: Vector, radius: float) -> Path:
    scene = bpy.context.scene
    cam = _ensure_camera()
    cam.data.type = "PERSP"  # type: ignore[attr-defined]

    dist = max(1.8 * radius, 1.5)
    cam.location = center + Vector((dist, -dist, dist * 0.75))
    _point_camera_at(cam, center)

    _ensure_light()
    mat = _make_material("TurntableMat")
    _assign_material_to_meshes(mat)

    out_path = out_root / "previews" / f"{asset_id}_turntable.png"
    _ensure_parent_dir(out_path)
    scene.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)
    return out_path


def _render_ortho(asset_id: str, out_root: Path, center: Vector, size: float) -> Path:
    scene = bpy.context.scene
    cam = _ensure_camera()
    cam.data.type = "ORTHO"  # type: ignore[attr-defined]
    cam.data.ortho_scale = max(size * 1.35, 1.0)  # type: ignore[attr-defined]

    cam.location = center + Vector((0.0, -3.0, 0.0))
    _point_camera_at(cam, center)

    # Silhouette-friendly: white emission on black background.
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    assert nt is not None
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out_node = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(bg.outputs["Background"], out_node.inputs["Surface"])

    mat = _make_material("OrthoSilhouette", emission=(1.0, 1.0, 1.0, 1.0))
    _assign_material_to_meshes(mat)

    out_path = out_root / "previews" / f"{asset_id}_ortho.png"
    _ensure_parent_dir(out_path)
    scene.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)
    return out_path


def _mesh_metrics(require_uvs: bool, require_normals: bool, require_tangents: bool) -> tuple[dict, list[str], list[str]]:
    depsgraph = bpy.context.evaluated_depsgraph_get()
    metrics: dict = {}
    errors: list[str] = []
    warnings: list[str] = []

    triangle_count = 0
    uv_layers_total = 0
    uv_area_total = 0.0
    meshes_missing_uv = 0
    meshes_missing_normals = 0
    non_manifold_edges = 0
    loose_verts = 0
    loose_edges = 0

    mesh_objs = _gather_mesh_objects()
    if not mesh_objs:
        errors.append("no mesh objects found in scene")
        return metrics, errors, warnings

    for obj in mesh_objs:
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        try:
            mesh.calc_loop_triangles()
            triangle_count += len(mesh.loop_triangles)

            uv_layers_total += len(mesh.uv_layers)
            if not mesh.uv_layers:
                meshes_missing_uv += 1
            else:
                uv_layer = mesh.uv_layers.active or mesh.uv_layers[0]
                uvs = uv_layer.data
                for tri in mesh.loop_triangles:
                    a = uvs[tri.loops[0]].uv
                    b = uvs[tri.loops[1]].uv
                    c = uvs[tri.loops[2]].uv
                    area = abs((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)) * 0.5
                    uv_area_total += float(area)

            if require_normals:
                try:
                    mesh.calc_normals_split()
                except Exception:  # noqa: BLE001
                    meshes_missing_normals += 1

            if require_tangents:
                if not mesh.uv_layers:
                    errors.append("tangents required but no UVs present")
                else:
                    uv_name = (mesh.uv_layers.active or mesh.uv_layers[0]).name
                    try:
                        mesh.calc_tangents(uvmap=uv_name)
                    except Exception as e:  # noqa: BLE001
                        errors.append(f"failed to calculate tangents ({e})")

            bm = bmesh.new()
            bm.from_mesh(mesh)
            non_manifold_edges += sum(1 for e in bm.edges if not e.is_manifold)
            loose_edges += sum(1 for e in bm.edges if len(e.link_faces) == 0)
            loose_verts += sum(1 for v in bm.verts if len(v.link_edges) == 0)
            bm.free()
        finally:
            eval_obj.to_mesh_clear()

    metrics["triangle_count"] = triangle_count
    metrics["uv_layers"] = uv_layers_total
    metrics["uv_area_total"] = uv_area_total
    metrics["meshes_missing_uv"] = meshes_missing_uv
    metrics["meshes_missing_normals"] = meshes_missing_normals
    metrics["non_manifold_edges"] = non_manifold_edges
    metrics["loose_edges"] = loose_edges
    metrics["loose_verts"] = loose_verts

    if require_uvs:
        if meshes_missing_uv > 0:
            errors.append(f"UVs required but {meshes_missing_uv} mesh(es) have no UV layers")
        elif uv_area_total <= 1e-6:
            errors.append("UVs required but UV area appears degenerate (near-zero)")

    if require_normals:
        if meshes_missing_normals > 0:
            errors.append(f"normals required but failed to calculate split normals on {meshes_missing_normals} mesh(es)")

    if non_manifold_edges > 0:
        errors.append(f"non-manifold edges detected ({non_manifold_edges})")

    if loose_edges > 0 or loose_verts > 0:
        warnings.append(f"loose geometry detected (edges={loose_edges}, verts={loose_verts})")

    return metrics, errors, warnings


def _load_report(path: Path) -> dict:
    if not path.exists():
        return {"ok": True, "errors": [], "warnings": [], "metrics": {}, "previews": {}}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {"ok": True}


def _write_report(path: Path, report: dict) -> None:
    _ensure_parent_dir(path)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    argv = sys.argv
    if "--" not in argv:
        print("error: expected '--' followed by args", file=sys.stderr)
        return 2
    args = _parse_args(argv[argv.index("--") + 1 :])

    spec_path = Path(args.spec).resolve()
    out_root = Path(args.out_root).resolve()
    report_path = Path(args.report).resolve()

    spec = _load_json(spec_path)
    asset_id = spec.get("asset_id", "unknown")
    asset_type = spec.get("asset_type")

    if asset_type not in ("mesh_3d_hardsurface", "character_3d_lowpoly"):
        print(f"error: unsupported 3D asset_type '{asset_type}'", file=sys.stderr)
        return 2

    seed = int(spec.get("seed", 0))
    random.seed(seed)

    model_rel = _first_primary_glb_output(spec)
    model_path = (out_root / model_rel).resolve()

    export = spec.get("export", {}) if isinstance(spec.get("export", {}), dict) else {}
    require_uvs = bool(export.get("require_uvs", True))
    require_normals = bool(export.get("require_normals", True))
    require_tangents = bool(export.get("require_tangents", False))

    triangle_budget = int(spec.get("triangle_budget", 0))

    _clear_scene()
    _setup_render()

    report = _load_report(report_path)
    report.setdefault("errors", [])
    report.setdefault("warnings", [])
    report.setdefault("metrics", {})
    report.setdefault("previews", {})

    generated_placeholder = False
    if not model_path.exists() and args.generate_placeholder:
        generated_placeholder = True
        if asset_type == "mesh_3d_hardsurface":
            obj = _create_hardsurface_prop(seed)
        else:
            obj = _create_lowpoly_character(seed)
        _smart_uv_unwrap(obj)
        _export_glb(model_path, require_tangents=require_tangents)

    if not model_path.exists():
        report["ok"] = False
        report["errors"].append(f"missing model file: {model_path}")
        report["metrics"]["model_path"] = str(model_path)
        _write_report(report_path, report)
        return 1

    try:
        _import_glb(model_path)
    except Exception as e:  # noqa: BLE001
        report["ok"] = False
        report["errors"].append(f"failed to import glb: {e}")
        report["metrics"]["model_path"] = str(model_path)
        _write_report(report_path, report)
        return 1

    meshes = _gather_mesh_objects()
    mins, maxs = _bounds_world(meshes)
    center = (mins + maxs) * 0.5
    size = max(maxs.x - mins.x, maxs.y - mins.y, maxs.z - mins.z)
    radius = max(size * 0.5, 0.25)

    turntable_path = _render_turntable(asset_id, out_root, center=center, radius=radius)
    ortho_path = _render_ortho(asset_id, out_root, center=center, size=size)

    report["previews"]["turntable_png"] = str(turntable_path)
    report["previews"]["ortho_png"] = str(ortho_path)
    report["metrics"]["model_path"] = str(model_path)
    report["metrics"]["generated_placeholder_model"] = generated_placeholder

    metrics, errors, warnings = _mesh_metrics(
        require_uvs=require_uvs,
        require_normals=require_normals,
        require_tangents=require_tangents,
    )
    report["metrics"].update(metrics)

    # Budget checks (narrow and actionable).
    if triangle_budget > 0:
        report["metrics"]["triangle_budget"] = triangle_budget
        if metrics.get("triangle_count", 0) > triangle_budget:
            errors.append(f"triangle_count {metrics.get('triangle_count')} exceeds triangle_budget {triangle_budget}")

    report["errors"].extend(errors)
    report["warnings"].extend(warnings)
    report["ok"] = len(report["errors"]) == 0

    _write_report(report_path, report)

    if args.mode == "validate":
        return 0 if report["ok"] else 1
    return 0


raise SystemExit(main())
