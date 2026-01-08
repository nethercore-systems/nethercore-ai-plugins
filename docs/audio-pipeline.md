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
│  Outputs:  .studio/sonic-identity.md (persisted)                │
│            Design specs stay in conversation (no .spec.md files)│
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        zx-procgen                                │
│                   SYNTHESIS - "How to Make"                      │
│                                                                  │
│  Commands: /generate-sfx, /generate-instrument                   │
│  Agents:   instrument-architect, sfx-architect                   │
│  Outputs:  .studio/instruments/*.spec.py, .wav files             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       tracker-music                              │
│                 COMPOSITION - "Arrange It"                       │
│                                                                  │
│  Commands: /generate-song                                        │
│  Agents:   song-generator                                        │
│  Outputs:  .studio/specs/music/*.spec.py, .xm/.it files         │
└─────────────────────────────────────────────────────────────────┘
```

## Plugin Responsibilities

| Plugin | Role | What It Does | What It Outputs |
|--------|------|--------------|-----------------|
| **sound-design** | DESIGN | Defines audio style, SFX layer patterns, music theory | `.studio/sonic-identity.md`, design specs in conversation |
| **zx-procgen** | SYNTHESIS | Generates actual audio using NumPy/SciPy | `.studio/instruments/*.spec.py`, `.wav` files |
| **tracker-music** | COMPOSITION | Arranges music into tracker modules | `.studio/specs/music/*.spec.py`, `.xm`/`.it` files |

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

**"Design" phase agents** keep specs in conversation context:
- `sfx-architect` (sound-design) - Outputs design in conversation, then offers synthesis
- `music-architect` (sound-design) - Outputs design in conversation, then offers generation

**"Synthesis" agents** create parsable `.spec.py` files:
- `instrument-architect` (zx-procgen) - Outputs `.studio/instruments/*.spec.py` with synthesis params
- `sfx-architect` (also zx-procgen) - Outputs `.studio/specs/sounds/*.spec.py`

**"Generator" agents** create runnable output:
- `song-generator` (tracker-music) - Outputs `.spec.py` specs and complete `.xm`/`.it` files

## Recommended Workflows

### Workflow 1: Complete SFX Creation

1. **Establish Style** (once per project)
   ```
   /establish-sonic-identity "dark fantasy RPG"
   → Creates .studio/sonic-identity.md
   ```

2. **Design SFX** (design → synthesis in one flow)
   ```
   /design-sfx "sword impact"
   → Shows design spec in conversation (layers, frequencies, synthesis approach)
   → Offers: "Ready to synthesize? I can spawn sfx-architect."
   → User says yes → sfx-architect creates .spec.py and .wav
   ```

### Workflow 2: Complete Music Creation

1. **Establish Style** (once per project)
   ```
   /establish-sonic-identity "8-bit platformer"
   ```

2. **Design Track** (design → generation in one flow)
   ```
   /design-soundtrack "boss battle"
   → Shows design spec in conversation (tempo, key, structure, chord progressions)
   → Offers: "Ready to generate? I can spawn song-generator."
   → User says yes → song-generator creates .spec.py files and .xm
   ```

   The song-generator handles instruments and composition together,
   creating `.studio/instruments/*.spec.py` and `.studio/specs/music/*.spec.py`.

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
    ┌───────────────────────┴───────────────────────┐
    │                                               │
    ▼ (SFX path)                                    ▼ (Music path)

Design in conversation                 Design in conversation
         │                                      │
         ▼                                      ▼
.studio/specs/sounds/*.spec.py    .studio/instruments/*.spec.py
         │                        .studio/specs/music/*.spec.py
         ▼                                      │
  generated/audio/*.wav                         ▼
                                   generated/tracks/*.xm
                                   generated/audio/*.wav (instruments)
                                                │
                                                ▼
                                       nether.toml → ROM
```

**Key change:** Design specs stay in conversation, only `.spec.py` files are persisted.

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
   → /design-sfx shows spec in conversation
   → Offers to synthesize → User says yes
   → sfx-architect creates .spec.py and .wav

3. User: "Design a boss battle theme"
   → /design-soundtrack shows spec in conversation
   → Offers to generate → User says yes
   → song-generator creates instrument specs, song spec, and .xm file
```

**Key difference:** No intermediate `.spec.md` files clutter the project.
Design flows directly from conversation to synthesis/composition.

## Troubleshooting

### "Which plugin do I use?"

| Situation | Answer |
|-----------|--------|
| "I want to plan my audio style" | sound-design |
| "I want actual audio files" | zx-procgen |
| "I want tracker music" | tracker-music (uses zx-procgen for samples) |

### "Why keep design in conversation instead of files?"

1. **Efficiency** - No wasteful intermediate files
2. **Flow** - Design → synthesis happens in one conversation
3. **Consistency** - Only `.spec.py` files that parsers actually use are persisted
4. **Review** - User can review design in conversation before confirming generation
