# Generation Recipes

Recipes combine style tokens, palettes, materials, and constraints into safe, reusable bundles.

## Recipe Structure

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

## Example Recipes

### Medieval Fantasy

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

MEDIEVAL_STONE = GenerationRecipe(
    name="medieval_stone",
    description="Stone structures, walls, arches",
    base_style=StyleToken.WEATHERED,
    palette=ColorPalette.MUTED,
    material="stone.mossy",
    shape_hints=["wall", "pillar", "arch"],
    scale_range=(1.0, 8.0),
    noise_amplitude_range=(0.02, 0.08),
    poly_budget=(200, 800),
    texture_resolution=256,
    uv_texel_density=128.0,
)
```

### Sci-Fi

```python
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

SCIFI_PROP = GenerationRecipe(
    name="scifi_prop",
    description="Sci-fi props, crates, containers",
    base_style=StyleToken.PRISTINE,
    palette=ColorPalette.COOL_METAL,
    material="metal.polished",
    shape_hints=["crate", "container", "device"],
    scale_range=(0.3, 2.0),
    noise_amplitude_range=(0.0, 0.005),
    poly_budget=(100, 400),
    texture_resolution=256,
    uv_texel_density=256.0,
)
```

### Cyberpunk

```python
CYBERPUNK_SIGN = GenerationRecipe(
    name="cyberpunk_sign",
    description="Neon signs, holographic displays",
    base_style=StyleToken.CYBERPUNK,
    palette=ColorPalette.NEON,
    material="tech.hologram",
    shape_hints=["sign", "display", "billboard"],
    scale_range=(0.5, 4.0),
    noise_amplitude_range=(0.0, 0.0),
    poly_budget=(20, 100),
    texture_resolution=128,
    uv_texel_density=64.0,
)
```

### Horror/Gothic

```python
GOTHIC_PROP = GenerationRecipe(
    name="gothic_prop",
    description="Horror/gothic props and furniture",
    base_style=StyleToken.GOTHIC,
    palette=ColorPalette.MUTED,
    material="wood.charred",
    shape_hints=["coffin", "tombstone", "candelabra"],
    scale_range=(0.3, 2.0),
    noise_amplitude_range=(0.02, 0.06),
    poly_budget=(100, 400),
    texture_resolution=256,
    uv_texel_density=256.0,
)
```

## Recipe Selection Guide

| Game Type | Recommended Recipe | Why |
|-----------|-------------------|-----|
| Medieval RPG | MEDIEVAL_PROP, MEDIEVAL_STONE | Rustic + WarmEarthy |
| Sci-Fi | SCIFI_PANEL, SCIFI_PROP | Geometric + CoolMetal |
| Horror | GOTHIC_PROP | Gothic + Muted |
| Cyberpunk | CYBERPUNK_SIGN | Cyberpunk + Neon |
| Cartoon | Custom (Stylized + Vibrant) | Vibrant colors |

## Custom Recipes

Create project-specific recipes in `.studio/recipes/`:

```python
# .studio/recipes/my_game.py

MY_GAME_WEAPON = GenerationRecipe(
    name="weapon",
    description="Stylized fantasy weapons",
    base_style=StyleToken.FANTASY,
    palette=ColorPalette.VIBRANT,
    material="metal.polished",
    shape_hints=["sword", "axe", "mace"],
    scale_range=(0.8, 1.5),
    noise_amplitude_range=(0.005, 0.015),
    poly_budget=(200, 600),
    texture_resolution=256,
    uv_texel_density=512.0,
)
```
