from __future__ import annotations

import re
import shutil
from importlib import resources
from pathlib import Path

from . import __version__


_CATEGORIES = [
    "textures",
    "normals",
    "sounds",
    "instruments",
    "music",
    "meshes",
    "characters",
    "animations",
]


def _write_core_version_config(project_root: Path) -> None:
    cfg = project_root / "ai_studio.toml"
    line = f'core_version = "{__version__}"\n'
    if not cfg.exists():
        cfg.write_text(
            "# ai-studio project configuration\n" + line,
            encoding="utf-8",
        )
        return

    text = cfg.read_text(encoding="utf-8")
    if re.search(r'^\s*core_version\s*=\s*".*"\s*$', text, flags=re.MULTILINE):
        text = re.sub(r'^\s*core_version\s*=\s*".*"\s*$', line.strip(), text, flags=re.MULTILINE) + "\n"
        cfg.write_text(text, encoding="utf-8")
        return

    cfg.write_text(text.rstrip() + "\n\n" + line, encoding="utf-8")


def _ensure_generated_gitignore(generated_root: Path) -> None:
    generated_root.mkdir(parents=True, exist_ok=True)
    gi = generated_root / ".gitignore"
    if gi.exists():
        return
    gi.write_text(
        "# Generated assets - regenerate with: ai-studio generate\n*\n!.gitignore\n",
        encoding="utf-8",
    )


def init_project(project_root: Path) -> None:
    project_root = project_root.resolve()
    studio_root = project_root / ".studio"

    studio_root.mkdir(parents=True, exist_ok=True)
    for p in ["specs", "direction", "designs", "analysis"]:
        (studio_root / p).mkdir(parents=True, exist_ok=True)

    # Preserve user data under .studio/specs/** etc, but overwrite generator + parsers.
    dst_generate = studio_root / "generate.py"
    dst_parsers = studio_root / "parsers"

    template_root = resources.files("ai_studio_core").joinpath("templates/project/studio")
    with resources.as_file(template_root) as src_root:
        shutil.copy2(src_root / "generate.py", dst_generate)

        if dst_parsers.exists():
            shutil.rmtree(dst_parsers)
        shutil.copytree(src_root / "parsers", dst_parsers)

    # Ensure spec category folders exist (preserve contents).
    for cat in _CATEGORIES:
        (studio_root / "specs" / cat).mkdir(parents=True, exist_ok=True)

    # Output directories (legacy conventions used by .studio/generate.py).
    generated = project_root / "generated"
    for p in [
        generated / "textures",
        generated / "normals",
        generated / "meshes",
        generated / "characters",
        generated / "animations",
        generated / "sounds" / "instruments",
        generated / "music",
    ]:
        p.mkdir(parents=True, exist_ok=True)
    _ensure_generated_gitignore(generated)

    _write_core_version_config(project_root)

