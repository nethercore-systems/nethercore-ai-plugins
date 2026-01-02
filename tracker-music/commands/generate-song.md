---
description: Interactive wizard for generating tracker music from a description
argument-hint: "[mood/style description] [--format xm|it] [--spec path/to/spec.md]"
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

## Arguments

- **description**: Mood/style (e.g., "dark mysterious boss theme")
- **--format**: XM or IT (defaults to XM)
- **--spec**: Path to spec file with pre-defined parameters

## Step 1: Gather Requirements

**If --spec provided:** Read spec file, skip to Step 3.

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

Look for `.studio/sonic-identity.md` or `.studio/sonic-identity.local.md`. If found, incorporate style constraints.

## Step 4: Generate

Invoke song-generator agent:

```
Task tool:
- subagent_type: "tracker-music:song-generator"
- description: "Generate [mood] [context] song"
- prompt: All parameters, constraints, output path
```

## Step 5: Report Results

After completion, show:

```
Created: generated/tracks/boss_theme.it

Song Details:
- Key: D Minor, Tempo: 140 BPM
- Patterns: 4, Duration: ~45s (loops from order 2)
- Channels: 8

Instruments: Kick, Snare, Hi-hat, Bass, Lead, Pad

Next steps:
1. Test in MilkyTracker/OpenMPT
2. Add to nether.toml:
   [[assets.trackers]]
   id = "boss_theme"
   path = "music/boss_theme.it"
3. Use: music_play(rom_tracker(b"boss_theme", 10), 0.8, 1)
```

Offer follow-up: Test it / Generate another / Add to nether.toml / Done
