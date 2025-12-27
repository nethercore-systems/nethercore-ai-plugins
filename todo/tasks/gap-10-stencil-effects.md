# Gap 10: Stencil / Masked Rendering

**Status:** `[x]` Completed
**Priority:** LOW
**Plugin:** nethercore-zx-dev
**Type:** Skill

---

## Problem

FFI exists for stencil operations, NO usage patterns documented. Stencil buffer enables portals, scopes, mirrors, and masked effects.

## FFI Functions (from zx.rs)

- `stencil_begin()` - Start writing to stencil buffer
- `stencil_end()` - Stop writing to stencil buffer
- `stencil_clear()` - Clear stencil buffer
- `stencil_invert()` - Invert stencil mask

## What's Missing

- Portal/window rendering pattern
- Scope/binocular effect
- Mirror reflection technique
- UI masking for non-rectangular elements
- Stencil + depth interaction

## Prompt for Implementation

```
Add skill "stencil-effects" to nethercore-zx-dev. Triggers: "stencil", "portal",
"scope", "masked rendering", "mirror", "window effect". Cover: stencil buffer
basics, portal/window pattern (draw mask, then scene), scope/binocular effect,
mirror reflections (stencil + flipped camera), UI masking. Include code examples.
Source: include/zx.rs stencil section. ~800 words.
```

## Dependencies

- None

## Related Gaps

- Gap 17 (Camera) for mirror reflection camera flip
