#!/usr/bin/env python3
"""
Acoustic Guitar - Karplus-Strong with Body Resonance

Generates realistic plucked acoustic guitar sounds using physical modeling.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pathlib import Path

SAMPLE_RATE = 22050


def karplus_strong(freq: float, duration: float,
                   damping: float = 0.996,
                   brightness: float = 0.7) -> np.ndarray:
    """Core Karplus-Strong algorithm for plucked strings."""
    num_samples = int(SAMPLE_RATE * duration)
    delay_length = max(2, int(SAMPLE_RATE / freq))

    # Initialize with filtered noise (the "pluck" excitation)
    noise = np.random.randn(delay_length)

    # Filter initial noise based on brightness (softer pluck = less highs)
    if brightness < 1.0:
        cutoff = 0.1 + brightness * 0.8
        b, a = butter(2, cutoff, btype='low')
        noise = lfilter(b, a, noise)

    delay_line = noise.copy()
    output = np.zeros(num_samples)
    idx = 0

    for i in range(num_samples):
        output[i] = delay_line[idx]

        # Low-pass averaging: the key to natural decay
        next_idx = (idx + 1) % delay_length
        averaged = 0.5 * (delay_line[idx] + delay_line[next_idx]) * damping
        delay_line[idx] = averaged
        idx = (idx + 1) % delay_length

    return output


def body_resonance(signal: np.ndarray, freq: float) -> np.ndarray:
    """Add guitar body resonance for warmth."""
    t = np.linspace(0, len(signal) / SAMPLE_RATE, len(signal))

    # Body resonance around 100-200 Hz
    body_freq = min(200, freq * 0.5)
    body = np.sin(2 * np.pi * body_freq * t) * 0.08
    body *= np.exp(-t * 4)

    # Second harmonic emphasis from soundboard
    harm2 = np.sin(2 * np.pi * freq * 2 * t) * 0.05
    harm2 *= np.exp(-t * 3)

    return signal + body + harm2


def generate_acoustic_guitar(freq: float, duration: float = 1.5,
                             style: str = 'steel') -> np.ndarray:
    """
    Generate complete acoustic guitar note.

    Args:
        freq: Note frequency in Hz
        duration: Note duration in seconds
        style: 'steel' (bright) or 'nylon' (warm)
    """
    if style == 'steel':
        damping = 0.996
        brightness = 0.75
    else:  # nylon
        damping = 0.994
        brightness = 0.45

    # Generate plucked string
    string = karplus_strong(freq, duration, damping, brightness)

    # Add body resonance
    output = body_resonance(string, freq)

    # Slight chorusing for richness (two strings slightly detuned)
    detune = 1.003
    string2 = karplus_strong(freq * detune, duration, damping, brightness)
    output += string2 * 0.15

    # Normalize
    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("assets/audio/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate samples at different pitches
    notes = {
        'E2': 82.41,
        'A2': 110.0,
        'D3': 146.83,
        'G3': 196.0,
        'B3': 246.94,
        'E4': 329.63,
    }

    for name, freq in notes.items():
        # Steel string version
        audio = generate_acoustic_guitar(freq, 2.0, 'steel')
        sf.write(output_dir / f"guitar_steel_{name.lower()}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Nylon string version
        audio = generate_acoustic_guitar(freq, 2.0, 'nylon')
        sf.write(output_dir / f"guitar_nylon_{name.lower()}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated guitar samples in {output_dir}")


if __name__ == "__main__":
    main()
