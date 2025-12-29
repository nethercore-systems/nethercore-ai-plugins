---
description: Resume development from where you left off - check pending tasks and get next-step recommendations
allowed-tools:
  - Read
  - Glob
  - Task
  - AskUserQuestion
argument-hint: "[--quick|--full|--auto]"
---

# Continue Development

Resume your development session by checking pending work and recommending next steps.

## Arguments

| Argument | Behavior |
|----------|----------|
| (none) | Show status, recommend next step, ask before dispatching |
| `--quick` | Just display status files, no analysis or dispatch |
| `--full` | Run comprehensive project-health-monitor |
| `--auto` | Auto-dispatch first pending task without confirmation |

## Process

### 1. Check State Files

Read these files if they exist:

```bash
# Check for state files
ls .studio/dispatch-queue.md .studio/project-status.md 2>/dev/null
```

**Dispatch Queue** (`.studio/dispatch-queue.md`):
- Show pending tasks with priority order
- Identify first actionable task

**Project Status** (`.studio/project-status.md`):
- Show current phase and completion percentage
- Show last completed task
- Show any blockers

### 2. Display Status

Always show current state first:

```
**Session Status**

Dispatch Queue: [X] pending tasks
1. [First task] → [agent]
2. [Second task] → [agent]

Project Status: [Phase] ([X]% complete)
Last: [last completed task]
Blockers: [any blockers, or "None"]
```

If no state files exist:
```
**Session Status**

No dispatch queue found.
No project status found.

This appears to be a fresh session or new project.
```

### 3. Determine Action

Based on mode:

| Mode | Action |
|------|--------|
| `--quick` | Stop after displaying status |
| `--full` | Invoke `ai-game-studio:project-health-monitor` for comprehensive assessment |
| Default | Continue to recommendation step |
| `--auto` | Continue to recommendation, then auto-dispatch |

### 4. Recommendation (Default and --auto modes)

If dispatch-queue has pending tasks:
- Recommend the first pending task
- Show the agent to use

Otherwise:
- Invoke `ai-game-studio:next-step-suggester` agent for analysis
- Let it scan for incomplete work and recommend

### 5. Dispatch

**Default mode:** Ask for confirmation
```
Continue with this? (yes/no/other)
```

**--auto mode:** Dispatch immediately without asking

On confirmation (or --auto):
- Invoke the appropriate agent via Task tool
- Pass full context from status files

## Output Format

### With Pending Tasks
```
**Session Status**

Dispatch Queue: 2 pending tasks
1. Generate barrel textures → zx-procgen:asset-generator
2. Implement collision detection → zx-dev:feature-implementer

Project Status: Implementation Phase (45% complete)
Last: Player movement system
Blockers: None

**Recommended Next Step:**
→ Generate barrel textures
  Agent: zx-procgen:asset-generator
  Context: Barrel mesh exists, needs textures for rendering

Continue with this? (yes/no/other)
```

### Fresh Session
```
**Session Status**

No dispatch queue found.
No project status found.

Analyzing project state...

[next-step-suggester output]
```

## Examples

```
ai-game-studio:continue
→ Shows status, recommends first pending task, asks "Continue with this?"

ai-game-studio:continue --quick
→ Just shows dispatch-queue and project-status, no further action

ai-game-studio:continue --full
→ Runs project-health-monitor for comprehensive 6-dimension analysis

ai-game-studio:continue --auto
→ Shows status, then immediately dispatches first pending task
```

## Relationship to Other Components

```
ai-game-studio:continue
    ↓
Check .studio/dispatch-queue.md + .studio/project-status.md
    ↓
--quick: Display and stop
--full: project-health-monitor (comprehensive)
default: Recommend + ask → dispatch on confirm
--auto: Recommend → auto-dispatch
    ↓
Appropriate specialist agent
```

## When to Use Each Mode

| Situation | Recommended Mode |
|-----------|------------------|
| Starting a new session | `ai-game-studio:continue` (default) |
| Quick status check | `ai-game-studio:continue --quick` |
| Lost track of project state | `ai-game-studio:continue --full` |
| Hands-off automation | `ai-game-studio:continue --auto` |
| Just want to see pending work | `ai-game-studio:continue --quick` |
