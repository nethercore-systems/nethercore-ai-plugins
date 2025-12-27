# Gap 1: Procedural Music (XM Tracker)

**Status:** `[x]` Completed
**Priority:** HIGH
**Plugin:** nethercore-zx-procgen
**Type:** Skill

---

## Problem

Sound effects are covered, but music composition is NOT covered. Currently just says "use MilkyTracker" with no procedural/compositional help.

## What's Missing

- XM module structure (patterns, instruments, samples)
- XM effects (arpeggio, vibrato, portamento, volume slides)
- Composition patterns (melodies, bass, percussion, pads)
- Genre templates (action, puzzle, title screen, boss)
- Loop point design for seamless looping
- Integration with procedural-sounds for custom instrument samples

## Prompt for Implementation

```
Add skill "procedural-music" to nethercore-zx-procgen. Triggers: "create music",
"XM tracker", "compose", "soundtrack", "tracker module", "game music". Cover: XM
structure (patterns, instruments, samples), XM effects (arpeggio, vibrato, portamento,
volume slides, etc), composition patterns (melodies, bass, percussion, pads), genre
templates (action, title, boss, ambient), loop points. Integration: use procedural-
sounds skill to generate custom instrument samples as WAVs. Tools: MilkyTracker/
OpenMPT. Constraints: 22kHz samples, 16MB ROM. Add references/ for effect commands
and composition patterns. ~1500 words.
```

## Dependencies

- None (standalone skill)

## Related Gaps

- Uses procedural-sounds for sample generation
