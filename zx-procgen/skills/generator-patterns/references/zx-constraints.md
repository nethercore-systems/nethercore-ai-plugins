# ZX Asset Constraints (Shared Reference)

Canonical reference for Nethercore ZX asset limits. Use this instead of duplicating in agents/skills.

## Mesh Budgets

| Use Case | Triangle Budget |
|----------|-----------------|
| Swarm entities | 50-150 |
| Props | 50-300 |
| Characters | 200-500 |
| Vehicles | 300-800 |
| Hero/close-up | 500-2000 |

### By Game Size

| Game Size | Hero | Standard | Background |
|-----------|------|----------|------------|
| Tiny (1-5 assets) | 2000 | 1000 | 500 |
| Small (5-20) | 1500 | 750 | 300 |
| Medium (20-50) | 1000 | 500 | 200 |
| Large (50-100) | 750 | 350 | 150 |
| Massive (100+) | 500 | 250 | 100 |

### Mesh Format

- **Output:** GLB/GLTF (preferred), OBJ
- **Coordinate system:** Y-up, right-handed
- **Index limit:** 65k vertices (u16)
- **Triangulated:** Yes (quads auto-converted)

## Texture Limits

| Constraint | Limit |
|------------|-------|
| Max resolution | 512 x 512 |
| Required sizes | Power of 2 (64, 128, 256, 512) |
| VRAM budget | 4MB total |
| Matcap resolution | 64x64 or 128x128 typical |
| Format | PNG (RGBA8) |

## Audio Specs

| Requirement | Value |
|-------------|-------|
| Format | WAV (16-bit PCM) |
| Sample rate | 22,050 Hz |
| Channels | Mono |
| Max SFX duration | 5 seconds |
| Peak level | < 0.95 (avoid clipping) |

## Animation/Skeleton Limits

| Constraint | Limit |
|------------|-------|
| Max bones | 256 |
| Bones per vertex | 4 |
| Weight sum | 1.0 (normalized) |

## Render Modes

| Mode | Maps | Use Case |
|------|------|----------|
| 0 | Albedo | Unlit/Lambert, UI, sprites |
| 1 | Albedo + Matcaps | Stylized, retro |
| 2 | Albedo + MRE | PBR-ish metal/rough |
| 3 | Albedo + SSE + Specular | Classic Blinn-Phong |

### MRE Channels (Mode 2)

| Channel | 0.0 | 1.0 |
|---------|-----|-----|
| R (Metallic) | Dielectric | Metal |
| G (Roughness) | Mirror | Diffuse |
| B (Emissive) | None | Max glow |

### SSE Channels (Mode 3)

| Channel | 0.0 | 1.0 |
|---------|-----|-----|
| R (Specular Damping) | Full spec | No spec |
| G (Shininess) | Diffuse | Mirror |
| B (Emissive) | None | Max glow |

## File Size Limits (Code)

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤300 | Ideal per file |
| Soft | 400 | Consider splitting |
| Hard | 500 | MUST split |

## Memory Summary

| Asset | Typical Size |
|-------|--------------|
| 256x256 RGBA | 256KB |
| 512x512 RGBA | 1MB |
| 100 tri mesh | ~2KB |
| 1s mono audio | 44KB |
