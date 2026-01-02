---
name: Project Status Tracking
description: This skill should be used when the user asks about "project status", "where did we leave off", "what's next", "continue development", "resume project", or when an orchestrator needs to persist or restore project state. Provides the format for tracking game development progress across sessions.
version: 1.0.0
---

# Project Status Tracking

Track progress in `.studio/project-status.md` for session continuity.

## Status File Format

```markdown
# Project Status: [Game Title]

## Current Phase
[Design | Assets | Implementation | Publish] ([X]% complete)

## Summary
[One sentence: current focus]

## Completed
- [x] [Task] → [artifact path]

## In Progress
- [ ] [Task] ([current step])

## Next Steps
1. [Next]
2. [Following]

## Blockers
- [Blocker] | [Resolution]

## Session Log
| Date | Agent | Action | Result |
|------|-------|--------|--------|
```

## Orchestrator Behavior

**Session Start:**
1. Check for `.studio/project-status.md`
2. If exists: summarize state, ask to continue
3. If new: create initial status

**During Work:** Update after completing tasks or hitting blockers.

**Before Stopping:** Update In Progress, Next Steps, add to Session Log.

## Phase Definitions

| Phase | % | Activities |
|-------|---|------------|
| Creative Foundation | 0-10 | Vision, sonic identity |
| Design | 10-25 | GDD, constraints, asset specs |
| Visual Assets | 25-45 | Textures, meshes, characters |
| Audio Assets | 45-55 | Music, SFX |
| Implementation | 55-80 | Code, integration |
| Testing | 80-90 | Sync tests, optimization |
| Publish | 90-100 | Marketing, ROM, upload |

## Quality Checkpoints

| After | Agents |
|-------|--------|
| Creative | creative-director |
| Design | design-reviewer, accessibility-auditor |
| Visual | art-director, asset-quality-reviewer |
| Audio | sound-director |
| Code | tech-director, rollback-reviewer |
| Pre-Publish | release-validator |
