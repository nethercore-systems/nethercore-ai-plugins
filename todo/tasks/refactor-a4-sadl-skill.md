# Refactor A4: Semantic Asset Language (SADL) Skill

**Status:** `[ ]` Not Started
**Priority:** HIGH
**Action:** Create NEW semantic-asset-language skill for style tokens

---

## Problem

LLMs can understand creative intent but have no vocabulary to translate it to procedural parameters. Gap 22 defines what should be covered, this refactor is the implementation action.

## Proposed Skill

- Plugin: `nethercore-zx-procgen`
- Skill: `semantic-asset-language` (NEW)

## Content

### Style Tokens
```rust
enum StyleToken {
    Rustic,      // Aged, worn, natural
    Cyberpunk,   // Neon, chrome, high contrast
    Organic,     // Smooth curves, natural patterns
    Geometric,   // Sharp edges, mathematical
    Fantasy,     // Magical, ethereal
    PostApoc,    // Damaged, dirty
    Minimalist,  // Simple, clean
    Baroque,     // Ornate, detailed
}
```

### Color Palettes
- WarmEarthy, CoolMetal, Neon, Muted, Vibrant
- HSL ranges for each palette
- Sampling functions

### Material Semantics
- `metal.polished`, `metal.rusted`, `metal.copper`
- `wood.polished`, `wood.weathered`, `wood.painted`
- `stone.rough`, `stone.polished`, `stone.mossy`
- PBR parameter mappings

### Shape Vocabulary
- Primitive mappings (barrel, crate, crystal)
- Composition rules

### Constrained Recipes
- Safe parameter ranges
- Style-specific presets

## Implementation Steps

1. Create skill file following Gap 22 specification
2. Define all style tokens with parameter modifiers
3. Define all color palettes with HSL ranges
4. Define material database with PBR params
5. Add code examples for applying styles

## Dependencies

- None

## Related Gaps

- Gap 22 (AI-First Creative Pipeline) - this is part of Gap 22
- A5 (Creative Agents) uses this vocabulary
