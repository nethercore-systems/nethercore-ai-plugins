# XM Effect Command Reference

Complete reference for XM tracker effect commands supported by Nethercore ZX.

## Main Effect Column (0-F, G-R, X)

| Effect | Hex | Name | Parameter | Description |
|--------|-----|------|-----------|-------------|
| 0 | 0xy | Arpeggio | x=semi1, y=semi2 | Rapidly switch between note, note+x, note+y |
| 1 | 1xx | Portamento Up | xx=speed | Slide pitch up by xx units per tick |
| 2 | 2xx | Portamento Down | xx=speed | Slide pitch down by xx units per tick |
| 3 | 3xx | Tone Portamento | xx=speed | Glide to note at speed xx |
| 4 | 4xy | Vibrato | x=speed, y=depth | Oscillate pitch |
| 5 | 5xy | Tone Porta + Vol Slide | xy=vol slide | Combine 3xx with Axy |
| 6 | 6xy | Vibrato + Vol Slide | xy=vol slide | Combine 4xy with Axy |
| 7 | 7xy | Tremolo | x=speed, y=depth | Oscillate volume |
| 8 | 8xx | Set Panning | xx=position | 00=left, 80=center, FF=right |
| 9 | 9xx | Sample Offset | xx=offset | Start sample at xx×256 samples |
| A | Axy | Volume Slide | x=up, y=down | Slide volume per tick |
| B | Bxx | Position Jump | xx=order | Jump to order xx |
| C | Cxx | Set Volume | xx=volume | Set volume (00-40) |
| D | Dxx | Pattern Break | xx=row | Jump to row xx of next pattern |
| E | Exy | Extended Effects | See below | Extended effect sub-commands |
| F | Fxx | Set Speed/Tempo | xx=value | xx<32: speed, xx>=32: BPM |
| G | Gxx | Set Global Volume | xx=volume | Set global volume (00-40) |
| H | Hxy | Global Volume Slide | xy=slide | Slide global volume |
| K | Kxx | Key Off | xx=tick | Release note at tick xx |
| L | Lxx | Set Envelope Position | xx=pos | Jump envelope to position |
| P | Pxy | Panning Slide | x=left, y=right | Slide panning |
| R | Rxy | Retrigger | x=vol change, y=ticks | Retrigger note every y ticks |

## Extended Effects (Exy)

| Effect | Hex | Name | Parameter | Description |
|--------|-----|------|-----------|-------------|
| E1 | E1x | Fine Porta Up | x=speed | Fine pitch slide up |
| E2 | E2x | Fine Porta Down | x=speed | Fine pitch slide down |
| E3 | E3x | Glissando Control | x=on/off | Quantize portamento to semitones |
| E4 | E4x | Vibrato Waveform | x=type | 0=sine, 1=ramp, 2=square |
| E5 | E5x | Set Finetune | x=finetune | Override sample finetune |
| E6 | E6x | Pattern Loop | x=count | x=0: set start, x>0: loop x times |
| E7 | E7x | Tremolo Waveform | x=type | 0=sine, 1=ramp, 2=square |
| E8 | E8x | Set Panning (Coarse) | x=position | 0=left, 8=center, F=right |
| E9 | E9x | Retrigger Note | x=ticks | Retrigger every x ticks |
| EA | EAx | Fine Volume Up | x=amount | Fine volume slide up |
| EB | EBx | Fine Volume Down | x=amount | Fine volume slide down |
| EC | ECx | Note Cut | x=tick | Cut note at tick x |
| ED | EDx | Note Delay | x=tick | Delay note until tick x |
| EE | EEx | Pattern Delay | x=rows | Delay pattern x extra rows |

## Volume Column Effects

The volume column (0-64 sets volume directly, 65+ are effects):

| Range | Hex | Effect | Description |
|-------|-----|--------|-------------|
| 00-40 | 00-40 | Set Volume | Direct volume 0-64 |
| 60-6F | 60-6F | Volume Slide Down | Slide down by y |
| 70-7F | 70-7F | Volume Slide Up | Slide up by y |
| 80-8F | 80-8F | Fine Vol Down | Fine slide down |
| 90-9F | 90-9F | Fine Vol Up | Fine slide up |
| A0-AF | A0-AF | Vibrato Speed | Set vibrato speed |
| B0-BF | B0-BF | Vibrato Depth | Set vibrato depth |
| C0-CF | C0-CF | Set Panning | Set pan position |
| D0-DF | D0-DF | Pan Slide Left | Slide pan left |
| E0-EF | E0-EF | Pan Slide Right | Slide pan right |
| F0-FF | F0-FF | Tone Portamento | Glide to note |

## Common Effect Patterns

### Chiptune Arpeggio
```
C-4 01 -- 047  ; Major chord arpeggio (C-E-G)
--- -- -- 037  ; Minor chord (C-Eb-G)
--- -- -- 057  ; Power chord (C-G-C)
```

### Fade In
```
C-4 01 00 ---  ; Start at volume 0
--- -- -- A04  ; Slide up 4 per tick
```

### Fade Out with Note Cut
```
C-4 01 40 ---  ; Start at full volume
--- -- -- A40  ; Slide down 4 per tick
--- -- -- EC8  ; Cut note at tick 8
```

### Vibrato + Volume Swell
```
C-4 01 20 4A3  ; Vibrato speed A, depth 3
--- -- -- 604  ; Continue vibrato + vol slide up
```

### Pattern Section Loop
```
Row 0: --- -- -- E60  ; Set loop point
Row 8: --- -- -- E63  ; Loop 3 times back to row 0
```

### Tempo Change for Transitions
```
; Slow section (80 BPM)
--- -- -- F50  ; Set tempo 80

; Speed up for action
--- -- -- F8C  ; Set tempo 140
```

### Note Delay for Shuffle/Swing
```
C-4 01 -- ---    ; On beat
--- -- -- ED3    ; Delay 3 ticks (swing feel)
C-4 01 -- ---    ; On beat
```

## Effect Priority and Interaction

- Only one effect per cell (effect column)
- Volume column effects are independent
- Tone portamento (3xx) needs target note
- Vibrato (4xy) continues until new note
- Position jump (Bxx) and pattern break (Dxx) can combine
- Speed <32 sets ticks/row, >=32 sets BPM
