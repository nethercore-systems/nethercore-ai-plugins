from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal


_BLENDER_ONLY_CATEGORIES = {"meshes", "characters", "animations"}


def _spec_category(spec_path: Path) -> str | None:
    parts = spec_path.parts
    try:
        idx = parts.index("specs")
    except ValueError:
        return None
    if idx + 1 >= len(parts):
        return None
    return parts[idx + 1]


def build_legacy_generate_argv(
    *,
    project_root: Path,
    blender_bin: str | None,
    only: str | None,
    spec: str | None,
    dry_run: bool,
) -> list[str]:
    studio_entry = Path(".studio") / "generate.py"

    use_blender = False
    if only in _BLENDER_ONLY_CATEGORIES:
        use_blender = True
    elif spec is not None:
        cat = _spec_category(Path(spec))
        if cat in _BLENDER_ONLY_CATEGORIES:
            use_blender = True

    args: list[str] = []
    if use_blender:
        if blender_bin is None:
            raise RuntimeError("blender not found (required for meshes/characters/animations)")
        args.extend([blender_bin, "--background", "--python", str(studio_entry), "--"])
    else:
        args.extend([sys.executable, str(studio_entry)])

    if only:
        args.extend(["--only", only])
    if spec:
        args.extend(["--spec", spec])
    if dry_run:
        args.append("--dry-run")

    return args


def validate_legacy_project(project_root: Path) -> None:
    studio_entry = project_root / ".studio" / "generate.py"
    if not studio_entry.exists():
        raise FileNotFoundError(f"missing legacy studio generator: {studio_entry} (run: ai-studio init)")


Mode = Literal["legacy_studio"]

