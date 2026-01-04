# Project Memory File Templates

## creative-direction.md

```markdown
---
# Creative Direction Configuration
# This file is read by the creative-direction plugin

# Art Direction
art_style: [style-name]  # e.g., dark-fantasy-painterly, pixel-art-retro
color_palette: [palette-name]  # e.g., desaturated-warm, vibrant-neon
style_spectrums:
  fidelity: 5     # 1=stylized, 9=realistic
  detail: 5       # 1=simple, 9=complex
  saturation: 5   # 1=muted, 9=vibrant
  contrast: 5     # 1=low-key, 9=high-key
  form: 5         # 1=geometric, 9=organic
  line: 5         # 1=hard-edge, 9=soft

# Sound Direction
sonic_identity: [identity]  # e.g., organic-ambient, synthetic-punchy
mix_priority: [priority]    # gameplay-first, music-forward, ambient-rich
audio_pillars:
  - [pillar-1]
  - [pillar-2]

# Tech Direction
architecture: [pattern]     # ecs-rollback, component-based, traditional-oop
determinism: [required|optional]
file_size_limit: 300        # Maximum lines per source file

# Creative Vision
creative_pillars:
  - [pillar-1]
  - [pillar-2]
  - [pillar-3]
target_audience: [audience-description]
avoid_patterns:
  - [anti-pattern-1]
  - [anti-pattern-2]
---

# Project Vision

[Write your experience promise here - one paragraph describing the core experience]

---

# Art Direction Notes

Accumulated visual direction decisions:

<!-- Add entries with dates -->

---

# Sound Direction Notes

Accumulated audio direction decisions:

<!-- Add entries with dates -->

---

# Tech Direction Notes

Accumulated technical direction decisions:

<!-- Add entries with dates -->

---

# Current Focus

What's being worked on:
- [Current task 1]
- [Current task 2]

Next priorities:
- [Next task 1]
```

## project-status.md

```markdown
# Project Status

Last updated: YYYY-MM-DD HH:MM

## Phase

Current: [Phase Name]  <!-- e.g., Prototype, Alpha, Beta, Polish -->
Started: YYYY-MM-DD
Target: YYYY-MM-DD

## Current Sprint/Focus

Focus: [What we're building right now]

### In Progress

- [ ] [Task 1]
  - [x] [Subtask completed]
  - [ ] [Subtask pending]
- [ ] [Task 2]

### Completed This Sprint

- [x] [Completed task 1]
- [x] [Completed task 2]

## Recent Decisions

- YYYY-MM-DD: [Decision made]
- YYYY-MM-DD: [Another decision]

## Blockers

- [Blocker description] - [Status/notes]

OR

- None currently

## Next Up

After current work:
1. [Next priority 1]
2. [Next priority 2]
3. [Next priority 3]

## Notes for Next Session

[Any context the next session needs to know]
```

## architecture/decisions.md

```markdown
# Architecture Decision Records

This document indexes all architecture decisions for the project.

## Decision Log

| # | Title | Status | Date |
|---|-------|--------|------|
| 1 | [Decision title] | [Proposed/Accepted/Deprecated] | YYYY-MM-DD |

## Quick Reference

### Current Architecture

- **Pattern**: [e.g., ECS with rollback support]
- **Language**: [e.g., Rust with WASM target]
- **Build System**: [e.g., Cargo + nether CLI]

### Key Decisions Summary

1. **[Topic]**: [One-line summary of decision]
2. **[Topic]**: [One-line summary of decision]

### Superseded Decisions

| Original | Superseded By | Date |
|----------|---------------|------|
| ADR-XXX | ADR-YYY | YYYY-MM-DD |
```

## Individual ADR Template

File: `architecture/NNN-short-title.md`

```markdown
# ADR-[NUMBER]: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date

YYYY-MM-DD

## Context

[What is the issue that motivates this decision? What forces are at play?]

## Decision

[What is the change we're making?]

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative

- [Drawback or trade-off 1]
- [Drawback or trade-off 2]

### Neutral

- [Side effect or consideration]

## Alternatives Considered

### [Alternative 1 Name]

- **Description**: [What this option was]
- **Rejected because**: [Why we didn't choose it]

### [Alternative 2 Name]

- **Description**: [What this option was]
- **Rejected because**: [Why we didn't choose it]

## Related Decisions

- ADR-XXX: [Related decision]
- ADR-YYY: [Another related decision]
```

## art-direction.md (Shared)

```markdown
# Art Direction

This document captures the visual style decisions for the project.

## Style Summary

| Aspect | Choice |
|--------|--------|
| Art Style | [Name/Description] |
| Primary Palette | [Palette name] |
| Fidelity Level | [1-9 with description] |

## Visual Pillars

1. **[Pillar 1]**: [How it manifests visually]
2. **[Pillar 2]**: [How it manifests visually]
3. **[Pillar 3]**: [How it manifests visually]

## Color Palette

### Primary Colors

| Name | Hex | Usage |
|------|-----|-------|
| Dominant | #XXXXXX | [Where used] |
| Secondary | #XXXXXX | [Where used] |
| Accent | #XXXXXX | [Where used] |

### Functional Colors

| Function | Color | Notes |
|----------|-------|-------|
| Player/Friendly | #XXXXXX | [Notes] |
| Enemy/Danger | #XXXXXX | [Notes] |
| Interactive | #XXXXXX | [Notes] |

## Reference Images

[Link to or describe reference images/mood boards]

## Style Presets

For procedural assets, use these style presets:
- Style: [token]
- Palette: [token]
- Materials: [comma-separated list]

## Decision History

- YYYY-MM-DD: [Decision and rationale]
- YYYY-MM-DD: [Decision and rationale]
```

## sound-direction.md (Shared)

```markdown
# Sound Direction

This document captures the audio style decisions for the project.

## Audio Summary

| Aspect | Choice |
|--------|--------|
| Sonic Identity | [Description] |
| Music Style | [Genre/Instrumentation] |
| SFX Character | [Description] |

## Audio Pillars

1. **[Pillar 1]**: [How it manifests in audio]
2. **[Pillar 2]**: [How it manifests in audio]
3. **[Pillar 3]**: [How it manifests in audio]

## Mix Priorities

1. [Highest priority category]
2. [Second priority]
3. [Third priority]
4. [Fourth priority]

## Reference Audio

| Type | Reference | Why |
|------|-----------|-----|
| Music | [Game/Artist] | [What we're drawing from] |
| SFX | [Game/Source] | [What we're drawing from] |
| Overall | [Game/Film] | [What we're drawing from] |

## ZX Audio Budget

| Category | Channels | Notes |
|----------|----------|-------|
| Music | X | [Notes] |
| SFX | X | [Notes] |
| Ambient | X | [Notes] |

## Decision History

- YYYY-MM-DD: [Decision and rationale]
- YYYY-MM-DD: [Decision and rationale]
```

## Quick Setup Script

```bash
#!/bin/bash
# Initialize project memory structure

mkdir -p .studio/architecture

# Create creative direction file
cat > .studio/creative-direction.md << 'EOF'
---
# Creative Direction - Edit this file to configure project direction
art_style: undefined
creative_pillars: []
---

# Project Vision

[Define your experience promise here]

# Direction Notes

<!-- Add dated entries as decisions are made -->
EOF

# Create project status
cat > .studio/project-status.md << 'EOF'
# Project Status

Last updated: $(date +%Y-%m-%d)

## Phase

Current: Setup

## Current Focus

- [ ] Define creative direction
- [ ] Establish architecture

## Notes

Project memory initialized.
EOF

# Create ADR index
cat > .studio/architecture/decisions.md << 'EOF'
# Architecture Decision Records

| # | Title | Status | Date |
|---|-------|--------|------|
EOF

echo "Project memory initialized in .studio/"
```
