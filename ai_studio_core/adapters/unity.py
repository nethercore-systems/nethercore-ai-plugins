from __future__ import annotations

import json
import shutil
from pathlib import Path

from ..config import load_config


def export_from_report(*, report_path: Path, dest_root: Path) -> Path:
    """
    Minimal adapter: copies validated outputs into a Unity-friendly folder layout and
    writes a small manifest JSON. Does not require Unity installed.
    """
    report_path = report_path.resolve()
    dest_root = dest_root.resolve()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("report JSON must be an object")

    out_root = report_path.parent.parent
    project_root = out_root.parent
    cfg = load_config(project_root)

    outputs = report.get("outputs", [])
    if not isinstance(outputs, list):
        raise ValueError("report.outputs must be a list")

    copied: list[str] = []
    unity_assets = dest_root / "Assets" / "AIStudio"
    for o in outputs:
        if not isinstance(o, dict):
            continue
        rel = o.get("path")
        if not isinstance(rel, str):
            continue
        src = out_root / rel
        dst = unity_assets / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)
            copied.append(rel)

    manifest = {
        "engine": "unity",
        "engine_default_targets": list(cfg.engine_default_targets),
        "conventions": {
            "units": cfg.convention_units,
            "up_axis": cfg.convention_up_axis,
            "forward_axis": cfg.convention_forward_axis,
            "scale": cfg.convention_scale,
        },
        "copied_files": copied,
        "source_report": str(report_path),
    }

    dest_root.mkdir(parents=True, exist_ok=True)
    manifest_path = dest_root / "ai_studio_unity_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path

