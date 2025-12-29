---
description: This skill documents the dispatch queue pattern for tracking pending tasks across sessions. Use when managing task continuity, understanding what work is pending, or implementing the /continue workflow.
---

# Dispatch Queue Pattern

The dispatch queue (`.studio/dispatch-queue.md`) tracks pending tasks that should be completed but haven't been started yet. It enables session continuity and prevents work from being forgotten.

## File Location

```
.studio/
├── dispatch-queue.md      # Pending tasks
├── project-status.md      # Overall project state
└── creative-direction.local.md  # Project memory
```

## File Format

```markdown
# Dispatch Queue

## Pending Tasks (Priority Order)

### 1. [Task Name]
- **Agent:** [fully-qualified agent name]
- **Context:** [what needs to be done and why]
- **Blocked by:** [dependencies, or "None"]
- **Added:** [session/date when queued]

### 2. [Next Task]
- **Agent:** [agent name]
- **Context:** [context]
- **Blocked by:** [dependencies]
- **Added:** [when]

## Completed This Session
- [x] [Task description] → [result/artifact path]
- [x] [Another task] → [result]

## Notes
[Any context for next session]
```

## Example Dispatch Queue

```markdown
# Dispatch Queue

## Pending Tasks (Priority Order)

### 1. Generate barrel textures
- **Agent:** zx-procgen:asset-generator
- **Context:** Barrel mesh exists at assets/meshes/barrel.glb, needs albedo and MRE textures
- **Blocked by:** None
- **Added:** After mesh generation

### 2. Implement collision detection
- **Agent:** zx-dev:feature-implementer
- **Context:** Player can walk through walls, need AABB collision with track boundaries
- **Blocked by:** None (can parallelize with #1)
- **Added:** During feature planning

### 3. Add jump sound effect
- **Agent:** zx-procgen:sfx-architect
- **Context:** Player jump has no audio feedback, need satisfying "whoosh" sound
- **Blocked by:** None
- **Added:** Polish pass review

## Completed This Session
- [x] Generate barrel mesh → assets/meshes/barrel.glb
- [x] Implement player movement → src/player.rs

## Notes
Barrel textures are highest priority - without them the barrel won't render properly.
Collision can be done in parallel if time permits.
```

## When to Update

### Add Tasks
- After identifying work during feature implementation
- When completion-auditor finds gaps
- When project-health-monitor identifies missing features
- When user requests something that can't be done immediately
- When SubagentStop hook identifies follow-up work

### Remove/Complete Tasks
- When task is dispatched and completed successfully
- When task becomes irrelevant (design changed)
- When task is blocked indefinitely

### Session Boundaries
- **Session Start:** Read queue, offer to continue first task
- **Session End:** Update queue with any pending work identified

## Priority Ordering

Tasks should be ordered by:

1. **Blockers first** - Tasks that block other work
2. **Critical path** - Tasks required for playable game
3. **Quick wins** - Fast tasks that unblock progress
4. **Polish** - Nice-to-have improvements

## Integration with ai-game-studio:continue

The `ai-game-studio:continue` command reads the dispatch queue:

```
ai-game-studio:continue          → Shows queue, recommends #1, asks to dispatch
ai-game-studio:continue --quick  → Just shows queue contents
ai-game-studio:continue --auto   → Auto-dispatches #1 without asking
```

## Integration with Agents

### next-step-suggester
Checks dispatch-queue first:
```
1. Read .studio/dispatch-queue.md
2. If tasks pending → recommend first one
3. Otherwise → scan for incomplete work
```

### request-dispatcher
Updates dispatch-queue before stopping:
```
Before STOPPING:
1. Update .studio/dispatch-queue.md with any pending tasks
```

### completion-auditor
May add tasks when finding gaps:
```
If gap found:
1. Add remediation task to dispatch-queue
2. Mark priority based on severity
```

## Task Format Details

### Agent Field
Use fully-qualified agent names:
- `zx-procgen:asset-generator`
- `zx-dev:feature-implementer`
- `ai-game-studio:completion-auditor`

### Context Field
Include enough information to resume:
- What exists already
- What needs to be created/fixed
- Any relevant file paths
- Design decisions already made

### Blocked By Field
Options:
- `None` - Ready to start
- `#2` - Blocked by another task in queue
- `[specific dependency]` - External blocker
- `User decision needed` - Requires clarification

## Automation Patterns

### Auto-Queue from Hooks
SubagentStop hooks can suggest adding to queue:
```
After asset-generator completes:
"Consider adding integration task to dispatch queue"
```

### Auto-Complete from Dispatch
When `ai-game-studio:continue --auto` dispatches a task:
1. Task moves from "Pending" to being worked
2. On completion, move to "Completed This Session"
3. Remove from pending list

## Empty Queue

When dispatch queue is empty or doesn't exist:
```markdown
# Dispatch Queue

## Pending Tasks (Priority Order)

No pending tasks.

## Completed This Session
(none yet)

## Notes
Run project-health-monitor to identify potential work.
```

## Queue Cleanup

Periodically clean the queue:
- Remove completed tasks older than 1 session
- Archive "Completed This Session" to project-status.md
- Remove tasks that are no longer relevant
