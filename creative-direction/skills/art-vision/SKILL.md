---
name: Art Vision
description: This skill should be used when the user asks about "art direction", "visual style", "color palette", "aesthetic", "visual coherence", "art style guide", "visual identity", "character design style", "environment style", "UI style", or discusses establishing or reviewing the visual direction of a game. Provides comprehensive art direction framework for defining and maintaining visual coherence.
version: 1.0.0
---

# Art Vision

Establish and maintain visual coherence across all game assets through a systematic art direction framework.

## Core Principles

### Visual Hierarchy

Every scene communicates through three levels:

1. **Primary Focus** - Where the player should look (characters, interactive objects)
2. **Secondary Context** - Environmental storytelling, navigation cues
3. **Tertiary Atmosphere** - Background, ambient detail, mood reinforcement

Ensure consistent hierarchy treatment across all assets. Primary elements should "read" at a glance.

### Style Spectrum Positioning

Position the game on key style spectrums:

| Spectrum | Left | Right |
|----------|------|-------|
| Fidelity | Stylized | Realistic |
| Detail | Simplified | Complex |
| Saturation | Desaturated | Vibrant |
| Contrast | Low-key | High-key |
| Form | Geometric | Organic |
| Line | Hard-edge | Soft/Painterly |

Document the position for each spectrum in the style bible. All assets should align.

### Color Theory Application

Define the palette using these categories:

**Primary Palette (3-5 colors)**
- Dominant color: 60% usage, sets tone
- Secondary color: 30% usage, creates interest
- Accent color: 10% usage, draws attention

**Functional Colors**
- Player/friendly: Consistent hue across all friendly elements
- Enemy/danger: Distinct from friendly, high recognition
- Interactive: Highlight affordances, subtle but learnable
- UI: Works on all backgrounds, maintains readability

**Emotional Palette Mapping**
- Safe zones: Warmer, more saturated
- Danger zones: Cooler, desaturated, or high contrast
- Transition areas: Blend between palettes

## Style Bible Structure

Create a style bible document with these sections:

### 1. Visual Pillars

Define 3-5 visual pillars - non-negotiable style principles:

```
Example pillars:
- "Readable silhouettes at all zoom levels"
- "Hand-painted texture feeling, not photo-real"
- "Color tells gameplay, not just aesthetics"
- "Negative space is a design element"
```

### 2. Reference Board

Collect reference images that capture the target aesthetic. Organize by:
- Overall mood
- Character style
- Environment style
- UI style
- Effects/VFX

### 3. Color Keys

Create color key paintings for:
- Each major environment type
- Time of day variations (if applicable)
- Emotional state variations (combat, exploration, dialogue)

### 4. Material Definitions

For ZX games, reference SADL material tokens. Define how materials should look:
- Surface roughness
- Specular behavior
- Color temperature shifts
- Weathering/age characteristics

### 5. Character Design Language

Define consistent traits:
- Proportion rules (head-to-body ratio, limb proportions)
- Silhouette requirements (identifiable at small scale)
- Costume design principles (color coding, functional detail)
- Face style (eyes, expression range)

### 6. Environment Design Language

Define spatial principles:
- Scale relationships (human-to-environment ratios)
- Architectural vocabulary (shapes, motifs)
- Vegetation style (simplified vs detailed)
- Lighting mood per zone type

## Coherence Assessment

When reviewing assets for coherence, check:

### Style Consistency
- Does the asset match the fidelity level of other assets?
- Is the detail density appropriate for its role in hierarchy?
- Does it use the defined shape language?

### Color Adherence
- Is the palette used correctly?
- Are functional colors applied consistently?
- Does saturation match the style spectrum position?

### Technical Consistency
- Consistent texture resolution relative to screen size
- Similar shading model across asset types
- Matching edge treatment (hard/soft)

### Composition in Context
- Does the asset integrate with its intended environment?
- Does it compete or complement existing visual hierarchy?
- Does it maintain the established spatial relationships?

## Integration with SADL

When working with Nethercore ZX procgen assets, map art direction to SADL:

**Style Tokens**
Select style tokens that match the established style:
- `rustic`, `cyberpunk`, `organic`, `geometric`, etc.
- Consistent token usage across related asset types

**Palettes**
Map the defined palette to SADL palette tokens:
- `warm_earthy`, `cool_metal`, `neon`, `pastel`, etc.
- Maintain palette consistency in generation prompts

**Materials**
Reference the material database for consistent surfaces:
- Document material preferences in style bible
- Apply consistently across generated assets

## Director Notes Format

When providing art direction feedback, structure notes as:

```
COHERENCE CHECK: [Asset/Area being reviewed]

ALIGNMENT:
- [What aligns with style bible]

DRIFT:
- [What deviates from established style]

RECOMMENDATIONS:
1. [Specific actionable adjustment]
2. [Priority: High/Medium/Low]

REFERENCE:
- [Link to style bible section or reference image]
```

## Establishing Art Direction

For new projects, run the vision establishment workflow:

1. **Gather inspiration** - Collect 10-20 reference images
2. **Extract patterns** - Identify common visual themes
3. **Define spectrums** - Position on each style spectrum
4. **Create pillars** - Write 3-5 visual principles
5. **Build palette** - Define primary, functional, emotional colors
6. **Document materials** - Specify surface treatments
7. **Create color keys** - Paint key moments
8. **Validate** - Test style against early assets

Store decisions in `.studio/creative-direction.local.md` for session persistence.

## Additional Resources

### Reference Files

For detailed guidance on specific topics:
- **`references/color-theory.md`** - Advanced color theory and palette building
- **`references/composition.md`** - Visual hierarchy and composition principles
- **`references/style-spectrums.md`** - Detailed spectrum definitions with examples

### SADL Integration

For ZX games, consult the SADL skill in `zx-procgen`:
- Style token definitions
- Material database
- Palette specifications
