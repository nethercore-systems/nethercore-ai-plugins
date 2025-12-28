# Color Theory for Game Art Direction

## Color Psychology in Games

### Emotional Associations

**Warm Colors (Red → Yellow)**
- Red: Danger, urgency, power, health
- Orange: Energy, warmth, caution
- Yellow: Optimism, treasure, attention

**Cool Colors (Green → Blue → Violet)**
- Green: Nature, healing, safety, poison (context-dependent)
- Blue: Calm, cold, water, mana/magic
- Violet: Mystery, magic, corruption, royalty

**Neutral Colors**
- White: Purity, light, empty, sterile
- Black: Darkness, void, death, power
- Gray: Neutrality, technology, ambiguity
- Brown: Earth, stability, mundane

### Context Shifts

Colors change meaning based on saturation and context:
- Bright red = health pickup
- Dark red = blood, danger
- Pale red/pink = friendly, healing

## Palette Construction Methods

### Monochromatic

Single hue, varying saturation and value.

```
Base Hue: 220° (Blue)
├── Dark:   HSV(220, 80, 20) - Shadows
├── Mid:    HSV(220, 60, 50) - Base
├── Light:  HSV(220, 40, 80) - Highlights
└── Accent: HSV(220, 90, 95) - Effects
```

**When to use**: Minimalist aesthetics, single-mood environments

### Analogous

3-5 adjacent hues on the wheel.

```
Center: 180° (Cyan)
├── -30°: 150° (Spring Green)
├── -15°: 165° (Green-Cyan)
├── Base: 180° (Cyan)
├── +15°: 195° (Cyan-Blue)
└── +30°: 210° (Blue)
```

**When to use**: Natural, harmonious environments (forests, underwater)

### Complementary

Opposite hues on the wheel.

```
Primary: 30° (Orange)
Complement: 210° (Blue)
```

**When to use**: High contrast, player vs. enemy distinction

### Split-Complementary

One hue + two adjacent to its complement.

```
Primary: 30° (Orange)
Split 1: 180° (Cyan)
Split 2: 240° (Blue-Violet)
```

**When to use**: Dynamic visuals with less harsh contrast

### Triadic

Three hues equally spaced (120° apart).

```
Primary: 0° (Red)
Secondary: 120° (Green)
Tertiary: 240° (Blue)
```

**When to use**: Balanced variety, multiple factions

## Value Structure

### The 5-Value System

Structure scenes with five value groups:

1. **Black (0-20%)**: Deep shadows, voids
2. **Dark (20-40%)**: Shadows, recessed areas
3. **Mid (40-60%)**: Local color, base materials
4. **Light (60-80%)**: Lit surfaces, highlights
5. **White (80-100%)**: Specular, light sources

### Notan (2-Value)

Reduce to black and white to check readability:
- If silhouettes are unclear, increase value contrast
- Player and enemies should read as distinct shapes

### Value for Depth

- **Foreground**: Higher contrast, darker darks
- **Midground**: Local values, full range
- **Background**: Lower contrast, pushed toward atmosphere color

## Saturation Control

### Saturation Rules

1. **Focus = Higher Saturation**: Draw eye to important elements
2. **Distance = Lower Saturation**: Atmospheric perspective
3. **Shadows = Lower Saturation**: Realistic light falloff
4. **Danger = Saturation Shift**: Break palette to signal threat

### The 60-30-10 Rule

- 60% coverage: Dominant color (often desaturated)
- 30% coverage: Secondary color (moderate saturation)
- 10% coverage: Accent color (high saturation)

## Practical Palette Templates

### Dark Fantasy

```yaml
dominant: HSV(220, 20, 25)   # Desaturated dark blue
secondary: HSV(30, 30, 40)   # Muted warm brown
accent: HSV(45, 80, 80)      # Warm gold (treasure, fire)
danger: HSV(0, 70, 50)       # Dark blood red
friendly: HSV(180, 40, 60)   # Soft cyan (magic, allies)
```

### Cyberpunk

```yaml
dominant: HSV(260, 30, 15)   # Dark purple-black
secondary: HSV(300, 60, 40)  # Magenta
accent: HSV(180, 90, 100)    # Bright cyan
danger: HSV(340, 80, 70)     # Hot pink-red
friendly: HSV(160, 70, 80)   # Mint green
```

### Nature/Pastoral

```yaml
dominant: HSV(120, 40, 50)   # Soft green
secondary: HSV(45, 50, 70)   # Warm straw
accent: HSV(200, 60, 80)     # Sky blue
danger: HSV(0, 60, 60)       # Rust red
friendly: HSV(60, 70, 90)    # Sunny yellow
```

## Color Accessibility

### Color Blindness Considerations

**Deuteranopia (Red-Green)**: ~8% of males
- Avoid red vs. green for critical distinction
- Use shape + color redundancy
- Test with deuteranopia simulation

**Protanopia (Red Weak)**: ~1% of population
- Reds appear darker than expected
- Ensure value contrast, not just hue

**Tritanopia (Blue-Yellow)**: Rare
- Blue and yellow can be confused
- Less common, lower priority

### Solutions

1. **Redundant coding**: Shape + color + size
2. **High value contrast**: Works without hue perception
3. **Colorblind mode**: Optional palette remapping
4. **Icon overlays**: Symbol redundancy for critical info

## Implementation Checklist

When establishing a palette:

- [ ] Define primary palette (3-5 colors with hex/HSV values)
- [ ] Document color meanings (what does each color signify)
- [ ] Create functional color assignments (player, enemy, interactive)
- [ ] Test value structure (notan check)
- [ ] Verify accessibility (colorblind simulation)
- [ ] Create color key paintings for each environment type
- [ ] Document exceptions (when rules can be broken)
