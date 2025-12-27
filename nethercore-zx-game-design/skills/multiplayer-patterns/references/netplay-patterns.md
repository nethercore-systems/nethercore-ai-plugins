# Netplay Design Patterns

Common multiplayer patterns for Nethercore ZX games with GGRS rollback netcode.

## Fighting Game Pattern

The gold standard for rollback netcode.

### State Structure
```rust
struct FightingGameState {
    // Per-player state (~200 bytes each)
    players: [PlayerState; 4],

    // Match state
    timer: u16,
    round: u8,

    // RNG for any random elements
    rng_state: u64,
}

struct PlayerState {
    position: FixedPoint2D,      // 8 bytes
    velocity: FixedPoint2D,      // 8 bytes
    facing: i8,                  // 1 byte
    health: u16,                 // 2 bytes
    meter: u16,                  // 2 bytes
    state: CharacterState,       // 4 bytes (enum)
    state_frame: u16,            // 2 bytes
    hitstun: u8,                 // 1 byte
    blockstun: u8,               // 1 byte
    input_buffer: [u16; 10],     // 20 bytes
    // ~50 bytes per player
}
```

### Input Handling
```rust
struct FightingInput {
    buttons: u16,  // Bitmask
    // Button layout:
    // 0: Up, 1: Down, 2: Left, 3: Right
    // 4: A (Light), 5: B (Heavy), 6: X (Special), 7: Y (Throw)
    // 8: L1 (Block), 9: R1 (Dash)
}
```

### Frame Advantage Design
- Design moves with rollback in mind
- Avoid moves that require frame-perfect reactions
- Build in input buffer (6+ frames)
- Use hitstop to mask latency

---

## Racing Game Pattern

Continuous input with interpolation needs.

### State Structure
```rust
struct RacingGameState {
    vehicles: [VehicleState; 4],
    track_objects: Vec<TrackObject>,
    lap_data: [LapInfo; 4],
    rng_state: u64,
}

struct VehicleState {
    position: FixedPoint3D,      // 12 bytes
    velocity: FixedPoint3D,      // 12 bytes
    rotation: FixedQuat,         // 16 bytes
    angular_velocity: FixedPoint3D,
    throttle: u8,
    steering: i8,
    drift_state: DriftState,
    boost_meter: u16,
}
```

### Input Handling
```rust
struct RacingInput {
    steering: i8,      // -128 to 127
    throttle: u8,      // 0 to 255 (analog)
    brake: u8,         // 0 to 255 (analog)
    buttons: u8,       // Boost, item, etc.
}
```

### Interpolation for Smooth Visuals
- Store previous and current state
- Interpolate for rendering (not gameplay)
- Keep physics deterministic
- Use fixed-point math

---

## Co-op Action Pattern

Shared world with entity management.

### State Structure
```rust
struct CoopGameState {
    players: [CoopPlayerState; 4],
    enemies: EntityPool<Enemy>,  // Fixed-size pool
    projectiles: EntityPool<Projectile>,
    world_state: WorldState,
    rng_state: u64,
}

struct EntityPool<T> {
    entities: [Option<T>; MAX_ENTITIES],
    next_id: u32,
}
```

### Entity Spawning
Deterministic spawning is critical:
```rust
fn spawn_enemy(&mut self, position: FixedPoint3D) {
    // Get next ID deterministically
    let id = self.enemies.next_id;
    self.enemies.next_id += 1;

    // Use seeded random for variation
    let variant = random() % 3;

    // Add to pool
    self.enemies.add(Enemy {
        id,
        position,
        variant,
        health: ENEMY_HEALTH[variant],
    });
}
```

### Entity Removal
Remove in deterministic order:
```rust
fn cleanup_dead_entities(&mut self) {
    // Always process in ID order
    for i in 0..self.enemies.entities.len() {
        if let Some(enemy) = &self.enemies.entities[i] {
            if enemy.health == 0 {
                self.enemies.entities[i] = None;
            }
        }
    }
}
```

---

## Party Game Pattern

Variable rules with spectator support.

### State Structure
```rust
struct PartyGameState {
    players: [PartyPlayerState; 4],
    minigame_state: MinigameState,
    scores: [u32; 4],
    current_round: u8,
    rng_state: u64,
}

enum MinigameState {
    Countdown { frames_left: u16 },
    Playing { minigame_data: Box<dyn MinigameData> },
    Results { winner: Option<u8>, display_timer: u16 },
}
```

### Minigame Isolation
Each minigame has isolated state:
```rust
trait MinigameData: Send + Sync {
    fn update(&mut self, inputs: &[PlayerInput; 4]);
    fn serialize(&self) -> Vec<u8>;
    fn deserialize(data: &[u8]) -> Self;
    fn is_complete(&self) -> bool;
    fn get_rankings(&self) -> [u8; 4];
}
```

---

## Input Delay Recommendations

| Game Type | Recommended Delay | Rollback Frames |
|-----------|-------------------|-----------------|
| Fighting | 3-4 frames | 6-8 |
| Racing | 2-3 frames | 4-6 |
| Action/Co-op | 4-5 frames | 6-10 |
| Party | 3-4 frames | 6-8 |
| Turn-based | 0 (lockstep) | N/A |

---

## Network Quality Handling

### Detecting Poor Connection
```rust
struct ConnectionQuality {
    ping_ms: u32,
    packet_loss_percent: u8,
    jitter_ms: u16,
}

fn assess_quality(quality: &ConnectionQuality) -> QualityLevel {
    if quality.ping_ms < 50 && quality.packet_loss_percent < 1 {
        QualityLevel::Excellent
    } else if quality.ping_ms < 100 && quality.packet_loss_percent < 3 {
        QualityLevel::Good
    } else if quality.ping_ms < 150 && quality.packet_loss_percent < 5 {
        QualityLevel::Fair
    } else {
        QualityLevel::Poor
    }
}
```

### Graceful Degradation
- Increase input delay dynamically
- Show connection indicator to players
- Consider pause on severe degradation
- Log disconnection events for debugging

---

## Spectator Mode Pattern

For games supporting spectators:

```rust
struct SpectatorState {
    // Spectators receive state, don't send input
    game_state: GameState,
    spectator_camera: CameraState,

    // Delay spectator view for fairness
    delay_frames: u16,
    state_buffer: RingBuffer<GameState>,
}
```

### Spectator-Specific Considerations
- Buffer more state for smooth playback
- Allow camera freedom without affecting game
- Delay stream to prevent ghosting
- Compress state for lower bandwidth

---

## Desync Recovery

When desync is detected:

1. **Detect:** Hash mismatch on confirmed frame
2. **Report:** Log which frame and which player desynced
3. **Attempt Recovery:**
   - Request full state from host
   - Pause game briefly
   - Resync all players
4. **If Recovery Fails:**
   - End match gracefully
   - Save replay up to desync
   - Report to developer

```rust
fn on_desync_detected(frame: u32, expected_hash: u64, actual_hash: u64) {
    log_error!("Desync at frame {}: expected {:x}, got {:x}",
               frame, expected_hash, actual_hash);

    if can_recover() {
        request_state_sync();
    } else {
        end_match_with_error(MatchError::Desync);
    }
}
```
