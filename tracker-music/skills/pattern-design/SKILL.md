---
name: Pattern Design
description: |
  Use this skill when structuring tracker songs - pattern layout, song structure, efficiency, and loop design.

  **Trigger phrases:** "song structure", "pattern layout", "order table", "loop point", "how many patterns", "verse chorus", "song form"

  **Load references when:**
  - Genre-specific templates → `references/genre-templates.md`
  - Loop point techniques → `references/loop-techniques.md`

  For effect usage, use `tracker-fundamentals`.
  For format-specific details, use `xm-format` or `it-format`.
version: 1.0.0
---

# Pattern Design

## Core Concepts

### Pattern vs Order Table

```
Patterns: Unique musical content (A, B, C, D)
Order Table: Sequence of pattern playback

Order: [0, 1, 1, 2, 1, 1, 2, 3, 0]
       [A, B, B, C, B, B, C, D, A]  ← Song structure

Result: A plays once, B twice, C once, B twice again, etc.
```

**Key insight:** Reuse patterns via order table. Never duplicate pattern content.

### Standard Pattern Length

| Length | Rows | Use Case |
|--------|------|----------|
| Short | 32 | Fills, transitions |
| Standard | 64 | Verses, choruses |
| Extended | 128 | Long sections (rare) |

**Default:** 64 rows (4 bars at 16 rows per bar)

### Rows per Beat

| Speed | BPM | Rows/Beat | Feel |
|-------|-----|-----------|------|
| 3 | 150+ | 4 | Fast, energetic |
| 4 | 120-150 | 4 | Standard dance |
| 6 | 100-130 | 8 | Standard rock |
| 8 | 80-100 | 8 | Slow, atmospheric |

**Formula:** Rows per beat = Speed × 4 / (BPM / 60)

## Song Structures

### Loop-Based (Game Background Music)

Most game music needs to loop seamlessly:

```
Order: [0, 1, 1, 2, 1, 1, 2, 3]
        ↓  ↓←loop back←←←←↓

Pattern 0: Intro (plays once)
Pattern 1: Main A (verse)
Pattern 2: Main B (chorus/variation)
Pattern 3: Transition (leads back to 1)

Restart Position: 1 (skip intro on loop)
```

### Linear (Cutscenes, Victory Jingles)

One-shot, no loop:

```
Order: [0, 1, 2]  (End command at pattern 2's end)

Pattern 0: Opening
Pattern 1: Development
Pattern 2: Resolution + Fade/End
```

### Adaptive (Dynamic Music)

Multiple sections that can be jumped to:

```
Order: [0, 1, 1, 2, 2, 3, 3, 4]
        │  └─explore─┘ │ └combat┘ │
        │             │          └─boss

Music system jumps between sections based on gameplay.
```

## Pattern Efficiency

### The 4-Pattern Song

Most simple tracks need only 4 patterns:

| Pattern | Content | Duration |
|---------|---------|----------|
| 0 | Intro | 4-8 bars |
| 1 | Verse/Main | 8 bars |
| 2 | Chorus/Variation | 8 bars |
| 3 | Bridge/Breakdown | 4-8 bars |

Order table creates full song: `[0, 1, 1, 2, 1, 1, 2, 3, 1, 2]`

### Pattern Variation Without Duplication

Instead of copying pattern 1 to make pattern 1b:

**Use these techniques:**

1. **Effect-based variation:** Same pattern, add effects on repeat
   ```
   First play: No vibrato
   Second play: Add vibrato on leads
   ```

2. **Volume variation:** Same pattern, duck instruments
   ```
   First play: Full drums
   Second play: Reduce hi-hat volume
   ```

3. **Order position awareness:** Effects that only trigger at certain pattern orders

4. **Break into sub-patterns:**
   ```
   Instead of: Pattern 1 (full 64 rows) × 2 copies
   Use: Pattern 1a (32 rows) + Pattern 1b (32 rows)
   Order: [1a, 1b, 1a, 1c] ← 1c has variation
   ```

### Pattern Size Budget

| Song Length | Patterns | Order Length |
|-------------|----------|--------------|
| 30s loop | 2-3 | 4-6 |
| 1min loop | 4-5 | 8-12 |
| 2min loop | 6-8 | 16-24 |
| 3min full | 8-12 | 24-36 |

## Section Design

### Intro Pattern

**Purpose:** Establish mood, grab attention, set up loop

```
Rows 0-15:  Sparse (drums only, or ambient pad)
Rows 16-31: Add bass
Rows 32-47: Add melody fragment
Rows 48-63: Build to full groove
```

**Key:** Should lead naturally into main section.

### Main/Verse Pattern

**Purpose:** Core groove, repeatable foundation

```
Rows 0-15:  Full groove established
Rows 16-31: Groove continues, possible variation
Rows 32-47: Melodic content
Rows 48-63: Lead into next section or repeat
```

**Key:** Must be satisfying on repeat.

### Chorus/Hook Pattern

**Purpose:** Peak energy, most memorable

```
Rows 0-15:  Impact! Full energy from start
Rows 16-31: Hook melody prominent
Rows 32-47: Hook continues/develops
Rows 48-63: Prepare for transition
```

**Key:** Instantly recognizable, emotionally satisfying.

### Bridge/Breakdown Pattern

**Purpose:** Contrast, tension release, ear refresh

```
Rows 0-15:  Strip elements (drums out, or minimal)
Rows 16-31: Different harmonic content
Rows 32-47: Build or stay sparse
Rows 48-63: Transition back to main
```

**Key:** Should feel like a departure, making return impactful.

### Transition Pattern

**Purpose:** Smooth bridge between sections

```
Rows 0-31:  Fade current section
Rows 32-47: Drum fill or riser
Rows 48-63: Prepare new section energy
```

**Key:** Never jarring. Use volume fades and fills.

## Row-Level Structure

### 64-Row Pattern Grid

```
Rows    | Bar | Beat | Typical Content
--------|-----|------|----------------
0-15    | 1   | 1-4  | Phrase A
16-31   | 2   | 1-4  | Phrase A (variation)
32-47   | 3   | 1-4  | Phrase B
48-63   | 4   | 1-4  | Phrase B + transition
```

### Drum Programming Grid

```
Row | Beat | Kick | Snare | HH
----|------|------|-------|----
0   | 1.1  | X    |       | X
4   | 1.2  |      | X     | X
8   | 1.3  | X    |       | X
12  | 1.4  |      | X     | X
16  | 2.1  | X    |       | X
...
```

### Melody Phrase Length

| Phrase Type | Rows | Notes |
|-------------|------|-------|
| Short motif | 8-16 | 2-4 notes |
| Medium phrase | 16-32 | 4-8 notes |
| Long phrase | 32-64 | 8+ notes |

**Tip:** End phrases on strong beats (row 0, 16, 32, 48).

## Loop Point Design

### Seamless Loop Requirements

1. **Harmonic continuity:** Last chord leads to first
2. **Rhythmic continuity:** Beat doesn't skip
3. **Timbral continuity:** Same instruments active
4. **Dynamic continuity:** Similar volume levels

### Loop Preparation (Last 8 Rows)

```
Row 56: Start any volume fades (A08)
Row 57: Continue fades
Row 58: Prepare transition (maybe drum fill start)
Row 59: Continue transition
Row 60: Clear held notes or prepare for loop
Row 61: Final fade frames
Row 62: Optional: Position jump effect (Bxx)
Row 63: Last row - clean state for loop
```

### Restart Position

Set restart position to skip intro:

```python
module = XmModule(
    # ...
    restart_position=1,  # Skip pattern 0 on loop
)
```

### Testing Loops

1. Play through loop point 5+ times
2. Listen for:
   - Clicks or pops
   - Jarring volume changes
   - Rhythmic hiccups
   - Harmonic clashes
3. Adjust fades, add/remove notes as needed

## Order Table Patterns

### Standard Pop/Rock

```
Order: [Intro, V, V, C, V, V, C, C, Bridge, C, Outro]
       [  0  , 1, 1, 2, 1, 1, 2, 2,   3  , 2,   4  ]
```

### Dance/Electronic

```
Order: [Intro, Build, Drop, Break, Drop, Outro]
       [  0  ,  1   ,  2  ,   3  ,  2  ,   4  ]
```

### Ambient/Atmospheric

```
Order: [A, B, A, C, B, A]  ← Minimal, evolving
       [0, 1, 0, 2, 1, 0]
```

### Boss Battle

```
Order: [Ominous, Attack, Intense, Attack, Desperate, Loop→Attack]
       [   0   ,   1   ,   2   ,   1   ,     3     ,     1     ]
```

## Practical Examples

### 4-Pattern Dance Track

```python
order_table = [
    0,  # Intro (8 bars)
    1,  # Main groove (8 bars)
    1,  # Main groove repeat
    2,  # Build + drop (8 bars)
    1,  # Main groove
    1,  # Main groove
    2,  # Build + drop
    3,  # Breakdown (8 bars)
    2,  # Final drop
]
restart_position = 1  # Loop from main groove
```

### 3-Pattern Ambient Loop

```python
order_table = [
    0,  # Intro pad (8 bars)
    1,  # Main texture (16 bars)
    1,
    2,  # Variation (8 bars)
    1,  # Return
]
restart_position = 1  # Loop from main texture
```

### 2-Pattern Victory Jingle

```python
order_table = [
    0,  # Fanfare (4 bars)
    1,  # Resolution + hold (4 bars, ends)
]
# No restart - one-shot
# Add pattern break to end at row 0 of non-existent pattern
```

## Anti-Patterns

### Pattern Bloat

**Bad:** 20 patterns that are 90% identical
**Good:** 5 patterns with order table repetition

### Copy-Paste Patterns

**Bad:** Duplicate pattern to change 2 notes
**Good:** Use sub-patterns or effect variations

### Ignoring Loop Point

**Bad:** Song just cuts off and restarts
**Good:** Fade out, drum fill, harmonic resolution

### Over-Long Patterns

**Bad:** 256-row patterns with sparse content
**Good:** 64-row patterns, use order table for length
