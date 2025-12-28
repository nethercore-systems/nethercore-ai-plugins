# Style Spectrum Definitions

Position your game on each spectrum to define its visual identity. Document positions in the style bible.

## Fidelity Spectrum

**Stylized ←————————————→ Realistic**

### Stylized (1-3)
- Exaggerated proportions
- Simplified forms
- Abstracted textures
- Clear readable shapes
- Timeless aesthetic

Examples: Cuphead, Hollow Knight, Okami

### Moderate (4-6)
- Recognizable proportions with artistic license
- Some detail abstraction
- Stylized materials with realistic lighting
- Balance of readability and immersion

Examples: Borderlands, Valorant, Fortnite

### Realistic (7-9)
- Accurate proportions
- High-detail textures
- Physically-based materials
- Photographic reference
- Ages with technology

Examples: The Last of Us, Red Dead Redemption, Horizon

### Questions to Answer
- Is visual clarity or immersion the priority?
- What reference sources should artists use?
- How will the style age over time?

---

## Detail Spectrum

**Simplified ←————————————→ Complex**

### Simplified (1-3)
- Flat colors or minimal gradients
- Few edge details
- Large shape language
- Iconic over representational
- Fast to produce

Examples: Thomas Was Alone, Superhot, VVVVVV

### Moderate (4-6)
- Some texture detail
- Medium shape complexity
- Recognizable but not exhaustive
- Balanced production time

Examples: Celeste, Dead Cells, Slay the Spire

### Complex (7-9)
- Intricate patterns and textures
- High polygon/resolution
- Layered detail levels
- Rewards close inspection
- High production cost

Examples: Ori series, Hades, Hollow Knight

### Questions to Answer
- What's the viewing distance? (Close-up vs distant camera)
- What's the production timeline?
- How many unique assets are needed?

---

## Saturation Spectrum

**Desaturated ←————————————→ Vibrant**

### Desaturated (1-3)
- Near-monochromatic
- Muted, washed out
- Grim, serious, or melancholic tone
- Color used sparingly for emphasis

Examples: Limbo, Inside, Dark Souls

### Moderate (4-6)
- Natural saturation levels
- Color present but controlled
- Balanced emotional range
- Versatile mood palette

Examples: Breath of the Wild, Ghost of Tsushima, Subnautica

### Vibrant (7-9)
- High saturation throughout
- Bold color choices
- Energetic, playful, or fantastical
- Strong immediate impact

Examples: Rayman Legends, Splatoon, Katamari Damacy

### Questions to Answer
- What emotional range does the game need?
- Is readability or atmosphere priority?
- How does saturation change with game state?

---

## Contrast Spectrum

**Low-Key ←————————————→ High-Key**

### Low-Key (1-3)
- Dark overall value
- Limited bright areas
- Noir, horror, or mysterious mood
- Shadows dominate

Examples: Limbo, Darkest Dungeon, Amnesia

### Moderate (4-6)
- Full value range
- Balanced light/dark
- Natural lighting feel
- Adaptable mood

Examples: Most AAA games, Zelda series, Uncharted

### High-Key (7-9)
- Bright overall value
- Limited shadows
- Light, airy, optimistic
- Highlights dominate

Examples: Journey, Monument Valley, A Short Hike

### Questions to Answer
- What's the primary emotional tone?
- How important are shadows for gameplay?
- What time of day / lighting scenario is typical?

---

## Form Spectrum

**Geometric ←————————————→ Organic**

### Geometric (1-3)
- Hard edges, flat planes
- Mathematical precision
- Clean, artificial, controlled
- Tech, architecture, abstract

Examples: Superhot, Fez, Thomas Was Alone

### Moderate (4-6)
- Mix of geometric and organic
- Stylized natural forms
- Architectural with organic touches
- Versatile application

Examples: Portal, Hades, Transistor

### Organic (7-9)
- Curved, flowing forms
- Natural imperfection
- Biological, living aesthetic
- Nature, creatures, flowing

Examples: Ori series, Hollow Knight (bugs), Subnautica

### Questions to Answer
- What's the world's nature? (Tech vs nature)
- What emotion should forms convey?
- What's the dominant subject matter?

---

## Line Spectrum

**Hard-Edge ←————————————→ Soft/Painterly**

### Hard-Edge (1-3)
- Clean, defined outlines
- Sharp transitions
- Graphic, illustrative
- Cel-shaded appearance

Examples: Jet Set Radio, Borderlands, Guilty Gear

### Moderate (4-6)
- Selective outlines
- Some soft blending
- Mixed edge treatment
- Context-dependent lines

Examples: Okami, Hades, Genshin Impact

### Soft/Painterly (7-9)
- No or minimal outlines
- Blended transitions
- Brushstroke textures
- Traditional painting feel

Examples: Ori series, Limbo, Child of Light

### Questions to Answer
- Is graphic clarity or painterly mood priority?
- How will characters read against backgrounds?
- What art historical style is referenced?

---

## Using the Spectrums

### 1. Rate Your Game

For each spectrum, pick a position (1-9):

```
Fidelity:   [   ] Stylized ←——[X]——→ Realistic
Detail:     [   ] Simple ←—[X]———→ Complex
Saturation: [   ] Muted ←————[X]→ Vibrant
Contrast:   [   ] Low-key ←—[X]——→ High-key
Form:       [   ] Geometric ←[X]——→ Organic
Line:       [   ] Hard ←——[X]———→ Soft
```

### 2. Document in Style Bible

```yaml
style_spectrums:
  fidelity: 4      # Moderate, slightly stylized
  detail: 6        # Moderate complexity
  saturation: 5    # Balanced, natural
  contrast: 4      # Slightly low-key
  form: 7          # Organic dominant
  line: 3          # Hard-edge, graphic
```

### 3. Validate Assets

When reviewing assets, check spectrum alignment:
- Does this asset match the documented position?
- If it differs, is it intentional (e.g., faction differentiation)?
- Are all artists calibrated to the same positions?

### 4. Handle Exceptions

Document when and why spectrums shift:
- UI may be more geometric than game world
- Effects may be more vibrant than environments
- Different factions may occupy different positions

---

## Spectrum Combinations

### Common Pairings

**Stylized + Desaturated + Low-Key**
→ Indie horror, atmospheric puzzle

**Realistic + Moderate + Moderate**
→ AAA action-adventure

**Stylized + Vibrant + High-Key**
→ Casual, family-friendly

**Stylized + Simple + Hard-Edge**
→ Minimalist, arcade

### Tension Combinations

**Realistic + Vibrant**
→ Fantasy realism (Horizon, Monster Hunter)

**Simple + Organic**
→ Stylized nature (Journey, Flower)

**Complex + Hard-Edge**
→ Graphic but detailed (Hades, Okami)

Use spectrum combinations to find your unique visual identity.
