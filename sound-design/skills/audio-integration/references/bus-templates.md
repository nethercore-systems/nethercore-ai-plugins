# Bus Structure Templates

Audio bus configurations for different game types.

## Standard Game Template

```
                        ┌─────────────┐
                        │ Master Bus  │
                        │ Limiter     │
                        └──────┬──────┘
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  Music   │    │   SFX    │    │  Voice   │
        │ Sidechain│    │ Compress │    │ De-esser │
        └────┬─────┘    └────┬─────┘    └──────────┘
             │               │
    ┌────────┴───────┐   ┌──┴───┬─────────┐
    ▼                ▼   ▼      ▼         ▼
┌────────┐    ┌─────────┐ ┌─────┐ ┌─────┐ ┌─────────┐
│Ambient │    │Combat   │ │ UI  │ │World│ │Creatures│
│Music   │    │Music    │ │Dry  │ │3D   │ │3D       │
└────────┘    └─────────┘ └─────┘ └─────┘ └─────────┘
```

### Bus Settings

| Bus | Volume | Compression | Reverb Send |
|-----|--------|-------------|-------------|
| Master | 0 dB | 4:1 limiter | - |
| Music | -3 dB | 2:1 | 10% |
| SFX | 0 dB | 2:1 | Varies |
| Voice | +2 dB | 3:1 | 5% |
| UI | -2 dB | None | 0% |
| World | 0 dB | Light | By zone |
| Ambient Music | -6 dB | None | Pre-baked |
| Combat Music | 0 dB | None | Pre-baked |

---

## Mobile Game Template (Simplified)

```
              ┌─────────────┐
              │ Master Bus  │
              └──────┬──────┘
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Music  │  │  SFX   │  │  UI    │
    └────────┘  └────────┘  └────────┘
```

Fewer buses = less CPU overhead.

---

## AAA Template (Complex)

```
                              ┌─────────────┐
                              │ Master Bus  │
                              └──────┬──────┘
           ┌──────────────┬──────────┼──────────┬──────────────┐
           ▼              ▼          ▼          ▼              ▼
      ┌────────┐    ┌──────────┐ ┌──────┐ ┌──────────┐  ┌───────────┐
      │ Music  │    │   SFX    │ │Voice │ │ Ambient  │  │ Cinematic │
      └───┬────┘    └────┬─────┘ └──┬───┘ └────┬─────┘  └───────────┘
          │              │          │          │
    ┌─────┴─────┐    ┌───┴───┐     │    ┌─────┴─────┐
    │           │    │       │     │    │           │
┌───────┐ ┌───────┐ ┌───┐ ┌───┐ ┌───┐ ┌───────┐ ┌───────┐
│Explore│ │Combat │ │ UI│ │Wpn│ │NPC│ │Nature │ │Machine│
└───────┘ └───────┘ └───┘ └───┘ └───┘ └───────┘ └───────┘
```

---

## Processing Chains

### Music Bus
```
Input → Sidechain Compressor (keyed by Voice) →
EQ (high-pass 30Hz) → Stereo Widener → Output
```

### SFX Bus
```
Input → Compressor (2:1, fast) →
EQ (cut 200-400Hz mud) → Limiter → Output
```

### Voice Bus
```
Input → High-pass 80Hz → De-esser (6kHz) →
Compressor (3:1) → EQ boost 2-4kHz → Output
```

### Master Bus
```
All Buses → Master Compressor (2:1) →
EQ → Limiter (-1dB) → Output
```

---

## Reverb Bus Configuration

Separate reverb buses for different spaces:

```
┌─────────────────────────────────────────┐
│              Sound Sources              │
└───────────────────┬─────────────────────┘
                    │ Sends
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────┐    ┌──────────┐    ┌──────────┐
│Room Rev│    │Hall Rev  │    │Cave Rev  │
│0.5s    │    │2.5s      │    │4s        │
└────┬───┘    └────┬─────┘    └────┬─────┘
     └─────────────┴───────────────┘
                   │
                   ▼
            ┌──────────┐
            │ Reverb   │
            │ Return   │
            └──────────┘
```

**Zone-based switching:** Blend between reverb buses based on player location.

---

## Voice Stealing Configuration

```rust
struct VoicePool {
    max_voices: usize,          // 32-64 typical
    reserved_critical: usize,   // 4-8 always available for priority 1

    stealing_rules: StealingRules {
        steal_from_lower_priority: true,
        steal_oldest_first: true,
        fade_out_time_ms: 50,
        min_play_time_ms: 100,  // Don't steal sounds that just started
    }
}
```
