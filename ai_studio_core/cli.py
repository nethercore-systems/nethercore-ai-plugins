from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from . import __version__


@dataclass(frozen=True)
class DoctorResult:
    name: str
    found: bool
    detail: str


def _command_path(name: str) -> str | None:
    return shutil.which(name)


def _run_doctor() -> tuple[int, list[DoctorResult]]:
    checks: list[DoctorResult] = []

    blender_path = _command_path("blender")
    checks.append(
        DoctorResult(
            name="blender",
            found=blender_path is not None,
            detail=blender_path or "not found (required for 3D preview/validation)",
        )
    )

    ffmpeg_path = _command_path("ffmpeg")
    checks.append(
        DoctorResult(
            name="ffmpeg",
            found=ffmpeg_path is not None,
            detail=ffmpeg_path or "not found (optional; used for video encodes)",
        )
    )

    missing_required = any((c.name == "blender" and not c.found) for c in checks)
    return (1 if missing_required else 0), checks


def cmd_doctor(_: argparse.Namespace) -> int:
    code, checks = _run_doctor()
    print("ai-studio doctor")
    for c in checks:
        status = "OK" if c.found else "MISSING"
        print(f"- {c.name}: {status} ({c.detail})")
    return code


def cmd_init(args: argparse.Namespace) -> int:
    from .project_init import init_project

    project_dir = Path(args.project_dir) if args.project_dir else Path(".")
    init_project(project_dir)
    print(f"OK: installed .studio scaffold into {project_dir.resolve()}")
    print("Pinned: ai_studio.toml (core_version)")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    from .legacy_studio import build_legacy_generate_argv, validate_legacy_project

    project_root = Path(getattr(args, "project", ".")) if getattr(args, "project", None) else Path(".")
    project_root = project_root.resolve()

    try:
        validate_legacy_project(project_root)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    blender_bin = _command_path("blender")
    try:
        argv = build_legacy_generate_argv(
            project_root=project_root,
            blender_bin=blender_bin,
            only=getattr(args, "only", None),
            spec=getattr(args, "spec", None),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except RuntimeError as e:
        print(f"error: {e}. Run: ai-studio doctor", file=sys.stderr)
        return 2

    proc = subprocess.run(argv, check=False, cwd=project_root)
    return int(proc.returncode)


def _base_report(*, spec, spec_path: Path) -> dict:
    return {
        "ok": True,
        "asset_id": spec.asset_id,
        "asset_type": str(getattr(spec.asset_type, "value", spec.asset_type)),
        "core_version": __version__,
        "spec_path": str(spec_path),
        "outputs": [
            {"kind": o.kind.value, "format": o.format.value, "path": o.path}
            for o in spec.outputs  # type: ignore[attr-defined]
        ],
        "errors": [],
        "warnings": [],
        "metrics": {},
        "previews": {},
    }


def _run_blender(
    *,
    blender_path: Path,
    mode: str,
    spec_path: Path,
    out_root: Path,
    report_path: Path,
    generate_placeholder: bool,
) -> int:
    script = resources.files("ai_studio_core.blender").joinpath("entrypoint.py")
    with resources.as_file(script) as script_path:
        argv = [
            str(blender_path),
            "--background",
            "--factory-startup",
            "--python",
            str(script_path),
            "--",
            "--mode",
            mode,
            "--spec",
            str(spec_path.resolve()),
            "--out-root",
            str(out_root.resolve()),
            "--report",
            str(report_path.resolve()),
        ]
        if generate_placeholder:
            argv.append("--generate-placeholder")
        proc = subprocess.run(argv, check=False)
        return int(proc.returncode)


def cmd_validate(args: argparse.Namespace) -> int:
    if not args.spec:
        print("error: --spec is required", file=sys.stderr)
        return 2

    try:
        from .specs.io import dump_json, load_asset_spec_json
    except ModuleNotFoundError as e:
        if e.name == "pydantic":
            print("error: validation requires pydantic. Install with: pip install -e .", file=sys.stderr)
            return 2
        raise

    try:
        spec = load_asset_spec_json(args.spec)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    from .config import load_config

    cfg = load_config(Path(".").resolve())
    out_root = Path(args.out) if args.out else Path(cfg.paths_output_root)
    report_path = out_root / "reports" / f"{spec.asset_id}.report.json"

    report = _base_report(spec=spec, spec_path=Path(args.spec))
    dump_json(report, report_path)

    asset_type = report["asset_type"]
    if asset_type in ("mesh_3d_hardsurface", "character_3d_lowpoly"):
        blender_bin = _command_path("blender")
        if blender_bin is None:
            report["ok"] = False
            report["errors"].append("blender not found (required for 3D artifact validation/preview)")
            dump_json(report, report_path)
            print("Validation failed: blender not found. Run: ai-studio doctor", file=sys.stderr)
            print(f"Report: {report_path}")
            return 2

        code = _run_blender(
            blender_path=Path(blender_bin),
            mode="validate",
            spec_path=Path(args.spec),
            out_root=out_root,
            report_path=report_path,
            generate_placeholder=bool(getattr(args, "generate_placeholder", False)),
        )
        try:
            final = json.loads(report_path.read_text(encoding="utf-8"))
            ok = bool(final.get("ok")) if isinstance(final, dict) else False
        except Exception:  # noqa: BLE001
            ok = False
        print(f"Report: {report_path}")
        return 0 if (code == 0 and ok) else 1

    print(f"OK: {spec.asset_id} ({asset_type})")
    print(f"Report: {report_path}")
    return 0


def cmd_preview(args: argparse.Namespace) -> int:
    if not args.spec:
        print("error: --spec is required", file=sys.stderr)
        return 2

    blender_bin = _command_path("blender")
    if blender_bin is None:
        print("error: blender not found (required for 3D preview). Run: ai-studio doctor", file=sys.stderr)
        return 2

    try:
        from .specs.io import dump_json, load_asset_spec_json
    except ModuleNotFoundError as e:
        if e.name == "pydantic":
            print("error: preview requires pydantic. Install with: pip install -e .", file=sys.stderr)
            return 2
        raise

    try:
        spec = load_asset_spec_json(args.spec)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    asset_type = str(getattr(spec.asset_type, "value", spec.asset_type))
    if asset_type not in ("mesh_3d_hardsurface", "character_3d_lowpoly"):
        print(f"error: preview currently supports only 3D specs (got {asset_type})", file=sys.stderr)
        return 2

    from .config import load_config

    cfg = load_config(Path(".").resolve())
    out_root = Path(args.out) if args.out else Path(cfg.paths_output_root)
    report_path = out_root / "reports" / f"{spec.asset_id}.report.json"

    report = _base_report(spec=spec, spec_path=Path(args.spec))
    dump_json(report, report_path)

    code = _run_blender(
        blender_path=Path(blender_bin),
        mode="preview",
        spec_path=Path(args.spec),
        out_root=out_root,
        report_path=report_path,
        generate_placeholder=True,
    )
    if code != 0:
        print(f"Report: {report_path}")
        return code

    try:
        final = json.loads(report_path.read_text(encoding="utf-8"))
        previews = final.get("previews", {}) if isinstance(final, dict) else {}
    except Exception:  # noqa: BLE001
        previews = {}

    if isinstance(previews, dict):
        if previews.get("turntable_png"):
            print(f"Turntable: {previews['turntable_png']}")
        if previews.get("ortho_png"):
            print(f"Ortho: {previews['ortho_png']}")
    print(f"Report: {report_path}")
    return 0


def cmd_lint_repo(args: argparse.Namespace) -> int:
    from .lint_repo import lint_repo

    repo_root = Path(args.repo_root).resolve()
    messages = lint_repo(repo_root)

    errors = [m for m in messages if m.level == "error"]
    warnings = [m for m in messages if m.level == "warning"]

    for m in errors:
        print(f"ERROR: {m.message}", file=sys.stderr)
    for m in warnings:
        print(f"WARNING: {m.message}", file=sys.stderr)

    if errors:
        print(f"lint-repo: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))", file=sys.stderr)
        return 1

    print(f"lint-repo: OK ({len(warnings)} warning(s))")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-studio", description="AI Asset Studio core CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser("init", help="Install/upgrade a project scaffold")
    init_p.add_argument("project_dir", nargs="?", help="Target project directory (default: current directory)")
    init_p.set_defaults(func=cmd_init)

    gen_p = subparsers.add_parser("generate", help="Run generation from a spec")
    gen_p.add_argument("--project", help="Target project directory (default: current directory)")
    gen_p.add_argument("--spec", help="Path to a legacy .studio spec (e.g. .studio/specs/textures/foo.spec.py)")
    gen_p.add_argument("--only", help="Legacy .studio category (textures/normals/sounds/instruments/music/meshes/characters/animations)")
    gen_p.add_argument("--dry-run", action="store_true", help="Print what would be generated without writing outputs")
    gen_p.add_argument("--out", help="(reserved) Output directory (default: project convention)")
    gen_p.set_defaults(func=cmd_generate)

    val_p = subparsers.add_parser("validate", help="Validate a spec and/or output artifacts")
    val_p.add_argument("--spec", help="Path to an asset spec")
    val_p.add_argument("--out", help="Output directory root (default: generated/)")
    val_p.add_argument(
        "--generate-placeholder",
        action="store_true",
        help="If the 3D model is missing, generate a deterministic placeholder before validating",
    )
    val_p.set_defaults(func=cmd_validate)

    prev_p = subparsers.add_parser("preview", help="Render deterministic previews (thumbnails/turntables)")
    prev_p.add_argument("--spec", help="Path to an asset spec")
    prev_p.add_argument("--out", help="Output directory root (default: generated/)")
    prev_p.set_defaults(func=cmd_preview)

    doc_p = subparsers.add_parser("doctor", help="Diagnose tool dependencies (blender, ffmpeg, etc.)")
    doc_p.set_defaults(func=cmd_doctor)

    lint_p = subparsers.add_parser("lint-repo", help="Lint repo internals (references, templates, examples)")
    lint_p.add_argument("--repo-root", default=".", help="Path to the nethercore-ai-plugins repo root")
    lint_p.set_defaults(func=cmd_lint_repo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help(sys.stderr)
        return 2
    return int(func(args))
