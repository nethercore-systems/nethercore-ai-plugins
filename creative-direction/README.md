# Creative Direction Plugin

Ensures coherence and quality across all game development disciplines through specialized director agents and vision skills.

## Philosophy

Directors are different from reviewers:
- **Reviewers** check compliance with specifications
- **Directors** ensure qualitative coherence and guard the vision

This plugin provides four specialized directors, each with their own vision skill and continuous monitoring.

## Components

### Directors (Agents)

| Director | Domain | Purpose |
|----------|--------|---------|
| Art Director | Visual | Ensures visual coherence across all assets |
| Sound Director | Audio | Ensures sonic identity and mix coherence |
| Tech Director | Code | Ensures architectural quality and patterns |
| Creative Director | Overall | Guards the vision, coordinates other directors |

### Vision Skills

| Skill | Purpose |
|-------|---------|
| `art-vision` | Visual style bible, color theory, composition |
| `sound-vision` | Audio style guide, sonic identity, mixing |
| `tech-vision` | Architecture patterns, code quality standards |
| `creative-vision` | Overall game vision, creative pillars |

### Commands

| Command | Purpose |
|---------|---------|
| `creative-direction:establish-vision` | Interactive wizard to establish project vision |

Depending on your Claude/Codex client, commands may also appear as slash commands (e.g. `/establish-vision`).

## Usage

### Establishing Vision (Start of Project)

```
User: I'm starting a new game with a dark fantasy aesthetic
Claude: [Loads art-vision skill, helps define style bible]
Claude: [Creates .studio/creative-direction.md with vision decisions]
```

### Continuous Monitoring

As you work, directors automatically monitor:
- Visual assets for style consistency
- Audio for mix and identity coherence
- Code for architectural patterns

### Periodic Reviews

Request comprehensive reviews at milestones:
```
User: Review the art direction for all character assets
Claude: [Art director agent performs holistic review]
```

### Creative Drift Check

```
User: Has the game drifted from the original vision?
Claude: [Creative director compares implementation to vision]
```

## Vision Storage

Vision decisions persist in `.studio/creative-direction.md`:

```yaml
---
art_style: dark-fantasy-painterly
color_palette: desaturated-warm
architecture: ecs-with-rollback
creative_pillars:
  - atmospheric-dread
  - meaningful-choices
  - emergent-narrative
---
```

## Integration with Other Plugins

- **zx-procgen**: Art director validates generated assets against visual style tokens
- **zx-dev**: Tech director extends rollback-reviewer with broader architectural review
- **game-design**: Creative director validates implementation against GDD

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "creative-direction@nethercore-ai-plugins": true
  }
}
```
