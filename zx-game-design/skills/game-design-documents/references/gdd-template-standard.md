# Standard GDD Template

**Game Title:** [Working Title]
**Author:** [Name]
**Version:** [0.1.0]
**Date:** [Date]
**Target Platform:** Nethercore ZX

---

## 1. Overview

### High Concept
[2-3 sentences describing the core game experience]

### Target Audience
[Who is this game for? Skill level? Age range?]

### Reference Games
[1-3 games that inspired this design, with specific aspects referenced]

### Unique Selling Points
1. [What makes this game stand out?]
2. [Key differentiator]
3. [Core innovation]

---

## 2. ZX Platform Configuration

### Render Mode

| Setting | Value |
|---------|-------|
| Mode | [0: Lambert / 1: Matcap / 2: MR-Blinn-Phong / 3: Blinn-Phong] |
| Rationale | [Why this mode matches the art direction] |

### Tick Rate

| Setting | Value |
|---------|-------|
| Rate | [24 / 30 / 60 / 120] fps |
| Rationale | [Why this rate for this game type] |

### Multiplayer Configuration

| Setting | Value |
|---------|-------|
| Player Count | [1-4] |
| Mode | [Single / Local Co-op / Online / Both] |
| Determinism Notes | [Any special considerations] |

---

## 3. Core Mechanics

### Primary Mechanic
**[Name of mechanic]**
[Detailed description of how it works]

### Secondary Mechanics
1. **[Mechanic 2]:** [Description]
2. **[Mechanic 3]:** [Description]

### Game Loop

```
[Visual diagram or step-by-step of the core loop]

Example:
┌─────────────┐
│   EXPLORE   │
└──────┬──────┘
       ↓
┌─────────────┐
│  ENCOUNTER  │
└──────┬──────┘
       ↓
┌─────────────┐
│   RESOLVE   │
└──────┬──────┘
       ↓
┌─────────────┐
│   REWARD    │
└──────┴──────→ Loop
```

### Progression System
[How does the player advance? Levels? Upgrades? Story?]

---

## 4. Controls

### Full Control Scheme

| Input | Action | Context |
|-------|--------|---------|
| Left Stick | Movement | Gameplay |
| Right Stick | Camera | Gameplay |
| D-Pad | [Action] | [Context] |
| A | [Primary action] | Gameplay |
| B | [Cancel/Back] | Menus |
| X | [Action] | Gameplay |
| Y | [Action] | Gameplay |
| L1/R1 | [Modifier] | Gameplay |
| L2/R2 | [Analog action] | Gameplay |
| Start | Pause | All |
| Select | [Action] | [Context] |

### Control Feel Notes
[Describe input responsiveness, aim assist, dead zones, etc.]

---

## 5. Level/World Structure

### Overview
[How is the game world organized? Linear levels? Open world? Hub?]

### Level List

| Level | Theme | Key Features | Est. Size |
|-------|-------|--------------|-----------|
| 1 | [Theme] | [Features] | ~___KB |
| 2 | [Theme] | [Features] | ~___KB |
| ... | | | |

### Difficulty Progression
[How does difficulty scale across levels?]

---

## 6. Memory Budget

### ROM Allocation (16 MB Total)

| Category | Budget | Breakdown |
|----------|--------|-----------|
| WASM Code | ___KB | Game logic, libraries |
| Meshes | ___MB | [X] characters, [X] levels |
| Textures | ___MB | Diffuse, materials, UI |
| Audio | ___MB | [X] SFX, [X] music tracks |
| Animations | ___KB | [X] characters × [X] anims |
| Fonts/UI | ___KB | Fonts, UI atlas |
| **Total** | ___MB | Remaining: ___MB |

### RAM State (4 MB, target < 100KB for state)

| Category | Size | Notes |
|----------|------|-------|
| Player state | ~___bytes | Per player |
| Entity pool | ~___bytes | Max [X] entities |
| World state | ~___bytes | Active level data |
| Input buffer | ~___bytes | Rollback frames |
| **State Total** | ~___KB | |

---

## 7. Audio Design

### Music

| Track | Purpose | Duration | Est. Size |
|-------|---------|----------|-----------|
| Main Theme | Title screen | ~30s loop | ~___KB |
| [Level Theme] | [Where used] | ~___s | ~___KB |
| ... | | | |

### Sound Effects

| Category | Count | Examples |
|----------|-------|----------|
| Player | [X] | Jump, land, attack, hurt, death |
| Enemy | [X] | [Examples] |
| UI | [X] | Select, confirm, cancel |
| Environment | [X] | [Examples] |

### Audio Channel Budget (16 channels)

| Category | Reserved Channels |
|----------|-------------------|
| Music | 1 (dedicated) |
| Player SFX | [X] |
| Enemy SFX | [X] |
| Environment | [X] |
| UI | [X] |
| **Total** | ≤16 |

---

## 8. Asset Specifications

### Characters

| Character | Mesh Size | Textures | Animations | Total |
|-----------|-----------|----------|------------|-------|
| Player | ~___KB | ___×___ diff + mat | [X] anims | ~___KB |
| [Enemy 1] | ~___KB | ___×___ | [X] anims | ~___KB |
| ... | | | | |

### Environments

| Environment | Mesh Size | Textures | Notes |
|-------------|-----------|----------|-------|
| [Level 1] | ~___KB | [X] × ___×___ | [Notes] |
| ... | | | |

### Procgen Opportunities

Mark assets suitable for procedural generation:
- [ ] [Asset type] — [PROCGEN: technique]
- [ ] [Asset type] — [PROCGEN: technique]

---

## 9. Technical Considerations

### Performance Targets
- Target frame rate: [X] fps
- Max entities on screen: [X]
- Draw call budget: [X]

### Known Challenges
1. **[Challenge]:** [How to address]
2. **[Challenge]:** [How to address]

### zx-dev Integration Points
- [ ] [Feature] → zx-dev: [System]
- [ ] [Feature] → zx-dev: [System]

---

## 10. Development Roadmap

### Phase 1: Prototype
- [ ] Core mechanic implementation
- [ ] Placeholder assets
- [ ] Basic game loop

### Phase 2: Pre-Production
- [ ] All mechanics functional
- [ ] Art direction established
- [ ] Full level blockouts

### Phase 3: Production
- [ ] Final assets
- [ ] Polish pass
- [ ] Bug fixing

### Phase 4: Release
- [ ] Testing complete
- [ ] ROM packaged
- [ ] Distribution
