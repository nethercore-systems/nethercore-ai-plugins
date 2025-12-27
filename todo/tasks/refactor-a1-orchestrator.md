# Refactor A1: Orchestrator Plugin

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Action:** Move game-orchestrator from game-design to NEW dedicated plugin

---

## Problem

The game-orchestrator agent currently lives in nethercore-zx-game-design, but it has broader responsibilities that span multiple plugins. It should be its own dedicated plugin.

## Current Location

- Plugin: `nethercore-zx-game-design`
- Agent: `game-orchestrator`

## Proposed Change

Move to: NEW plugin `nethercore-zx-orchestrator`

This gives the orchestrator:
- Independence from game-design skills
- Ability to coordinate across all ZX plugins
- Cleaner separation of concerns

## Implementation Steps

1. Create new plugin `nethercore-zx-orchestrator`
2. Move game-orchestrator agent definition
3. Update any cross-references
4. Update INDEX.md in game-design plugin
5. Test orchestrator still works

## Dependencies

- Should be done after core functionality is stable (Phase 6)

## Related Gaps

- None directly, but orchestrator coordinates work across all plugins
