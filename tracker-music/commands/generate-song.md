---
description: Interactive wizard for generating tracker music from a description
argument-hint: "[mood/style description]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
---

# Generate Song Command

Guide the user through generating a complete tracker song.

## Process

### Phase 1: Understand the Request

If the user provided a description, parse it. Otherwise, ask:

"What kind of song do you need? Please describe:
- **Mood:** (e.g., triumphant, mysterious, aggressive, peaceful)
- **Context:** (e.g., boss battle, exploration, menu, victory jingle)
- **Style:** (e.g., chiptune, orchestral, electronic, ambient)"

### Phase 2: Confirm Parameters

Present the interpreted parameters:

"Based on your description, I'll create:
- **Mood:** [Mood]
- **Key:** [Key] [Mode]
- **Tempo:** [BPM] BPM
- **Format:** [XM/IT]
- **Duration:** ~[X] bars ([Y] seconds at this tempo)
- **Instruments:** [List]

Does this sound right? Any adjustments?"

### Phase 3: Check for Sonic Identity

Look for `.studio/sonic-identity.md` or `.studio/sonic-identity.local.md`:

```
If found:
  "I found your project's sonic identity. I'll follow those style guidelines."
  Load and apply constraints.

If not found:
  "No sonic identity found. Would you like me to:
  1. Generate with default style for the mood
  2. Run /establish-sonic-identity first"
```

### Phase 4: Generate

Invoke the song-generator agent with the confirmed parameters.

Create the file at: `assets/music/[song_name].[xm|it]`

### Phase 5: Report Results

"Created: `assets/music/[filename].[xm|it]`

**Song Details:**
- Key: [Key] [Mode]
- Tempo: [BPM] BPM
- Patterns: [N] patterns, [M] orders
- Duration: ~[X] seconds (loops from order [Y])
- Channels: [N] channels

**Instruments:**
1. [Instrument 1] - [Role]
2. [Instrument 2] - [Role]
...

**Next steps:**
1. Test in MilkyTracker/OpenMPT
2. Add to nether.toml:
   ```toml
   [[assets.trackers]]
   id = \"[song_name]\"
   path = \"music/[filename].[xm|it]\"
   ```
3. Use in game: `music_play(rom_tracker(b\"[song_name]\", [len]), 0.8, 1)`

Would you like me to:
- Generate another song?
- Modify this song?
- Add it to nether.toml?"

## Example Interactions

### Quick Generation

```
User: /generate-song dark mysterious boss theme