# Specialty Materials (Organic, Crystal, Tech, Concrete)

## Organics

### organic.skin
Human/creature skin.
```rust
"organic.skin" => PbrParams {
    base_color: [0.8, 0.6, 0.5], metallic: 0.0, roughness: 0.55,
    normal_strength: 0.5, ao_strength: 0.4, emission: 0.0, ior: 1.4,
}
```

### organic.bark
Tree bark.
```rust
"organic.bark" => PbrParams {
    base_color: [0.35, 0.25, 0.18], metallic: 0.0, roughness: 0.9,
    normal_strength: 1.2, ao_strength: 0.8, emission: 0.0, ior: 1.5,
}
```

### organic.bone / organic.chitin / organic.coral / organic.moss
```rust
"organic.bone" => base_color: [0.9, 0.85, 0.75], roughness: 0.6
"organic.chitin" => base_color: [0.2, 0.18, 0.15], roughness: 0.3
"organic.coral" => base_color: [0.9, 0.5, 0.45], roughness: 0.8
"organic.moss" => base_color: [0.25, 0.4, 0.2], roughness: 0.95
```

---

## Crystals

### crystal.clear
Transparent crystal.
```rust
"crystal.clear" => PbrParams {
    base_color: [0.98, 0.98, 1.0], metallic: 0.0, roughness: 0.02,
    normal_strength: 0.2, ao_strength: 0.2, emission: 0.0, ior: 2.4,
}
```

### crystal.colored
Colored gemstone.
```rust
"crystal.colored" => PbrParams {
    base_color: [0.4, 0.2, 0.8], metallic: 0.0, roughness: 0.05,
    normal_strength: 0.3, ao_strength: 0.25, emission: 0.0, ior: 1.54,
}
```

### crystal.magical
Glowing magical crystal.
```rust
"crystal.magical" => PbrParams {
    base_color: [0.3, 0.8, 0.9], metallic: 0.0, roughness: 0.1,
    normal_strength: 0.4, ao_strength: 0.3, emission: 0.6, ior: 1.8,
}
```

### crystal.corrupted
Dark, tainted crystal.
```rust
"crystal.corrupted" => PbrParams {
    base_color: [0.15, 0.05, 0.2], metallic: 0.0, roughness: 0.15,
    normal_strength: 0.5, ao_strength: 0.4, emission: 0.3, ior: 1.6,
}
```

---

## Tech

### tech.screen
Display screen (emissive).
```rust
"tech.screen" => PbrParams {
    base_color: [0.1, 0.15, 0.2], metallic: 0.0, roughness: 0.05,
    normal_strength: 0.1, ao_strength: 0.2, emission: 1.0, ior: 1.5,
}
```

### tech.panel
Metal tech panel.
```rust
"tech.panel" => PbrParams {
    base_color: [0.3, 0.32, 0.35], metallic: 0.9, roughness: 0.4,
    normal_strength: 0.5, ao_strength: 0.5, emission: 0.0, ior: 2.5,
}
```

### tech.circuit / tech.hologram
```rust
"tech.circuit" => base_color: [0.1, 0.35, 0.2], metallic: 0.3
"tech.hologram" => base_color: [0.3, 0.8, 1.0], emission: 1.5
```

---

## Concrete/Construction

### concrete.fresh / concrete.stained / concrete.cracked
```rust
"concrete.fresh" => base_color: [0.6, 0.58, 0.55], roughness: 0.85
"concrete.stained" => base_color: [0.45, 0.42, 0.4], roughness: 0.9
"concrete.cracked" => base_color: [0.5, 0.48, 0.45], roughness: 0.92
```
