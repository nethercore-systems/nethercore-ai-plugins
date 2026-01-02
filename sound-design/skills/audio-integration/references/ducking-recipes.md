# Ducking Recipes

Sidechain ducking configurations for common scenarios.

## Core Configuration

```rust
struct DuckingConfig {
    trigger_bus: Bus,      // What triggers ducking
    target_bus: Bus,       // What gets ducked
    threshold: f32,        // Trigger level (dB)
    duck_amount: f32,      // Reduction amount (dB)
    attack_ms: f32,        // How fast to duck
    release_ms: f32,       // How fast to recover
    hold_ms: f32,          // Hold before release
}
```

---

## Voice Ducks Music

Most important ducking relationship - ensure dialogue is always clear.

```rust
let voice_ducks_music = DuckingConfig {
    trigger_bus: Bus::Voice,
    target_bus: Bus::Music,
    threshold: -30.0,      // Trigger when voice > -30dB
    duck_amount: -9.0,     // Reduce music by 9dB
    attack_ms: 20.0,       // Fast duck
    release_ms: 400.0,     // Slow recovery
    hold_ms: 100.0,        // Hold briefly after voice stops
};
```

**Tuning tips:**
- More duck (-12dB) for action games with loud music
- Less duck (-6dB) for narrative games with quieter music
- Longer release for natural feel

---

## SFX Ducks Music

Keep gameplay sounds audible over music.

```rust
let sfx_ducks_music = DuckingConfig {
    trigger_bus: Bus::SFX,
    target_bus: Bus::Music,
    threshold: -20.0,      // Duck when SFX > -20dB
    duck_amount: -4.0,     // Reduce music by 4dB
    attack_ms: 10.0,       // Very fast
    release_ms: 300.0,     // Medium recovery
    hold_ms: 50.0,
};
```

**Notes:**
- Subtle ducking - music should still be present
- Fast attack for transient sounds
- May want different amounts for different SFX categories

---

## Critical Ducks All

Emergency sounds must cut through everything.

```rust
let critical_ducks_all = DuckingConfig {
    trigger_bus: Bus::Critical,
    target_bus: Bus::Master,  // Or create "duckable" bus
    threshold: -40.0,         // Very sensitive
    duck_amount: -12.0,       // Aggressive duck
    attack_ms: 5.0,           // Instant
    release_ms: 500.0,        // Slow recovery
    hold_ms: 200.0,
};
```

**Use for:**
- Player damage indicators
- Low health warnings
- Critical game events

---

## Pause Ducks Music

Fade music when pausing.

```rust
let pause_ducks_music = DuckingConfig {
    trigger_bus: Bus::PauseState,  // State-based, not audio
    target_bus: Bus::Music,
    threshold: 0.0,           // Trigger on state
    duck_amount: -20.0,       // Nearly mute
    attack_ms: 500.0,         // Slow fade
    release_ms: 1000.0,       // Slow return
    hold_ms: 0.0,
};
```

---

## Combat Intensity

Increase music volume during combat (inverse ducking).

```rust
fn apply_combat_boost(combat_intensity: f32, music_bus: &mut Bus) {
    // 0.0 = no combat, 1.0 = max combat
    let boost_db = combat_intensity * 3.0;  // Up to +3dB
    music_bus.volume = base_volume + boost_db;

    // Also reduce ambient
    let ambient_duck = combat_intensity * -6.0;  // Down to -6dB
    ambient_bus.volume = base_volume + ambient_duck;
}
```

---

## Multi-Stage Ducking

Different amounts based on trigger intensity:

```rust
fn calculate_duck(trigger_level: f32, config: &DuckingConfig) -> f32 {
    if trigger_level < config.threshold {
        return 0.0;  // No ducking
    }

    // Calculate how far above threshold
    let above = trigger_level - config.threshold;
    let duck_ratio = (above / 20.0).min(1.0);  // 20dB range

    // Apply ducking amount proportionally
    config.duck_amount * duck_ratio
}
```

---

## Ducking Matrix

Quick reference for all relationships:

| Trigger | Target | Amount | Attack | Release |
|---------|--------|--------|--------|---------|
| Voice | Music | -9dB | 20ms | 400ms |
| Voice | SFX | -3dB | 20ms | 200ms |
| SFX | Music | -4dB | 10ms | 300ms |
| Critical | All | -12dB | 5ms | 500ms |
| Combat | Ambient | -6dB | 100ms | 500ms |
| Pause | Music | -20dB | 500ms | 1000ms |
| Menu | Gameplay | -∞ | 200ms | 500ms |

---

## Implementation Pattern

```rust
struct DuckingSystem {
    configs: Vec<DuckingConfig>,
    current_ducks: HashMap<Bus, f32>,
}

impl DuckingSystem {
    fn update(&mut self, bus_levels: &HashMap<Bus, f32>) {
        for config in &self.configs {
            let trigger_level = bus_levels.get(&config.trigger_bus).unwrap_or(&-100.0);

            if *trigger_level > config.threshold {
                // Apply duck with smoothing
                let target = config.duck_amount;
                let current = self.current_ducks.entry(config.target_bus).or_insert(0.0);
                *current = lerp(*current, target, config.attack_ms / 1000.0);
            } else {
                // Release duck
                let current = self.current_ducks.entry(config.target_bus).or_insert(0.0);
                *current = lerp(*current, 0.0, config.release_ms / 1000.0);
            }
        }
    }
}
```
