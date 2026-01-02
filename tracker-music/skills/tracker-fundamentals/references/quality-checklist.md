# Quality Checklist

Pre-release validation checklist for tracker music. Use before finalizing any generated track.

## Polish Validation

- [ ] **Velocity variation**: No two adjacent repeating notes have identical velocity (unless intentional accent)
- [ ] **Sustained notes**: Held notes (8+ rows) have vibrato or other movement
- [ ] **Melodic transitions**: Portamento used for smooth note connections where appropriate
- [ ] **Loop boundaries**: Volume fades or fills at loop points for seamless playback
- [ ] **Pattern variety**: At least one variation per 4-bar phrase (no exact repeats >2x)
- [ ] **Effect purpose**: Every effect serves a musical purpose (not just decoration)

## Technical Validation

- [ ] **Channel clarity**: Each channel has a defined role (drums, bass, lead, etc.)
- [ ] **File validates**: `validate_xm()` or `validate_it()` passes without errors
- [ ] **File size**: Reasonable size (<500KB typical, <200KB for short loops)
- [ ] **Loop seamless**: Plays through loop point 5+ times without clicks/pops
- [ ] **Order table**: Uses pattern reuse (not duplicate patterns)
- [ ] **Sample names**: Match Nethercore handle naming for asset integration

## Output Structure

- [ ] **Generator script**: Located in `generators/tracks/[name].py`
- [ ] **Output file**: Located in `generated/tracks/[name].xm` or `.it`
- [ ] **Imports correct**: Uses `lib/` primitives, not pre-made instruments

## Playback Test

1. Open in MilkyTracker or OpenMPT
2. Play through loop point 5+ times
3. Listen for:
   - Clicks or pops at transitions
   - Jarring volume changes
   - Rhythmic hiccups
   - Harmonic clashes at loop
4. Adjust fades/fills as needed

## Nethercore Integration

After validation, add to `nether.toml`:

```toml
[[assets.trackers]]
id = "track_name"
path = "music/track_name.xm"
```

Usage in game code:

```rust
let music = rom_tracker(b"track_name", 10);
music_play(music, 0.8, 1);
```
