#!/usr/bin/env python3
"""
Electric Piano - FM Synthesis (DX7-style Rhodes)

Generates classic electric piano sounds using frequency modulation.
The iconic bell-like attack with warm sustain.

This example demonstrates the modular lib/ approach:
- Imports synthesis primitives from lib/
- Only defines instrument-specific logic
- Much smaller than monolithic approach

To run standalone, copy lib/ folder to your project or adjust import path.
"""
import sys
from pathlib import Path

# Add lib/ to path for standalone execution
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

import numpy as np
import soundfile as sf

from synthesis import fm_operator, multi_envelope
from waveforms import normalize

SAMPLE_RATE = 22050


def rhodes_piano(freq: float, duration: float = 1.5, velocity: float = 0.8) -> np.ndarray:
    """
    DX7-style Rhodes electric piano.

    Uses 1:1 FM ratio with rapidly decaying modulation index for
    characteristic bell-like attack that mellows into warmth.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Velocity affects brightness (modulation index)
    base_index = 3.0 + velocity * 3.0

    # FM modulation index envelope: fast decay for bell attack
    index_env = base_index * np.exp(-t * 8)

    # Tine peak for characteristic Rhodes attack
    tine_peak = 2.0 * np.exp(-((t - 0.02) ** 2) / 0.001)
    index_env = index_env + tine_peak * velocity

    # 1:1 ratio FM
    mod = np.sin(2 * np.pi * freq * t)
    carrier = fm_operator(freq, t, index_env, mod)

    # Second harmonic for body
    harm2 = np.sin(2 * np.pi * freq * 2 * t) * 0.15 * np.exp(-t * 4)

    # Amplitude envelope
    attack = 1 - np.exp(-t * 200)
    decay = np.exp(-t * (1.0 + (1 - velocity) * 2))
    amp_env = attack * decay

    output = (carrier + harm2) * amp_env
    return normalize(output)


def wurlitzer(freq: float, duration: float = 1.5, velocity: float = 0.8) -> np.ndarray:
    """
    Wurlitzer-style electric piano.

    Brighter and more reedy than Rhodes, with prominent harmonics.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    base_index = 4.0 + velocity * 4.0
    index_env = base_index * (0.7 * np.exp(-t * 12) + 0.3 * np.exp(-t * 3))

    mod = np.sin(2 * np.pi * freq * t)
    carrier = fm_operator(freq, t, index_env, mod)

    # Growl with detuned carrier
    growl_index = base_index * 0.5 * np.exp(-t * 6)
    growl = np.sin(2 * np.pi * freq * 1.01 * t + growl_index * mod) * 0.2

    # Odd harmonics for reedy quality
    harm3 = np.sin(2 * np.pi * freq * 3 * t) * 0.08 * np.exp(-t * 5)

    # Amplitude envelope
    attack = 1 - np.exp(-t * 200)
    decay = np.exp(-t * 2)
    amp_env = attack * decay

    output = (carrier + growl + harm3) * amp_env
    return normalize(output)


def main():
    output_dir = Path("generated/audio/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate demo samples
    for freq, name in [(261.63, 'c4'), (440.0, 'a4')]:
        # Rhodes
        audio = rhodes_piano(freq, 3.0, 0.8)
        sf.write(output_dir / f"rhodes_{name}.wav", audio, SAMPLE_RATE, subtype='PCM_16')

        # Wurlitzer
        audio = wurlitzer(freq, 3.0, 0.8)
        sf.write(output_dir / f"wurli_{name}.wav", audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated electric piano samples in {output_dir}")


if __name__ == "__main__":
    main()
