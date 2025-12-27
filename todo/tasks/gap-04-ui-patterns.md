# Gap 4: UI/UX Patterns

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

2D drawing FFI exists in zx-dev, but no design patterns for menus or HUDs.

## What's Missing

- Menu state machines (title -> game -> pause -> gameover)
- HUD layout patterns (health, score, minimap)
- Controller navigation (focus states, selection)
- Text/font rendering patterns

## Prompt for Implementation

```
Add skill "ui-patterns" to nethercore-zx-game-design. Triggers: "menu", "HUD",
"UI", "pause menu", "title screen", "user interface". Cover: menu state machines,
HUD layouts (health bars, score, minimap), controller navigation (focus, selection),
text rendering with rom_font. Reference 2D drawing FFI from zx-dev. Use references/
for common UI layouts. ~1200 words.
```

## Dependencies

- None

## Related Gaps

- Gap 24 (2D Sprites) covers *asset creation* for UI; this covers *code patterns*
