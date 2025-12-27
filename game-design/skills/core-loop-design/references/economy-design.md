# Game Economy Design

Frameworks for designing resource systems that create meaningful decisions.

---

## Economy Fundamentals

### What is a Game Economy?

A game economy is any system where:
- Resources are **generated** (sources)
- Resources are **consumed** (sinks)
- Players make **decisions** about resource use

### Economy Types

| Type | Description | Examples |
|------|-------------|----------|
| **Single currency** | One resource for all transactions | Gold, coins |
| **Multi-currency** | Different resources for different purposes | Gold + gems + materials |
| **Energy** | Time-gated resource | Stamina, action points |
| **Inventory** | Space-limited storage | Item slots, weight |
| **Abstract** | Non-physical resources | Reputation, time |

---

## Source and Sink Analysis

### Sources (Where Resources Come From)

**Fixed sources:**
- [ ] Quest rewards
- [ ] Boss drops
- [ ] One-time pickups
- [ ] Achievement rewards

**Renewable sources:**
- [ ] Enemy drops
- [ ] Resource nodes
- [ ] Passive generation
- [ ] Repeatable quests

**Player-controlled sources:**
- [ ] Crafting
- [ ] Trading
- [ ] Selling items
- [ ] Conversion from other resources

### Sinks (Where Resources Go)

**Required sinks:**
- [ ] Equipment purchases
- [ ] Ability unlocks
- [ ] Progression gates
- [ ] Quest requirements

**Optional sinks:**
- [ ] Consumables
- [ ] Cosmetics
- [ ] Side upgrades
- [ ] Quality-of-life purchases

**Removal sinks:**
- [ ] Death penalties
- [ ] Repair costs
- [ ] Time decay
- [ ] Conversion to other resources

---

## Economy Balance

### The Bathtub Model

```
        [Sources]
            │
            ▼
    ┌───────────────┐
    │   Player's    │ ← Water level = player wealth
    │   Resources   │
    └───────────────┘
            │
            ▼
        [Sinks]
```

**Balanced:** Sources ≈ Sinks (stable wealth)
**Inflationary:** Sources > Sinks (wealth grows, prices lose meaning)
**Deflationary:** Sources < Sinks (wealth shrinks, frustration)

### Balance Formulas

**Expected income per session:**
```
(Source A × Drop rate A × Kills per session) +
(Source B × Drop rate B × Nodes per session) +
...
= Total expected income
```

**Expected spending per session:**
```
(Consumable use × Cost) +
(Upgrade availability × Cost) +
(Death penalty × Expected deaths) +
...
= Total expected spending
```

**Target:** Income ≥ Spending with surplus for major purchases

---

## Currency Design

### Single Currency

**Pros:**
- Simple to understand
- Easy to balance
- Clear value comparison

**Cons:**
- One resource does everything
- Limited design space
- Can feel generic

**When to use:** Simple games, game jams, clear progression

### Multi-Currency

**Pros:**
- Specialized purposes
- More decision points
- Richer economy

**Cons:**
- Complex to balance
- Can confuse players
- Risk of resource overwhelm

**When to use:** RPGs, complex progression, longer games

### Currency Design Template

```
═══════════════════════════════════════════
CURRENCY: [Name]

Purpose: What this currency is primarily for
Visual: How it appears (icon, color)

Sources:
• Primary: _______________
• Secondary: _______________
• Rate: ___ per hour of play

Sinks:
• Primary: _______________
• Secondary: _______________
• Major purchases: _______________

Scarcity level: [ ] Abundant [ ] Moderate [ ] Scarce [ ] Very Scarce

Relationship to other currencies:
• Can convert to: _______________
• Can convert from: _______________
• Conversion rate: _______________
═══════════════════════════════════════════
```

---

## Pricing Strategy

### Price Anchoring

Establish reference prices early:
- First shop sets expectations
- Consistent pricing builds trust
- Deviations need justification

### Pricing Scale

**Linear pricing:**
```
Tier 1: 100
Tier 2: 200
Tier 3: 300
```
Simple, predictable, may not feel like big upgrades

**Exponential pricing:**
```
Tier 1: 100
Tier 2: 300
Tier 3: 900
```
Creates aspiration, makes high tiers feel significant

**Tiered pricing:**
```
Tier 1: 100
Tier 2: 150
Tier 3: 500
Tier 4: 600
Tier 5: 2000
```
Matches content breakpoints, feels designed

### Price Table Template

| Item Tier | Base Price | Drop Rate Balance | Session Count to Afford |
|-----------|------------|-------------------|------------------------|
| Common | | Should be affordable quickly | 0.5-1 |
| Uncommon | | Requires some saving | 2-3 |
| Rare | | Goal for several sessions | 5-10 |
| Legendary | | Long-term goal | 20+ |

---

## Scarcity Design

### Why Scarcity Matters

Abundant resources have no value. Scarcity creates:
- Meaningful decisions
- Satisfaction when acquired
- Motivation to play

### Scarcity Mechanisms

**Supply scarcity:**
- Limited sources
- Low drop rates
- One-time only

**Time scarcity:**
- Slow regeneration
- Cooldowns
- Session limits

**Space scarcity:**
- Inventory limits
- Storage caps
- Carrying capacity

**Opportunity scarcity:**
- Can't afford everything
- Mutually exclusive options
- Build commitment

### Scarcity Levels

| Level | Description | Player Feeling | Use For |
|-------|-------------|----------------|---------|
| Abundant | Always have plenty | Comfortable, maybe careless | Basic consumables |
| Moderate | Usually have enough | Careful but not worried | Standard upgrades |
| Scarce | Often run short | Strategic, thoughtful | Powerful items |
| Very scarce | Rarely have any | Precious, exciting to get | Build-defining gear |

---

## Economy Lifecycle

### Early Game Economy

**Goals:**
- Teach resource usage
- Provide frequent rewards
- Avoid frustrating shortages

**Design:**
- Generous sources
- Low prices
- Essential sinks only

### Mid Game Economy

**Goals:**
- Create meaningful decisions
- Introduce savings goals
- Add complexity

**Design:**
- Balanced sources/sinks
- Moderate scarcity
- Optional spending appears

### Late Game Economy

**Goals:**
- Reward mastery
- Maintain engagement
- Avoid inflation

**Design:**
- High-value sources gated by skill
- Expensive aspirational sinks
- Prestige/alternative currencies

---

## Common Economy Problems

### Inflation

**Symptoms:**
- Players have way too much currency
- Prices feel meaningless
- Nothing to buy

**Causes:**
- Sources too generous
- Not enough sinks
- No expensive goals

**Solutions:**
- Add prestige currencies
- Create money sinks (cosmetics, housing)
- Reduce source rates

### Deflation

**Symptoms:**
- Players never have enough
- Everything feels too expensive
- Grind is mandatory

**Causes:**
- Required purchases too frequent
- Sources too stingy
- Prices too high

**Solutions:**
- More sources
- Lower prices
- Make some purchases optional

### Dead Currency

**Symptoms:**
- Players ignore the resource
- Nothing worth buying
- Accumulates with no use

**Causes:**
- Poor sink design
- Better alternatives
- Unclear purpose

**Solutions:**
- Add desirable sinks
- Make it required for something
- Merge with another currency

---

## Economy Testing

### Simulation Method

1. Calculate expected income per hour
2. Calculate expected spending per hour
3. Project over full playthrough
4. Check for inflation/deflation points

### Playtest Checkpoints

| Checkpoint | Expected Wealth | Affordable Items | Session Count |
|------------|-----------------|------------------|---------------|
| End of tutorial | | | |
| First major unlock | | | |
| Mid-game | | | |
| Pre-finale | | | |
| End-game | | | |

### Warning Signs

- [ ] Players hoarding currency (not enough sinks)
- [ ] Players always broke (not enough sources)
- [ ] Players ignoring resource (not valuable)
- [ ] Players stressed about resource (too punishing)
- [ ] Players trivializing content with purchases (too powerful)

---

## Quick Reference

### Economy Design Checklist

- [ ] All resources have clear purpose
- [ ] Sources match intended scarcity
- [ ] Sinks are desirable (not just punishing)
- [ ] Prices are balanced to income
- [ ] Early game is generous
- [ ] Late game has aspirational goals
- [ ] Economy doesn't break at any point
