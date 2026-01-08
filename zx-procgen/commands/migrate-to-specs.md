---
description: Migrate ad-hoc asset generation to a spec-driven workflow
argument-hint: ""
allowed-tools: ["Read"]
---

# Migrate to Specs

Use this when a project currently has hand-made assets or one-off generator scripts and you want to standardize on a spec-driven workflow.

## Steps

1. Install `.studio/` scaffolding with `ai-studio init` (preferred) or `/init-procgen`.
2. Create specs under `.studio/specs/**` for existing assets (one spec per output artifact).
3. Use `ai-studio validate --spec <spec.json>` for JSON AssetSpecs (core contract).
4. For legacy `.spec.py` specs, run generation via `ai-studio generate`.

## Future work

Full automated migration from legacy `.spec.py` to JSON `AssetSpec` is intentionally out of scope for now.

