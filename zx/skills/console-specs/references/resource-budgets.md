# ZX Resource Budgets

## Console Limits

| Resource | Hard Limit | Typical | Warning |
|----------|------------|---------|---------|
| **ROM Total** | 16 MB | 8-12 MB | > 12 MB |
| **WASM Code** | 4 MB | 0.5-2 MB | > 2 MB |
| **Data Pack** | 12 MB | 4-10 MB | > 10 MB |
| **RAM** | 4 MB | 1-3 MB | > 3 MB |
| **VRAM** | 4 MB | 2-4 MB | > 3.5 MB |
| **State Snapshot** | - | 50-150 KB | > 200 KB |

## Data Pack Budget (12 MB max)

| Asset Type | Percentage | Budget |
|------------|------------|--------|
| Textures | 40-60% | 4.8-7.2 MB |
| Meshes | 20-30% | 2.4-3.6 MB |
| Audio | 10-20% | 1.2-2.4 MB |
| Animations | 5-15% | 0.6-1.8 MB |

## Genre Budget Examples

**Fighting Game (~12 MB):**
- Characters (8): ~6 MB
- Stages (4): ~3 MB
- Audio: ~2 MB
- Effects, UI, code: ~1 MB

**3D Platformer (~10 MB):**
- Player + animations: ~500 KB
- Levels (20): ~5 MB
- Enemies/NPCs: ~2 MB
- Audio: ~2 MB
- Code: ~500 KB

**Racing Game (~8 MB):**
- Vehicles (12): ~2 MB
- Tracks (6): ~4 MB
- Audio: ~1.5 MB
- Effects, UI, code: ~500 KB

## Quick Size Estimation

```
Texture: width x height x 0.5 bytes (BC7)
Mesh: vertices x 12-40 bytes (format dependent)
Audio: seconds x 44100 bytes (22050Hz mono)
XM Music: 50-200 KB per song
```

## State Snapshot Performance

| Size | Frame Budget | Status |
|------|--------------|--------|
| < 50 KB | < 1ms | Excellent |
| 50-100 KB | 1-2ms | Good |
| 100-200 KB | 2-4ms | Acceptable |
| > 200 KB | > 4ms | Optimize |
