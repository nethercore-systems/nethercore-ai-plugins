---
name: optimization
description: >-
  Optimization techniques for Nethercore WASM games. Covers WASM binary size
  reduction (LTO, wasm-opt), texture and mesh compression, audio optimization,
  and state size minimization. Use when a ROM exceeds size limits or when
  reducing build output size.
license: Apache-2.0
compatibility: Requires wasm-opt for post-build optimization. Works offline.
metadata:
  author: nethercore-systems
  version: "1.0.0"
---

# Nethercore Optimization

## WASM Optimization

### Cargo.toml Settings

```toml
[profile.release]
lto = true           # Link-time optimization
opt-level = "z"      # Optimize for size
codegen-units = 1    # Better optimization
panic = "abort"      # Smaller than unwind
strip = true         # Strip symbols
```

### Post-Build

```bash
wasm-opt -Oz game.wasm -o game.wasm
```

**Typical savings:** 20-40%

## Texture Optimization

All textures use BC7 compression (4:1 ratio):

| Original | Compressed |
|----------|------------|
| 256x256 RGBA (256 KB) | 64 KB |
| 512x512 RGBA (1 MB) | 256 KB |

**Resolution targets:**
- UI elements: 256x256
- Characters: 256-512
- Environment: 128-256

## Mesh Optimization

| Format | Size/Vertex |
|--------|-------------|
| Position only | 12 bytes |
| Pos + UV | 20 bytes |
| Pos + UV + Normal | 32 bytes |
| Full | 40 bytes |

**Poly targets:**
- Background props: 50-200
- Interactive props: 100-500
- Characters: 500-2000

## Audio Optimization

- Sample rate: 22050 Hz (engine limit)
- Channels: Mono only
- Use XM modules for music (95% savings vs WAV)

## State Size Reduction

```rust
// Use compact types
struct Position { x: f32, y: f32 }  // 8 bytes
struct Position { x: i16, y: i16 }  // 4 bytes (fixed-point)

// Fixed arrays, not Vec
entities: [Entity; 64],  // Known size
```

## Quick Wins Checklist

- [ ] LTO and opt-level = "z" in Cargo.toml
- [ ] wasm-opt -Oz on final binary
- [ ] Texture resolutions at 256x256 default
- [ ] Music as XM format
- [ ] Fixed arrays instead of Vec
