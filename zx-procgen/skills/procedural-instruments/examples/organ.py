#!/usr/bin/env python3
"""
Organ - Additive Synthesis with Drawbars

Hammond-style organ with tonewheel character and key click.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pathlib import Path

SAMPLE_RATE = 22050

# Hammond drawbar footage to harmonic ratios
# 16', 5-1/3', 8', 4', 2-2/3', 2', 1-3/5', 1-1/3', 1'
DRAWBAR_HARMONICS = [0.5, 1.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]

# Classic drawbar presets
PRESETS = {
    'full': '888888888',       # All drawbars full
    'jazz': '838000000',       # Classic jazz
    'gospel': '888800000',     # Gospel/blues
    'rock': '888888800',       # Rock organ
    'cathedral': '868000468',  # Pipe organ feel
    'jimmy': '888000000',      # Jimmy Smith style
    'booker': '888630000',     # Booker T style
}


def drawbar_organ(freq: float, duration: float = 1.0,
                  drawbars: str = '888888888') -> np.ndarray:
    """
    Hammond-style drawbar organ.

    Args:
        drawbars: 9-digit string, each 0-8 for drawbar level
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    # Parse drawbar settings
    for i, char in enumerate(drawbars[:9]):
        level = int(char) / 8.0
        if level > 0:
            harm_ratio = DRAWBAR_HARMONICS[i]
            harm_freq = freq * harm_ratio

            # Skip if above Nyquist
            if harm_freq < SAMPLE_RATE / 2:
                output += np.sin(2 * np.pi * harm_freq * t) * level

    return output


def tonewheel_character(signal: np.ndarray) -> np.ndarray:
    """
    Add Hammond tonewheel artifacts for authenticity.

    Real Hammond organs have slight crosstalk and phase wobble.
    """
    # Slight amplitude wobble (tonewheel wow)
    t = np.linspace(0, len(signal) / SAMPLE_RATE, len(signal))
    wow = 1 + 0.003 * np.sin(2 * np.pi * 0.5 * t)  # Very subtle

    # Add very faint crosstalk noise
    noise = np.random.randn(len(signal)) * 0.005

    return signal * wow + noise


def key_click(duration: float, intensity: float = 0.5) -> np.ndarray:
    """
    Generate Hammond key click - the distinctive attack.

    The click comes from all tonewheels briefly connecting.
    """
    click_samples = int(SAMPLE_RATE * 0.012)  # ~12ms click
    full_samples = int(SAMPLE_RATE * duration)

    click = np.zeros(full_samples)

    # Click is burst of harmonics
    t_click = np.linspace(0, 0.012, click_samples)
    for freq in [800, 1600, 2400, 3200, 4800]:
        click[:click_samples] += np.sin(2 * np.pi * freq * t_click) * 0.1

    # Shape with fast decay
    click[:click_samples] *= np.exp(-t_click * 300) * intensity

    return click


def hammond_organ(freq: float, duration: float = 1.0,
                  preset: str = 'full',
                  click: bool = True,
                  leslie: bool = False) -> np.ndarray:
    """
    Complete Hammond organ with optional effects.

    Args:
        preset: Drawbar preset name or 9-digit string
        click: Add key click
        leslie: Add Leslie speaker simulation (rotary)
    """
    # Get drawbar setting
    if preset in PRESETS:
        drawbars = PRESETS[preset]
    else:
        drawbars = preset

    # Generate base organ tone
    output = drawbar_organ(freq, duration, drawbars)

    # Add tonewheel character
    output = tonewheel_character(output)

    # Add key click
    if click:
        output += key_click(duration, 0.6)

    # Leslie speaker effect (simplified)
    if leslie:
        output = leslie_effect(output)

    # Amplitude envelope (organ has instant attack/release typically)
    t = np.linspace(0, duration, len(output))
    # Slight attack to avoid click
    attack = np.minimum(t * 200, 1.0)
    # Quick release at end
    release_time = min(0.05, duration * 0.1)
    release = np.where(t > duration - release_time,
                       (duration - t) / release_time, 1.0)
    env = attack * release

    output *= env

    return output / (np.max(np.abs(output)) + 1e-10)


def leslie_effect(signal: np.ndarray, speed: str = 'slow') -> np.ndarray:
    """
    Simplified Leslie rotary speaker effect.

    Real Leslie has separate horn and drum at different speeds.
    This is a simplified single-rotor approximation.
    """
    t = np.linspace(0, len(signal) / SAMPLE_RATE, len(signal))

    # Rotation speed
    if speed == 'slow':
        rate = 0.8  # Hz
    elif speed == 'fast':
        rate = 6.0  # Hz
    else:
        rate = 3.0  # chorale

    # Amplitude modulation (volume varies as speaker rotates)
    am = 1 + 0.3 * np.sin(2 * np.pi * rate * t)

    # Frequency modulation (Doppler effect)
    # This is simplified - real implementation would need pitch shifting
    fm = np.sin(2 * np.pi * rate * t + np.pi / 2) * 0.002

    # Apply (AM only for simplicity, FM requires more complex processing)
    output = signal * am

    # Add slight chorus for width
    delay_samples = int(0.003 * SAMPLE_RATE)  # 3ms
    delayed = np.zeros_like(output)
    delayed[delay_samples:] = signal[:-delay_samples] * 0.3
    output += delayed

    return output


def pipe_organ(freq: float, duration: float = 2.0,
               stops: list[str] = ['principal', 'flute']) -> np.ndarray:
    """
    Pipe organ approximation with different stops.

    Stops:
    - principal: Standard pipe sound
    - flute: Softer, rounder
    - reed: Brighter, more buzz
    - mixture: Multiple high harmonics
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    for stop in stops:
        if stop == 'principal':
            # Rich harmonic content
            for h in range(1, 8):
                amp = 1.0 / h
                output += np.sin(2 * np.pi * freq * h * t) * amp
        elif stop == 'flute':
            # Mostly fundamental, soft
            output += np.sin(2 * np.pi * freq * t) * 0.8
            output += np.sin(2 * np.pi * freq * 2 * t) * 0.1
        elif stop == 'reed':
            # Bright, saw-like
            for h in range(1, 12):
                amp = 1.0 / h
                output += np.sin(2 * np.pi * freq * h * t) * amp
        elif stop == 'mixture':
            # High harmonics (mutation stops)
            for h in [2, 3, 4, 5, 6, 8]:
                output += np.sin(2 * np.pi * freq * h * t) * 0.3

    # Pipe organ has slow attack (wind filling pipe)
    attack = 1 - np.exp(-t * 5)

    # Add subtle air noise
    noise = np.random.randn(len(t)) * 0.01
    noise *= np.exp(-t * 10)

    output = output * attack + noise

    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("generated/sounds/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    notes = {
        'C3': 130.81,
        'G3': 196.0,
        'C4': 261.63,
        'G4': 392.0,
    }

    for name, freq in notes.items():
        note = name.lower()

        # Hammond presets
        for preset_name in ['full', 'jazz', 'gospel', 'rock']:
            audio = hammond_organ(freq, 2.0, preset=preset_name)
            sf.write(output_dir / f"organ_hammond_{preset_name}_{note}.wav",
                     audio, SAMPLE_RATE, subtype='PCM_16')

        # Hammond with Leslie
        audio = hammond_organ(freq, 3.0, preset='full', leslie=True)
        sf.write(output_dir / f"organ_hammond_leslie_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Pipe organ
        audio = pipe_organ(freq, 3.0, stops=['principal', 'flute'])
        sf.write(output_dir / f"organ_pipe_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated organ samples in {output_dir}")


if __name__ == "__main__":
    main()
