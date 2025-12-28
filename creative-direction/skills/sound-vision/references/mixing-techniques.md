# Audio Mixing Techniques for Games

## Fundamental Mixing Concepts

### Gain Staging

Proper level management from source to output:

1. **Source Level**: Record/design sounds at optimal level (-18 to -12dBFS peak)
2. **Channel Level**: Set relative balance between elements
3. **Bus Level**: Group processing (e.g., all SFX through one bus)
4. **Master Level**: Final output protection (-1dBFS peak max)

### Headroom

Leave space for peaks and dynamics:
- Target RMS: -18 to -14dBFS for music
- Target RMS: -20 to -16dBFS for ambient
- Reserve: -6dB for transients above RMS

### Unity Gain

When adding processing, compensate for volume changes:
- EQ boosts → reduce output
- Compression → makeup gain to match original
- Effects → dry/wet balance to maintain level

## EQ Strategies

### Subtractive EQ (Clean First)

Remove problems before adding character:

```
Common Problem Areas:
80-120Hz:    Mud, rumble (high-pass filter here for non-bass sounds)
200-400Hz:   Boxiness, congestion
2-4kHz:      Harshness, ear fatigue
5-8kHz:      Sibilance, brittleness
```

### Additive EQ (Add Character)

After cleaning, enhance:

```
Enhancement Areas:
60-100Hz:    Weight, power (for bass, impacts)
1-2kHz:      Presence, attack
3-5kHz:      Clarity, cut-through
10kHz+:      Air, openness
```

### Carving Space

Each element needs its own frequency territory:

```
Example Allocation:
Footsteps:   80-200Hz (weight), 2-4kHz (detail)
Weapons:     40-100Hz (boom), 4-8kHz (crack)
UI:          1-4kHz (clear, mid-focused)
Music:       Full range but ducked in action frequencies
Ambience:    Avoid 1-4kHz (leave room for gameplay)
```

## Compression

### Purpose

- Control dynamics (reduce difference between loud and soft)
- Add punch and consistency
- Glue elements together

### Key Parameters

**Threshold**: Level at which compression begins
**Ratio**: How much compression (2:1 gentle, 8:1+ limiting)
**Attack**: How fast compression engages (fast = controlled, slow = punchy)
**Release**: How fast compression releases (auto or tempo-matched)
**Makeup Gain**: Compensate for volume reduction

### Game Audio Settings

**Player Actions (punchy)**
```
Ratio: 4:1
Attack: 10-30ms (let transient through)
Release: 100-200ms
```

**Ambient (smooth)**
```
Ratio: 2:1
Attack: 50-100ms
Release: 300-500ms
```

**Music (glue)**
```
Ratio: 2:1 - 3:1
Attack: 20-50ms
Release: Auto or 250ms
```

## Reverb and Space

### Creating Cohesive Space

All sounds should share believable acoustics:

1. **Define the space**: Interior, exterior, abstract
2. **Set room size**: Small, medium, large, infinite
3. **Choose character**: Bright, dark, neutral
4. **Determine wetness**: Dry (close), wet (far/reflective)

### Reverb Categories

**Convolution Reverb**
- Realistic, based on real space recordings
- CPU-intensive
- Good for: realistic environments

**Algorithmic Reverb**
- Flexible, adjustable parameters
- More efficient
- Good for: stylized or abstract spaces

### Per-Category Reverb

```
Player Sounds:    Short, dry (immediate, close)
Enemy Sounds:     Medium, matches environment
Music:            Matched to game world or separate (non-diegetic)
Ambience:         Baked into ambience, minimal added
UI:               None or minimal (non-spatial)
```

## Dynamics Processing

### Ducking

Lower one sound when another plays:

**Music Ducking**
- Trigger: Dialogue, important SFX
- Amount: -6 to -12dB
- Attack: 50-100ms
- Release: 500-1000ms

**Ambient Ducking**
- Trigger: Player actions, threats
- Amount: -3 to -6dB
- Attack: 20-50ms
- Release: 200-400ms

### Sidechaining

Use one signal to control another's dynamics:

**Combat Sidechain**
- Music sidechained to combat SFX
- Pumping effect can add energy
- Match release to music tempo

### Limiting

Prevent clipping and control peaks:

- Master limiter at -1dBFS ceiling
- Per-bus limiting for category control
- Transparent limiting (fast attack/release)

## Spatialization

### 2D vs 3D Sounds

**2D (Non-positional)**
- UI feedback
- Non-diegetic music
- Player grunts/vocalizations
- Critical gameplay cues

**3D (Positional)**
- Enemy sounds
- Environmental SFX
- Diegetic music sources
- Collectibles/interactables

### Distance Attenuation

```
Curves:
Linear:      Even falloff, less natural
Logarithmic: Natural falloff, human perception
Custom:      Game-specific (e.g., stealth games need long range)

Typical Ranges:
Footsteps:   5-20 meters
Weapons:     10-50 meters
Explosions:  20-100 meters
Ambience:    May not attenuate (environmental)
```

### Occlusion/Obstruction

**Occlusion** (through walls)
- Low-pass filter
- Volume reduction
- Reverb increase

**Obstruction** (around corners)
- Less filtering
- Delay/early reflections
- Direction diffusion

## Mastering for Games

### Platform Targets

**PC/Console**
- Full dynamic range possible
- High-quality audio support
- -14 LUFS integrated recommended

**Mobile**
- Compressed dynamics (noisy environments)
- Limited frequency response
- -12 LUFS integrated recommended

### Loudness Standards

```
Streaming/Broadcast: -14 LUFS
Game Average:        -16 to -14 LUFS
Peaks:               -1 to -3 dBTP
```

### Final Chain

```
1. Bus Compression (glue)
2. Bus EQ (tonal balance)
3. Stereo Enhancement (width)
4. Limiter (peak control)
5. Meter (verification)
```

## Mixing Workflow

### 1. Reference Check
- Compare to reference games/mixes
- Match overall tonality and loudness
- Note frequency balance differences

### 2. Foundation Mix
- Set levels for main elements
- Establish frequency territories
- Create basic spatial placement

### 3. Detail Pass
- Add compression and dynamics
- Fine-tune EQ
- Add reverb and space

### 4. Integration Test
- Play the game
- Note what's too loud/quiet
- Check clarity during action

### 5. Polish
- Address integration issues
- Refine transitions
- Final limiting and loudness
