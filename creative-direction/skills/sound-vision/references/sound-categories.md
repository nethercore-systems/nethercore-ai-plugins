# Sound Effect Categories and Design

## Category Taxonomy

### Player Sounds

Sounds directly caused by or related to the player character.

**Movement**
- Footsteps (surface-aware)
- Jumps, landings
- Climbing, swimming
- Dash, dodge, roll

**Actions**
- Attack swings, impacts
- Ability activations
- Item use (potions, tools)
- Interactions (doors, switches)

**Feedback**
- Damage taken
- Health changes
- Status effects
- Death

**Design Principles**:
- Highest priority in mix
- Immediate response (< 50ms latency)
- Consistent across all player types
- Satisfying, responsive feel

### Enemy Sounds

Sounds from hostile entities.

**Presence**
- Idle sounds, breathing
- Movement sounds
- Ambient presence

**Threat**
- Attack windups (telegraphs)
- Attack execution
- Special ability sounds

**Response**
- Damage taken
- Stagger, stunned
- Death

**Design Principles**:
- Distinct from player sounds
- Clear threat identification
- Spatial positioning
- Readable attack telegraphs

### Environment Sounds

World-building audio.

**Ambient Beds**
- Room tone
- Weather
- Time-of-day atmosphere
- Zone-specific ambience

**Ambient Details**
- Bird calls, insects
- Water, wind effects
- Creaking, settling sounds
- Distant activity

**Interactive Environment**
- Doors, gates
- Breakables
- Traps triggering
- Moving platforms

**Design Principles**:
- Support, don't compete with gameplay
- Create sense of place
- Subtle variation
- Spatial consistency

### UI Sounds

Interface and feedback audio.

**Navigation**
- Menu hover, select
- Scroll, page turn
- Tab switching
- Menu open/close

**Feedback**
- Confirmation
- Error/invalid
- Warning
- Achievement

**Game State**
- Save/load
- Pause/unpause
- Level transition
- Game over/victory

**Design Principles**:
- Non-diegetic (no spatial position)
- Consistent across all UI
- Quick, non-intrusive
- Learnable patterns

### Collectibles/Pickups

Item collection sounds.

**Categories**
- Currency (coins, gems)
- Health/resources
- Power-ups
- Key items
- Weapons/equipment

**Design Principles**:
- Satisfying "reward" feel
- Value indicated by sound
- Quick to not interrupt flow
- Pleasant on repetition

## Sound Design Approaches

### Foley (Recorded Sounds)

**Strengths**:
- Natural, organic feel
- Quick to implement
- Realistic detail

**Use for**:
- Footsteps
- Cloth/movement
- Object handling
- Body impacts

### Synthesized Sounds

**Strengths**:
- Complete control
- Unique character
- Easy variation

**Use for**:
- UI feedback
- Sci-fi/fantasy elements
- Abstract effects
- Stylized impacts

### Hybrid (Layered)

**Strengths**:
- Best of both worlds
- Rich, complex sounds
- Unique but grounded

**Use for**:
- Weapons
- Magic/abilities
- Creatures
- Major impacts

## Sound Design Templates

### Impact Sound Layers

```
Layer 1 - Transient:  Initial "crack" or "thud" (50-100ms)
Layer 2 - Body:       Mid-frequency meat (100-300ms)
Layer 3 - Sub:        Low-frequency weight (100-500ms)
Layer 4 - Tail:       Decay/reverb/debris (500ms+)
```

### Movement Sound Elements

```
Footstep:
├── Surface Impact:   What they're stepping on
├── Material:         Shoe/foot material
├── Weight:           Character mass
└── Environment:      Room reverb

Jump:
├── Effort:           Character vocalization
├── Takeoff:          Ground departure
├── Air:              Whoosh (optional)
└── Landing:          Impact + recovery
```

### Weapon Sound Elements

```
Melee Swing:
├── Whoosh:           Air displacement
├── Effort:           Grunt/breath
└── Material:         Blade/blunt character

Melee Hit:
├── Impact:           Flesh, armor, material
├── Feedback:         Crunch, squelch, clang
└── Target Response:  Pain, stagger

Ranged Shot:
├── Mechanism:        Trigger, string, release
├── Propulsion:       Gunshot, arrow flight
├── Projectile:       Whoosh, whistle
└── Impact:           Hit or miss feedback
```

### Magic/Ability Elements

```
Cast:
├── Gather:           Energy accumulation
├── Release:          Ability fires
├── Travel:           Projectile or area
└── Impact/Effect:    Result

Buff/Status:
├── Application:      Initial hit
├── Loop:             Sustained effect (subtle)
└── End:              Effect expires
```

## Variation Strategies

### Randomization Parameters

**Pitch**
- Range: ±2-5 semitones for subtle variation
- Range: ±12 semitones for obvious variation
- Consider musical context

**Volume**
- Range: ±1-3dB for subtle variation
- More variation for ambient sounds
- Less for critical feedback

**Timing**
- Slight delays for organic feel
- Jitter: 0-50ms for footsteps
- Quantize to beat for rhythmic sounds

### Round-Robin

Multiple sound files played in rotation:
- Minimum 3 variations for common sounds
- 5-8 variations for very frequent sounds (footsteps)
- Shuffle or sequential order

### Procedural Variation

Real-time modification:
- Filter sweeps
- Granular synthesis
- Parameter modulation
- Concatenative synthesis

## Mix Placement

### Frequency Slots

```
Category          Primary Frequency Range
──────────────────────────────────────────
Footsteps         80-300Hz (weight), 2-5kHz (detail)
Weapons           40-150Hz (power), 3-8kHz (attack)
UI                1-4kHz (clarity)
Ambience          Below 500Hz, above 8kHz (space)
Voice             500Hz-4kHz (intelligibility)
Music             Full spectrum (ducked in gameplay)
```

### Spatial Placement

```
Category          Spatial Treatment
──────────────────────────────────────────
Player            Centered, close, minimal reverb
Enemies           Positional, distance-based
Environment       Stereo spread, ambient reverb
UI                Centered, non-spatial
Music             Wide stereo, separate space
```

## ZX Audio Considerations

### 8-Channel SFX Budget

Allocate by priority:

```
Reserved Channels:
├── Channel 1:    Player action (always)
├── Channel 2:    Player feedback (damage, etc.)
├── Channels 3-4: Combat/enemies
├── Channels 5-6: Environment
└── Channels 7-8: UI + overflow
```

### Channel Stealing

When all channels full:
1. Determine new sound priority
2. Find lowest priority playing sound
3. If new > playing, steal channel
4. Apply quick fade to avoid click

### Format Optimization

```
High Priority (full quality):
- Player actions
- UI feedback
- Key game sounds

Medium Priority:
- Enemy sounds
- Important environment

Low Priority (compressed):
- Ambient beds
- Background detail
- Distant sounds
```

## Quality Checklist

### Per-Sound Checks

- [ ] Distinct, recognizable character
- [ ] Appropriate loudness relative to category
- [ ] Clean transients, no unwanted clicks
- [ ] Proper length (no wasted tail)
- [ ] Variation exists (pitch, selection, etc.)
- [ ] Spatial treatment matches category
- [ ] Works in context with other sounds

### Per-Category Checks

- [ ] Consistent loudness within category
- [ ] Consistent processing aesthetic
- [ ] Frequency ranges don't overlap destructively
- [ ] Priority system works correctly
- [ ] Enough variation for repetition tolerance

### Full Mix Checks

- [ ] Player always audible
- [ ] No frequency masking conflicts
- [ ] Music and SFX balanced
- [ ] Spatial image coherent
- [ ] Dynamic range appropriate
- [ ] No clipping at any point
