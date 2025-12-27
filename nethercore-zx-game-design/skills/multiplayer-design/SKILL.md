---
name: Multiplayer Design for ZX
description: This skill should be used when the user asks about "multiplayer design", "online play", "netcode", "rollback", "GGRS", "determinism", "deterministic gameplay", "input prediction", "netplay testing", "4-player online", or discusses multiplayer game mechanics for Nethercore ZX.
version: 0.1.0
---

# Multiplayer Design for ZX

Comprehensive guidance for designing multiplayer games that work with Nethercore ZX's GGRS rollback netcode. Covers determinism requirements, state design, testing strategies, and multiplayer patterns.

## ZX Multiplayer Capabilities

| Feature | Value |
|---------|-------|
| Max Players | 4 (any mix of local + remote) |
| Netcode | GGRS deterministic rollback |
| Rollback Window | 8 frames typical |
| Rollback Cost | ~2ms for 8 frames (at 60fps) |
| State Snapshot | ~0.25ms per save (50KB state) |

## Rollback Netcode Fundamentals

### How GGRS Works

1. **Input Prediction:** When remote input hasn't arrived, predict it (usually "same as last frame")
2. **State Advance:** Run `update()` with predicted inputs
3. **Correction:** When actual input arrives, if it differs from prediction:
   - Restore previous state snapshot
   - Re-run `update()` with correct inputs
   - Fast-forward to current frame
4. **Smooth Play:** Visual result appears seamless to players

### Why Determinism Matters

For rollback to work, re-running the same inputs **must** produce identical results. Any non-determinism causes **desync** — players see different game states.

**Desync = broken multiplayer.**

## Determinism Requirements

### What MUST Be Deterministic

| System | Requirement |
|--------|-------------|
| Physics | Fixed-point math OR identical floating-point behavior |
| AI | Deterministic decision making, seeded random |
| Animations | Frame-based, not time-based |
| Spawning | Seeded random for positions/timing |
| All gameplay logic | Same inputs → same outputs, always |

### What CAN Break Determinism

**Forbidden in `update()`:**
- `std::time` / system clock
- `rand()` without seeding
- Hash map iteration (order varies by platform)
- Floating-point edge cases (NaN, denormals)
- External I/O

**Use Instead:**
- `tick_count()` FFI for game time
- `random()` FFI for seeded RNG
- Fixed iteration order (arrays, sorted collections)
- Fixed-point math for critical calculations

### Random Number Generation

ZX provides seeded random via FFI:

```rust
// FFI function - deterministic across all clients
fn random() -> u32  // Returns seeded random value
```

**Rules:**
- Initialize RNG seed at match start (shared by all players)
- Call `random()` in identical order across all clients
- Never use external random sources

## State Design for Rollback

### Minimize State Size

Smaller state = faster rollback.

**Target:** < 100 KB for game state

**Good state design:**
```
Game State (~5 KB):
├── Players: 4 × 500 bytes = 2 KB
│   ├── Position (12 bytes)
│   ├── Velocity (12 bytes)
│   ├── Health/damage (8 bytes)
│   ├── State enum (4 bytes)
│   └── Animation frame (4 bytes)
├── Entities: 20 × 100 bytes = 2 KB
├── World state: 500 bytes
├── RNG state: 64 bytes
└── Input buffer: 500 bytes
```

**What to exclude from state:**
- Asset references (immutable, in ROM)
- Cached calculations (can recompute)
- Visual-only data (particles, screen shake)
- Audio state (not gameplay-affecting)

### Separate Rollback vs. Non-Rollback Data

```rust
// MUST be in rollback state
struct GameState {
    players: [PlayerState; 4],
    entities: Vec<Entity>,
    rng_state: u64,
    frame_count: u32,
}

// NOT in rollback state (visual only)
struct VisualState {
    particles: Vec<Particle>,
    screen_shake: f32,
    audio_playing: Vec<SoundId>,
}
```

### State Serialization

State must serialize/deserialize identically:
- Use fixed-size types
- Avoid pointers (use indices/handles)
- Document byte layout
- Test serialization round-trips

## Multiplayer Game Patterns

### Fighting Games

**Ideal for rollback.** Tight input windows, small state.

| Aspect | Recommendation |
|--------|----------------|
| State size | ~5 KB |
| Input complexity | 2-4 buttons + directions |
| Rollback tolerance | 4-8 frames |
| Tick rate | 60 fps |

**Key determinism areas:**
- Hitbox/hurtbox collision
- Combo state machines
- Damage calculation

### Racing Games

**Good for rollback.** Continuous input, moderate state.

| Aspect | Recommendation |
|--------|----------------|
| State size | ~20 KB (4 vehicles + track) |
| Input complexity | Analog steering + buttons |
| Rollback tolerance | 4-6 frames |
| Tick rate | 60 or 120 fps |

**Key determinism areas:**
- Physics simulation
- Collision response
- Position interpolation

### Action/Adventure (Co-op)

**Moderate for rollback.** More entities, larger state.

| Aspect | Recommendation |
|--------|----------------|
| State size | ~50-100 KB |
| Input complexity | Full controller |
| Rollback tolerance | 6-10 frames |
| Tick rate | 30 or 60 fps |

**Key determinism areas:**
- AI decision making
- World state changes
- Entity spawning

### Turn-Based Games

**Easy for netcode.** Can use simpler sync than rollback.

| Aspect | Recommendation |
|--------|----------------|
| State size | Variable |
| Input complexity | Discrete actions |
| Approach | Lockstep or command sync |
| Tick rate | 30 fps or lower |

## Input Handling

### Input Structure

```rust
struct PlayerInput {
    buttons: u16,      // Bitmask of pressed buttons
    left_stick: (i8, i8),  // Quantized -128 to 127
    right_stick: (i8, i8),
    triggers: (u8, u8),    // 0-255
}
```

### Input Delay

Intentional input delay improves online experience:
- **3 frames:** Minimal perceivable delay
- **4-5 frames:** Good balance for most games
- **6+ frames:** Noticeable but still playable

**Why add delay?** More time for inputs to arrive reduces rollbacks.

### Input Buffer

Store recent inputs for rollback:
```
Input Buffer (60 frames × 4 players):
├── Frame N: [P1 input, P2 input, P3 input, P4 input]
├── Frame N-1: [P1 input, P2 input, P3 input, P4 input]
├── ...
└── Frame N-59: [...]
```

## Testing Multiplayer

### Testing Progression

1. **Local Single-Player**
   - Verify basic gameplay
   - No networking involved

2. **Local Multi-Player**
   - 2-4 controllers on same machine
   - Test input handling for all players

3. **Synthetic Desync Test**
   - Run two game instances
   - Feed identical inputs
   - Compare state hashes
   - Any difference = determinism bug

4. **Local Network Test**
   - Two machines on same LAN
   - Low latency, test basic netcode

5. **Simulated Latency**
   - Add artificial delay (50-200ms)
   - Test rollback behavior

6. **Real Online Test**
   - Different networks/regions
   - Various latency conditions

### Desync Debugging

When state differs between clients:

1. **Add state hashing:** Hash game state each frame
2. **Log divergence frame:** Find first frame where hashes differ
3. **Compare state dumps:** What changed?
4. **Check suspects:**
   - Random calls
   - Floating-point precision
   - Hash map iteration
   - Uninitialized memory

### Network Condition Simulation

Test under adverse conditions:
- **Packet loss:** 1-5% simulated drops
- **Jitter:** Variable latency (±50ms)
- **Spikes:** Occasional high latency (200ms+)
- **Disconnect/reconnect:** Brief connection drops

## Design Considerations

### Latency-Tolerant Mechanics

Design mechanics that feel good with latency:

**Good for netplay:**
- Projectiles (travel time masks latency)
- Charging moves (commitment before release)
- Position-based attacks (spacing game)
- Large hitboxes (forgiving)

**Challenging for netplay:**
- Frame-1 reversals (require precise timing)
- Tiny hitboxes (precision suffers)
- Time-critical counters
- Heavy visual feedback on every input

### Visual Smoothing

Hide rollback corrections:

- **Interpolation:** Smooth position between states
- **Animation blending:** Don't snap animations
- **Particle persistence:** Keep particles through rollbacks
- **Audio continuation:** Don't restart sounds on rollback

### Handling Disconnects

Design for connection issues:

- **Timeout detection:** How long before kick?
- **Reconnection:** Can players rejoin?
- **AI takeover:** Does AI control disconnected player?
- **Match pause:** Does game pause for reconnection?

## Additional Resources

### Reference Files

For detailed patterns and checklists:
- **`references/determinism-checklist.md`** — Verification checklist
- **`references/netplay-patterns.md`** — Common multiplayer patterns

### Integration with zx-dev

The zx-dev plugin provides:
- **Rollback Safety Reviewer agent** — Detects non-deterministic code
- FFI documentation for `random()`, `tick_count()`
- State serialization patterns
