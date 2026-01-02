# Nethercore Audio Pipeline

End-to-end audio workflow spanning three plugins, each handling a distinct phase.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       sound-design                               │
│                  DESIGN - "What and Why"                         │
│                                                                  │
│  Commands: /establish-sonic-identity, /design-sfx, /design-soundtrack
│  Agents:   sfx-architect, music-architect, sonic-designer       │
│  Outputs:  .studio/sonic-identity.md, .studio/sfx/*.spec.md,    │
│            .studio/music/*.spec.md                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        zx-procgen                                │
│                   SYNTHESIS - "How to Make"                      │
│                                                                  │
│  Commands: /generate-sfx, /generate-instrument                   │
│  Agents:   instrument-architect                                  │
│  Outputs:  Python synthesis scripts, .wav files                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       tracker-music                              │
│                 COMPOSITION - "Arrange It"                       │
│                                                                  │
│  Commands: /generate-song                                        │
│  Agents:   song-generator                                        │
│  Outputs:  .xm or .it tracker files                             │
└─────────────────────────────────────────────────────────────────┘
```

## Plugin Responsibilities

| Plugin | Role | What It Does | What It Outputs |
|--------|------|--------------|-----------------|
| **sound-design** | DESIGN | Defines audio style, SFX layer patterns, music theory | `.studio/*.spec.md` specification files |
| **zx-procgen** | SYNTHESIS | Generates actual audio using NumPy/SciPy | Python scripts, `.wav` files |
| **tracker-music** | COMPOSITION | Arranges music into tracker modules | `.xm` or `.it` files |

## When to Use Each Plugin

| You want to... | Use This |
|----------------|----------|
| Define your game's overall audio aesthetic | `sound-design:/establish-sonic-identity` |
| Plan what a sound effect should be | `sound-design:/design-sfx` or `sfx-architect` |
| Plan what a music track should be | `sound-design:/design-soundtrack` or `music-architect` |
| Generate actual .wav SFX files | `zx-procgen:/generate-sfx` |
| Generate instrument samples | `zx-procgen:/generate-instrument` or `instrument-architect` |
| Create complete tracker music files | `tracker-music:/generate-song` or `song-generator` |

## Agent Clarification

**"Architect" agents** create specifications and design documents:
- `sfx-architect` (sound-design) - Outputs `.studio/sfx/*.spec.md` with layer breakdown
- `music-architect` (sound-design) - Outputs `.studio/music/*.spec.md` with harmony/structure
- `instrument-architect` (zx-procgen) - Outputs Python synthesis code for specific instruments

**"Generator" agents** create runnable output:
- `song-generator` (tracker-music) - Outputs complete `.xm` or `.it` tracker files

## Recommended Workflows

### Workflow 1: Complete SFX Creation

1. **Establish Style** (once per project)
   ```
   /establish-sonic-identity "dark fantasy RPG"
   → Creates .studio/sonic-identity.md
   ```

2. **Design SFX** (design layer)
   ```
   /design-sfx "sword impact"
   → Creates .studio/sfx/sword-impact.spec.md
   → Contains layers, frequencies, synthesis approach
   ```

3. **Generate Code** (synthesis layer)
   ```
   /generate-sfx hit generated/audio/sword_hit.py
   → Creates Python script using spec guidance
   → Run script to produce sword_hit.wav
   ```

### Workflow 2: Complete Music Creation

1. **Establish Style** (once per project)
   ```
   /establish-sonic-identity "8-bit platformer"
   ```

2. **Design Track** (design layer)
   ```
   /design-soundtrack "boss battle"
   → Creates .studio/music/boss-battle.spec.md
   → Contains tempo, key, chord progressions, structure
   ```

3. **Generate Instruments** (synthesis layer)
   ```
   /generate-instrument bass punchy
   /generate-instrument lead square
   → Creates Python scripts for instrument samples
   ```

4. **Compose Song** (composition layer)
   ```
   /generate-song "boss battle per spec"
   → Creates complete .xm or .it file using instruments and spec
   ```

### Workflow 3: Quick SFX (Skip Design)

For rapid iteration, skip the design phase:
```
/generate-sfx laser
→ Creates laser.py with sensible defaults
```

### Workflow 4: Quick Song (Skip Design)

```
/generate-song "mysterious ambient exploration theme"
→ Generates complete tracker file from description
```

## Data Flow

```
                   .studio/sonic-identity.md
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
    .studio/sfx/*.spec.md      .studio/music/*.spec.md
              │                           │
              ▼                           ▼
   Python synthesis scripts    Python instrument scripts
              │                           │
              ▼                           ▼
      generated/audio/*.wav         generated/audio/*.wav
                                          │
                                          ▼
                               .xm/.it tracker files
                                          │
                                          ▼
                                 nether.toml → ROM
```

## Cross-Plugin Skill Loading

When working on audio, Claude automatically loads relevant skills:

| Task | Skills Loaded |
|------|---------------|
| Establishing audio direction | `sonic-style-language`, `audio-integration` |
| Designing SFX | `sfx-design`, `procedural-sounds` |
| Designing music | `music-composition`, `tracker-fundamentals` |
| Generating SFX | `procedural-sounds` |
| Generating instruments | `procedural-instruments` |
| Composing tracker music | `xm-format` or `it-format`, `pattern-design` |

## Example: Full Audio Pipeline

```
User: "I'm making a dark fantasy RPG. Help me with the audio."

1. Claude uses /establish-sonic-identity
   → Creates sonic-identity.md with Orchestral + Dark Ambient style

2. User: "Design a sword hit sound"
   → sfx-architect creates .studio/sfx/sword-hit.spec.md

3. User: "Generate that sound effect"
   → /generate-sfx produces Python script
   → Script generates sword_hit.wav

4. User: "Design a boss battle theme"
   → music-architect creates .studio/music/boss-battle.spec.md

5. User: "Generate the instruments I need"
   → instrument-architect creates synthesis scripts
   → Scripts generate instrument samples

6. User: "Compose the boss theme"
   → song-generator creates boss_battle.it
   → Uses the generated instruments and follows spec
```

## Troubleshooting

### "Which plugin do I use?"

| Situation | Answer |
|-----------|--------|
| "I want to plan my audio style" | sound-design |
| "I want actual audio files" | zx-procgen |
| "I want tracker music" | tracker-music (uses zx-procgen for samples) |

### "Why separate design from synthesis?"

1. **Iteration** - Change specs without regenerating
2. **Consistency** - All audio follows the same style guide
3. **Parallelization** - Design all specs first, batch generate later
4. **Review** - Specs can be reviewed before committing to generation
