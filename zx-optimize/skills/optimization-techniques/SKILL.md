---
name: Optimization Techniques
description: This skill should be used when the user asks about "optimize", "compress", "reduce size", "smaller", "wasm-opt", "BC7", "LTO", "opt-level", "asset compression", "mesh optimization", "texture compression", "audio optimization", "state size", or needs guidance on reducing ROM size, WASM size, or improving performance in Nethercore ZX games.
version: 1.0.0
---

# Optimization Techniques for Nethercore ZX

Concrete methods to reduce resource usage and improve performance.

## WASM Code Optimization

### Cargo.toml Settings

```toml
[profile.release]
lto = true           # Link-time optimization
opt-level = "z"      # Optimize for size (not speed)
codegen-units = 1    # Better optimization, slower compile
panic = "abort"      # Smaller than unwind
strip = true         # Strip symbols
```

### Post-Build Optimization

```bash
# Install wasm-opt (part of binaryen)
cargo install wasm-opt

# Optimize the WASM binary
wasm-opt -Oz game.wasm -o game.wasm
```

**Typical savings:** 20-40% reduction

### Dependency Audit

```bash
# Check dependency sizes
cargo bloat --release --wasm

# Common bloat sources:
# - serde (consider miniserde or nanoserde)
# - regex (use simple string matching)
# - std formatting (avoid format!() in tight loops)
```

## Texture Optimization

### BC7 Compression
All ZX textures use BC7 compression (4:1 ratio).

| Original | BC7 Compressed |
|----------|----------------|
| 256×256 RGBA (256 KB) | 64 KB |
| 512×512 RGBA (1 MB) | 256 KB |
| 1024×1024 RGBA (4 MB) | 1 MB |

### Resolution Guidelines

| Use Case | Max Resolution | Reason |
|----------|----------------|--------|
| UI elements | 256×256 | Close to camera |
| Character | 256×256 or 512×512 | Visible detail |
| Environment | 128×128 or 256×256 | Distance |
| Skybox | 512×512 | Large coverage |

### Texture Atlasing

Combine multiple sprites into atlases:
- Reduces draw calls
- Better cache utilization
- Fewer asset files

```
16 separate 64×64 sprites = 16 files
1 atlas 256×256 = 1 file, same total pixels
```

## Mesh Optimization

### Vertex Format Selection

| Format | Size/Vertex | Use Case |
|--------|-------------|----------|
| Position only | 12 bytes | Simple shapes |
| Pos + UV | 20 bytes | Textured static |
| Pos + UV + Normal | 32 bytes | Lit objects |
| Full (Pos+UV+Norm+Color) | 40 bytes | Characters |

### Poly Count Targets

| Object Type | Target Polygons |
|-------------|-----------------|
| Background props | 50-200 |
| Interactive props | 100-500 |
| Characters | 500-2000 |
| Vehicles | 500-1500 |
| Environments | 2000-5000 total |

### Mesh Techniques

- **LOD not needed** - ZX games typically close-up
- **Octahedral normal encoding** - 2 bytes vs 12
- **Indexed geometry** - Share vertices
- **Remove backfaces** - If never visible

## Audio Optimization

### Engine Constraints
- **Sample rate:** 22050 Hz only (engine limit)
- **Channels:** Mono only
- **Format:** 16-bit PCM for samples

### Optimization Strategies

| Technique | Savings |
|-----------|---------|
| Shorter samples | Proportional |
| XM modules for music | 10-50× vs WAV |
| Procedural SFX | Near-zero storage |
| Shared sound banks | Reduce duplicates |

### XM Module Benefits

```
3-minute WAV @ 22050Hz mono = ~4 MB
3-minute XM module = 50-200 KB
Savings: 95%+
```

## State Size Reduction

For rollback netcode performance:

### Data Type Selection

```rust
// Before: 16 bytes per entity position
struct Position { x: f64, y: f64 }

// After: 8 bytes per entity position
struct Position { x: f32, y: f32 }

// Even smaller: 4 bytes with fixed-point
struct Position { x: i16, y: i16 } // 8.8 fixed
```

### State Architecture

```rust
// BAD: Dynamic allocation
struct GameState {
    entities: Vec<Entity>,      // Unknown size
    particles: Vec<Particle>,   // Can grow
}

// GOOD: Fixed allocation
struct GameState {
    entities: [Entity; 64],     // Fixed 64 max
    entity_count: u8,
    particles: [Particle; 256], // Fixed pool
    particle_count: u8,
}
```

### Cosmetic vs Gameplay State

Only serialize gameplay-critical state:

```rust
// Serialized (affects gameplay)
struct PlayerState {
    x: f32, y: f32,
    health: u8,
    ammo: u8,
}

// NOT serialized (visual only)
struct PlayerVisuals {
    animation_frame: u8,
    particle_trail: [Particle; 8],
    screen_shake: f32,
}
```

## Quick Wins Checklist

- [ ] Enable LTO and opt-level = "z" in Cargo.toml
- [ ] Run wasm-opt -Oz on final binary
- [ ] Use BC7 for all textures
- [ ] Check texture resolutions (256×256 default)
- [ ] Audit mesh vertex formats
- [ ] Convert music to XM format
- [ ] Use fixed arrays instead of Vec
- [ ] Separate cosmetic from gameplay state

## Automated Optimization

Use the **optimizer agent** to:
1. Update Cargo.toml settings
2. Run wasm-opt on output
3. Report size reduction achieved
