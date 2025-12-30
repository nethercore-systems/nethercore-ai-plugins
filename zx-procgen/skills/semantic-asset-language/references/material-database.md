# Material Database Reference

Complete material definitions for style guides. Materials map semantic descriptors to PBR parameters using dot notation: `category.variant`.

## Material Structure

```rust
pub struct PbrParams {
    pub base_color: [f32; 3],     // RGB (0-1 range)
    pub metallic: f32,            // 0 = dielectric, 1 = full metal
    pub roughness: f32,           // 0 = mirror, 1 = fully rough
    pub normal_strength: f32,     // Normal map intensity (0-2)
    pub ao_strength: f32,         // Ambient occlusion (0-1)
    pub emission: f32,            // Emission intensity (0 = none, >0 = glow)
    pub ior: f32,                 // Index of refraction (1.0-3.0)
}

impl Default for PbrParams {
    fn default() -> Self {
        Self {
            base_color: [0.5, 0.5, 0.5],
            metallic: 0.0,
            roughness: 0.5,
            normal_strength: 1.0,
            ao_strength: 0.5,
            emission: 0.0,
            ior: 1.5,
        }
    }
}
```

---

## Metals

All metals have `metallic: 1.0` (or close to it). Roughness varies by finish.

### metal.polished

Mirror-finish metal, highly reflective.

```rust
"metal.polished" => PbrParams {
    base_color: [0.9, 0.9, 0.9],
    metallic: 1.0,
    roughness: 0.05,
    normal_strength: 0.2,
    ao_strength: 0.3,
    emission: 0.0,
    ior: 2.5,
}
```

### metal.brushed

Directional scratches, softer reflections.

```rust
"metal.brushed" => PbrParams {
    base_color: [0.85, 0.85, 0.88],
    metallic: 1.0,
    roughness: 0.35,
    normal_strength: 0.6,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 2.5,
}
```

### metal.chrome

High-polish chrome plating.

```rust
"metal.chrome" => PbrParams {
    base_color: [0.95, 0.95, 0.97],
    metallic: 1.0,
    roughness: 0.02,
    normal_strength: 0.1,
    ao_strength: 0.2,
    emission: 0.0,
    ior: 2.9,
}
```

### metal.iron

Dark, slightly rough iron.

```rust
"metal.iron" => PbrParams {
    base_color: [0.35, 0.35, 0.38],
    metallic: 1.0,
    roughness: 0.55,
    normal_strength: 0.8,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 2.95,
}
```

### metal.rusted

Heavily oxidized, rough surface.

```rust
"metal.rusted" => PbrParams {
    base_color: [0.5, 0.3, 0.2],
    metallic: 0.3,           // Rust reduces metallic appearance
    roughness: 0.85,
    normal_strength: 1.2,
    ao_strength: 0.9,
    emission: 0.0,
    ior: 1.8,
}
```

### metal.oxidized

Light patina/oxidation (copper green, bronze brown).

```rust
"metal.oxidized" => PbrParams {
    base_color: [0.4, 0.55, 0.45],  // Verdigris green
    metallic: 0.6,
    roughness: 0.6,
    normal_strength: 0.9,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 2.0,
}
```

### metal.gold

Polished gold.

```rust
"metal.gold" => PbrParams {
    base_color: [1.0, 0.84, 0.0],
    metallic: 1.0,
    roughness: 0.15,
    normal_strength: 0.3,
    ao_strength: 0.3,
    emission: 0.0,
    ior: 0.47,  // Gold has unusual IOR
}
```

### metal.copper

Polished copper.

```rust
"metal.copper" => PbrParams {
    base_color: [0.95, 0.64, 0.54],
    metallic: 1.0,
    roughness: 0.25,
    normal_strength: 0.4,
    ao_strength: 0.35,
    emission: 0.0,
    ior: 1.1,
}
```

### metal.brass

Polished brass alloy.

```rust
"metal.brass" => PbrParams {
    base_color: [0.89, 0.73, 0.35],
    metallic: 1.0,
    roughness: 0.3,
    normal_strength: 0.4,
    ao_strength: 0.35,
    emission: 0.0,
    ior: 1.5,
}
```

### metal.bronze

Aged bronze.

```rust
"metal.bronze" => PbrParams {
    base_color: [0.8, 0.5, 0.2],
    metallic: 0.9,
    roughness: 0.45,
    normal_strength: 0.6,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.18,
}
```

### metal.painted

Painted metal surface.

```rust
"metal.painted" => PbrParams {
    base_color: [0.5, 0.5, 0.5],  // Color varies
    metallic: 0.0,               // Paint is dielectric
    roughness: 0.4,
    normal_strength: 0.3,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

### metal.riveted

Industrial metal with visible rivets.

```rust
"metal.riveted" => PbrParams {
    base_color: [0.4, 0.4, 0.42],
    metallic: 0.95,
    roughness: 0.5,
    normal_strength: 1.0,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 2.5,
}
```

---

## Woods

Woods are dielectric (`metallic: 0.0`) with varied roughness based on finish.

### wood.fresh

New, unweathered wood.

```rust
"wood.fresh" => PbrParams {
    base_color: [0.65, 0.5, 0.35],
    metallic: 0.0,
    roughness: 0.6,
    normal_strength: 0.8,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.weathered

Old, gray, weathered wood.

```rust
"wood.weathered" => PbrParams {
    base_color: [0.35, 0.32, 0.28],
    metallic: 0.0,
    roughness: 0.9,
    normal_strength: 1.0,
    ao_strength: 0.8,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.polished

Lacquered/varnished wood.

```rust
"wood.polished" => PbrParams {
    base_color: [0.55, 0.35, 0.2],
    metallic: 0.0,
    roughness: 0.2,
    normal_strength: 0.5,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.painted

Painted wood surface.

```rust
"wood.painted" => PbrParams {
    base_color: [0.8, 0.8, 0.8],  // Color varies
    metallic: 0.0,
    roughness: 0.45,
    normal_strength: 0.3,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.charred

Burnt, blackened wood.

```rust
"wood.charred" => PbrParams {
    base_color: [0.1, 0.08, 0.06],
    metallic: 0.0,
    roughness: 0.95,
    normal_strength: 1.2,
    ao_strength: 0.95,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.mossy

Wood with moss/lichen growth.

```rust
"wood.mossy" => PbrParams {
    base_color: [0.25, 0.35, 0.2],
    metallic: 0.0,
    roughness: 0.85,
    normal_strength: 1.0,
    ao_strength: 0.8,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.oak

Specific oak wood.

```rust
"wood.oak" => PbrParams {
    base_color: [0.6, 0.45, 0.28],
    metallic: 0.0,
    roughness: 0.65,
    normal_strength: 0.9,
    ao_strength: 0.55,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.mahogany

Dark reddish mahogany.

```rust
"wood.mahogany" => PbrParams {
    base_color: [0.45, 0.22, 0.15],
    metallic: 0.0,
    roughness: 0.55,
    normal_strength: 0.7,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.ebony

Very dark ebony wood.

```rust
"wood.ebony" => PbrParams {
    base_color: [0.12, 0.1, 0.08],
    metallic: 0.0,
    roughness: 0.4,
    normal_strength: 0.6,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 1.5,
}
```

### wood.rotting

Decaying, soft wood.

```rust
"wood.rotting" => PbrParams {
    base_color: [0.3, 0.28, 0.22],
    metallic: 0.0,
    roughness: 0.95,
    normal_strength: 1.3,
    ao_strength: 0.9,
    emission: 0.0,
    ior: 1.5,
}
```

---

## Stones

### stone.rough

Natural rough stone.

```rust
"stone.rough" => PbrParams {
    base_color: [0.45, 0.42, 0.4],
    metallic: 0.0,
    roughness: 0.85,
    normal_strength: 1.0,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 1.5,
}
```

### stone.polished

Polished stone surface.

```rust
"stone.polished" => PbrParams {
    base_color: [0.55, 0.52, 0.5],
    metallic: 0.0,
    roughness: 0.15,
    normal_strength: 0.4,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

### stone.mossy

Stone with moss growth.

```rust
"stone.mossy" => PbrParams {
    base_color: [0.35, 0.45, 0.3],
    metallic: 0.0,
    roughness: 0.8,
    normal_strength: 0.9,
    ao_strength: 0.8,
    emission: 0.0,
    ior: 1.5,
}
```

### stone.cracked

Damaged, cracked stone.

```rust
"stone.cracked" => PbrParams {
    base_color: [0.42, 0.4, 0.38],
    metallic: 0.0,
    roughness: 0.9,
    normal_strength: 1.2,
    ao_strength: 0.85,
    emission: 0.0,
    ior: 1.5,
}
```

### stone.marble

Polished marble.

```rust
"stone.marble" => PbrParams {
    base_color: [0.95, 0.93, 0.9],
    metallic: 0.0,
    roughness: 0.1,
    normal_strength: 0.3,
    ao_strength: 0.3,
    emission: 0.0,
    ior: 1.5,
}
```

### stone.dark

Dark stone/basalt.

```rust
"stone.dark" => PbrParams {
    base_color: [0.2, 0.18, 0.18],
    metallic: 0.0,
    roughness: 0.75,
    normal_strength: 0.8,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 1.5,
}
```

### stone.sandstone

Warm sandstone.

```rust
"stone.sandstone" => PbrParams {
    base_color: [0.76, 0.6, 0.42],
    metallic: 0.0,
    roughness: 0.8,
    normal_strength: 0.9,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 1.5,
}
```

---

## Fabrics

### fabric.cotton

Plain cotton fabric.

```rust
"fabric.cotton" => PbrParams {
    base_color: [0.85, 0.83, 0.8],
    metallic: 0.0,
    roughness: 0.9,
    normal_strength: 0.4,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.5,
}
```

### fabric.silk

Smooth, shiny silk.

```rust
"fabric.silk" => PbrParams {
    base_color: [0.9, 0.85, 0.8],
    metallic: 0.0,
    roughness: 0.25,
    normal_strength: 0.3,
    ao_strength: 0.3,
    emission: 0.0,
    ior: 1.5,
}
```

### fabric.velvet

Soft velvet with sheen.

```rust
"fabric.velvet" => PbrParams {
    base_color: [0.3, 0.1, 0.15],
    metallic: 0.0,
    roughness: 0.7,
    normal_strength: 0.5,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 1.5,
}
```

### fabric.wool

Rough wool texture.

```rust
"fabric.wool" => PbrParams {
    base_color: [0.6, 0.55, 0.5],
    metallic: 0.0,
    roughness: 0.95,
    normal_strength: 0.6,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 1.5,
}
```

### fabric.burlap

Coarse burlap/hessian.

```rust
"fabric.burlap" => PbrParams {
    base_color: [0.55, 0.45, 0.35],
    metallic: 0.0,
    roughness: 0.95,
    normal_strength: 0.9,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 1.5,
}
```

### fabric.synthetic

Modern synthetic fabric.

```rust
"fabric.synthetic" => PbrParams {
    base_color: [0.5, 0.5, 0.55],
    metallic: 0.0,
    roughness: 0.6,
    normal_strength: 0.3,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

---

## Leathers

### leather.brown

Classic brown leather.

```rust
"leather.brown" => PbrParams {
    base_color: [0.45, 0.3, 0.2],
    metallic: 0.0,
    roughness: 0.55,
    normal_strength: 0.7,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.5,
}
```

### leather.worn

Aged, worn leather.

```rust
"leather.worn" => PbrParams {
    base_color: [0.4, 0.32, 0.25],
    metallic: 0.0,
    roughness: 0.75,
    normal_strength: 0.9,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 1.5,
}
```

### leather.fine

High-quality polished leather.

```rust
"leather.fine" => PbrParams {
    base_color: [0.25, 0.15, 0.1],
    metallic: 0.0,
    roughness: 0.35,
    normal_strength: 0.5,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

---

## Plastics

### plastic.glossy

Shiny plastic.

```rust
"plastic.glossy" => PbrParams {
    base_color: [0.8, 0.2, 0.2],  // Color varies
    metallic: 0.0,
    roughness: 0.15,
    normal_strength: 0.2,
    ao_strength: 0.3,
    emission: 0.0,
    ior: 1.5,
}
```

### plastic.matte

Matte plastic finish.

```rust
"plastic.matte" => PbrParams {
    base_color: [0.5, 0.5, 0.5],
    metallic: 0.0,
    roughness: 0.7,
    normal_strength: 0.2,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.5,
}
```

### plastic.rubber

Rubber material.

```rust
"plastic.rubber" => PbrParams {
    base_color: [0.15, 0.15, 0.15],
    metallic: 0.0,
    roughness: 0.9,
    normal_strength: 0.4,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.5,
}
```

### plastic.translucent

Semi-transparent plastic.

```rust
"plastic.translucent" => PbrParams {
    base_color: [0.9, 0.9, 0.95],
    metallic: 0.0,
    roughness: 0.2,
    normal_strength: 0.1,
    ao_strength: 0.2,
    emission: 0.0,
    ior: 1.45,
}
```

---

## Organics

### organic.skin

Human/creature skin.

```rust
"organic.skin" => PbrParams {
    base_color: [0.8, 0.6, 0.5],
    metallic: 0.0,
    roughness: 0.55,
    normal_strength: 0.5,
    ao_strength: 0.4,
    emission: 0.0,
    ior: 1.4,
}
```

### organic.bark

Tree bark.

```rust
"organic.bark" => PbrParams {
    base_color: [0.35, 0.25, 0.18],
    metallic: 0.0,
    roughness: 0.9,
    normal_strength: 1.2,
    ao_strength: 0.8,
    emission: 0.0,
    ior: 1.5,
}
```

### organic.bone

Bone material.

```rust
"organic.bone" => PbrParams {
    base_color: [0.9, 0.85, 0.75],
    metallic: 0.0,
    roughness: 0.6,
    normal_strength: 0.5,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.5,
}
```

### organic.chitin

Insect exoskeleton.

```rust
"organic.chitin" => PbrParams {
    base_color: [0.2, 0.18, 0.15],
    metallic: 0.0,
    roughness: 0.3,
    normal_strength: 0.6,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 1.56,
}
```

### organic.coral

Coral structure.

```rust
"organic.coral" => PbrParams {
    base_color: [0.9, 0.5, 0.45],
    metallic: 0.0,
    roughness: 0.8,
    normal_strength: 0.9,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 1.5,
}
```

### organic.moss

Soft moss.

```rust
"organic.moss" => PbrParams {
    base_color: [0.25, 0.4, 0.2],
    metallic: 0.0,
    roughness: 0.95,
    normal_strength: 0.6,
    ao_strength: 0.7,
    emission: 0.0,
    ior: 1.5,
}
```

---

## Crystals

### crystal.clear

Transparent crystal.

```rust
"crystal.clear" => PbrParams {
    base_color: [0.98, 0.98, 1.0],
    metallic: 0.0,
    roughness: 0.02,
    normal_strength: 0.2,
    ao_strength: 0.2,
    emission: 0.0,
    ior: 2.4,  // Diamond-like
}
```

### crystal.colored

Colored gemstone.

```rust
"crystal.colored" => PbrParams {
    base_color: [0.4, 0.2, 0.8],  // Amethyst example
    metallic: 0.0,
    roughness: 0.05,
    normal_strength: 0.3,
    ao_strength: 0.25,
    emission: 0.0,
    ior: 1.54,
}
```

### crystal.magical

Glowing magical crystal.

```rust
"crystal.magical" => PbrParams {
    base_color: [0.3, 0.8, 0.9],
    metallic: 0.0,
    roughness: 0.1,
    normal_strength: 0.4,
    ao_strength: 0.3,
    emission: 0.6,
    ior: 1.8,
}
```

### crystal.corrupted

Dark, tainted crystal.

```rust
"crystal.corrupted" => PbrParams {
    base_color: [0.15, 0.05, 0.2],
    metallic: 0.0,
    roughness: 0.15,
    normal_strength: 0.5,
    ao_strength: 0.4,
    emission: 0.3,
    ior: 1.6,
}
```

---

## Tech

### tech.screen

Display screen (emissive).

```rust
"tech.screen" => PbrParams {
    base_color: [0.1, 0.15, 0.2],
    metallic: 0.0,
    roughness: 0.05,
    normal_strength: 0.1,
    ao_strength: 0.2,
    emission: 1.0,
    ior: 1.5,
}
```

### tech.panel

Metal tech panel.

```rust
"tech.panel" => PbrParams {
    base_color: [0.3, 0.32, 0.35],
    metallic: 0.9,
    roughness: 0.4,
    normal_strength: 0.5,
    ao_strength: 0.5,
    emission: 0.0,
    ior: 2.5,
}
```

### tech.circuit

Circuit board.

```rust
"tech.circuit" => PbrParams {
    base_color: [0.1, 0.35, 0.2],  // PCB green
    metallic: 0.3,
    roughness: 0.5,
    normal_strength: 0.7,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 1.5,
}
```

### tech.hologram

Holographic display.

```rust
"tech.hologram" => PbrParams {
    base_color: [0.3, 0.8, 1.0],
    metallic: 0.0,
    roughness: 0.0,
    normal_strength: 0.0,
    ao_strength: 0.0,
    emission: 1.5,
    ior: 1.0,
}
```

---

## Concrete/Construction

### concrete.fresh

New concrete.

```rust
"concrete.fresh" => PbrParams {
    base_color: [0.6, 0.58, 0.55],
    metallic: 0.0,
    roughness: 0.85,
    normal_strength: 0.7,
    ao_strength: 0.6,
    emission: 0.0,
    ior: 1.5,
}
```

### concrete.stained

Dirty, stained concrete.

```rust
"concrete.stained" => PbrParams {
    base_color: [0.45, 0.42, 0.4],
    metallic: 0.0,
    roughness: 0.9,
    normal_strength: 0.9,
    ao_strength: 0.75,
    emission: 0.0,
    ior: 1.5,
}
```

### concrete.cracked

Damaged concrete.

```rust
"concrete.cracked" => PbrParams {
    base_color: [0.5, 0.48, 0.45],
    metallic: 0.0,
    roughness: 0.92,
    normal_strength: 1.1,
    ao_strength: 0.85,
    emission: 0.0,
    ior: 1.5,
}
```

---

## Material Lookup Function

```rust
pub fn material_from_semantic(descriptor: &str) -> Option<PbrParams> {
    match descriptor {
        // Metals
        "metal.polished" => Some(/* params */),
        "metal.brushed" => Some(/* params */),
        "metal.chrome" => Some(/* params */),
        "metal.iron" => Some(/* params */),
        "metal.rusted" => Some(/* params */),
        "metal.oxidized" => Some(/* params */),
        "metal.gold" => Some(/* params */),
        "metal.copper" => Some(/* params */),
        "metal.brass" => Some(/* params */),
        "metal.bronze" => Some(/* params */),
        "metal.painted" => Some(/* params */),
        "metal.riveted" => Some(/* params */),

        // Woods
        "wood.fresh" => Some(/* params */),
        "wood.weathered" => Some(/* params */),
        "wood.polished" => Some(/* params */),
        "wood.painted" => Some(/* params */),
        "wood.charred" => Some(/* params */),
        "wood.mossy" => Some(/* params */),
        "wood.oak" => Some(/* params */),
        "wood.mahogany" => Some(/* params */),
        "wood.ebony" => Some(/* params */),
        "wood.rotting" => Some(/* params */),

        // Stones
        "stone.rough" => Some(/* params */),
        "stone.polished" => Some(/* params */),
        "stone.mossy" => Some(/* params */),
        "stone.cracked" => Some(/* params */),
        "stone.marble" => Some(/* params */),
        "stone.dark" => Some(/* params */),
        "stone.sandstone" => Some(/* params */),

        // ... all other categories

        _ => None,
    }
}
```
