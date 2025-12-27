# Style Tokens Reference

Complete style token definitions for SADL. Each token modifies base generation parameters to achieve a consistent visual style.

## Token Definition Structure

```rust
pub enum StyleToken {
    // Natural/Historical
    Rustic,
    Medieval,
    Ancient,
    Victorian,

    // Modern/Futuristic
    Cyberpunk,
    Scifi,
    Industrial,
    Minimalist,

    // Organic/Natural
    Organic,
    Overgrown,
    Crystalline,
    Elemental,

    // Stylized
    Fantasy,
    Gothic,
    Steampunk,
    Dieselpunk,

    // Abstract/Artistic
    Geometric,
    Abstract,
    Baroque,
    ArtDeco,

    // Condition-based
    PostApoc,
    Pristine,
    Corrupted,
    Ethereal,
}

pub struct StyleModifiers {
    pub roughness_offset: f32,      // Added to base roughness
    pub saturation_scale: f32,      // Multiplied with saturation
    pub detail_level: DetailLevel,  // Low, Medium, High, Extreme
    pub edge_hardness: f32,         // 0.0 = soft, 1.0 = sharp
    pub noise_octaves_offset: i32,  // Added to noise octaves
    pub damage_amount: f32,         // 0.0 = pristine, 1.0 = destroyed
    pub color_temperature: f32,     // -1.0 = cool, 1.0 = warm
    pub pattern_scale: f32,         // Pattern size multiplier
    pub emission_tendency: f32,     // Likelihood of emissive elements
}

pub enum DetailLevel {
    Low,      // Flat, simple surfaces
    Medium,   // Standard detail
    High,     // Rich texturing
    Extreme,  // Maximum detail
}
```

---

## Natural/Historical Tokens

### Rustic

Aged, worn, natural materials with visible use and weathering.

```rust
StyleToken::Rustic => StyleModifiers {
    roughness_offset: 0.3,
    saturation_scale: 0.7,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.3,
    noise_octaves_offset: 1,
    damage_amount: 0.4,
    color_temperature: 0.3,      // Warm
    pattern_scale: 1.0,
    emission_tendency: 0.0,
}
```

**Use for:** Barns, wooden furniture, farm equipment, leather goods, handcrafted items.

**Typical materials:** wood.weathered, leather.worn, metal.rusted, fabric.burlap

---

### Medieval

European medieval aesthetic - stone, iron, heavy construction.

```rust
StyleToken::Medieval => StyleModifiers {
    roughness_offset: 0.25,
    saturation_scale: 0.6,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.5,
    noise_octaves_offset: 1,
    damage_amount: 0.3,
    color_temperature: 0.1,      // Slightly warm
    pattern_scale: 1.2,
    emission_tendency: 0.05,     // Torches, forges
}
```

**Use for:** Castles, armor, weapons, taverns, markets, dungeons.

**Typical materials:** stone.rough, metal.iron, wood.oak, fabric.wool

---

### Ancient

Old civilizations - weathered stone, faded colors, archaeological feel.

```rust
StyleToken::Ancient => StyleModifiers {
    roughness_offset: 0.4,
    saturation_scale: 0.5,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.2,          // Eroded edges
    noise_octaves_offset: 2,
    damage_amount: 0.6,
    color_temperature: 0.2,
    pattern_scale: 1.5,
    emission_tendency: 0.0,
}
```

**Use for:** Ruins, temples, tombs, artifacts, fossils.

**Typical materials:** stone.weathered, metal.oxidized, ceramic.cracked

---

### Victorian

19th century elegance - ornate, rich, formal.

```rust
StyleToken::Victorian => StyleModifiers {
    roughness_offset: -0.1,      // More polished
    saturation_scale: 0.8,
    detail_level: DetailLevel::High,
    edge_hardness: 0.6,
    noise_octaves_offset: 0,
    damage_amount: 0.1,
    color_temperature: 0.2,
    pattern_scale: 0.8,          // Finer patterns
    emission_tendency: 0.1,      // Gas lamps
}
```

**Use for:** Mansions, furniture, clothing, gadgets, street scenes.

**Typical materials:** wood.polished, fabric.velvet, metal.brass, leather.fine

---

## Modern/Futuristic Tokens

### Cyberpunk

Neon, chrome, high contrast, high-tech low-life.

```rust
StyleToken::Cyberpunk => StyleModifiers {
    roughness_offset: -0.2,      // More reflective
    saturation_scale: 1.4,       // Vivid colors
    detail_level: DetailLevel::High,
    edge_hardness: 0.9,          // Sharp edges
    noise_octaves_offset: 0,
    damage_amount: 0.2,
    color_temperature: -0.3,     // Cool with neon accents
    pattern_scale: 0.7,
    emission_tendency: 0.7,      // Lots of neon/screens
}
```

**Use for:** Cities, tech, vehicles, clothing, weapons, UI elements.

**Typical materials:** metal.chrome, tech.screen, plastic.glossy, fabric.synthetic

---

### Scifi

Clean futuristic - sleek, minimal, advanced technology.

```rust
StyleToken::Scifi => StyleModifiers {
    roughness_offset: -0.15,
    saturation_scale: 0.9,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.85,
    noise_octaves_offset: -1,    // Cleaner surfaces
    damage_amount: 0.05,
    color_temperature: -0.2,     // Cool
    pattern_scale: 0.6,
    emission_tendency: 0.4,
}
```

**Use for:** Spaceships, stations, equipment, uniforms, interfaces.

**Typical materials:** metal.brushed, plastic.matte, tech.panel, composite.carbon

---

### Industrial

Factories, machinery, utilitarian design.

```rust
StyleToken::Industrial => StyleModifiers {
    roughness_offset: 0.2,
    saturation_scale: 0.5,       // Desaturated
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.7,
    noise_octaves_offset: 1,
    damage_amount: 0.35,
    color_temperature: -0.1,
    pattern_scale: 1.3,
    emission_tendency: 0.15,
}
```

**Use for:** Factories, pipes, machinery, warehouses, tools.

**Typical materials:** metal.painted, metal.rusted, concrete.stained, rubber.worn

---

### Minimalist

Simple, clean, essential forms only.

```rust
StyleToken::Minimalist => StyleModifiers {
    roughness_offset: -0.1,
    saturation_scale: 0.6,
    detail_level: DetailLevel::Low,
    edge_hardness: 0.8,
    noise_octaves_offset: -2,    // Very clean
    damage_amount: 0.0,
    color_temperature: 0.0,      // Neutral
    pattern_scale: 2.0,          // Large, simple shapes
    emission_tendency: 0.1,
}
```

**Use for:** Modern furniture, UI, icons, architectural elements.

**Typical materials:** plastic.matte, wood.light, metal.white, fabric.cotton

---

## Organic/Natural Tokens

### Organic

Natural, flowing, biological forms.

```rust
StyleToken::Organic => StyleModifiers {
    roughness_offset: 0.1,
    saturation_scale: 0.9,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.1,          // Very soft edges
    noise_octaves_offset: 2,     // Natural variation
    damage_amount: 0.0,
    color_temperature: 0.1,
    pattern_scale: 1.0,
    emission_tendency: 0.05,
}
```

**Use for:** Creatures, plants, terrain, caves, coral.

**Typical materials:** organic.skin, organic.bark, organic.chitin, stone.natural

---

### Overgrown

Nature reclaiming - moss, vines, decay.

```rust
StyleToken::Overgrown => StyleModifiers {
    roughness_offset: 0.25,
    saturation_scale: 0.85,
    detail_level: DetailLevel::High,
    edge_hardness: 0.2,
    noise_octaves_offset: 2,
    damage_amount: 0.5,
    color_temperature: 0.15,
    pattern_scale: 0.9,
    emission_tendency: 0.02,     // Bioluminescence
}
```

**Use for:** Ruins, abandoned structures, forest floors, swamps.

**Typical materials:** stone.mossy, wood.rotting, metal.rusted, organic.moss

---

### Crystalline

Gemstones, ice, mineral formations.

```rust
StyleToken::Crystalline => StyleModifiers {
    roughness_offset: -0.3,      // Very smooth
    saturation_scale: 1.2,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.95,         // Sharp facets
    noise_octaves_offset: 0,
    damage_amount: 0.0,
    color_temperature: -0.2,
    pattern_scale: 0.5,
    emission_tendency: 0.3,
}
```

**Use for:** Gems, ice caves, magical crystals, mineral veins.

**Typical materials:** crystal.clear, crystal.colored, crystal.magical, ice.solid

---

### Elemental

Primal forces - fire, water, earth, air manifestations.

```rust
StyleToken::Elemental => StyleModifiers {
    roughness_offset: 0.0,       // Varies by element
    saturation_scale: 1.3,
    detail_level: DetailLevel::High,
    edge_hardness: 0.5,
    noise_octaves_offset: 3,     // Chaotic natural patterns
    damage_amount: 0.0,
    color_temperature: 0.0,      // Varies by element
    pattern_scale: 0.8,
    emission_tendency: 0.5,      // Often glowing
}
```

**Use for:** Elementals, magical effects, environmental hazards.

**Typical materials:** Depends on element - lava, water, stone, energy

---

## Stylized Tokens

### Fantasy

Magical, colorful, exaggerated proportions.

```rust
StyleToken::Fantasy => StyleModifiers {
    roughness_offset: 0.05,
    saturation_scale: 1.2,
    detail_level: DetailLevel::High,
    edge_hardness: 0.4,
    noise_octaves_offset: 1,
    damage_amount: 0.1,
    color_temperature: 0.2,
    pattern_scale: 0.9,
    emission_tendency: 0.25,
}
```

**Use for:** Magic items, creatures, enchanted locations, artifacts.

**Typical materials:** metal.enchanted, crystal.magical, fabric.silk, wood.ancient

---

### Gothic

Dark, ornate, dramatic shadows.

```rust
StyleToken::Gothic => StyleModifiers {
    roughness_offset: 0.15,
    saturation_scale: 0.6,
    detail_level: DetailLevel::High,
    edge_hardness: 0.7,
    noise_octaves_offset: 1,
    damage_amount: 0.25,
    color_temperature: -0.2,     // Cool
    pattern_scale: 0.7,
    emission_tendency: 0.1,
}
```

**Use for:** Cathedrals, crypts, vampires, spooky mansions.

**Typical materials:** stone.dark, metal.iron, wood.ebony, fabric.black

---

### Steampunk

Victorian + steam technology - brass, gears, leather.

```rust
StyleToken::Steampunk => StyleModifiers {
    roughness_offset: 0.1,
    saturation_scale: 0.75,
    detail_level: DetailLevel::Extreme,
    edge_hardness: 0.6,
    noise_octaves_offset: 1,
    damage_amount: 0.2,
    color_temperature: 0.4,      // Warm brass tones
    pattern_scale: 0.6,          // Fine gears and details
    emission_tendency: 0.15,
}
```

**Use for:** Gadgets, vehicles, clothing, cities, weapons.

**Typical materials:** metal.brass, metal.copper, leather.brown, wood.mahogany

---

### Dieselpunk

1920s-40s + diesel tech - rivets, heavy machinery.

```rust
StyleToken::Dieselpunk => StyleModifiers {
    roughness_offset: 0.2,
    saturation_scale: 0.6,
    detail_level: DetailLevel::High,
    edge_hardness: 0.75,
    noise_octaves_offset: 1,
    damage_amount: 0.3,
    color_temperature: 0.1,
    pattern_scale: 0.9,
    emission_tendency: 0.1,
}
```

**Use for:** War machines, factories, cities, uniforms.

**Typical materials:** metal.riveted, metal.painted, leather.military, rubber.industrial

---

## Abstract/Artistic Tokens

### Geometric

Mathematical precision, hard edges, patterns.

```rust
StyleToken::Geometric => StyleModifiers {
    roughness_offset: -0.1,
    saturation_scale: 0.9,
    detail_level: DetailLevel::Medium,
    edge_hardness: 1.0,          // Maximum sharpness
    noise_octaves_offset: -2,
    damage_amount: 0.0,
    color_temperature: 0.0,
    pattern_scale: 1.0,
    emission_tendency: 0.2,
}
```

**Use for:** Abstract art, UI, tech, mathematical constructs.

**Typical materials:** Any with clean surfaces

---

### Abstract

Non-representational, artistic expression.

```rust
StyleToken::Abstract => StyleModifiers {
    roughness_offset: 0.0,
    saturation_scale: 1.1,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.5,          // Variable
    noise_octaves_offset: 2,
    damage_amount: 0.0,
    color_temperature: 0.0,
    pattern_scale: 0.7,
    emission_tendency: 0.3,
}
```

**Use for:** Art pieces, dream sequences, special effects.

**Typical materials:** Variable - artistic choice

---

### Baroque

Ornate, extravagant, richly detailed.

```rust
StyleToken::Baroque => StyleModifiers {
    roughness_offset: -0.05,
    saturation_scale: 0.9,
    detail_level: DetailLevel::Extreme,
    edge_hardness: 0.55,
    noise_octaves_offset: 1,
    damage_amount: 0.1,
    color_temperature: 0.3,
    pattern_scale: 0.5,          // Fine ornate details
    emission_tendency: 0.1,
}
```

**Use for:** Palaces, cathedrals, royal items, ornate frames.

**Typical materials:** metal.gold, wood.carved, fabric.brocade, stone.marble

---

### ArtDeco

1920s-30s geometric elegance, symmetry.

```rust
StyleToken::ArtDeco => StyleModifiers {
    roughness_offset: -0.15,
    saturation_scale: 0.8,
    detail_level: DetailLevel::High,
    edge_hardness: 0.9,
    noise_octaves_offset: -1,
    damage_amount: 0.05,
    color_temperature: 0.1,
    pattern_scale: 0.8,
    emission_tendency: 0.2,
}
```

**Use for:** Buildings, furniture, jewelry, posters.

**Typical materials:** metal.chrome, metal.gold, stone.marble, glass.black

---

## Condition-based Tokens

### PostApoc

Post-apocalyptic - damaged, improvised, scavenged.

```rust
StyleToken::PostApoc => StyleModifiers {
    roughness_offset: 0.35,
    saturation_scale: 0.55,
    detail_level: DetailLevel::High,
    edge_hardness: 0.4,
    noise_octaves_offset: 2,
    damage_amount: 0.7,          // Heavy damage
    color_temperature: 0.15,
    pattern_scale: 1.1,
    emission_tendency: 0.05,
}
```

**Use for:** Wasteland, ruins, improvised weapons, survivors.

**Typical materials:** metal.rusted, fabric.torn, plastic.degraded, concrete.cracked

---

### Pristine

Brand new, factory fresh, untouched.

```rust
StyleToken::Pristine => StyleModifiers {
    roughness_offset: -0.2,
    saturation_scale: 1.0,
    detail_level: DetailLevel::Medium,
    edge_hardness: 0.8,
    noise_octaves_offset: -1,
    damage_amount: 0.0,          // No damage
    color_temperature: 0.0,
    pattern_scale: 1.0,
    emission_tendency: 0.1,
}
```

**Use for:** New products, showrooms, clean environments.

**Typical materials:** Any with low roughness, no damage

---

### Corrupted

Tainted, infected, wrong - horror elements.

```rust
StyleToken::Corrupted => StyleModifiers {
    roughness_offset: 0.2,
    saturation_scale: 0.7,
    detail_level: DetailLevel::High,
    edge_hardness: 0.3,
    noise_octaves_offset: 3,     // Chaotic patterns
    damage_amount: 0.5,
    color_temperature: -0.3,     // Sickly cool
    pattern_scale: 0.6,
    emission_tendency: 0.35,     // Unnatural glow
}
```

**Use for:** Infected areas, evil artifacts, monsters, blight.

**Typical materials:** organic.corrupted, crystal.corrupted, metal.tainted

---

### Ethereal

Otherworldly, ghostly, spiritual.

```rust
StyleToken::Ethereal => StyleModifiers {
    roughness_offset: -0.25,
    saturation_scale: 0.7,
    detail_level: DetailLevel::Low,
    edge_hardness: 0.2,
    noise_octaves_offset: 1,
    damage_amount: 0.0,
    color_temperature: -0.1,
    pattern_scale: 1.5,
    emission_tendency: 0.6,      // Glowing, transparent
}
```

**Use for:** Ghosts, spirits, magical effects, dreams.

**Typical materials:** Special translucent/emissive materials

---

## Combining Style Tokens

Style tokens can be blended for hybrid aesthetics:

```rust
pub fn blend_styles(a: StyleToken, b: StyleToken, weight: f32) -> StyleModifiers {
    let ma = a.modifiers();
    let mb = b.modifiers();
    let w = weight.clamp(0.0, 1.0);
    let inv = 1.0 - w;

    StyleModifiers {
        roughness_offset: ma.roughness_offset * inv + mb.roughness_offset * w,
        saturation_scale: ma.saturation_scale * inv + mb.saturation_scale * w,
        detail_level: if w > 0.5 { mb.detail_level } else { ma.detail_level },
        edge_hardness: ma.edge_hardness * inv + mb.edge_hardness * w,
        noise_octaves_offset: ((ma.noise_octaves_offset as f32 * inv) +
                               (mb.noise_octaves_offset as f32 * w)).round() as i32,
        damage_amount: ma.damage_amount * inv + mb.damage_amount * w,
        color_temperature: ma.color_temperature * inv + mb.color_temperature * w,
        pattern_scale: ma.pattern_scale * inv + mb.pattern_scale * w,
        emission_tendency: ma.emission_tendency * inv + mb.emission_tendency * w,
    }
}

// Example: 70% Steampunk, 30% Gothic
let hybrid = blend_styles(StyleToken::Steampunk, StyleToken::Gothic, 0.3);
```
