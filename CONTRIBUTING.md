# Contributing (nethercore-ai-plugins / ai-studio-core)

This repo contains two layers:

- **Plugin packs** (Markdown/JSON skills, commands, agents)
- **`ai-studio-core`** (a stable Python package + CLI for specs, validation, previews)

Core goal: keep workflows working while making the core **deterministic and checkable**.

## Local Setup (Core)

```bash
python3 -m pip install -e .
```

Verify:

```bash
ai-studio --help
ai-studio lint-repo --repo-root .
ai-studio validate --spec templates/specs/texture_2d_brick_wall.json --out generated
```

### 3D (optional)

3D preview/validation requires Blender on PATH.

```bash
ai-studio doctor
ai-studio preview --spec templates/specs/mesh_3d_hardsurface_crate.json --out generated
ai-studio validate --spec templates/specs/mesh_3d_hardsurface_crate.json --out generated --artifacts --generate-placeholder
```

Scope guardrails:

- Supported 3D types: **hardsurface props** + **lowpoly characters** only
- Anything organic/cloth/etc is out of scope for now (document as future work)

## Adding a New Asset Type (Core Contract)

When you add an asset type, it must be **fully checkable**:

1. Add a new schema in `ai_studio_core/specs/models.py`
   - Add to `AssetType`
   - Add a Pydantic model with `extra="forbid"`
   - Add explicit numeric budgets/constraints (avoid open-ended fields)
2. Add at least one example spec in `templates/specs/`
3. Document the fields/rules in `docs/SPEC_REFERENCE.md`
4. Update `ai_studio_core/lint_repo.py` if the new type adds new referenced resources (presets, templates, etc.)

## Validation Standards

`ai-studio validate` must:

- Fail with actionable messages (no stack traces)
- Produce a report JSON under `<out>/reports/<asset_id>.report.json`
- For 3D types: include preview paths and geometry metrics when Blender is available

## CI

CI is defined in `.github/workflows/ci.yml` and enforces:

- `ai-studio lint-repo`
- Validation of all `templates/specs/*.json`

To run the same checks locally:

```bash
ai-studio lint-repo --repo-root .
for spec in templates/specs/*.json; do
  ai-studio validate --spec "$spec" --out generated-ci
done
```
