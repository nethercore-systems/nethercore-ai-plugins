# System Verification Checklists

## Inventory System

- [ ] Item struct/enum defined
- [ ] Inventory struct with slots
- [ ] Pickup logic works
- [ ] UI displays inventory
- [ ] Item usage works
- [ ] Persistence (if applicable)

## Combat System

- [ ] Attack logic works
- [ ] Attack has hitbox/detection
- [ ] Damage applies to enemies
- [ ] Health decreases correctly
- [ ] Death/defeat works
- [ ] Death animation/effect plays
- [ ] Entity removed/respawned
- [ ] Feedback present (visual/audio)

## Save System

- [ ] Serialization works
- [ ] All necessary fields included
- [ ] save_data() persists
- [ ] load_data() retrieves correctly
- [ ] State restored properly
- [ ] UI present for save/load

## Core Gameplay Loop

- [ ] Player can provide input
- [ ] Game state updates in response
- [ ] Visual feedback rendered
- [ ] Win/lose condition works (or endless)

## Technical Requirements

- [ ] Build succeeds (nether build)
- [ ] Game runs (nether run)
- [ ] No crashes in first 60 seconds
- [ ] Sync test passes (if multiplayer)
