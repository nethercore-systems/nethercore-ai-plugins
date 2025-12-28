---
name: Semantic Asset Description Language (SADL)
description: This skill should be used when the user asks about "SADL", "semantic asset", "style token", "design asset", "creative asset", "asset description", "material semantic", "shape vocabulary", "color palette semantic", "style guide", "asset recipe", "constrained generation", "quality heuristics", "asset quality metrics", "creative workflow", "asset pipeline design", or wants to translate creative intent ("make it look rustic", "cyberpunk vibe", "weathered medieval") into procedural generation parameters. Provides the Semantic Asset Description Language specification for bridging creative descriptions and procedural code.
version: 1.0.0
---

# Semantic Asset Description Language (SADL)

SADL bridges creative intent and procedural generation. Instead of manually guessing parameter values, describe assets semantically and let the system translate to concrete parameters.

## Core Concepts

SADL has four pillars:

1. **Style Tokens** - Visual style descriptors (rustic, cyberpunk, organic)
2. **Color Palettes** - Semantic color schemes (warm_earthy, neon, pastel)
3. **Materials** - PBR parameter presets (metal.polished, wood.weathered)
4. **Shape Vocabulary** - Base primitive descriptors (barrel, crystal, humanoid)

These combine into **Generation Recipes** - constrained parameter bundles that produce consistent, quality results.

---

## Style Tokens

Style tokens modify base generation parameters to achieve a visual style. Each token defines offsets and multipliers for roughness, saturation, detail level, edge hardness, noise, and damage.

### Core Style Token Structure

```rust
pub struct StyleModifiers {
    pub roughness_offset: f32,      // Added to base roughness (-0.3 to +0.5)
    pub saturation_scale: f32,      // Multiplied with saturation (0.5 to 1.5)
    pub detail_level: DetailLevel,  // Low, Medium, High, Extreme
    pub edge_hardness: f32,         // 0.0 = soft organic, 1.0 = sharp geometric
    pub noise_octaves_offset: i32,  // Added to noise octaves (-2 to +3)
    pub damage_amount: f32,         // 0.0 = pristine, 1.0 = destroyed
    pub color_temperature: f32,     // -1.0 = cool, 0.0 = neutral, 1.0 = warm
}

pub enum DetailLevel {
    Low,      // Minimal detail, flat surfaces
    Medium,   // Standard detail
    High,     // Rich detail, many features
    Extreme,  // Maximum detail (use sparingly)
}
```

### Applying Style Tokens

```rust
pub fn apply_style(base: &MaterialParams, style: StyleToken) -> MaterialParams {
    let mods = style.modifiers();
    MaterialParams {
        roughness: (base.roughness + mods.roughness_offset).clamp(0.0, 1.0),
        saturation: (base.saturation * mods.saturation_scale).clamp(0.0, 1.0),
        detail_level: mods.detail_level,
        edge_hardness: mods.edge_hardness,
        damage: mods.damage_amount,
        // ... apply other modifiers
    }
}

// Usage
let base = MaterialParams::default();
let styled = apply_style(&base, StyleToken::Cyberpunk);
```

For the complete list of **15+ style tokens** with full parameter values, see `references/style-tokens.md`.

---

## Color Palettes

Color palettes define HSL ranges for consistent color schemes. Each palette specifies allowed hue ranges, saturation bounds, and lightness bounds.

### Palette Structure

```rust
pub struct PaletteSpec {
    pub hue_ranges: Vec<(f32, f32)>,      // Allowed hue ranges (0-360)
    pub saturation_range: (f32, f32),     // Min-max saturation (0-1)
    pub lightness_range: (f32, f32),      // Min-max lightness (0-1)
    pub accent_hue_offset: f32,           // Offset for accent colors
    pub primary_weight: f32,              // Weight for primary vs accent (0-1)
}

impl ColorPalette {
    /// Sample a color from this palette
    pub fn sample(&self, rng: &mut impl Rng) -> [f32; 3] {
        let spec = self.spec();
        let hue_range = &spec.hue_ranges[rng.gen_range(0..spec.hue_ranges.len())];
        let h = rng.gen_range(hue_range.0..hue_range.1);
        let s = rng.gen_range(spec.saturation_range.0..spec.saturation_range.1);
        let l = rng.gen_range(spec.lightness_range.0..spec.lightness_range.1);
        hsl_to_rgb(h, s, l)
    }

    /// Sample primary and accent colors
    pub fn sample_pair(&self, rng: &mut impl Rng) -> ([f32; 3], [f32; 3]) {
        let primary = self.sample(rng);
        let accent = self.sample_accent(rng);
        (primary, accent)
    }
}
```

### Common Palettes

| Palette | Hue Range | Saturation | Lightness | Use For |
|---------|-----------|------------|-----------|---------|
| WarmEarthy | 15-45 (orange-brown) | 0.3-0.6 | 0.2-0.5 | Wood, leather, earth |
| CoolMetal | 200-240 (blue-gray) | 0.1-0.3 | 0.4-0.7 | Steel, chrome, iron |
| Neon | 280-320, 160-200 | 0.8-1.0 | 0.5-0.7 | Cyberpunk, arcade |
| Pastel | Any hue | 0.3-0.5 | 0.7-0.85 | Soft, dreamy, cute |
| Muted | Any hue | 0.1-0.3 | 0.3-0.6 | Stone, concrete, worn |
| Vibrant | Any hue | 0.7-1.0 | 0.4-0.6 | Fantasy, cartoon |

For the complete list of **12 color palettes** with full specifications, see `references/color-palettes.md`.

---

## Material Database

Materials map semantic descriptors to PBR parameters. Use dot notation: `category.variant`.

### Material Structure

```rust
pub struct PbrParams {
    pub base_color: [f32; 3],     // RGB (0-1)
    pub metallic: f32,            // 0 = dielectric, 1 = metal
    pub roughness: f32,           // 0 = mirror, 1 = rough
    pub normal_strength: f32,     // Normal map intensity
    pub ao_strength: f32,         // Ambient occlusion
    pub emission: f32,            // 0 = none, >0 = glow
}

/// Lookup material by semantic descriptor
pub fn material_from_semantic(descriptor: &str) -> Option<PbrParams> {
    match descriptor {
        "metal.polished" => Some(PbrParams {
            base_color: [0.9, 0.9, 0.9],
            metallic: 1.0,
            roughness: 0.1,
            ..Default::default()
        }),
        "wood.weathered" => Some(PbrParams {
            base_color: [0.35, 0.30, 0.25],
            metallic: 0.0,
            roughness: 0.9,
            normal_strength: 1.0,
            ..Default::default()
        }),
        // ... more materials
        _ => None,
    }
}
```

### Material Categories

| Category | Variants | Key Properties |
|----------|----------|----------------|
| metal | polished, brushed, rusted, oxidized, chrome, gold, copper | High metallic |
| wood | fresh, weathered, painted, charred, mossy | Low metallic, high roughness |
| stone | polished, rough, mossy, cracked, marble | Low metallic, varied roughness |
| fabric | cotton, silk, leather, velvet, wool | Low metallic, medium roughness |
| plastic | glossy, matte, rubber, translucent | Low metallic, varied roughness |
| organic | skin, bark, bone, chitin, coral | Low metallic, organic patterns |
| crystal | clear, colored, magical, corrupted | Low roughness, optional emission |
| tech | screen, panel, circuit, hologram | Varied, often emissive |

For the complete **40+ material definitions** with PBR values, see `references/material-database.md`.

---

## Generation Recipes

Recipes combine style tokens, palettes, materials, and constraints into safe, reusable bundles.

### Recipe Structure

```rust
pub struct GenerationRecipe {
    pub name: &'static str,
    pub description: &'static str,
    pub base_style: StyleToken,
    pub palette: ColorPalette,
    pub material: &'static str,
    pub shape_hints: Vec<&'static str>,

    // Constraints
    pub scale_range: (f32, f32),
    pub noise_amplitude_range: (f32, f32),
    pub poly_budget: (u32, u32),
    pub texture_resolution: u32,
    pub uv_texel_density: f32,
}

impl GenerationRecipe {
    /// Generate parameters from this recipe
    pub fn generate(&self, rng: &mut impl Rng) -> GeneratedParams {
        let style_mods = self.base_style.modifiers();
        let base_material = material_from_semantic(self.material).unwrap();
        let color = self.palette.sample(rng);

        GeneratedParams {
            material: apply_style(&base_material, self.base_style),
            color,
            scale: rng.gen_range(self.scale_range.0..self.scale_range.1),
            noise_amp: rng.gen_range(self.noise_amplitude_range.0..self.noise_amplitude_range.1),
            max_polys: rng.gen_range(self.poly_budget.0..self.poly_budget.1),
            texture_size: self.texture_resolution,
        }
    }
}
```

### Example Recipes

```rust
pub const MEDIEVAL_PROP: GenerationRecipe = GenerationRecipe {
    name: "medieval_prop",
    description: "Medieval-fantasy props (barrels, crates, furniture)",
    base_style: StyleToken::Rustic,
    palette: ColorPalette::WarmEarthy,
    material: "wood.weathered",
    shape_hints: vec!["crate", "barrel", "chest"],
    scale_range: (0.5, 2.0),
    noise_amplitude_range: (0.01, 0.05),
    poly_budget: (100, 500),
    texture_resolution: 256,
    uv_texel_density: 256.0,
};

pub const SCIFI_PANEL: GenerationRecipe = GenerationRecipe {
    name: "scifi_panel",
    description: "Sci-fi wall panels, consoles, tech surfaces",
    base_style: StyleToken::Geometric,
    palette: ColorPalette::CoolMetal,
    material: "metal.brushed",
    shape_hints: vec!["panel", "console", "terminal"],
    scale_range: (1.0, 4.0),
    noise_amplitude_range: (0.0, 0.01),
    poly_budget: (50, 200),
    texture_resolution: 256,
    uv_texel_density: 512.0,
};
```

---

## Quality Heuristics

SADL includes self-assessment heuristics for generated assets. Use these to validate output quality.

### Texture Quality

```rust
pub struct TextureQuality {
    pub contrast: f32,         // Should be > 0.15
    pub noise_coherence: f32,  // Should be > 0.4
    pub tileability: f32,      // Should be > 0.8 for tiling textures
    pub unique_colors: u32,    // Should be > 50
    pub histogram_balance: f32, // Should be > 0.3
}

impl TextureQuality {
    pub fn passes_minimum(&self) -> bool {
        self.contrast > 0.15 &&
        self.noise_coherence > 0.4 &&
        self.histogram_balance > 0.3
    }

    pub fn issues(&self) -> Vec<&'static str> {
        let mut issues = vec![];
        if self.contrast <= 0.15 {
            issues.push("Too flat - add more variation");
        }
        if self.tileability <= 0.8 {
            issues.push("Visible seams when tiled");
        }
        issues
    }
}
```

### Mesh Quality

```rust
pub struct MeshQuality {
    pub triangle_count: u32,
    pub degenerate_tris: u32,      // Should be 0
    pub uv_coverage: f32,          // Should be > 0.95
    pub uv_overlap: f32,           // Should be < 0.05
    pub max_stretch: f32,          // Should be < 2.0
    pub watertight: bool,          // No holes
}

impl MeshQuality {
    pub fn passes_for_budget(&self, max_triangles: u32) -> bool {
        self.triangle_count <= max_triangles &&
        self.degenerate_tris == 0 &&
        self.uv_coverage > 0.95 &&
        self.max_stretch < 2.0
    }
}
```

### Animation Quality (12 Principles)

| Principle | Heuristic | Check |
|-----------|-----------|-------|
| Anticipation | Pre-action pose exists | Duration > 0 for windup |
| Follow-through | Post-action settle | Overshoot + settle frames |
| Arcs | Motion paths curved | Not linear interpolation |
| Timing | Appropriate duration | Action-specific ranges |
| Exaggeration | Poses pushed | Scale > 1.0 at peaks |

For complete quality heuristics with measurement code, see `references/quality-heuristics.md`.

---

## Creative Workflow

SADL supports an iterative creative workflow:

```
1. DESCRIBE  →  "I want a weathered medieval barrel"
2. INTERPRET →  Style: Rustic, Palette: WarmEarthy, Material: wood.weathered
3. GENERATE  →  Produce mesh + textures with recipe constraints
4. ASSESS    →  Run quality heuristics, identify issues
5. REFINE    →  Adjust parameters based on assessment
6. PRESENT   →  Show result with quality metrics
7. FEEDBACK  →  User approves or requests changes
8. ITERATE   →  Loop back to step 5 if needed
```

### Creative Agents

SADL is implemented by four specialized agents:

| Agent | Role | Mode |
|-------|------|------|
| `asset-designer` | Interprets requirements → specs | Interactive / Autonomous |
| `asset-generator` | Produces code from specs | Autonomous |
| `asset-critic` | Evaluates quality, suggests fixes | Lenient / Normal / Strict |
| `creative-orchestrator` | Coordinates full pipeline | Interactive / Autonomous |

---

## Quick Reference

### Semantic Description Examples

| Natural Language | SADL Translation |
|------------------|------------------|
| "rusty old barrel" | Style: Rustic, Material: metal.rusted, Shape: barrel |
| "glowing crystal" | Style: Fantasy, Material: crystal.magical, Emission: 0.8 |
| "clean sci-fi panel" | Style: Geometric, Material: metal.brushed, Damage: 0.0 |
| "overgrown stone" | Style: Organic, Material: stone.mossy, Palette: Muted |
| "neon cyberpunk sign" | Style: Cyberpunk, Material: tech.hologram, Palette: Neon |

### Common Combinations

| Game Type | Recommended Recipe |
|-----------|-------------------|
| Medieval RPG | Rustic + WarmEarthy + wood/stone |
| Sci-Fi | Geometric + CoolMetal + metal/tech |
| Horror | Gothic + Muted + stone/organic |
| Cartoon | Stylized + Vibrant + any |
| Cyberpunk | Cyberpunk + Neon + metal/tech |

---

## Additional Resources (Language-Agnostic)

All reference files use data tables and pseudocode algorithms that work across any language:

- `references/style-tokens.md` - Complete style token definitions with tables and multi-language examples
- `references/color-palettes.md` - Full palette specifications
- `references/material-database.md` - All material PBR values
- `references/quality-heuristics.md` - Quality measurement algorithms
