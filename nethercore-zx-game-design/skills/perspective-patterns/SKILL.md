---
name: Perspective-Based Design Patterns
description: This skill should be used when the user asks about "side-scroller design", "top-down game", "third-person design", "first-person game", "camera style", "2D game design", "3D game design", "perspective choice", "camera perspective", or discusses choosing a camera/view approach for their Nethercore ZX game.
version: 0.1.0
---

# Perspective-Based Design Patterns

Design patterns organized by camera perspective for Nethercore ZX games. Each perspective has optimal render modes, memory budgets, control schemes, and common genres.

## Perspective Overview

| Perspective | Dimensions | Render Modes | Common Genres |
|-------------|------------|--------------|---------------|
| Side-Scroller | 2D/2.5D | 0, 1, 3 | Platformer, Fighter, Puzzle |
| Top-Down | 2D/2.5D | 0, 1, 2 | Racing, Shooter, Strategy |
| Third-Person | Full 3D | 1, 2, 3 | Action, Adventure, Platformer |
| First-Person | Full 3D | 2, 3 | Shooter, Exploration |

## Side-Scroller (2D/2.5D)

### Characteristics
- Camera fixed on one axis (usually horizontal scroll)
- Player moves left/right, may jump up/down
- Depth used for parallax or 2.5D layering

### Recommended Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 0 (Lambert) or 3 (Blinn-Phong) | 0 for sprites, 3 for 2.5D |
| Tick Rate | 60 fps | Smooth platforming |
| Resolution | 960×540 (fixed) | Wide format good for horizontal |

### Control Scheme

| Input | Action |
|-------|--------|
| D-Pad / Left Stick | Move left/right |
| A | Jump |
| B | Attack / Interact |
| X/Y | Special abilities |
| L1/R1 | Shoulder functions (dash, etc.) |

**Notes:**
- D-pad preferred for precision platforming
- Analog stick viable for analog-speed movement
- Vertical stick input often unused or for ladder climbing

### Memory Budget Example (Platformer)

```
ROM Budget (~8 MB):
├── Player + animations: 400 KB
├── Enemies (10 types): 1 MB
├── Tilesets (5 worlds): 2 MB
├── Backgrounds (parallax layers): 1.5 MB
├── Audio: 2 MB
├── Code: 200 KB
└── UI: 300 KB
```

### Common Design Patterns

**Level Structure:**
- Linear progression or hub-based
- Checkpoints every 30-60 seconds of gameplay
- Hidden areas reward exploration

**Enemy Patterns:**
- Ground-based (walkers, jumpers)
- Aerial (flyers, divers)
- Stationary hazards (shooters, traps)

**Camera Behavior:**
- Follow player with slight lead
- Lock during boss encounters
- Vertical scroll for climbing sections

### Genre Variations

| Genre | Key Design Focus |
|-------|------------------|
| Platformer | Jump physics, level geometry |
| Fighter | Hitboxes, frame data, spacing |
| Puzzle | Logic systems, interactions |
| Run & Gun | Enemy patterns, shooting mechanics |
| Metroidvania | Interconnected map, ability gating |

---

## Top-Down (2D/2.5D)

### Characteristics
- Camera looks down at play area
- Full 360° movement in horizontal plane
- Often used for vehicles or overhead action

### Recommended Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 0 or 2 | 0 for sprites, 2 for 3D top-down |
| Tick Rate | 60 fps | Standard for action |
| Resolution | 960×540 | Good visibility |

### Control Scheme

| Input | Action |
|-------|--------|
| Left Stick | Movement (8-way or 360°) |
| Right Stick | Aim direction (twin-stick) |
| A | Primary action |
| B | Secondary action |
| L2/R2 | Analog controls (speed, aim) |

**Notes:**
- Twin-stick for shooters (move + aim separately)
- Single-stick for simpler games
- D-pad works for 8-directional movement

### Memory Budget Example (Racing)

```
ROM Budget (~10 MB):
├── Vehicles (8 types): 1 MB
├── Tracks (6 tracks): 4 MB
├── Track textures: 2 MB
├── Effects (skid, dust): 500 KB
├── Audio: 2 MB
├── Code: 300 KB
└── UI: 200 KB
```

### Common Design Patterns

**Movement Systems:**
- Grid-based (puzzle, strategy)
- Free movement (shooters, racing)
- Physics-based (vehicles)

**View Distance:**
- Fixed zoom (consistent scale)
- Dynamic zoom (show more during speed)
- Minimap for navigation

**Multiplayer Considerations:**
- Split-screen viable
- Shared screen with viewport management
- Off-screen indicators

### Genre Variations

| Genre | Key Design Focus |
|-------|------------------|
| Racing | Track design, physics feel |
| Twin-Stick Shooter | Enemy spawns, bullet patterns |
| Strategy | Unit management, fog of war |
| Puzzle | Grid mechanics, undo system |
| Dungeon Crawler | Room generation, combat |

---

## Third-Person (3D)

### Characteristics
- Camera follows behind/beside player character
- Full 3D movement and environment
- Character always visible (except close walls)

### Recommended Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 2 or 3 | 2 for modern, 3 for retro |
| Tick Rate | 60 fps | Smooth 3D movement |
| Resolution | 960×540 | Standard 3D |

### Control Scheme

| Input | Action |
|-------|--------|
| Left Stick | Character movement |
| Right Stick | Camera control |
| A | Jump / Confirm |
| B | Attack / Cancel |
| X/Y | Actions / Abilities |
| L1 | Target lock / Strafe |
| R1 | Block / Guard |
| L2/R2 | Aim / Fire (action games) |
| L3/R3 | Sprint / Camera reset |

**Notes:**
- Right stick camera is expected in modern 3D
- Target lock helps combat camera management
- L3 sprint is genre standard

### Memory Budget Example (Action-Adventure)

```
ROM Budget (~12 MB):
├── Player (high-poly hero): 500 KB
├── NPCs/Enemies (15 types): 3 MB
├── Environments (4 areas): 4 MB
├── Environment textures: 2 MB
├── Audio: 2 MB
├── Animations: 500 KB
└── Code + UI: 500 KB
```

### Common Design Patterns

**Camera Systems:**
- Follow cam (offset behind player)
- Orbit cam (player rotates, camera follows)
- Context-sensitive (tightens in combat)
- Collision avoidance (push through walls)

**Combat Patterns:**
- Lock-on targeting
- Directional attacks (based on stick)
- Combo systems
- Dodge/roll mechanics

**World Design:**
- Hub + levels or open sections
- Verticality (climbing, falling)
- Landmark navigation

### Genre Variations

| Genre | Key Design Focus |
|-------|------------------|
| 3D Platformer | Jump feel, camera, collectibles |
| Character Action | Combat depth, style systems |
| Adventure | Exploration, puzzle integration |
| Third-Person Shooter | Cover, aiming, enemy AI |

---

## First-Person (3D)

### Characteristics
- Camera IS the player's view
- No visible player character
- Maximum immersion, limited peripheral vision

### Recommended Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 2 or 3 | Lighting important for atmosphere |
| Tick Rate | 60 or 120 fps | Smooth look essential |
| Resolution | 960×540 | Standard |

### Control Scheme

| Input | Action |
|-------|--------|
| Left Stick | Move forward/back, strafe |
| Right Stick | Look/aim |
| A | Jump |
| B | Crouch / Slide |
| X | Reload / Interact |
| Y | Switch weapon |
| L2 | Aim down sights |
| R2 | Fire |
| L1/R1 | Grenades / Abilities |

**Notes:**
- Look sensitivity is critical — allow configuration
- Dead zones affect aim precision
- 120 fps tick rate improves aim feel

### Memory Budget Example (Shooter)

```
ROM Budget (~10 MB):
├── Weapons (8 types + hands): 1 MB
├── Enemies (6 types): 2 MB
├── Levels (4 maps): 4 MB
├── Level textures: 1.5 MB
├── Audio: 1 MB
├── Code: 300 KB
└── UI (HUD, menus): 200 KB
```

### Common Design Patterns

**View Considerations:**
- Limited peripheral vision
- Audio cues for off-screen threats
- Minimap or compass for navigation
- Clear HUD design

**Movement Feel:**
- Head bob (optional, can cause nausea)
- Weapon sway
- Inertia and momentum
- Footstep sounds for feedback

**Combat Patterns:**
- Hitscan or projectile weapons
- Recoil patterns
- Aim assist (console-friendly)
- Clear hit feedback

### Genre Variations

| Genre | Key Design Focus |
|-------|------------------|
| FPS | Weapon balance, map flow, multiplayer |
| Horror | Atmosphere, resource tension |
| Exploration | Environmental storytelling |
| Puzzle | First-person manipulation |

---

## Perspective Selection Guide

### Decision Flowchart

```
What's the core experience?

├── Character-focused action/story
│   ├── Need to see character? → Third-Person
│   └── Immersive world? → First-Person
│
├── Precision platforming
│   └── → Side-Scroller
│
├── Vehicle/overhead action
│   └── → Top-Down
│
└── Tactical/strategic view
    └── → Top-Down
```

### Perspective Tradeoffs

| Aspect | Side-Scroll | Top-Down | Third-Person | First-Person |
|--------|-------------|----------|--------------|--------------|
| Asset complexity | Low | Low-Med | High | Medium |
| Camera complexity | Low | Low | High | Low |
| Control complexity | Low | Medium | High | Medium |
| Immersion | Low | Low | Medium | High |
| Spatial awareness | High | High | Medium | Low |
| Motion sickness risk | None | None | Low | Medium |

### Hybrid Approaches

Some games blend perspectives:

- **2.5D:** Side-scroller with 3D graphics (Mode 1 or 3)
- **Isometric:** Top-down angled view (Mode 2)
- **Over-shoulder:** Close third-person (approaching first)
- **Dynamic:** Switch perspectives contextually

## Additional Resources

### Reference Files

For detailed perspective-specific guides:
- **`references/side-scroller-patterns.md`** — Platformer and 2D design
- **`references/3d-camera-systems.md`** — Camera implementation patterns
- **`references/control-feel.md`** — Input tuning for each perspective
