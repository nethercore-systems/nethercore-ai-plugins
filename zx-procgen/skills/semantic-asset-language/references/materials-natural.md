# Natural Materials (Woods & Stones)

## Woods

Woods are dielectric (`metallic: 0.0`) with varied roughness based on finish.

### wood.fresh
New, unweathered wood.
```rust
"wood.fresh" => PbrParams {
    base_color: [0.65, 0.5, 0.35], metallic: 0.0, roughness: 0.6,
    normal_strength: 0.8, ao_strength: 0.5, emission: 0.0, ior: 1.5,
}
```

### wood.weathered
Old, gray, weathered wood.
```rust
"wood.weathered" => PbrParams {
    base_color: [0.35, 0.32, 0.28], metallic: 0.0, roughness: 0.9,
    normal_strength: 1.0, ao_strength: 0.8, emission: 0.0, ior: 1.5,
}
```

### wood.polished
Lacquered/varnished wood.
```rust
"wood.polished" => PbrParams {
    base_color: [0.55, 0.35, 0.2], metallic: 0.0, roughness: 0.2,
    normal_strength: 0.5, ao_strength: 0.4, emission: 0.0, ior: 1.5,
}
```

### wood.charred
Burnt, blackened wood.
```rust
"wood.charred" => PbrParams {
    base_color: [0.1, 0.08, 0.06], metallic: 0.0, roughness: 0.95,
    normal_strength: 1.2, ao_strength: 0.95, emission: 0.0, ior: 1.5,
}
```

### wood.mossy
Wood with moss/lichen growth.
```rust
"wood.mossy" => PbrParams {
    base_color: [0.25, 0.35, 0.2], metallic: 0.0, roughness: 0.85,
    normal_strength: 1.0, ao_strength: 0.8, emission: 0.0, ior: 1.5,
}
```

### wood.oak / wood.mahogany / wood.ebony
```rust
"wood.oak" => base_color: [0.6, 0.45, 0.28], roughness: 0.65
"wood.mahogany" => base_color: [0.45, 0.22, 0.15], roughness: 0.55
"wood.ebony" => base_color: [0.12, 0.1, 0.08], roughness: 0.4
```

---

## Stones

### stone.rough
Natural rough stone.
```rust
"stone.rough" => PbrParams {
    base_color: [0.45, 0.42, 0.4], metallic: 0.0, roughness: 0.85,
    normal_strength: 1.0, ao_strength: 0.7, emission: 0.0, ior: 1.5,
}
```

### stone.polished
Polished stone surface.
```rust
"stone.polished" => PbrParams {
    base_color: [0.55, 0.52, 0.5], metallic: 0.0, roughness: 0.15,
    normal_strength: 0.4, ao_strength: 0.4, emission: 0.0, ior: 1.5,
}
```

### stone.mossy
Stone with moss growth.
```rust
"stone.mossy" => PbrParams {
    base_color: [0.35, 0.45, 0.3], metallic: 0.0, roughness: 0.8,
    normal_strength: 0.9, ao_strength: 0.8, emission: 0.0, ior: 1.5,
}
```

### stone.marble
Polished marble.
```rust
"stone.marble" => PbrParams {
    base_color: [0.95, 0.93, 0.9], metallic: 0.0, roughness: 0.1,
    normal_strength: 0.3, ao_strength: 0.3, emission: 0.0, ior: 1.5,
}
```

### stone.dark
Dark stone/basalt.
```rust
"stone.dark" => PbrParams {
    base_color: [0.2, 0.18, 0.18], metallic: 0.0, roughness: 0.75,
    normal_strength: 0.8, ao_strength: 0.7, emission: 0.0, ior: 1.5,
}
```

### stone.sandstone
Warm sandstone.
```rust
"stone.sandstone" => PbrParams {
    base_color: [0.76, 0.6, 0.42], metallic: 0.0, roughness: 0.8,
    normal_strength: 0.9, ao_strength: 0.6, emission: 0.0, ior: 1.5,
}
```

### stone.cracked
Damaged, cracked stone.
```rust
"stone.cracked" => PbrParams {
    base_color: [0.42, 0.4, 0.38], metallic: 0.0, roughness: 0.9,
    normal_strength: 1.2, ao_strength: 0.85, emission: 0.0, ior: 1.5,
}
```
