---
name: Project Memory
description: This skill should be used when the user asks about "project memory", "persistent context", "guidance files", ".studio files", "session persistence", "direction files", "context between sessions", or discusses maintaining project context across Claude sessions. Provides framework for persistent project guidance.
version: 1.0.0
---

# Project Memory

Maintain project context across sessions through structured files in `.studio/`.

## Why It Matters

Claude sessions are stateless. Without persistent documentation:
- Direction decisions lost
- Style choices must be re-explained
- Architecture patterns forgotten

## Directory Structure

```
project/
├── .studio/
│   ├── creative-direction.md        # Vision and pillars
│   ├── art-direction.md             # Visual style
│   ├── sound-direction.md           # Audio direction
│   ├── tech-direction.md            # Technical constraints
│   ├── visual-style.md              # Detailed visual specs
│   ├── sonic-identity.md            # Audio style specs
│   ├── project-status.md            # Work state
│   ├── architecture/                # ADRs
│   │   ├── decisions.md
│   │   └── 001-*.md
│   ├── characters/                  # Character specs
│   ├── mechanics/                   # Mechanic specs
│   ├── assets/                      # Asset specs
│   ├── animations/                  # Motion descriptions
│   ├── music/                       # Music specs
│   ├── sfx/                         # SFX specs
│   └── analysis/                    # Analysis reports
└── ...
```

All `.studio/` files are committed and shared with the team.

## Creative Direction File Format

```yaml
---
art_style: dark-fantasy-painterly
color_palette: desaturated-warm
sonic_identity: organic-ambient
architecture: ecs-with-rollback
determinism: required
file_size_limit: 300
creative_pillars:
  - atmospheric-dread
  - meaningful-choices
---

# Project Vision
[Experience promise]

# Art Direction Notes
- 2024-01-15: Established dark fantasy palette

# Sound Direction Notes
- 2024-01-16: Organic textures over synthetic

# Tech Direction Notes
- 2024-01-15: Using fixed-point math
```

## Session Workflow

**Start:** Check `.studio/` files, load context
**During:** Ensure consistency with previous decisions, update if new
**End:** Update project-status.md, document new decisions

## File Size Limits

| File | Target | Max |
|------|--------|-----|
| creative-direction.md | 200 | 500 |
| project-status.md | 50 | 100 |
| Individual ADRs | 100 | 200 |

When files grow: archive old decisions, keep recent, link to archives.

## References

- **`references/file-templates.md`** - Copy-paste templates
