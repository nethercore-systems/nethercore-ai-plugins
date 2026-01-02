#!/usr/bin/env python3
"""
Synth Bass - Subtractive Synthesis

Classic analog-style bass with filter envelope for punch and warmth.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pathlib import Path

SAMPLE_RATE = 22050


def saw_wave(freq: float, t: np.ndarray) -> np.ndarray:
    """Band-limited sawtooth approximation."""
    # Use additive synthesis to avoid aliasing
    output = np.zeros_like(t)
    num_harmonics = min(20, int(SAMPLE_RATE / 2 / freq))

    for h in range(1, num_harmonics + 1):
        output += np.sin(2 * np.pi * freq * h * t) * (1.0 / h)

    return output * 2 / np.pi


def apply_filter_envelope(signal: np.ndarray,
                          cutoff_start: float, cutoff_end: float,
                          attack: float = 0.01,
                          decay: float = 0.2,
                          resonance: float = 2.0) -> np.ndarray:
    """Apply time-varying lowpass filter."""
    t = np.linspace(0, len(signal) / SAMPLE_RATE, len(signal))

    # Filter envelope: attack to peak, then decay to sustain
    env = np.where(
        t < attack,
        t / attack,  # Attack phase
        np.exp(-(t - attack) / decay)  # Decay phase
    )
    cutoff = cutoff_end + (cutoff_start - cutoff_end) * env

    # Process in chunks for time-varying filter
    output = np.zeros_like(signal)
    chunk_size = SAMPLE_RATE // 100  # 10ms chunks

    for i in range(0, len(signal), chunk_size):
        chunk = signal[i:i + chunk_size]
        freq = cutoff[min(i + chunk_size // 2, len(cutoff) - 1)]
        freq_norm = min(freq / (SAMPLE_RATE / 2), 0.99)

        if freq_norm > 0.01:
            b, a = butter(2, freq_norm, btype='low')
            output[i:i + len(chunk)] = lfilter(b, a, chunk)
        else:
            output[i:i + len(chunk)] = chunk * 0.1

    return output


def mono_bass(freq: float, duration: float = 0.5,
              style: str = 'punchy') -> np.ndarray:
    """
    Classic mono synth bass.

    Styles:
    - 'punchy': Quick filter decay, percussive
    - 'smooth': Slower filter, rounder
    - 'acid': High resonance, squelchy
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Detuned oscillators for thickness
    osc1 = saw_wave(freq, t)
    osc2 = saw_wave(freq * 1.005, t)  # Slight detune
    osc = (osc1 + osc2) * 0.5

    # Sub oscillator (one octave down, sine)
    sub = np.sin(2 * np.pi * freq * 0.5 * t) * 0.6

    # Style-dependent filter settings
    if style == 'punchy':
        cutoff_start, cutoff_end = 2000, 150
        decay = 0.08
    elif style == 'smooth':
        cutoff_start, cutoff_end = 1200, 300
        decay = 0.3
    else:  # acid
        cutoff_start, cutoff_end = 3000, 200
        decay = 0.15

    # Apply filter envelope
    filtered = apply_filter_envelope(osc, cutoff_start, cutoff_end,
                                     attack=0.005, decay=decay)

    # Combine with sub
    output = filtered + sub

    # Amplitude envelope
    amp_attack = 1 - np.exp(-t * 150)
    amp_decay = np.exp(-t * 3)
    amp = amp_attack * amp_decay

    output *= amp

    return output / (np.max(np.abs(output)) + 1e-10)


def reese_bass(freq: float, duration: float = 1.0) -> np.ndarray:
    """
    Reese bass - heavily detuned saws for massive sound.

    Classic DnB/Neuro bass.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Multiple detuned oscillators
    detune_cents = [-15, -5, 0, 5, 15]
    output = np.zeros_like(t)

    for cents in detune_cents:
        detune_ratio = 2 ** (cents / 1200)
        osc = saw_wave(freq * detune_ratio, t)
        output += osc * 0.2

    # Low-pass filter (static, just to tame highs)
    b, a = butter(2, 800 / (SAMPLE_RATE / 2), btype='low')
    output = lfilter(b, a, output)

    # Sub layer
    sub = np.sin(2 * np.pi * freq * 0.5 * t) * 0.4
    output += sub

    # Simple envelope
    env = (1 - np.exp(-t * 30)) * np.exp(-t * 1)
    output *= env

    return output / (np.max(np.abs(output)) + 1e-10)


def sub_bass(freq: float, duration: float = 0.5) -> np.ndarray:
    """
    Pure sub bass - sine wave with punch.

    For when you just need low end.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Pure sine at fundamental
    fundamental = np.sin(2 * np.pi * freq * t)

    # Slight saturation for presence
    saturated = np.tanh(fundamental * 1.5) * 0.7

    # Attack click for definition
    click = np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 50) * 0.3

    output = saturated + click

    # Envelope
    env = (1 - np.exp(-t * 100)) * np.exp(-t * 4)
    output *= env

    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("generated/audio/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    bass_notes = {
        'E1': 41.20,
        'A1': 55.0,
        'D2': 73.42,
        'G2': 98.0,
        'C2': 65.41,
        'F2': 87.31,
    }

    for name, freq in bass_notes.items():
        note = name.lower()

        # Punchy bass
        audio = mono_bass(freq, 1.0, 'punchy')
        sf.write(output_dir / f"bass_punchy_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Smooth bass
        audio = mono_bass(freq, 1.5, 'smooth')
        sf.write(output_dir / f"bass_smooth_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Reese bass
        audio = reese_bass(freq, 2.0)
        sf.write(output_dir / f"bass_reese_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Sub bass
        audio = sub_bass(freq, 1.0)
        sf.write(output_dir / f"bass_sub_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated synth bass samples in {output_dir}")


if __name__ == "__main__":
    main()
