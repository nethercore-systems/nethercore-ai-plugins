# Optimization Code Examples

## Dependency Audit

```bash
# Check dependency sizes
cargo bloat --release --wasm

# Common bloat sources:
# - serde (consider miniserde or nanoserde)
# - regex (use simple string matching)
# - std formatting (avoid format!() in tight loops)
```

## Texture Atlasing

Combine multiple sprites into atlases:

```
16 separate 64×64 sprites = 16 files
1 atlas 256×256 = 1 file, same total pixels
```

Benefits:
- Fewer draw calls
- Better cache utilization
- Fewer asset files

## Mesh Techniques

```rust
// Octahedral normal encoding: 2 bytes vs 12
// Indexed geometry: share vertices
// Remove backfaces if never visible
```

## State Architecture

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

## Cosmetic vs Gameplay State

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

## LTO Troubleshooting

If LTO build fails:
- Some dependencies don't support LTO
- Try `lto = "thin"` instead of `true`

If wasm-opt not found:
- `cargo install wasm-opt`
- Or download from binaryen releases

If build takes too long:
- `codegen-units = 1` is slow but worth it
- Only applies to release builds
