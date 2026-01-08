from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .models import AssetSpec, format_validation_error, parse_asset_spec


def load_asset_spec_json(path: str | Path) -> AssetSpec:
    spec_path = Path(path)
    raw = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("spec JSON must be an object at the top level")
    try:
        return parse_asset_spec(raw)
    except ValidationError as e:
        msg = format_validation_error(e)
        raise ValueError(msg) from None


def dump_json(data: Any, path: str | Path) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

