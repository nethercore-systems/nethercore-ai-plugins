# SFX Recipes

Production-ready pyo recipes for common game sound effects.

## Quick Reference

| Recipe | File | Duration | Technique |
|--------|------|----------|-----------|
| Laser/Zap | `laser.py` | 0.15-0.3s | SuperSaw sweep |
| Explosion | `explosion.py` | 0.5-1.5s | Layered noise |
| Coin/Pickup | `coin.py` | 0.3-0.5s | Arpeggio |
| Jump | `jump.py` | 0.15-0.3s | Pitch arc |
| Hit/Punch | `hit.py` | 0.05-0.2s | Noise transient |
| Powerup | `powerup.py` | 0.4-0.8s | FM + chorus |
| Footstep | `footstep.py` | 0.05-0.15s | Filtered noise |
| UI Click | `ui-click.py` | 0.02-0.08s | Sine blip |

## Usage

Each recipe is a standalone Python script:

```bash
# Generate with default settings
python laser.py

# Generates: laser.wav
```

## Customization

Each script has clearly documented parameter sections:

```python
# =============================================================================
# PARAMETERS - Adjust these to customize the sound
# =============================================================================

START_FREQ = 1200       # Starting frequency (Hz)
END_FREQ = 200          # Ending frequency (Hz)
# ...
```

## Variations

Each recipe includes preset variations as functions:

```python
# In laser.py
def laser_high_energy():
    """More intense, higher pitched laser."""
    # ...

def laser_retro():
    """Classic 8-bit style zap."""
    # ...

if __name__ == "__main__":
    # laser_retro()  # Uncomment to use variation
    render()
```

## Batch Generation

For generating complete sound sets:

```python
# In footstep.py
def render_all_surfaces(output_dir="."):
    """Render footsteps for all surfaces."""
    # Generates: footstep_concrete.wav, footstep_wood.wav, etc.

# In ui-click.py
def render_ui_set(output_dir="."):
    """Render a complete UI sound set."""
    # Generates: ui_click.wav, ui_hover.wav, ui_confirm.wav, etc.
```

## Integration

Output WAVs to your assets directory and reference in `nether.toml`:

```toml
[[assets.sounds]]
id = "laser"
path = "assets/audio/laser.wav"
```

## Adding New Recipes

Follow the template structure:

1. Parameter section at top with documented settings
2. Build function returning pyo signal chain
3. Render function with offline server setup
4. Variation functions for common presets
5. Main block with render call
