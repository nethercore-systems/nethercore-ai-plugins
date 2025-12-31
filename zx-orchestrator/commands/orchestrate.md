---
description: Launch the game development orchestrator for full pipeline coordination
argument-hint: "[action] - start, continue, status, or phase name"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "Task", "AskUserQuestion", "Skill"]
---

# Game Development Orchestrator

Launch the game-orchestrator agent to coordinate the full Nethercore ZX game development pipeline.

## Actions

Parse the argument to determine what action to take:

| Argument | Action |
|----------|--------|
| (none) | Check for existing project and ask user what to do |
| `start` | Begin a new game project from scratch |
| `continue` | Resume existing project from last checkpoint |
| `status` | Show current project status and progress |
| `vision` | Jump to Phase 0: Creative Foundation |
| `design` | Jump to Phase 1: Design |
| `visual` or `assets` | Jump to Phase 2: Visual Assets |
| `audio` | Jump to Phase 3: Audio Assets |
| `implement` or `code` | Jump to Phase 4: Implementation |
| `test` or `optimize` | Jump to Phase 5: Testing & Optimization |
| `publish` | Jump to Phase 6: Publish |
| `review` | Run quality review checkpoints for current phase |

## Process

1. **Check for existing project state:**
   - Look for `.studio/project-status.md`
   - Look for `docs/design/game-design.md` (GDD)
   - Look for `nether.toml` (project manifest)

2. **Based on argument and state, invoke game-orchestrator agent:**

   Use Task tool with these parameters:
   ```
   subagent_type: "zx-orchestrator:game-orchestrator"
   description: "[Action]: [brief description]"
   prompt: |
     Action: [action from arguments]
     Current State:
     - GDD exists: [yes/no]
     - Project manifest: [yes/no]
     - Current phase: [phase name or "none"]
     - Last checkpoint: [date/time or "none"]

     [Include any relevant context from project-status.md]

     Please [action-specific instruction].
   ```

3. **For `status` action:**
   - Read `.studio/project-status.md` if exists
   - Summarize current phase, progress, and next steps
   - Show quality checkpoint status

4. **For `review` action:**
   - Determine current phase from project state
   - Invoke appropriate review agents:
     - After Creative: creative-director
     - After Design: design-reviewer, accessibility-auditor
     - After Visual: art-director, asset-quality-reviewer
     - After Audio: sound-director
     - After Implementation: tech-director, rollback-reviewer
     - Before Publish: release-validator, creative-director

## Examples

```bash
# Start fresh
/orchestrate start

# Continue where you left off
/orchestrate continue

# Check status
/orchestrate status

# Jump to specific phase
/orchestrate design
/orchestrate audio
/orchestrate publish

# Run quality review
/orchestrate review
```

## Output

When orchestrating, always show:
1. Current phase and progress percentage
2. Quality checkpoint status
3. What's being worked on
4. Next steps

---

**Remember:** The orchestrator is HUMAN-DRIVEN. Always ask for user input on creative and design decisions. Never assume - always confirm with the user before major phase transitions.
