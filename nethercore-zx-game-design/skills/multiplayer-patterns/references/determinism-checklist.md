# Determinism Checklist

Use this checklist to verify your Nethercore ZX game maintains determinism for rollback netcode.

## Pre-Implementation Checklist

Before writing gameplay code:

- [ ] Identified all systems that affect game state
- [ ] Planned RNG seeding strategy
- [ ] Chosen fixed-point or consistent floating-point approach
- [ ] Designed state struct with serialization in mind
- [ ] Documented iteration order for all collections

## Code Review Checklist

For each system in `update()`:

### Random Number Generation
- [ ] All randomness uses `random()` FFI
- [ ] No `std::rand`, `rand::random`, or OS random
- [ ] RNG calls happen in identical order across frames
- [ ] RNG seed initialized from shared match data

### Time and Timing
- [ ] Game time from `tick_count()` FFI only
- [ ] No `std::time`, `SystemTime`, or `Instant`
- [ ] No `chrono` or date/time libraries
- [ ] Animation timing is frame-based, not duration-based

### Collections and Iteration
- [ ] No `HashMap` iteration (order not guaranteed)
- [ ] Use `BTreeMap` or sorted `Vec` instead
- [ ] Fixed iteration order for all entity updates
- [ ] Array indices used consistently

### Floating-Point Math
- [ ] No NaN-producing operations (0/0, sqrt(-1))
- [ ] No infinity from overflow
- [ ] Consider fixed-point for critical calculations
- [ ] Test on target WASM runtime

### Memory and State
- [ ] No uninitialized memory in state
- [ ] All state fields explicitly zeroed
- [ ] No pointer addresses in calculations
- [ ] State size is deterministic

### External Systems
- [ ] No file I/O in update
- [ ] No network calls in update
- [ ] No system calls in update
- [ ] No thread spawning in update

### AI and Decision Making
- [ ] AI decisions use seeded random
- [ ] AI state fully included in game state
- [ ] No timing-based AI (use tick count)
- [ ] Pathfinding is deterministic

### Physics
- [ ] Collision detection order is consistent
- [ ] Physics step is fixed (not delta-time)
- [ ] Contact resolution order is defined
- [ ] Impulse calculations are reproducible

## Testing Checklist

Verification steps:

### Replay Test
- [ ] Record input sequence
- [ ] Replay produces identical state hash
- [ ] Works across multiple replays
- [ ] Works after code changes (regression)

### Dual-Instance Test
- [ ] Run two game instances
- [ ] Feed identical inputs
- [ ] State hashes match every frame
- [ ] Test for extended play sessions (1000+ frames)

### Cross-Platform Test
- [ ] Test on different OS (if applicable)
- [ ] Test on different CPU architectures
- [ ] State hashes match across platforms

### Stress Test
- [ ] Rapid input changes
- [ ] Maximum entity count
- [ ] Edge cases (zero values, maximums)
- [ ] Long play sessions

## Common Bugs by Category

### Bug: Desync after random event
**Cause:** Random calls in different order
**Fix:** Ensure all random calls happen in consistent order, even if result isn't used

### Bug: Desync after entity spawn
**Cause:** Entity iteration order changed
**Fix:** Use stable entity IDs, iterate in ID order

### Bug: Desync during combat
**Cause:** Hash map for collision pairs
**Fix:** Use sorted list or consistent hashing

### Bug: Desync after reconnect
**Cause:** State not fully restored
**Fix:** Verify all state fields serialized/deserialized

### Bug: Gradual drift
**Cause:** Floating-point accumulation
**Fix:** Reset accumulated values periodically, or use fixed-point

## State Hash Implementation

Add state hashing for debugging:

```rust
fn hash_game_state(state: &GameState) -> u64 {
    let mut hasher = XxHash64::with_seed(0);

    // Hash in consistent order
    hasher.write_u32(state.frame_count);
    hasher.write_u64(state.rng_state);

    for player in &state.players {
        hasher.write(&player.position.to_bytes());
        hasher.write(&player.velocity.to_bytes());
        hasher.write_u32(player.state as u32);
    }

    for entity in &state.entities {
        hasher.write_u32(entity.id);
        hasher.write(&entity.position.to_bytes());
    }

    hasher.finish()
}
```

## Debugging Workflow

When desync occurs:

1. **Find divergence frame**
   ```
   Frame 100: Hash A=12345, B=12345 ✓
   Frame 101: Hash A=12345, B=12346 ✗ ← First difference
   ```

2. **Compare states at frame 101**
   - Which field differs?
   - What happened between 100 and 101?

3. **Trace the cause**
   - Was random called?
   - Was iteration order assumed?
   - Was external state accessed?

4. **Fix and verify**
   - Apply fix
   - Re-run dual-instance test
   - Test extended sessions

## Quick Reference Card

### ✓ Safe in `update()`
- `random()` FFI
- `tick_count()` FFI
- Array iteration
- BTreeMap iteration
- Fixed-point math
- Seeded algorithms

### ✗ Forbidden in `update()`
- `std::time`
- `rand::random`
- `HashMap` iteration
- System calls
- File I/O
- Pointer addresses
