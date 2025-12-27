# Core Loop Design Worksheet

Complete this worksheet to design and document your game's loop structure.

---

## Game Identity

**Game Title:** _________________

**Genre:** _________________

**Target Session Length:** _____ minutes

**Core Fantasy:** What does the player want to feel?
```
_________________
```

---

## Part 1: Micro Loop (Seconds)

The moment-to-moment actions.

### Primary Action

**What does the player do most often?**
```
Action: _________________
Input method: _________________
Duration: _____ seconds
```

### Action Feedback

**What happens immediately after action?**

| Feedback Type | Description |
|---------------|-------------|
| Visual | |
| Audio | |
| Haptic | (if applicable) |

### Action Reward

**What does the player gain from single action?**
- [ ] Progress toward goal
- [ ] Resources/items
- [ ] Information
- [ ] Position advantage
- [ ] Damage dealt
- [ ] Other: _________________

### Micro Loop Diagram

```
[Action: _______]
       ↓
[Feedback: _______]
       ↓
[Reward: _______]
       ↓
[Next action decision]
```

---

## Part 2: Core Loop (Minutes)

The main gameplay cycle.

### Core Cycle

**What is the repeatable unit of gameplay?**

```
Step 1: _________________
     ↓
Step 2: _________________
     ↓
Step 3: _________________
     ↓
Step 4: _________________
     ↓
[Return to Step 1 with reward]
```

**Duration:** _____ minutes

### Core Loop Components

**Challenge:**
What obstacle does player face?
```
_________________
```

**Skill Required:**
What skill does player develop?
```
_________________
```

**Decision Points:**
What meaningful choices exist?
```
1. _________________
2. _________________
3. _________________
```

**Reward:**
What does completing one cycle provide?
```
_________________
```

### Core Loop Satisfaction

Rate each aspect (1-5):

| Aspect | Rating | Notes |
|--------|--------|-------|
| Clarity (player knows what to do) | /5 | |
| Agency (player feels in control) | /5 | |
| Feedback (player sees results) | /5 | |
| Mastery (player improves over time) | /5 | |
| Variety (cycles feel different) | /5 | |

---

## Part 3: Meta Loop (Hours)

Session-level progression.

### Session Structure

**What happens across a full play session?**

```
Session start: _________________
     ↓
Early session: _________________
     ↓
Mid session: _________________
     ↓
Late session: _________________
     ↓
Session end: _________________
```

### Session Goals

**What can player accomplish in one session?**
- [ ] Complete a level/dungeon
- [ ] Defeat a boss
- [ ] Acquire meaningful upgrade
- [ ] Progress story
- [ ] Unlock new content
- [ ] Complete collection
- [ ] Other: _________________

### Session Rewards

**What motivates player to return?**

| Reward Type | How Provided |
|-------------|--------------|
| Power increase | |
| New content access | |
| Story revelation | |
| Collection progress | |
| Skill improvement | |

### Save/Progress System

**How is progress saved?**
- [ ] Auto-save (how often: _______)
- [ ] Checkpoint save
- [ ] Manual save
- [ ] Permadeath/run-based

**What persists between sessions?**
```
_________________
```

**What resets between sessions?**
```
_________________
```

---

## Part 4: Loop Integration

How loops connect.

### Loop Hierarchy

```
MICRO LOOP (_____ seconds)
    │
    │ Micro rewards accumulate to:
    ▼
CORE LOOP (_____ minutes)
    │
    │ Core rewards accumulate to:
    ▼
META LOOP (_____ hours)
    │
    │ Meta rewards provide:
    ▼
REASON TO PLAY AGAIN
```

### Reward Flow

| Level | Reward | Feeds Into |
|-------|--------|------------|
| Micro | | Core loop via: |
| Core | | Meta loop via: |
| Meta | | Return via: |

### Pacing Integration

**Tension curve through loops:**

```
Tension
High   │           M
       │     c   c  \c
       │   c/ \c/ \  \
       │  /          \
Low    │ m  m  m  m  m \
       └────────────────→ Time

m = micro loops  c = core loops  M = meta climax
```

---

## Part 5: Progression System

### Progression Type

**Primary progression:** (choose one)
- [ ] Vertical (more power)
- [ ] Horizontal (more options)
- [ ] Skill-based (player improves)
- [ ] Content-based (new areas/story)

**Secondary progression:** (choose one)
- [ ] Vertical (more power)
- [ ] Horizontal (more options)
- [ ] Skill-based (player improves)
- [ ] Content-based (new areas/story)

### Progression Curve

**Describe your progression curve:**
```
_________________
```

**Power level at key points:**

| Point | Power Level | Time to Reach |
|-------|-------------|---------------|
| Tutorial complete | | |
| 25% through game | | |
| 50% through game | | |
| 75% through game | | |
| Game complete | | |

### Progression Visibility

**How does player see their progress?**
- [ ] Level number
- [ ] Stats/attributes
- [ ] Visual character changes
- [ ] Unlocked abilities
- [ ] Map/area completion
- [ ] Story progress
- [ ] Achievement/collection
- [ ] Other: _________________

---

## Part 6: Economy

### Resources

List all game resources:

| Resource | Source | Sink | Scarcity Level |
|----------|--------|------|----------------|
| | | | Low/Med/High |
| | | | Low/Med/High |
| | | | Low/Med/High |
| | | | Low/Med/High |

### Economy Flow

```
[Sources]              [Sinks]
____________          ____________
____________   ───→   ____________
____________          ____________
      ↓                    ↓
    Player              Economy
   inventory             drain
```

### Balance Checkpoints

| Checkpoint | Expected Resources | Actual |
|------------|-------------------|--------|
| Early game | | |
| Mid game | | |
| Late game | | |

---

## Part 7: Validation

### Loop Quality Checklist

**Micro loop:**
- [ ] Action is clear
- [ ] Feedback is immediate
- [ ] Repetition doesn't bore quickly

**Core loop:**
- [ ] Complete cycle in target time
- [ ] Meaningful decisions exist
- [ ] Skill is rewarded
- [ ] Variety prevents monotony

**Meta loop:**
- [ ] Session goals are achievable
- [ ] Progress feels meaningful
- [ ] Reason to return exists

### Risk Assessment

**Potential loop problems:**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Grind feels required | Low/Med/High | |
| Loop becomes boring | Low/Med/High | |
| Progression too slow | Low/Med/High | |
| Progression too fast | Low/Med/High | |
| Economy breaks | Low/Med/High | |

---

## Summary

### One-Page Loop Summary

```
═══════════════════════════════════════════
GAME: _______________

CORE FANTASY: _______________

LOOPS:
• Micro (___s): [action] → [feedback] → [reward]
• Core (___m): [challenge] → [skill] → [progress]
• Meta (___h): [session] → [achievement] → [return]

PROGRESSION: _______________ curve
             _______________ type

ECONOMY: _______________
         Sources: _______________
         Sinks: _______________

SESSION: _____ minutes target
         Save system: _______________
═══════════════════════════════════════════
```

---

## Next Steps

After completing this worksheet:
1. Prototype the micro loop first
2. Test if action feels good in isolation
3. Add core loop structure
4. Test if cycles are satisfying
5. Add meta progression
6. Test if sessions feel complete
