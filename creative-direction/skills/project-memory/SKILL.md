---
name: Project Memory
description: This skill should be used when the user asks about "project memory", "persistent context", "guidance files", ".claude files", "session persistence", "direction files", "context between sessions", "architecture notes", "project documentation", or discusses maintaining project context and direction across Claude sessions. Provides framework for persistent project guidance through structured documentation files.
version: 1.0.0
---

# Project Memory

Maintain project context and direction across Claude sessions through structured documentation in `.studio/` directory.

## Core Principles

### Why Project Memory Matters

Claude sessions are stateless—each new session starts fresh. Without persistent documentation:
- Direction decisions are lost
- Style choices must be re-explained
- Architecture patterns are forgotten
- Previous context is unavailable

Project memory solves this through structured files that Claude reads at session start.

### The .studio/ Directory

```
project/
├── .studio/
│   ├── creative-direction.local.md  # Vision and direction
│   ├── architecture/                # Technical decisions
│   │   ├── decisions.md             # ADR index
│   │   └── 001-*.md                 # Individual ADRs
│   ├── art-direction.md             # Style bible reference
│   ├── sound-direction.md           # Audio style reference
│   └── project-status.md            # Current work state
├── .gitignore                        # Add .studio/*.local.md
└── ...
```

### File Types

**Local Files** (`.local.md`): Not committed, personal context
- `.studio/creative-direction.local.md`
- Contains session-specific notes
- Ignored by git

**Shared Files**: Committed, team context
- `.studio/architecture/*.md`
- `.studio/art-direction.md`
- Visible to all contributors

## Creative Direction File

### Structure

```markdown
---
# Creative Direction Configuration
# Read by creative-direction plugin at session start

art_style: dark-fantasy-painterly
color_palette: desaturated-warm
style_spectrums:
  fidelity: 4
  saturation: 3
  contrast: 4

sonic_identity: organic-ambient
mix_priority: gameplay-first

architecture: ecs-with-rollback
determinism: required
file_size_limit: 300

creative_pillars:
  - atmospheric-dread
  - meaningful-choices
  - emergent-narrative

target_audience: indie-horror-fans
avoid_patterns:
  - jump-scares
  - excessive-gore
---

# Project Vision

[Experience promise goes here - one paragraph]

# Art Direction Notes

[Accumulated decisions about visual style]
- 2024-01-15: Established dark fantasy palette
- 2024-01-20: Decided against cel-shading

# Sound Direction Notes

[Accumulated decisions about audio]
- 2024-01-16: Organic textures over synthetic
- 2024-01-22: Silence as design tool

# Tech Direction Notes

[Accumulated decisions about architecture]
- 2024-01-15: Using fixed-point math
- 2024-01-18: ECS pattern for entities

# Current Focus

[What's being worked on right now]
- Implementing player movement
- Next: Enemy AI behaviors
```

### Updating the File

Append decisions chronologically:

```markdown
# Art Direction Notes

- 2024-01-15: Established dark fantasy palette
- 2024-01-20: Decided against cel-shading
+ - 2024-01-25: Character silhouettes must read at 32px height
```

## Architecture Documentation

### ADR Index

Maintain `decisions.md` as an index:

```markdown
# Architecture Decision Records

| # | Title | Status | Date |
|---|-------|--------|------|
| 1 | Use Fixed-Point Math | Accepted | 2024-01-15 |
| 2 | ECS Architecture | Accepted | 2024-01-16 |
| 3 | Asset Streaming | Proposed | 2024-01-20 |
```

### Individual ADRs

Each decision in its own file:

```
.studio/architecture/
├── decisions.md
├── 001-fixed-point-math.md
├── 002-ecs-architecture.md
└── 003-asset-streaming.md
```

## Project Status File

### Structure

Track current work state:

```markdown
# Project Status

Last updated: 2024-01-25 14:30

## Current Sprint/Phase

Phase: Prototype
Focus: Core movement and combat

## In Progress

- [ ] Player movement system
  - [x] Basic movement
  - [ ] Jump mechanics
  - [ ] Dash ability
- [ ] Enemy AI
  - [ ] Patrol behavior
  - [ ] Chase behavior

## Recent Decisions

- 2024-01-25: Changed jump to variable height
- 2024-01-24: Added dash with cooldown

## Blockers

- None currently

## Next Up

- Collision system
- Level loading
```

### When to Update

Update project-status.md:
- At start of work session (what to resume)
- When completing significant work
- When making important decisions
- When hitting blockers

## Reading Project Memory

### Session Start

At session start, Claude should:
1. Check for `.studio/creative-direction.local.md`
2. Read project status if exists
3. Note relevant architecture decisions
4. Load direction context into session

### During Work

When making decisions:
1. Check existing decisions in memory files
2. Ensure consistency with previous choices
3. Update memory if new decisions made

### Session End

Before ending significant work:
1. Update project-status.md
2. Document any new decisions
3. Note pending work for next session

## File Size Management

### Large File Prevention

Memory files should stay manageable:

| File | Target | Max |
|------|--------|-----|
| creative-direction.local.md | 200 lines | 500 lines |
| project-status.md | 50 lines | 100 lines |
| Individual ADRs | 100 lines | 200 lines |
| Style guides | 300 lines | 500 lines |

### When Files Grow

If a file exceeds limits:
1. Archive old decisions to separate file
2. Keep only recent/relevant in main file
3. Link to archives

```markdown
# Art Direction Notes

For decisions before 2024-01-01, see [art-direction-archive.md]

- 2024-01-15: ...
```

## Best Practices

### Do

- Update memory files when making decisions
- Keep files focused and current
- Use consistent formatting
- Include dates on all entries
- Link between related documents

### Don't

- Duplicate information across files
- Include implementation details (code belongs in code)
- Let files grow unbounded
- Forget to update status at session end
- Include sensitive information

### Git Integration

Add to `.gitignore`:
```
.studio/*.local.md
```

Commit shared files:
```
.studio/architecture/
.studio/art-direction.md
.studio/sound-direction.md
```

## Quick Reference

### File Checklist

For a well-documented project:
- [ ] `.studio/creative-direction.local.md` - Vision and pillars
- [ ] `.studio/project-status.md` - Current work state
- [ ] `.studio/architecture/decisions.md` - ADR index
- [ ] Individual ADRs for significant decisions
- [ ] `.gitignore` includes `.studio/*.local.md`

### Template Starter

Create minimal memory with:

```bash
mkdir -p .studio/architecture
touch .studio/creative-direction.local.md
touch .studio/project-status.md
touch .studio/architecture/decisions.md
echo ".studio/*.local.md" >> .gitignore
```

## Additional Resources

### Reference Files

For templates and examples:
- **`references/file-templates.md`** - Copy-paste templates for all file types
