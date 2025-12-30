---
name: Project Status Tracking
description: This skill should be used when the user asks about "project status", "where did we leave off", "what's next", "continue development", "resume project", "track progress", "development status", "project phases", "current phase", or when an orchestrator needs to persist or restore project state. Provides the standardized format for tracking game development progress across sessions.
version: 1.0.0
---

# Project Status Tracking

## Overview

Project status is tracked in `.studio/project-status.md` to maintain continuity across sessions. Orchestrators MUST read this file at session start and update it after each major task.

## Status File Location

```
my-game/
├── .studio/
│   └── project-status.md    ← Status file
├── docs/
├── src/
└── assets/
```

## Status File Format

```markdown
# Project Status: [Game Title]

## Current Phase
[Design | Assets | Implementation | Publish] ([X]% complete)

## Summary
[One sentence: what's currently being worked on]

## Completed
- [x] [Task description] → [artifact path or result]
- [x] [Task description] → [artifact path or result]

## In Progress
- [ ] [Task being worked on] ([current step])

## Next Steps
1. [Immediate next task]
2. [Following task]
3. [After that]

## Blockers
- [Blocker description] | [Suggested resolution]

## Artifacts
| Artifact | Path | Status |
|----------|------|--------|
| GDD | docs/design/game-design.md | Complete |
| Asset Specs | docs/design/asset-specs.md | In Progress |
| Player Mesh | assets/characters/player.gltf | Pending |

## Session Log
| Date | Agent | Action | Result |
|------|-------|--------|--------|
| 2024-01-15 | game-orchestrator | Created GDD | Complete |
| 2024-01-15 | asset-designer | Designed player | 3 style specs |
```

---

## Orchestrator Behavior

### At Session Start

1. Check for `.studio/project-status.md`
2. If exists, read and report current state
3. Ask user if they want to continue from last position
4. If new project, create initial status file

### During Development

Update status after:
- Completing any phase
- Creating any artifact (GDD, mesh, texture, etc.)
- Encountering a blocker
- Making significant progress

### Before Stopping

1. Update "In Progress" with current task
2. Update "Next Steps" with remaining work
3. Log the session in "Session Log"

---

## Example Status Updates

### After Creating GDD

```markdown
## Completed
- [x] Game Design Document → docs/design/game-design.md

## In Progress
- [ ] Asset Specifications (awaiting user input on art style)

## Next Steps
1. Complete asset specifications
2. Generate player character mesh
3. Scaffold project structure
```

### After Generating Assets

```markdown
## Completed
- [x] Game Design Document → docs/design/game-design.md
- [x] Asset Specifications → docs/design/asset-specs.md
- [x] Player mesh → assets/characters/player.gltf
- [x] Player textures → assets/characters/player_*.png

## In Progress
- [ ] Enemy mesh (skeleton defined, generating geometry)

## Next Steps
1. Complete enemy mesh and rig
2. Generate walk/attack animations
3. Scaffold game project
```

---

## Phase Definitions

| Phase | % Range | Key Activities |
|-------|---------|----------------|
| **Creative Foundation** | 0-10% | Vision pillars, sonic identity, creative direction |
| **Design** | 10-25% | World building, characters, GDD, constraints, asset specs |
| **Visual Assets** | 25-45% | Textures, meshes, characters, animations |
| **Audio Assets** | 45-55% | Music tracks, sound effects, audio review |
| **Implementation** | 55-80% | Scaffolding, systems, features, asset integration |
| **Testing & Optimization** | 80-90% | Sync tests, build analysis, optimization |
| **Publish** | 90-100% | Marketing assets, ROM packaging, platform upload |

## Quality Review Checkpoints

| Checkpoint | After Phase | Agents |
|------------|-------------|--------|
| Vision Check | Creative Foundation | creative-director |
| Design Review | Design | design-reviewer, accessibility-auditor |
| Art Review | Visual Assets | art-director, asset-quality-reviewer |
| Audio Review | Audio Assets | sound-director |
| Tech Review | Implementation | tech-director, rollback-reviewer |
| Release Review | Pre-Publish | release-validator, creative-director |

---

## Status File Commands

### Create/Update Status

```bash
# Orchestrator creates/updates via Write tool
# File: .studio/project-status.md
```

### Quick Status Check

Orchestrators should provide a quick status summary when asked:

```
Project: [Game Title]
Phase: Assets (45%)
Last: Generated player mesh
Next: Generate enemy mesh, then animations
Blockers: None
```

---

## Reference Files

- `references/plugin-reference.md` - Complete list of all plugins, commands, skills, and agents

---

## Integration with Orchestrators

Orchestrators should include in their system prompts:

```
## Session Continuity

**At Session Start:**
1. Check for .studio/project-status.md
2. If exists, read and summarize current state
3. Ask: "Would you like to continue from [last task]?"

**Before Stopping:**
1. Update .studio/project-status.md with current state
2. Ensure "In Progress" reflects current work
3. Log this session
```
