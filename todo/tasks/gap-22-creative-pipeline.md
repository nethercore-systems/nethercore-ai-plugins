# Gap 22: AI-First Creative Asset Pipeline

**Status:** `[ ]` Not Started
**Priority:** HIGH
**Plugin:** nethercore-zx-procgen
**Type:** Skill + Agents

---

## Problem

NOT covered. Current agents only review/optimize existing assets. No creative generation workflow.

LLMs are excellent at understanding creative intent ("make it look more organic", "give it a cyberpunk vibe", "weathered medieval style") but the current plugin has no system for translating these descriptions into procedural parameters.

Developers must manually:
1. Interpret creative requirements into specific values
2. Guess at parameter combinations
3. Iterate through trial and error
4. Have no way to describe "good" vs "bad" results programmatically

## What Should Exist

### Semantic Asset Description Language (SADL)
- **Style Tokens:** rustic, cyberpunk, organic, geometric
- **Color Palettes:** warm_earthy, neon, muted, vibrant
- **Materials:** metal.polished, wood.weathered, stone.rough
- **Shapes:** barrel, crystal, humanoid, mechanical

### Creative Agents (Configurable Mode: Interactive | Autonomous)
- **asset-designer** - Interprets requirements, produces specs
- **asset-generator** - Produces procedural code from specs
- **asset-critic** - Evaluates quality, suggests fixes
- **creative-orchestrator** - Coordinates full pipeline

### Quality Heuristics (Self-Assessment)
- Texture: contrast > 0.2, noise coherence, tileability
- Mesh: poly budget, no degenerates, UV coverage > 95%
- Animation: arc principle, anticipation, follow-through

### Iterative Refinement Workflow
Generate → Self-Assess → Present → Feedback → Refine

## Code Examples

### Style Tokens with Parameter Modifiers

```rust
/// Style token definitions with parameter modifiers
pub enum StyleToken {
    Rustic,      // Aged, worn, natural materials
    Cyberpunk,   // Neon, chrome, high contrast
    Organic,     // Smooth curves, natural patterns
    Geometric,   // Sharp edges, mathematical precision
    Fantasy,     // Magical, ethereal, saturated
    PostApoc,    // Damaged, dirty, improvised
    Minimalist,  // Simple, clean, low detail
    Baroque,     // Ornate, detailed, complex
}

/// Parameter modifiers for each style token
pub struct StyleModifiers {
    pub roughness_offset: f32,      // Added to base roughness
    pub saturation_scale: f32,      // Multiplied with saturation
    pub detail_level: DetailLevel,  // Low, Medium, High
    pub edge_hardness: f32,         // 0.0 = soft, 1.0 = sharp
    pub noise_octaves_offset: i32,  // Added to noise octaves
    pub damage_amount: f32,         // 0.0 = pristine, 1.0 = destroyed
}

impl StyleToken {
    pub fn modifiers(&self) -> StyleModifiers {
        match self {
            StyleToken::Rustic => StyleModifiers {
                roughness_offset: 0.3,
                saturation_scale: 0.7,
                detail_level: DetailLevel::Medium,
                edge_hardness: 0.3,
                noise_octaves_offset: 1,
                damage_amount: 0.4,
            },
            StyleToken::Cyberpunk => StyleModifiers {
                roughness_offset: -0.2,     // More reflective
                saturation_scale: 1.4,      // More vivid
                detail_level: DetailLevel::High,
                edge_hardness: 0.9,         // Sharp edges
                noise_octaves_offset: 0,
                damage_amount: 0.1,
            },
            StyleToken::Organic => StyleModifiers {
                roughness_offset: 0.1,
                saturation_scale: 0.9,
                detail_level: DetailLevel::Medium,
                edge_hardness: 0.1,         // Very soft
                noise_octaves_offset: 2,    // More natural variation
                damage_amount: 0.0,
            },
            // ... additional style tokens
        }
    }
}

/// Apply style token to base material parameters
pub fn apply_style(base: &MaterialParams, style: StyleToken) -> MaterialParams {
    let mods = style.modifiers();
    MaterialParams {
        roughness: (base.roughness + mods.roughness_offset).clamp(0.0, 1.0),
        saturation: base.saturation * mods.saturation_scale,
        detail_level: mods.detail_level,
        // ... apply other modifiers
    }
}
```

### Color Palette Semantics

```rust
/// Semantic color palettes with HSL ranges
pub enum ColorPalette {
    WarmEarthy,    // Browns, oranges, tans (wood, leather, earth)
    CoolMetal,     // Silvers, blues, grays (steel, chrome, iron)
    Neon,          // Bright magentas, cyans, greens (cyberpunk, arcade)
    Muted,         // Low saturation, any hue (stone, concrete, fabric)
    Vibrant,       // High saturation, varied hue (fantasy, cartoon)
    Monochrome,    // Single hue, varied lightness (stylized)
}

pub struct PaletteSpec {
    pub hue_ranges: Vec<(f32, f32)>,      // Allowed hue ranges (0-360)
    pub saturation_range: (f32, f32),     // Min-max saturation (0-1)
    pub lightness_range: (f32, f32),      // Min-max lightness (0-1)
    pub primary_weight: f32,              // Weight for primary vs accent
}

impl ColorPalette {
    pub fn spec(&self) -> PaletteSpec {
        match self {
            ColorPalette::WarmEarthy => PaletteSpec {
                hue_ranges: vec![(15.0, 45.0)],  // Orange-brown range
                saturation_range: (0.3, 0.6),
                lightness_range: (0.2, 0.5),
                primary_weight: 0.8,
            },
            ColorPalette::Neon => PaletteSpec {
                hue_ranges: vec![(280.0, 320.0), (160.0, 200.0)],  // Magenta + Cyan
                saturation_range: (0.8, 1.0),
                lightness_range: (0.5, 0.7),
                primary_weight: 0.5,  // Equal primary/accent
            },
            // ... additional palettes
        }
    }

    /// Generate a color from this palette
    pub fn sample(&self, rng: &mut impl Rng) -> [f32; 3] {
        let spec = self.spec();
        let hue_range = &spec.hue_ranges[rng.gen_range(0..spec.hue_ranges.len())];
        let h = rng.gen_range(hue_range.0..hue_range.1);
        let s = rng.gen_range(spec.saturation_range.0..spec.saturation_range.1);
        let l = rng.gen_range(spec.lightness_range.0..spec.lightness_range.1);
        hsl_to_rgb(h, s, l)
    }
}
```

### Material Database

```rust
/// Material database - maps semantic strings to PBR params
pub fn material_from_semantic(descriptor: &str) -> Option<PbrParams> {
    match descriptor {
        // Metals
        "metal.polished" => Some(PbrParams {
            base_color: [0.9, 0.9, 0.9],
            metallic: 1.0,
            roughness: 0.1,
            normal_strength: 0.3,
            ao_strength: 0.5,
            emission: 0.0,
        }),
        "metal.rusted" => Some(PbrParams {
            base_color: [0.5, 0.3, 0.2],
            metallic: 0.3,      // Rust is less metallic
            roughness: 0.8,
            normal_strength: 1.0,
            ao_strength: 0.9,
            emission: 0.0,
        }),
        // Woods
        "wood.weathered" => Some(PbrParams {
            base_color: [0.35, 0.30, 0.25],
            metallic: 0.0,
            roughness: 0.9,
            normal_strength: 1.0,
            ao_strength: 0.9,
            emission: 0.0,
        }),
        // Stones
        "stone.mossy" => Some(PbrParams {
            base_color: [0.35, 0.45, 0.30],
            metallic: 0.0,
            roughness: 0.85,
            normal_strength: 0.9,
            ao_strength: 1.0,
            emission: 0.0,
        }),
        // ... additional materials
        _ => None,
    }
}
```

### Constrained Generation Recipes

```rust
/// A constrained generation recipe with safe parameter ranges
pub struct GenerationRecipe {
    pub name: &'static str,
    pub description: &'static str,
    pub base_style: StyleToken,
    pub palette: ColorPalette,
    pub material: &'static str,
    pub shape_base: &'static str,
    pub scale_range: (f32, f32),
    pub noise_amplitude_range: (f32, f32),
    pub detail_poly_budget: (u32, u32),
    pub uv_texel_density: f32,
}

pub const RECIPES: &[GenerationRecipe] = &[
    GenerationRecipe {
        name: "medieval_prop",
        description: "Generic medieval-fantasy props (barrels, crates, furniture)",
        base_style: StyleToken::Rustic,
        palette: ColorPalette::WarmEarthy,
        material: "wood.weathered",
        shape_base: "crate",
        scale_range: (0.5, 2.0),
        noise_amplitude_range: (0.01, 0.05),
        detail_poly_budget: (100, 500),
        uv_texel_density: 256.0,
    },
    GenerationRecipe {
        name: "scifi_panel",
        description: "Sci-fi wall panels, consoles, tech surfaces",
        base_style: StyleToken::Geometric,
        palette: ColorPalette::CoolMetal,
        material: "metal.brushed",
        shape_base: "crate",
        scale_range: (1.0, 4.0),
        noise_amplitude_range: (0.0, 0.01),
        detail_poly_budget: (50, 200),
        uv_texel_density: 512.0,
    },
];
```

### Quality Heuristics

```rust
/// Quality assessment for generated textures
pub struct TextureQuality {
    pub contrast: f32,         // 0-1, should be > 0.2
    pub noise_coherence: f32,  // 0-1, should be > 0.5
    pub tileability: f32,      // 0-1, edge continuity score
    pub unique_colors: u32,    // Should be > 100 for most textures
    pub histogram_balance: f32, // 0-1, avoid over-bright/dark
}

impl TextureQuality {
    pub fn passes_minimum(&self) -> bool {
        self.contrast > 0.15 &&
        self.noise_coherence > 0.4 &&
        self.tileability > 0.8 &&
        self.unique_colors > 50 &&
        self.histogram_balance > 0.3
    }

    pub fn issues(&self) -> Vec<&'static str> {
        let mut issues = vec![];
        if self.contrast <= 0.15 { issues.push("Too flat/uniform - add more variation"); }
        if self.noise_coherence <= 0.4 { issues.push("Noise too random - increase coherence"); }
        if self.tileability <= 0.8 { issues.push("Visible seams when tiled - check edges"); }
        if self.unique_colors <= 50 { issues.push("Too few colors - add subtle variation"); }
        if self.histogram_balance <= 0.3 { issues.push("Too dark or too bright overall"); }
        issues
    }
}

/// Quality assessment for generated meshes
pub struct MeshQuality {
    pub vertex_count: u32,
    pub triangle_count: u32,
    pub degenerate_tris: u32,      // Should be 0
    pub uv_coverage: f32,          // Should be > 0.95
    pub uv_overlap: f32,           // Should be < 0.05
    pub max_stretch: f32,          // UV stretch, should be < 2.0
    pub watertight: bool,          // No holes
}

impl MeshQuality {
    pub fn passes_for_budget(&self, max_triangles: u32) -> bool {
        self.triangle_count <= max_triangles &&
        self.degenerate_tris == 0 &&
        self.uv_coverage > 0.95 &&
        self.uv_overlap < 0.05 &&
        self.max_stretch < 2.0
    }
}
```

## Prompt for Implementation

```
Add skill "semantic-asset-language" to nethercore-zx-procgen. Triggers: "SADL",
"semantic asset", "style token", "design asset", "creative asset", "asset
description", "material semantic", "shape vocabulary", "color palette semantic".

Create agents: asset-designer, asset-generator, asset-critic, creative-orchestrator
in nethercore-zx-procgen.

Cover: Full SADL specification (style tokens → parameters, color palettes → HSL,
materials → PBR, shapes → primitives), constrained generation recipes (safe
parameter ranges), quality heuristics (texture contrast/coherence/tileability,
mesh poly/UV/watertight, animation principles), agent definitions with configurable
modes (interactive vs autonomous), iterative refinement workflow, LLM self-assessment
prompts.

Agents should use parameters block for mode configuration. asset-designer and
creative-orchestrator support interactive/autonomous modes. asset-critic supports
lenient/normal/strict strictness.

Include complete Rust code examples for style tokens, color palettes, material
database, shape vocabulary, constrained recipes, quality assessment functions.
~2500 words for skill, ~500 words per agent.
```

## Dependencies

- None

## Related Gaps

- Gap 15 (Character Pipeline) for character generation via creative agents
- A4 (SADL Skill) and A5 (Creative Agents) are refactors related to this gap
