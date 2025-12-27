# Dialogue Writing Guide

Practical techniques for writing effective game dialogue.

---

## Dialogue Fundamentals

### Every Line Must Earn Its Place

Dialogue in games competes for player attention. Each line should serve at least one purpose:

| Purpose | Priority | Example |
|---------|----------|---------|
| **Gameplay info** | High | "The key is in the tower" |
| **Immediate motivation** | High | "Help us before nightfall" |
| **Character voice** | Medium | "Another adventurer? How tiresome." |
| **World texture** | Medium | "Before the war, this was a garden" |
| **Emotional beat** | Situational | "I never thought I'd see home again" |
| **Comedy/relief** | Situational | "At least you're not on fire" |

### The Three-Line Rule

Can this be said in fewer lines? Usually yes.

**Before:**
> "Greetings, traveler. I am the keeper of this library. I have been here for many years, guarding the ancient texts. We have books on many subjects. Is there something specific you seek? Perhaps I can help you find it."

**After:**
> "Welcome to the Archive. What do you seek?"

---

## Character Voice

### Establishing Distinct Voices

Each character should be identifiable by dialogue alone.

**Voice components:**
- **Vocabulary:** Simple or complex, technical or plain
- **Sentence length:** Terse or verbose
- **Tone:** Formal or casual, warm or cold
- **Rhythm:** Measured or rapid, flowing or choppy
- **Quirks:** Catchphrases, verbal tics, topics they return to

### Voice Template

```
CHARACTER: [Name]

Vocabulary level: [ ] Simple [ ] Average [ ] Complex
Sentence length: [ ] Short [ ] Medium [ ] Long
Formality: [ ] Very formal [ ] Formal [ ] Casual [ ] Very casual
Emotional range: [ ] Restrained [ ] Moderate [ ] Expressive
Speech speed: [ ] Slow/measured [ ] Normal [ ] Fast/eager

Signature phrases: _________________
Topics they mention often: _________________
Words they never use: _________________
Verbal tics: _________________
```

### Voice Contrast

Dialogue scenes work when voices contrast:

| Character A | Character B | Dynamic |
|-------------|-------------|---------|
| Formal | Casual | Culture clash |
| Verbose | Terse | Information asymmetry |
| Optimistic | Cynical | Philosophical tension |
| Expert | Novice | Teaching moment |

---

## Dialogue Structure

### Conversation Flow

```
[Greeting/Context] ─── Establishes situation
       ↓
[Topic selection] ─── Player chooses direction
       ↓
[Information exchange] ─── Core content
       ↓
[Reaction/consequence] ─── Shows dialogue mattered
       ↓
[Exit/continuation] ─── Clean conclusion or next topic
```

### Topic Organization

For NPCs with multiple topics:

```
[Main greeting]
  ├─ [Primary topic] ─── What player likely came for
  │     └─ [Follow-up options]
  ├─ [Secondary topic] ─── Additional useful info
  │     └─ [Follow-up options]
  ├─ [Character topic] ─── Learn about the NPC
  │     └─ [Deeper conversation if available]
  └─ [Exit]
```

### Player Dialogue Options

**Good options are:**
- Distinct from each other
- Clear in meaning
- Representative of player intent

**Option format:**
```
[What player says (or gist)] → [What NPC infers]
```

**Avoid:**
- Options that all lead to same response
- Options where player can't predict NPC reaction
- "Gotcha" options that don't mean what they seem

---

## Exposition Techniques

### The Information Problem

Players need information. Exposition dumps are boring. Solution: make exposition active.

### Active Exposition Methods

**Through conflict:**
> "You think the ancient war was about territory? The factions fought for something far more dangerous."

**Through discovery:**
> "This marking... I've seen it before. In the ruins beneath the capital."

**Through urgency:**
> "No time to explain—the barrier falls at midnight. You need to reach the temple before then."

**Through teaching:**
> "Watch the blade angle. Like this. The metal here was folded by the old masters."

### The "Ice Cream Truck" Principle

Players will wait for information they want. They won't wait for information you want to give them.

**Create curiosity first:**
1. Show something unexplained
2. Let player wonder
3. Reveal explanation when player seeks it

---

## Player Choice in Dialogue

### Choice Types

| Type | Player Experience | Design Complexity |
|------|-------------------|-------------------|
| **Flavor** | Expression, roleplay | Low |
| **Information** | Choose what to learn | Low-Medium |
| **Tactical** | Affect immediate situation | Medium |
| **Strategic** | Affect story direction | High |
| **Moral** | Express values | Medium-High |

### Designing Good Choices

**The choice should be:**
- Clear (player understands options)
- Meaningful (outcomes differ)
- Informed (player has context)
- Unobvious (no "right answer")

**Example of weak choice:**
> A) "I'll help you"
> B) "I won't help you"
> C) "Tell me more"

C is clearly the "safe" option. A and B force commitment without information.

**Improved version:**
> A) "I'll investigate the ruins" (stealth approach)
> B) "I'll confront the mayor directly" (direct approach)
> C) "I need to think about this" (defer decision)

Each option is a distinct approach with clear implications.

---

## Dialogue for Game States

### First Meeting

Establish character and offer core services/information.
- Brief introduction
- Clear function ("I'm the blacksmith")
- Optional: one memorable line

### Return Visits

Acknowledge relationship while staying efficient.
- Short greeting variant
- Skip reintroduction
- Reference previous interactions if significant

### Post-Event

React to major game events.
- Comment on what happened
- Show impact on character
- May unlock new dialogue

### Quest States

**Quest available:**
> "I have a problem. Perhaps you can help."

**Quest in progress:**
> "Any progress on [objective]?"

**Quest complete:**
> "You did it! Here's your reward."

**Quest failed:**
> "I heard what happened. A shame."

---

## Common Mistakes

### The Exposition Monologue

**Problem:** NPC talks for paragraphs.
**Solution:** Break into exchanges. Player responds or prompts.

### The Identical Response

**Problem:** All dialogue options lead to same NPC response.
**Solution:** If you can't write different responses, consolidate options.

### The Omniscient NPC

**Problem:** Random NPC knows all player's business.
**Solution:** NPCs should know only what they'd realistically know.

### The Time-Frozen Conversation

**Problem:** Urgent situations, but NPCs chat casually.
**Solution:** Match dialogue urgency to situation urgency.

### The Colorless Exchange

**Problem:** Information delivered, but no character or flavor.
**Solution:** Add one character-specific element to each exchange.

---

## Dialogue Testing

### Self-Tests

1. **Read aloud:** Does it sound natural?
2. **Cover names:** Can you tell who's speaking?
3. **Cut test:** Remove a line. Is anything lost?
4. **Purpose test:** What does each line accomplish?

### Player Testing

1. **Comprehension:** Did they understand the information?
2. **Engagement:** Did they read it all?
3. **Character:** Can they describe the character?
4. **Choice:** Did they feel their choices mattered?

---

## Dialogue Economy

### Word Budget

Set limits based on game scope:

| NPC Type | Word Budget |
|----------|-------------|
| Flavor NPC | 20-50 words total |
| Service NPC | 50-150 words total |
| Minor quest NPC | 150-400 words total |
| Major NPC | 400-1000 words total |
| Core character | 1000+ words total |

### Prioritizing Dialogue

1. **Essential:** Gameplay-critical information
2. **Important:** Main story and character development
3. **Enriching:** World building and flavor
4. **Polish:** Extra lines for immersion

Cut from bottom up if over budget.

---

## Quick Reference

### Line-Writing Checklist

- [ ] Serves a clear purpose
- [ ] Could not be shorter
- [ ] Character voice is present
- [ ] Appropriate to situation
- [ ] Player can respond meaningfully
- [ ] Information is clear

### Scene-Writing Checklist

- [ ] Clear structure (beginning, middle, end)
- [ ] Voices are distinct
- [ ] Player has agency
- [ ] Purpose is achieved efficiently
- [ ] Exit is clean
- [ ] State changes are handled
