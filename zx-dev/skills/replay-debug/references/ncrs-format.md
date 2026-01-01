# NCRS Format Reference

Complete specification for the Nethercore Replay Script (`.ncrs`) format.

## File Structure

NCRS files use TOML format with a header section and frames array:

```toml
# Header (required)
console = "zx"
seed = 12345
players = 2

# Frames array - inline table syntax (compact)
frames = [
  { f = 0, p1 = "idle", p2 = "idle" },
  { f = 1, p1 = "a", p2 = "idle", snap = true },
]

# OR - expanded syntax (more readable for complex frames)
[[frames]]
f = 0
p1 = "idle"
p2 = "idle"

[[frames]]
f = 1
p1 = "a"
p2 = "idle"
snap = true
assert = "$velocity_y < 0"
```

## Header Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `console` | string | Yes | Console identifier (always `"zx"` for ZX games) |
| `seed` | integer | Yes | Random seed for deterministic execution |
| `players` | integer | Yes | Number of players (1-4) |

## Frame Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `f` | integer | Yes | Frame number (0-indexed) |
| `p1` | string/object | No | Player 1 input |
| `p2` | string/object | No | Player 2 input |
| `p3` | string/object | No | Player 3 input |
| `p4` | string/object | No | Player 4 input |
| `snap` | boolean | No | Capture debug variable snapshot |
| `assert` | string | No | Assertion condition to evaluate |
| `action` | string | No | Debug action to invoke (by name) |
| `action_params` | object | No | Parameters for the debug action |

## Input Formats

### Symbolic Format (Recommended)

Use button names, combine with `+`:

```toml
frames = [
  { f = 0, p1 = "idle" },          # No buttons pressed
  { f = 1, p1 = "a" },              # Just A button
  { f = 2, p1 = "right" },          # Just right
  { f = 3, p1 = "right+a" },        # Right + A (move and jump)
  { f = 4, p1 = "up+right+b" },     # Diagonal + button
]
```

### Button Names (ZX Console)

**D-Pad:**
- `up`, `down`, `left`, `right`

**Face Buttons:**
- `a`, `b`, `x`, `y`

**Shoulder Buttons:**
- `l`, `r`, `l2`, `r2`

**System:**
- `start`, `select`

**Special:**
- `idle` - No buttons pressed (0x00)

### Hex Format

Raw byte value for exact input specification:

```toml
frames = [
  { f = 0, p1 = 0x00 },   # idle
  { f = 1, p1 = 0x10 },   # A button
  { f = 2, p1 = 0x18 },   # A + right
]
```

### Analog Input Format

For consoles with analog sticks (not typically used on ZX):

```toml
[[frames]]
f = 0
[frames.p1]
buttons = ["a"]
lstick = [1.0, 0.0]     # Full right
rstick = [0.0, 0.0]     # Neutral
lt = 0.0                 # Left trigger
rt = 0.8                 # Right trigger (partial)
```

**Analog Fields:**
- `lstick = [x, y]` - Left stick (-1.0 to 1.0)
- `rstick = [x, y]` - Right stick (-1.0 to 1.0)
- `lt` - Left trigger (0.0 to 1.0)
- `rt` - Right trigger (0.0 to 1.0)
- `buttons = ["a", "b"]` - Digital buttons

## Snapshot Flag

When `snap = true` is set on a frame:

1. Capture ALL debug-registered variables BEFORE `update()`
2. Execute `update()` with the given inputs
3. Capture ALL debug-registered variables AFTER `update()`
4. Include the pre/post values and delta in the execution report

```toml
frames = [
  { f = 59, p1 = "idle", snap = true },   # Capture state before jump
  { f = 60, p1 = "a", snap = true },       # Capture during jump input
  { f = 61, p1 = "a", snap = true },       # Capture next frame
]
```

Report output for snapped frames:

```json
{
  "frame": 60,
  "input": "a",
  "pre": {
    "$player_y": 100,
    "$velocity_y": 0,
    "$on_ground": true
  },
  "post": {
    "$player_y": 99.5,
    "$velocity_y": -8.0,
    "$on_ground": false
  },
  "delta": {
    "$player_y": -0.5,
    "$velocity_y": -8.0,
    "$on_ground": "true -> false"
  }
}
```

## Assertion Flag

Assertions evaluate conditions AFTER `update()` using debug variable values:

```toml
frames = [
  { f = 1, p1 = "a", assert = "$velocity_y < 0" },
  { f = 5, p1 = "idle", assert = "$on_ground == false" },
  { f = 60, p1 = "idle", assert = "$health >= 50" },
]
```

### Supported Operators

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

### Assertion Report Output

```json
{
  "assertions": [
    {
      "frame": 1,
      "condition": "$velocity_y < 0",
      "passed": true,
      "actual": -8.0
    },
    {
      "frame": 60,
      "condition": "$health >= 50",
      "passed": false,
      "actual": 45,
      "expected": ">= 50"
    }
  ]
}
```

### Combined snap + assert

Capture state AND verify condition in one frame:

```toml
frames = [
  { f = 1, p1 = "a", snap = true, assert = "$velocity_y < 0" },
]
```

## Debug Variables

Variables are registered in game code with `debug_register_*` functions:

```rust
// Registration
debug_register_f32(b"player_x", 8, &PLAYER_X);

// In NCRS, reference as $player_x
assert = "$player_x > 100"
```

### Common Variable Names

| Variable | Type | Typical Use |
|----------|------|-------------|
| `$player_x` | f32 | Horizontal position |
| `$player_y` | f32 | Vertical position |
| `$velocity_x` | f32 | Horizontal velocity |
| `$velocity_y` | f32 | Vertical velocity |
| `$on_ground` | bool | Grounded state |
| `$health` | i32/f32 | Player health |
| `$score` | i32 | Game score |
| `$frame` | u32 | Frame counter |

### Finding Available Variables

Grep game code for registered variables:

```bash
grep -r "debug_register" src/
```

## Debug Actions

Debug actions are callable functions registered by games that can be invoked from scripts. Use them to skip menus, load specific levels, or set up test scenarios without lengthy input sequences.

### Registering Actions (Game Code)

Actions are registered using the `debug_action_*` FFI functions:

```rust
// Register action with parameters
debug_action_begin(b"Load Level".as_ptr(), 10, b"debug_load_level".as_ptr(), 16);
debug_action_param_i32(b"level".as_ptr(), 5, 1);  // "level" param, default 1
debug_action_end();

// Action with multiple parameters
debug_action_begin(b"Set Position".as_ptr(), 12, b"debug_set_pos".as_ptr(), 13);
debug_action_param_f32(b"x".as_ptr(), 1, 0.0);
debug_action_param_f32(b"y".as_ptr(), 1, 0.0);
debug_action_end();

// Boolean parameter
debug_action_begin(b"God Mode".as_ptr(), 8, b"debug_god_mode".as_ptr(), 14);
debug_action_param_bool(b"enabled".as_ptr(), 7, false);
debug_action_end();
```

### Finding Available Actions

```bash
grep -r "debug_action_begin" src/
```

### Using Actions in Scripts

Actions are invoked using the `action` and `action_params` frame fields:

```toml
# Invoke action with parameters
[[frames]]
f = 0
action = "Load Level"
action_params = { level = 2 }

# Invoke action without parameters
[[frames]]
f = 0
action = "Skip Menu"

# Continue testing after action
[[frames]]
f = 1
p1 = "idle"
snap = true
```

### Parameter Types

| FFI Function | TOML Syntax | Example |
|--------------|-------------|---------|
| `debug_action_param_i32` | `{ name = 42 }` | `{ level = 2 }` |
| `debug_action_param_f32` | `{ name = 1.5 }` | `{ x = 100.0 }` |
| `debug_action_param_bool` | `{ name = true }` | `{ enabled = true }` |

### Common Actions

| Action | Parameters | Use Case |
|--------|------------|----------|
| Load Level | `{ level = N }` | Skip to specific level |
| Set Position | `{ x, y }` | Place player for collision tests |
| Set Health | `{ health = N }` | Test low-health scenarios |
| Spawn Enemy | `{ type, x, y }` | Create specific test scenarios |
| Skip Menu | (none) | Bypass title/menu screens |
| God Mode | `{ enabled = bool }` | Isolate mechanics from damage |

### Why Use Actions?

**Instead of:**
- Recording 5 minutes of menu navigation
- Playing through tutorial levels
- Manually positioning enemies

**Use:**
- `action = "Load Level"` to skip to specific levels
- `action = "Set Position"` to place player at exact coordinates
- `action = "Spawn Enemy"` to create targeted test scenarios

**Benefits:**
- **Faster execution** - Skip irrelevant gameplay
- **Focused tests** - Test exactly what matters
- **Less brittle** - Immune to menu/UI changes
- **Reusable** - Same action works across scripts

## Execution Report Format

Complete report structure:

```json
{
  "version": "1.0",
  "script": "jump_test.ncrs",
  "executed_at": "2025-01-15T14:30:00Z",
  "duration_ms": 523,
  "frames_executed": 30,

  "registered_variables": [
    { "name": "$player_x", "type": "f32", "description": "Player X position" },
    { "name": "$velocity_y", "type": "f32", "description": "Vertical velocity" },
    { "name": "$on_ground", "type": "bool", "description": "Is player grounded" }
  ],

  "snapshots": [
    {
      "frame": 0,
      "input": "idle",
      "pre": { "$player_x": 100, "$velocity_y": 0 },
      "post": { "$player_x": 100, "$velocity_y": 0 },
      "delta": {}
    },
    {
      "frame": 1,
      "input": "a",
      "pre": { "$player_x": 100, "$velocity_y": 0, "$on_ground": true },
      "post": { "$player_x": 100, "$velocity_y": -8.0, "$on_ground": false },
      "delta": { "$velocity_y": -8.0, "$on_ground": "true -> false" }
    }
  ],

  "assertions": [
    { "frame": 1, "condition": "$velocity_y < 0", "passed": true, "actual": -8.0 }
  ],

  "summary": {
    "frames_with_snap": 2,
    "assertions_passed": 1,
    "assertions_failed": 0,
    "total_frames": 30,
    "status": "PASSED"
  }
}
```

## CLI Commands

### Run Script

```bash
# Basic execution
nether replay run test.ncrs

# With JSON report output
nether replay run test.ncrs --report report.json

# Headless (no window, max speed)
nether replay run test.ncrs --headless

# Stop on first assertion failure
nether replay run test.ncrs --fail-fast

# With timeout (for CI)
nether replay run test.ncrs --timeout 60

# Batch run
nether replay run tests/*.ncrs --report-dir ./results/
```

### Validate Syntax

```bash
nether replay validate test.ncrs
```

### Convert Formats

```bash
# Script to binary
nether replay compile test.ncrs --output test.ncrp

# Binary to script
nether replay decompile session.ncrp --output session.ncrs
```

### Record New Script

```bash
# Record gameplay to script format
nether play game.rom --record session.ncrs
```

## Example Scripts

### Movement Test

```toml
# Test: Holding right increases X position
console = "zx"
seed = 0
players = 1

frames = [
  { f = 0, p1 = "idle", snap = true },
  { f = 1, p1 = "right" },
  { f = 2, p1 = "right" },
  { f = 30, p1 = "right", snap = true, assert = "$player_x > 100" },
]
```

### Jump Test

```toml
# Test: Press A to jump
console = "zx"
seed = 0
players = 1

frames = [
  { f = 0, p1 = "idle", snap = true },
  { f = 1, p1 = "a", snap = true, assert = "$velocity_y < 0" },
  { f = 2, p1 = "a", snap = true, assert = "$on_ground == false" },
  { f = 30, p1 = "idle", snap = true },
]
```

### Collision Test

```toml
# Test: Player stops at wall
console = "zx"
seed = 0
players = 1

frames = [
  { f = 0, p1 = "right", snap = true },
  { f = 30, p1 = "right", snap = true },   # Approach wall
  { f = 60, p1 = "right", snap = true },   # Should be stopped
  { f = 90, p1 = "right", snap = true },   # Position unchanged
]
```

### Physics Analysis

```toml
# Debug: Frame-by-frame jump physics
console = "zx"
seed = 0
players = 1

frames = [
  { f = 0, p1 = "idle", snap = true },   # Ground state
  { f = 1, p1 = "a", snap = true },       # Jump pressed
  { f = 2, p1 = "idle", snap = true },    # Released
  { f = 3, p1 = "idle", snap = true },    # Rising
  { f = 4, p1 = "idle", snap = true },    # Rising
  { f = 5, p1 = "idle", snap = true },    # Near peak
  { f = 6, p1 = "idle", snap = true },    # Peak
  { f = 7, p1 = "idle", snap = true },    # Falling
  { f = 8, p1 = "idle", snap = true },    # Falling
]
```

### Action-Based Setup

```toml
# Test: Boss fight on level 3
console = "zx"
seed = 42
players = 1

# Setup phase - skip to level 3 and position player
[[frames]]
f = 0
action = "Load Level"
action_params = { level = 3 }

[[frames]]
f = 1
action = "Set Position"
action_params = { x = 100.0, y = 50.0 }

# Now test the boss fight
[[frames]]
f = 2
p1 = "idle"
snap = true

[[frames]]
f = 3
p1 = "a"
snap = true
assert = "$velocity_y < 0"

# Continue testing...
```

## Best Practices

1. **Start with frame 0 snap** - Always capture initial state
2. **Use actions for setup** - Skip menus and level navigation with debug actions
3. **Minimal scripts** - Keep under 100 frames when possible
4. **Focused assertions** - Test one behavior per script
5. **Use meaningful seeds** - Different seeds for different test scenarios
6. **Comment complex scripts** - TOML supports `#` comments
7. **Organize by feature** - Group related tests in subdirectories
