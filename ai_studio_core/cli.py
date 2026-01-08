from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
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
    print("ai-studio init: not implemented yet", file=sys.stderr)
    if args.project_dir:
        _ = Path(args.project_dir)
    return 2


def cmd_generate(args: argparse.Namespace) -> int:
    print("ai-studio generate: not implemented yet", file=sys.stderr)
    _ = args
    return 2


def cmd_validate(args: argparse.Namespace) -> int:
    print("ai-studio validate: not implemented yet", file=sys.stderr)
    _ = args
    return 2


def cmd_preview(args: argparse.Namespace) -> int:
    print("ai-studio preview: not implemented yet", file=sys.stderr)
    _ = args
    return 2


def cmd_lint_repo(args: argparse.Namespace) -> int:
    print("ai-studio lint-repo: not implemented yet", file=sys.stderr)
    _ = args
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-studio", description="AI Asset Studio core CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser("init", help="Install/upgrade a project scaffold")
    init_p.add_argument("project_dir", nargs="?", help="Target project directory (default: current directory)")
    init_p.set_defaults(func=cmd_init)

    gen_p = subparsers.add_parser("generate", help="Run generation from a spec")
    gen_p.add_argument("--spec", help="Path to an asset spec")
    gen_p.add_argument("--out", help="Output directory (default: project convention)")
    gen_p.set_defaults(func=cmd_generate)

    val_p = subparsers.add_parser("validate", help="Validate a spec and/or output artifacts")
    val_p.add_argument("--spec", help="Path to an asset spec")
    val_p.add_argument("--out", help="Output directory root (default: generated/)")
    val_p.set_defaults(func=cmd_validate)

    prev_p = subparsers.add_parser("preview", help="Render deterministic previews (thumbnails/turntables)")
    prev_p.add_argument("--spec", help="Path to an asset spec")
    prev_p.add_argument("--out", help="Output directory root (default: generated/)")
    prev_p.set_defaults(func=cmd_preview)

    doc_p = subparsers.add_parser("doctor", help="Diagnose tool dependencies (blender, ffmpeg, etc.)")
    doc_p.set_defaults(func=cmd_doctor)

    lint_p = subparsers.add_parser("lint-repo", help="Lint repo internals (references, templates, examples)")
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

