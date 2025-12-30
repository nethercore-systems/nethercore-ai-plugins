# Metal Materials

All metals have `metallic: 1.0` (or close to it). Roughness varies by finish.

## metal.polished
Mirror-finish metal, highly reflective.
```rust
"metal.polished" => PbrParams {
    base_color: [0.9, 0.9, 0.9], metallic: 1.0, roughness: 0.05,
    normal_strength: 0.2, ao_strength: 0.3, emission: 0.0, ior: 2.5,
}
```

## metal.brushed
Directional scratches, softer reflections.
```rust
"metal.brushed" => PbrParams {
    base_color: [0.85, 0.85, 0.88], metallic: 1.0, roughness: 0.35,
    normal_strength: 0.6, ao_strength: 0.4, emission: 0.0, ior: 2.5,
}
```

## metal.chrome
High-polish chrome plating.
```rust
"metal.chrome" => PbrParams {
    base_color: [0.95, 0.95, 0.97], metallic: 1.0, roughness: 0.02,
    normal_strength: 0.1, ao_strength: 0.2, emission: 0.0, ior: 2.9,
}
```

## metal.iron
Dark, slightly rough iron.
```rust
"metal.iron" => PbrParams {
    base_color: [0.35, 0.35, 0.38], metallic: 1.0, roughness: 0.55,
    normal_strength: 0.8, ao_strength: 0.6, emission: 0.0, ior: 2.95,
}
```

## metal.rusted
Heavily oxidized, rough surface.
```rust
"metal.rusted" => PbrParams {
    base_color: [0.5, 0.3, 0.2], metallic: 0.3, roughness: 0.85,
    normal_strength: 1.2, ao_strength: 0.9, emission: 0.0, ior: 1.8,
}
```

## metal.oxidized
Light patina/oxidation (copper green, bronze brown).
```rust
"metal.oxidized" => PbrParams {
    base_color: [0.4, 0.55, 0.45], metallic: 0.6, roughness: 0.6,
    normal_strength: 0.9, ao_strength: 0.7, emission: 0.0, ior: 2.0,
}
```

## metal.gold
Polished gold.
```rust
"metal.gold" => PbrParams {
    base_color: [1.0, 0.84, 0.0], metallic: 1.0, roughness: 0.15,
    normal_strength: 0.3, ao_strength: 0.3, emission: 0.0, ior: 0.47,
}
```

## metal.copper
Polished copper.
```rust
"metal.copper" => PbrParams {
    base_color: [0.95, 0.64, 0.54], metallic: 1.0, roughness: 0.25,
    normal_strength: 0.4, ao_strength: 0.35, emission: 0.0, ior: 1.1,
}
```

## metal.brass
Polished brass alloy.
```rust
"metal.brass" => PbrParams {
    base_color: [0.89, 0.73, 0.35], metallic: 1.0, roughness: 0.3,
    normal_strength: 0.4, ao_strength: 0.35, emission: 0.0, ior: 1.5,
}
```

## metal.bronze
Aged bronze.
```rust
"metal.bronze" => PbrParams {
    base_color: [0.8, 0.5, 0.2], metallic: 0.9, roughness: 0.45,
    normal_strength: 0.6, ao_strength: 0.5, emission: 0.0, ior: 1.18,
}
```

## metal.painted
Painted metal surface.
```rust
"metal.painted" => PbrParams {
    base_color: [0.5, 0.5, 0.5], metallic: 0.0, roughness: 0.4,
    normal_strength: 0.3, ao_strength: 0.4, emission: 0.0, ior: 1.5,
}
```

## metal.riveted
Industrial metal with visible rivets.
```rust
"metal.riveted" => PbrParams {
    base_color: [0.4, 0.4, 0.42], metallic: 0.95, roughness: 0.5,
    normal_strength: 1.0, ao_strength: 0.7, emission: 0.0, ior: 2.5,
}
```
