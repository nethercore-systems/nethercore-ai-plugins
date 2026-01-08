---
description: Write an INSTRUMENT spec and run the unified generator
argument-hint: "<id>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Generate Instrument

Create an INSTRUMENT spec at `.studio/specs/instruments/<id>.spec.py`.

## Output

- Writes: `.studio/specs/instruments/<id>.spec.py`
- Generate with: `ai-studio generate --only instruments` (legacy: `python .studio/generate.py --only instruments`)

## Spec Template

```python
# <id> Instrument Specification
# Run: ai-studio generate --only instruments

INSTRUMENT = {
    "instrument": {
        "name": "<id>",
        "category": "lead",
        "base_note": "C4",
        "sample_rate": 22050,
        "synthesis": {"type": "karplus_strong", "damping": 0.996, "brightness": 0.6},
        "envelope": {"attack": 0.01, "decay": 0.3, "sustain": 0.4, "release": 0.2},
        "output": {"duration": 1.0, "bit_depth": 16, "loop": True, "loop_start": 0.1, "loop_end": 0.9},
    }
}
```
