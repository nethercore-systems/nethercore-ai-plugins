# Visual Composition for Games

## Composition Fundamentals

### Purpose of Composition

Composition guides the player's eye and communicates:
1. **Where to look** - Focus and attention
2. **Where to go** - Navigation and path
3. **What matters** - Hierarchy and importance
4. **How to feel** - Mood and tension

### The Rule of Thirds

Divide the frame into a 3x3 grid. Place key elements at:
- **Power points**: Grid intersections
- **Lines**: Along vertical/horizontal thirds

For games:
- Player character often at left-third (reading direction)
- Goals/objectives at right-third
- HUD avoids center third (gameplay area)

### Leading Lines

Lines that guide the eye toward focal points:

**Types:**
- Explicit: Roads, rivers, corridors
- Implicit: Character gaze, weapon aim, lighting direction
- Environmental: Architecture, terrain contours

**In games:**
- Level design uses leading lines for navigation
- Combat arenas use lines to highlight threats
- Cutscenes use lines for cinematic framing

### Framing

Use environmental elements to frame subjects:
- Doorways, windows, archways
- Vegetation, pillars, vehicles
- Light pools, shadows

**Benefits:**
- Draws attention to framed subject
- Creates depth layers
- Establishes context

## Visual Hierarchy in Games

### The 3-Second Test

A player should understand the scene in 3 seconds:
1. **Second 1**: What am I? (player identification)
2. **Second 2**: What's threatening? (enemies, hazards)
3. **Second 3**: Where should I go? (objectives, paths)

### Hierarchy Tools

**Size**: Larger = More important
**Contrast**: Higher contrast = More attention
**Saturation**: More saturated = More prominent
**Detail**: More detail = More focus
**Motion**: Moving elements draw eye
**Isolation**: Separated elements stand out

### Layered Hierarchy

```
LAYER 1 (Immediate)
├── Player character
├── Health/critical HUD
└── Immediate threats

LAYER 2 (Active)
├── Interactive objects
├── Enemies (non-immediate)
└── Pickups/resources

LAYER 3 (Environmental)
├── Navigation cues
├── Environmental storytelling
└── Background detail

LAYER 4 (Ambient)
├── Atmospheric effects
├── Sky/horizon
└── Distant detail
```

## Game-Specific Composition

### Camera Considerations

**Third-Person**
- Character typically in lower third
- Negative space in direction of movement
- Horizon at upper or lower third

**Top-Down**
- Player often centered or offset to edge
- Objectives visible in frame
- Clear read of navigation options

**Side-Scrolling**
- Character in left third (for left-to-right progression)
- Rightward negative space for upcoming content
- Vertical thirds for platform levels

### HUD Integration

HUD should complement, not compete with, game composition:
- **Safe zones**: Keep critical gameplay in center
- **Corner anchoring**: HUD elements at screen edges
- **Transparency**: Let action show through when needed
- **Dynamic hiding**: Reduce HUD during exploration/narrative

### Combat Composition

During combat, composition shifts:
- **Player prominence**: Always visible and readable
- **Threat clarity**: Enemies distinctly composed
- **Attack telegraphing**: Visual space for threat indicators
- **Exit visibility**: Escape routes should be apparent

## Depth and Space

### Creating Depth

**Overlapping**: Objects in front of others
**Size diminution**: Smaller = Further
**Atmospheric perspective**: Haze, desaturation with distance
**Detail falloff**: Less detail in background
**Shadow and light**: Lighting establishes depth

### Spatial Rhythm

Alternate between:
- Open spaces (rest, overview)
- Tight spaces (tension, action)
- Vertical spaces (awe, danger)
- Horizontal spaces (journey, progress)

### The Z-Axis

Even 2D games benefit from depth layers:
- **Parallax layers**: Background, midground, foreground
- **Entity sorting**: Proper overlap based on Y position
- **Shadow casting**: Grounds objects in space

## Mood Through Composition

### Stability vs. Tension

**Stable (Safe zones)**
- Horizontal lines dominant
- Symmetrical or balanced
- Central placement
- Even distribution

**Tense (Danger zones)**
- Diagonal lines dominant
- Asymmetrical, unbalanced
- Off-center placement
- Clustered or sparse extremes

### Scale and Power

**Small player, large environment**: Vulnerability, exploration
**Player-scale environments**: Adventure, action
**Player larger than elements**: Power fantasy, control

### Negative Space

Empty space communicates:
- **Isolation**: Character alone in vast space
- **Focus**: Single object demands attention
- **Anticipation**: Space implies something will fill it
- **Rest**: Visual breathing room

## Practical Application

### Scene Composition Checklist

- [ ] Primary focal point is clear
- [ ] Secondary elements support, don't compete
- [ ] Leading lines guide appropriately
- [ ] Depth is established
- [ ] Hierarchy serves gameplay
- [ ] HUD integrates cleanly
- [ ] Mood matches narrative intent

### Common Mistakes

**Over-cluttering**
- Too many competing elements
- No clear hierarchy
- Visual noise

**Under-composition**
- Empty without purpose
- No focal point
- Boring layouts

**Fighting the camera**
- Composition that doesn't work at game's camera angle
- Elements that obstruct gameplay
- HUD covering critical areas

### Testing Composition

1. **Screenshot test**: Pause game, evaluate as a still image
2. **Blur test**: Blur screenshot, check if shapes read
3. **B&W test**: Remove color, check value structure
4. **Squint test**: Squint at screen, see what stands out
5. **3-second test**: Look away, look back, note first impressions
