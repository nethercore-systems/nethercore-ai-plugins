# Parser Roadmap (zx-procgen)

This document tracks planned improvements for the legacy `.studio/` parser-based pipeline.

## Current Direction

The canonical scaffold now lives in:

- `ai_studio_core/templates/project/studio/`

Plugins should orchestrate usage via the core CLI:

- `ai-studio init`
- `ai-studio generate`
- `ai-studio validate`
- `ai-studio preview`

## Planned Enhancements (Future)

- Migrate legacy `.spec.py` formats to strict JSON `AssetSpec` per asset type
- Expand validators and reports (especially for 3D determinism)
- Replace ad-hoc pipeline steps in plugins with `ai-studio` CLI calls only

See `docs/ROADMAP_CORE_SPLIT.md` for the cross-repo plan and phase definitions.

