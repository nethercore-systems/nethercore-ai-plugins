

# IT Effect Commands Reference

Complete reference for Impulse Tracker effect commands. Based on [ITTECH.TXT](https://github.com/schismtracker/schismtracker/wiki/ITTECH.TXT).

## Effect Command Format

```python
ItNote.play("C-4", 1, 64).with_effect(effect, param)
```

- **effect**: 1-26 (A-Z letters)
- **param**: 0-255 (0x00-0xFF)

## Effect Commands (A-Z)

### A - Set Speed
Sets ticks per row (tempo control).

```python
.with_effect(1, 6)    # 6 ticks per row (default)
.with_effect(1, 3)    # Faster (3 ticks/row)
.with_effect(1, 12)   # Slower (12 ticks/row)
```

**Range:** 1-255 ticks/row
**Default:** 6

### B - Position Jump
Jump to a specific pattern in the order table.

```python
.with_effect(2, 0)    # Jump to first pattern
.with_effect(2, 5)    # Jump to 6th pattern (0-indexed)
```

**Range:** 0-255 (pattern index in order table)

### C - Pattern Break
Break to row in next pattern.

```python
.with_effect(3, 0)     # Break to row 0 of next pattern
.with_effect(3, 16)    # Break to row 16 of next pattern
```

**Range:** 0-63 (row number)
**Note:** Param is in decimal, not hex (16 = row 16, not 0x16)

### D - Volume Slide
Slide volume up or down.

```python
.with_effect(4, 0x0F)  # Slide down by F
.with_effect(4, 0xF0)  # Slide up by F
.with_effect(4, 0x00)  # Continue previous slide
```

**Format:** `0xUDwhere U = up amount, D = down amount
**Note:** Only one nibble should be non-zero

### E - Pitch Slide Down
Slide pitch down (portamento down).

```python
.with_effect(5, 0x10)  # Slide down by 10
.with_effect(5, 0xE0)  # Fine slide down E (once per row)
.with_effect(5, 0xF0)  # Extra fine slide down (once per row)
```

**Format:**
- `0x01-0xDF`: Regular slide
- `0xE0-0xEF`: Fine slide (E + value)
- `0xF0-0xFF`: Extra fine slide (F + value)

### F - Pitch Slide Up
Slide pitch up (portamento up).

```python
.with_effect(6, 0x10)  # Slide up by 10
.with_effect(6, 0xE0)  # Fine slide up E (once per row)
.with_effect(6, 0xF0)  # Extra fine slide up (once per row)
```

**Format:** Same as E (pitch slide down)

### G - Tone Portamento
Slide to note (pitch bend to target note).

```python
# Set target note, then use G to slide to it
pattern.set_note(0, 0, ItNote.play("C-4", 1, 64))
pattern.set_note(16, 0, ItNote.play("G-4", 1, 64).with_effect(7, 0x10))
```

**Param:** Slide speed (0 = use previous speed)

### H - Vibrato
Apply vibrato to note (pitch oscillation).

```python
.with_effect(8, 0x34)  # Speed 3, depth 4
.with_effect(8, 0x00)  # Continue previous vibrato
```

**Format:** `0xSD` where S = speed, D = depth

### I - Tremor
Rapidly toggle volume on/off.

```python
.with_effect(9, 0x34)  # 3 ticks on, 4 ticks off
```

**Format:** `0xON` where O = on time, N = off time

### J - Arpeggio
Rapidly cycle through three notes (chord effect).

```python
.with_effect(10, 0x00)  # No arpeggio
.with_effect(10, 0x37)  # Major chord (0, +3, +7 semitones)
.with_effect(10, 0x47)  # Minor chord (0, +4, +7 semitones)
```

**Format:** `0x12` cycles between base note, +1 semitone, +2 semitones

### K - Vibrato + Volume Slide
Combines H (vibrato) and D (volume slide).

```python
.with_effect(11, 0x0F)  # Vibrato + volume slide down F
.with_effect(11, 0xF0)  # Vibrato + volume slide up F
```

**Format:** Same as D (volume slide)

### L - Tone Portamento + Volume Slide
Combines G (tone portamento) and D (volume slide).

```python
.with_effect(12, 0x0F)  # Porta to note + volume slide down
.with_effect(12, 0xF0)  # Porta to note + volume slide up
```

**Format:** Same as D (volume slide)

### M - Set Channel Volume
Set the channel's base volume (separate from note volume).

```python
.with_effect(13, 0x40)  # Set channel volume to 64 (full)
.with_effect(13, 0x20)  # Set channel volume to 32 (half)
```

**Range:** 0-64

### N - Channel Volume Slide
Slide the channel volume up or down.

```python
.with_effect(14, 0x0F)  # Channel volume slide down F
.with_effect(14, 0xF0)  # Channel volume slide up F
```

**Format:** Same as D (volume slide)

### O - Sample Offset
Start playing sample from a specific offset.

```python
.with_effect(15, 0x80)  # Start at offset 0x8000
.with_effect(15, 0x00)  # Use previous offset
```

**Format:** `param * 256` = byte offset into sample

### P - Panning Slide
Slide panning left or right.

```python
.with_effect(16, 0x0F)  # Slide left by F
.with_effect(16, 0xF0)  # Slide right by F
.with_effect(16, 0xE0)  # Fine slide left (once per row)
.with_effect(16, 0x0E)  # Fine slide right (once per row)
```

**Format:** `0xLR` where L = left amount, R = right amount

### Q - Retrigger Note
Retrigger note at regular intervals.

```python
.with_effect(17, 0x03)  # Retrigger every 3 ticks
.with_effect(17, 0x81)  # Retrigger every tick, volume *0.5
```

**Format:** `0xVT` where V = volume change, T = retrigger time
**Volume change (V):**
- 0: No change
- 1-5: Volume - (1, 2, 4, 8, 16)
- 6-7: Volume * (2/3, 1/2)
- 8: Reserved
- 9-13: Volume + (1, 2, 4, 8, 16)
- 14-15: Volume * (3/2, 2)

### R - Tremolo
Apply tremolo to volume (volume oscillation).

```python
.with_effect(18, 0x34)  # Speed 3, depth 4
```

**Format:** `0xSD` where S = speed, D = depth

### S - Extended Effects
Sub-effects for various special commands.

```python
.with_effect(19, 0xC3)  # Note cut after 3 ticks (SC3)
.with_effect(19, 0xD2)  # Note delay 2 ticks (SD2)
.with_effect(19, 0xB0)  # Set loop point (SB0)
.with_effect(19, 0xB3)  # Loop pattern 3 times (SB3)
```

**Format:** `0xXY` where X = sub-effect, Y = param

**Sub-effects:**
- `S0y`: Set filter (obsolete)
- `S1y`: Set glissando (0=off, 1=on)
- `S2y`: Set finetune
- `S3y`: Set vibrato waveform (0=sine, 1=ramp down, 2=square, 3=random)
- `S4y`: Set tremolo waveform
- `S5y`: Set panbrello waveform
- `S6y`: Fine pattern delay (y extra ticks)
- `S7y`: Instrument control (past note actions)
- `S8y`: Set panning (0=left, 8=center, F=right)
- `S9y`: Sound control (surround, reverb)
- `SAy`: High sample offset (upper 8 bits)
- `SBy`: Pattern loop (0=set loop, 1-F=loop y times)
- `SCy`: Note cut after y ticks
- `SDy`: Note delay y ticks
- `SEy`: Pattern delay y rows
- `SFy`: Set active macro

### T - Set Tempo (BPM)
Set tempo in beats per minute.

```python
.with_effect(20, 125)   # 125 BPM (default)
.with_effect(20, 140)   # 140 BPM (faster)
.with_effect(20, 0x10)  # Tempo slide down
.with_effect(20, 0x20)  # Tempo slide up
```

**Format:**
- `0x00-0x0F`: Tempo slide down
- `0x10-0x1F`: Tempo slide up
- `32-255`: Set absolute BPM

### U - Fine Vibrato
Vibrato with finer depth control (1/4 depth of H).

```python
.with_effect(21, 0x34)  # Fine vibrato, speed 3, depth 4
```

**Format:** Same as H (vibrato)

### V - Set Global Volume
Set the global volume for all channels.

```python
.with_effect(22, 0x80)  # Set global volume to 128 (full)
.with_effect(22, 0x40)  # Set global volume to 64 (half)
```

**Range:** 0-128

### W - Global Volume Slide
Slide the global volume up or down.

```python
.with_effect(23, 0x0F)  # Global volume slide down F
.with_effect(23, 0xF0)  # Global volume slide up F
```

**Format:** Same as D (volume slide)

### X - Set Panning
Set stereo panning position.

```python
.with_effect(24, 0x00)  # Hard left
.with_effect(24, 0x80)  # Center
.with_effect(24, 0xFF)  # Hard right
```

**Range:** 0-255 (0=left, 128=center, 255=right)

### Y - Panbrello
Apply panbrello (panning oscillation).

```python
.with_effect(25, 0x34)  # Speed 3, depth 4
```

**Format:** `0xSD` where S = speed, D = depth

### Z - MIDI Macro / Filter
Trigger MIDI macro or set filter cutoff.

```python
.with_effect(26, 0x80)  # Set filter cutoff
```

**Note:** Functionality depends on MIDI macro configuration

## Common Effect Patterns

### Kick Drum with Pitch Slide

```python
note = ItNote.play("C-5", kick_instr, 64)
    .with_effect(5, 0x40)  # Pitch slide down (E40)
```

### Snare with Volume Fade

```python
note = ItNote.play("C-4", snare_instr, 64)
    .with_effect(4, 0x08)  # Volume slide down (D08)
```

### Bass with Portamento

```python
# Row 0: Start note
pattern.set_note(0, 0, ItNote.play("C-3", bass_instr, 64))
# Row 16: Slide to new note
pattern.set_note(16, 0, ItNote.play("G-3", bass_instr, 64).with_effect(7, 0x20))
```

### Arpeggio Chord

```python
# Major chord (0, +4, +7)
note = ItNote.play("C-4", lead_instr, 64)
    .with_effect(10, 0x47)  # Arpeggio (J47)
```

### Pattern Loop

```python
# Set loop point
pattern.set_note(0, 0, ItNote().with_effect(19, 0xB0))  # SB0
# Loop 4 times
pattern.set_note(32, 0, ItNote().with_effect(19, 0xB4))  # SB4
```

## Volume Column vs Effect Column

IT allows volume effects in the volume column (0-212):

| Range | Effect | Equivalent |
|-------|--------|------------|
| 0-64 | Set volume | - |
| 65-74 | Fine volume up | `D0x` |
| 75-84 | Fine volume down | `Dx0` |
| 85-94 | Volume slide up | `Dx0` |
| 95-104 | Volume slide down | `D0x` |
| 105-114 | Pitch slide down | `Ex0` |
| 115-124 | Pitch slide up | `Fx0` |
| 128-192 | Set panning | `X` |
| 193-202 | Tone portamento | `Gx0` |
| 203-212 | Vibrato | `H0x` |

Use `ItNote.with_volume_column(value)` to access these.

## Reference

Full specification: [ITTECH.TXT](https://github.com/schismtracker/schismtracker/wiki/ITTECH.TXT)
