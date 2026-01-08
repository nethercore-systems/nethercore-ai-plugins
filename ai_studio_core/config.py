from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _load_toml_bytes(path: Path) -> dict[str, Any]:
    try:
        import tomllib  # py311+
    except ModuleNotFoundError:  # pragma: no cover
        import tomli as tomllib  # type: ignore[no-redef]

    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("ai_studio.toml must parse to a table/object")
    return raw


@dataclass(frozen=True)
class StudioConfig:
    core_version: str | None = None
    engine_default_targets: tuple[str, ...] = ("godot",)
    export_model_3d: str = "glb"
    export_texture_2d: str = "png"
    export_audio_sfx: str = "wav"
    export_music: str = "xm"
    convention_units: str = "meters"
    convention_up_axis: str = "Y"
    convention_forward_axis: str = "-Z"
    convention_scale: float = 1.0
    paths_output_root: str = "generated"
    paths_studio_root: str = ".studio"


def load_config(project_root: Path) -> StudioConfig:
    cfg_path = project_root / "ai_studio.toml"
    if not cfg_path.exists():
        return StudioConfig()

    raw = _load_toml_bytes(cfg_path)

    engine = raw.get("engine", {}) if isinstance(raw.get("engine", {}), dict) else {}
    export = raw.get("export", {}) if isinstance(raw.get("export", {}), dict) else {}
    conventions = raw.get("conventions", {}) if isinstance(raw.get("conventions", {}), dict) else {}
    paths = raw.get("paths", {}) if isinstance(raw.get("paths", {}), dict) else {}

    default_targets = engine.get("default_targets")
    if isinstance(default_targets, list) and all(isinstance(x, str) for x in default_targets):
        engine_default_targets: tuple[str, ...] = tuple(default_targets)
    else:
        engine_default_targets = StudioConfig.engine_default_targets

    return StudioConfig(
        core_version=raw.get("core_version") if isinstance(raw.get("core_version"), str) else None,
        engine_default_targets=engine_default_targets,
        export_model_3d=export.get("model_3d") if isinstance(export.get("model_3d"), str) else StudioConfig.export_model_3d,
        export_texture_2d=export.get("texture_2d")
        if isinstance(export.get("texture_2d"), str)
        else StudioConfig.export_texture_2d,
        export_audio_sfx=export.get("audio_sfx") if isinstance(export.get("audio_sfx"), str) else StudioConfig.export_audio_sfx,
        export_music=export.get("music") if isinstance(export.get("music"), str) else StudioConfig.export_music,
        convention_units=conventions.get("units") if isinstance(conventions.get("units"), str) else StudioConfig.convention_units,
        convention_up_axis=conventions.get("up_axis")
        if isinstance(conventions.get("up_axis"), str)
        else StudioConfig.convention_up_axis,
        convention_forward_axis=conventions.get("forward_axis")
        if isinstance(conventions.get("forward_axis"), str)
        else StudioConfig.convention_forward_axis,
        convention_scale=float(conventions.get("scale"))
        if isinstance(conventions.get("scale"), (int, float))
        else StudioConfig.convention_scale,
        paths_output_root=paths.get("output_root") if isinstance(paths.get("output_root"), str) else StudioConfig.paths_output_root,
        paths_studio_root=paths.get("studio_root") if isinstance(paths.get("studio_root"), str) else StudioConfig.paths_studio_root,
    )

