# Determinism Rules for ZX Games

ZX uses GGRS rollback netcode requiring 100% deterministic game logic.

## Patterns to Avoid

### Non-Deterministic RNG

```rust
// BAD - Different seeds per instance
let r = rand::thread_rng().gen::<f32>();

// GOOD - GGRS-seeded deterministic RNG
let r = zx::random();
```

### HashMap/HashSet

```rust
// BAD - Iteration order varies
let map: HashMap<K, V> = ...;
for (k, v) in map.iter() { ... }

// GOOD - Sorted iteration
let map: BTreeMap<K, V> = ...;
for (k, v) in map.iter() { ... }
```

### System Time

```rust
// BAD - Wall clock differs between instances
let now = Instant::now();
let elapsed = start.elapsed();

// GOOD - Frame-based timing
let frame = state.frame_count;
let elapsed_frames = frame - start_frame;
```

### Floating-Point

```rust
// BAD - Accumulation errors
position += velocity * 0.016666667;

// GOOD - Fixed-point or integer math
position += velocity / 60;  // Integer division
```

## Search Patterns for Investigation

Common non-deterministic patterns to grep for:

```
rand::thread_rng
HashMap::new
HashSet::new
Instant::now
SystemTime::now
f32::sin  # Transcendental functions can vary
f64::cos
```

## Why These Matter

GGRS rollback netcode:
1. Runs game logic on all clients
2. Compares state checksums
3. Rolls back and resimulates on mismatch

If game logic isn't deterministic, checksums diverge and the game desyncs.

## Testing for Determinism

```bash
# Run sync test - compares two instances
nether run --sync-test --frames 1000

# If it fails at frame N, look for what changed at frame N
# Use desync-investigator agent for detailed analysis
```
