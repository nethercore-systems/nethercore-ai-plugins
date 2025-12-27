# Side-Scroller Design Patterns

Comprehensive patterns for 2D/2.5D side-scrolling games on Nethercore ZX.

## Level Design Patterns

### Linear Progression
Classic left-to-right progression with occasional verticality.

```
Start → Intro Area → Challenge 1 → Checkpoint → Challenge 2 → Boss → End
```

**Best for:** Action games, run & gun, linear platformers

**Memory considerations:**
- Load level in segments if large
- Unload off-screen sections
- Pre-load upcoming section during gameplay

### Hub-Based
Central hub connecting to multiple levels.

```
         Level A
            ↑
Level D ← HUB → Level B
            ↓
         Level C
```

**Best for:** Metroidvania, exploration, RPG elements

**Memory considerations:**
- Keep hub small (~100KB)
- Swap level data when entering/exiting
- Maintain player state separately

### Endless/Procedural
Infinitely generating segments.

```
[Segment Pool] → [Current Segment] → [Next Segment] → [Generate Next]
```

**Best for:** Runners, roguelites, high-score chasers

**Memory considerations:**
- Pool of segment templates
- Generate ahead, destroy behind
- Seed-based for determinism (multiplayer)

---

## Movement Systems

### Platform Physics

**Core Variables:**
| Variable | Typical Value | Feel Impact |
|----------|---------------|-------------|
| Gravity | 0.5-1.0 units/frame² | Higher = snappy |
| Jump velocity | 8-15 units/frame | Higher = higher jump |
| Max fall speed | 12-20 units/frame | Terminal velocity |
| Run acceleration | 0.5-1.5 units/frame² | Higher = responsive |
| Max run speed | 4-8 units/frame | Game pace |
| Air control | 0.3-0.8 multiplier | Higher = more air control |

**Coyote Time:**
Allow jump for a few frames after leaving platform:
```
coyote_frames = 6  // About 0.1 seconds at 60fps
```

**Jump Buffering:**
Remember jump input for a few frames before landing:
```
jump_buffer_frames = 8  // About 0.13 seconds at 60fps
```

### Variable Jump Height
Allow higher jumps by holding button:
```
if jump_button_released and velocity_y < 0:
    velocity_y *= 0.5  // Cut upward velocity
```

---

## Camera Systems

### Basic Follow
Camera follows player with some offset:
```
camera_x = player_x - screen_width/2 + look_ahead
camera_y = player_y - screen_height/2 + vertical_offset
```

### Lookahead
Camera leads in movement direction:
```
if player_facing_right:
    target_x = player_x + lookahead_distance
else:
    target_x = player_x - lookahead_distance

camera_x = lerp(camera_x, target_x, 0.1)
```

### Lock Zones
Lock camera in specific areas:
```
if in_boss_room:
    camera_x = boss_room_center_x
    camera_y = boss_room_center_y
```

### Vertical Smoothing
Only follow vertically when grounded:
```
if player_grounded:
    target_y = player_y + offset
    camera_y = lerp(camera_y, target_y, 0.1)
// Else: keep current Y
```

---

## Enemy Patterns

### Ground Walker
Basic back-and-forth patrol:
```
if facing_right and hit_wall_right:
    turn_left()
elif facing_left and hit_wall_left:
    turn_right()
elif facing_right and no_ground_ahead_right:
    turn_left()  // Don't walk off ledges
elif facing_left and no_ground_ahead_left:
    turn_right()
```

### Jumper
Periodically jumps toward player:
```
jump_timer -= 1
if jump_timer <= 0:
    direction = sign(player_x - self_x)
    velocity_x = jump_horizontal_speed * direction
    velocity_y = jump_vertical_speed
    jump_timer = jump_cooldown
```

### Flyer
Sine wave or pursuit flight:
```
// Sine wave
y = base_y + sin(time * frequency) * amplitude

// Pursuit
direction = normalize(player_position - self_position)
velocity = direction * fly_speed
```

### Shooter
Stationary or mobile with projectile attacks:
```
if can_see_player:
    shoot_timer -= 1
    if shoot_timer <= 0:
        spawn_projectile(toward_player)
        shoot_timer = shoot_cooldown
```

---

## Collision Detection

### Tile-Based
Simple and performant:
```
function get_tile(x, y):
    tile_x = floor(x / TILE_SIZE)
    tile_y = floor(y / TILE_SIZE)
    return tilemap[tile_y][tile_x]

function is_solid(x, y):
    return get_tile(x, y).solid
```

### Hitbox Sweep
For precise collision:
```
// Move X first
new_x = position_x + velocity_x
if not collides_at(new_x, position_y):
    position_x = new_x
else:
    // Push out
    while collides_at(position_x + sign(velocity_x), position_y):
        position_x += sign(velocity_x)
    velocity_x = 0

// Then move Y
new_y = position_y + velocity_y
// Similar logic...
```

### Slope Handling
For smooth slopes:
```
if on_slope:
    // Snap to slope surface
    slope_y = get_slope_height_at(position_x)
    position_y = slope_y
    grounded = true
```

---

## Parallax Backgrounds

### Layer Setup
| Layer | Scroll Rate | Content |
|-------|-------------|---------|
| 0 (back) | 0.1 | Sky, distant mountains |
| 1 | 0.3 | Far buildings, trees |
| 2 | 0.5 | Mid-ground decoration |
| 3 | 0.7 | Near decoration |
| 4 | 1.0 | Main gameplay layer |
| 5 (front) | 1.2 | Foreground decoration |

### Implementation
```
for each layer in layers:
    layer_offset_x = camera_x * layer.scroll_rate
    draw_layer(layer, layer_offset_x)
```

### Looping Backgrounds
For infinite scrolling:
```
offset = (camera_x * scroll_rate) % layer_width
if offset < 0:
    offset += layer_width
draw_layer_at(-offset)
draw_layer_at(layer_width - offset)  // Seamless wrap
```

---

## Checkpoint System

### Save Point Design
```
struct Checkpoint {
    position: Point,
    activated: bool,
    world_state: WorldStateSnapshot,
}

struct WorldStateSnapshot {
    collected_items: BitSet,
    unlocked_doors: BitSet,
    defeated_bosses: BitSet,
}
```

### Respawn Logic
```
function respawn():
    player_position = current_checkpoint.position
    restore_world_state(current_checkpoint.world_state)
    player_health = max_health
```

---

## Power-Up Patterns

### Temporary Power-Up
```
struct TemporaryPowerUp {
    type: PowerUpType,
    remaining_frames: u16,
}

function update_powerups():
    for powerup in active_powerups:
        powerup.remaining_frames -= 1
        if powerup.remaining_frames <= 0:
            remove_powerup(powerup)
```

### Stackable Power-Up
```
player.speed_boosts += 1
player.max_speed = base_speed + (speed_boost_amount * player.speed_boosts)
```

### Equipment Power-Up
```
struct Equipment {
    slot: EquipmentSlot,
    item: EquipmentItem,
}

function equip(item):
    unequip(item.slot)
    player.equipment[item.slot] = item
    apply_stat_changes(item)
```

---

## Screen Transitions

### Fade Transition
```
transition_frames = 30  // 0.5 seconds at 60fps

function update_transition():
    if transitioning_out:
        fade_alpha += (255 / transition_frames)
        if fade_alpha >= 255:
            load_new_area()
            transitioning_in = true
            transitioning_out = false
    elif transitioning_in:
        fade_alpha -= (255 / transition_frames)
        if fade_alpha <= 0:
            transitioning_in = false
```

### Slide Transition
For connected rooms:
```
function update_slide():
    slide_progress += slide_speed
    old_room_offset = -slide_progress * screen_width
    new_room_offset = screen_width - (slide_progress * screen_width)

    if slide_progress >= 1.0:
        transition_complete()
```

---

## Memory Optimization

### Entity Pooling
```
const MAX_ENEMIES = 20
const MAX_PROJECTILES = 50

struct EntityPool<T> {
    entities: [Option<T>; MAX],
    active_count: u16,
}

function spawn(pool, entity):
    for i in 0..pool.entities.len():
        if pool.entities[i].is_none():
            pool.entities[i] = Some(entity)
            pool.active_count += 1
            return i
    return POOL_FULL
```

### Level Streaming
For large levels:
```
const CHUNK_SIZE = 256  // tiles

struct LevelChunk {
    tiles: [Tile; CHUNK_SIZE * 16],
    entities: Vec<EntityDef>,
}

function update_chunks():
    current_chunk = floor(camera_x / (CHUNK_SIZE * TILE_SIZE))
    for chunk in chunks:
        if abs(chunk.index - current_chunk) > 1:
            unload_chunk(chunk)
        else:
            ensure_loaded(chunk)
```

---

## ZX-Specific Considerations

### Render Mode Selection
- **Mode 0 (Lambert):** Best for pure 2D sprites
- **Mode 3 (Blinn-Phong):** For 2.5D with 3D-rendered sprites

### Resolution Usage
- 960×540 is wide — good for horizontal scrolling
- Consider letterboxing for vertical-focused sections
- UI safe zones: 48px from edges

### Texture Budget
For a typical side-scroller:
- Player sprites: ~500KB (all animations)
- Enemies (10 types): ~1MB
- Tileset: ~500KB
- Backgrounds: ~1MB
- Effects: ~500KB
- Total: ~3.5MB (fits comfortably)
