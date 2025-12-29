---
name: AI & Behavior Patterns
description: This skill should be used when the user asks about "enemy AI", "state machine", "FSM", "patrol", "pathfinding", "NPC behavior", "chase", "flee", "wander", "AI behavior", "steering behaviors", "line of sight", "aggression", "attack patterns", "behavior tree", "waypoint", "grid pathfinding", "A*", or implements AI systems for Nethercore ZX games.
version: 1.0.0
---

# AI & Behavior Patterns for Nethercore ZX

Enemy AI and NPC behaviors for ZX games. All patterns are deterministic for rollback netcode compatibility.

## Rollback Safety Requirements

AI logic MUST be deterministic:

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Time | `delta_time()`, `tick_count()` | System clock |
| Random | `random()`, `random_range()` | `rand()`, external RNG |
| Iteration | Arrays, `Vec` | HashMap (non-deterministic order) |
| Decisions | Frame-based timers | Real-time delays |

Use `random()` from the FFI for any AI randomness (target selection, patrol delays).

---

## Finite State Machines

The foundation of game AI. Each entity has a current state with defined transitions.

### Basic FSM Pattern

```rust
#[derive(Clone, Copy, PartialEq)]
enum EnemyState {
    Idle,
    Patrol,
    Chase,
    Attack,
    Flee,
}

struct Enemy {
    state: EnemyState,
    x: f32, y: f32,
    health: i16,
    target_x: f32, target_y: f32,
    state_timer: u32,
}

impl Enemy {
    fn update(&mut self, player_x: f32, player_y: f32) {
        match self.state {
            EnemyState::Idle => self.update_idle(player_x, player_y),
            EnemyState::Patrol => self.update_patrol(player_x, player_y),
            EnemyState::Chase => self.update_chase(player_x, player_y),
            EnemyState::Attack => self.update_attack(),
            EnemyState::Flee => self.update_flee(player_x, player_y),
        }
        if self.state_timer > 0 {
            self.state_timer -= 1;
        }
    }

    fn transition(&mut self, new_state: EnemyState) {
        self.state = new_state;
        self.state_timer = 0;  // Reset timer on transition
    }
}
```

### State Transitions

Define clear conditions for state changes:

```rust
const SIGHT_RANGE: f32 = 200.0;
const ATTACK_RANGE: f32 = 30.0;
const FLEE_HEALTH: i16 = 20;

impl Enemy {
    fn update_idle(&mut self, player_x: f32, player_y: f32) {
        let dist = self.distance_to(player_x, player_y);

        if self.health < FLEE_HEALTH {
            self.transition(EnemyState::Flee);
        } else if dist < SIGHT_RANGE && self.can_see_player(player_x, player_y) {
            self.transition(EnemyState::Chase);
        } else if self.state_timer == 0 {
            // Start patrol after idle delay
            self.transition(EnemyState::Patrol);
        }
    }

    fn update_chase(&mut self, player_x: f32, player_y: f32) {
        let dist = self.distance_to(player_x, player_y);

        if self.health < FLEE_HEALTH {
            self.transition(EnemyState::Flee);
        } else if dist < ATTACK_RANGE {
            self.transition(EnemyState::Attack);
        } else if dist > SIGHT_RANGE * 1.5 {
            // Lost sight of player
            self.transition(EnemyState::Idle);
        } else {
            self.move_toward(player_x, player_y);
        }
    }

    fn distance_to(&self, x: f32, y: f32) -> f32 {
        let dx = x - self.x;
        let dy = y - self.y;
        (dx * dx + dy * dy).sqrt()
    }
}
```

---

## Movement Behaviors

Common AI movement patterns.

### Patrol (Waypoint Following)

```rust
struct Patrol {
    waypoints: [(f32, f32); 4],
    current: usize,
    wait_timer: u32,
}

const PATROL_SPEED: f32 = 1.5;
const WAYPOINT_THRESHOLD: f32 = 5.0;
const WAIT_FRAMES: u32 = 60;

impl Enemy {
    fn update_patrol(&mut self, player_x: f32, player_y: f32) {
        // Check for player detection first
        if self.distance_to(player_x, player_y) < SIGHT_RANGE {
            if self.can_see_player(player_x, player_y) {
                self.transition(EnemyState::Chase);
                return;
            }
        }

        // Handle waiting at waypoint
        if self.patrol.wait_timer > 0 {
            self.patrol.wait_timer -= 1;
            return;
        }

        // Move toward current waypoint
        let (wx, wy) = self.patrol.waypoints[self.patrol.current];
        let dist = self.distance_to(wx, wy);

        if dist < WAYPOINT_THRESHOLD {
            // Reached waypoint, advance to next
            self.patrol.current = (self.patrol.current + 1) % self.patrol.waypoints.len();
            self.patrol.wait_timer = WAIT_FRAMES;
        } else {
            self.move_toward(wx, wy);
        }
    }
}
```

### Chase (Follow Target)

```rust
const CHASE_SPEED: f32 = 2.5;

impl Enemy {
    fn move_toward(&mut self, target_x: f32, target_y: f32) {
        let dx = target_x - self.x;
        let dy = target_y - self.y;
        let dist = (dx * dx + dy * dy).sqrt();

        if dist > 0.1 {
            self.x += (dx / dist) * CHASE_SPEED;
            self.y += (dy / dist) * CHASE_SPEED;
        }
    }
}
```

### Flee (Run Away)

```rust
const FLEE_SPEED: f32 = 3.0;
const SAFE_DISTANCE: f32 = 300.0;

impl Enemy {
    fn update_flee(&mut self, player_x: f32, player_y: f32) {
        let dist = self.distance_to(player_x, player_y);

        if dist > SAFE_DISTANCE {
            self.transition(EnemyState::Idle);
            return;
        }

        // Move away from player
        let dx = self.x - player_x;
        let dy = self.y - player_y;
        let len = (dx * dx + dy * dy).sqrt();

        if len > 0.1 {
            self.x += (dx / len) * FLEE_SPEED;
            self.y += (dy / len) * FLEE_SPEED;
        }
    }
}
```

### Wander (Random Movement)

```rust
const WANDER_SPEED: f32 = 1.0;
const DIRECTION_CHANGE_FRAMES: u32 = 90;

impl Enemy {
    fn update_wander(&mut self) {
        if self.state_timer == 0 {
            // Pick new random direction
            let angle = random() * core::f32::consts::TAU;
            self.target_x = self.x + angle.cos() * 50.0;
            self.target_y = self.y + angle.sin() * 50.0;
            self.state_timer = DIRECTION_CHANGE_FRAMES;
        }

        self.move_toward_speed(self.target_x, self.target_y, WANDER_SPEED);
    }

    fn move_toward_speed(&mut self, target_x: f32, target_y: f32, speed: f32) {
        let dx = target_x - self.x;
        let dy = target_y - self.y;
        let dist = (dx * dx + dy * dy).sqrt();

        if dist > speed {
            self.x += (dx / dist) * speed;
            self.y += (dy / dist) * speed;
        }
    }
}
```

---

## Sensing

### Line-of-Sight Detection

Use raycasting from the physics skill for visibility checks:

```rust
impl Enemy {
    fn can_see_player(&self, player_x: f32, player_y: f32) -> bool {
        let dx = player_x - self.x;
        let dy = player_y - self.y;
        let dist = (dx * dx + dy * dy).sqrt();

        if dist > SIGHT_RANGE {
            return false;
        }

        // Raycast to check for obstacles
        let ray = Ray {
            origin: [self.x, self.y, 0.0],
            direction: [dx / dist, dy / dist, 0.0],
        };

        // Check against world geometry
        for wall in &WORLD_WALLS {
            if let Some(t) = ray.intersect_aabb(wall) {
                if t < dist {
                    return false;  // Wall blocks view
                }
            }
        }
        true
    }
}
```

### Proximity Detection (Hearing)

Simple distance-based awareness:

```rust
const HEARING_RANGE: f32 = 100.0;

impl Enemy {
    fn can_hear_player(&self, player_x: f32, player_y: f32, player_running: bool) -> bool {
        let range = if player_running { HEARING_RANGE * 1.5 } else { HEARING_RANGE };
        self.distance_to(player_x, player_y) < range
    }
}
```

### Memory (Last Known Position)

Track where the player was last seen:

```rust
struct Enemy {
    last_known_x: f32,
    last_known_y: f32,
    memory_timer: u32,
    // ...
}

const MEMORY_DURATION: u32 = 180;  // 3 seconds at 60fps

impl Enemy {
    fn update_memory(&mut self, player_x: f32, player_y: f32) {
        if self.can_see_player(player_x, player_y) {
            self.last_known_x = player_x;
            self.last_known_y = player_y;
            self.memory_timer = MEMORY_DURATION;
        } else if self.memory_timer > 0 {
            self.memory_timer -= 1;
        }
    }

    fn has_memory(&self) -> bool {
        self.memory_timer > 0
    }
}
```

---

## Steering Behaviors

Simple physics-based movement for smooth AI.

### Seek and Arrive

```rust
const MAX_SPEED: f32 = 3.0;
const ARRIVE_RADIUS: f32 = 50.0;

fn seek(current: [f32; 2], target: [f32; 2]) -> [f32; 2] {
    let dx = target[0] - current[0];
    let dy = target[1] - current[1];
    let dist = (dx * dx + dy * dy).sqrt();

    if dist > 0.1 {
        [dx / dist * MAX_SPEED, dy / dist * MAX_SPEED]
    } else {
        [0.0, 0.0]
    }
}

fn arrive(current: [f32; 2], target: [f32; 2]) -> [f32; 2] {
    let dx = target[0] - current[0];
    let dy = target[1] - current[1];
    let dist = (dx * dx + dy * dy).sqrt();

    if dist < 0.1 {
        return [0.0, 0.0];
    }

    // Slow down when approaching target
    let speed = if dist < ARRIVE_RADIUS {
        MAX_SPEED * (dist / ARRIVE_RADIUS)
    } else {
        MAX_SPEED
    };

    [dx / dist * speed, dy / dist * speed]
}
```

---

## Combat AI

### Attack Pattern with Cooldown

```rust
const ATTACK_COOLDOWN: u32 = 45;
const ATTACK_WINDUP: u32 = 15;
const ATTACK_ACTIVE: u32 = 10;

struct Enemy {
    attack_cooldown: u32,
    attack_frame: u32,
    // ...
}

impl Enemy {
    fn update_attack(&mut self) {
        if self.attack_frame == 0 && self.attack_cooldown == 0 {
            // Start attack windup
            self.attack_frame = ATTACK_WINDUP + ATTACK_ACTIVE;
        }

        if self.attack_frame > 0 {
            self.attack_frame -= 1;

            // Attack is active during specific frames
            if self.attack_frame < ATTACK_ACTIVE && self.attack_frame > 0 {
                // Check hitbox collision with player
            }

            if self.attack_frame == 0 {
                self.attack_cooldown = ATTACK_COOLDOWN;
                self.transition(EnemyState::Chase);
            }
        }

        if self.attack_cooldown > 0 {
            self.attack_cooldown -= 1;
        }
    }

    fn can_attack(&self) -> bool {
        self.attack_cooldown == 0 && self.attack_frame == 0
    }
}
```

### Aggression Levels

```rust
#[derive(Clone, Copy)]
enum Aggression {
    Passive,    // Won't attack unless attacked
    Defensive,  // Attacks if player gets too close
    Aggressive, // Actively hunts player
}

impl Enemy {
    fn should_chase(&self, player_dist: f32) -> bool {
        match self.aggression {
            Aggression::Passive => self.was_damaged,
            Aggression::Defensive => player_dist < SIGHT_RANGE * 0.5,
            Aggression::Aggressive => player_dist < SIGHT_RANGE,
        }
    }
}
```

---

## Additional Resources

### Reference Files

- **`references/advanced-fsm.md`** — Hierarchical state machines, behavior tree basics
- **`references/pathfinding-algorithms.md`** — Grid A*, waypoint graphs, navigation meshes

### Related Skills

- **`physics-collision`** — Raycasting for line-of-sight detection
- **`gameplay-mechanics`** — Combat systems, hitboxes for AI attacks
- **`multiplayer-design`** — Determinism requirements for AI state
