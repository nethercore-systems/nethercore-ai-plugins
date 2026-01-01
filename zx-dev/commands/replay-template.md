---
description: Generate a replay template for common test scenarios
argument-hint: "[type: jump|collision|movement|physics|input|setup]"
allowed-tools: ["AskUserQuestion", "Write", "Grep"]
---

# Generate Replay Template

Create a starter NCRS template for common test scenarios.

## Step 1: Determine Template Type

**If argument provided**, use that template type.

**If no argument**, use AskUserQuestion:

- Question: "Which test template do you want?"
- Header: "Template"
- Options:
  - **setup** - Template using debug actions to skip to specific scenarios
  - **jump** - Test jump mechanics (A button applies velocity)
  - **collision** - Test wall/platform collision detection
  - **movement** - Test left/right movement and stopping
  - **physics** - Frame-by-frame physics analysis (detailed snaps)
  - **input** - Test button combinations and input handling

## Step 2: Create Test Directory

Ensure tests/replay/ exists:

```bash
mkdir -p tests/replay
```

## Step 3: Generate Template

### Setup Template

**File:** `tests/replay/setup_template.ncrs`

First, discover available debug actions:

```bash
grep -r "debug_action_begin" src/
```

Then generate a template using found actions:

```toml
# Action-Based Test Setup Template
# Uses debug actions to skip menus and set up specific test scenarios
# Replace action names and params with those registered in your game

console = "zx"
seed = 42
players = 1

# === SETUP PHASE ===
# Use debug actions to skip menus and get to test state

# Skip menu (if registered)
[[frames]]
f = 0
action = "Skip Menu"

# Load specific level (if registered)
[[frames]]
f = 1
action = "Load Level"
action_params = { level = 3 }

# Position player at specific location (if registered)
[[frames]]
f = 2
action = "Set Position"
action_params = { x = 100.0, y = 50.0 }

# Set health for edge case testing (if registered)
[[frames]]
f = 3
action = "Set Health"
action_params = { health = 1 }

# === TEST PHASE ===
# Now run the actual test

[[frames]]
f = 4
p1 = "idle"
snap = true

# Perform action to test
[[frames]]
f = 5
p1 = "a"
snap = true
assert = "$velocity_y < 0"

# Continue testing...
[[frames]]
f = 10
p1 = "idle"
snap = true
```

**Note:** Remove actions that aren't registered in your game. Check `grep -r "debug_action_begin" src/` output for available actions and their parameter names.

### Jump Template

**File:** `tests/replay/jump_template.ncrs`

```toml
# Jump Mechanics Test Template
# Modify assertions based on your game's jump parameters
# Expected: velocity_y goes negative when A pressed while grounded

console = "zx"
seed = 0
players = 1

frames = [
  # Initial state - should be on ground
  { f = 0, p1 = "idle", snap = true },

  # Jump input - velocity should go negative
  { f = 1, p1 = "a", snap = true, assert = "$velocity_y < 0" },

  # Airborne check
  { f = 2, p1 = "a", snap = true, assert = "$on_ground == false" },

  # Release and continue rising
  { f = 5, p1 = "idle", snap = true },

  # Peak of jump
  { f = 15, p1 = "idle", snap = true },

  # Falling
  { f = 25, p1 = "idle", snap = true },

  # Landed
  { f = 50, p1 = "idle", snap = true, assert = "$on_ground == true" },
]
```

### Collision Template

**File:** `tests/replay/collision_template.ncrs`

```toml
# Collision Detection Test Template
# Tests that player stops when hitting a wall
# Modify frame numbers based on wall distance from spawn

console = "zx"
seed = 0
players = 1

frames = [
  # Starting position
  { f = 0, p1 = "idle", snap = true },

  # Begin moving toward wall
  { f = 1, p1 = "right" },

  # Moving - position should increase
  { f = 30, p1 = "right", snap = true },

  # Continue toward wall
  { f = 60, p1 = "right", snap = true },

  # At wall - compare these snapshots
  { f = 90, p1 = "right", snap = true },

  # Still pressing - position should NOT change
  { f = 100, p1 = "right", snap = true },
  { f = 110, p1 = "right", snap = true },

  # Release
  { f = 120, p1 = "idle", snap = true },
]
```

### Movement Template

**File:** `tests/replay/movement_template.ncrs`

```toml
# Movement Test Template
# Tests basic horizontal movement and stopping
# Adjust assertions based on your game's movement speed

console = "zx"
seed = 0
players = 1

frames = [
  # Initial state
  { f = 0, p1 = "idle", snap = true },

  # Move right - velocity should be positive
  { f = 1, p1 = "right", snap = true },
  { f = 10, p1 = "right", snap = true },

  # Stop - velocity should return to 0
  { f = 20, p1 = "idle", snap = true },
  { f = 25, p1 = "idle", snap = true },

  # Move left - velocity should be negative
  { f = 30, p1 = "left", snap = true },
  { f = 40, p1 = "left", snap = true },

  # Stop again
  { f = 50, p1 = "idle", snap = true },

  # Diagonal movement
  { f = 60, p1 = "right+up", snap = true },
  { f = 70, p1 = "left+down", snap = true },

  # Final state
  { f = 80, p1 = "idle", snap = true },
]
```

### Physics Template

**File:** `tests/replay/physics_template.ncrs`

```toml
# Physics Analysis Template
# Frame-by-frame capture for detailed physics debugging
# Heavy on snapshots - use for precise analysis

console = "zx"
seed = 0
players = 1

frames = [
  # Pre-action baseline
  { f = 0, p1 = "idle", snap = true },

  # Action start - every frame captured
  { f = 1, p1 = "a", snap = true },
  { f = 2, p1 = "a", snap = true },
  { f = 3, p1 = "a", snap = true },
  { f = 4, p1 = "idle", snap = true },
  { f = 5, p1 = "idle", snap = true },
  { f = 6, p1 = "idle", snap = true },
  { f = 7, p1 = "idle", snap = true },
  { f = 8, p1 = "idle", snap = true },
  { f = 9, p1 = "idle", snap = true },
  { f = 10, p1 = "idle", snap = true },

  # Continue with less frequency
  { f = 15, p1 = "idle", snap = true },
  { f = 20, p1 = "idle", snap = true },
  { f = 25, p1 = "idle", snap = true },
  { f = 30, p1 = "idle", snap = true },
]
```

### Input Template

**File:** `tests/replay/input_template.ncrs`

```toml
# Input Handling Test Template
# Tests button registration and combinations
# Verify each input type is processed correctly

console = "zx"
seed = 0
players = 1

frames = [
  # Baseline
  { f = 0, p1 = "idle", snap = true },

  # Single buttons
  { f = 1, p1 = "a", snap = true },
  { f = 5, p1 = "b", snap = true },
  { f = 10, p1 = "x", snap = true },
  { f = 15, p1 = "y", snap = true },

  # D-pad
  { f = 20, p1 = "up", snap = true },
  { f = 25, p1 = "down", snap = true },
  { f = 30, p1 = "left", snap = true },
  { f = 35, p1 = "right", snap = true },

  # Diagonals
  { f = 40, p1 = "up+right", snap = true },
  { f = 45, p1 = "down+left", snap = true },

  # Button combinations
  { f = 50, p1 = "right+a", snap = true },
  { f = 55, p1 = "left+b", snap = true },
  { f = 60, p1 = "up+a+b", snap = true },

  # Shoulder buttons
  { f = 65, p1 = "l", snap = true },
  { f = 70, p1 = "r", snap = true },
  { f = 75, p1 = "l+r", snap = true },

  # System buttons
  { f = 80, p1 = "start", snap = true },
  { f = 85, p1 = "select", snap = true },

  # Return to idle
  { f = 90, p1 = "idle", snap = true },
]
```

## Step 4: Report Template Created

After writing the template:

**Template created:** `tests/replay/[type]_template.ncrs`

**Next steps:**
1. Edit the template to match your game's parameters
2. Adjust frame numbers for your game's timing
3. Update assertions for your expected values
4. Run with: `nether replay run tests/replay/[type]_template.ncrs --report report.json`

**Available debug variables:**
```bash
grep -r "debug_register" src/
```

Use these variable names in assertions (prefix with `$`).

**Available debug actions:**
```bash
grep -r "debug_action_begin" src/
```

Use actions to skip setup and jump directly to test scenarios.
