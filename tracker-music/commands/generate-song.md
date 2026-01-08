---
description: Interactive wizard for generating tracker music from a description
argument-hint: "[mood/style description] [--format xm|it]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
  - Task
---

# Generate Song Command

Generate a complete tracker song (XM or IT format) from a mood/style description.

## Spec-Driven Workflow

This command creates `.spec.py` files (with SONG dict) that are parsed to XM/IT modules:

```
User description → song spec (.spec.py) → song_parser.py → .xm/.it
```

All specs use `.spec.py` extension. The folder and dict name identify the type.

## Arguments

- **description**: Mood/style (e.g., "dark mysterious boss theme")
- **--format**: XM or IT (defaults to XM)

## Step 1: Gather Requirements

**If description provided:** Parse for mood, context, style. If clear enough, proceed.

**If unclear or missing:**

Use AskUserQuestion:
- "What kind of song?" → Triumphant / Mysterious / Aggressive / Peaceful
- "What's the context?" → Menu / Gameplay / Boss Battle / Exploration

## Step 2: Confirm Parameters

Present interpreted parameters:
- Mood, Key, Mode, Tempo, Format, Instruments

Use AskUserQuestion to confirm or adjust.

## Step 3: Check Sonic Identity

Look for `.studio/sonic-identity.md`. If found, incorporate style constraints.

## Step 4: Generate

Invoke song-generator agent:

```
Task tool:
- subagent_type: "tracker-music:song-generator"
- description: "Generate [mood] [context] song"
- prompt: |
    Create a .spec.py file (SONG dict) for: [description]

    Requirements:
    - Create instrument specs in .studio/instruments/*.spec.py if needed
    - Create song spec in .studio/specs/music/[name].spec.py
    - Run song_parser.py to generate output
    - Output to generated/tracks/

    Parameters:
    - Format: [xm/it]
    - Mood: [mood]
    - Context: [context]
    - Tempo: [bpm]
```

## Step 5: Report Results

After completion, show:

```
Created:
- .studio/specs/music/boss_theme.spec.py (spec - committed)
- generated/tracks/boss_theme.xm (output - gitignored)

Song Details:
- Key: D Minor, Tempo: 140 BPM
- Patterns: 4, Duration: ~45s (loops from order 2)
- Channels: 8

Instruments: Kick, Snare, Hi-hat, Bass, Lead, Pad

Next steps:
1. Test in MilkyTracker/OpenMPT
2. Add to nether.toml:
   [[assets.sounds]]
   id = "boss_theme"
   path = "../generated/tracks/boss_theme.xm"
3. Use: music_play(rom_tracker(b"boss_theme", 10), 0.8, 1)
```

Offer follow-up: Test it / Generate another / Add to nether.toml / Done
