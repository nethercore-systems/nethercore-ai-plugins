# Material Sound Signatures

Acoustic characteristics for different materials to guide synthesis and recording.

## Metal

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | High mids, resonant | 1-8kHz prominent |
| Decay | Long ring | 200ms-2s |
| Character | Clangy, bright | Clear transient |

**Variations:**
- Thin metal: Higher pitch, shorter ring
- Thick metal: Lower pitch, longer ring
- Rusty: Duller, less ring
- Hollow: More resonance

**Synthesis approach:**
- FM synthesis for bell-like quality
- Resonant bandpass filters
- Long decay envelope

---

## Wood

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Low mids | 200Hz-2kHz |
| Decay | Medium | 100-300ms |
| Character | Thuddy, warm | Soft transient |

**Variations:**
- Hard wood: Brighter, more crack
- Soft wood: Duller, more thud
- Hollow: More resonance, boxiness
- Solid: Shorter, denser

**Synthesis approach:**
- Filtered noise for body
- Short resonant filter for knock
- Quick decay envelope

---

## Stone/Concrete

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Wide band | 100Hz-6kHz |
| Decay | Short | 50-150ms |
| Character | Crunchy, solid | Sharp transient |

**Variations:**
- Gravel: Multiple short impacts
- Boulder: Deep boom, debris
- Brick: Crumbly, mid-focused
- Tile: Brighter, crack-like

**Synthesis approach:**
- Noise burst for crunch
- Layered impacts for debris
- Short, punchy envelope

---

## Flesh/Organic

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Low mids | 100Hz-1kHz |
| Decay | Short | 50-100ms |
| Character | Thuddy, soft | Dull transient |

**Variations:**
- Punch: More low end, slap
- Slice: Higher, sharper
- Squish: Wet, squelchy
- Thump: Dry, solid

**Synthesis approach:**
- Low-passed noise
- Very short decay
- Layer wet sounds for gore

---

## Glass

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Very high | 2-12kHz |
| Decay | Medium | 100-500ms |
| Character | Shatter, tinkle | Bright transient |

**Variations:**
- Thin glass: Higher, shorter
- Thick glass: Lower, crunchier
- Crystal: More ring, musical
- Bottle: Hollow resonance

**Synthesis approach:**
- High-passed noise burst
- Multiple layered impacts
- Additive harmonics for ring

---

## Plastic/Synthetic

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Upper mids | 1-4kHz |
| Decay | Short | 30-100ms |
| Character | Clicky, hollow | Sharp transient |

**Variations:**
- Hard plastic: Clicky, sharp
- Soft plastic: Dull, muted
- Hollow: More resonance
- Solid: Denser, shorter

---

## Cloth/Fabric

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | High | 2-8kHz |
| Decay | Very short | 20-80ms |
| Character | Soft, rustling | No transient |

**Synthesis approach:**
- Filtered white noise
- Amplitude modulation for movement
- Very soft envelope

---

## Liquid/Water

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Wide, filtered | Varies |
| Decay | Variable | 50ms-2s |
| Character | Splashy, bubbly | Complex |

**Variations:**
- Splash: Burst + droplets
- Drip: Single drop + ripple
- Pour: Continuous filtered noise
- Bubble: Resonant pops

**Synthesis approach:**
- Filtered noise with modulation
- Resonant filters for bubbles
- Layered droplet samples

---

## Magic/Ethereal

| Property | Value | Notes |
|----------|-------|-------|
| Frequency | Full range | Synthetic |
| Decay | Long | 500ms-3s |
| Character | Otherworldly | Complex |

**Common elements:**
- Shimmer: High sparkly layer
- Whoosh: Filtered sweep
- Tone: Sustained pitch element
- Reverb: Long tail for space

**Synthesis approach:**
- FM synthesis for bells
- Granular for texture
- Heavy reverb and delay
- Pitch sweeps and modulation
