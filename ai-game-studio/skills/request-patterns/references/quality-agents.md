# Quality Agent Selection

Four agents handle asset quality - choose based on need:

| Agent | Question | Use When |
|-------|----------|----------|
| asset-critic | "Does this match the style spec?" | Comparing output to creative intent |
| asset-quality-reviewer | "Does this fit ZX limits?" | Checking technical compliance |
| quality-analyzer | "How good is this overall?" | Holistic assessment with scores |
| quality-enhancer | "Make this better" | Actively improving assets |

## Decision Flow

```
"Check my assets" →
├── Against spec/intent? → asset-critic
├── Against ZX budgets? → asset-quality-reviewer
├── Overall quality?    → quality-analyzer
└── Improve them?       → quality-enhancer
```

## Quality Pipeline Order

1. **asset-critic** - Verify spec compliance after generation
2. **asset-quality-reviewer** - Verify ZX technical limits
3. **quality-analyzer** - Get holistic quality score
4. **quality-enhancer** - Improve if score is low

## Examples

| Request | Route To |
|---------|----------|
| "Does this mesh match my style spec?" | asset-critic |
| "Will these textures fit in ROM?" | asset-quality-reviewer |
| "Rate my asset quality" | quality-analyzer |
| "Make these textures better" | quality-enhancer |
| "Are these production ready?" | quality-analyzer → asset-quality-reviewer |
