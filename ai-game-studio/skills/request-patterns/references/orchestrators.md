# Orchestrator Selection

Four orchestrators at different abstraction levels:

| Orchestrator | Plugin | Scope | Use When |
|--------------|--------|-------|----------|
| game-orchestrator | zx-orchestrator | Full pipeline | Building complete game from GDD to ROM |
| creative-orchestrator | zx-procgen | Asset generation | Generating assets for existing project |
| request-dispatcher | ai-game-studio | Single request | Have a vague or complex request |
| parallel-coordinator | zx-orchestrator | Parallelization | 4+ independent tasks |

## Decision Flow

```
What do you need?
├── "Build a complete game" ────────→ game-orchestrator
├── "Generate all assets for my GDD" → creative-orchestrator
├── "I have a complex request" ─────→ request-dispatcher
└── "Run these tasks in parallel" ──→ parallel-coordinator
```

## When to Use Each

**game-orchestrator:**
- Starting a new game from scratch
- Human-driven development with checkpoints
- 7-phase pipeline (Creative → Design → Visual → Audio → Code → Test → Publish)

**creative-orchestrator:**
- Have GDD/asset specs, need assets generated
- Style-based asset pipeline
- Autonomous asset generation workflow

**request-dispatcher:**
- Single, possibly vague request
- Don't know which agent to use
- Request spans multiple domains

**parallel-coordinator:**
- Have 4+ independent tasks
- Need dependency analysis
- Maximize parallel execution

## Examples

| Request | Route To |
|---------|----------|
| "Make a fighting game" | game-orchestrator |
| "Generate all characters from GDD" | creative-orchestrator |
| "Improve my game" | request-dispatcher |
| "Generate textures, meshes, and sounds" | parallel-coordinator |

## Nesting

Orchestrators can invoke each other:
- game-orchestrator → creative-orchestrator (asset phase)
- request-dispatcher → parallel-coordinator (multi-domain)
- creative-orchestrator → parallel-coordinator (concurrent assets)
