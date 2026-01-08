# AssetSpec Reference (ai-studio-core)

This document defines the **machine-validated** `AssetSpec` JSON format used by `ai-studio validate`.

Design goals:

- **Specs are the contract** (LLMs produce specs; tools validate them deterministically).
- **Low ambiguity**: prefer enums + explicit numeric budgets over open-ended prose.
- **Narrow 3D scope** (for now): **hardsurface props** + **lowpoly characters** only.

## Common Fields (all asset types)

### `asset_id` (string, required)

Stable identifier used in filenames and reports.

- Pattern: `[a-z][a-z0-9_-]{2,63}`
- Use lowercase and `_`/`-` separators.

### `asset_type` (string enum, required)

One of:

- `audio_sfx`
- `music`
- `texture_2d`
- `sprite_2d`
- `mesh_3d_hardsurface`
- `character_3d_lowpoly`

### `style_tags` (string[], optional)

Short tags that describe style intent (e.g. `["lowpoly", "clean", "readable"]`).

### `license` (string, required)

Asset licensing identifier (e.g. `CC0-1.0`, `CC-BY-4.0`, `proprietary`). This is informational but required.

### `seed` (int, required)

Determinism seed (`0..2^32-1`). Always set this for reproducible generation and previews.

### `variants` (array, optional)

Optional variants, each with:

- `variant_id` (string)
- `seed` (int)

### `outputs` (array, required)

Describes expected output artifacts under the chosen output root (default `generated/`).

Each output entry:

- `kind`: `primary` | `metadata` | `preview`
- `format`: `png` | `wav` | `ogg` | `json` | `glb` | `gltf` | `xm` | `it`
- `path`: relative path using forward slashes, must end with the matching extension (e.g. `textures/foo.png`)

Rules:

- `outputs` must include at least one `kind: "primary"`.
- `outputs[].path` must be unique.

### `engine_targets` (string[], optional)

Optional engine targets:

- `godot`
- `unity`
- `unreal`

## Asset-Type Specific Fields

### `audio_sfx`

Additional required fields:

- `duration_seconds` (float, `0.01..30.0`)
- `sample_rate_hz` (int, `8000..96000`)
- `channels` (int, `1..2`)

Primary outputs must be `wav` or `ogg`.

### `music`

Additional required fields:

- `tempo_bpm` (int, `40..260`)
- `loop` (bool, default `true`)

Primary outputs must be `xm` or `it`.

### `texture_2d`

Additional required fields:

- `resolution` (tuple `[width, height]`, max `8192x8192`)
- `tileable` (bool, default `true`)
- `maps` (array, 1+), each:
  - `map_type`: `albedo` | `normal` | `roughness` | `metallic` | `ao` | `emissive`
  - `format`: `"png"`

Primary outputs must be `png`.

### `sprite_2d`

Additional required fields:

- `frame_width` (int)
- `frame_height` (int)
- `frame_count` (int)
- `pivot` (object, optional):
  - `x` (float `0..1`)
  - `y` (float `0..1`)
- `trim_transparent` (bool, default `true`)

Primary outputs must be `png`.

### `mesh_3d_hardsurface`

Additional required fields:

- `triangle_budget` (int)
- `max_material_slots` (int, `1..4`)
- `use_normal_map` (bool)
- `export` (object):
  - `format`: `"glb"` (recommended)
  - `require_uvs` (bool)
  - `require_normals` (bool)
  - `require_tangents` (bool; must be `true` when `use_normal_map` is `true`)

Primary outputs must be `glb`.

### `character_3d_lowpoly`

Additional required fields:

- `triangle_budget` (int)
- `skeleton_preset` (string enum):
  - `humanoid_basic_v1`
- `constraints` (object):
  - `max_bone_influences` (int, `1..4`)
  - `max_bones` (int, `1..128`)
- `use_normal_map` (bool)
- `export` (object):
  - `format`: `"glb"`
  - `require_uvs` (bool)
  - `require_normals` (bool)
  - `require_tangents` (bool; must be `true` when `use_normal_map` is `true`)

Primary outputs must be `glb`.

## 3D Scope (Explicit)

The current core tooling only commits to:

- **Hardsurface props** (`mesh_3d_hardsurface`)
- **Lowpoly characters** (`character_3d_lowpoly`)

Everything else (organic sculpts, cloth sim, hair, photoreal scans, VFX, etc.) is out of scope for now and should be treated as a future extension.

