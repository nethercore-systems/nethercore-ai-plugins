---
description: Write a SOUND spec for an SFX and run the unified generator
argument-hint: "<id>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Generate SFX

Create a SOUND spec at `.studio/specs/sounds/<id>.spec.py`.

## Output

- Writes: `.studio/specs/sounds/<id>.spec.py`
- Generate with: `python .studio/generate.py --only sounds`

## Spec Template

```python
# <id> SFX Specification
# Run: python .studio/generate.py --only sounds

SOUND = {
    "sound": {
        "name": "<id>",
        "category": "ui",
        "duration": 0.2,
        "sample_rate": 22050,
        "layers": [],
        "envelope": {"attack": 0.005, "decay": 0.15, "sustain": 0, "release": 0.05},
        "normalize": True,
        "peak_db": -3.0,
    }
}
```
