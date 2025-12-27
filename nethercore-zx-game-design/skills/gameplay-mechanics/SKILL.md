---
name: Gameplay Mechanics Library
description: This skill should be used when the user asks about "platformer physics", "variable jump", "coyote time", "jump buffer", "wall jump", "hitbox", "hurtbox", "combat system", "i-frames", "invincibility frames", "knockback", "combo system", "inventory", "item pickup", "equipment", "dialogue system", "text box", "typewriter effect", "movement mechanics", "acceleration", "dash", "dodge", "8-directional movement", or implements common gameplay patterns for Nethercore ZX games.
version: 0.1.0
---

# Gameplay Mechanics Library

Tested, rollback-safe implementations of common gameplay patterns for Nethercore ZX. Every pattern uses deterministic logic compatible with GGRS rollback netcode.

## Rollback Safety Requirements

All gameplay code MUST be deterministic:

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Time | `delta_time()`, `tick_count()` | System clock, `std::time` |
| Random | `random()`, `random_range()` | `rand()`, external RNG |
| Input | `button_pressed()`, `button_held()` | OS input events |
| State | Fixed-point or consistent floats | Platform-dependent floats |

The FFI provides all timing and input functions needed for deterministic gameplay.

---

## Platformer Mechanics

Core physics patterns for 2D/2.5D platformers.

### Variable-Height Jump

Hold jump button longer for higher jumps.

```rust
const JUMP_VELOCITY: f32 = -12.0;
const JUMP_CUT_MULTIPLIER: f32 = 0.5;
const GRAVITY: f32 = 0.6;

fn update_jump(player: &mut Player) {
    // Apply gravity
    player.vel_y += GRAVITY;

    // Cut jump short when button released while rising
    if button_released(0, button::A) && player.vel_y < 0.0 {
        player.vel_y *= JUMP_CUT_MULTIPLIER;
    }

    // Initiate jump
    if button_pressed(0, button::A) && player.grounded {
        player.vel_y = JUMP_VELOCITY;
        player.grounded = false;
    }
}
```

### Coyote Time

Grace period allowing jumps shortly after leaving a platform.

```rust
const COYOTE_FRAMES: u32 = 6;  // ~100ms at 60fps

struct Player {
    coyote_timer: u32,
    grounded: bool,
    // ...
}

fn update_coyote(player: &mut Player) {
    if player.grounded {
        player.coyote_timer = COYOTE_FRAMES;
    } else if player.coyote_timer > 0 {
        player.coyote_timer -= 1;
    }
}

fn can_jump(player: &Player) -> bool {
    player.grounded || player.coyote_timer > 0
}
```

### Jump Buffering

Queue jump input before landing for responsive controls.

```rust
const BUFFER_FRAMES: u32 = 8;  // ~133ms at 60fps

struct Player {
    jump_buffer: u32,
    // ...
}

fn update_buffer(player: &mut Player) {
    if button_pressed(0, button::A) {
        player.jump_buffer = BUFFER_FRAMES;
    } else if player.jump_buffer > 0 {
        player.jump_buffer -= 1;
    }
}

fn try_jump(player: &mut Player) {
    if player.grounded && player.jump_buffer > 0 {
        player.vel_y = JUMP_VELOCITY;
        player.jump_buffer = 0;
        player.grounded = false;
    }
}
```

See **`references/platformer-mechanics.md`** for wall jumping, moving platforms, and one-way platforms.

---

## Combat Mechanics

Frame-based combat systems with hitboxes and damage.

### Hitbox/Hurtbox System

Separate collision volumes for attacks and vulnerability.

```rust
#[derive(Clone, Copy)]
struct Hitbox {
    x: i16, y: i16,           // Offset from entity
    width: i16, height: i16,
    damage: u8,
    knockback: i16,
    active_start: u8,         // Frame attack becomes active
    active_end: u8,           // Frame attack ends
}

#[derive(Clone, Copy)]
struct Hurtbox {
    x: i16, y: i16,
    width: i16, height: i16,
}

fn check_hit(hitbox: &Hitbox, attacker_x: i16, attacker_y: i16,
             hurtbox: &Hurtbox, defender_x: i16, defender_y: i16) -> bool {
    let hx = attacker_x + hitbox.x;
    let hy = attacker_y + hitbox.y;
    let dx = defender_x + hurtbox.x;
    let dy = defender_y + hurtbox.y;

    hx < dx + hurtbox.width && hx + hitbox.width > dx &&
    hy < dy + hurtbox.height && hy + hitbox.height > dy
}
```

### Invincibility Frames (i-Frames)

Temporary invulnerability after taking damage.

```rust
const IFRAMES_DURATION: u32 = 45;  // ~750ms at 60fps

struct Entity {
    iframes: u32,
    health: i16,
    // ...
}

fn take_damage(entity: &mut Entity, damage: u8) {
    if entity.iframes == 0 {
        entity.health -= damage as i16;
        entity.iframes = IFRAMES_DURATION;
    }
}

fn update_iframes(entity: &mut Entity) {
    if entity.iframes > 0 {
        entity.iframes -= 1;
    }
}

fn is_vulnerable(entity: &Entity) -> bool {
    entity.iframes == 0
}
```

### Knockback and Hitstun

Push entities backward and freeze their input.

```rust
struct Entity {
    hitstun: u32,
    knockback_vel: f32,
    facing_right: bool,
    // ...
}

fn apply_knockback(entity: &mut Entity, knockback: i16, from_right: bool) {
    entity.knockback_vel = if from_right { -knockback as f32 } else { knockback as f32 };
    entity.hitstun = (knockback as u32) / 2;  // Hitstun proportional to knockback
}

fn update_knockback(entity: &mut Entity) {
    if entity.hitstun > 0 {
        entity.x += entity.knockback_vel as i16;
        entity.knockback_vel *= 0.85;  // Friction
        entity.hitstun -= 1;
    }
}

fn can_act(entity: &Entity) -> bool {
    entity.hitstun == 0
}
```

See **`references/combat-mechanics.md`** for combo systems and attack state machines.

---

## Movement Patterns

Character movement for various game styles.

### 8-Directional Movement (Top-Down)

```rust
const MOVE_SPEED: f32 = 3.0;

fn update_movement(player: &mut Player) {
    let mut dx: f32 = 0.0;
    let mut dy: f32 = 0.0;

    if button_held(0, button::LEFT)  { dx -= 1.0; }
    if button_held(0, button::RIGHT) { dx += 1.0; }
    if button_held(0, button::UP)    { dy -= 1.0; }
    if button_held(0, button::DOWN)  { dy += 1.0; }

    // Normalize diagonal movement
    let len = (dx * dx + dy * dy).sqrt();
    if len > 0.0 {
        dx = dx / len * MOVE_SPEED;
        dy = dy / len * MOVE_SPEED;
    }

    player.x += dx;
    player.y += dy;
}
```

### Acceleration and Deceleration

Smooth movement with inertia.

```rust
const MAX_SPEED: f32 = 6.0;
const ACCEL: f32 = 0.8;
const FRICTION: f32 = 0.85;

fn update_velocity(player: &mut Player) {
    let input_x = left_stick_x(0);  // -1.0 to 1.0

    if input_x.abs() > 0.1 {
        // Accelerate toward input direction
        player.vel_x += input_x * ACCEL;
        player.vel_x = player.vel_x.clamp(-MAX_SPEED, MAX_SPEED);
    } else {
        // Apply friction when no input
        player.vel_x *= FRICTION;
    }

    player.x += player.vel_x;
}
```

### Dash Mechanic

Quick burst of speed with cooldown.

```rust
const DASH_SPEED: f32 = 15.0;
const DASH_DURATION: u32 = 8;
const DASH_COOLDOWN: u32 = 30;

struct Player {
    dash_timer: u32,
    dash_cooldown: u32,
    dash_dir_x: f32,
    dash_dir_y: f32,
    // ...
}

fn try_dash(player: &mut Player) {
    if button_pressed(0, button::L1) && player.dash_cooldown == 0 {
        player.dash_timer = DASH_DURATION;
        player.dash_cooldown = DASH_COOLDOWN;
        // Lock dash direction at activation
        player.dash_dir_x = left_stick_x(0);
        player.dash_dir_y = left_stick_y(0);
        // Normalize
        let len = (player.dash_dir_x.powi(2) + player.dash_dir_y.powi(2)).sqrt();
        if len > 0.1 {
            player.dash_dir_x /= len;
            player.dash_dir_y /= len;
        } else {
            player.dash_dir_x = if player.facing_right { 1.0 } else { -1.0 };
            player.dash_dir_y = 0.0;
        }
    }
}

fn update_dash(player: &mut Player) {
    if player.dash_timer > 0 {
        player.x += player.dash_dir_x * DASH_SPEED;
        player.y += player.dash_dir_y * DASH_SPEED;
        player.dash_timer -= 1;
    }
    if player.dash_cooldown > 0 {
        player.dash_cooldown -= 1;
    }
}

fn is_dashing(player: &Player) -> bool {
    player.dash_timer > 0
}
```

See **`references/movement-patterns.md`** for tank controls and analog stick handling.

---

## Items and Inventory

Pickup, storage, and equipment patterns.

### Simple Item Pickup

```rust
const PICKUP_RADIUS: f32 = 16.0;

struct Item {
    x: f32, y: f32,
    item_type: u8,
    active: bool,
}

fn check_pickup(player: &Player, item: &mut Item) -> Option<u8> {
    if !item.active { return None; }

    let dx = player.x - item.x;
    let dy = player.y - item.y;
    let dist_sq = dx * dx + dy * dy;

    if dist_sq < PICKUP_RADIUS * PICKUP_RADIUS {
        item.active = false;
        Some(item.item_type)
    } else {
        None
    }
}
```

### Fixed-Slot Inventory

```rust
const INVENTORY_SIZE: usize = 8;
const EMPTY_SLOT: u8 = 0xFF;

struct Inventory {
    slots: [u8; INVENTORY_SIZE],
    selected: u8,
}

impl Inventory {
    fn new() -> Self {
        Self {
            slots: [EMPTY_SLOT; INVENTORY_SIZE],
            selected: 0,
        }
    }

    fn add_item(&mut self, item: u8) -> bool {
        for slot in &mut self.slots {
            if *slot == EMPTY_SLOT {
                *slot = item;
                return true;
            }
        }
        false  // Inventory full
    }

    fn use_selected(&mut self) -> Option<u8> {
        let item = self.slots[self.selected as usize];
        if item != EMPTY_SLOT {
            self.slots[self.selected as usize] = EMPTY_SLOT;
            Some(item)
        } else {
            None
        }
    }
}
```

See **`references/inventory-systems.md`** for equipment slots and consumable cooldowns.

---

## Dialogue and Text

Text box systems with progressive reveal.

### Typewriter Effect

```rust
const CHARS_PER_FRAME: u32 = 2;

struct DialogueBox {
    text: &'static str,
    chars_shown: u32,
    finished: bool,
}

impl DialogueBox {
    fn update(&mut self) {
        if !self.finished {
            self.chars_shown += CHARS_PER_FRAME;
            if self.chars_shown >= self.text.len() as u32 {
                self.chars_shown = self.text.len() as u32;
                self.finished = true;
            }
        }

        // Skip to end on button press
        if button_pressed(0, button::A) && !self.finished {
            self.chars_shown = self.text.len() as u32;
            self.finished = true;
        }
    }

    fn render(&self) {
        // Draw box background
        draw_rect(50.0, 400.0, 860.0, 100.0, 0x000000CC);

        // Draw visible portion of text
        let visible = &self.text[..self.chars_shown as usize];
        draw_text_str(visible, 60.0, 420.0, 24.0, 0xFFFFFFFF);
    }
}
```

### Choice Selection

```rust
struct ChoiceMenu {
    options: &'static [&'static str],
    selected: u8,
}

impl ChoiceMenu {
    fn update(&mut self) {
        if button_pressed(0, button::UP) && self.selected > 0 {
            self.selected -= 1;
        }
        if button_pressed(0, button::DOWN) {
            if (self.selected as usize) < self.options.len() - 1 {
                self.selected += 1;
            }
        }
    }

    fn confirm(&self) -> Option<u8> {
        if button_pressed(0, button::A) {
            Some(self.selected)
        } else {
            None
        }
    }

    fn render(&self) {
        for (i, option) in self.options.iter().enumerate() {
            let y = 420.0 + i as f32 * 30.0;
            let color = if i == self.selected as usize {
                0xFFFF00FF  // Yellow for selected
            } else {
                0xFFFFFFFF  // White for unselected
            };
            draw_text_str(option, 80.0, y, 24.0, color);
        }
        // Draw selection arrow
        let arrow_y = 420.0 + self.selected as f32 * 30.0;
        draw_text_str(">", 60.0, arrow_y, 24.0, 0xFFFF00FF);
    }
}
```

See **`references/dialogue-systems.md`** for branching dialogue state machines and portrait rendering.

---

## Additional Resources

### Reference Files

Detailed implementations with complete code:
- **`references/platformer-mechanics.md`** — Wall jump, moving platforms, one-way platforms
- **`references/combat-mechanics.md`** — Combo systems, attack state machines, hit detection
- **`references/movement-patterns.md`** — Tank controls, analog input, momentum
- **`references/inventory-systems.md`** — Equipment, consumables, stackable items
- **`references/dialogue-systems.md`** — Portraits, branching trees, save/load state

### Related Skills

- **`multiplayer-design`** — Rollback safety and determinism patterns
- **`perspective-patterns`** — Camera and control schemes per game type
- **`physics-collision`** (Gap 16) — Underlying collision detection systems
