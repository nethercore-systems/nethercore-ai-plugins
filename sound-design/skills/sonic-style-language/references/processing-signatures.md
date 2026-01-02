# Processing Signatures

Effect character definitions and signal chains for different audio styles.

## Reverb Signatures

| Signature | Character | Decay | Use For |
|-----------|-----------|-------|---------|
| `reverb.none` | Dry, intimate | 0s | Chiptune, close sounds |
| `reverb.room` | Natural, small | 0.3-0.8s | Acoustic, realistic |
| `reverb.hall` | Spacious, concert | 1.5-3s | Orchestral, epic |
| `reverb.cathedral` | Massive, ethereal | 4-10s | Ambient, sacred |
| `reverb.plate` | Bright, musical | 1-2s | Vocals, snares |
| `reverb.spring` | Metallic, vintage | 0.5-1.5s | Lo-fi, retro |

---

## Distortion Signatures

| Signature | Character | Use For |
|-----------|-----------|---------|
| `distortion.none` | Clean | Most sounds |
| `distortion.warm` | Subtle saturation | Warmth, presence |
| `distortion.crunch` | Moderate overdrive | Rock, aggression |
| `distortion.heavy` | Aggressive clipping | Metal, industrial |
| `distortion.bitcrush` | Digital degradation | Retro, glitch |
| `distortion.tape` | Analog warmth | Lo-fi, vintage |

---

## Filter Signatures

| Signature | Character | Use For |
|-----------|-----------|---------|
| `filter.lowpass.warm` | Remove highs | Distance, muffled |
| `filter.lowpass.telephone` | Narrow band | Radio, phone effect |
| `filter.highpass.thin` | Remove lows | Tinny, small |
| `filter.bandpass.nasal` | Mid-focused | Voice effect |
| `filter.notch` | Remove specific freq | Problem solving |

---

## Style → Processing Mapping

| Style | Reverb | Distortion | Other |
|-------|--------|------------|-------|
| Orchestral | Hall/Cathedral | None | Natural dynamics |
| Chiptune | None/Room | None | Minimal processing |
| Electronic | Plate/Digital | Warm | Compression, sidechain |
| Industrial | Large/None | Heavy | Aggressive filtering |
| Ambient | Cathedral | None | Long delay, modulation |
| Dark Ambient | Massive | Bitcrush | Pitch modulation |
| Hybrid | Mixed | Warm | Parallel compression |
| Lo-Fi | Room + filter | Tape | Saturation, vinyl noise |
| Synthwave | Gated/Plate | None | Chorus, delay |

---

## Signal Chain Templates

### Orchestral Chain
```
Source → Light EQ → Hall Reverb (30% wet) → Gentle Compression → Master
```

### Electronic Chain
```
Source → EQ → Compression → Sidechain → Plate Reverb (20% wet) → Limiter
```

### Lo-Fi Chain
```
Source → Low-pass Filter → Tape Saturation → Room Reverb → Vinyl Noise Layer
```

### Horror/Dark Ambient Chain
```
Source → Pitch Modulation → Cathedral Reverb (60% wet) → Low-pass Filter → Master
```

---

## Dynamic Processing

| Context | Compression | Limiter | Notes |
|---------|-------------|---------|-------|
| Music | 2:1 - 4:1 | -1dB | Preserve dynamics |
| SFX | 4:1 - 8:1 | -0.5dB | Consistent levels |
| Dialogue | 3:1 - 6:1 | -1dB | Clarity focus |
| Master | 2:1 | -0.3dB | Glue, loudness |
