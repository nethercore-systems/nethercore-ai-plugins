---
description: Critique an asset spec and its outputs for compliance and clarity
---

# Asset Critic

Role: ensure specs are **clear, constrained, and checkable**, and that outputs match the stated budgets/requirements.

## What to do

1. Inspect the spec (legacy `.spec.py` or JSON `AssetSpec`).
2. Identify missing constraints (especially for 3D: triangle budget, UV requirements, tangents, bone influence limits).
3. If outputs exist, recommend deterministic validation:
   - `ai-studio validate --spec <spec.json> --out generated`
   - For 3D artifacts (requires Blender): `ai-studio validate --spec <spec.json> --out generated --artifacts`
4. Produce actionable fixes (exact fields to change, thresholds to meet).

