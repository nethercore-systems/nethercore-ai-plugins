# Audio State Machines

Patterns for managing audio based on game state.

## Basic State Machine

```rust
enum AudioState {
    Menu,
    Exploration,
    Combat,
    Stealth,
    Cutscene,
    Paused,
    GameOver,
}

struct AudioStateConfig {
    music_volume: f32,
    sfx_volume: f32,
    ambient_volume: f32,
    active_music_layer: u32,
    reverb_override: Option<ReverbType>,
    ducking_profile: DuckingProfile,
}
```

---

## State Configurations

| State | Music | SFX | Ambient | Special |
|-------|-------|-----|---------|---------|
| Menu | 100% | 50% | 0% | No 3D audio |
| Exploration | 80% | 100% | 100% | Full soundscape |
| Combat | 100% | 110% | 50% | Aggressive ducking |
| Stealth | 60% | 120% | 80% | Heightened awareness |
| Cutscene | 100% | 80% | 60% | Dialogue priority |
| Paused | 30% | 0% | 0% | Low-pass filter |
| GameOver | 50% | 50% | 30% | Muted, somber |

---

## State Transitions

```rust
struct AudioStateManager {
    current_state: AudioState,
    target_state: AudioState,
    transition_progress: f32,
    transition_duration: f32,
}

impl AudioStateManager {
    fn transition_to(&mut self, new_state: AudioState, duration: f32) {
        self.target_state = new_state;
        self.transition_duration = duration;
        self.transition_progress = 0.0;
    }

    fn update(&mut self, delta: f32) {
        if self.current_state == self.target_state {
            return;
        }

        self.transition_progress += delta / self.transition_duration;

        if self.transition_progress >= 1.0 {
            self.current_state = self.target_state;
            self.transition_progress = 1.0;
        }

        // Apply interpolated config
        let current_config = get_config(self.current_state);
        let target_config = get_config(self.target_state);
        let blended = lerp_config(current_config, target_config, self.transition_progress);
        apply_config(blended);
    }
}
```

---

## Transition Durations

| From | To | Duration | Notes |
|------|-----|----------|-------|
| Any | Combat | 0.5s | Fast, urgent |
| Combat | Exploration | 2s | Slow cooldown |
| Any | Paused | 0.3s | Quick fade |
| Paused | Previous | 0.5s | Resume |
| Any | Cutscene | 1s | Smooth |
| Any | Menu | 1s | Standard |
| Any | GameOver | 1.5s | Dramatic |

---

## Combat Intensity System

Sub-states within combat:

```rust
struct CombatAudioState {
    base_state: AudioState,  // Combat
    intensity: f32,          // 0.0 to 1.0
    enemy_count: u32,
    player_health: f32,
    boss_active: bool,
}

impl CombatAudioState {
    fn calculate_intensity(&mut self) {
        let enemy_factor = (self.enemy_count as f32 / 10.0).min(1.0);
        let health_factor = 1.0 - self.player_health;  // Low health = more intense
        let boss_factor = if self.boss_active { 0.3 } else { 0.0 };

        self.intensity = (enemy_factor * 0.4 +
                         health_factor * 0.3 +
                         boss_factor).min(1.0);
    }

    fn apply_to_music(&self, music: &mut AdaptiveMusic) {
        music.set_intensity(self.intensity);

        // Low health = add tension layer
        if self.player_health < 0.3 {
            music.enable_layer("heartbeat");
        }

        // Boss = full power
        if self.boss_active {
            music.enable_all_layers();
        }
    }
}
```

---

## Environment State Blending

For seamless area transitions:

```rust
struct EnvironmentAudio {
    zones: Vec<AudioZone>,
    current_blend: HashMap<ZoneId, f32>,
}

struct AudioZone {
    id: ZoneId,
    bounds: BoundingBox,
    ambient_loop: SoundId,
    reverb_preset: ReverbPreset,
    music_track: Option<MusicId>,
    blend_distance: f32,
}

impl EnvironmentAudio {
    fn update(&mut self, player_pos: Vec3) {
        // Calculate blend weights for all nearby zones
        for zone in &self.zones {
            let distance = zone.bounds.distance_to(player_pos);

            if distance < zone.blend_distance {
                let weight = 1.0 - (distance / zone.blend_distance);
                self.current_blend.insert(zone.id, weight);
            } else if distance < 0.0 {  // Inside zone
                self.current_blend.insert(zone.id, 1.0);
            } else {
                self.current_blend.remove(&zone.id);
            }
        }

        // Normalize weights
        let total: f32 = self.current_blend.values().sum();
        if total > 0.0 {
            for weight in self.current_blend.values_mut() {
                *weight /= total;
            }
        }

        // Apply blended audio
        self.apply_blended_audio();
    }
}
```

---

## State Triggers

Common events that trigger state changes:

```rust
fn handle_game_event(event: GameEvent, audio: &mut AudioStateManager) {
    match event {
        GameEvent::EnemySpotted => {
            if audio.current_state == AudioState::Exploration {
                audio.transition_to(AudioState::Combat, 0.5);
            }
        }
        GameEvent::AllEnemiesDefeated => {
            audio.transition_to(AudioState::Exploration, 2.0);
        }
        GameEvent::CutsceneStarted => {
            audio.transition_to(AudioState::Cutscene, 1.0);
        }
        GameEvent::Paused => {
            audio.transition_to(AudioState::Paused, 0.3);
        }
        GameEvent::Unpaused => {
            audio.transition_to(audio.previous_state, 0.5);
        }
        GameEvent::PlayerDied => {
            audio.transition_to(AudioState::GameOver, 1.5);
        }
        GameEvent::BossEncounterStarted => {
            audio.transition_to(AudioState::Combat, 0.3);
            audio.combat_state.boss_active = true;
        }
    }
}
```
