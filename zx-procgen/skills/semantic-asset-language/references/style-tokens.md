# Style Tokens Reference

Complete style token definitions for style guides. Each token modifies base generation parameters to achieve a consistent visual style. These definitions are language-agnostic.

## Token Definition Structure

Style tokens modify these parameters:

| Parameter | Description | Range |
|-----------|-------------|-------|
| roughness_offset | Added to base roughness | -0.3 to 0.4 |
| saturation_scale | Multiplied with saturation | 0.5 to 1.4 |
| detail_level | Surface complexity | Low, Medium, High, Extreme |
| edge_hardness | Edge sharpness | 0.0 (soft) to 1.0 (sharp) |
| noise_octaves_offset | Added to noise octaves | -2 to 3 |
| damage_amount | Wear and damage | 0.0 (pristine) to 1.0 (destroyed) |
| color_temperature | Color warmth | -1.0 (cool) to 1.0 (warm) |
| pattern_scale | Pattern size multiplier | 0.5 to 2.0 |
| emission_tendency | Likelihood of glow | 0.0 to 0.7 |

---

## Natural/Historical Tokens

### Rustic

Aged, worn, natural materials with visible use and weathering.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.3 |
| saturation_scale | 0.7 |
| detail_level | Medium |
| edge_hardness | 0.3 |
| noise_octaves_offset | 1 |
| damage_amount | 0.4 |
| color_temperature | 0.3 (warm) |
| pattern_scale | 1.0 |
| emission_tendency | 0.0 |

**Use for:** Barns, wooden furniture, farm equipment, leather goods, handcrafted items.

**Typical materials:** wood.weathered, leather.worn, metal.rusted, fabric.burlap

---

### Medieval

European medieval aesthetic - stone, iron, heavy construction.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.25 |
| saturation_scale | 0.6 |
| detail_level | Medium |
| edge_hardness | 0.5 |
| noise_octaves_offset | 1 |
| damage_amount | 0.3 |
| color_temperature | 0.1 |
| pattern_scale | 1.2 |
| emission_tendency | 0.05 |

**Use for:** Castles, armor, weapons, taverns, markets, dungeons.

**Typical materials:** stone.rough, metal.iron, wood.oak, fabric.wool

---

### Ancient

Old civilizations - weathered stone, faded colors, archaeological feel.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.4 |
| saturation_scale | 0.5 |
| detail_level | Medium |
| edge_hardness | 0.2 (eroded) |
| noise_octaves_offset | 2 |
| damage_amount | 0.6 |
| color_temperature | 0.2 |
| pattern_scale | 1.5 |
| emission_tendency | 0.0 |

**Use for:** Ruins, temples, tombs, artifacts, fossils.

**Typical materials:** stone.weathered, metal.oxidized, ceramic.cracked

---

### Victorian

19th century elegance - ornate, rich, formal.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.1 (polished) |
| saturation_scale | 0.8 |
| detail_level | High |
| edge_hardness | 0.6 |
| noise_octaves_offset | 0 |
| damage_amount | 0.1 |
| color_temperature | 0.2 |
| pattern_scale | 0.8 (finer) |
| emission_tendency | 0.1 |

**Use for:** Mansions, furniture, clothing, gadgets, street scenes.

**Typical materials:** wood.polished, fabric.velvet, metal.brass, leather.fine

---

## Modern/Futuristic Tokens

### Cyberpunk

Neon, chrome, high contrast, high-tech low-life.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.2 (reflective) |
| saturation_scale | 1.4 (vivid) |
| detail_level | High |
| edge_hardness | 0.9 (sharp) |
| noise_octaves_offset | 0 |
| damage_amount | 0.2 |
| color_temperature | -0.3 (cool with neon) |
| pattern_scale | 0.7 |
| emission_tendency | 0.7 (lots of neon) |

**Use for:** Cities, tech, vehicles, clothing, weapons, UI elements.

**Typical materials:** metal.chrome, tech.screen, plastic.glossy, fabric.synthetic

---

### Scifi

Clean futuristic - sleek, minimal, advanced technology.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.15 |
| saturation_scale | 0.9 |
| detail_level | Medium |
| edge_hardness | 0.85 |
| noise_octaves_offset | -1 (cleaner) |
| damage_amount | 0.05 |
| color_temperature | -0.2 (cool) |
| pattern_scale | 0.6 |
| emission_tendency | 0.4 |

**Use for:** Spaceships, stations, equipment, uniforms, interfaces.

**Typical materials:** metal.brushed, plastic.matte, tech.panel, composite.carbon

---

### Industrial

Factories, machinery, utilitarian design.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.2 |
| saturation_scale | 0.5 (desaturated) |
| detail_level | Medium |
| edge_hardness | 0.7 |
| noise_octaves_offset | 1 |
| damage_amount | 0.35 |
| color_temperature | -0.1 |
| pattern_scale | 1.3 |
| emission_tendency | 0.15 |

**Use for:** Factories, pipes, machinery, warehouses, tools.

**Typical materials:** metal.painted, metal.rusted, concrete.stained, rubber.worn

---

### Minimalist

Simple, clean, essential forms only.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.1 |
| saturation_scale | 0.6 |
| detail_level | Low |
| edge_hardness | 0.8 |
| noise_octaves_offset | -2 (very clean) |
| damage_amount | 0.0 |
| color_temperature | 0.0 (neutral) |
| pattern_scale | 2.0 (large shapes) |
| emission_tendency | 0.1 |

**Use for:** Modern furniture, UI, icons, architectural elements.

**Typical materials:** plastic.matte, wood.light, metal.white, fabric.cotton

---

## Organic/Natural Tokens

### Organic

Natural, flowing, biological forms.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.1 |
| saturation_scale | 0.9 |
| detail_level | Medium |
| edge_hardness | 0.1 (very soft) |
| noise_octaves_offset | 2 (natural variation) |
| damage_amount | 0.0 |
| color_temperature | 0.1 |
| pattern_scale | 1.0 |
| emission_tendency | 0.05 |

**Use for:** Creatures, plants, terrain, caves, coral.

**Typical materials:** organic.skin, organic.bark, organic.chitin, stone.natural

---

### Overgrown

Nature reclaiming - moss, vines, decay.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.25 |
| saturation_scale | 0.85 |
| detail_level | High |
| edge_hardness | 0.2 |
| noise_octaves_offset | 2 |
| damage_amount | 0.5 |
| color_temperature | 0.15 |
| pattern_scale | 0.9 |
| emission_tendency | 0.02 (bioluminescence) |

**Use for:** Ruins, abandoned structures, forest floors, swamps.

**Typical materials:** stone.mossy, wood.rotting, metal.rusted, organic.moss

---

### Crystalline

Gemstones, ice, mineral formations.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.3 (very smooth) |
| saturation_scale | 1.2 |
| detail_level | Medium |
| edge_hardness | 0.95 (sharp facets) |
| noise_octaves_offset | 0 |
| damage_amount | 0.0 |
| color_temperature | -0.2 |
| pattern_scale | 0.5 |
| emission_tendency | 0.3 |

**Use for:** Gems, ice caves, magical crystals, mineral veins.

**Typical materials:** crystal.clear, crystal.colored, crystal.magical, ice.solid

---

### Elemental

Primal forces - fire, water, earth, air manifestations.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.0 (varies by element) |
| saturation_scale | 1.3 |
| detail_level | High |
| edge_hardness | 0.5 |
| noise_octaves_offset | 3 (chaotic) |
| damage_amount | 0.0 |
| color_temperature | 0.0 (varies) |
| pattern_scale | 0.8 |
| emission_tendency | 0.5 (often glowing) |

**Use for:** Elementals, magical effects, environmental hazards.

**Typical materials:** Depends on element - lava, water, stone, energy

---

## Stylized Tokens

### Fantasy

Magical, colorful, exaggerated proportions.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.05 |
| saturation_scale | 1.2 |
| detail_level | High |
| edge_hardness | 0.4 |
| noise_octaves_offset | 1 |
| damage_amount | 0.1 |
| color_temperature | 0.2 |
| pattern_scale | 0.9 |
| emission_tendency | 0.25 |

**Use for:** Magic items, creatures, enchanted locations, artifacts.

**Typical materials:** metal.enchanted, crystal.magical, fabric.silk, wood.ancient

---

### Gothic

Dark, ornate, dramatic shadows.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.15 |
| saturation_scale | 0.6 |
| detail_level | High |
| edge_hardness | 0.7 |
| noise_octaves_offset | 1 |
| damage_amount | 0.25 |
| color_temperature | -0.2 (cool) |
| pattern_scale | 0.7 |
| emission_tendency | 0.1 |

**Use for:** Cathedrals, crypts, vampires, spooky mansions.

**Typical materials:** stone.dark, metal.iron, wood.ebony, fabric.black

---

### Steampunk

Victorian + steam technology - brass, gears, leather.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.1 |
| saturation_scale | 0.75 |
| detail_level | Extreme |
| edge_hardness | 0.6 |
| noise_octaves_offset | 1 |
| damage_amount | 0.2 |
| color_temperature | 0.4 (warm brass) |
| pattern_scale | 0.6 (fine gears) |
| emission_tendency | 0.15 |

**Use for:** Gadgets, vehicles, clothing, cities, weapons.

**Typical materials:** metal.brass, metal.copper, leather.brown, wood.mahogany

---

### Dieselpunk

1920s-40s + diesel tech - rivets, heavy machinery.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.2 |
| saturation_scale | 0.6 |
| detail_level | High |
| edge_hardness | 0.75 |
| noise_octaves_offset | 1 |
| damage_amount | 0.3 |
| color_temperature | 0.1 |
| pattern_scale | 0.9 |
| emission_tendency | 0.1 |

**Use for:** War machines, factories, cities, uniforms.

**Typical materials:** metal.riveted, metal.painted, leather.military, rubber.industrial

---

## Abstract/Artistic Tokens

### Geometric

Mathematical precision, hard edges, patterns.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.1 |
| saturation_scale | 0.9 |
| detail_level | Medium |
| edge_hardness | 1.0 (maximum) |
| noise_octaves_offset | -2 |
| damage_amount | 0.0 |
| color_temperature | 0.0 |
| pattern_scale | 1.0 |
| emission_tendency | 0.2 |

**Use for:** Abstract art, UI, tech, mathematical constructs.

**Typical materials:** Any with clean surfaces

---

### Baroque

Ornate, extravagant, richly detailed.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.05 |
| saturation_scale | 0.9 |
| detail_level | Extreme |
| edge_hardness | 0.55 |
| noise_octaves_offset | 1 |
| damage_amount | 0.1 |
| color_temperature | 0.3 |
| pattern_scale | 0.5 (fine ornate) |
| emission_tendency | 0.1 |

**Use for:** Palaces, cathedrals, royal items, ornate frames.

**Typical materials:** metal.gold, wood.carved, fabric.brocade, stone.marble

---

### ArtDeco

1920s-30s geometric elegance, symmetry.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.15 |
| saturation_scale | 0.8 |
| detail_level | High |
| edge_hardness | 0.9 |
| noise_octaves_offset | -1 |
| damage_amount | 0.05 |
| color_temperature | 0.1 |
| pattern_scale | 0.8 |
| emission_tendency | 0.2 |

**Use for:** Buildings, furniture, jewelry, posters.

**Typical materials:** metal.chrome, metal.gold, stone.marble, glass.black

---

## Condition-based Tokens

### PostApoc

Post-apocalyptic - damaged, improvised, scavenged.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.35 |
| saturation_scale | 0.55 |
| detail_level | High |
| edge_hardness | 0.4 |
| noise_octaves_offset | 2 |
| damage_amount | 0.7 (heavy) |
| color_temperature | 0.15 |
| pattern_scale | 1.1 |
| emission_tendency | 0.05 |

**Use for:** Wasteland, ruins, improvised weapons, survivors.

**Typical materials:** metal.rusted, fabric.torn, plastic.degraded, concrete.cracked

---

### Pristine

Brand new, factory fresh, untouched.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.2 |
| saturation_scale | 1.0 |
| detail_level | Medium |
| edge_hardness | 0.8 |
| noise_octaves_offset | -1 |
| damage_amount | 0.0 (none) |
| color_temperature | 0.0 |
| pattern_scale | 1.0 |
| emission_tendency | 0.1 |

**Use for:** New products, showrooms, clean environments.

**Typical materials:** Any with low roughness, no damage

---

### Corrupted

Tainted, infected, wrong - horror elements.

| Parameter | Value |
|-----------|-------|
| roughness_offset | 0.2 |
| saturation_scale | 0.7 |
| detail_level | High |
| edge_hardness | 0.3 |
| noise_octaves_offset | 3 (chaotic) |
| damage_amount | 0.5 |
| color_temperature | -0.3 (sickly cool) |
| pattern_scale | 0.6 |
| emission_tendency | 0.35 (unnatural glow) |

**Use for:** Infected areas, evil artifacts, monsters, blight.

**Typical materials:** organic.corrupted, crystal.corrupted, metal.tainted

---

### Ethereal

Otherworldly, ghostly, spiritual.

| Parameter | Value |
|-----------|-------|
| roughness_offset | -0.25 |
| saturation_scale | 0.7 |
| detail_level | Low |
| edge_hardness | 0.2 |
| noise_octaves_offset | 1 |
| damage_amount | 0.0 |
| color_temperature | -0.1 |
| pattern_scale | 1.5 |
| emission_tendency | 0.6 (glowing) |

**Use for:** Ghosts, spirits, magical effects, dreams.

**Typical materials:** Special translucent/emissive materials

---

## Combining Style Tokens

Style tokens can be blended for hybrid aesthetics:

**Algorithm (pseudocode):**
```
function blend_styles(style_a, style_b, weight):
    modifiers_a = get_modifiers(style_a)
    modifiers_b = get_modifiers(style_b)
    w = clamp(weight, 0.0, 1.0)
    inv = 1.0 - w

    return {
        roughness_offset: modifiers_a.roughness_offset * inv + modifiers_b.roughness_offset * w,
        saturation_scale: modifiers_a.saturation_scale * inv + modifiers_b.saturation_scale * w,
        detail_level: modifiers_b.detail_level if w > 0.5 else modifiers_a.detail_level,
        edge_hardness: modifiers_a.edge_hardness * inv + modifiers_b.edge_hardness * w,
        noise_octaves_offset: round(modifiers_a.noise_octaves_offset * inv + modifiers_b.noise_octaves_offset * w),
        damage_amount: modifiers_a.damage_amount * inv + modifiers_b.damage_amount * w,
        color_temperature: modifiers_a.color_temperature * inv + modifiers_b.color_temperature * w,
        pattern_scale: modifiers_a.pattern_scale * inv + modifiers_b.pattern_scale * w,
        emission_tendency: modifiers_a.emission_tendency * inv + modifiers_b.emission_tendency * w,
    }

# Example: 70% Steampunk, 30% Gothic
hybrid = blend_styles("steampunk", "gothic", 0.3)
```

---

## Language Examples

### Python

```python
from dataclasses import dataclass
from enum import Enum

class DetailLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

@dataclass
class StyleModifiers:
    roughness_offset: float
    saturation_scale: float
    detail_level: DetailLevel
    edge_hardness: float
    noise_octaves_offset: int
    damage_amount: float
    color_temperature: float
    pattern_scale: float
    emission_tendency: float

STYLE_TOKENS = {
    "cyberpunk": StyleModifiers(
        roughness_offset=-0.2,
        saturation_scale=1.4,
        detail_level=DetailLevel.HIGH,
        edge_hardness=0.9,
        noise_octaves_offset=0,
        damage_amount=0.2,
        color_temperature=-0.3,
        pattern_scale=0.7,
        emission_tendency=0.7,
    ),
    # ... other styles
}

def apply_style(base_params: dict, style_name: str) -> dict:
    style = STYLE_TOKENS[style_name]
    return {
        "roughness": base_params["roughness"] + style.roughness_offset,
        "saturation": base_params["saturation"] * style.saturation_scale,
        # ... apply other modifiers
    }
```

### JSON Schema

```json
{
  "type": "object",
  "properties": {
    "style": {
      "enum": ["rustic", "medieval", "cyberpunk", "scifi", "..."]
    },
    "modifiers": {
      "type": "object",
      "properties": {
        "roughness_offset": { "type": "number", "minimum": -0.3, "maximum": 0.4 },
        "saturation_scale": { "type": "number", "minimum": 0.5, "maximum": 1.4 },
        "detail_level": { "enum": ["low", "medium", "high", "extreme"] },
        "edge_hardness": { "type": "number", "minimum": 0, "maximum": 1 },
        "noise_octaves_offset": { "type": "integer", "minimum": -2, "maximum": 3 },
        "damage_amount": { "type": "number", "minimum": 0, "maximum": 1 },
        "color_temperature": { "type": "number", "minimum": -1, "maximum": 1 },
        "pattern_scale": { "type": "number", "minimum": 0.5, "maximum": 2 },
        "emission_tendency": { "type": "number", "minimum": 0, "maximum": 0.7 }
      }
    }
  }
}
```
