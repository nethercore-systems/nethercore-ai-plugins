---
name: Game Feel & Polish
description: This skill should be used when the user asks about "game feel", "juice", "polish", "screen shake", "camera shake", "hit pause", "freeze frame", "hitstop", "particles", "impact", "feedback", "responsiveness", "weight", "crunch", "satisfying", "punchy", or discusses making gameplay feel more impactful and responsive in Nethercore ZX games.
version: 1.0.0
---

# Game Feel & Polish for Nethercore ZX

Game feel ("juice") transforms functional mechanics into satisfying experiences. This skill covers techniques to add impact, weight, and responsiveness using ZX FFI functions. All code MUST be deterministic for rollback netcode compatibility.

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Exaggeration** | Screen shake, scale bounces, speed lines |
| **Anticipation** | Wind-up animations, audio cues before action |
| **Follow-through** | Lingering effects after action ends |
| **Immediate feedback** | Visual + audio response within 1-2 frames |

---

## Screen Shake

Apply camera offset to convey impact. Use `camera_set()` with added shake offset.

### Basic Screen Shake

```rust
struct ScreenShake {
    intensity: f32,
    duration: u32,
    remaining: u32,
}

impl ScreenShake {
    fn trigger(&mut self, intensity: f32, duration: u32) {
        self.intensity = intensity;
        self.duration = duration;
        self.remaining = duration;
    }

    fn update(&mut self) -> (f32, f32) {
        if self.remaining == 0 {
            return (0.0, 0.0);
        }

        // Decay intensity over time
        let t = self.remaining as f32 / self.duration as f32;
        let current_intensity = self.intensity * t;

        // Use deterministic random for shake offset
        let offset_x = (random() * 2.0 - 1.0) * current_intensity;
        let offset_y = (random() * 2.0 - 1.0) * current_intensity;

        self.remaining -= 1;
        (offset_x, offset_y)
    }
}

fn apply_camera_with_shake(base_x: f32, base_y: f32, base_z: f32,
                           target_x: f32, target_y: f32, target_z: f32,
                           shake: &ScreenShake) {
    let (shake_x, shake_y) = shake.update();
    unsafe {
        camera_set(
            base_x + shake_x,
            base_y + shake_y,
            base_z,
            target_x + shake_x,
            target_y + shake_y,
            target_z
        );
    }
}
```

### Directional Shake

For impacts with a clear direction (punches, explosions):

```rust
fn directional_shake(intensity: f32, direction_x: f32, direction_y: f32) -> (f32, f32) {
    // Shake primarily along impact direction
    let main = intensity * 0.8;
    let side = intensity * 0.3 * (random() * 2.0 - 1.0);

    // Normalize direction
    let len = (direction_x * direction_x + direction_y * direction_y).sqrt();
    let dx = if len > 0.0 { direction_x / len } else { 1.0 };
    let dy = if len > 0.0 { direction_y / len } else { 0.0 };

    // Perpendicular direction
    let px = -dy;
    let py = dx;

    (dx * main + px * side, dy * main + py * side)
}
```

### Shake Intensity Guidelines

| Event | Intensity | Duration (ticks) |
|-------|-----------|------------------|
| Light hit | 2-4 px | 4-6 |
| Heavy hit | 6-10 px | 8-12 |
| Explosion | 12-20 px | 15-25 |
| Boss attack | 15-25 px | 20-30 |
| Death | 20-30 px | 30-45 |

---

## Hit Pause (Freeze Frames)

Momentary freeze on impact adds weight and allows the player to register hits.

### Basic Hit Pause

```rust
struct HitPause {
    remaining: u32,
}

impl HitPause {
    fn trigger(&mut self, frames: u32) {
        self.remaining = self.remaining.max(frames);
    }

    fn is_paused(&self) -> bool {
        self.remaining > 0
    }

    fn update(&mut self) {
        if self.remaining > 0 {
            self.remaining -= 1;
        }
    }
}

fn update(game: &mut Game) {
    game.hit_pause.update();

    if game.hit_pause.is_paused() {
        // Skip gameplay updates during pause
        // Still allow visual effects and input buffering
        return;
    }

    // Normal gameplay update
    update_physics(game);
    update_entities(game);
}

fn render(game: &Game) {
    // Always render, even during hit pause
    render_gameplay(game);

    // Optional: flash effect during hit pause
    if game.hit_pause.is_paused() {
        draw_rect(0.0, 0.0, 960.0, 540.0, 0xFFFFFF20);
    }
}
```

### Asymmetric Hit Pause

Freeze the attacker longer than the victim for rhythmic combat:

```rust
fn apply_hit(attacker: &mut Entity, victim: &mut Entity, game: &mut Game) {
    // Victim takes damage
    victim.health -= attacker.attack_damage;
    victim.hitstun = 20;

    // Attacker freezes slightly longer for emphasis
    attacker.freeze_frames = 5;
    victim.freeze_frames = 3;

    // Global hit pause
    game.hit_pause.trigger(3);

    // Effects
    game.screen_shake.trigger(8.0, 6);
    play_sound(game.hit_sound, 1.0, 0.0);
}
```

### Hit Pause Duration Guidelines

| Action | Pause (frames) |
|--------|----------------|
| Light attack | 2-3 |
| Medium attack | 4-5 |
| Heavy attack | 6-8 |
| Critical hit | 10-15 |
| Super move | 15-25 |

---

## Sound-Visual Synchronization

Align audio with visual feedback for maximum impact.

### Impact Timing

```rust
fn on_attack_hit(game: &mut Game, hit_pos: [f32; 3], damage: u32) {
    // Frame 0: Everything happens together
    play_sound(game.hit_sound, 1.0, 0.0);     // Audio
    spawn_hit_particles(game, hit_pos);        // Visual
    game.screen_shake.trigger(damage as f32 * 0.5, 6);  // Camera
    game.hit_pause.trigger(3);                 // Freeze

    // Frame 1+: Secondary effects
    game.pending_effects.push(Effect {
        delay: 2,
        effect_type: EffectType::SecondaryFlash(hit_pos),
    });
}
```

### Layered Sound Design

```rust
fn play_impact_sfx(game: &Game, intensity: u8) {
    // Layer multiple sounds for richness
    play_sound(game.sfx_impact_base, 1.0, 0.0);

    if intensity > 1 {
        play_sound(game.sfx_impact_crunch, 0.7, 0.0);
    }

    if intensity > 2 {
        play_sound(game.sfx_impact_bass, 0.5, 0.0);
    }
}
```

---

## Anticipation and Follow-Through

### Wind-Up Before Attack

```rust
#[derive(Clone, Copy)]
enum AttackState {
    Idle,
    WindUp { remaining: u32 },
    Active { remaining: u32 },
    Recovery { remaining: u32 },
}

const WINDUP_FRAMES: u32 = 8;
const ACTIVE_FRAMES: u32 = 4;
const RECOVERY_FRAMES: u32 = 12;

fn start_attack(player: &mut Player) {
    player.attack_state = AttackState::WindUp { remaining: WINDUP_FRAMES };

    // Audio cue at start of wind-up
    play_sound(player.sfx_whoosh_charge, 0.6, 0.0);
}

fn update_attack(player: &mut Player, game: &mut Game) {
    player.attack_state = match player.attack_state {
        AttackState::WindUp { remaining } => {
            if remaining > 0 {
                AttackState::WindUp { remaining: remaining - 1 }
            } else {
                // Attack becomes active
                play_sound(player.sfx_whoosh_swing, 1.0, 0.0);
                AttackState::Active { remaining: ACTIVE_FRAMES }
            }
        }
        AttackState::Active { remaining } => {
            // Hitbox active during these frames
            check_attack_hits(player, game);
            if remaining > 0 {
                AttackState::Active { remaining: remaining - 1 }
            } else {
                AttackState::Recovery { remaining: RECOVERY_FRAMES }
            }
        }
        AttackState::Recovery { remaining } => {
            if remaining > 0 {
                AttackState::Recovery { remaining: remaining - 1 }
            } else {
                AttackState::Idle
            }
        }
        AttackState::Idle => AttackState::Idle,
    };
}
```

### Scale Punch on Land

Quick scale animation when landing from a jump:

```rust
struct ScaleEffect {
    scale_x: f32,
    scale_y: f32,
    recovery_speed: f32,
}

impl ScaleEffect {
    fn squash(&mut self) {
        // Flatten on land
        self.scale_x = 1.3;
        self.scale_y = 0.7;
    }

    fn stretch(&mut self) {
        // Elongate when jumping
        self.scale_x = 0.8;
        self.scale_y = 1.2;
    }

    fn update(&mut self) {
        // Recover toward neutral
        self.scale_x += (1.0 - self.scale_x) * self.recovery_speed;
        self.scale_y += (1.0 - self.scale_y) * self.recovery_speed;
    }
}

fn on_land(player: &mut Player) {
    player.scale.squash();
    play_sound(player.sfx_land, 0.5, 0.0);
    spawn_dust_particles(player.x, player.y);
}
```

---

## Input Responsiveness

### Input Buffering

Accept inputs slightly before they become valid:

```rust
const INPUT_BUFFER_FRAMES: u32 = 6;

struct InputBuffer {
    jump_buffer: u32,
    attack_buffer: u32,
}

impl InputBuffer {
    fn update(&mut self) {
        // Record inputs
        if button_pressed(0, button::A) {
            self.jump_buffer = INPUT_BUFFER_FRAMES;
        }
        if button_pressed(0, button::X) {
            self.attack_buffer = INPUT_BUFFER_FRAMES;
        }

        // Decay buffers
        self.jump_buffer = self.jump_buffer.saturating_sub(1);
        self.attack_buffer = self.attack_buffer.saturating_sub(1);
    }

    fn consume_jump(&mut self) -> bool {
        if self.jump_buffer > 0 {
            self.jump_buffer = 0;
            true
        } else {
            false
        }
    }

    fn consume_attack(&mut self) -> bool {
        if self.attack_buffer > 0 {
            self.attack_buffer = 0;
            true
        } else {
            false
        }
    }
}
```

### Coyote Time

Allow jumps briefly after leaving a platform (see gameplay-mechanics skill for full implementation).

---

## Simple Particle Effects

Lightweight particle system for impacts, dust, and sparks:

```rust
const MAX_PARTICLES: usize = 64;

struct Particle {
    active: bool,
    x: f32, y: f32,
    vx: f32, vy: f32,
    life: u32,
    max_life: u32,
    color: u32,
    size: f32,
}

struct ParticleSystem {
    particles: [Particle; MAX_PARTICLES],
}

impl ParticleSystem {
    fn spawn(&mut self, x: f32, y: f32, count: u8, config: ParticleConfig) {
        let mut spawned = 0;
        for particle in &mut self.particles {
            if !particle.active && spawned < count {
                particle.active = true;
                particle.x = x;
                particle.y = y;
                particle.vx = (random() - 0.5) * config.spread;
                particle.vy = (random() - 0.5) * config.spread - config.upward_bias;
                particle.life = config.lifetime;
                particle.max_life = config.lifetime;
                particle.color = config.color;
                particle.size = config.size;
                spawned += 1;
            }
        }
    }

    fn update(&mut self) {
        for p in &mut self.particles {
            if p.active {
                p.x += p.vx;
                p.y += p.vy;
                p.vy += 0.2;  // Gravity
                p.life = p.life.saturating_sub(1);
                if p.life == 0 {
                    p.active = false;
                }
            }
        }
    }

    fn render(&self) {
        for p in &self.particles {
            if p.active {
                // Fade out based on remaining life
                let alpha = ((p.life as f32 / p.max_life as f32) * 255.0) as u32;
                let color = (p.color & 0xFFFFFF00) | alpha;
                draw_circle(p.x, p.y, p.size, color);
            }
        }
    }
}

struct ParticleConfig {
    spread: f32,
    upward_bias: f32,
    lifetime: u32,
    color: u32,
    size: f32,
}
```

### Common Particle Presets

```rust
fn spawn_hit_particles(particles: &mut ParticleSystem, x: f32, y: f32) {
    particles.spawn(x, y, 8, ParticleConfig {
        spread: 8.0,
        upward_bias: 2.0,
        lifetime: 15,
        color: 0xFFFF00FF,
        size: 4.0,
    });
}

fn spawn_dust_particles(particles: &mut ParticleSystem, x: f32, y: f32) {
    particles.spawn(x, y, 5, ParticleConfig {
        spread: 3.0,
        upward_bias: 1.0,
        lifetime: 20,
        color: 0x888888FF,
        size: 3.0,
    });
}

fn spawn_spark_particles(particles: &mut ParticleSystem, x: f32, y: f32) {
    particles.spawn(x, y, 12, ParticleConfig {
        spread: 12.0,
        upward_bias: 0.0,
        lifetime: 8,
        color: 0xFFFFFFFF,
        size: 2.0,
    });
}
```

---

## Complete Game Feel System

```rust
struct GameFeel {
    screen_shake: ScreenShake,
    hit_pause: HitPause,
    particles: ParticleSystem,
}

impl GameFeel {
    fn update(&mut self) {
        self.hit_pause.update();
        self.particles.update();
    }

    fn on_hit(&mut self, pos: [f32; 2], intensity: u8, hit_sfx: u32) {
        // Shake based on intensity
        self.screen_shake.trigger(intensity as f32 * 3.0, 6 + intensity as u32 * 2);

        // Hit pause
        self.hit_pause.trigger(2 + intensity as u32);

        // Particles
        self.particles.spawn(pos[0], pos[1], 6 + intensity * 2, ParticleConfig {
            spread: 6.0 + intensity as f32 * 2.0,
            upward_bias: 1.5,
            lifetime: 12 + intensity as u32 * 3,
            color: 0xFFFF00FF,
            size: 3.0 + intensity as f32,
        });

        // Sound
        play_sound(hit_sfx, 0.8 + intensity as f32 * 0.1, 0.0);
    }

    fn render(&self) {
        self.particles.render();
    }
}
```

---

## Additional Resources

### Reference Files

For advanced techniques:
- **`references/advanced-techniques.md`** — Speed lines, motion blur, impact frames, slow motion

### Related Skills

- **`gameplay-mechanics`** — Coyote time, jump buffering, i-frames
- **`physics-collision`** — Knockback and bounce responses
- **`perspective-patterns`** — Camera follow and smoothing
