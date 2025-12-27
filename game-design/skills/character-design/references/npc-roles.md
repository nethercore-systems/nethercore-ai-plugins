# NPC Roles and Design Patterns

Comprehensive guide to NPC functions and how to design them effectively.

---

## Core NPC Functions

Every NPC should serve at least one clear function. Combine functions to create efficiency.

### Service Providers

NPCs who give the player something tangible.

**Merchant**
- **Function:** Trades items/services for currency
- **Design keys:**
  - Inventory matches area/story point
  - Prices internally consistent
  - Location makes sense (why are they here?)
- **Memorable additions:**
  - Specialization (weapons only, rare items, stolen goods)
  - Personality that affects transactions
  - Stock that changes over time

**Crafter**
- **Function:** Transforms player resources into items
- **Design keys:**
  - Clear recipe/requirements display
  - Meaningful upgrade path
  - Time or resource cost
- **Memorable additions:**
  - Specialties and limitations
  - Quality variation
  - Personal stakes in what they create

**Healer**
- **Function:** Restores player resources (health, mana, status)
- **Design keys:**
  - Clear cost structure
  - Location accessibility
  - Emergency vs convenience
- **Memorable additions:**
  - Lore reason for healing ability
  - Conditions or restrictions
  - Commentary on player's condition

### Information Providers

NPCs who give the player knowledge.

**Quest Giver**
- **Function:** Provides objectives and direction
- **Design keys:**
  - Clear objective communication
  - Motivation for asking player
  - Reward structure
- **Memorable additions:**
  - Personal stake in quest outcome
  - Updates during quest
  - Reaction to completion

**Lore Keeper**
- **Function:** Provides world information
- **Design keys:**
  - Information is useful or enriching
  - Delivery is engaging (not exposition dumps)
  - Player can access when wanted
- **Memorable additions:**
  - Expertise has limits
  - Bias or incorrect beliefs
  - Information has cost

**Guide**
- **Function:** Helps player navigate
- **Design keys:**
  - Clear directions
  - Available when needed
  - Doesn't interrupt flow
- **Memorable additions:**
  - Local knowledge adds texture
  - Hidden information rewards exploration
  - Wrong occasionally (with tells)

### Tutorial Roles

NPCs who teach the player.

**Mentor**
- **Function:** Teaches mechanics and abilities
- **Design keys:**
  - Explains clearly without condescending
  - Demonstrates when possible
  - Available for review
- **Memorable additions:**
  - Personal history with skills taught
  - Limitations (can't do everything)
  - Arc of their own

**Training Dummy**
- **Function:** Allows safe practice
- **Design keys:**
  - Clear feedback on actions
  - No failure penalty
  - Tests relevant skills
- **Memorable additions:**
  - Personality despite role
  - Increasing difficulty options
  - Comments on player performance

### Narrative Roles

NPCs who primarily serve the story.

**Ally**
- **Function:** Supports player's goals
- **Design keys:**
  - Reliability (player can count on them)
  - Limitations (can't solve problems for player)
  - Emotional connection opportunity
- **Memorable additions:**
  - Personal goals that sometimes conflict
  - Growth during story
  - Moments of vulnerability

**Foil**
- **Function:** Contrasts with player/protagonist
- **Design keys:**
  - Clear philosophical difference
  - Competent in own right
  - Forces player to examine their path
- **Memorable additions:**
  - Valid point of view
  - Mutual respect despite difference
  - Potential for conversion

**Victim**
- **Function:** Creates stakes and motivation
- **Design keys:**
  - Player cares about their fate
  - Threat feels real
  - Resolution is satisfying
- **Memorable additions:**
  - Agency of their own
  - Can be saved or lost based on player action
  - Not purely passive

### Access Control

NPCs who regulate player progress.

**Gatekeeper**
- **Function:** Controls access to areas/abilities
- **Design keys:**
  - Clear requirements communicated
  - Blocking feels fair
  - Opening feels earned
- **Memorable additions:**
  - Reason for blocking makes sense
  - Relationship changes when access granted
  - Hidden exceptions or shortcuts

**Examiner**
- **Function:** Tests player to grant access
- **Design keys:**
  - Test matches required skill
  - Failure is instructive
  - Success feels earned
- **Memorable additions:**
  - Standards have history
  - Multiple approaches accepted
  - Acknowledgment of mastery

---

## NPC Personality Shortcuts

Quick methods for making NPCs feel distinct.

### The Trait Triangle

Give each NPC exactly three traits:
1. **Visible trait** (immediately apparent)
2. **Revealed trait** (discovered through interaction)
3. **Hidden trait** (discovered in key moments)

### The Contradiction Method

Define one apparent trait, then contradict it:
- The gruff soldier who writes poetry
- The cheerful merchant hiding grief
- The cowardly assistant with hidden bravery

### The Expertise Method

Give each NPC one thing they know more about than anyone:
- The guard who knows every shortcut
- The cook who knows everyone's secrets
- The child who knows where things are hidden

### The Speech Pattern Method

Distinguish NPCs through how they speak:
- Length (terse vs verbose)
- Register (formal vs casual)
- Rhythm (quick vs measured)
- Vocabulary (technical vs simple)
- Verbal tics (catchphrases, repeated words)

---

## NPC Economy

### How Many NPCs?

Calculate based on development capacity:

| NPC Depth | Dev Time | Recommended Per Game |
|-----------|----------|---------------------|
| Deep (arc, unique art, many lines) | High | 3-5 |
| Medium (personality, some lines) | Medium | 5-15 |
| Light (function, brief interaction) | Low | 10-30 |
| Flavor (minimal, ambient) | Minimal | As needed |

### Combining Functions

Reduce NPC count by combining functions:
- Merchant + Quest giver
- Mentor + Gatekeeper
- Guide + Lore keeper
- Ally + Foil

### Recurring NPCs

Get more value from NPCs by recurring:
- Appears in multiple areas
- Role evolves over time
- Relationship deepens
- Callbacks to earlier interactions

---

## NPC Placement

### Where Should NPCs Be?

**Safe zones:** Service providers, healers, merchants
**Transition areas:** Guides, warning givers
**Challenge areas:** Minimal NPCs, allies in distress
**Exploration rewards:** Lore keepers, hidden merchants

### NPC Schedules

For dynamic worlds:
- Where are they during day vs night?
- Do they move between locations?
- Are they available during certain conditions only?

### NPC Density

Match density to area purpose:
- Hubs: Higher density, more services
- Wilderness: Sparse, meaningful encounters
- Dungeons: Minimal, high impact
- Towns: Varied density by district

---

## Common NPC Mistakes

### Avoid These

**The exposition machine:** NPC whose only purpose is delivering backstory
**The quest vending machine:** NPC with no personality, just objectives
**The unhelpful helper:** Ally who can't actually assist
**The static statue:** NPC who never reacts to world changes
**The unreliable service:** Key function that's unavailable when needed

### Signs of Good NPC Design

- Players remember their names
- Players seek them out
- Players quote their lines
- Players care about their fate
- NPCs serve clear gameplay function
