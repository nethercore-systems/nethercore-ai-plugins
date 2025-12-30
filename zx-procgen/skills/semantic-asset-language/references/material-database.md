# Material Database Reference

Materials map semantic descriptors to PBR parameters using dot notation: `category.variant`.

## Material Structure

```python
from dataclasses import dataclass

@dataclass
class PbrParams:
    base_color: tuple[float, float, float]  # RGB (0-1 range)
    metallic: float            # 0 = dielectric, 1 = full metal
    roughness: float           # 0 = mirror, 1 = fully rough
    normal_strength: float     # Normal map intensity (0-2)
    ao_strength: float         # Ambient occlusion (0-1)
    emission: float            # Emission intensity (0 = none, >0 = glow)
    ior: float                 # Index of refraction (1.0-3.0)
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

```python
from typing import Optional

def material_from_semantic(descriptor: str) -> Optional[PbrParams]:
    parts = descriptor.split('.')
    category_lookups = {
        "metal": lookup_metal,
        "wood": lookup_wood,
        "stone": lookup_stone,
        # ... other categories
    }
    lookup_fn = category_lookups.get(parts[0])
    if lookup_fn and len(parts) > 1:
        return lookup_fn(parts[1])
    return None
```

## Common Patterns

**Weathering progression:**
- Fresh → Aged → Damaged (roughness increases, metallic decreases)

**Emission materials:**
- tech.screen, tech.hologram, crystal.magical, crystal.corrupted

**High-IOR materials:**
- crystal.clear (2.4), metal.chrome (2.9), metal.iron (2.95)
