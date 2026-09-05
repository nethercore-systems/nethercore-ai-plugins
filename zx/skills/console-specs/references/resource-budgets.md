# ZX Resource Budgets

## Console Limits

These are console resource budgets, not file-ingestion safety caps.

| Resource | Hard Limit | Typical | Warning |
|----------|------------|---------|---------|
| **ROM Total** | 16 MiB (WASM code + assets) | 8-12 MiB | > 12 MiB |
| **WASM Code + Data Pack** | Share the 16 MiB ROM budget | Measure the packed cart | Leave headroom |
| **RAM** | 4 MiB WASM linear memory | 1-3 MiB | > 3 MiB |
| **VRAM** | 4 MiB GPU textures and mesh buffers | 2-4 MiB | > 3.5 MiB |
| **State Snapshot** | - | 50-150 KB | > 200 KB |

## File Read Safety Caps (not gameplay budgets)

The host uses larger caps while reading files defensively. They do not expand
the ZX ROM/RAM/VRAM limits above.

| File class | Read cap |
|------------|----------|
| ROM file | 512 MiB |
| WASM file | 128 MiB |
| PNG file | 32 MiB |

## Content Planning

`shared/src/console.rs` defines a shared 16 MiB ROM budget; it does not impose
a 4 MiB-code/12 MiB-data split. The separate 4 MiB RAM limit is linear memory,
not a WASM file-size cap. Keep headroom; measure loaded VRAM separately.

The typical/warning figures and genre examples below are planning heuristics,
not measured guarantees or extra platform limits.

## Genre Budget Examples

**Fighting Game (~12 MiB):**
- Characters (8): ~6 MiB
- Stages (4): ~3 MiB
- Audio: ~2 MiB
- Effects, UI, code: ~1 MiB

**3D Platformer (~10 MiB):**
- Player + animations: ~500 KiB
- Levels (20): ~5 MiB
- Enemies/NPCs: ~2 MiB
- Audio: ~2 MiB
- Code: ~500 KiB

**Racing Game (~8 MiB):**
- Vehicles (12): ~2 MiB
- Tracks (6): ~4 MiB
- Audio: ~1.5 MiB
- Effects, UI, code: ~500 KiB

## Quick Size Estimation

```
Texture: width x height x ~1 byte (BC7), plus metadata/alignment
Mesh: vertices x 12-40 bytes (format dependent)
Audio: seconds x 44100 bytes (22050Hz mono)
XM Music: 50-200 KiB per song
```

## State Snapshot Performance

| Size | Frame Budget | Status |
|------|--------------|--------|
| < 50 KB | < 1ms | Excellent |
| 50-100 KB | 1-2ms | Good |
| 100-200 KB | 2-4ms | Acceptable |
| > 200 KB | > 4ms | Optimize |
