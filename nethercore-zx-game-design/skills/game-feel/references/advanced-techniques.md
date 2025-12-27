# Advanced Game Feel Techniques

Extended patterns for speed lines, motion blur, impact frames, slow motion, and other polish effects.

---

## Speed Lines

Draw motion lines to emphasize high-speed movement.

### Radial Speed Lines

```rust
struct SpeedLines {
    active: bool,
    intensity: f32,
    direction_x: f32,
    direction_y: f32,
}

impl SpeedLines {
    fn update(&mut self, player_vel_x: f32, player_vel_y: f32, threshold: f32) {
        let speed = (player_vel_x * player_vel_x + player_vel_y * player_vel_y).sqrt();
        self.active = speed > threshold;

        if self.active {
            self.intensity = ((speed - threshold) / 10.0).min(1.0);
            self.direction_x = player_vel_x / speed;
            self.direction_y = player_vel_y / speed;
        }
    }

    fn render(&self) {
        if !self.active { return; }

        let center_x = 480.0;
        let center_y = 270.0;
        let num_lines = (self.intensity * 20.0) as u32;

        for i in 0..num_lines {
            // Random angle with bias toward movement direction
            let base_angle = i as f32 * (360.0 / num_lines as f32) * (3.14159 / 180.0);

            // Start and end points from center
            let inner_radius = 200.0 + random() * 50.0;
            let outer_radius = 400.0 + random() * 100.0;

            let x1 = center_x + base_angle.cos() * inner_radius;
            let y1 = center_y + base_angle.sin() * inner_radius;
            let x2 = center_x + base_angle.cos() * outer_radius;
            let y2 = center_y + base_angle.sin() * outer_radius;

            let alpha = (self.intensity * 128.0) as u32;
            draw_line(x1, y1, x2, y2, 2.0, 0xFFFFFF00 | alpha);
        }
    }
}
```

### Horizontal Speed Lines (Side-Scroller)

```rust
fn render_horizontal_speed_lines(player_x: f32, player_y: f32, speed: f32) {
    let threshold = 8.0;
    if speed.abs() < threshold { return; }

    let intensity = ((speed.abs() - threshold) / 10.0).min(1.0);
    let num_lines = (intensity * 15.0) as u32;
    let direction = if speed > 0.0 { -1.0 } else { 1.0 };

    for i in 0..num_lines {
        // Random vertical position near player
        let y = player_y - 50.0 + random() * 100.0;
        let length = 30.0 + random() * 50.0;
        let x_start = player_x + direction * 20.0 + random() * 30.0 * direction;

        let alpha = ((intensity * 180.0) * (1.0 - i as f32 / num_lines as f32)) as u32;
        draw_line(x_start, y, x_start + length * direction, y, 2.0, 0xFFFFFF00 | alpha);
    }
}
```

---

## Motion Trail (Ghost Effect)

Leave fading copies of the player during fast movement.

```rust
const TRAIL_LENGTH: usize = 5;

struct MotionTrail {
    positions: [(f32, f32, u32); TRAIL_LENGTH],  // x, y, texture
    current_index: usize,
    frame_counter: u32,
    capture_interval: u32,
}

impl MotionTrail {
    fn update(&mut self, x: f32, y: f32, texture: u32) {
        self.frame_counter += 1;
        if self.frame_counter >= self.capture_interval {
            self.frame_counter = 0;
            self.positions[self.current_index] = (x, y, texture);
            self.current_index = (self.current_index + 1) % TRAIL_LENGTH;
        }
    }

    fn render(&self, current_x: f32, current_y: f32) {
        for i in 0..TRAIL_LENGTH {
            let idx = (self.current_index + TRAIL_LENGTH - 1 - i) % TRAIL_LENGTH;
            let (x, y, texture) = self.positions[idx];

            // Skip if too close to current position
            let dist = ((x - current_x).powi(2) + (y - current_y).powi(2)).sqrt();
            if dist < 5.0 { continue; }

            // Fade based on age
            let alpha = ((TRAIL_LENGTH - i) as f32 / TRAIL_LENGTH as f32 * 0.5) * 255.0;
            let tint = 0xFFFFFF00 | (alpha as u32);

            draw_sprite_tinted(texture, x, y, 32.0, 32.0, tint);
        }
    }
}
```

---

## Impact Frame

Flash white or invert colors for a single frame on big impacts.

```rust
struct ImpactFrame {
    white_flash: u32,
    invert_frame: u32,
}

impl ImpactFrame {
    fn trigger_flash(&mut self, frames: u32) {
        self.white_flash = frames;
    }

    fn trigger_invert(&mut self, frames: u32) {
        self.invert_frame = frames;
    }

    fn update(&mut self) {
        self.white_flash = self.white_flash.saturating_sub(1);
        self.invert_frame = self.invert_frame.saturating_sub(1);
    }

    fn render_overlay(&self) {
        if self.white_flash > 0 {
            // White flash overlay
            let alpha = (self.white_flash as f32 * 40.0).min(200.0) as u32;
            draw_rect(0.0, 0.0, 960.0, 540.0, 0xFFFFFF00 | alpha);
        }

        if self.invert_frame > 0 {
            // Note: True inversion requires shader support
            // Simulate with strong white overlay
            draw_rect(0.0, 0.0, 960.0, 540.0, 0xFFFFFF80);
        }
    }
}
```

### Impact Flash on Hit

```rust
fn on_critical_hit(game: &mut Game, target: &mut Entity, damage: u32) {
    // Damage
    target.health -= damage as i32;

    // Impact frame effects
    game.impact_frame.trigger_flash(2);

    // Extra strong shake
    game.screen_shake.trigger(20.0, 12);

    // Long hit pause
    game.hit_pause.trigger(8);

    // Slow motion aftermath
    game.slow_motion.trigger(0.3, 20);

    // Sound
    play_sound(game.sfx_critical, 1.0, 0.0);
}
```

---

## Slow Motion

Temporarily reduce game speed for dramatic effect.

### Time Scale System

```rust
struct SlowMotion {
    time_scale: f32,
    target_scale: f32,
    remaining: u32,
    transition_speed: f32,
}

impl SlowMotion {
    fn trigger(&mut self, scale: f32, duration: u32) {
        self.target_scale = scale;
        self.remaining = duration;
    }

    fn update(&mut self) -> f32 {
        if self.remaining > 0 {
            self.remaining -= 1;
            // Smoothly approach target scale
            self.time_scale += (self.target_scale - self.time_scale) * self.transition_speed;
        } else {
            // Return to normal
            self.time_scale += (1.0 - self.time_scale) * self.transition_speed;
        }

        self.time_scale.clamp(0.1, 1.0)
    }
}

fn game_update(game: &mut Game) {
    let time_scale = game.slow_motion.update();
    let dt = unsafe { delta_time() } * time_scale;

    // Use scaled delta time for physics
    update_physics(game, dt);

    // Note: Input should NOT be scaled
    update_input(game);
}
```

### Kill Cam Slow Motion

```rust
fn on_kill(game: &mut Game, position: [f32; 2]) {
    // Dramatic slowdown
    game.slow_motion.trigger(0.2, 45);

    // Camera focus on kill location
    game.camera_target = position;

    // Particle burst
    game.particles.spawn(position[0], position[1], 30, ParticleConfig {
        spread: 15.0,
        upward_bias: 5.0,
        lifetime: 40,
        color: 0xFF4400FF,
        size: 6.0,
    });
}
```

---

## Entity Flash on Damage

Flash entities white or red when taking damage.

```rust
struct DamageFlash {
    remaining: u32,
    flash_color: u32,
}

impl DamageFlash {
    fn trigger(&mut self, color: u32, duration: u32) {
        self.flash_color = color;
        self.remaining = duration;
    }

    fn get_tint(&self) -> u32 {
        if self.remaining > 0 && (self.remaining / 2) % 2 == 0 {
            self.flash_color
        } else {
            0xFFFFFFFF  // No tint
        }
    }

    fn update(&mut self) {
        self.remaining = self.remaining.saturating_sub(1);
    }
}

fn render_entity(entity: &Entity) {
    let tint = entity.damage_flash.get_tint();
    draw_sprite_tinted(entity.texture, entity.x, entity.y, 32.0, 32.0, tint);
}

fn on_take_damage(entity: &mut Entity, damage: u32) {
    entity.health -= damage as i32;
    entity.damage_flash.trigger(0xFF8888FF, 20);  // Red flash for 20 frames
    entity.iframes = 45;
}
```

---

## Rumble Patterns

Controller vibration (if supported) to complement visual feedback.

```rust
// Note: Rumble FFI depends on platform support
// These patterns are conceptual for when available

struct RumblePattern {
    left_intensity: f32,   // Heavy motor
    right_intensity: f32,  // Light motor
    duration: u32,
}

const RUMBLE_LIGHT_HIT: RumblePattern = RumblePattern {
    left_intensity: 0.2,
    right_intensity: 0.4,
    duration: 4,
};

const RUMBLE_HEAVY_HIT: RumblePattern = RumblePattern {
    left_intensity: 0.7,
    right_intensity: 0.3,
    duration: 8,
};

const RUMBLE_EXPLOSION: RumblePattern = RumblePattern {
    left_intensity: 1.0,
    right_intensity: 0.5,
    duration: 15,
};

const RUMBLE_ENGINE: RumblePattern = RumblePattern {
    left_intensity: 0.3,
    right_intensity: 0.0,
    duration: 1,  // Continuous, re-apply each frame
};
```

---

## Combo Meter with Juice

Animated combo counter that scales and flashes.

```rust
struct ComboMeter {
    count: u32,
    timer: u32,
    display_scale: f32,
    flash_alpha: f32,
}

const COMBO_TIMEOUT: u32 = 120;  // 2 seconds at 60fps

impl ComboMeter {
    fn add_hit(&mut self) {
        self.count += 1;
        self.timer = COMBO_TIMEOUT;
        self.display_scale = 1.5;  // Pop up on new hit
        self.flash_alpha = 1.0;
    }

    fn update(&mut self) {
        if self.timer > 0 {
            self.timer -= 1;
            if self.timer == 0 {
                self.count = 0;  // Combo dropped
            }
        }

        // Animate back to normal
        self.display_scale += (1.0 - self.display_scale) * 0.2;
        self.flash_alpha *= 0.9;
    }

    fn render(&self, x: f32, y: f32) {
        if self.count < 2 { return; }

        // Flash background
        if self.flash_alpha > 0.1 {
            let flash_color = 0xFFFF0000 | ((self.flash_alpha * 128.0) as u32);
            draw_circle(x, y, 50.0 * self.display_scale, flash_color);
        }

        // Combo text
        let text = format!("{}x", self.count);
        let size = 32.0 * self.display_scale;

        // Color based on combo level
        let color = if self.count >= 20 {
            0xFF0000FF  // Red for massive combos
        } else if self.count >= 10 {
            0xFF8800FF  // Orange
        } else if self.count >= 5 {
            0xFFFF00FF  // Yellow
        } else {
            0xFFFFFFFF  // White
        };

        draw_text_shadowed(&text, x - size * 0.5, y - size * 0.3, size, color);

        // Timer bar
        let timer_ratio = self.timer as f32 / COMBO_TIMEOUT as f32;
        draw_rect(x - 30.0, y + 25.0, 60.0 * timer_ratio, 4.0, 0xFFFFFF88);
    }
}
```

---

## Screen Effects

### Vignette

Darken screen edges for focus or damage indication.

```rust
fn render_vignette(intensity: f32, color: u32) {
    // Draw multiple overlapping rects at edges
    let alpha = (intensity * 200.0) as u32;
    let edge_color = (color & 0xFFFFFF00) | alpha;

    // Top and bottom
    draw_rect(0.0, 0.0, 960.0, 80.0 * intensity, edge_color);
    draw_rect(0.0, 540.0 - 80.0 * intensity, 960.0, 80.0 * intensity, edge_color);

    // Left and right
    draw_rect(0.0, 0.0, 80.0 * intensity, 540.0, edge_color);
    draw_rect(960.0 - 80.0 * intensity, 0.0, 80.0 * intensity, 540.0, edge_color);
}

fn render_damage_vignette(health: i32, max_health: i32) {
    let health_ratio = health as f32 / max_health as f32;
    if health_ratio < 0.3 {
        let intensity = 1.0 - (health_ratio / 0.3);
        // Pulse red vignette when low health
        let pulse = ((tick_count() as f32 * 0.1).sin() * 0.5 + 0.5) * intensity;
        render_vignette(pulse, 0xFF0000FF);
    }
}
```

### Screen Zoom

Quick zoom in/out for impact.

```rust
struct ScreenZoom {
    current_fov: f32,
    target_fov: f32,
    base_fov: f32,
}

impl ScreenZoom {
    fn impact_zoom(&mut self) {
        // Quick zoom in
        self.target_fov = self.base_fov * 0.9;
    }

    fn update(&mut self) {
        // Smooth recovery
        self.current_fov += (self.target_fov - self.current_fov) * 0.15;
        self.target_fov += (self.base_fov - self.target_fov) * 0.1;

        unsafe {
            camera_fov(self.current_fov);
        }
    }
}
```

---

## Landing Impact

Full landing sequence with all juice elements.

```rust
fn on_land(player: &mut Player, game: &mut Game, fall_speed: f32) {
    let intensity = (fall_speed / 20.0).min(1.0);

    // Squash effect
    player.scale.squash();

    // Screen shake proportional to fall speed
    if intensity > 0.3 {
        game.screen_shake.trigger(intensity * 10.0, (intensity * 8.0) as u32);
    }

    // Dust particles
    let dust_count = (intensity * 10.0) as u8;
    game.particles.spawn(player.x, player.y + player.height * 0.5, dust_count, ParticleConfig {
        spread: 4.0,
        upward_bias: 0.5,
        lifetime: 15,
        color: 0x886644FF,
        size: 3.0,
    });

    // Sound based on intensity
    if intensity > 0.7 {
        play_sound(game.sfx_heavy_land, intensity, 0.0);
    } else {
        play_sound(game.sfx_light_land, intensity * 0.7, 0.0);
    }

    // Brief pause for heavy landings
    if intensity > 0.8 {
        game.hit_pause.trigger(2);
    }
}
```

---

## Audio Ducking

Lower music volume during important sound effects.

```rust
struct AudioMixer {
    music_volume: f32,
    target_music_volume: f32,
    duck_timer: u32,
}

impl AudioMixer {
    fn duck(&mut self, amount: f32, duration: u32) {
        self.target_music_volume = (1.0 - amount).max(0.1);
        self.duck_timer = duration;
    }

    fn update(&mut self) {
        if self.duck_timer > 0 {
            self.duck_timer -= 1;
            if self.duck_timer == 0 {
                self.target_music_volume = 1.0;
            }
        }

        // Smooth volume transition
        self.music_volume += (self.target_music_volume - self.music_volume) * 0.1;

        // Apply to music channel
        unsafe {
            music_volume(self.music_volume);
        }
    }
}

fn on_boss_hit(game: &mut Game) {
    // Duck music so hit sound stands out
    game.audio_mixer.duck(0.5, 15);

    // Play hit sound
    play_sound(game.sfx_boss_hit, 1.0, 0.0);
}
```
