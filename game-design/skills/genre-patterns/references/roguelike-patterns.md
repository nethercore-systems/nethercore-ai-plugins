# Roguelike Design Patterns

---

## Core Roguelike Elements

| Element | Traditional | Roguelite Variant |
|---------|-------------|-------------------|
| Permadeath | Total reset | Meta-progression persists |
| Procedural generation | Always | Usually |
| Turn-based | Required | Optional |
| Progression | Per-run only | Unlocks between runs |

---

## Run Structure

```
[Start] → [Early game] → [Mid game] → [Late game] → [Boss/End]
   │           │              │            │
  Easy      Building       Testing      Mastery
  items      synergies      build        test
```

### Run Length Guidelines

| Length | Target Audience | Design Notes |
|--------|-----------------|--------------|
| 15-30 min | Casual, quick sessions | Fast pacing, fewer decisions |
| 30-60 min | Standard | Balanced progression |
| 60-120 min | Dedicated | Deep builds, high stakes |

---

## Meta-Progression (Roguelite)

### What Can Persist

| Type | Example | Danger Level |
|------|---------|--------------|
| Unlocks | New items/characters enter pool | Low |
| Knowledge | Player learns patterns | None |
| Power | Permanent stat boosts | High (can trivialize) |
| Story | Narrative progression | Low |

---

## Build Diversity Checklist

- [ ] Multiple viable "archetypes"
- [ ] Synergies between items
- [ ] No dominant strategy
- [ ] Bad runs are still winnable
- [ ] Good runs feel powerful

---

## Item Design

### Item Types

| Type | Effect | Balance |
|------|--------|---------|
| Stat boost | Raw numbers | Common, low impact |
| Ability | New action | Uncommon, medium impact |
| Synergy enabler | Multiplies other items | Rare, high impact |
| Build-definer | Changes playstyle | Very rare, run-defining |

### Drop Rate Balance
```
Common: 60-70%
Uncommon: 20-30%
Rare: 8-15%
Legendary: 2-5%
```

---

## Seed-Based Generation

Critical for:
- Rollback multiplayer (netcode requires determinism)
- Sharing runs
- Debugging
- Competitive play

Implementation: All randomness flows from single seed.
