# Optimization Techniques

## WASM Size Reduction

### Cargo Settings (Full)

```toml
[profile.release]
lto = true
opt-level = "z"
codegen-units = 1
panic = "abort"
strip = true

[profile.release.package."*"]
opt-level = "z"
```

### Post-Processing

```bash
# Install wasm-opt
cargo install wasm-opt

# Optimize binary
wasm-opt -Oz target/wasm32-unknown-unknown/release/game.wasm -o game_opt.wasm

# Compare sizes
ls -la game.wasm game_opt.wasm
```

### Code Size Tips

- Avoid `format!()` and string formatting
- Use `#[inline(never)]` on cold paths
- Minimize generic instantiations
- Prefer `core` over `std` where possible

## Texture Optimization

### Size Calculation

```
Compressed size = width * height * 0.5 bytes (BC7)
```

### Resolution Guidelines

| Asset Type | Max Resolution | Typical |
|------------|---------------|---------|
| UI icons | 64x64 | 32x32 |
| Character | 512x512 | 256x256 |
| Environment | 256x256 | 128x128 |
| Skybox | 512x512 | 256x256 |

### Texture Atlas

Combine small textures into atlas:
- Reduces draw calls
- Better cache utilization
- Single load operation

## State Optimization

### Compact Data Types

```rust
// Before: 24 bytes per entity
struct Entity {
    x: f64,      // 8 bytes
    y: f64,      // 8 bytes
    health: i32, // 4 bytes
    _pad: i32,   // 4 bytes
}

// After: 8 bytes per entity
struct Entity {
    x: i16,      // 2 bytes (fixed-point)
    y: i16,      // 2 bytes
    health: u16, // 2 bytes
    flags: u16,  // 2 bytes
}
```

### Fixed Arrays

```rust
// Bad: Vec allocates on heap, size varies
entities: Vec<Entity>,

// Good: Fixed size, predictable snapshot
entities: [Entity; MAX_ENTITIES],
active_count: u16,
```

## Audio Optimization

### Format Comparison

| Format | Size per second |
|--------|----------------|
| WAV 44.1kHz stereo | 176 KB |
| WAV 22kHz mono | 44 KB |
| XM module | 5-20 KB |

### Music Strategy

Use XM/IT tracker format for music:
- 95%+ size savings
- Procedural variation
- Looping built-in
