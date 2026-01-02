# Variation Strategies

Techniques to prevent repetition fatigue for frequently-played sounds.

## Overview

| Method | Memory Cost | CPU Cost | Variety Level |
|--------|-------------|----------|---------------|
| Pre-made variations | High | Low | Maximum |
| Pitch randomization | None | Low | Good |
| Volume randomization | None | None | Subtle |
| Filter randomization | None | Medium | Good |
| Layer randomization | Medium | Low | High |
| Component synthesis | Medium | High | Maximum |

---

## Pre-made Variations

Create 3-5 distinct versions of the same sound.

**Best for:** Important sounds heard frequently (footsteps, hits)

**Implementation:**
```python
class SoundVariations:
    def __init__(self, variations: list):
        self.variations = variations
        self.last_played = -1

    def get_next(self, strategy='no_repeat'):
        if strategy == 'random':
            return random.choice(self.variations)
        elif strategy == 'no_repeat':
            # Don't play same sound twice
            idx = random.randint(0, len(self.variations) - 1)
            while idx == self.last_played and len(self.variations) > 1:
                idx = random.randint(0, len(self.variations) - 1)
            self.last_played = idx
            return self.variations[idx]
        elif strategy == 'round_robin':
            self.last_played = (self.last_played + 1) % len(self.variations)
            return self.variations[self.last_played]
```

---

## Pitch Randomization

Apply random pitch shift at runtime.

**Best for:** All frequently-played sounds

**Typical ranges:**
- Subtle: ±1 semitone
- Normal: ±2 semitones
- Noticeable: ±3-4 semitones

**Implementation:**
```python
def play_with_pitch_variation(sound, range_semitones=2.0):
    shift = random.uniform(-range_semitones, range_semitones)
    # Convert semitones to playback rate
    rate = 2 ** (shift / 12.0)
    play_sound(sound, playback_rate=rate)
```

**Caution:** Large pitch shifts affect duration and character.

---

## Volume Randomization

Apply random volume changes.

**Best for:** Natural-sounding variation

**Typical ranges:**
- Subtle: ±1 dB
- Normal: ±2 dB
- Dynamic: ±3 dB

**Implementation:**
```python
def play_with_volume_variation(sound, range_db=2.0):
    db_change = random.uniform(-range_db, range_db)
    gain = 10 ** (db_change / 20.0)
    play_sound(sound, volume=gain)
```

---

## Filter Randomization

Vary the tone/brightness at runtime.

**Best for:** Ambient sounds, footsteps

**Implementation:**
```python
def play_with_filter_variation(sound, cutoff_range=500):
    base_cutoff = 4000  # Hz
    variation = random.uniform(-cutoff_range, cutoff_range)
    play_sound(sound, lowpass_cutoff=base_cutoff + variation)
```

---

## Layer Randomization

Store sound components separately, combine randomly.

**Best for:** Complex sounds (explosions, impacts)

**Structure:**
```
explosion/
├── transients/
│   ├── trans_01.wav
│   ├── trans_02.wav
│   └── trans_03.wav
├── bodies/
│   ├── body_01.wav
│   └── body_02.wav
└── tails/
    ├── tail_01.wav
    └── tail_02.wav
```

**Implementation:**
```python
def play_randomized_layers(layer_folders):
    for folder in layer_folders:
        samples = get_samples_in_folder(folder)
        selected = random.choice(samples)
        play_sound(selected)
```

**Variation count:** 3 × 2 × 2 = 12 combinations from 7 files

---

## Combined Approach

For maximum variation, combine multiple techniques:

```python
def play_sound_with_full_variation(sound_group):
    # 1. Select variation
    base_sound = sound_group.get_next('no_repeat')

    # 2. Apply pitch variation
    pitch_shift = random.uniform(-2.0, 2.0)  # semitones

    # 3. Apply volume variation
    volume_db = random.uniform(-2.0, 1.0)  # dB

    # 4. Apply filter variation (optional)
    cutoff_offset = random.uniform(-300, 300)  # Hz

    play_sound(
        base_sound,
        pitch_shift=pitch_shift,
        volume_db=volume_db,
        filter_offset=cutoff_offset
    )
```

---

## Recommendations by Category

| Sound Type | Pre-made | Pitch | Volume | Filter |
|------------|----------|-------|--------|--------|
| Footsteps | 5+ | ±2 | ±2dB | ±300Hz |
| Impacts | 3-5 | ±2 | ±2dB | - |
| UI clicks | 1 | ±1 | ±1dB | - |
| Whooshes | 3 | ±3 | ±2dB | ±500Hz |
| Weapons | 3-5 | ±2 | ±1dB | - |
| Creatures | 3+ | ±3 | ±2dB | ±200Hz |
| Ambient | 1 (long) | - | - | - |

---

## Selection Strategies

| Strategy | Use Case |
|----------|----------|
| Random | General use |
| No-repeat | Prevent immediate repetition |
| Round-robin | Predictable cycling |
| Weighted | Favor certain variations |
| Distance-based | Closer = more variation |
