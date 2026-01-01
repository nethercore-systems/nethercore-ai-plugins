---
description: Analyze the most recent report.json from a replay test
argument-hint: "[path to report.json]"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Analyze Replay Test Report

Parse a replay execution report to identify root causes and suggest fixes.

## Step 1: Locate Report File

**If argument provided**: Use the specified path.

**If no argument**: Search for recent report files:

```bash
# Check common locations
ls -la report.json 2>/dev/null
ls -la *.report.json 2>/dev/null
ls -la tests/replay/*.json 2>/dev/null
```

If multiple reports found, use AskUserQuestion to let user select.

## Step 2: Read and Parse Report

Read the JSON report file. Extract key sections:

### Summary Section

```json
{
  "summary": {
    "status": "PASSED" | "FAILED",
    "assertions_passed": N,
    "assertions_failed": N,
    "frames_with_snap": N
  }
}
```

### Failed Assertions

```json
{
  "assertions": [
    {
      "frame": 1,
      "condition": "$velocity_y < 0",
      "passed": false,
      "actual": 0,
      "expected": "< 0"
    }
  ]
}
```

### Snapshots with Deltas

```json
{
  "snapshots": [
    {
      "frame": 1,
      "input": "a",
      "pre": { "$velocity_y": 0 },
      "post": { "$velocity_y": 0 },
      "delta": {}
    }
  ]
}
```

## Step 3: Analyze Results

### If Test PASSED

Report success with summary:
- All N assertions passed
- Highlight key state changes from snapshots
- Suggest removing test if verifying a fix

### If Test FAILED

Identify the failure pattern:

**Pattern: Variable stayed at initial value**
```
Frame 1: $velocity_y = 0 -> 0 (delta: none)
Assertion failed: "$velocity_y < 0" (actual: 0)
```

Diagnosis: The expected change didn't happen.
- For jump: Jump force not applied
- For movement: Input not processed or blocked

**Pattern: Variable changed unexpectedly**
```
Frame 1: $health = 100 -> 50 (delta: -50)
Assertion failed: "$health >= 100"
```

Diagnosis: Something modified state unexpectedly.
- Check for unintended damage sources
- Look for initialization issues

**Pattern: Value wrong direction**
```
Frame 1: $velocity_y = 0 -> 5 (delta: +5)
Assertion failed: "$velocity_y < 0"
```

Diagnosis: Change happened but with wrong sign/value.
- Velocity applied to wrong axis
- Sign error in calculation

## Step 4: Identify Root Cause

Based on the failure pattern, search game code:

**For velocity issues:**
```bash
grep -r "velocity" src/ | grep -v test
```

**For input issues:**
```bash
grep -rE "a_pressed|a_just_pressed|input\." src/
```

**For specific variable:**
```bash
grep -r "[variable_name]" src/
```

Read the relevant code sections to find the bug.

## Step 5: Report Findings

Structure the analysis report:

### Summary

**Status:** FAILED (1 assertion failed)

### Failed Assertion

- **Frame:** 1
- **Condition:** `$velocity_y < 0`
- **Actual value:** 0
- **Expected:** negative (player jumping)

### State Analysis

Frame 1 snapshot shows `$velocity_y` remained 0 after pressing A. The jump input was not applied.

### Likely Cause

Based on code analysis, the issue is in `src/player.rs:42`:

```rust
// Current code - always returns false after first frame
if input.a_pressed() {
    self.velocity_y = -JUMP_FORCE;
}
```

Should be:
```rust
// Fixed - triggers on button press, not held
if input.a_just_pressed() {
    self.velocity_y = -JUMP_FORCE;
}
```

### Recommended Fix

Change `a_pressed()` to `a_just_pressed()` on line 42 of `src/player.rs`.

### Verification

After fixing, re-run the test:
```bash
nether replay run tests/replay/jump_test.ncrs --report report.json
```

## Common Diagnosis Patterns

| Symptom | Likely Cause | Check For |
|---------|--------------|-----------|
| Velocity stayed 0 | Input not processed | `a_pressed` vs `a_just_pressed` |
| Position unchanged | Collision blocking | Collision code, hitbox sizes |
| Wrong direction | Sign error | Negative/positive velocity |
| Gradual drift | Float precision | Fixed-point conversion |
| Random failures | Non-determinism | `random()` vs external random |
| State corruption | Wrong variable | Copy-paste errors, typos |
