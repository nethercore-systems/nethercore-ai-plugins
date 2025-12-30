# Sound Design Plugin

Platform-agnostic game audio design plugin for Claude Code. The audio equivalent of what the visual style guide does for assets - translates creative intent into concrete specifications.

## Overview

This plugin provides the **audio style guide** framework for game audio design, covering:

- **Sonic Styles** - Overall audio aesthetic (Orchestral, Chiptune, Industrial, etc.)
- **Mood Palettes** - Emotional character (Tense, Triumphant, Mysterious, etc.)
- **Instrument Palettes** - Sound source categories
- **Synthesis Techniques** - FM, wavetable, granular, and more
- **Composition Patterns** - Music structure, chord progressions, adaptive music
- **SFX Design** - Layering, archetypes, and implementation

## Components

### Skills (5)

| Skill | Description |
|-------|-------------|
| `sonic-style-language` | audio style specification - styles, moods, instruments, processing signatures |
| `synthesis-techniques` | FM, wavetable, granular, physical modeling, Karplus-Strong |
| `music-composition` | Theory, chord progressions, structure, adaptive music, leitmotifs |
| `sfx-design` | Layering, archetypes, impact design, UI audio, variation |
| `audio-integration` | Mix architecture, priorities, spatial audio, ducking, states |

### Commands (3)

| Command | Description |
|---------|-------------|
| `/establish-sonic-identity` | Interactive wizard to create audio style specification for a game |
| `/design-soundtrack` | Design music tracks with structure and chord progressions |
| `/design-sfx` | Design sound effects with layering and synthesis specs |

### Agents (4)

| Agent | Trigger | Description |
|-------|---------|-------------|
| `sonic-designer` | Creative audio intent | Translates descriptions to audio style specs |
| `sfx-architect` | SFX creation | Designs effects with layers and synthesis code |
| `music-architect` | Music composition | Designs tracks with harmony and structure |
| `audio-coherence-reviewer` | Audio review | Validates consistency with sonic identity |

## Quick Start

### 1. Establish Sonic Identity

Run the wizard to create your game's audio direction:

```
/establish-sonic-identity "dark fantasy RPG"
```

This creates `.studio/sonic-identity.md` with:
- Sonic style (Orchestral + Dark Ambient)
- Mood palette (Mysterious, Tense, Triumphant, etc.)
- Instrument recommendations
- Processing signatures
- Mix priorities

### 2. Design Music

Create track specifications:

```
/design-soundtrack "boss battle"
```

Produces `.studio/music/boss-battle.spec.md` with:
- Tempo, key, time signature
- Chord progressions per section
- Structure diagram
- Instrumentation
- Loop point design
- Adaptive layers (if applicable)

### 3. Design SFX

Create sound effect specifications:

```
/design-sfx "sword impact"
```

Produces `.studio/sfx/sword-impact.spec.md` with:
- Layer breakdown
- Synthesis parameters
- Variation strategy
- Implementation code

### 4. Review Coherence

Validate all audio works together:

```
Ask: "Review my audio for consistency"
→ Triggers audio-coherence-reviewer agent
```

## audio style guide

The audio style guide provides semantic descriptors for audio, similar to how the visual style guide works for visual assets.

### Example Audio Style Specification

```yaml
game: "Dark Fantasy RPG"

style:
  primary: Orchestral
  secondary: Dark Ambient

mood_palette:
  exploration: Mysterious + Melancholic
  combat: Aggressive + Epic
  story: Tense + Triumphant

instruments:
  primary:
    - orchestral.strings.epic
    - orchestral.brass.dark
  accent:
    - orchestral.percussion.timpani
  texture:
    - synth.pad.evolving

processing:
  reverb: reverb.hall
  character: warm, cinematic

mix_priorities:
  1: player_feedback
  2: dialogue
  3: combat_sfx
  4: music
  5: ambient
```

### Genre Mappings

| Genre | Primary Style | Secondary | Mood Tendency |
|-------|---------------|-----------|---------------|
| Fantasy RPG | Orchestral | Ambient | Epic, Mysterious |
| Sci-Fi Shooter | Electronic | Hybrid | Aggressive, Tense |
| Horror | Dark Ambient | Industrial | Eerie, Tense |
| Platformer | Chiptune | Acoustic | Playful, Triumphant |
| Racing | Electronic | Synthwave | Aggressive, Frantic |
| Puzzle | Ambient | Lo-Fi | Peaceful, Mysterious |

## Synthesis Techniques Reference

| Technique | Best For | Complexity |
|-----------|----------|------------|
| Subtractive | Warm analog sounds | Low |
| FM | Bells, metallic, digital | Medium |
| Wavetable | Evolving textures | Medium |
| Granular | Time-stretch, textures | High |
| Karplus-Strong | Plucked strings | Low |
| Additive | Precise harmonics | High |

## Integration with Other Plugins

### With game-design plugin
- Read GDDs to auto-suggest sonic direction
- Align music moods with gameplay contexts

### With zx-procgen
- audio style specs feed into `procedural-sounds` skill
- Music specs guide `procedural-music` skill

### With creative-direction plugin
- Complements `sound-director` agent
- Provides design specs, creative-direction provides review

## Files Created

The plugin creates specs in `.studio/`:

```
.studio/
├── sonic-identity.md      # From /establish-sonic-identity
├── music/
│   ├── main-theme.spec.md
│   ├── boss-battle.spec.md
│   └── ...
└── sfx/
    ├── sword-impact.spec.md
    ├── jump.spec.md
    └── ...
```

## Installation

Add to your `.claude/settings.local.json`:

```json
{
  "enabledPlugins": {
    "sound-design@nethercore-ai-plugins": true
  }
}
```

## License

Licensed under MIT or Apache-2.0, at your option.
