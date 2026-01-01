---
description: Generate a test script for the described scenario
argument-hint: "[description of bug or behavior to test]"
allowed-tools: ["AskUserQuestion", "Write", "Read", "Grep", "Glob"]
---

# Generate Replay Test Script

Create a minimal NCRS replay script to reproduce and debug a reported issue.

## Step 1: Gather Bug Information

**If no argument provided**, use AskUserQuestion:

- Question: "What issue or behavior do you want to test?"
- Header: "Bug"
- Options:
  - **Jump not working** - Player doesn't jump when pressing A
  - **Movement issues** - Player not moving correctly
  - **Collision problems** - Clipping through walls/floors

The user can type a custom description.

**If argument provided**, parse the description for:
- What action triggers the issue (button press, movement, etc.)
- What is the expected behavior
- What is the actual behavior

## Step 2: Discover Debug Variables

Search the game code for registered debug variables:

```bash
grep -r "debug_register" src/
```

Identify available variables like:
- `$player_x`, `$player_y` - Position
- `$velocity_x`, `$velocity_y` - Movement
- `$on_ground` - Grounded state
- Custom game-specific variables

## Step 3: Discover Debug Actions

Search for available debug actions that can simplify test setup:

```bash
grep -r "debug_action_begin" src/
```

Look for actions that can skip setup:
- `Load Level` - Jump to specific levels
- `Set Position` - Place player at exact coordinates
- `Skip Menu` - Bypass title/menu screens
- `Spawn Enemy` - Create test scenarios

**If relevant actions exist**, use them instead of long input sequences to reach the test scenario faster.

## Step 4: Determine Test Directory

Check if tests/replay/ exists:

```bash
test -d tests/replay && echo "EXISTS" || mkdir -p tests/replay
```

## Step 5: Generate Test Script

Create a minimal `.ncrs` file based on the bug description.

**Template structure (basic):**

```toml
# [Bug Description] Test
# Tests: [what behavior is being verified]
# Expected: [expected behavior]

console = "zx"
seed = 0
players = 1

frames = [
  # Initial state - always capture frame 0
  { f = 0, p1 = "idle", snap = true },

  # Action frames - reproduce the bug
  { f = 1, p1 = "[input]", snap = true },

  # Assertion - verify expected behavior
  { f = [N], p1 = "[input]", snap = true, assert = "[condition]" },

  # After effect - capture result
  { f = [N+offset], p1 = "idle", snap = true },
]
```

**Template with action setup (when available):**

```toml
# [Bug Description] Test
# Tests: [what behavior is being verified]
# Expected: [expected behavior]

console = "zx"
seed = 0
players = 1

# Setup phase - use actions to skip to relevant state
[[frames]]
f = 0
action = "Load Level"
action_params = { level = 3 }

# Begin actual test
[[frames]]
f = 1
p1 = "idle"
snap = true

# Reproduce the bug
[[frames]]
f = 2
p1 = "[input]"
snap = true
assert = "[condition]"
```

**Generate assertions based on bug type:**

| Bug Type | Typical Assertion |
|----------|-------------------|
| Jump not working | `assert = "$velocity_y < 0"` |
| Not moving | `assert = "$player_x > [initial]"` or `$velocity_x != 0` |
| Clipping | Compare positions at collision frames |
| Health issues | `assert = "$health == [expected]"` |
| Input not registering | Snap frames around input, check state changes |

**Naming convention:** `[issue]_test.ncrs` (e.g., `jump_test.ncrs`, `collision_test.ncrs`)

## Step 6: Write Test File

Write to `tests/replay/[name]_test.ncrs`.

Include comments explaining:
- What the test verifies
- What the expected behavior is
- What each frame section tests

## Step 7: Provide Run Instructions

After writing the file, tell the user:

**Test created:** `tests/replay/[name]_test.ncrs`

**Run the test:**
```bash
nether replay run tests/replay/[name]_test.ncrs --report report.json
```

**Or run headlessly:**
```bash
nether replay run tests/replay/[name]_test.ncrs --headless --report report.json
```

**After running**, share `report.json` for analysis with `/replay-analyze`.

## Best Practices

1. **Use actions for setup** - Skip menus/levels with debug actions when available
2. **Keep scripts minimal** - Under 100 frames when possible
3. **Always capture frame 0** - Establishes baseline state
4. **Snap around the action** - Before, during, and after the bug occurs
5. **One bug per script** - Focused tests are easier to debug
6. **Use meaningful assertions** - Assert the expected correct behavior
7. **Comment each section** - Explain what frames are testing
