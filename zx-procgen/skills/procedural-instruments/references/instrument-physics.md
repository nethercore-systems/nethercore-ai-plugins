# Instrument Physics

Understanding what makes each instrument sound unique helps create more realistic synthesis.

## Why Instruments Sound Different

Every acoustic instrument has:
1. **Excitation** - How the sound is initiated (pluck, bow, blow, strike)
2. **Resonator** - What vibrates (string, air column, membrane)
3. **Radiator** - How sound projects (body, bell, soundboard)

The interaction of these creates the characteristic sound.

---

## String Instruments

### Guitar (Plucked)

**Excitation:** Pluck creates broadband noise burst
**Resonator:** String (determines pitch via length/tension)
**Radiator:** Hollow body amplifies and colors

**Key Characteristics:**
- Attack transient from pluck (brief noise)
- Harmonics decay at different rates (highs faster than lows)
- Body resonances add warmth
- Steel strings: bright, sustain; Nylon: warm, quicker decay

**Synthesis Approach:** Karplus-Strong with brightness parameter

### Piano (Struck)

**Excitation:** Hammer strike (complex, inharmonic impact)
**Resonator:** Multiple strings per note (chorus effect)
**Radiator:** Large soundboard

**Key Characteristics:**
- Complex attack (hammer felt → string contact)
- String stiffness causes inharmonicity (higher partials sharp)
- Sympathetic resonance from other strings
- Sustain pedal extends all strings

**Synthesis Approach:** Extended Karplus-Strong with stiffness, or multi-layered samples

### Violin (Bowed)

**Excitation:** Bow creates stick-slip friction (continuous)
**Resonator:** String
**Radiator:** Violin body (f-holes)

**Key Characteristics:**
- Continuous excitation (can sustain indefinitely)
- Bowing pressure affects brightness
- Vibrato is standard performance technique
- Rich harmonics, especially odd

**Synthesis Approach:** Waveguide or wavetable (bowing is complex)

---

## Wind Instruments

### Flute

**Excitation:** Air stream split by edge (edge tone)
**Resonator:** Open tube (standing wave)
**Radiator:** Open holes

**Key Characteristics:**
- Breath noise in attack
- Nearly pure tone (few harmonics)
- Breathiness increases at low volumes
- Clear, focused sound

**Synthesis Approach:** Sine wave with breath noise, low harmonic content

### Clarinet

**Excitation:** Single reed vibration
**Resonator:** Cylindrical bore (closed at mouthpiece)
**Radiator:** Bell and open holes

**Key Characteristics:**
- Closed pipe = odd harmonics only (hollow sound)
- Rich "woody" tone
- Wide dynamic range
- Distinct register break

**Synthesis Approach:** Additive with odd harmonics, or FM

### Trumpet

**Excitation:** Lip buzzing (controlled chaos)
**Resonator:** Conical/cylindrical brass tube
**Radiator:** Flared bell

**Key Characteristics:**
- Bright, powerful
- All harmonics present
- Lip tension controls brightness
- Mute changes character dramatically

**Synthesis Approach:** Subtractive (saw + filter) with breath transient

---

## Percussion

### Drums (Membranophones)

**Excitation:** Strike
**Resonator:** Stretched membrane
**Radiator:** Drum shell

**Key Characteristics:**
- Inharmonic partials (complex circular modes)
- Very fast attack
- Decay depends on tuning and damping
- Shell material affects color

**Synthesis Approach:** Noise burst + filtered resonance, or FM with inharmonic ratios

### Bells (Idiophones)

**Excitation:** Strike
**Resonator:** Metal itself
**Radiator:** Metal surface

**Key Characteristics:**
- Highly inharmonic partials
- Very long decay (metal rings)
- Characteristic "minor third" partials in large bells
- Strike point affects spectrum

**Synthesis Approach:** FM with non-integer ratios, or additive with analyzed partials

### Marimba/Vibraphone

**Excitation:** Mallet strike on bar
**Resonator:** Wooden/metal bar + resonator tube
**Radiator:** Resonator tube

**Key Characteristics:**
- Fundamental emphasized by resonator
- Warm, focused tone
- Vibraphone: motor creates tremolo
- Marimba: wooden = warmer

**Synthesis Approach:** FM or additive with fundamental emphasis

---

## Keyboard Instruments

### Electric Piano (Rhodes)

**Excitation:** Hammer strikes tine
**Resonator:** Metal tine + tonebar
**Radiator:** Electromagnetic pickup

**Key Characteristics:**
- Bell-like attack (tine)
- Warm sustain (asymmetric waveform)
- Velocity affects brightness dramatically
- Characteristic "bark" at high velocity

**Synthesis Approach:** FM synthesis (DX7 algorithm)

### Hammond Organ

**Excitation:** Electromagnetic (tonewheels)
**Resonator:** Electromechanical
**Radiator:** Leslie speaker (optional)

**Key Characteristics:**
- Additive harmonic structure (drawbars)
- Key click (mechanical artifact, now desired)
- Leslie speaker creates doppler/tremolo
- Sustained indefinitely

**Synthesis Approach:** Additive synthesis with drawbar levels

---

## Common Acoustic Phenomena

### Formants

Fixed resonant frequencies in a sound source (independent of pitch).

| Instrument | Formant Region |
|------------|----------------|
| Voice "ah" | 800, 1200 Hz |
| Voice "ee" | 300, 2500 Hz |
| Guitar body | 80-100, 200-250 Hz |
| Violin body | 280, 400-500 Hz |

**Implementation:** Band-pass filters at formant frequencies

### Sympathetic Resonance

Other strings/parts vibrate in response to played note.

- Piano sustain pedal enables this
- Creates richness and complexity
- Sitar has dedicated sympathetic strings

**Implementation:** Add quiet harmonic-related tones

### Attack Transients

The first 10-50ms of a sound often contains noise or inharmonic content.

| Instrument | Attack Character |
|------------|------------------|
| Guitar | Pluck noise + finger/pick sound |
| Piano | Hammer thump |
| Trumpet | Breath burst |
| Drum | Impact noise |

**Implementation:** Add filtered noise burst with fast decay

### Inharmonicity

Real instruments don't have perfectly harmonic partials.

| Instrument | Inharmonicity |
|------------|---------------|
| Strings | Higher partials slightly sharp (stiffness) |
| Bells | Completely inharmonic |
| Drums | Inharmonic (circular membrane modes) |
| Flutes | Nearly harmonic |

**Implementation:** Adjust partial frequency ratios from integer values

---

## Quick Reference: Instrument → Technique

| Instrument | Primary Technique | Key Parameters |
|------------|------------------|----------------|
| Acoustic Guitar | Karplus-Strong | damping, brightness |
| Electric Guitar | KS + distortion | damping, drive |
| Bass Guitar | KS (long delay) | damping, sub blend |
| Piano | Extended KS / sample | stiffness, velocity layers |
| Electric Piano | FM | ratio=1:1, index decay |
| Organ | Additive | drawbar levels |
| Strings | Wavetable + unison | detune, position |
| Flute | Sine + noise | breath amount |
| Trumpet | Subtractive | filter envelope, breath |
| Bells | FM (inharmonic) | non-integer ratio |
| Drums | Noise + filter | decay, pitch |
| Synth Pad | Wavetable | position sweep, detune |
| Synth Lead | Subtractive | filter envelope, resonance |
| Synth Bass | Subtractive | filter cutoff, sub |
