# Tracker Music Plugin

Platform-agnostic tracker music generation for Nethercore fantasy consoles. Generate polished XM and IT tracker modules programmatically from mood/style descriptions.

## Where This Plugin Fits

This plugin handles **music composition** - creating complete tracker files from design specs or descriptions.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ sound-design│ → │  zx-procgen │ → │tracker-music│
│   DESIGN    │    │  SYNTHESIS  │    │ COMPOSITION │
│             │    │             │    │  ← YOU ARE  │
│             │    │             │    │     HERE    │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Use this plugin to:**
- Generate complete .xm/.it tracker files (`/generate-song`, `song-generator`)
- Understand tracker polish techniques (`tracker-fundamentals` skill)
- Learn XM/IT format specifics (`xm-format`, `it-format` skills)

**Prerequisites (optional but recommended):**
- Audio style from `sound-design:/establish-sonic-identity`
- Music spec from `sound-design:/design-soundtrack`
- Instrument samples from `zx-procgen:/generate-instrument`

See [Audio Pipeline Guide](../docs/audio-pipeline.md) for complete workflows.

## Overview

This plugin enables Claude to generate complete, polished tracker music autonomously. Given a description like "dark mysterious boss theme", Claude can produce a professional-quality XM or IT file with proper effects, structure, and polish.

**Key Capabilities:**
- **Philosophy-driven generation** - Understands WHY to use effects, not just WHAT they do
- **Pattern efficiency** - Maximizes reuse, minimizes file size
- **Polish techniques** - Professional touches that separate amateur from polished output
- **End-to-end generation** - From mood description to playable tracker file

## Components

### Skills (4)

| Skill | Description |
|-------|-------------|
| `tracker-fundamentals` | Philosophy, polish techniques, when/why to use effects |
| `pattern-design` | Song structure, pattern efficiency, channel allocation |
| `xm-format` | XM file generation, effects, Python writer library |
| `it-format` | IT file generation, advanced features, Python writer library |

### Agents (1)

| Agent | Trigger | Description |
|-------|---------|-------------|
| `song-generator` | "generate a song", "make tracker music" | End-to-end song generation from mood/style description |

### Commands (2)

| Command | Description | Token Efficiency |
|---------|-------------|------------------|
| `/init-tracker-music` | Copy XM/IT writers to project (fast setup) ⚡ | 85% savings |
| `/generate-song` | Interactive song generation wizard | Standard |

## Quick Start

### Option 1: Set Up Infrastructure (Recommended for Projects) ⚡

**Token-efficient setup** - copies XM/IT writer files using native OS commands:

```
/init-tracker-music
```

This instantly sets up your tracker music project:
- Copies `xm_writer.py`, `it_writer.py`, `xm_types.py`, `it_types.py` to `lib/`
- Creates directory structure (`songs/`, `instruments/`, `patterns/`, `generated/`)
- Generates example song template and wrapper scripts
- **Uses 85% fewer tokens** (130 lines vs 904 lines)

**Best for:** New music composition projects, working with multiple songs, token-conscious workflows

### Option 2: Generate a Single Song (Quick)

**AI-assisted composition** - describe what you want and let the agent compose:

```
Ask: "Generate a dark, mysterious boss battle theme"
→ Triggers song-generator agent
→ Produces: boss_battle.it with embedded samples
```

Or use the command:

```
/generate-song "exploration theme for a haunted forest"
```

**Best for:** Quick one-off songs, experimenting with styles, learning tracker music

## Skill Architecture

### tracker-fundamentals (WHY)

The philosophical foundation - why certain effects create certain feelings:

- **Vibrato** for warmth and organic feel
- **Portamento** for smooth transitions and emphasis
- **Arpeggios** for chords without polyphony
- **Volume slides** for dynamics and expression
- **Pitch bends** for attack punch and character

### pattern-design (WHAT)

Structural patterns for effective songs:

- Genre-specific templates (action, ambient, boss, victory)
- Channel role conventions
- Pattern reuse strategies
- Loop point design

### xm-format / it-format (HOW)

Implementation details:

- Python writer libraries
- Effect command references
- Format specifications
- Examples

## Format Comparison

| Feature | XM | IT |
|---------|----|----|
| Channels | 32 max | 64 max |
| Note range | C-0 to B-7 (8 octaves) | C-0 to B-9 (10 octaves) |
| Polyphony | Note-off only | NNA (fade, continue, cut) |
| Pitch envelope | No | Yes |
| Resonant filter | No | Yes |
| File size | Smaller | Larger |
| Complexity | Simpler | More powerful |

**Choose XM when:** Simpler songs, smaller file size, sufficient features
**Choose IT when:** Need polyphony, pitch envelopes, filters, or >32 channels

## Integration with Other Plugins

### With sound-design plugin
- Uses `music-composition` skill for music theory (modes, progressions)
- Uses `sonic-style-language` for style definitions
- Complements `music-architect` agent for composition design

### With zx-procgen (or other console-specific plugins)
- Uses `procedural-instruments` for sample synthesis
- Uses `procedural-sounds` for SFX samples
- Output files integrate with nether.toml asset pipeline

### With creative-direction plugin
- Follows `.studio/sonic-identity.md` when present
- `sound-director` agent validates coherence

## Example Output

Given: "Create an 8-bit style victory fanfare"

```python
# Generated by song-generator agent
from xm_writer import *

# Triumphant chord progression: I - IV - V - I
# Tempo: 130 BPM, Key: C Major
# Polish: Arpeggio chords, volume swells, clean loop

module = XmModule(
    name="Victory",
    num_channels=4,
    default_speed=6,
    default_bpm=130,
    # ... complete implementation
)
```

## Installation

Add to your `.claude/settings.local.json`:

```json
{
  "enabledPlugins": {
    "tracker-music@nethercore-ai-plugins": true
  }
}
```

## License

Licensed under MIT or Apache-2.0, at your option.
