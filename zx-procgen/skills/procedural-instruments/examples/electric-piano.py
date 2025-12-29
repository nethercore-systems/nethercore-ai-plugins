#!/usr/bin/env python3
"""
Electric Piano - FM Synthesis (DX7-style Rhodes)

Generates classic electric piano sounds using frequency modulation.
The iconic bell-like attack with warm sustain.
"""
import numpy as np
import soundfile as sf
from pathlib import Path

SAMPLE_RATE = 22050


def fm_operator(freq: float, t: np.ndarray, index: np.ndarray,
                modulator: np.ndarray | None = None) -> np.ndarray:
    """Single FM operator with optional modulation input."""
    phase = 2 * np.pi * freq * t
    if modulator is not None:
        phase = phase + index * modulator
    return np.sin(phase)


def rhodes_piano(freq: float, duration: float = 1.5,
                 velocity: float = 0.8) -> np.ndarray:
    """
    DX7-style Rhodes electric piano.

    Uses 2-operator FM with 1:1 ratio and decaying index.
    The key is the rapidly decaying modulation index creating
    the characteristic bell-like attack that mellows into warmth.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Velocity affects brightness (modulation index)
    base_index = 3.0 + velocity * 3.0  # 3-6 based on velocity

    # FM modulation index envelope: fast decay for bell attack
    index_env = base_index * np.exp(-t * 8)

    # Add slight second peak for "tine" character
    tine_peak = 2.0 * np.exp(-((t - 0.02) ** 2) / 0.001)
    index_env = index_env + tine_peak * velocity

    # Modulator (1:1 ratio with carrier)
    mod = np.sin(2 * np.pi * freq * t)

    # Carrier with FM
    carrier = np.sin(2 * np.pi * freq * t + index_env * mod)

    # Second harmonic for body (subtle)
    harm2 = np.sin(2 * np.pi * freq * 2 * t) * 0.15
    harm2_env = np.exp(-t * 4)

    # Amplitude envelope: quick attack, gradual decay
    attack_time = 0.005
    attack = 1 - np.exp(-t / attack_time * 5)
    decay = np.exp(-t * (1.0 + (1 - velocity) * 2))  # Softer = quicker decay
    amp_env = attack * decay

    # Combine
    output = (carrier + harm2 * harm2_env) * amp_env

    return output / (np.max(np.abs(output)) + 1e-10)


def wurlitzer(freq: float, duration: float = 1.5,
              velocity: float = 0.8) -> np.ndarray:
    """
    Wurlitzer-style electric piano.

    Brighter and more "reedy" than Rhodes, with prominent harmonics.
    Uses asymmetric FM for more harmonic content.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Higher base index for brighter sound
    base_index = 4.0 + velocity * 4.0

    # Two-stage decay for wurli character
    index_env = base_index * (0.7 * np.exp(-t * 12) + 0.3 * np.exp(-t * 3))

    # Modulator at 1:1
    mod = np.sin(2 * np.pi * freq * t)

    # Carrier with FM
    carrier = np.sin(2 * np.pi * freq * t + index_env * mod)

    # Add growl with slightly detuned second carrier
    growl_index = base_index * 0.5 * np.exp(-t * 6)
    growl = np.sin(2 * np.pi * freq * 1.01 * t + growl_index * mod) * 0.2

    # Odd harmonics for reedy quality
    harm3 = np.sin(2 * np.pi * freq * 3 * t) * 0.08 * np.exp(-t * 5)

    # Amplitude envelope
    attack = 1 - np.exp(-t * 200)
    decay = np.exp(-t * 2)
    amp_env = attack * decay

    output = (carrier + growl + harm3) * amp_env

    return output / (np.max(np.abs(output)) + 1e-10)


def generate_chromatic_samples(generator_func, name: str,
                               output_dir: Path, octaves: list[int] = [3, 4, 5]):
    """Generate samples across multiple octaves."""
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    base_freqs = [261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 493.88]

    for octave in octaves:
        for note, base_freq in zip(notes, base_freqs):
            # Adjust for octave (C4 = 261.63)
            freq = base_freq * (2 ** (octave - 4))
            note_name = f"{note}{octave}".lower()

            # Generate at different velocities for expression
            for vel_name, velocity in [('soft', 0.4), ('medium', 0.7), ('hard', 1.0)]:
                audio = generator_func(freq, 2.0, velocity)
                filename = f"{name}_{note_name}_{vel_name}.wav"
                sf.write(output_dir / filename, audio, SAMPLE_RATE, subtype='PCM_16')


def main():
    output_dir = Path("assets/audio/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate Rhodes samples
    print("Generating Rhodes electric piano...")
    generate_chromatic_samples(rhodes_piano, "rhodes", output_dir)

    # Generate Wurlitzer samples
    print("Generating Wurlitzer electric piano...")
    generate_chromatic_samples(wurlitzer, "wurli", output_dir)

    # Quick single-note demos
    for freq, name in [(261.63, 'c4'), (440.0, 'a4')]:
        sf.write(output_dir / f"epiano_demo_{name}.wav",
                 rhodes_piano(freq, 3.0, 0.8), SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated electric piano samples in {output_dir}")


if __name__ == "__main__":
    main()
