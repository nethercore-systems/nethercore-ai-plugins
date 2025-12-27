---
name: Narrative Design
description: This skill should be used when the user asks about "story structure", "narrative", "plot", "quest design", "dialogue writing", "branching narrative", "story arc", "exposition", "cutscenes", "narrative pacing", "quest types", "player choices", "story beats", "writing for games", or needs to design narrative elements for their game.
version: 1.0.0
---

# Narrative Design for Games

Frameworks for integrating story into gameplay. Focus on narrative that enhances player experience rather than interrupting it.

## Core Principle: Player as Protagonist

In games, the player IS the main character. Narrative design must:
- Support player agency
- Make player actions meaningful
- Avoid taking control away unnecessarily
- Integrate story with gameplay

The best game stories are ones the player feels they created through their choices.

---

## Story Structure for Games

### Adapting Traditional Structure

Games use modified story structures that account for player agency:

**Three-Act Structure (Adapted)**

| Act | Traditional | Game Adaptation |
|-----|-------------|-----------------|
| **Act 1** | Setup | Tutorial + World introduction + Goal established |
| **Act 2** | Confrontation | Core gameplay loop + Escalating challenges |
| **Act 3** | Resolution | Climax + Denouement + Player reflection |

**Act 2 is 60-70% of gameplay** — this is where most content lives.

### The Hero's Journey (Game Version)

| Stage | Game Implementation |
|-------|---------------------|
| **Ordinary World** | Starting area, tutorial |
| **Call to Adventure** | Inciting incident, first quest |
| **Refusal** | Optional or shown through NPC doubt |
| **Meeting the Mentor** | Tutorial NPC, ability unlock |
| **Crossing the Threshold** | Leave starting area, point of no return |
| **Tests, Allies, Enemies** | Core gameplay content |
| **Approach** | Preparing for major challenge |
| **Ordeal** | Major boss/challenge, potential failure |
| **Reward** | New ability, revelation, achievement |
| **The Road Back** | Consequences of ordeal, new stakes |
| **Resurrection** | Final challenge, everything at stake |
| **Return** | Ending, reflection on journey |

### Non-Linear Alternatives

**Hub and Spoke:**
- Central hub with branching content
- Player chooses order
- Stories within stories

**Open World:**
- Main quest + Side content
- Player creates their own narrative path
- Emergent storytelling from systems

**Episodic:**
- Self-contained segments
- Connected by theme/character
- Good for session-based play

---

## Story Beats

### Beat Types

| Beat Type | Function | Player State |
|-----------|----------|--------------|
| **Hook** | Capture interest | Curious, intrigued |
| **Setup** | Establish context | Informed, oriented |
| **Escalation** | Raise stakes | Tense, engaged |
| **Twist** | Subvert expectations | Surprised, recontextualizing |
| **Climax** | Peak tension | Thrilled, focused |
| **Resolution** | Release tension | Satisfied, reflective |

### Beat Pacing

Alternate tension levels:

```
Tension
High   |     *     *         *****
       |    / \   / \       /     \
       |   /   \ /   \     /       \
Low    |  *     *     *****         *
       +--------------------------------→ Time
        Hook  Escape  Explore  Climax  End
```

**Rule:** Never maintain maximum tension too long. Give players breathing room.

### Integrating Beats with Gameplay

| Story Beat | Gameplay Support |
|------------|------------------|
| Hook | Dramatic opening, player immediately engaged |
| Escalation | Increasing difficulty, new enemy types |
| Twist | Mechanical change, new ability, environment shift |
| Climax | Boss fight, time pressure, full skill test |
| Resolution | Safe zone, reward collection, reflection time |

---

## Quest Design

### Quest Anatomy

Every quest needs:

1. **Clear objective:** What to do
2. **Motivation:** Why to do it
3. **Challenge:** What makes it interesting
4. **Reward:** What you get
5. **Closure:** Sense of completion

### Quest Types

| Type | Structure | Best For |
|------|-----------|----------|
| **Kill/Defeat** | Find target, overcome it | Combat focus, clear objective |
| **Fetch** | Get item, bring it back | Exploration, resource gathering |
| **Escort** | Protect entity during travel | Tension, relationship building |
| **Investigate** | Find clues, solve mystery | Exploration, narrative focus |
| **Defend** | Protect location/entity | Tension, time pressure |
| **Deliver** | Transport item/message | Exploration, NPC connection |
| **Survive** | Endure until condition met | Horror, tension |
| **Race** | Complete before time/rival | Urgency, skill test |

### Quest Design Template

```
QUEST NAME: _______________

Objective: [What player must do]
Given by: [Who/what initiates]
Location: [Where it takes place]
Challenge: [What makes it interesting]
Reward: [What player receives]
Stakes: [What happens if player fails/ignores]

Optional:
- Multiple solutions: [Yes/No, describe]
- Branching outcomes: [Yes/No, describe]
- Connection to other quests: [describe]
```

### Quest Chains

Link quests for narrative momentum:

**Linear chain:**
Quest A → Quest B → Quest C

**Branching chain:**
```
Quest A → Quest B1 → Quest C1 (ending 1)
       ↘ Quest B2 → Quest C2 (ending 2)
```

**Convergent chain:**
```
Quest A → Quest B1 ↘
                     Quest D (same destination)
Quest A → Quest B2 ↗
```

---

## Dialogue Writing

### Dialogue Purposes

Every line should serve at least one purpose:

| Purpose | Example |
|---------|---------|
| **Information** | "The key is in the tower" |
| **Character** | "I never trusted wizards" |
| **Emotion** | "Please... find my daughter" |
| **Choice setup** | "Will you help the village or seek the treasure?" |
| **World building** | "Before the war, this was a garden" |
| **Humor/relief** | "Another adventurer? At least you're not on fire" |

### Dialogue Guidelines

**Keep it short:**
- Players read faster than NPCs speak
- Long text blocks get skipped
- Break into multiple exchanges if needed

**Voice each character:**
- Distinct vocabulary
- Consistent speech patterns
- Personality in word choice

**Show, don't tell:**
- NPCs react to what player has done
- Environment reflects narrative
- Actions speak louder than exposition

**Player dialogue:**
- Keep options distinct and clear
- Show consequences when possible
- Avoid "false choices" that lead to same outcome

### Dialogue Structure

**Branching dialogue:**
```
[NPC greeting based on relationship]
  ├─ [Topic A] → [Response] → [Follow-up options]
  ├─ [Topic B] → [Response] → [End or branch]
  └─ [Exit]
```

**Tracked dialogue:**
- Remember previous conversations
- Unlock new options based on events
- Close topics that are resolved

---

## Branching Narratives

### Branching Complexity Levels

| Level | Description | Development Cost |
|-------|-------------|------------------|
| **Flavor** | Different dialogue, same outcome | Low |
| **Tactical** | Different paths to same goal | Medium |
| **Strategic** | Different goals, different endings | High |
| **Systemic** | Emergent from interacting systems | Very High |

### Branch Management

**The funnel approach:**
Many branches early → Converge at key points → Branch again

```
Start ──┬── Path A ──┐
        ├── Path B ──┼── Convergence ──┬── Ending X
        └── Path C ──┘                 └── Ending Y
```

**State tracking:**
Track player choices to:
- Adjust NPC reactions
- Unlock/lock content
- Determine endings
- Calculate "affinity" scores

### Choice Design

**Good choices:**
- Clear what each option means
- Distinct outcomes
- Connect to player values
- Have consequences (or appear to)

**Avoid:**
- "Right answer" obvious
- Choices that don't matter
- Information needed isn't available
- Outcomes that punish curiosity

---

## Exposition Techniques

### Exposition Methods (Best to Worst)

| Method | Immersion | Player Attention |
|--------|-----------|------------------|
| Environmental storytelling | High | Active discovery |
| Gameplay integration | High | Learning by doing |
| NPC dialogue | Medium | Requested by player |
| Found documents | Medium | Optional reading |
| Cutscenes | Low-Medium | Passive watching |
| Text dumps | Low | Often skipped |

### Environmental Storytelling

Tell story through the world:

**Object placement:**
- A sword stuck in the ground marks a grave
- Empty bottles suggest desperation
- Barricaded doors show fear

**Architecture:**
- Grandeur suggests former glory
- Repairs suggest resilience
- Destruction suggests violence

**Environmental sequence:**
- Blood trail leads somewhere
- Footprints tell a path
- Damage pattern reveals event

### The "Ask, Don't Tell" Method

Let players request information rather than forcing it:

**Instead of:** Automatic lore dump when entering area
**Try:** NPC who answers questions when asked

**Instead of:** Long cutscene explaining backstory
**Try:** Environmental hints + optional deep lore for curious players

---

## Pacing

### Narrative Pacing vs Gameplay Pacing

| Narrative | Gameplay | Player State |
|-----------|----------|--------------|
| Tension rising | Challenge increasing | Focused, stressed |
| Twist/revelation | New mechanic/area | Excited, curious |
| Resolution | Victory/reward | Satisfied, relaxed |
| Setup | Safe zone/hub | Exploring, choosing |

**Keep in sync:** Story beats should align with gameplay beats.

### Pacing Tools

**Speed up:**
- Time pressure
- Chase sequences
- Rapid revelations
- Short dialogue

**Slow down:**
- Safe zones
- Optional content
- Exploration time
- Longer dialogue options

**Punctuate:**
- Boss fights
- Cutscenes (sparingly)
- Major revelations
- Permanent changes

---

## Endings

### Ending Types

| Type | Player Experience | When to Use |
|------|-------------------|-------------|
| **Victory** | Triumph, satisfaction | Most games |
| **Bittersweet** | Thoughtful, complex | Story-focused games |
| **Tragedy** | Emotional impact | If earned throughout |
| **Open** | Imagination, continuation | Sequels, player-driven |
| **Multiple** | Replayability, ownership | Choice-heavy games |

### Ending Design

**Checklist for satisfying endings:**
- [ ] Resolves main conflict
- [ ] Addresses major character arcs
- [ ] Rewards player investment
- [ ] Feels earned by player actions
- [ ] Doesn't invalidate player choices
- [ ] Provides closure (or intentional open-ness)

---

## Additional Resources

### Reference Files

- **`references/story-structures.md`** — Detailed story structure templates
- **`references/quest-patterns.md`** — Quest design patterns and examples
- **`references/dialogue-guide.md`** — Dialogue writing techniques

### Related Skills

- **`character-design`** — Characters in your narrative
- **`world-building`** — Setting for your story
- **`player-psychology`** — Player engagement with narrative
