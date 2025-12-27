# Refactor A5: Creative Agents Suite

**Status:** `[ ]` Not Started
**Priority:** HIGH
**Action:** Create NEW creative agent suite for asset generation

---

## Problem

Current agents only review/optimize existing assets. No agents for creative generation workflow. Gap 22 defines what should be covered, this refactor is the implementation action.

## Proposed Agents

- Plugin: `nethercore-zx-procgen`
- Agents: 4 new agents

### asset-designer
```yaml
name: asset-designer
description: Interprets creative requirements into SADL specifications
color: blue
parameters:
  mode:
    type: enum
    values: [interactive, autonomous]
    default: interactive
```

**Interactive mode:** Asks clarifying questions, confirms with user
**Autonomous mode:** Makes creative decisions, explains reasoning

### asset-generator
```yaml
name: asset-generator
description: Produces procedural generation code from SADL specs
color: green
```

Generates Rust code from SADL specifications, applies style modifiers.

### asset-critic
```yaml
name: asset-critic
description: Evaluates generated assets and suggests improvements
color: orange
parameters:
  strictness:
    type: enum
    values: [lenient, normal, strict]
    default: normal
```

**Lenient:** Only critical issues
**Normal:** Quality issues
**Strict:** Best practice deviations

### creative-orchestrator
```yaml
name: creative-orchestrator
description: Coordinates the full design → generate → critique pipeline
color: magenta
parameters:
  mode:
    type: enum
    values: [interactive, autonomous]
  max_iterations:
    type: number
    default: 3
```

## Implementation Steps

1. Create agent definitions in procgen plugin
2. Implement asset-designer with mode parameter
3. Implement asset-generator with code templates
4. Implement asset-critic with quality heuristics
5. Implement creative-orchestrator pipeline
6. Test full workflow

## Dependencies

- A4 (SADL Skill) provides the vocabulary these agents use

## Related Gaps

- Gap 22 (AI-First Creative Pipeline) - this is part of Gap 22
