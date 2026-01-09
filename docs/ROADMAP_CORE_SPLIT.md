# ROADMAP: Split “AI Asset Studio Core” from Plugin Packs

Historically this repo mixed:

- **Plugin packs** (Claude Code/Codex skills/commands/agents; mostly Markdown/JSON)
- **A project scaffold + pipeline code**

It is now split into a stable, versioned **core** repo (`ai-studio-core`) and this fast-iterating **plugin ecosystem** repo (`nethercore-ai-plugins`).

## 1) Inventory: What Exists Today

### Plugin packs (docs + prompts)

Top-level plugin folders:

- `ai-game-studio/` — orchestration / project health / dispatch queue patterns
- `creative-direction/` — art/sound/tech direction agents + skills
- `game-design/` — design agents + skills
- `sound-design/` — sound design agents + skills
- `tracker-music/` — tracker composition guidance + example Python snippets
- `zx-*` (`zx-dev/`, `zx-procgen/`, `zx-orchestrator/`, `zx-publish/`, `zx-test/`, etc.) — ZX/Nethercore-specific workflows

### Pipeline code + scaffold

The “real” pipeline implementation shipped as files is the `.studio/` scaffold:

- `ai_studio_core/templates/project/studio/generate.py` — unified generator entrypoint (in `ai-studio-core`)
- `ai_studio_core/templates/project/studio/parsers/**` — category parsers (textures, normals, sounds, music, meshes, characters, animations) (in `ai-studio-core`)

This scaffold is copied into user projects via `ai-studio init` (preferred) or the legacy `init-procgen` command and becomes the executable pipeline inside the project.

## 2) Stable Contracts That Belong in Core

Core should own the parts that must be deterministic, validated, and stable over time:

### Specs (machine-validated)

- **AssetSpec schema(s)** for each asset type (strict, low ambiguity; especially for 3D)
- Example specs and templates
- A single, versioned spec reference doc

### Entrypoints (CLI surface)

- `ai-studio init` — install/upgrade scaffolds and templates into a project
- `ai-studio generate` — run generation from a spec (initially wraps existing `.studio` pipelines)
- `ai-studio validate` — validate specs and output artifacts (report JSON)
- `ai-studio preview` — deterministic preview rendering (especially for 3D)
- `ai-studio doctor` — dependency diagnosis (Blender/ffmpeg/etc.)
- `ai-studio lint-repo` — repo integrity checks (references resolve; examples validate)

### Validators + Reports

- A stable **report JSON format** (pass/fail, metrics, warnings, paths)
- A deterministic validator harness so CI can enforce correctness

### Preview Rendering (3D determinism)

- Headless Blender rendering for:
  - turntable thumbnail
  - silhouette-friendly ortho render
- Metrics extraction for triangle counts, UV presence/quality, normals/tangents, non-manifold checks

### Engine Export Adapters (lightweight)

Adapters should only translate outputs/metadata into engine-friendly layout/metadata:

- `ai_studio_core.adapters.godot`
- `ai_studio_core.adapters.unity`

No heavy coupling; avoid requiring engine installs.

## 3) Proposed Target Structure (End State)

This is the *desired* end state; migration is incremental.

```
ai-studio-core/                 # Repo A (standalone core)
  ai_studio_core/               # Python package (stable library + CLI)
  templates/                    # scaffolds + example specs/presets
  docs/                         # SPEC_REFERENCE, etc.
  .github/workflows/            # core CI

nethercore-ai-plugins/          # Repo B (plugins)
  zx-procgen/                   # wrappers + prompts only
  zx-dev/
  ...
  docs/
    ROADMAP_CORE_SPLIT.md
    SPEC_REFERENCE.md           # pointer to core docs
  .github/workflows/            # plugin CI (installs pinned core)
```

Near-term we **do not move existing plugin directories**. Plugins route workflows through the core CLI (`ai-studio`) installed from a pinned release.

## 4) Migration Strategy (No Big-Bang)

### Compatibility guarantees

- Existing projects with `.studio/generate.py` keep working.
- Existing plugin commands keep working (but can emit deprecation notices when they call old paths).
- `.studio/` remains supported, but core also supports a configurable studio root (default `.studio/`).

### Strategy: “wrap, then extract”

1. **Wrap** existing behavior behind `ai-studio` CLI (no pipeline rewrite).
2. **Extract** stable modules from the `.studio/` scaffold into core over time.
3. **Replace** plugin command implementations with `ai-studio …` calls once the CLI is stable.

## 5) Phased Plan (with Definition of Done)

### Phase 0 — Roadmap + scaffolding (low risk)

**Work:**
- Add this roadmap.
- Add `ai_studio_core` package + `ai-studio` CLI skeleton.

**DoD:**
- `ai-studio --help` works.
- `ai-studio doctor` reports missing deps without crashing.

### Phase 1 — Specs become the contract

**Work:**
- Define strict `AssetSpec` schemas (JSON) per asset type.
- Provide examples under `templates/specs/`.
- Implement `ai-studio validate --spec …` for spec-only validation and a report JSON.

**DoD:**
- All example specs validate successfully.
- Invalid spec errors are actionable (no stack traces).

### Phase 2 — Canonical templates + init flow

**Work:**
- Add `templates/project/.studio/**` as the canonical scaffold.
- Implement `ai-studio init` to install/upgrade `.studio/` deterministically.
- Keep legacy plugin commands working, but treat the `ai-studio-core` repo as the canonical scaffold source.

**DoD:**
- `ai-studio init` installs `.studio/` and creates expected `generated/` subfolders.
- Existing `init-procgen` workflow continues to work (possibly by calling `ai-studio init`).

### Phase 3 — Deterministic 3D preview + artifact validation (narrow scope)

**Scope guardrails (explicit):**
- Supported 3D asset types: **hardsurface props** + **lowpoly characters** only.
- Everything else (organic sculpting, cloth, VFX, photogrammetry) is **out of scope** and becomes a documented future item.

**Work:**
- Implement `ai-studio preview` using headless Blender:
  - Import the generated/exported `.glb` (preferred) referenced by spec outputs.
  - Render:
    - `generated/previews/<asset_id>_turntable.png`
    - `generated/previews/<asset_id>_ortho.png`
  - Determinism: fixed scene, fixed lighting, fixed camera, fixed render settings, seed applied.
- Implement 3D artifact checks in `ai-studio validate`:
  - triangle count vs spec budget
  - UVs present (and non-degenerate UV area)
  - normals present and consistent
  - tangents required when normal mapping enabled
  - non-manifold / loose geometry warnings (best-effort, actionable)
  - glTF/GLB format checks
- Emit report JSON:
  - `generated/reports/<asset_id>.report.json`
  - includes pass/fail, metrics, warnings, preview paths

**DoD:**
- `ai-studio preview` produces images for the example 3D specs (when Blender is installed).
- `ai-studio validate` produces a report and fails when constraints are violated.
- 3D promises remain narrow and documented.

### Phase 4 — Plugins orchestrate; core implements

**Work:**
- Update plugin commands that run/copy pipeline code to call `ai-studio` instead.
- Add deprecation notices for old command names/paths and provide a migration hint.
- Ensure generated projects record their required core version (`ai_studio.toml`).

**DoD:**
- Existing plugin workflows still work (same outputs/paths).
- Core is the only place where pipelines/validators/previews are implemented.

### Phase 5 — Repo hygiene + CI enforcement

**Work:**
- Implement `ai-studio lint-repo` to ensure references resolve and examples validate.
- Add GitHub Actions running `lint-repo` and validating example specs.
- Add `CONTRIBUTING.md` with checkable standards.

**DoD:**
- CI fails if referenced files are missing.
- CI fails if example specs become invalid.

## 6) Risks + Mitigations

### Blender availability and CI portability

**Risk:** Blender isn’t always installed locally or in CI.

**Mitigation:**
- `ai-studio doctor` reports tool presence clearly.
- CI runs 3D smoke tests only when Blender is available; otherwise it runs spec validation and repo lint.
- Local docs provide deterministic “how to run 3D validations” steps.

### Breaking existing `.studio/` projects

**Risk:** Moving or rewriting scaffold code breaks downstream projects.

**Mitigation:**
- Keep `.studio/` entrypoints stable and backward compatible.
- Start by wrapping existing code paths behind `ai-studio` commands.
- Provide a compatibility shim so old paths continue working with warnings.

### Over-promising 3D quality

**Risk:** Broad 3D scope leads to non-deterministic results and weak validation.

**Mitigation:**
- Narrow supported 3D to hardsurface props + lowpoly characters.
- Require explicit budgets and constraints in schema.
- Treat everything else as “future work” in docs and tooling output.
