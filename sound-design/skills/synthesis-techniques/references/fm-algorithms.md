# FM Algorithms

Common operator configurations for FM synthesis.

## 2-Operator Algorithms

### 2-op Stack (DX7-like)
```
[2] → [1] → Out

Op 2 modulates Op 1
- Simple but effective
- Good for: bass, leads, bells
```

### 2-op Parallel
```
[1] → Out
[2] → Out

Both carriers, mixed output
- Two independent tones
- Good for: layered sounds
```

---

## 4-Operator Algorithms

### Algorithm 1: Full Stack
```
[4] → [3] → [2] → [1] → Out

Each modulates the next
- Maximum harmonic complexity
- Good for: metallic, harsh
```

### Algorithm 2: Branched
```
[4] → [3] ─┐
           ├→ [1] → Out
[2] ───────┘

Two modulators sum into carrier
- Blended modulation
- Good for: complex bells
```

### Algorithm 3: Parallel Stacks
```
[4] → [3] → Out
[2] → [1] → Out

Two independent 2-op stacks
- Layered tones
- Good for: organs, pads
```

### Algorithm 4: Mixed
```
[4] → [3] → [1] → Out
      [2] ───┘

Three modulators, blended
- Rich harmonics
- Good for: brass, strings
```

### Algorithm 5: Parallel with Mod
```
[4] → [3] → Out
[2] → [1] → Out
       ↓
     [3] also

Op 2 modulates both Op 1 and Op 3
- Complex interaction
- Good for: evolving sounds
```

---

## 6-Operator Algorithms (DX7 Full)

### Algorithm 1
```
[6] → [5] → [4] → [3] → [2] → [1] → Out
```

### Algorithm 5 (Electric Piano)
```
[6] → [5] → [4] ─┐
                 ├→ [1] → Out
[3] → [2] ───────┘
```

### Algorithm 13 (Bell/Pad)
```
[6] → [5] → Out
[4] → [3] → Out
[2] → [1] → Out
```

### Algorithm 32 (Organ)
```
[6] → Out
[5] → Out
[4] → Out
[3] → Out
[2] → Out
[1] → Out
```

---

## Common Ratios

| Ratio | Character | Sound |
|-------|-----------|-------|
| 1:1 | Harmonic | Warm, bass |
| 2:1 | Octave harmonic | Clear, bell |
| 3:1 | Fifth harmonic | Hollow |
| 1:2 | Sub-octave | Deep |
| 1:1.41 | Non-integer | Metallic |
| 1:3.14 | Irrational | Very metallic |
| 1:7 | High harmonic | Nasal, bright |

---

## Modulation Index Guide

| Index | Character |
|-------|-----------|
| 0-1 | Subtle, warm |
| 1-3 | Clear harmonics |
| 3-6 | Bright, metallic |
| 6-10 | Aggressive, harsh |
| 10+ | Noise-like |

**Note:** Index often modulated by envelope for dynamic timbre.

---

## Classic DX7 Patches

### E. Piano 1
- Algorithm 5
- Ratio: 1:1 and 1:7
- Index: 3, fast decay
- Velocity controls index

### Brass
- Algorithm 2
- Ratio: 1:1
- Index: 5-8, slow attack
- Envelope follows dynamics

### Bell
- Algorithm 1
- Ratio: 1:1.41
- Index: 4-7, long decay
- Slight detune for richness

### Bass
- Algorithm 1
- Ratio: 1:1
- Index: 2-4, pluck envelope
- Low operator frequencies
