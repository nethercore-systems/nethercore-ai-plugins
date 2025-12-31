# Loop Techniques Reference

Advanced techniques for seamless music loops.

## Loop Point Fundamentals

### The Perfect Loop

A perfect loop satisfies:

1. **Zero-click transition** - No audio artifacts
2. **Rhythmic continuity** - Beat flows naturally
3. **Harmonic resolution** - Chords make sense
4. **Energy matching** - Volume/intensity consistent
5. **Timbral continuity** - Same instruments active

### Loop Boundary Rows

```
Pattern End (last 8 rows):
Row 56: Begin fade if needed, hold sustains
Row 57: Continue any fades
Row 58: Last new note placements
Row 59: Allow note tails
Row 60: Prepare for loop (volume normalize)
Row 61: Final effect commands
Row 62: Pattern break or position jump
Row 63: Clean - no new attacks

Pattern Start (first 4 rows):
Row 0:  Primary hits (kick, chord attack)
Row 1:  Follow-up (hi-hat, continuation)
Row 2:  Establish groove
Row 3:  Melody entrance point
```

## Transition Techniques

### Volume Fade Crossover

Fade out end while attack at start creates seamless blend:

```
Pattern end:
Row 60: Lead note with A04 (volume slide down)
Row 61: --- -- -- A04
Row 62: --- -- -- A04
Row 63: --- -- -- A04 (nearly silent)

Pattern start:
Row 0:  New attack at full volume
```

### Sustained Pad Bridge

Keep a pad sustaining across the loop point:

```
Pattern end:
Row 48-63: Pad continues, no note-off

Pattern start:
Row 0: Pad note re-triggered or continues
       Other instruments attack fresh
```

### Drum Fill Transition

Use fills to mask loop boundary:

```
Pattern end:
Row 56: Tom fill begins
Row 60: Crash cymbal (covers transition)
Row 63: Fill ends

Pattern start:
Row 0:  Kick attack (cymbal still ringing)
```

## Harmonic Loop Preparation

### Dominant to Tonic

End on V chord, loop to I chord:

```
Key of C major:
Pattern end, rows 48-63: G major chord (V)
Pattern start, row 0: C major chord (I)
→ Creates natural resolution
```

### Suspended Resolution

End on sus4, resolve to major:

```
Pattern end: Csus4 (C-F-G)
Pattern start: C major (C-E-G)
→ Satisfying resolution across loop
```

### Pedal Tone

Keep bass note constant while harmony moves:

```
Pattern end: C (bass) with G chord above
Pattern start: C (bass) with C chord above
→ Bass continuity masks harmonic change
```

## Restart Position Strategy

### Skip Intro on Loop

```python
module = XmModule(
    order_table=[0, 1, 1, 2, 1, 1, 2, 3],
    restart_position=1,  # Skip pattern 0 (intro)
)
# Plays: Intro, V, V, C, V, V, C, Bridge → V, V, C, V, V, C, Bridge → ...
```

### Loop to Specific Section

```python
# After outro, loop back to chorus
module = XmModule(
    order_table=[0, 1, 2, 3, 4],  # Intro, V, C, V, Outro
    restart_position=2,  # Loop from Chorus
)
# Plays: Intro, V, C, V, Outro → C, V, Outro → C, V, Outro → ...
```

### Full Song Loop

```python
module = XmModule(
    order_table=[0, 1, 2, 3],
    restart_position=0,  # Loop entire song
)
```

## Common Loop Problems and Solutions

### Problem: Click at Loop Point

**Cause:** Sudden volume change or sample cut
**Solution:**
```
- Add volume fade in last 4 rows
- Ensure notes end naturally before loop
- Use note-off (===) instead of sudden cut
```

### Problem: Rhythmic Skip

**Cause:** Last row count doesn't match beat
**Solution:**
```
- Ensure pattern length is multiple of beat (usually 64)
- Check loop point aligns with downbeat
- Use pattern break (Cxx) to end exactly on beat
```

### Problem: Harmonic Clash

**Cause:** End chord conflicts with start chord
**Solution:**
```
- End on V or vii°, start on I
- Use common tones between chords
- Fade harmony before loop, attack fresh
```

### Problem: Energy Mismatch

**Cause:** End too quiet/loud compared to start
**Solution:**
```
- Match dynamics between last and first bars
- Use intro as buildup, loop from main section
- Normalize volumes in last 8 rows
```

### Problem: Hanging Notes

**Cause:** Sustained notes cut abruptly at loop
**Solution:**
```
- Add note-off before loop point
- Use NNA_FADE (IT) for smooth note release
- Match sustain state at loop start
```

## Advanced Loop Architectures

### Multi-Section Loop

```
Order: [0, 1, 1, 2, 1, 1, 2, 3]
        ↓
        └── restart_position = 1

After pattern 3 (bridge), jumps to pattern 1 (verse)
Creates: Intro → Verse-Chorus cycle
```

### Adaptive Loop Points

```
Pattern 1 ends with: Bxx (position jump to order xx)
Pattern 2 ends normally (continues to next order)

Order: [0, 1, 2, 3]
       Pattern 1 can jump to different locations
       Based on gameplay state, music_jump() to different orders
```

### Seamless Intensity Layers

```
Pattern 1 (low intensity): Sparse drums, pad
Pattern 2 (med intensity): Add bass, melody
Pattern 3 (high intensity): Full arrangement

All three share:
- Same tempo
- Same harmonic progression
- Same loop point characteristics

music_jump() between them for adaptive music
```

## Loop Testing Checklist

1. [ ] Listen through loop point 10+ times
2. [ ] Check with eyes closed (focus on audio only)
3. [ ] Verify no clicks or pops
4. [ ] Confirm beat doesn't skip
5. [ ] Harmony resolves naturally
6. [ ] Energy level consistent
7. [ ] Test at different playback points
8. [ ] Verify restart_position skips intro correctly
9. [ ] Test after long playback (5+ minutes)
10. [ ] Listen on different audio systems
