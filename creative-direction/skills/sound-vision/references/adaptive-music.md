# Adaptive Music for Games

## What is Adaptive Music?

Music that responds to gameplay state, creating a dynamic score that:
- Matches emotional intensity to action
- Transitions smoothly between states
- Enhances player agency
- Never feels repetitive or disconnected

## Adaptive Techniques

### 1. Horizontal Re-sequencing

**Concept**: Playing different musical segments in different orders

**Implementation**:
```
EXPLORATION → ALERT → COMBAT → VICTORY
     ↓          ↓        ↓         ↓
 [seg_A]    [seg_B]  [seg_C]   [seg_D]
```

**Transitions**:
- Quantized: Wait for musical measure to switch
- Immediate: Hard cut on state change
- Crossfade: Blend over 1-4 bars

**Best for**: Clear game states, predictable transitions

### 2. Vertical Remixing (Layering)

**Concept**: Stacking/unstacking instrument layers

**Implementation**:
```
Base Layer:     Always playing (drums, bass)
Layer 2:        Add on light tension (strings)
Layer 3:        Add on combat (brass, percussion)
Layer 4:        Add on boss/climax (full orchestra)
```

**Transitions**:
- Fade individual layers in/out
- Quantize to beat or measure
- Use volume automation

**Best for**: Smooth intensity scaling, immersive transitions

### 3. Transition Segments

**Concept**: Dedicated musical bridges between states

**Implementation**:
```
[Exploration] → [Transition_to_Combat] → [Combat]
                        ↑
              2-4 bar musical bridge
```

**Types**:
- Stingers: Short 1-2 bar hits
- Bridges: 4-8 bar transitions
- Tails: Decay from previous section

**Best for**: Polished feel, avoiding jarring cuts

### 4. Stem-Based Mixing

**Concept**: Real-time control of individual instrument stems

**Implementation**:
```
Stems:
├── Drums
├── Bass
├── Rhythm Section
├── Lead Melody
├── Pads/Strings
└── FX/Textures

Controller:
- Intensity 0-25%:   Drums (soft), Pads
- Intensity 25-50%:  + Bass, Rhythm
- Intensity 50-75%:  + Lead Melody
- Intensity 75-100%: + Full percussion, FX
```

**Best for**: Granular control, dynamic range

### 5. Generative/Procedural

**Concept**: Algorithmic music composition in real-time

**Techniques**:
- Probability-based note selection
- Rule-based harmony
- Tempo and key modulation
- Parameterized generation

**Best for**: Infinite variation, unique soundtracks

## State Machine Design

### Define Musical States

```
States:
├── AMBIENT (peaceful, environmental)
├── EXPLORATION (curious, mysterious)
├── TENSION (rising danger)
├── COMBAT_LIGHT (minor enemies)
├── COMBAT_HEAVY (significant fight)
├── BOSS (epic confrontation)
├── VICTORY (triumph)
├── DEFEAT (somber)
└── MENU/PAUSE (non-diegetic)
```

### Transition Rules

```
AMBIENT → EXPLORATION:     Player moves
EXPLORATION → TENSION:     Enemy spotted
TENSION → COMBAT_LIGHT:    Enemy attacks
COMBAT_LIGHT → AMBIENT:    All enemies dead (delay 5s)
COMBAT_HEAVY → BOSS:       Boss enters
BOSS → VICTORY:            Boss defeated
```

### Transition Timing

**Immediate transitions** (gameplay critical):
- Death → Defeat stinger
- Victory → Victory fanfare

**Musical transitions** (wait for downbeat):
- Exploration → Combat
- Combat → Ambient
- Zone changes

**Crossfade transitions**:
- Intensity changes within state
- Subtle mood shifts

## Energy Curves

### Intensity Mapping

Map gameplay parameters to music intensity (0.0 - 1.0):

```python
def calculate_intensity():
    base = ambient_intensity  # 0.0 - 0.2

    if enemies_nearby:
        base += 0.2

    if in_combat:
        base += 0.3 * (1 - player_health_percent)
        base += 0.1 * enemy_count

    if boss_fight:
        base += 0.4

    return clamp(base, 0.0, 1.0)
```

### Hysteresis

Prevent rapid state flickering:

```
Enter Combat:  Threat level > 0.6 for 1 second
Exit Combat:   Threat level < 0.2 for 5 seconds
```

### Cool-down Periods

After high-intensity events, enforce musical rest:
- Post-combat: 10-30 seconds of ambient before next combat music
- Boss defeat: Extended victory music before ambient
- Death: Somber music with pause before respawn

## Practical Implementation

### Middleware Integration

Popular adaptive music tools:
- **Wwise**: Event-based, state machines, RTPCs
- **FMOD**: Horizontal/vertical mixing, parameters
- **Custom**: Direct integration with game engine

### RTPC (Real-Time Parameter Control)

Map game values to music parameters:

```
Game Parameter    →    Music Parameter
───────────────────────────────────────
Health (0-100)    →    Tension (100-0)
Speed (0-max)     →    Tempo multiplier
Enemy distance    →    Threat intensity
Time of day       →    Key/mode shift
```

### Cue Points

Define synchronization points in music:

```
CUE_MEASURE_START:  Safe transition point
CUE_BEAT:           Quick transition point
CUE_BREAKDOWN:      Intense section marker
CUE_BUILDUP:        Tension rising marker
```

### Memory and Streaming

**Considerations**:
- Keep base layers in memory
- Stream additional layers as needed
- Pre-load transition segments
- Unload unused music zones

## ZX-Specific Adaptive Music

For Nethercore ZX's 4-channel limit:

### Channel Allocation

```
Channel 1: Bass/Drums (always)
Channel 2: Melody/Lead (exploration+)
Channel 3: Harmony/Pad (combat intensity)
Channel 4: SFX reserved OR texture layer
```

### Simplified States

```
States (3-4 max):
├── CALM (2 channels)
├── ACTIVE (3 channels)
└── INTENSE (4 channels, music dominates)
```

### Quick Transitions

With limited polyphony, prefer:
- Hard cuts on measure boundaries
- Short crossfades (1-2 beats)
- Stingers over long transitions

## Mixing for Adaptive

### Separation by State

**Quiet States**:
- Music louder, more detailed
- Full frequency range
- More spatial width

**Loud States**:
- Music supports, doesn't compete
- Mid-frequency focus
- Narrower stereo (leave room for SFX)

### Automation Presets

Per-state mixing presets:

```
EXPLORATION:
  music_volume: -6dB
  music_lowpass: OFF
  sfx_ducking: light

COMBAT:
  music_volume: -12dB
  music_lowpass: 8kHz (subtle)
  sfx_ducking: heavy
```

## Testing Adaptive Music

### Playthrough Testing

1. Play through full game path
2. Note every music transition
3. Check for jarring moments
4. Verify state machine accuracy

### Edge Cases

- Rapid state changes (flickering)
- Long gameplay in single state (repetition)
- Unexpected player behavior
- Multiple simultaneous triggers

### Metrics to Track

- Time in each state
- Transition frequency
- Audio memory usage
- CPU overhead
