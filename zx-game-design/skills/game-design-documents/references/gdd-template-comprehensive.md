# Comprehensive GDD Template

**Game Title:** [Working Title]
**Subtitle:** [Optional tagline]
**Author:** [Name / Team]
**Version:** [0.1.0]
**Last Updated:** [Date]
**Target Platform:** Nethercore ZX

---

# Part 1: Vision & Concept

## 1.1 Executive Summary

### High Concept
[2-3 sentences: What is this game? What does the player experience?]

### Genre & Perspective
- **Genre:** [e.g., 3D Platformer, Fighting, Racing]
- **Perspective:** [Side-scroller / Top-down / Third-person / First-person]
- **Camera:** [Fixed / Follow / Free]

### Target Audience
| Attribute | Description |
|-----------|-------------|
| Age Range | [e.g., 13+] |
| Skill Level | [Casual / Core / Hardcore] |
| Play Session | [5-10 min / 30-60 min / 2+ hours] |
| Accessibility | [Considerations] |

### Unique Selling Points
1. [Primary differentiator]
2. [Secondary differentiator]
3. [Tertiary differentiator]

### Reference Games
| Game | Aspect Referenced |
|------|-------------------|
| [Game 1] | [What inspired from it] |
| [Game 2] | [What inspired from it] |
| [Game 3] | [What inspired from it] |

---

## 1.2 Player Experience Goals

### Core Fantasy
[What fantasy does this game fulfill for the player?]

### Emotional Journey
[What emotions should the player feel? At what points?]

### Moment-to-Moment Feel
[How should each second of gameplay feel?]

---

# Part 2: Platform Configuration

## 2.1 Render Mode Selection

| Setting | Value |
|---------|-------|
| **Mode** | [0: Lambert / 1: Matcap / 2: MR-Blinn-Phong / 3: Blinn-Phong] |
| **Rationale** | [Detailed explanation] |

### Visual Style Guidelines
[How does this render mode inform the art direction?]

### Texture Workflow
| Channel | Purpose | Format |
|---------|---------|--------|
| Slot 0 | [Albedo] | [Resolution] |
| Slot 1 | [MRE/SSE/Matcap] | [Resolution] |
| Slot 2 | [Specular/Matcap] | [Resolution] |

---

## 2.2 Tick Rate & Timing

| Setting | Value |
|---------|-------|
| **Tick Rate** | [24 / 30 / 60 / 120] fps |
| **Rationale** | [Why this rate?] |

### Timing Considerations
- Input latency requirements
- Animation smoothness needs
- Network considerations (if multiplayer)

---

## 2.3 Multiplayer Configuration

| Setting | Value |
|---------|-------|
| **Max Players** | [1-4] |
| **Modes Supported** | [Single / Local / Online / All] |
| **Netcode** | GGRS Rollback |

### Determinism Requirements
| System | Determinism Notes |
|--------|-------------------|
| Physics | [How handled] |
| AI | [How handled] |
| Random | [Seeded via random() FFI] |
| Animation | [Frame-based, not time-based] |

### Rollback State Design
```
Game State (~___KB):
├── Player states: ___bytes × 4
├── Entity pool: ___bytes × max
├── World state: ___bytes
├── Input history: ___bytes
└── RNG state: ___bytes
```

---

# Part 3: Gameplay Systems

## 3.1 Core Mechanics

### Primary Mechanic: [Name]
[Detailed description]

**Implementation Notes:**
- [Technical consideration 1]
- [Technical consideration 2]

### Secondary Mechanics

#### [Mechanic 2 Name]
[Description and implementation notes]

#### [Mechanic 3 Name]
[Description and implementation notes]

---

## 3.2 Game Loop

### Macro Loop (Session)
```
[Diagram of overall session flow]
```

### Micro Loop (Moment-to-Moment)
```
[Diagram of core gameplay loop]
```

### Reward Loop
[How are players rewarded? What's the psychological hook?]

---

## 3.3 Progression System

### Player Progression
[How does the player character grow/change?]

### World Progression
[How does the game world respond to player progress?]

### Difficulty Curve
```
Difficulty
    │
    │            ┌──────
    │       ┌────┘
    │  ┌────┘
    │──┘
    └─────────────────────► Level
      1    2    3    4    5
```

---

## 3.4 Controls

### Control Scheme

| Input | Gameplay | Menus | Cutscenes |
|-------|----------|-------|-----------|
| Left Stick | [Action] | Navigate | - |
| Right Stick | [Action] | - | - |
| D-Pad | [Action] | Navigate | - |
| A | [Action] | Confirm | Skip |
| B | [Action] | Back | Skip |
| X | [Action] | [Action] | - |
| Y | [Action] | [Action] | - |
| L1 | [Action] | Tab left | - |
| R1 | [Action] | Tab right | - |
| L2 | [Action] | - | - |
| R2 | [Action] | - | - |
| L3 | [Action] | - | - |
| R3 | [Action] | - | - |
| Start | Pause | Close | Skip |
| Select | [Action] | [Action] | - |

### Control Feel Parameters
| Parameter | Value | Notes |
|-----------|-------|-------|
| Dead zone | [0.0-1.0] | |
| Acceleration | [Linear/Ease] | |
| Turn speed | [deg/tick] | |
| Aim assist | [None/Light/Heavy] | |

---

# Part 4: Content Design

## 4.1 World Structure

### World Map/Flow
```
[Diagram of world/level connections]
```

### Level Overview

| # | Name | Theme | Duration | Mechanics Introduced |
|---|------|-------|----------|---------------------|
| 1 | [Name] | [Theme] | ~X min | [Mechanics] |
| 2 | [Name] | [Theme] | ~X min | [Mechanics] |
| ... | | | | |

---

## 4.2 Level Design

### [Level 1 Name]

**Theme:** [Visual/audio theme]
**Duration:** [Expected time]
**Objective:** [What player must do]

**Key Moments:**
1. [Moment 1 - what happens, why it's memorable]
2. [Moment 2]
3. [Moment 3]

**Layout:**
```
[ASCII or description of level layout]
```

**Technical Budget:**
- Mesh: ~___KB
- Textures: ~___KB
- Entities: Max ___
- Audio channels used: ___

[Repeat for each level]

---

## 4.3 Characters & Entities

### Playable Characters

#### [Character 1 Name]

| Attribute | Value |
|-----------|-------|
| Role | [Role in game] |
| Mesh Size | ~___KB |
| Texture Set | ___×___ diff + ___×___ mat |
| Animation Count | [X] animations |
| Total Size | ~___KB |

**Animations:**
| Animation | Frames | Loop |
|-----------|--------|------|
| Idle | [X] | Yes |
| Walk | [X] | Yes |
| Run | [X] | Yes |
| Jump | [X] | No |
| Attack | [X] | No |
| Hurt | [X] | No |
| Death | [X] | No |

**Abilities:**
1. [Ability 1]: [Description]
2. [Ability 2]: [Description]

[Repeat for each character]

---

### Enemies/NPCs

#### [Enemy 1 Name]

| Attribute | Value |
|-----------|-------|
| Type | [Grunt / Elite / Boss] |
| Behavior | [AI description] |
| Mesh Size | ~___KB |
| Total Size | ~___KB |

**Attack Patterns:**
1. [Pattern 1]
2. [Pattern 2]

[Repeat for each enemy type]

---

## 4.4 Items & Collectibles

| Item | Purpose | Visual | Spawn Locations |
|------|---------|--------|-----------------|
| [Item 1] | [Purpose] | [Description] | [Where found] |
| [Item 2] | [Purpose] | [Description] | [Where found] |

---

# Part 5: Narrative Design

## 5.1 Story Overview

### Premise
[1-2 paragraphs: What's the story setup?]

### Plot Summary
[Brief outline of story arc]

### Ending(s)
[How does the story conclude? Multiple endings?]

---

## 5.2 Characters

### [Main Character]
- **Role:** Protagonist
- **Motivation:** [What drives them?]
- **Arc:** [How do they change?]

### [Supporting Character]
[Same structure]

### [Antagonist]
[Same structure]

---

## 5.3 Storytelling Methods

| Method | Usage |
|--------|-------|
| Cutscenes | [When/how used] |
| In-game dialogue | [When/how used] |
| Environmental storytelling | [Examples] |
| Collectibles/lore | [Examples] |

---

# Part 6: Art Direction

## 6.1 Visual Style

### Style Guide
[Description of overall visual approach]

### Color Palette
| Usage | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| Characters | [Color] | [Color] | [Color] |
| Environments | [Color] | [Color] | [Color] |
| UI | [Color] | [Color] | [Color] |

### Lighting Approach
[How is lighting used? Mood? Time of day?]

---

## 6.2 Asset Specifications

### Texture Standards

| Asset Type | Diffuse | Material | Max Size |
|------------|---------|----------|----------|
| Characters | ___×___ | ___×___ | ___KB |
| Props | ___×___ | ___×___ | ___KB |
| Environment | ___×___ | ___×___ | ___KB |
| UI | ___×___ | N/A | ___KB |

### Mesh Standards

| Asset Type | Triangle Budget | Format |
|------------|-----------------|--------|
| Characters | ___-___ tris | POS_UV_NORMAL_SKINNED |
| Props | ___-___ tris | POS_UV_NORMAL |
| Environment | ___-___ tris | POS_UV_NORMAL |

---

## 6.3 Procgen Asset Opportunities

| Asset | Technique | Parameters |
|-------|-----------|------------|
| [Texture type] | [Noise/Pattern] | [Key params] |
| [Mesh type] | [Procedural] | [Key params] |
| [Sound type] | [Synthesis] | [Key params] |

---

# Part 7: Audio Design

## 7.1 Music

### Music Style
[Genre, mood, instrumentation]

### Track List

| Track | Purpose | Duration | Loop Point | Size |
|-------|---------|----------|------------|------|
| Main Theme | Title | ~___s | ___s | ~___KB |
| [Level] | Gameplay | ~___s | ___s | ~___KB |
| Boss | Combat | ~___s | ___s | ~___KB |
| Victory | Win state | ~___s | N/A | ~___KB |
| Game Over | Lose state | ~___s | N/A | ~___KB |

---

## 7.2 Sound Effects

### Sound Categories

| Category | Count | Examples |
|----------|-------|----------|
| Player Actions | [X] | Jump, land, attack_1, attack_2, hurt, death |
| Enemy Sounds | [X] | [List] |
| Environment | [X] | [List] |
| UI Feedback | [X] | Select, confirm, cancel, error |
| Ambient | [X] | [List] |

### Sound Design Notes
[Special audio considerations, layering, etc.]

---

## 7.3 Audio Channel Plan

| Channel | Reserved For | Priority |
|---------|--------------|----------|
| Music | Background music | Always |
| 0-3 | Player sounds | High |
| 4-7 | Enemy sounds | Medium |
| 8-11 | Environment | Low |
| 12-15 | UI / Effects | Variable |

---

# Part 8: Memory Budget (Detailed)

## 8.1 ROM Budget (16 MB)

### Code
| Component | Size |
|-----------|------|
| Game logic | ~___KB |
| Libraries | ~___KB |
| **Subtotal** | ~___KB |

### Meshes
| Category | Count | Average | Total |
|----------|-------|---------|-------|
| Characters | [X] | ~___KB | ~___KB |
| Environments | [X] | ~___KB | ~___MB |
| Props | [X] | ~___KB | ~___KB |
| Effects | [X] | ~___KB | ~___KB |
| **Subtotal** | | | ~___MB |

### Textures
| Category | Count | Size Each | Total |
|----------|-------|-----------|-------|
| Char Diffuse | [X] | ~___KB | ~___KB |
| Char Material | [X] | ~___KB | ~___KB |
| Env Diffuse | [X] | ~___KB | ~___MB |
| Env Material | [X] | ~___KB | ~___MB |
| UI Atlas | [X] | ~___KB | ~___KB |
| **Subtotal** | | | ~___MB |

### Audio
| Category | Count | Total |
|----------|-------|-------|
| Music | [X] tracks | ~___MB |
| SFX | [X] sounds | ~___KB |
| **Subtotal** | | ~___MB |

### Animations
| Category | Count | Total |
|----------|-------|-------|
| Character anims | [X] | ~___KB |
| Object anims | [X] | ~___KB |
| **Subtotal** | | ~___KB |

### Summary
| Category | Size |
|----------|------|
| Code | ~___KB |
| Meshes | ~___MB |
| Textures | ~___MB |
| Audio | ~___MB |
| Animations | ~___KB |
| Fonts/Other | ~___KB |
| **TOTAL** | ~___MB |
| **Remaining** | ~___MB |

---

## 8.2 RAM State Budget

| Component | Size | Notes |
|-----------|------|-------|
| Player state × 4 | ~___bytes | Position, velocity, health, etc. |
| Entity pool | ~___bytes | [X] entities × ___bytes |
| World state | ~___bytes | Active level data |
| Input buffer | ~___bytes | [X] frames × 4 players |
| RNG state | ~___bytes | Seeded random state |
| **TOTAL STATE** | ~___KB | Target < 100KB |

---

# Part 9: Technical Design

## 9.1 Architecture Overview

### System Diagram
```
[Diagram of major game systems and their relationships]
```

### Core Systems
1. **[System 1]:** [Purpose and approach]
2. **[System 2]:** [Purpose and approach]
3. **[System 3]:** [Purpose and approach]

---

## 9.2 Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Frame rate | [X] fps | [Tick rate] |
| Max entities | [X] | Active in scene |
| Draw calls | [X] | Per frame |
| State snapshot | <___ms | For rollback |
| 8-frame rollback | <___ms | Total |

---

## 9.3 Technical Challenges

### Challenge 1: [Name]
**Problem:** [Description]
**Solution:** [Approach]
**zx-dev Reference:** [Relevant system]

### Challenge 2: [Name]
[Same structure]

---

## 9.4 Plugin Integration Points

### zx-dev
| Feature | zx-dev System | Notes |
|---------|---------------|-------|
| [Feature] | [System] | [Notes] |
| [Feature] | [System] | [Notes] |

### zx-procgen
| Asset | Procgen Technique | Parameters |
|-------|-------------------|------------|
| [Asset] | [Technique] | [Params] |
| [Asset] | [Technique] | [Params] |

---

# Part 10: Development Plan

## 10.1 Milestones

### Milestone 1: Prototype
**Goal:** [What defines success]
**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

### Milestone 2: Vertical Slice
**Goal:** [What defines success]
**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

### Milestone 3: Alpha
**Goal:** [What defines success]
**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

### Milestone 4: Beta
**Goal:** [What defines success]
**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

### Milestone 5: Release
**Goal:** [What defines success]
**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

---

## 10.2 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Strategy] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Strategy] |
| [Risk 3] | [H/M/L] | [H/M/L] | [Strategy] |

---

## 10.3 Testing Plan

### Quality Targets
| Area | Target |
|------|--------|
| Frame rate stability | [X]% at target |
| Memory usage | <[X]% of limits |
| Crash rate | [X] per hour |
| Rollback correctness | 100% deterministic |

### Testing Phases
1. **Unit testing:** [Approach]
2. **Integration testing:** [Approach]
3. **Playtest sessions:** [Schedule]
4. **Online testing:** [P2P test plan]

---

# Appendices

## Appendix A: Glossary
| Term | Definition |
|------|------------|
| [Term] | [Definition] |

## Appendix B: References
- [Reference 1]
- [Reference 2]

## Appendix C: Revision History
| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | [Date] | Initial draft |
