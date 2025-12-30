---
name: Visual Style Guide
description: |
  Use this skill for consistent visual style across assets.

  **Triggers:** "visual style", "art style", "how should it look", "color palette", "material", "PBR".

  **Before generating:** Check `.studio/visual-style.local.md` for project style.

  **Load references when:**
  - Style tokens (retro, gothic, etc.) → `references/style-tokens.md`
  - Color palettes → `references/color-palettes.md`
  - PBR material params → `references/material-database.md`
  - Metal materials specifically → `references/materials-metals.md`
  - Natural materials (wood, stone) → `references/materials-natural.md`
  - Quality assessment → `references/quality-heuristics.md`
version: 3.0.0
---

# Visual Style Guide

Reference for maintaining consistent visual style across procedurally generated assets.

## Style Presets

Style tokens modify base generation parameters to achieve a visual style. Each token defines offsets and multipliers for roughness, saturation, detail level, edge hardness, noise, and damage.

### Core Style Token Structure

```python
from dataclasses import dataclass
from enum import Enum

class DetailLevel(Enum):
    LOW = "low"          # Minimal detail, flat surfaces
    MEDIUM = "medium"    # Standard detail
    HIGH = "high"        # Rich detail, many features
    EXTREME = "extreme"  # Maximum detail (use sparingly)

@dataclass
class StyleModifiers:
    roughness_offset: float     # Added to base roughness (-0.3 to +0.5)
    saturation_scale: float     # Multiplied with saturation (0.5 to 1.5)
    detail_level: DetailLevel   # Low, Medium, High, Extreme
    edge_hardness: float        # 0.0 = soft organic, 1.0 = sharp geometric
    noise_octaves_offset: int   # Added to noise octaves (-2 to +3)
    damage_amount: float        # 0.0 = pristine, 1.0 = destroyed
    color_temperature: float    # -1.0 = cool, 0.0 = neutral, 1.0 = warm
```

### Applying Style Tokens

```python
def apply_style(base: MaterialParams, style: StyleToken) -> MaterialParams:
    """Apply style modifiers to base material parameters."""
    mods = style.modifiers()
    return MaterialParams(
        roughness=np.clip(base.roughness + mods.roughness_offset, 0.0, 1.0),
        saturation=np.clip(base.saturation * mods.saturation_scale, 0.0, 1.0),
        detail_level=mods.detail_level,
        edge_hardness=mods.edge_hardness,
        damage=mods.damage_amount,
        # ... apply other modifiers
    )

# Usage
base = MaterialParams()
styled = apply_style(base, StyleToken.CYBERPUNK)
```

For the complete list of **15+ style tokens** with full parameter values, see `references/style-tokens.md`.

---

## Color Palettes

Color palettes define HSL ranges for consistent color schemes. Each palette specifies allowed hue ranges, saturation bounds, and lightness bounds.

### Palette Structure

```python
from dataclasses import dataclass
from typing import List
import random
import colorsys

@dataclass
class PaletteSpec:
    hue_ranges: List[tuple[float, float]]  # Allowed hue ranges (0-360)
    saturation_range: tuple[float, float]   # Min-max saturation (0-1)
    lightness_range: tuple[float, float]    # Min-max lightness (0-1)
    accent_hue_offset: float                # Offset for accent colors
    primary_weight: float                    # Weight for primary vs accent (0-1)

class ColorPalette:
    def __init__(self, spec: PaletteSpec):
        self.spec = spec

    def sample(self) -> tuple[float, float, float]:
        """Sample a color from this palette."""
        hue_range = random.choice(self.spec.hue_ranges)
        h = random.uniform(hue_range[0], hue_range[1]) / 360.0  # Normalize to 0-1
        s = random.uniform(*self.spec.saturation_range)
        l = random.uniform(*self.spec.lightness_range)
        return colorsys.hls_to_rgb(h, l, s)  # Returns RGB tuple

    def sample_pair(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Sample primary and accent colors."""
        primary = self.sample()
        accent = self.sample_accent()
        return (primary, accent)
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

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PbrParams:
    base_color: tuple[float, float, float]  # RGB (0-1)
    metallic: float = 0.0           # 0 = dielectric, 1 = metal
    roughness: float = 0.5          # 0 = mirror, 1 = rough
    normal_strength: float = 1.0    # Normal map intensity
    ao_strength: float = 1.0        # Ambient occlusion
    emission: float = 0.0           # 0 = none, >0 = glow

# Material database
MATERIALS = {
    "metal.polished": PbrParams(
        base_color=(0.9, 0.9, 0.9),
        metallic=1.0,
        roughness=0.1
    ),
    "wood.weathered": PbrParams(
        base_color=(0.35, 0.30, 0.25),
        metallic=0.0,
        roughness=0.9,
        normal_strength=1.0
    ),
    # ... more materials
}

def material_from_semantic(descriptor: str) -> Optional[PbrParams]:
    """Lookup material by semantic descriptor."""
    return MATERIALS.get(descriptor)
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

```python
from dataclasses import dataclass
from typing import List
import random

@dataclass
class GenerationRecipe:
    name: str
    description: str
    base_style: StyleToken
    palette: ColorPalette
    material: str
    shape_hints: List[str]

    # Constraints
    scale_range: tuple[float, float]
    noise_amplitude_range: tuple[float, float]
    poly_budget: tuple[int, int]
    texture_resolution: int
    uv_texel_density: float

    def generate(self) -> 'GeneratedParams':
        """Generate parameters from this recipe."""
        style_mods = self.base_style.modifiers()
        base_material = material_from_semantic(self.material)
        color = self.palette.sample()

        return GeneratedParams(
            material=apply_style(base_material, self.base_style),
            color=color,
            scale=random.uniform(*self.scale_range),
            noise_amp=random.uniform(*self.noise_amplitude_range),
            max_polys=random.randint(*self.poly_budget),
            texture_size=self.texture_resolution
        )
```

### Example Recipes

```python
MEDIEVAL_PROP = GenerationRecipe(
    name="medieval_prop",
    description="Medieval-fantasy props (barrels, crates, furniture)",
    base_style=StyleToken.RUSTIC,
    palette=ColorPalette.WARM_EARTHY,
    material="wood.weathered",
    shape_hints=["crate", "barrel", "chest"],
    scale_range=(0.5, 2.0),
    noise_amplitude_range=(0.01, 0.05),
    poly_budget=(100, 500),
    texture_resolution=256,
    uv_texel_density=256.0,
)

SCIFI_PANEL = GenerationRecipe(
    name="scifi_panel",
    description="Sci-fi wall panels, consoles, tech surfaces",
    base_style=StyleToken.GEOMETRIC,
    palette=ColorPalette.COOL_METAL,
    material="metal.brushed",
    shape_hints=["panel", "console", "terminal"],
    scale_range=(1.0, 4.0),
    noise_amplitude_range=(0.0, 0.01),
    poly_budget=(50, 200),
    texture_resolution=256,
    uv_texel_density=512.0,
)
```

---

## Quality Heuristics

The style guide includes self-assessment heuristics for generated assets. Use these to validate output quality.

### Texture Quality

```python
from dataclasses import dataclass
from typing import List

@dataclass
class TextureQuality:
    contrast: float         # Should be > 0.15
    noise_coherence: float  # Should be > 0.4
    tileability: float      # Should be > 0.8 for tiling textures
    unique_colors: int      # Should be > 50
    histogram_balance: float # Should be > 0.3

    def passes_minimum(self) -> bool:
        return (
            self.contrast > 0.15 and
            self.noise_coherence > 0.4 and
            self.histogram_balance > 0.3
        )

    def issues(self) -> List[str]:
        issues = []
        if self.contrast <= 0.15:
            issues.append("Too flat - add more variation")
        if self.tileability <= 0.8:
            issues.append("Visible seams when tiled")
        return issues
```

### Mesh Quality

```python
from dataclasses import dataclass

@dataclass
class MeshQuality:
    triangle_count: int
    degenerate_tris: int      # Should be 0
    uv_coverage: float        # Should be > 0.95
    uv_overlap: float         # Should be < 0.05
    max_stretch: float        # Should be < 2.0
    watertight: bool          # No holes

    def passes_for_budget(self, max_triangles: int) -> bool:
        return (
            self.triangle_count <= max_triangles and
            self.degenerate_tris == 0 and
            self.uv_coverage > 0.95 and
            self.max_stretch < 2.0
        )
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

The style guide supports an iterative creative workflow:

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

The style guide is implemented by four specialized agents:

| Agent | Role | Mode |
|-------|------|------|
| `asset-designer` | Interprets requirements → specs | Interactive / Autonomous |
| `asset-generator` | Produces code from specs | Autonomous |
| `asset-critic` | Evaluates quality, suggests fixes | Lenient / Normal / Strict |
| `creative-orchestrator` | Coordinates full pipeline | Interactive / Autonomous |

---

## Quick Reference

### Semantic Description Examples

| Natural Language | Style Translation |
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
