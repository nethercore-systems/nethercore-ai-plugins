# Emotional Design for Games

## Emotional Architecture

### The Emotional Core

Every game should have a primary emotional target:

| Category | Primary Emotion | Supporting Emotions |
|----------|-----------------|---------------------|
| Horror | Fear | Dread, anxiety, relief |
| Action | Excitement | Power, triumph, flow |
| Puzzle | Satisfaction | Curiosity, frustration, eureka |
| Narrative | Empathy | Sadness, joy, anger |
| Simulation | Mastery | Control, progress, relaxation |
| Competition | Tension | Pride, rivalry, vindication |

### Emotional Palette

Like colors, emotions work together:

**Complementary Emotions** (enhance each other):
- Fear + Relief = Catharsis
- Frustration + Triumph = Satisfaction
- Tension + Release = Excitement

**Analogous Emotions** (blend smoothly):
- Wonder → Curiosity → Discovery
- Anxiety → Dread → Fear
- Pride → Satisfaction → Contentment

**Contrasting Emotions** (create impact):
- Safety → Danger (sudden threat)
- Calm → Panic (escalation)
- Boredom → Excitement (pacing)

## Emotional Journey Design

### The Emotional Arc

Map emotions across the player experience:

```
         ▲ Intensity
         │
    Joy  │                    ╭──────╮
         │                   ╱        ╲
         │        ╭─────────╯          ╲────╮
Wonder   │       ╱                          ╲
         │      ╱                            ╲ Melancholy
         │─────╯                              ╲─────────
         │ Curiosity                          Reflection
         └──────────────────────────────────────────────► Time
              Start      Mid-Game      Climax      End
```

### Pacing Principles

**Wave Pattern**: Alternate intensity
```
HIGH    ▓▓░░▓▓▓░░░▓▓▓▓░░▓▓▓▓▓░░
LOW     ░░▓▓░░░▓▓▓░░░░▓▓░░░░░▓▓
        Start ──────────────► End
```

**Escalating Pattern**: Build over time
```
HIGH                          ▓▓▓▓
                         ▓▓▓▓▓
                    ▓▓▓▓▓
               ▓▓▓▓▓
          ▓▓▓▓▓
LOW   ▓▓▓▓
      Start ──────────────► End
```

**Punctuated Pattern**: Baseline with spikes
```
HIGH            ▓         ▓▓      ▓▓▓
               ▓▓▓       ▓▓▓▓    ▓▓▓▓▓
LOW   ▓▓▓▓▓▓▓▓▓░░░▓▓▓▓▓▓▓░░░░▓▓▓▓░░░░░▓▓▓
      Start ──────────────────────────► End
```

### Beat Design

Structure emotional moments:

**Setup**: Establish baseline emotion
**Build**: Increase intensity gradually
**Trigger**: The moment of peak emotion
**Aftermath**: Processing and recovery

Example (Fear sequence):
```
Setup:    Player enters dark area, ambient tension
Build:    Strange sounds, glimpses of threat
Trigger:  Monster encounter, chase sequence
Aftermath: Escape to safety, catch breath
```

## Emotion Through Disciplines

### Art and Emotion

**Color**:
- Warm colors → comfort, energy
- Cool colors → calm, sadness
- Desaturation → melancholy, dread

**Composition**:
- Open space → freedom, vulnerability
- Tight space → claustrophobia, focus
- Symmetry → stability, order
- Asymmetry → tension, unease

**Light**:
- Bright → safety, hope
- Dark → danger, mystery
- Contrast → drama, attention

### Sound and Emotion

**Music**:
- Major keys → happiness, triumph
- Minor keys → sadness, tension
- Tempo → energy level
- Dynamics → intensity variation

**SFX**:
- Sharp sounds → alertness, danger
- Soft sounds → calm, comfort
- Low frequency → power, dread
- High frequency → tension, alarm

**Silence**:
- Sudden silence → anticipation, dread
- Peaceful silence → rest, meditation
- Oppressive silence → isolation, vulnerability

### Mechanics and Emotion

**Control**:
- High control → empowerment, mastery
- Low control → vulnerability, tension
- Precise control → satisfaction, flow
- Loose control → panic, chaos

**Feedback**:
- Immediate feedback → satisfaction, clarity
- Delayed feedback → anticipation, anxiety
- Generous feedback → confidence, reward
- Punishing feedback → stakes, caution

**Stakes**:
- High stakes → tension, investment
- Low stakes → relaxation, experimentation
- Permanent consequences → weight, dread
- Reversible consequences → freedom, play

## Emotion by Game State

### Menu/Loading

Target: Anticipation, immersion introduction
- Music sets tone
- Visuals establish world
- No frustration (fast, smooth)

### Onboarding/Tutorial

Target: Confidence, curiosity
- Success rate high
- Gentle learning curve
- Wonder at new systems

### Core Loop

Target: [Varies by game]
- Matches primary emotional target
- Sustainable intensity
- Flow state access

### Fail States

Target: Motivation, not frustration
- Clear feedback (why fail?)
- Quick recovery (low friction)
- Progress preserved (not punitive)

### Victory States

Target: Satisfaction, triumph
- Clear acknowledgment
- Proportional celebration
- Setup for next challenge

### Rest Points

Target: Relief, preparation
- Safe spaces
- Progress saving
- Emotional processing

## Emotional Testing

### Playtesting Questions

**During play**:
- "What are you feeling right now?"
- "On a scale of 1-10, how tense are you?"
- "What's making you feel that way?"

**After play**:
- "What was the most emotional moment?"
- "When were you most frustrated?"
- "When were you most satisfied?"
- "Describe the game in emotional terms"

### Emotional Heat Map

Track emotional states across the game:

```
Area/Level | Fear | Joy | Frustration | Satisfaction
───────────┼──────┼─────┼─────────────┼─────────────
Tutorial   |  1   |  4  |      2      |      5
Level 1    |  3   |  5  |      2      |      5
Boss 1     |  6   |  2  |      5      |      8
Level 2    |  5   |  3  |      3      |      4
...
```

### Red Flags

**Emotional Problems**:
- Extended frustration without relief
- Boredom in core loop
- Fear without safety opportunities
- Triumph without challenge

**Pacing Problems**:
- Intensity too consistent (no contrast)
- Spikes too frequent (exhaustion)
- Recovery too long (disengagement)
- Build too slow (boredom)

## Emotional Coherence

### Vision Alignment

Each emotional moment should:
- Support creative pillars
- Match experience promise
- Serve the emotional arc
- Fit the tonal palette

### Cross-Discipline Check

For each emotional beat:
- Does art support the emotion?
- Does sound support the emotion?
- Do mechanics support the emotion?
- Do they reinforce each other?

### Anti-Pattern Detection

**Mixed Messages**:
- Happy music during tragedy
- Cheerful visuals in horror
- Power fantasy mechanics in vulnerability narrative

**Emotional Whiplash**:
- Jarring tone shifts
- Inconsistent intensity
- Unearned emotional moments

**Emotional Numbness**:
- Too much of one emotion
- No contrast or variety
- Predictable patterns
