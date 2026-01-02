#!/usr/bin/env python3
"""
Brass/Lead - Subtractive with Attack Transients

Brass section sounds and bright synth leads with breath/attack noise.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pathlib import Path

SAMPLE_RATE = 22050


def breath_noise(duration: float, intensity: float = 0.3) -> np.ndarray:
    """Generate breath noise for wind instrument attacks."""
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples)

    # Band-limited noise (breath is mostly mid-high frequencies)
    noise = np.random.randn(samples)
    b, a = butter(2, [300 / (SAMPLE_RATE / 2), 4000 / (SAMPLE_RATE / 2)], btype='band')
    noise = lfilter(b, a, noise)

    # Shape with attack envelope
    env = np.exp(-t * 15) * intensity

    return noise * env


def saw_oscillator(freq: float, t: np.ndarray) -> np.ndarray:
    """Band-limited sawtooth for brass sound."""
    output = np.zeros_like(t)
    num_harmonics = min(25, int(SAMPLE_RATE / 2 / freq))

    for h in range(1, num_harmonics + 1):
        output += np.sin(2 * np.pi * freq * h * t) / h

    return output * 2 / np.pi


def brass_section(freq: float, duration: float = 1.0,
                  attack_time: float = 0.08,
                  brightness: float = 0.7) -> np.ndarray:
    """
    Brass section sound (trumpet/horn ensemble).

    Key characteristics:
    - Slow attack with breath noise
    - Filter opens during attack
    - Rich harmonics
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Base oscillator (slightly detuned for ensemble)
    osc1 = saw_oscillator(freq, t)
    osc2 = saw_oscillator(freq * 1.003, t)
    osc3 = saw_oscillator(freq * 0.997, t)
    osc = (osc1 + osc2 * 0.5 + osc3 * 0.5) / 2

    # Filter envelope: opens as note attacks
    filter_env = 1 - np.exp(-t / attack_time * 3)
    cutoff_min = 400
    cutoff_max = 800 + brightness * 3000
    cutoff = cutoff_min + (cutoff_max - cutoff_min) * filter_env

    # Apply time-varying filter
    filtered = np.zeros_like(osc)
    chunk_size = SAMPLE_RATE // 100

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        freq_norm = min(cutoff[min(i, len(cutoff) - 1)] / (SAMPLE_RATE / 2), 0.99)
        b, a = butter(2, freq_norm, btype='low')
        filtered[i:i + len(chunk)] = lfilter(b, a, chunk)

    # Amplitude envelope with slow attack
    amp_env = (1 - np.exp(-t / attack_time * 4))

    # Add breath noise at attack
    breath = breath_noise(duration, 0.25)

    output = filtered * amp_env + breath

    return output / (np.max(np.abs(output)) + 1e-10)


def trumpet(freq: float, duration: float = 1.0,
            muted: bool = False) -> np.ndarray:
    """
    Solo trumpet sound.

    Brighter and more focused than section.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Trumpet has prominent odd harmonics
    output = np.zeros_like(t)
    harmonics = [1, 2, 3, 4, 5, 6, 7, 8]
    amps = [1.0, 0.6, 0.8, 0.4, 0.5, 0.3, 0.2, 0.15]

    for h, amp in zip(harmonics, amps):
        if freq * h < SAMPLE_RATE / 2:
            # Slight random phase for natural sound
            phase = np.random.rand() * 2 * np.pi
            output += np.sin(2 * np.pi * freq * h * t + phase) * amp

    # Muted trumpet has reduced highs
    if muted:
        b, a = butter(2, 1500 / (SAMPLE_RATE / 2), btype='low')
        output = lfilter(b, a, output)
        # Mute adds nasal resonance
        output += np.sin(2 * np.pi * freq * 2.5 * t) * 0.3
    else:
        # Open trumpet filter
        b, a = butter(2, 4000 / (SAMPLE_RATE / 2), btype='low')
        output = lfilter(b, a, output)

    # Attack envelope
    attack = 1 - np.exp(-t * 20)

    # Add breath
    breath = breath_noise(duration, 0.15)

    output = output * attack + breath

    return output / (np.max(np.abs(output)) + 1e-10)


def synth_lead(freq: float, duration: float = 0.5,
               style: str = 'bright') -> np.ndarray:
    """
    Synth lead sounds.

    Styles:
    - bright: High resonance, cutting
    - warm: Lower cutoff, rounder
    - aggressive: Distortion, harsh
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Pulse wave for lead character
    duty = 0.3  # 30% pulse
    osc = np.where((freq * t) % 1 < duty, 1.0, -1.0)

    # Add sub for body
    sub = np.sin(2 * np.pi * freq * t) * 0.4

    combined = osc + sub

    if style == 'bright':
        cutoff = 3000
        resonance = 0.8
    elif style == 'warm':
        cutoff = 1500
        resonance = 0.3
    else:  # aggressive
        cutoff = 4000
        resonance = 0.9
        combined = np.tanh(combined * 2)  # Soft clip distortion

    # Filter
    cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)
    b, a = butter(2, cutoff_norm, btype='low')
    output = lfilter(b, a, combined)

    # Snappy envelope for lead
    amp = (1 - np.exp(-t * 100)) * np.exp(-t * 2)
    output *= amp

    return output / (np.max(np.abs(output)) + 1e-10)


def supersaw(freq: float, duration: float = 1.0,
             voices: int = 7, detune: float = 15.0) -> np.ndarray:
    """
    Classic supersaw for trance/EDM leads.

    Multiple detuned saws for massive width.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    # Spread voices across detune range
    detune_spread = np.linspace(-detune, detune, voices)

    for cents in detune_spread:
        ratio = 2 ** (cents / 1200)
        voice = saw_oscillator(freq * ratio, t)
        output += voice / voices

    # High-pass to remove mud
    b, a = butter(2, 100 / (SAMPLE_RATE / 2), btype='high')
    output = lfilter(b, a, output)

    # Envelope
    amp = (1 - np.exp(-t * 30)) * np.exp(-t * 0.5)
    output *= amp

    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("generated/audio/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    notes = {
        'C4': 261.63,
        'E4': 329.63,
        'G4': 392.0,
        'C5': 523.25,
    }

    for name, freq in notes.items():
        note = name.lower()

        # Brass section
        audio = brass_section(freq, 2.0)
        sf.write(output_dir / f"brass_section_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Trumpet
        audio = trumpet(freq, 2.0, muted=False)
        sf.write(output_dir / f"trumpet_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Muted trumpet
        audio = trumpet(freq, 2.0, muted=True)
        sf.write(output_dir / f"trumpet_muted_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Synth leads
        for style in ['bright', 'warm', 'aggressive']:
            audio = synth_lead(freq, 1.0, style)
            sf.write(output_dir / f"lead_{style}_{note}.wav",
                     audio, SAMPLE_RATE, subtype='PCM_16')

        # Supersaw
        audio = supersaw(freq, 2.0)
        sf.write(output_dir / f"lead_supersaw_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated brass/lead samples in {output_dir}")


if __name__ == "__main__":
    main()
