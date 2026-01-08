#!/usr/bin/env python3
"""
Acoustic Guitar - Karplus-Strong with Body Resonance

Generates realistic plucked acoustic guitar sounds using physical modeling.

This example demonstrates the modular lib/ approach:
- Imports Karplus-Strong from lib/synthesis
- Only defines guitar-specific body resonance and styling
"""
import sys
from pathlib import Path

# Add lib/ to path for standalone execution
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

import numpy as np
import soundfile as sf

from synthesis import karplus_strong
from waveforms import normalize

SAMPLE_RATE = 22050


def body_resonance(signal: np.ndarray, freq: float) -> np.ndarray:
    """Add guitar body resonance for warmth."""
    t = np.linspace(0, len(signal) / SAMPLE_RATE, len(signal))

    # Body resonance around 100-200 Hz
    body_freq = min(200, freq * 0.5)
    body = np.sin(2 * np.pi * body_freq * t) * 0.08 * np.exp(-t * 4)

    # Second harmonic emphasis from soundboard
    harm2 = np.sin(2 * np.pi * freq * 2 * t) * 0.05 * np.exp(-t * 3)

    return signal + body + harm2


def acoustic_guitar(freq: float, duration: float = 1.5, style: str = 'steel') -> np.ndarray:
    """
    Generate complete acoustic guitar note.

    Args:
        freq: Note frequency in Hz
        duration: Note duration in seconds
        style: 'steel' (bright) or 'nylon' (warm)
    """
    presets = {
        'steel': {'damping': 0.996, 'brightness': 0.75},
        'nylon': {'damping': 0.994, 'brightness': 0.45},
    }
    params = presets.get(style, presets['steel'])

    # Generate plucked string using lib/synthesis
    string = karplus_strong(freq, duration, **params, sample_rate=SAMPLE_RATE)

    # Add body resonance
    output = body_resonance(string, freq)

    # Slight chorusing for richness
    string2 = karplus_strong(freq * 1.003, duration, **params, sample_rate=SAMPLE_RATE)
    output += string2 * 0.15

    return normalize(output)


def main():
    output_dir = Path("generated/sounds/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Standard guitar notes
    notes = {
        'E2': 82.41,
        'A2': 110.0,
        'D3': 146.83,
        'G3': 196.0,
        'B3': 246.94,
        'E4': 329.63,
    }

    for name, freq in notes.items():
        note = name.lower()

        # Steel string
        audio = acoustic_guitar(freq, 2.0, 'steel')
        sf.write(output_dir / f"guitar_steel_{note}.wav", audio, SAMPLE_RATE, subtype='PCM_16')

        # Nylon string
        audio = acoustic_guitar(freq, 2.0, 'nylon')
        sf.write(output_dir / f"guitar_nylon_{note}.wav", audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated guitar samples in {output_dir}")


if __name__ == "__main__":
    main()
