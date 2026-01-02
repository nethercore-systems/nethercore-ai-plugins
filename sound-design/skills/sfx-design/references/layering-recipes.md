# Layering Recipes

Category-specific layer breakdowns for common game sounds.

## Impact Sounds

### Light Impact (UI click, small hit)
```
Layer 1: Transient
  - Square wave or click
  - 1-2kHz, 5-15ms
  - Immediate attack, fast decay

Layer 2: Body (optional)
  - Filtered noise or sine
  - 50-100ms decay
  - Low-pass at 2-4kHz
```
**Total duration:** 50-150ms

### Medium Impact (punch, collision)
```
Layer 1: Transient
  - Click or thump
  - 10-30ms
  - Sharp attack

Layer 2: Body
  - Material-specific
  - 100-200ms
  - Mid frequencies

Layer 3: Tail
  - Room reverb or ring
  - 200-500ms
  - Subtle
```
**Total duration:** 200-500ms

### Heavy Impact (explosion, big hit)
```
Layer 1: Transient
  - Noise burst, high-passed
  - 10-30ms

Layer 2: Low boom
  - Sine sweep 100Hz → 40Hz
  - 200-500ms decay

Layer 3: Mid crunch
  - Filtered noise
  - Band-pass 300-2000Hz
  - 100-300ms

Layer 4: High sizzle
  - High-passed noise
  - 500ms+ decay

Layer 5: Sub rumble (optional)
  - Low sine, 30-60Hz
  - Long decay
```
**Total duration:** 1-3s

---

## Movement Sounds

### Whoosh/Swing
```
Layer 1: Core whoosh
  - Filtered white noise
  - Band-pass sweep (low→high or high→low)
  - Duration matches movement speed

Layer 2: Pitch element (optional)
  - Saw or sine wave
  - Pitch bend matching direction
```
**Parameters:**
- Fast swing: 100-200ms, brighter
- Slow swing: 300-500ms, deeper

### Footstep Template
```
Layer 1: Transient
  - Click/thud based on surface
  - 10-30ms

Layer 2: Material body
  - Surface-specific:
    - Grass: soft filtered noise
    - Stone: short crunch
    - Metal: clang with ring
    - Wood: knock

Layer 3: Environment
  - Room/space reverb
  - Match the environment
```

---

## UI Sounds

### Button Click
```
Layer 1: Click
  - Square wave pop or filtered click
  - 1-2kHz fundamental
  - 10-30ms, very fast envelope

Layer 2: Ring (optional)
  - Gentle sine decay
  - 300-800Hz
  - 50-100ms
```

### Confirm/Accept
```
Layer 1: Primary tone
  - Rising pitch or chord
  - Major interval (3rd or 5th)
  - 100-200ms

Layer 2: Sparkle (optional)
  - High shimmer
  - 50-100ms
```

### Error/Cancel
```
Layer 1: Negative tone
  - Descending pitch
  - Minor interval or dissonant
  - 100-200ms

Layer 2: Buzz (optional)
  - Slight distortion
  - Adds "wrong" feeling
```

### Hover
```
Single layer:
  - Very subtle tick or hum
  - 20-50ms
  - High frequency, quiet
```

---

## Weapon Sounds

### Sword Swing
```
Layer 1: Whoosh
  - Filtered noise sweep
  - 100-200ms

Layer 2: Metal ring (optional)
  - High metallic tone
  - Short decay
```

### Sword Impact
```
Layer 1: Transient
  - Sharp click
  - 5-15ms

Layer 2: Metal ring
  - FM or resonant filter
  - 100-300ms

Layer 3: Target material
  - Depends on what's hit
```

### Bow Release
```
Layer 1: Twang
  - Plucked string sound
  - 50-100ms

Layer 2: Whoosh
  - Air movement
  - 100-200ms
```

### Gun/Projectile
```
Layer 1: Transient
  - Sharp noise burst
  - 10-30ms

Layer 2: Body
  - Low thump or explosion
  - 50-200ms

Layer 3: Tail
  - Echo/reverb
  - 200ms-1s
```

---

## Creature Sounds

### Small Creature
```
Base frequency: 500Hz+ fundamental
Character: Quick, chattery

Layers:
  - Pitched noise bursts
  - Formant filtering (higher formants)
  - Fast modulation
```

### Medium Creature
```
Base frequency: 150-300Hz fundamental
Character: Growls, barks, roars

Layers:
  - Low growl (filtered noise + sine)
  - Mid-range character
  - Clear emotional read
```

### Large Creature
```
Base frequency: 50-150Hz fundamental
Character: Slow, rumbling

Layers:
  - Very low drone
  - Sub harmonics
  - Long reverb tail
  - Slow attack and decay
```

---

## Ambient Layers

### Forest
```
Layer 1: Wind bed (30s loop)
Layer 2: Bird calls (45s loop, random triggers)
Layer 3: Rustling leaves (20s loop)
Layer 4: Insects (60s loop)
```

### Cave
```
Layer 1: Low drone/hum (45s)
Layer 2: Drips (random triggers)
Layer 3: Distant echoes (random)
```

### City
```
Layer 1: Traffic bed (60s)
Layer 2: Crowd murmur (45s)
Layer 3: Distant sirens (random)
Layer 4: HVAC hum (30s)
```
