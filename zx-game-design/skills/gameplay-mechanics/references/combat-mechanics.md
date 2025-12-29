# Combat Mechanics Reference

Rollback-safe combat system implementations for Nethercore ZX fighting games, action games, and beat 'em ups.

## Hitbox/Hurtbox System (Complete)

Separate attack volumes (hitboxes) from vulnerability volumes (hurtboxes) for precise combat.

```rust
use crate::ffi::*;

/// Attack collision volume
#[derive(Clone, Copy, Default)]
#[repr(C)]
struct Hitbox {
    offset_x: i16,        // Offset from entity center
    offset_y: i16,
    width: i16,
    height: i16,
    damage: u8,
    knockback_x: i8,      // Horizontal knockback force
    knockback_y: i8,      // Vertical knockback force
    hitstun: u8,          // Frames of stun on hit
}

/// Vulnerability volume
#[derive(Clone, Copy, Default)]
#[repr(C)]
struct Hurtbox {
    offset_x: i16,
    offset_y: i16,
    width: i16,
    height: i16,
}

/// Check AABB overlap between hitbox and hurtbox
fn check_hit(
    hitbox: &Hitbox, attacker_x: i16, attacker_y: i16, facing_right: bool,
    hurtbox: &Hurtbox, defender_x: i16, defender_y: i16
) -> bool {
    // Flip hitbox offset based on facing direction
    let hb_offset_x = if facing_right {
        hitbox.offset_x
    } else {
        -hitbox.offset_x - hitbox.width
    };

    let hb_x = attacker_x + hb_offset_x;
    let hb_y = attacker_y + hitbox.offset_y;

    let db_x = defender_x + hurtbox.offset_x;
    let db_y = defender_y + hurtbox.offset_y;

    // AABB intersection test
    hb_x < db_x + hurtbox.width &&
    hb_x + hitbox.width > db_x &&
    hb_y < db_y + hurtbox.height &&
    hb_y + hitbox.height > db_y
}
```

### Multi-Hitbox Attacks

Complex attacks with multiple hitboxes (e.g., sword slash with separate tip/body damage):

```rust
const MAX_HITBOXES: usize = 4;

struct Attack {
    hitboxes: [Option<Hitbox>; MAX_HITBOXES],
    active_start: u8,   // Frame attack becomes active
    active_end: u8,     // Frame attack ends
    recovery: u8,       // Frames before next action
}

fn get_active_hitboxes(attack: &Attack, frame: u8) -> impl Iterator<Item = &Hitbox> {
    attack.hitboxes.iter()
        .filter_map(|h| h.as_ref())
        .filter(move |_| frame >= attack.active_start && frame <= attack.active_end)
}
```

---

## Attack State Machine

Frame-based attack system with startup, active, and recovery phases.

```rust
#[derive(Clone, Copy, PartialEq)]
enum AttackState {
    Idle,
    Startup(u8),     // Frames until hitbox active
    Active(u8),      // Frames hitbox is active
    Recovery(u8),    // Frames until actionable
}

#[derive(Clone, Copy)]
struct AttackData {
    startup: u8,
    active: u8,
    recovery: u8,
    hitbox: Hitbox,
}

struct Fighter {
    x: i16,
    y: i16,
    facing_right: bool,
    attack_state: AttackState,
    current_attack: Option<AttackData>,
    hurtbox: Hurtbox,
}

impl Fighter {
    fn start_attack(&mut self, attack: AttackData) {
        if self.attack_state == AttackState::Idle {
            self.attack_state = AttackState::Startup(attack.startup);
            self.current_attack = Some(attack);
        }
    }

    fn update_attack(&mut self) -> Option<&Hitbox> {
        let mut active_hitbox = None;

        self.attack_state = match self.attack_state {
            AttackState::Idle => AttackState::Idle,

            AttackState::Startup(frames) => {
                if frames > 1 {
                    AttackState::Startup(frames - 1)
                } else {
                    // Transition to active
                    let active = self.current_attack.map(|a| a.active).unwrap_or(1);
                    AttackState::Active(active)
                }
            }

            AttackState::Active(frames) => {
                // Hitbox is active this frame
                if let Some(ref attack) = self.current_attack {
                    active_hitbox = Some(&attack.hitbox);
                }

                if frames > 1 {
                    AttackState::Active(frames - 1)
                } else {
                    // Transition to recovery
                    let recovery = self.current_attack.map(|a| a.recovery).unwrap_or(1);
                    AttackState::Recovery(recovery)
                }
            }

            AttackState::Recovery(frames) => {
                if frames > 1 {
                    AttackState::Recovery(frames - 1)
                } else {
                    self.current_attack = None;
                    AttackState::Idle
                }
            }
        };

        active_hitbox
    }

    fn can_act(&self) -> bool {
        self.attack_state == AttackState::Idle
    }
}
```

### Frame Data Table

Define attacks with frame data:

```rust
// Example: 3-hit combo
const LIGHT_PUNCH: AttackData = AttackData {
    startup: 3,
    active: 2,
    recovery: 8,
    hitbox: Hitbox {
        offset_x: 20, offset_y: -10,
        width: 30, height: 20,
        damage: 5, knockback_x: 2, knockback_y: 0, hitstun: 12,
    },
};

const MEDIUM_PUNCH: AttackData = AttackData {
    startup: 5,
    active: 3,
    recovery: 12,
    hitbox: Hitbox {
        offset_x: 15, offset_y: -15,
        width: 40, height: 30,
        damage: 10, knockback_x: 4, knockback_y: -1, hitstun: 16,
    },
};

const HEAVY_PUNCH: AttackData = AttackData {
    startup: 8,
    active: 4,
    recovery: 20,
    hitbox: Hitbox {
        offset_x: 10, offset_y: -20,
        width: 50, height: 40,
        damage: 20, knockback_x: 8, knockback_y: -3, hitstun: 24,
    },
};
```

---

## Invincibility Frames (i-Frames)

Temporary invulnerability after damage.

```rust
const IFRAMES_ON_HIT: u32 = 45;      // ~750ms at 60fps
const IFRAMES_FLASH_RATE: u32 = 4;   // Flash every N frames

struct Entity {
    health: i16,
    max_health: i16,
    iframes: u32,
    visible: bool,
}

impl Entity {
    fn take_damage(&mut self, damage: u8, knockback_x: i8, knockback_y: i8) -> bool {
        if self.iframes > 0 {
            return false;  // Still invulnerable
        }

        self.health -= damage as i16;
        self.iframes = IFRAMES_ON_HIT;

        // Apply knockback (handled by caller or separate system)
        true
    }

    fn update_iframes(&mut self) {
        if self.iframes > 0 {
            self.iframes -= 1;

            // Flash visibility
            self.visible = (self.iframes / IFRAMES_FLASH_RATE) % 2 == 0;
        } else {
            self.visible = true;
        }
    }

    fn is_vulnerable(&self) -> bool {
        self.iframes == 0
    }
}
```

### Different i-Frame Types

```rust
enum IFrameType {
    None,
    Hit(u32),         // From taking damage
    Dodge(u32),       // From dodging (may be shorter)
    Super(u32),       // From super move startup (invincible to throws)
}

impl Entity {
    fn is_vulnerable_to(&self, attack_type: AttackType) -> bool {
        match (&self.iframe_type, attack_type) {
            (IFrameType::None, _) => true,
            (IFrameType::Hit(_), _) => false,
            (IFrameType::Dodge(_), _) => false,
            (IFrameType::Super(_), AttackType::Throw) => false,
            (IFrameType::Super(_), _) => true,  // Super has throw invuln only
        }
    }
}
```

---

## Knockback and Hitstun

Push entities and freeze their actions on hit.

```rust
struct KnockbackState {
    vel_x: f32,
    vel_y: f32,
    hitstun: u32,
    gravity: f32,
}

impl KnockbackState {
    fn apply(&mut self, knockback_x: i8, knockback_y: i8, hitstun: u8, facing_right: bool) {
        // Knockback direction based on attacker facing
        let dir = if facing_right { 1.0 } else { -1.0 };
        self.vel_x = knockback_x as f32 * dir;
        self.vel_y = knockback_y as f32;
        self.hitstun = hitstun as u32;
    }

    fn update(&mut self) {
        if self.hitstun > 0 {
            // Apply knockback velocity
            self.vel_y += self.gravity;

            // Decay horizontal velocity
            self.vel_x *= 0.9;

            self.hitstun -= 1;
        }
    }

    fn get_velocity(&self) -> (f32, f32) {
        if self.hitstun > 0 {
            (self.vel_x, self.vel_y)
        } else {
            (0.0, 0.0)
        }
    }

    fn in_hitstun(&self) -> bool {
        self.hitstun > 0
    }
}
```

### Damage Calculation

```rust
struct DamageResult {
    final_damage: u16,
    was_critical: bool,
    was_blocked: bool,
}

fn calculate_damage(
    base_damage: u8,
    attacker_strength: u8,
    defender_defense: u8,
    is_blocking: bool,
    hit_count: u8,  // For combo scaling
) -> DamageResult {
    // Base calculation
    let mut damage = base_damage as u16 + (attacker_strength as u16 / 2);

    // Defense reduction
    damage = damage.saturating_sub(defender_defense as u16 / 4);

    // Block reduction (80% less damage)
    let was_blocked = is_blocking;
    if was_blocked {
        damage = damage / 5;
    }

    // Combo scaling (damage reduces with hit count)
    let scale = match hit_count {
        0..=2 => 100,
        3..=5 => 80,
        6..=9 => 60,
        _ => 40,
    };
    damage = (damage * scale) / 100;

    // Critical hit (use deterministic random)
    let crit_roll = random() % 100;
    let was_critical = crit_roll < 10;  // 10% crit chance
    if was_critical {
        damage = damage * 3 / 2;  // 1.5x damage
    }

    DamageResult {
        final_damage: damage.max(1),  // Always deal at least 1
        was_critical,
        was_blocked,
    }
}
```

---

## Combo System

Chain attacks together with timing windows.

```rust
const COMBO_WINDOW: u32 = 15;  // Frames to input next attack

#[derive(Clone, Copy, PartialEq)]
enum ComboState {
    Idle,
    Attack1,
    Attack2,
    Attack3,
    Finisher,
}

struct ComboTracker {
    state: ComboState,
    window_timer: u32,
    hit_confirmed: bool,  // Only continue combo if attack hit
}

impl ComboTracker {
    fn update(&mut self, attack_active: bool, hit_this_frame: bool) {
        // Track if attack connected
        if hit_this_frame {
            self.hit_confirmed = true;
        }

        // Combo window countdown
        if self.window_timer > 0 {
            self.window_timer -= 1;
        }

        // Reset if window expires
        if self.window_timer == 0 && self.state != ComboState::Idle {
            self.reset();
        }
    }

    fn try_advance(&mut self, button: u32) -> Option<AttackData> {
        // Can only advance if hit confirmed and in window
        if !self.hit_confirmed && self.state != ComboState::Idle {
            return None;
        }

        let next_attack = match (self.state, button) {
            // Ground combo: A -> A -> A -> B
            (ComboState::Idle, button::A) => {
                self.state = ComboState::Attack1;
                Some(LIGHT_PUNCH)
            }
            (ComboState::Attack1, button::A) => {
                self.state = ComboState::Attack2;
                Some(MEDIUM_PUNCH)
            }
            (ComboState::Attack2, button::A) => {
                self.state = ComboState::Attack3;
                Some(HEAVY_PUNCH)
            }
            (ComboState::Attack3, button::B) => {
                self.state = ComboState::Finisher;
                Some(FINISHER)
            }
            _ => None,
        };

        if next_attack.is_some() {
            self.window_timer = COMBO_WINDOW;
            self.hit_confirmed = false;
        }

        next_attack
    }

    fn reset(&mut self) {
        self.state = ComboState::Idle;
        self.window_timer = 0;
        self.hit_confirmed = false;
    }
}
```

### Hit Tracking (Prevent Multi-Hit)

Track which entities were hit by an attack to prevent hitting the same target multiple times:

```rust
const MAX_HIT_TARGETS: usize = 8;

struct HitTracker {
    hit_ids: [u16; MAX_HIT_TARGETS],
    count: u8,
}

impl HitTracker {
    fn new() -> Self {
        Self {
            hit_ids: [0; MAX_HIT_TARGETS],
            count: 0,
        }
    }

    fn already_hit(&self, entity_id: u16) -> bool {
        for i in 0..self.count as usize {
            if self.hit_ids[i] == entity_id {
                return true;
            }
        }
        false
    }

    fn record_hit(&mut self, entity_id: u16) {
        if (self.count as usize) < MAX_HIT_TARGETS {
            self.hit_ids[self.count as usize] = entity_id;
            self.count += 1;
        }
    }

    fn clear(&mut self) {
        self.count = 0;
    }
}
```

---

## Complete Combat Update

```rust
fn update_combat(attacker: &mut Fighter, defenders: &mut [Fighter]) {
    // Update attack state and get active hitbox
    let active_hitbox = attacker.update_attack();

    // Update i-frames for all fighters
    attacker.entity.update_iframes();
    for defender in defenders.iter_mut() {
        defender.entity.update_iframes();
    }

    // Check hits
    if let Some(hitbox) = active_hitbox {
        for defender in defenders.iter_mut() {
            if !defender.entity.is_vulnerable() {
                continue;
            }

            if attacker.hit_tracker.already_hit(defender.id) {
                continue;
            }

            if check_hit(
                hitbox, attacker.x, attacker.y, attacker.facing_right,
                &defender.hurtbox, defender.x, defender.y
            ) {
                // Apply damage
                let result = calculate_damage(
                    hitbox.damage,
                    attacker.strength,
                    defender.defense,
                    defender.is_blocking,
                    attacker.combo.hit_count,
                );

                if defender.entity.take_damage(
                    result.final_damage as u8,
                    hitbox.knockback_x,
                    hitbox.knockback_y
                ) {
                    // Apply knockback
                    defender.knockback.apply(
                        hitbox.knockback_x,
                        hitbox.knockback_y,
                        hitbox.hitstun,
                        attacker.facing_right
                    );

                    attacker.hit_tracker.record_hit(defender.id);
                    attacker.combo.hit_confirmed = true;
                }
            }
        }
    }

    // Clear hit tracker when attack ends
    if attacker.attack_state == AttackState::Idle {
        attacker.hit_tracker.clear();
    }

    // Update knockback physics
    for fighter in defenders.iter_mut() {
        fighter.knockback.update();
        let (kx, ky) = fighter.knockback.get_velocity();
        fighter.x += kx as i16;
        fighter.y += ky as i16;
    }
}
```
