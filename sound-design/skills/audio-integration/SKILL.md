---
name: Audio Integration
description: This skill should be used when the user asks about "audio mixing", "game audio mixing", "ducking", "sidechain", "audio priority", "mix priority", "spatial audio", "3D audio", "audio occlusion", "reverb zones", "audio bus", "master bus", "audio categories", "dynamic range", "compression for games", "loudness", "audio middleware", or wants to understand how to integrate and mix audio within a game. Provides patterns for audio system design and mixing.
version: 1.0.0
---

# Audio Integration

How audio elements work together in a game: mixing, prioritization, spatial positioning, and dynamic systems.

## Mix Architecture

### Bus Structure

Organize sounds into buses for group control:

```
                        ┌─────────────┐
                        │ Master Bus  │
                        └──────┬──────┘
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  Music   │    │   SFX    │    │  Voice   │
        └────┬─────┘    └────┬─────┘    └──────────┘
             │               │
    ┌────────┴───────┐   ┌──┴───┬─────────┐
    ▼                ▼   ▼      ▼         ▼
┌────────┐    ┌─────────┐ ┌─────┐ ┌─────┐ ┌─────────┐
│Ambient │    │Combat   │ │ UI  │ │World│ │Creatures│
│Music   │    │Music    │ └─────┘ └─────┘ └─────────┘
└────────┘    └─────────┘
```

### Bus Purposes

| Bus | Contents | Processing |
|-----|----------|------------|
| **Master** | Everything | Final limiter, loudness |
| **Music** | All music | Ducking input, reverb send |
| **SFX** | All sound effects | Compression, limiting |
| **Voice** | Dialogue, VO | De-esser, compression |
| **UI** | Interface sounds | Dry, consistent level |
| **World** | 3D positioned sounds | Spatial processing |
| **Ambient** | Loops, atmosphere | Low priority ducking |

---

## Mix Priorities

Not all sounds are equal. Define priorities:

### Priority Levels

```
Priority 1: CRITICAL (always audible)
  - Player damage feedback
  - Death sounds
  - Critical alerts

Priority 2: HIGH
  - Player actions (jump, attack)
  - Dialogue
  - Important pickups

Priority 3: MEDIUM
  - Enemy sounds
  - Weapon impacts
  - Music

Priority 4: LOW
  - Ambient details
  - Distant sounds
  - Non-essential SFX

Priority 5: BACKGROUND
  - Environmental loops
  - Crowd sounds
  - Atmospheric layers
```

### Voice/Channel Limiting

When too many sounds play, steal from lower priorities:

```rust
struct AudioChannel {
    priority: u8,
    volume: f32,
    age: f32,  // Time since started
    sound_id: u32,
}

fn steal_channel(channels: &mut [AudioChannel], new_priority: u8) -> Option<usize> {
    // Find lowest priority, oldest sound
    channels.iter()
        .enumerate()
        .filter(|(_, c)| c.priority <= new_priority)
        .max_by(|(_, a), (_, b)| {
            // Prefer lower priority, then older
            (a.priority, a.age).cmp(&(b.priority, b.age))
        })
        .map(|(i, _)| i)
}
```

---

## Ducking and Sidechaining

Lower some sounds when others play.

### Music Ducking

Reduce music when important sounds occur:

```rust
struct DuckingConfig {
    trigger_bus: Bus,      // What triggers ducking
    target_bus: Bus,       // What gets ducked
    threshold: f32,        // Trigger level
    duck_amount: f32,      // How much to reduce (dB)
    attack_ms: f32,        // How fast to duck
    release_ms: f32,       // How fast to recover
}

// Example: Duck music when SFX plays
let sfx_ducks_music = DuckingConfig {
    trigger_bus: Bus::SFX,
    target_bus: Bus::Music,
    threshold: -20.0,      // Duck when SFX > -20dB
    duck_amount: -6.0,     // Reduce music by 6dB
    attack_ms: 10.0,       // Fast duck
    release_ms: 500.0,     // Slow recovery
};
```

### Common Ducking Relationships

| Trigger | Target | Amount | Purpose |
|---------|--------|--------|---------|
| Voice | Music | -6 to -12dB | Hear dialogue |
| SFX | Music | -3 to -6dB | Hear actions |
| Critical | All | -6dB | Emergency alerts |
| Pause | Music | -∞ (mute) | Pause menu |

---

## Spatial Audio

Positioning sounds in 3D space.

### Distance Attenuation

```rust
fn calculate_volume(distance: f32, config: &AttenuationConfig) -> f32 {
    if distance <= config.min_distance {
        1.0
    } else if distance >= config.max_distance {
        0.0
    } else {
        // Various falloff curves:
        match config.curve {
            Linear => {
                1.0 - (distance - config.min_distance) /
                      (config.max_distance - config.min_distance)
            }
            Logarithmic => {
                let t = (distance - config.min_distance) /
                        (config.max_distance - config.min_distance);
                1.0 - t.log10() / 0.0_f32.log10() // Adjust curve
            }
            Inverse => {
                config.min_distance / distance
            }
        }
    }
}
```

### Attenuation Presets

| Sound Type | Min Dist | Max Dist | Curve |
|------------|----------|----------|-------|
| Voice | 1m | 15m | Linear |
| Footsteps | 0.5m | 20m | Inverse |
| Gunshots | 5m | 200m | Logarithmic |
| Ambient point | 2m | 50m | Linear |
| UI | N/A | N/A | 2D |

### Panning

```rust
fn calculate_pan(listener_pos: Vec3, listener_forward: Vec3,
                 sound_pos: Vec3) -> f32 {
    let to_sound = (sound_pos - listener_pos).normalize();
    let listener_right = listener_forward.cross(Vec3::UP);

    // -1 = full left, 0 = center, 1 = full right
    to_sound.dot(listener_right)
}
```

### Occlusion

Reduce high frequencies when sounds are blocked:

```rust
fn apply_occlusion(sound: &mut Sound, occlusion: f32) {
    // Occlusion: 0.0 = clear, 1.0 = fully blocked

    // Reduce volume
    sound.volume *= 1.0 - (occlusion * 0.5);

    // Apply low-pass filter (blocked sounds are muffled)
    let cutoff = lerp(20000.0, 500.0, occlusion);
    sound.lowpass_cutoff = cutoff;
}
```

---

## Reverb and Acoustics

Environmental audio treatment.

### Reverb Zones

Define acoustic spaces:

```rust
struct ReverbZone {
    bounds: BoundingBox,
    reverb_type: ReverbType,
    wet_level: f32,
    decay_time: f32,
    early_reflections: f32,
}

enum ReverbType {
    Room,       // Small indoor
    Hall,       // Large indoor
    Cathedral,  // Massive indoor
    Outdoor,    // Open air
    Cave,       // Reflective
    Custom,
}
```

### Reverb Parameters by Space

| Space | Decay | Early Ref | Wet Level |
|-------|-------|-----------|-----------|
| Small room | 0.3-0.8s | High | 20-40% |
| Large hall | 1.5-3s | Medium | 30-50% |
| Cathedral | 4-8s | Low | 40-60% |
| Outdoor | 0.1-0.3s | Very low | 10-20% |
| Cave | 2-5s | High | 50-70% |
| Bathroom | 0.5-1s | Very high | 40-60% |

### Reverb Send Architecture

```
Sound Source → Dry Path → Mix
      │
      └──────→ Reverb Bus → Mix

Adjust reverb send per sound type:
- Dialogue: Low reverb (clarity)
- Footsteps: Match environment
- Impacts: Medium reverb
- Music: Baked-in reverb
```

---

## Dynamic Range

Managing volume differences.

### Compression for Games

Different from music production:

| Context | Ratio | Attack | Release | Purpose |
|---------|-------|--------|---------|---------|
| Dialogue | 3:1 | 10ms | 200ms | Consistent level |
| SFX Bus | 2:1 | 1ms | 100ms | Punch, control |
| Music | 2:1 | 10ms | 300ms | Gentle control |
| Master | 4:1 | 5ms | 200ms | Peak limiting |

### Loudness Standards

| Platform | Target | True Peak |
|----------|--------|-----------|
| PC | -14 LUFS | -1 dBTP |
| Console | -14 to -16 LUFS | -1 dBTP |
| Mobile | -16 LUFS | -1 dBTP |
| Streaming | -14 LUFS | -2 dBTP |

### Dynamic Range Per Category

```
Music:        12-16 dB (allow dynamics)
SFX:          8-12 dB (consistent impact)
Dialogue:     6-8 dB (always clear)
UI:           4-6 dB (predictable)
Ambient:      10-14 dB (natural)
```

---

## Audio States

Change audio based on game state.

### State Machine

```rust
enum AudioState {
    Menu,
    Exploration,
    Combat,
    Stealth,
    Cutscene,
    Paused,
}

struct AudioStateConfig {
    music_volume: f32,
    sfx_volume: f32,
    ambient_volume: f32,
    active_music_layer: u32,
    reverb_override: Option<ReverbType>,
    ducking_profile: DuckingProfile,
}

fn transition_state(current: AudioState, target: AudioState,
                    duration: f32) {
    let current_config = get_config(current);
    let target_config = get_config(target);

    // Crossfade between configs
    start_crossfade(current_config, target_config, duration);
}
```

### State Configurations

| State | Music | SFX | Ambient | Notes |
|-------|-------|-----|---------|-------|
| Menu | 100% | 50% | 0% | Focus on music |
| Exploration | 80% | 100% | 100% | Full soundscape |
| Combat | 100% | 110% | 50% | SFX priority |
| Stealth | 60% | 120% | 80% | Heightened awareness |
| Cutscene | 100% | 80% | 60% | Dialogue priority |
| Paused | 30% | 0% | 0% | Minimal |

---

## Real-Time Audio Control

Expose audio to gameplay systems.

### Parameter System

```rust
struct AudioParameter {
    name: String,
    value: f32,           // Current
    target: f32,          // Target
    smoothing_ms: f32,    // Interpolation time
}

// Gameplay-driven parameters
let player_health = AudioParameter::new("player_health", 1.0, 50.0);
let tension_level = AudioParameter::new("tension", 0.0, 100.0);
let environment_type = AudioParameter::new("environment", 0.0, 10.0);

// Music responds to parameters
fn update_music(music: &mut AdaptiveMusic, params: &AudioParams) {
    let health = params.get("player_health");

    // Low health = more tense music
    if health < 0.3 {
        music.enable_layer("tension_layer");
        music.set_filter_cutoff(2000.0 + health * 6000.0);
    }
}
```

### Common Parameter Mappings

| Parameter | Controls |
|-----------|----------|
| Health | Music tension, heartbeat layer |
| Combat intensity | Music layers, enemy count |
| Speed | Whoosh intensity, wind |
| Altitude | Wind intensity, atmosphere |
| Time of day | Ambient layers, reverb |
| Environment | Reverb type, ambient loops |

---

## Performance Optimization

Audio uses CPU and memory.

### CPU Management

```rust
// Voice pooling
const MAX_VOICES: usize = 32;

// Update rates
const FULL_UPDATE_HZ: f32 = 60.0;    // Critical sounds
const REDUCED_UPDATE_HZ: f32 = 20.0;  // Background sounds

// LOD for audio
fn update_sound(sound: &mut Sound, distance: f32) {
    if distance < 10.0 {
        // Full quality
        sound.update_rate = FULL_UPDATE_HZ;
        sound.interpolation = Interpolation::Cubic;
    } else if distance < 50.0 {
        // Reduced
        sound.update_rate = REDUCED_UPDATE_HZ;
        sound.interpolation = Interpolation::Linear;
    } else {
        // Minimal
        sound.update_rate = 10.0;
        sound.interpolation = Interpolation::None;
    }
}
```

### Memory Management

```rust
// Streaming vs. resident
enum LoadType {
    Resident,   // < 500KB, frequently used
    Streaming,  // > 500KB, music, long ambient
    OnDemand,   // Rare sounds, load when needed
}

// Bank loading
struct AudioBank {
    name: String,
    sounds: Vec<SoundId>,
    memory_size: usize,
    load_state: LoadState,
}

fn preload_for_level(level: &Level) {
    let required_banks = level.get_audio_banks();
    for bank in required_banks {
        audio_system.load_bank(bank);
    }
}
```

---

## Testing Audio

### Checklist

- [ ] All sounds play without errors
- [ ] No clipping at master bus
- [ ] Priorities work correctly (try spawning 100 sounds)
- [ ] Ducking sounds natural
- [ ] Spatial audio pans correctly
- [ ] Reverb transitions smoothly
- [ ] Performance stays within budget
- [ ] Memory doesn't leak
- [ ] State transitions work

### Debug Tools

```rust
// Audio debug display
fn draw_audio_debug(ctx: &mut DrawContext) {
    // Show active voices
    draw_text(&format!("Voices: {}/{}", active_voices, MAX_VOICES));

    // Show bus levels
    for bus in &audio_buses {
        draw_meter(bus.name, bus.peak_level);
    }

    // Show 3D sound positions
    for sound in &active_3d_sounds {
        draw_world_icon(sound.position, "speaker");
    }
}
```

---

## Additional Resources

- `references/bus-templates.md` - Common bus configurations
- `references/ducking-recipes.md` - Ducking setups
- `references/platform-specs.md` - Platform audio limitations
