# Adaptive Music Patterns

Implementation patterns for music that responds to gameplay.

## Vertical Layering

Stack musical layers that can be added/removed based on intensity:

### Combat Intensity Example

```
Level 0 (Exploration):
  - Ambient pad only

Level 1 (Alert):
  + Subtle percussion
  + Bass drone

Level 2 (Combat):
  + Full drums
  + Bass line
  + Tension strings

Level 3 (Boss):
  + Brass fanfares
  + Choir
  + Maximum intensity
```

### Implementation Pattern

```rust
struct AdaptiveMusic {
    layers: Vec<AudioLayer>,
    current_intensity: f32,  // 0.0 to 1.0
}

impl AdaptiveMusic {
    fn set_intensity(&mut self, intensity: f32) {
        for (i, layer) in self.layers.iter_mut().enumerate() {
            let threshold = i as f32 / self.layers.len() as f32;
            layer.target_volume = if intensity >= threshold { 1.0 } else { 0.0 };
        }
    }

    fn update(&mut self, delta: f32) {
        for layer in &mut self.layers {
            // Smooth crossfade
            layer.volume = lerp(layer.volume, layer.target_volume, delta * 2.0);
        }
    }
}
```

### Layer Design Guidelines

| Layer | Content | Threshold | Fade Time |
|-------|---------|-----------|-----------|
| Base | Pad/drone | 0.0 | Always on |
| Rhythm | Light percussion | 0.2 | 1-2s |
| Bass | Bass line | 0.3 | 1s |
| Melody | Main theme | 0.5 | 2s |
| Intensity | Power elements | 0.7 | 1s |
| Maximum | Everything | 0.9 | 1s |

---

## Horizontal Resequencing

Play different sections based on game state:

### Section Pool Design

```
Explore_A, Explore_B, Explore_C  (random calm)
Tension_A, Tension_B             (random tense)
Combat_A, Combat_B               (random combat)
Victory                          (play on win)
```

### Transition Matrix

```
         To:
From:    Explore  Tension  Combat  Victory
Explore    ✓         ✓        ✓       -
Tension    ✓         ✓        ✓       -
Combat     -         ✓        ✓       ✓
Victory    ✓         -        -       -
```

### Implementation Pattern

```rust
struct MusicSection {
    name: String,
    bars: u32,
    intensity: f32,
    can_transition_to: Vec<String>,
}

fn select_next_section(current: &str, game_state: GameState) -> String {
    let valid_sections: Vec<_> = sections.iter()
        .filter(|s| current_section.can_transition_to.contains(&s.name))
        .filter(|s| s.intensity_matches(game_state))
        .collect();

    valid_sections.choose_random()
}
```

**Transition timing:** Always at phrase boundaries (every 4 or 8 bars)

---

## Stinger System

Short musical phrases for events:

| Event | Type | Length | Notes |
|-------|------|--------|-------|
| Item pickup | Rising arpeggio | 0.5-1s | Major key |
| Secret found | Mysterious phrase | 1-2s | Suspended chord |
| Enemy alert | Tense hit | 0.5s | Dissonant stab |
| Boss appear | Dramatic fanfare | 2-4s | Minor, powerful |
| Death | Descending phrase | 1-2s | Minor resolution |
| Level complete | Victory fanfare | 3-5s | Major, triumphant |

**Design rules:**
- Work over any current music
- Avoid strong harmonic content (clash risk)
- Be recognizable but short

---

## Parameter-Driven Music

Map gameplay values to musical parameters:

| Gameplay Value | Musical Control | Range |
|----------------|-----------------|-------|
| Player health | Filter cutoff, layer intensity | Low health = darker |
| Combat heat | Percussion layers, tempo feel | More enemies = more intense |
| Speed/velocity | Whoosh layers, tremolo | Faster = more movement |
| Altitude | Wind layers, reverb | Higher = more atmospheric |
| Time of day | Key brightness, instrument choice | Night = darker keys |
| Environment | Reverb type, ambient layers | Match space |

### Health-Driven Example

```rust
fn update_music_for_health(music: &mut AdaptiveMusic, health: f32) {
    // Low health = more tense
    if health < 0.3 {
        music.enable_layer("tension_layer");
        music.enable_layer("heartbeat");
        music.set_filter_cutoff(2000.0 + health * 6000.0);
    } else {
        music.disable_layer("tension_layer");
        music.disable_layer("heartbeat");
        music.set_filter_cutoff(20000.0);
    }
}
```

---

## Crossfade Techniques

| Transition | Duration | Use For |
|------------|----------|---------|
| Hard cut | 0ms | Dramatic moments |
| Quick fade | 100-500ms | Combat starts |
| Medium fade | 1-2s | State changes |
| Long fade | 3-5s | Ambient transitions |
| Beat-synced | 1-4 bars | Musical transitions |
