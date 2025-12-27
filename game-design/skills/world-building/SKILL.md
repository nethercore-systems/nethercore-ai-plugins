---
name: World Building
description: This skill should be used when the user asks about "world design", "game world", "lore", "world map", "factions", "cultures", "environmental storytelling", "world rules", "world consistency", "geography", "history", "time systems", "day night cycle", "world scope", or needs to design the setting and context for their game.
version: 1.0.0
---

# World Building for Games

Frameworks for creating coherent, memorable game worlds. Focus on what players experience and interact with, not encyclopedic lore documents.

## Core Principle: Playable Worlds

Game worlds exist to be played in, not read about. Every world element should either:
- Create gameplay opportunities
- Inform player decisions
- Establish mood and atmosphere
- Reward exploration or curiosity

Avoid lore that exists only in text dumps. Show the world through gameplay.

---

## World Scope Decision

Before building, determine scope based on game length and team size:

| Scope | Description | Suitable For |
|-------|-------------|--------------|
| **Contained** | Single location with depth (a mansion, a ship, a dungeon) | Short games, game jams, solo devs |
| **Regional** | Multiple connected areas with distinct identities | Medium games, small teams |
| **Expansive** | Multiple regions, complex relationships | Longer games, larger scope |

**Recommendation for indie/solo devs:** Start contained. A deeply realized small world beats a shallow large one.

---

## World Design Worksheet

### 1. The Elevator Pitch
One sentence describing your world's unique identity:
```
"A world where [unique element] means [consequence for inhabitants]"
```

### 2. The Core Tension
What conflict defines this world?
- Resource scarcity
- Ideological divide
- Environmental threat
- Power imbalance
- Hidden truth

### 3. The Player's Role
How does the player relate to this world?
- Native inhabitant
- Outsider arriving
- Returning after absence
- Awakening without memory
- Observer/chronicler

### 4. Scale and Boundaries
- What contains the world? (walls, sea, void, political borders)
- How long to traverse the playable space?
- What exists beyond boundaries? (nothing, threat, mystery)

---

## Geography and Space

### Functional Geography

Design geography that creates gameplay:

| Geographic Feature | Gameplay Function |
|-------------------|-------------------|
| Elevation changes | Verticality, vantage points, shortcuts |
| Water bodies | Barriers, navigation puzzles, resources |
| Dense areas (forests, cities) | Cover, exploration, getting lost |
| Open areas | Combat arenas, exposure, speed |
| Chokepoints | Encounters, gates, narrative beats |

### Landmark Design

Players navigate by landmarks. Every area needs:
- **Beacon landmark**: Visible from distance, aids orientation
- **Local landmarks**: Distinguish areas, aid memory
- **Hidden landmarks**: Reward exploration

### Connectivity

Map how areas connect:
```
[Starting Area]
      |
[Hub/Crossroads] --- [Optional Area]
      |
[Gate/Challenge]
      |
[New Region] --- [Secret Area]
```

---

## Cultures and Factions

### Faction Design Template

For each faction:

**Identity**
- Name and visual identity
- Core belief or motivation
- What they want from the player

**Relationships**
- Allied with: [faction]
- Opposed to: [faction]
- Neutral toward: [faction]

**Player Interaction**
- How player encounters them
- What player can gain from them
- What threatens the relationship

### Faction Dynamics

Create gameplay through faction relationships:
- **Allied factions**: Player actions benefit both
- **Opposed factions**: Helping one harms another
- **Neutral factions**: Can be swayed by player actions

**Keep it simple:** 2-4 factions maximum for most games.

---

## History and Lore

### The Iceberg Principle

- **Surface (10%)**: What players directly experience
- **Visible depth (20%)**: What players can discover through exploration
- **Hidden depth (70%)**: What you know but players may never see

Players should sense depth without needing to access it all.

### Lore Delivery Methods

**Preferred (show):**
- Environmental details
- NPC behavior and dialogue
- Item descriptions
- Architecture and design

**Use sparingly (tell):**
- Readable documents
- Exposition dialogue
- Cutscenes

### Historical Layers

Design history in layers visible in the world:
1. **Ancient**: Ruins, artifacts, forgotten technology
2. **Past**: Recent history, living memory, scars
3. **Present**: Current state, ongoing conflicts
4. **Implied future**: Where things are heading

---

## Time Systems

### Static vs Dynamic Time

**Static time**: World state doesn't change without player action
- Simpler to design
- Player has full control
- May feel artificial

**Dynamic time**: World changes independent of player
- More immersive
- Creates urgency
- Harder to balance

### Day/Night Cycles

If implementing day/night:

| Time | Gameplay Implications |
|------|----------------------|
| Dawn | Transition, new opportunities |
| Day | Normal activities, visibility |
| Dusk | Transition, preparation |
| Night | Different enemies, stealth opportunities, danger |

**Tip:** Only add day/night if it creates meaningful gameplay differences.

### Seasons and Eras

For longer games, consider:
- Seasonal changes affecting traversal and resources
- Story acts changing world state
- Player actions permanently altering regions

---

## Environmental Storytelling

### Object Placement

Tell stories through carefully placed objects:
- **Contrast**: A child's toy in a battlefield
- **Sequence**: Events told through object placement
- **Absence**: What's missing tells a story

### Architecture as Narrative

Buildings and structures communicate:
- Who built them (culture, resources)
- What happened since (decay, repair, repurpose)
- Current use (matches or contradicts original purpose)

### Ambient Details

Layer environmental storytelling:
1. **Background**: Sets overall mood
2. **Midground**: Tells location-specific stories
3. **Foreground**: Interactive elements with lore

---

## Consistency Rules

### The "Yes, But" Test

For every world rule, answer: "Can the player break this?"
- If yes: Either the rule is soft (bendable) or breaking it has consequences
- If no: The rule must be consistently enforced

### Internal Logic Checklist

- [ ] Economy makes sense (where do resources come from?)
- [ ] Power structures are clear (who's in charge and why?)
- [ ] Technology is consistent (no anachronisms without explanation)
- [ ] Magic/special systems have clear limits
- [ ] Geography is traversable in stated ways

### Player Expectations

Track what you've communicated to players:
- If water is dangerous, all water should be dangerous
- If NPCs can die, players expect consequences
- If doors can be opened, locked doors need explanation

---

## World Building Pitfalls

### Avoid These

**Kitchen sink worlds**: Too many elements without cohesion
**Lore dumps**: Exposition that stops gameplay
**Arbitrary restrictions**: Rules that exist only to limit player
**Ungrounded fantasy**: Magic without cost or limit
**Empty scale**: Large worlds with nothing in them

### Signs of Good World Design

- Players remember location names
- Players can navigate without UI markers
- World details inform gameplay decisions
- Exploration feels rewarding
- Returning to areas feels like coming home

---

## Additional Resources

### Reference Files

- **`references/world-scope-worksheet.md`** — Detailed world scope planning template
- **`references/consistency-checklist.md`** — Full internal consistency checklist

### Related Skills

- **`level-design`** — Spatial design within your world
- **`narrative-design`** — Stories told within your world
- **`character-design`** — Inhabitants of your world
