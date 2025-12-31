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

The user may provide:
- **description**: Free-form mood/style description (e.g., "dark mysterious boss theme")
- **--format**: XM or IT (defaults to XM)
- **--spec**: Path to a spec file (e.g., `.studio/music/menu-theme.spec.md`)

## Step 1: Parse Arguments and Gather Requirements

**If a spec file path was provided (--spec argument):**
1. Read the spec file to extract mood, style, tempo, key, instruments, and other parameters
2. Use those parameters instead of asking questions
3. Skip to Step 3

**If a description was provided but no spec file:**
1. Parse the description for mood, context, and style hints
2. If the description is clear enough (contains mood + context), proceed to Step 2
3. If the description is vague, use AskUserQuestion to clarify

**If no arguments were provided:**

Use AskUserQuestion to gather requirements:

- Question: "What kind of song do you need?"
- Header: "Mood"
- Options:
  - **Triumphant** - Victory, success, heroic moments
  - **Mysterious** - Exploration, secrets, unknown
  - **Aggressive** - Combat, boss battles, intensity
  - **Peaceful** - Calm, relaxation, safe areas

Then ask about context:

- Question: "What's the context for this music?"
- Header: "Context"
- Options:
  - **Menu/Title** - Main menu, title screen
  - **Gameplay** - General gameplay loop
  - **Boss Battle** - Intense combat encounters
  - **Exploration** - Wandering, discovering

## Step 2: Confirm Parameters

Present the interpreted parameters to the user for confirmation:

Based on the gathered information, determine:
- **Mood**: The emotional tone
- **Key**: Select appropriate key (D minor for dark, C major for bright, etc.)
- **Mode**: Major/minor/modal based on mood
- **Tempo**: BPM based on context (100-120 for exploration, 140-160 for combat)
- **Format**: XM (default) or IT if specified
- **Instruments**: Appropriate for the style (drums, bass, lead, pad)

Use AskUserQuestion to confirm:

- Question: "Generate with these parameters? (Mood: [mood], Key: [key], Tempo: [bpm] BPM, Format: [format])"
- Header: "Confirm"
- Options:
  - **Yes, generate** - Proceed with these parameters
  - **Adjust tempo** - Change the BPM
  - **Adjust key** - Change the musical key
  - **Adjust format** - Switch between XM and IT

If the user wants adjustments, use additional AskUserQuestion calls to refine.

## Step 3: Check for Sonic Identity

Check if the project has a sonic identity file:
- `.studio/sonic-identity.md`
- `.studio/sonic-identity.local.md`

**If found:**
Read the file and extract style constraints (instrument palette, tempo ranges, key preferences).
Incorporate these constraints into the generation parameters.

**If not found:**
Proceed with the parameters gathered in previous steps.

## Step 4: Generate the Song

Use the Task tool to invoke the song-generator agent:

```
Task tool parameters:
- subagent_type: "tracker-music:song-generator"
- description: "Generate [mood] [context] song"
- prompt: Include all gathered parameters:
  - Mood and context description
  - Key and mode
  - Tempo (BPM)
  - Format (XM or IT)
  - Instrument suggestions
  - Duration/loop requirements
  - Any sonic identity constraints
  - Output path: assets/music/[song_name].[xm|it]
```

Wait for the agent to complete and retrieve its results.

## Step 5: Report Results

After the agent completes, present the results:

1. **File created**: Show the path to the generated file
2. **Song details**: Key, tempo, pattern count, duration, channel count
3. **Instruments used**: List with roles
4. **Next steps**:
   - How to test (MilkyTracker, OpenMPT)
   - How to add to nether.toml
   - How to use in game code

Example output:
```
Created: assets/music/boss_theme.it

Song Details:
- Key: D Minor
- Tempo: 140 BPM
- Patterns: 4 patterns, 12 orders
- Duration: ~45 seconds (loops from order 2)
- Channels: 8

Instruments:
1. Kick - Punchy low drum
2. Snare - Tight snare hit
3. Hi-hat - Closed hat pattern
4. Bass - Dark synth bass
5. Lead - Aggressive saw lead
6. Pad - Ominous pad

Next steps:
1. Test in MilkyTracker or OpenMPT
2. Add to nether.toml:
   [[assets.trackers]]
   id = "boss_theme"
   path = "music/boss_theme.it"
3. Use in game: music_play(rom_tracker(b"boss_theme", 12345), 0.8, 1)
```

Then offer follow-up actions:

- Question: "What would you like to do next?"
- Header: "Next"
- Options:
  - **Test it** - Show how to preview the song
  - **Generate another** - Create a different song
  - **Add to nether.toml** - Configure for use in game
  - **Done** - Finish

## Error Handling

If the song-generator agent fails:
1. Report the specific error
2. Suggest simplifications (fewer channels, XM instead of IT)
3. Offer to retry with adjusted parameters
