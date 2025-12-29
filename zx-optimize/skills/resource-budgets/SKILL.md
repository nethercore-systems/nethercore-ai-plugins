---
name: Resource Budgets
description: This skill should be used when the user asks about "budget", "ROM size", "RAM limit", "VRAM budget", "memory", "size limits", "how much space", "resource planning", "asset budget", "data pack size", "WASM size", "state snapshot", or discusses memory allocation, resource planning, or size constraints for Nethercore ZX games.
version: 1.0.0
---

# Resource Budgets for Nethercore ZX

Plan and manage resource allocation within ZX console limits.

## Console Limits

| Resource | Hard Limit | Typical Usage | Warning Threshold |
|----------|------------|---------------|-------------------|
| **ROM Total** | 16 MB | 8-12 MB | > 12 MB |
| **WASM Code** | 4 MB | 0.5-2 MB | > 2 MB |
| **Data Pack** | 12 MB | 4-10 MB | > 10 MB |
| **RAM** | 4 MB | 1-3 MB | > 3 MB |
| **VRAM** | 4 MB | 2-4 MB | > 3.5 MB |
| **State Snapshot** | - | 50-150 KB | > 200 KB |

## Data Pack Budget by Asset Type

Typical allocation of the data pack (12 MB max):

| Asset Type | Percentage | Budget (12MB) | Notes |
|------------|------------|---------------|-------|
| Textures | 40-60% | 4.8-7.2 MB | BC7 compressed |
| Meshes | 20-30% | 2.4-3.6 MB | Packed vertex formats |
| Audio | 10-20% | 1.2-2.4 MB | XM modules + samples |
| Animations | 5-15% | 0.6-1.8 MB | Keyframes |

## Genre Budget Templates

### Platformer (2D/2.5D)
- Textures: 30% (sprites, tilesets)
- Meshes: 10% (simple geometry)
- Audio: 25% (music, SFX variety)
- Animations: 35% (character movement)

### Racing (3D)
- Textures: 50% (tracks, cars, environments)
- Meshes: 35% (vehicles, track geometry)
- Audio: 10% (engines, ambience)
- Animations: 5% (minimal)

### Fighting (2D/3D)
- Textures: 25% (character sprites/textures)
- Meshes: 15% (arenas)
- Audio: 15% (music, impact SFX)
- Animations: 45% (frame data critical)

### RPG/Adventure
- Textures: 45% (world, characters, UI)
- Meshes: 25% (environments)
- Audio: 20% (music, dialogue)
- Animations: 10% (basic movement)

## State Snapshot Sizing

For rollback netcode, state must serialize quickly:

| State Size | Frame Budget | Recommendation |
|------------|--------------|----------------|
| < 50 KB | < 1ms | Excellent |
| 50-100 KB | 1-2ms | Good |
| 100-200 KB | 2-4ms | Acceptable |
| > 200 KB | > 4ms | **Optimize** |

**State includes:** Entity positions, velocities, game state, timers, RNG state

## Warning Signs

### ROM > 12 MB
- Review largest assets with `nether build --verbose`
- Consider lower texture resolutions
- Check for duplicate or unused assets

### WASM > 2 MB
- Review `Cargo.toml` dependencies
- Enable LTO and `opt-level = "z"`
- Run `wasm-opt -Oz` post-build

### State > 200 KB
- Separate cosmetic from gameplay state
- Use compact types (u8 vs u32)
- Pool entities with fixed arrays

## Quick Size Estimation

```
Texture: width × height × 0.5 bytes (BC7)
Mesh: vertices × 12-40 bytes (format dependent)
Audio: seconds × 44100 bytes (22050Hz mono)
XM Music: 50-200 KB per song typical
```

## Build Analysis Command

Run to see resource breakdown:
```bash
nether build --verbose
```

Use the build-analyzer agent for detailed analysis and optimization recommendations.
