---
description: Generate a single asset by writing a spec and running the generator
argument-hint: "<type> <description>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Generate Asset

Generate **one** asset by:

1) Writing a legacy `.studio/specs/<category>/<id>.spec.py` file
2) Running the legacy generator via `ai-studio generate` (preferred) or `python .studio/generate.py`

> Note: `ai-studio` is the preferred interface. The underlying `.studio/` pipeline remains supported for compatibility.

## Args

- `<type>`: `texture` | `normal` | `sound` | `instrument` | `music` | `mesh` | `character` | `animation`
- `<description>`: short natural-language description of what to generate

## Output

- Writes a `.spec.py` into `.studio/specs/**`
- Generates outputs under `generated/**` (project convention)

## Run

After creating the spec, generate the relevant category:

```bash
ai-studio generate --only <category>
```

Legacy equivalent:

```bash
python .studio/generate.py --only <category>
```

