#!/usr/bin/env python3
"""
FM Bells - Inharmonic FM Synthesis

Tubular bells, chimes, and bell-like sounds using non-integer FM ratios.
"""
import numpy as np
import soundfile as sf
from pathlib import Path

SAMPLE_RATE = 22050


def fm_bell_basic(freq: float, duration: float = 2.0,
                  ratio: float = 2.76,
                  index: float = 8.0) -> np.ndarray:
    """
    Basic FM bell with inharmonic ratio.

    Non-integer ratios create the characteristic bell timbre.
    Common ratios: 1.4, 2.76, 3.5, 1.41 (sqrt2)
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    mod_freq = freq * ratio

    # Modulation index decays slowly (bells ring for a long time)
    index_env = index * np.exp(-t * 1.5)

    # Modulator
    mod = np.sin(2 * np.pi * mod_freq * t)

    # Carrier with FM
    carrier = np.sin(2 * np.pi * freq * t + index_env * mod)

    # Long decay amplitude envelope
    amp = np.exp(-t * 1.2)

    return carrier * amp


def tubular_bell(freq: float, duration: float = 3.0) -> np.ndarray:
    """
    Tubular bell / orchestral chime.

    Multiple FM operators for rich, complex bell sound.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    # Layer 1: Main body (1:2.76 ratio - classic bell)
    index1 = 6 * np.exp(-t * 0.8)
    mod1 = np.sin(2 * np.pi * freq * 2.76 * t)
    carrier1 = np.sin(2 * np.pi * freq * t + index1 * mod1)

    # Layer 2: High partial (1:4.07 for shimmer)
    index2 = 4 * np.exp(-t * 2)
    mod2 = np.sin(2 * np.pi * freq * 4.07 * t)
    carrier2 = np.sin(2 * np.pi * freq * 2 * t + index2 * mod2) * 0.4

    # Layer 3: Strike transient (higher frequencies, fast decay)
    strike_index = 10 * np.exp(-t * 20)
    strike_mod = np.sin(2 * np.pi * freq * 5.3 * t)
    strike = np.sin(2 * np.pi * freq * 3 * t + strike_index * strike_mod) * 0.3

    output = carrier1 + carrier2 + strike

    # Overall envelope with initial strike
    amp = (1 + 0.5 * np.exp(-t * 30)) * np.exp(-t * 0.8)
    output *= amp

    return output / (np.max(np.abs(output)) + 1e-10)


def church_bell(freq: float, duration: float = 5.0) -> np.ndarray:
    """
    Large church bell with beating partials.

    Church bells have complex inharmonic spectra with beating.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    # Church bell partials (approximate, based on tuned bell analysis)
    # These ratios create the characteristic "minor third" sound
    partials = [
        (1.0, 1.0, 0.8),    # Fundamental (hum note)
        (2.0, 0.7, 1.0),    # Octave
        (2.4, 0.5, 1.2),    # Minor third above octave
        (3.0, 0.4, 0.9),    # Twelfth
        (4.0, 0.3, 1.1),    # Double octave
        (5.0, 0.2, 1.3),    # Higher partial
        (6.3, 0.15, 1.5),   # Upper bell tone
    ]

    for ratio, amp, decay_rate in partials:
        partial_freq = freq * ratio

        if partial_freq < SAMPLE_RATE / 2:
            # Each partial has own decay rate
            partial_env = np.exp(-t * decay_rate)

            # Add slight beating via detuning
            detune = 1 + 0.002 * np.sin(2 * np.pi * 0.5 * t)

            partial = np.sin(2 * np.pi * partial_freq * detune * t) * amp * partial_env
            output += partial

    # Strike transient
    strike = np.random.randn(len(t)) * 0.1
    strike *= np.exp(-t * 40)
    output += strike

    return output / (np.max(np.abs(output)) + 1e-10)


def glockenspiel(freq: float, duration: float = 1.5) -> np.ndarray:
    """
    Glockenspiel / music box.

    Bright, metallic, shorter decay than bells.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Simple FM with 1:3 ratio for metallic brightness
    index = 5 * np.exp(-t * 8)
    mod = np.sin(2 * np.pi * freq * 3 * t)
    carrier = np.sin(2 * np.pi * freq * t + index * mod)

    # Add octave for brightness
    octave = np.sin(2 * np.pi * freq * 2 * t) * 0.4 * np.exp(-t * 4)

    output = carrier + octave

    # Quick decay
    amp = np.exp(-t * 3)
    output *= amp

    return output / (np.max(np.abs(output)) + 1e-10)


def vibraphone(freq: float, duration: float = 2.0,
               vibrato: bool = True) -> np.ndarray:
    """
    Vibraphone with optional motor vibrato.

    Warmer than glockenspiel, characteristic tremolo.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # FM with lower index for warmer sound
    index = 3 * np.exp(-t * 2)
    mod = np.sin(2 * np.pi * freq * 2 * t)
    carrier = np.sin(2 * np.pi * freq * t + index * mod)

    # Vibrato from rotating discs
    if vibrato:
        vib_rate = 5  # Hz
        vib_depth = 0.3
        tremolo = 1 + vib_depth * np.sin(2 * np.pi * vib_rate * t)
        carrier *= tremolo

    # Mellow decay
    amp = np.exp(-t * 1.5)
    output = carrier * amp

    return output / (np.max(np.abs(output)) + 1e-10)


def wind_chime(base_freq: float, duration: float = 3.0,
               num_chimes: int = 5) -> np.ndarray:
    """
    Wind chime cluster - multiple random bells.

    Creates ambient, random bell texture.
    """
    output = np.zeros(int(SAMPLE_RATE * duration))

    # Random chime hits
    np.random.seed(42)  # For reproducibility

    for i in range(num_chimes):
        # Random timing
        start_time = np.random.rand() * (duration - 1.5)
        start_sample = int(start_time * SAMPLE_RATE)

        # Random frequency (pentatonic for pleasant sound)
        scale_ratios = [1, 1.25, 1.5, 1.875, 2.0]  # Major pentatonic
        freq = base_freq * np.random.choice(scale_ratios) * (2 ** np.random.randint(0, 2))

        # Generate chime
        chime_duration = 1.5 + np.random.rand()
        chime = glockenspiel(freq, chime_duration)
        chime *= 0.3 + np.random.rand() * 0.4  # Random volume

        # Add to output
        end_sample = min(start_sample + len(chime), len(output))
        output[start_sample:end_sample] += chime[:end_sample - start_sample]

    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("generated/sounds/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Bell notes (pitched bells usually in upper register)
    notes = {
        'C4': 261.63,
        'E4': 329.63,
        'G4': 392.0,
        'C5': 523.25,
        'G5': 783.99,
    }

    for name, freq in notes.items():
        note = name.lower()

        # Tubular bell
        audio = tubular_bell(freq, 4.0)
        sf.write(output_dir / f"bell_tubular_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Church bell (only lower notes)
        if freq < 400:
            audio = church_bell(freq, 6.0)
            sf.write(output_dir / f"bell_church_{note}.wav",
                     audio, SAMPLE_RATE, subtype='PCM_16')

        # Glockenspiel
        audio = glockenspiel(freq, 2.0)
        sf.write(output_dir / f"glockenspiel_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Vibraphone
        audio = vibraphone(freq, 3.0, vibrato=True)
        sf.write(output_dir / f"vibraphone_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    # Wind chimes (ambient)
    audio = wind_chime(523.25, 8.0, num_chimes=12)
    sf.write(output_dir / "wind_chimes.wav", audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated bell samples in {output_dir}")


if __name__ == "__main__":
    main()
