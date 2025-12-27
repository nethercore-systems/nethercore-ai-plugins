# Story Structure Templates

Ready-to-use narrative structures adapted for games.

---

## Three-Act Structure

The foundation of Western storytelling, adapted for interactive media.

### Act 1: Setup (15-25% of game)

**Purpose:** Establish world, character, and stakes

| Beat | Function | Game Implementation |
|------|----------|---------------------|
| Opening | Hook the player | Dramatic first moment, immediate action |
| Normal world | Show starting state | Tutorial area, establish routine |
| Inciting incident | Disrupt the normal | Event that forces player into adventure |
| Debate | Show stakes | Why player should care, what's at risk |
| First threshold | Commit to adventure | Leave starting area, point of no return |

**Checklist for Act 1:**
- [ ] Player understands core mechanics
- [ ] Player knows their goal
- [ ] Player cares about the outcome
- [ ] Stakes are established
- [ ] The world feels real

### Act 2: Confrontation (50-60% of game)

**Purpose:** Challenge the player, develop story and characters

| Beat | Function | Game Implementation |
|------|----------|---------------------|
| Fun and games | Core gameplay | Main content, exploring mechanics |
| Gathering allies | Build support | Companion recruitment, faction alliances |
| Midpoint | Raise stakes | Major revelation, success or failure |
| Bad guys close in | Escalate threat | Enemy becomes more dangerous |
| All is lost | Low point | Major setback, apparent defeat |
| Dark night | Internal crisis | Character moment, player reflection |

**Act 2 Structure Options:**

**Linear:**
Beat A → Beat B → Beat C → Midpoint → Beat D → Beat E → Low point

**Hub-based:**
```
Midpoint
   |
Hub ──┬── Quest line A
      ├── Quest line B
      └── Quest line C
           |
        Low point
```

**Open:**
Player-driven exploration with story triggers at key moments

### Act 3: Resolution (20-30% of game)

**Purpose:** Conclude the story, satisfy the player

| Beat | Function | Game Implementation |
|------|----------|---------------------|
| Gathering strength | Prepare for finale | Upgrade, final side content, emotional moments |
| Break into three | Commit to ending | Final mission begins |
| Finale | Climactic challenge | Final boss, last puzzle, ultimate test |
| Final image | Closure | Ending cutscene, epilogue, credits |

**Checklist for Act 3:**
- [ ] Player feels prepared for finale
- [ ] All major threads resolved
- [ ] Challenge feels appropriate
- [ ] Victory feels earned
- [ ] Ending matches tone

---

## Five-Act Structure

For longer games with more complex narratives.

| Act | Name | Function | Length |
|-----|------|----------|--------|
| 1 | Exposition | Setup and introduction | 10-15% |
| 2 | Rising Action | Complications and challenges | 25-30% |
| 3 | Climax | Turning point, major event | 15-20% |
| 4 | Falling Action | Consequences and final preparation | 25-30% |
| 5 | Resolution | Finale and conclusion | 15-20% |

### Key Differences from Three-Act

- Midpoint becomes its own act (Act 3)
- More time for consequences after midpoint
- Better for games with major mid-game revelations
- Supports longer games with distinct phases

---

## Episodic Structure

For games with distinct chapters or levels.

### Episode Template

Each episode is a complete mini-story:

```
Cold open (hook)
    ↓
Setup (context for this episode)
    ↓
Complication (problem arises)
    ↓
Escalation (problem gets worse)
    ↓
Climax (peak of episode)
    ↓
Resolution (episode concludes)
    ↓
Cliffhanger/Hook (sets up next episode)
```

### Episode Connections

**Standalone:** Episodes can be played in any order
- Shared characters but independent stories
- Mechanics and setting are the connection

**Serialized:** Episodes must be played in order
- Continuing storyline
- Building stakes and character development

**Hybrid:** Core episodes in order, side episodes standalone
- Main quest line serialized
- Side content episodic

---

## Non-Linear Structures

For open-world or player-driven narratives.

### Hub Structure

```
        ┌─── Story A ───┐
        │               │
HUB ────┼─── Story B ───┼──── FINALE
        │               │
        └─── Story C ───┘
```

**How it works:**
- Central location (hub) branches to content
- Player chooses order
- All paths converge for finale

**Design considerations:**
- Each branch should be satisfying alone
- Convergence must acknowledge choices
- Hub should evolve as player progresses

### Parallel Storylines

Multiple interconnected narratives:

```
Story A: ─────────────────────────→
              ↓          ↑
Story B: ─────┴──────────┴────────→
              ↑          ↓
Story C: ─────┴──────────┴────────→
```

**How it works:**
- Multiple storylines progress simultaneously
- Intersections create connections
- Player choices affect multiple lines

### Emergent Narrative

Story emerges from gameplay systems:

**Components:**
- Systemic world (things happen without player)
- Player agency (choices affect world)
- Memory (world remembers consequences)
- Randomness (variation between playthroughs)

**Design considerations:**
- Systems must create interesting situations
- Player needs tools to interact with situations
- Stories must be recognizable as stories (beginning, middle, end)

---

## Tragedy Structure

For games with darker or more complex themes.

### Classic Tragedy Pattern

| Phase | Traditional | Game Version |
|-------|-------------|--------------|
| Prosperity | Hero starts strong | Player has power/advantage |
| Hubris | Pride or flaw | Player makes fateful choice |
| Nemesis | Consequences begin | Consequences affect gameplay |
| Recognition | Hero realizes truth | Player sees full impact |
| Catastrophe | Inevitable end | Tragic conclusion |

### Tragedy Design Notes

**Requirements:**
- Player must make the fateful choice (not forced)
- Consequences must feel fair (not arbitrary)
- Tragedy must be emotionally earned
- Some catharsis in the ending

**Avoid:**
- Making player feel tricked
- Punishing good play with bad story
- Nihilistic endings without meaning

---

## Mystery Structure

For investigation-focused narratives.

### Mystery Template

| Phase | Function | Player Activity |
|-------|----------|-----------------|
| Discovery | Find the mystery | Encounter unexplained situation |
| Investigation | Gather clues | Explore, interrogate, analyze |
| Complications | Deepen mystery | Red herrings, new questions |
| Revelation | Pieces come together | Connect clues, have insights |
| Confrontation | Face the truth | Confront perpetrator/reality |
| Resolution | Closure | Explanation, consequences |

### Mystery Design Principles

**Clue distribution:**
- Essential clues unmissable
- Optional clues provide shortcuts
- False clues should be identifiable

**Fair play:**
- Player has information to solve mystery
- Solution makes sense in retrospect
- Twist doesn't invalidate previous logic

**Pacing:**
- Revelation shouldn't come too early or late
- Allow player moments of insight
- Build to satisfying "aha" moment

---

## Choosing Your Structure

| Game Type | Recommended Structure |
|-----------|----------------------|
| Action/arcade | Minimal structure, episodic levels |
| RPG | Three or five-act, hub-based |
| Adventure | Mystery or three-act |
| Open world | Non-linear with main quest spine |
| Roguelike | Emergent + episodic runs |
| Horror | Mystery with tragedy elements |
| Fighting | Minimal frame + character episodes |

---

## Structure Adaptation Tips

### Scaling for Game Length

**Short games (1-3 hours):**
- Compress three-act into essentials
- One clear storyline
- Minimal sub-plots

**Medium games (5-15 hours):**
- Full three-act or episodic
- Room for sub-plots
- Character development possible

**Long games (20+ hours):**
- Five-act or hub structure
- Multiple storylines
- Deep character arcs

### Integrating with Gameplay

**Story should follow gameplay rhythm:**
- Story beats after gameplay achievements
- Calm story moments after intense gameplay
- Climax of story with climax of challenge

**Never:**
- Long story section preventing play
- Gameplay disconnected from story stakes
- Story ignoring player accomplishments
