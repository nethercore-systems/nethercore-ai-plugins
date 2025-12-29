# Example: Fighting Game GDD (Standard)

**Game Title:** Nether Clash
**Author:** Nethercore Studios
**Version:** 0.1.0
**Date:** 2025-01-15
**Target Platform:** Nethercore ZX

---

## 1. Overview

### High Concept
A 4-player arcade fighting game with stylized 3D characters and rollback netcode. Accessible 2-button combat with depth from spacing, timing, and character-specific specials.

### Target Audience
Core fighting game enthusiasts and casual players looking for local multiplayer fun. Ages 10+, skill level from beginner to competitive.

### Reference Games
- Smash Bros. — 4-player chaos, platform elements
- Street Fighter II — Spacing, special moves, character variety
- Power Stone — 3D arena movement, items

### Unique Selling Points
1. Seamless 4-player online with rollback netcode
2. Pick-up-and-play controls with competitive depth
3. 5th-gen aesthetic with modern polish

---

## 2. ZX Platform Configuration

### Render Mode

| Setting | Value |
|---------|-------|
| Mode | 3: Blinn-Phong |
| Rationale | Era-authentic 5th-gen arcade aesthetic, artistic specular control for flashy character shaders, rim lighting for character pop |

### Tick Rate

| Setting | Value |
|---------|-------|
| Rate | 60 fps |
| Rationale | Standard for fighting games, 16.67ms frame timing for precise hitbox/hurtbox interactions |

### Multiplayer Configuration

| Setting | Value |
|---------|-------|
| Max Players | 4 |
| Modes | Local + Online |
| Determinism | All gameplay deterministic, fixed-point math for physics |

---

## 3. Core Mechanics

### Primary Mechanic: 2-Button Combat
- **Light Attack (A):** Fast, short range, combos into itself
- **Heavy Attack (B):** Slow, long range, knockback

### Secondary Mechanics
1. **Directional Specials:** Direction + Heavy for character-specific moves
2. **Shield (L1):** Block attacks, depletes shield meter
3. **Dodge (R1):** Brief invincibility, costs meter

### Game Loop

```
┌─────────────┐
│   NEUTRAL   │ ← Players jockey for position
└──────┬──────┘
       ↓
┌─────────────┐
│   ATTACK    │ ← Land a hit, start combo
└──────┬──────┘
       ↓
┌─────────────┐
│   COMBO     │ ← Continue pressure
└──────┬──────┘
       ↓
┌─────────────┐
│  KNOCKBACK  │ ← Reset to neutral
└──────┴──────→ Loop until K.O.
```

### Progression System
Stock-based elimination. 3 stocks per player, last player standing wins.

---

## 4. Controls

### Full Control Scheme

| Input | Action | Context |
|-------|--------|---------|
| Left Stick | Movement | Gameplay |
| D-Pad | Movement (alternate) | Gameplay |
| A | Light Attack | Gameplay |
| B | Heavy Attack / Special | Gameplay |
| X | Taunt | Gameplay |
| Y | Item Pickup | Gameplay |
| L1 | Shield | Gameplay |
| R1 | Dodge | Gameplay |
| Start | Pause | All |

### Control Feel Notes
- 4 frame input buffer for combo leniency
- Analog stick with 0.15 dead zone
- D-pad preferred for precise movement

---

## 5. Level/World Structure

### Overview
4 fighting stages, each with unique hazards and platforms

### Stage List

| Stage | Theme | Key Features | Est. Size |
|-------|-------|--------------|-----------|
| Dojo | Traditional | Flat stage, no hazards (beginner) | ~400KB |
| Factory | Industrial | Moving platforms, conveyor floors | ~600KB |
| Volcano | Lava | Destructible platforms, lava hazard | ~700KB |
| Sky Arena | Clouds | Floating platforms, gusts of wind | ~600KB |

### Difficulty Progression
Stages unlock as player wins matches. Dojo always available as training stage.

---

## 6. Memory Budget

### ROM Allocation (16 MB Total)

| Category | Budget | Breakdown |
|----------|--------|-----------|
| WASM Code | 200KB | Game logic, state machine, netcode |
| Meshes | 3.2MB | 8 chars × 200KB + 4 stages × 400KB |
| Textures | 5.5MB | Characters (2.5MB) + Stages (2.5MB) + Effects (500KB) |
| Audio | 2.3MB | SFX (800KB) + Music (1.5MB) |
| Animations | 800KB | 8 chars × 100KB |
| Fonts/UI | 200KB | Font + UI atlas |
| **Total** | 12.2MB | Remaining: 3.8MB |

### RAM State (4 MB, target < 100KB for state)

| Category | Size | Notes |
|----------|------|-------|
| Player state | ~500 bytes × 4 | Position, velocity, hitbox, combo state |
| Stage state | ~1KB | Platform positions, hazard timers |
| Input buffer | ~2KB | 60 frames × 4 players |
| RNG state | 64 bytes | Seeded for items |
| **State Total** | ~5KB | Excellent for rollback |

---

## 7. Audio Design

### Music

| Track | Purpose | Duration | Est. Size |
|-------|---------|----------|-----------|
| Title Theme | Title screen | 45s loop | 200KB |
| Character Select | Menu | 30s loop | 130KB |
| Stage: Dojo | Gameplay | 60s loop | 260KB |
| Stage: Factory | Gameplay | 60s loop | 260KB |
| Stage: Volcano | Gameplay | 60s loop | 260KB |
| Stage: Sky Arena | Gameplay | 60s loop | 260KB |
| Victory Fanfare | Win screen | 10s | 45KB |
| Results | Post-match | 30s loop | 130KB |

### Sound Effects

| Category | Count | Examples |
|----------|-------|----------|
| Attacks | 24 | Light hit, heavy hit, special × 8 chars |
| Impact | 8 | Clash, block, shield break, K.O. |
| Movement | 8 | Jump, land, dash, dodge |
| UI | 8 | Select, confirm, ready, countdown |
| Stage | 16 | Lava bubble, platform creak, wind gust |

### Audio Channel Budget (16 channels)

| Category | Reserved Channels |
|----------|-------------------|
| Music | 1 (dedicated) |
| Player 1-4 SFX | 4 |
| Impact/clash | 4 |
| Stage ambient | 4 |
| UI | 3 |
| **Total** | 16 |

---

## 8. Asset Specifications

### Characters

| Character | Mesh Size | Textures | Animations | Total |
|-----------|-----------|----------|------------|-------|
| Karate Ken | 180KB | 512×512 diff + 256×256 SSE | 18 anims | 280KB |
| Iron Maya | 200KB | 512×512 diff + 256×256 SSE | 20 anims | 320KB |
| Blaze | 170KB | 512×512 diff + 256×256 SSE | 16 anims | 260KB |
| Frost | 170KB | 512×512 diff + 256×256 SSE | 16 anims | 260KB |
| Volt | 190KB | 512×512 diff + 256×256 SSE | 18 anims | 300KB |
| Shadow | 160KB | 512×512 diff + 256×256 SSE | 18 anims | 260KB |
| Titan | 220KB | 512×512 diff + 256×256 SSE | 14 anims | 300KB |
| Whisper | 150KB | 512×512 diff + 256×256 SSE | 20 anims | 260KB |

### Procgen Opportunities

- [ ] Stage floor textures — [PROCGEN: tileable noise patterns]
- [ ] Effect particles — [PROCGEN: simple shapes with glow]
- [ ] Impact sounds — [PROCGEN: synthesized hits]

---

## 9. Technical Considerations

### Performance Targets
- Target frame rate: 60 fps locked
- Max entities: 4 players + 8 projectiles + 4 items = 16
- Draw calls: ~30 per frame

### Known Challenges
1. **Rollback precision:** Use fixed-point math for all physics
2. **Animation sync:** Frame-based animations, not time-based
3. **Input delay:** 3-frame input delay for online consistency

### zx-dev Integration Points
- [ ] Character state machine → zx-dev: animation system
- [ ] Hitbox/hurtbox detection → zx-dev: collision primitives
- [ ] Rollback save/load → zx-dev: state serialization

---

## 10. Development Roadmap

### Phase 1: Prototype
- [ ] 2 characters with basic attacks
- [ ] 1 stage (Dojo)
- [ ] Local 2-player
- [ ] Basic hit detection

### Phase 2: Pre-Production
- [ ] All 8 characters blockout
- [ ] All 4 stages blockout
- [ ] 4-player local
- [ ] Special moves

### Phase 3: Production
- [ ] Final character art/animations
- [ ] Final stage art
- [ ] Online multiplayer
- [ ] All SFX and music

### Phase 4: Release
- [ ] Balance pass
- [ ] Online stress test
- [ ] ROM packaging
- [ ] Distribution
