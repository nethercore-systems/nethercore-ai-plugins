# Material Database Reference

Materials map semantic descriptors to PBR parameters using dot notation: `category.variant`.

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
```

## Quick Reference

| Category | Common Variants | Metallic | Notes |
|----------|-----------------|----------|-------|
| metal.* | polished, brushed, rusted, gold, copper | 1.0 | IOR varies by type |
| wood.* | fresh, weathered, polished, charred | 0.0 | All ior: 1.5 |
| stone.* | rough, polished, mossy, marble | 0.0 | High normal for rough |
| fabric.* | cotton, silk, velvet, wool | 0.0 | High roughness |
| leather.* | brown, worn, fine | 0.0 | Medium roughness |
| plastic.* | glossy, matte, rubber | 0.0 | Variable roughness |
| organic.* | skin, bark, bone, chitin | 0.0 | Varied IOR |
| crystal.* | clear, colored, magical | 0.0 | High IOR, may emit |
| tech.* | screen, panel, circuit | Varies | Screens emit light |
| concrete.* | fresh, stained, cracked | 0.0 | High roughness |

## Detailed References

- `materials-metals.md` - All metal variants with full PBR params
- `materials-natural.md` - Woods and stones
- `materials-soft.md` - Fabrics, leather, plastics
- `materials-specialty.md` - Organics, crystals, tech, concrete

## Material Lookup Pattern

```rust
pub fn material_from_semantic(descriptor: &str) -> Option<PbrParams> {
    let parts: Vec<&str> = descriptor.split('.').collect();
    match parts[0] {
        "metal" => lookup_metal(parts[1]),
        "wood" => lookup_wood(parts[1]),
        "stone" => lookup_stone(parts[1]),
        // ... other categories
        _ => None,
    }
}
```

## Common Patterns

**Weathering progression:**
- Fresh → Aged → Damaged (roughness increases, metallic decreases)

**Emission materials:**
- tech.screen, tech.hologram, crystal.magical, crystal.corrupted

**High-IOR materials:**
- crystal.clear (2.4), metal.chrome (2.9), metal.iron (2.95)
