#!/usr/bin/env python3
"""
Pluck Synth - Karplus-Strong with Filtering

Synth plucks for arpeggios, rhythmic parts, and melodic accents.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pathlib import Path

SAMPLE_RATE = 22050


def karplus_strong_filtered(freq: float, duration: float,
                            damping: float = 0.995,
                            brightness: float = 0.7,
                            body_resonance: float = 0.0) -> np.ndarray:
    """
    Karplus-Strong with pre and post filtering options.
    """
    num_samples = int(SAMPLE_RATE * duration)
    delay_length = max(2, int(SAMPLE_RATE / freq))

    # Initial excitation
    noise = np.random.randn(delay_length)

    # Filter excitation for brightness control
    if brightness < 1.0:
        cutoff = 0.1 + brightness * 0.8
        b, a = butter(2, cutoff, btype='low')
        noise = lfilter(b, a, noise)

    delay_line = noise.copy()
    output = np.zeros(num_samples)
    idx = 0

    for i in range(num_samples):
        output[i] = delay_line[idx]
        next_idx = (idx + 1) % delay_length
        averaged = 0.5 * (delay_line[idx] + delay_line[next_idx]) * damping
        delay_line[idx] = averaged
        idx = (idx + 1) % delay_length

    # Optional body resonance
    if body_resonance > 0:
        t = np.linspace(0, duration, num_samples)
        body = np.sin(2 * np.pi * freq * 0.5 * t) * body_resonance
        body *= np.exp(-t * 5)
        output += body

    return output / (np.max(np.abs(output)) + 1e-10)


def synth_pluck(freq: float, duration: float = 0.5,
                style: str = 'clean') -> np.ndarray:
    """
    Synthesizer pluck for arpeggios and melodic parts.

    Styles:
    - clean: Pure Karplus-Strong
    - filtered: With post low-pass
    - resonant: With resonant filter sweep
    - digital: FM-based pluck
    """
    if style == 'clean':
        return karplus_strong_filtered(freq, duration, 0.996, 0.8)

    elif style == 'filtered':
        base = karplus_strong_filtered(freq, duration, 0.996, 0.9)
        b, a = butter(2, 2000 / (SAMPLE_RATE / 2), btype='low')
        return lfilter(b, a, base)

    elif style == 'resonant':
        base = karplus_strong_filtered(freq, duration, 0.994, 0.95)
        t = np.linspace(0, duration, len(base))

        # Resonant filter sweep
        output = np.zeros_like(base)
        chunk_size = SAMPLE_RATE // 100

        for i in range(0, len(base), chunk_size):
            chunk = base[i:i + chunk_size]
            progress = i / len(base)
            cutoff = 4000 * np.exp(-progress * 5) + 500
            cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)
            b, a = butter(2, cutoff_norm, btype='low')
            output[i:i + len(chunk)] = lfilter(b, a, chunk)

        return output / (np.max(np.abs(output)) + 1e-10)

    else:  # digital
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

        # FM pluck
        index = 6 * np.exp(-t * 15)
        mod = np.sin(2 * np.pi * freq * t)
        carrier = np.sin(2 * np.pi * freq * t + index * mod)

        # Amplitude
        amp = np.exp(-t * 5)

        return carrier * amp


def harp(freq: float, duration: float = 2.0) -> np.ndarray:
    """
    Harp-like pluck with long sustain and body resonance.
    """
    # Long sustain pluck
    output = karplus_strong_filtered(freq, duration, 0.998, 0.6, 0.2)

    # Add sympathetic resonance (octave)
    t = np.linspace(0, duration, len(output))
    sympathetic = np.sin(2 * np.pi * freq * 2 * t) * 0.08
    sympathetic *= np.exp(-t * 2)
    output += sympathetic

    # Gentle high-cut for warmth
    b, a = butter(2, 3000 / (SAMPLE_RATE / 2), btype='low')
    output = lfilter(b, a, output)

    return output / (np.max(np.abs(output)) + 1e-10)


def koto(freq: float, duration: float = 1.5) -> np.ndarray:
    """
    Koto (Japanese string instrument).

    Characteristic: bright attack, quick pitch bend down.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Pitch bend at attack (characteristic of koto technique)
    bend = 1 + 0.03 * np.exp(-t * 20)  # Start sharp, settle to pitch

    # Two strings slightly detuned
    delay1 = max(2, int(SAMPLE_RATE / (freq * bend[0])))
    delay2 = max(2, int(SAMPLE_RATE / (freq * 1.003 * bend[0])))

    output = np.zeros_like(t)

    # String 1
    noise1 = np.random.randn(delay1) * 0.8
    b, a = butter(2, 0.9, btype='low')
    noise1 = lfilter(b, a, noise1)
    delay_line1 = noise1.copy()
    idx1 = 0

    for i in range(len(t)):
        output[i] = delay_line1[idx1]
        next_idx = (idx1 + 1) % delay1
        averaged = 0.5 * (delay_line1[idx1] + delay_line1[next_idx]) * 0.995
        delay_line1[idx1] = averaged
        idx1 = (idx1 + 1) % delay1

    # High-frequency emphasis for brightness
    b, a = butter(2, [2000 / (SAMPLE_RATE / 2), 6000 / (SAMPLE_RATE / 2)], btype='band')
    brightness = lfilter(b, a, output) * 0.3
    output += brightness

    return output / (np.max(np.abs(output)) + 1e-10)


def marimba(freq: float, duration: float = 1.0) -> np.ndarray:
    """
    Marimba - wooden bar percussion with resonator.

    Warm, wooden tone with clear fundamental.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Fundamental is strong
    fundamental = np.sin(2 * np.pi * freq * t)

    # Characteristic partial (roughly 4x fundamental for wood)
    partial = np.sin(2 * np.pi * freq * 4 * t) * 0.3

    # Quick decay with bump from resonator
    amp = np.exp(-t * 4) + 0.2 * np.exp(-t * 1.5)

    # Mallet attack noise
    attack = np.random.randn(int(SAMPLE_RATE * 0.01)) * 0.2
    attack *= np.linspace(1, 0, len(attack))

    output = (fundamental + partial) * amp
    output[:len(attack)] += attack

    # Low-pass for warmth
    b, a = butter(2, 2500 / (SAMPLE_RATE / 2), btype='low')
    output = lfilter(b, a, output)

    return output / (np.max(np.abs(output)) + 1e-10)


def kalimba(freq: float, duration: float = 1.5) -> np.ndarray:
    """
    Kalimba (thumb piano).

    Bright metallic pluck with long decay.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Main tone (slightly inharmonic for metal tine)
    main = np.sin(2 * np.pi * freq * t)

    # Inharmonic partials (metal bar modes)
    partial1 = np.sin(2 * np.pi * freq * 2.8 * t) * 0.3
    partial2 = np.sin(2 * np.pi * freq * 5.4 * t) * 0.1

    output = main + partial1 + partial2

    # Quick attack, medium-long decay
    amp = (1 - np.exp(-t * 100)) * np.exp(-t * 2)
    output *= amp

    # Slight attack noise
    noise = np.random.randn(len(t)) * 0.05
    noise *= np.exp(-t * 50)
    output += noise

    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("generated/sounds/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    notes = {
        'C3': 130.81,
        'E3': 164.81,
        'G3': 196.0,
        'C4': 261.63,
        'E4': 329.63,
        'G4': 392.0,
        'C5': 523.25,
    }

    for name, freq in notes.items():
        note = name.lower()

        # Synth plucks
        for style in ['clean', 'filtered', 'resonant', 'digital']:
            audio = synth_pluck(freq, 1.0, style)
            sf.write(output_dir / f"pluck_{style}_{note}.wav",
                     audio, SAMPLE_RATE, subtype='PCM_16')

        # Harp
        audio = harp(freq, 3.0)
        sf.write(output_dir / f"harp_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Koto
        audio = koto(freq, 2.0)
        sf.write(output_dir / f"koto_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Marimba
        audio = marimba(freq, 1.5)
        sf.write(output_dir / f"marimba_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Kalimba
        audio = kalimba(freq, 2.0)
        sf.write(output_dir / f"kalimba_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated pluck samples in {output_dir}")


if __name__ == "__main__":
    main()
