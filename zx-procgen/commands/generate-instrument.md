---
name: Generate Instrument Sample
description: Generate a high-quality procedural instrument sample using advanced synthesis techniques
argument-hint: "<instrument> [style]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Generate Instrument Sample

Generate a production-quality instrument sample for use in XM tracker music.

## Arguments

- `<instrument>`: The instrument type (e.g., "guitar", "piano", "bass", "pad", "bell")
- `[style]`: Optional style modifier (e.g., "warm", "bright", "aggressive", "ethereal")

## Examples

```
/generate-instrument guitar acoustic
/generate-instrument piano electric
/generate-instrument bass punchy
/generate-instrument pad warm
/generate-instrument bell tubular
```

## Workflow

1. **Parse the request** to understand instrument type and desired character
2. **Select synthesis technique**:
   - Plucked strings → Karplus-Strong
   - Keys → FM synthesis
   - Pads → Wavetable
   - Organs → Additive
   - Leads/Bass → Subtractive
   - Bells → FM with inharmonic ratios

3. **Load the appropriate example** from `zx-procgen/skills/procedural-instruments/examples/`

4. **Generate the Python script** customized for the user's needs

5. **Run the script** to generate WAV files

6. **Provide integration instructions** for XM tracker

## Instrument Quick Reference

| Instrument | Example File | Technique |
|------------|--------------|-----------|
| Acoustic Guitar | `acoustic-guitar.py` | Karplus-Strong |
| Electric Piano | `electric-piano.py` | FM Synthesis |
| Synth Bass | `synth-bass.py` | Subtractive |
| Strings/Pad | `strings-pad.py` | Wavetable |
| Organ | `organ.py` | Additive |
| Brass/Lead | `brass-lead.py` | Subtractive |
| Bells | `fm-bell.py` | FM (inharmonic) |
| Pluck Synth | `pluck-synth.py` | Karplus-Strong |

## Output

The command will:
1. Create a Python generator script in `generator/instruments/`
2. Run the script to generate WAV samples in `assets/audio/instruments/`
3. Show how to add to `nether.toml`
4. Explain how to use in XM tracker

## Related Skills

- `procedural-instruments` - Synthesis techniques and recipes
- `procedural-sounds` - SFX generation (for non-musical sounds)
- `procedural-music` - XM tracker composition
- `xm-writer` - Programmatic XM generation
