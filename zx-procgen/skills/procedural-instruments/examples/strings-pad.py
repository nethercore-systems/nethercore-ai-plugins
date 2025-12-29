#!/usr/bin/env python3
"""
Strings/Pad - Wavetable Synthesis with Unison Detuning

Lush, evolving string ensemble and pad sounds.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pathlib import Path

SAMPLE_RATE = 22050


def create_wavetable(num_frames: int = 32, frame_size: int = 2048) -> np.ndarray:
    """
    Create morphing wavetable: sine -> triangle -> saw-ish.

    Each frame has progressively more harmonics.
    """
    table = np.zeros((num_frames, frame_size))
    t = np.linspace(0, 1, frame_size, endpoint=False)

    for f in range(num_frames):
        # Add harmonics progressively
        progress = f / (num_frames - 1)
        num_harmonics = 1 + int(progress * 12)

        for h in range(1, num_harmonics + 1):
            # Saw-like amplitude rolloff
            amp = 1.0 / h
            # Soften odd harmonics slightly for warmth
            if h % 2 == 1:
                amp *= 0.9
            table[f] += np.sin(2 * np.pi * h * t) * amp

        # Normalize each frame
        max_val = np.max(np.abs(table[f]))
        if max_val > 0:
            table[f] /= max_val

    return table


def wavetable_oscillator(freq: float, duration: float,
                         table: np.ndarray,
                         pos_start: float = 0.0,
                         pos_end: float = 0.5,
                         pos_speed: float = 1.0) -> np.ndarray:
    """Play through wavetable with position modulation."""
    num_samples = int(SAMPLE_RATE * duration)
    num_frames, frame_size = table.shape
    output = np.zeros(num_samples)

    phase = 0.0
    phase_inc = freq / SAMPLE_RATE

    for i in range(num_samples):
        t = i / num_samples

        # Position sweeps through wavetable
        pos = pos_start + (pos_end - pos_start) * (t ** pos_speed)

        # Interpolate between frames
        frame_f = pos * (num_frames - 1)
        frame_a = int(frame_f) % num_frames
        frame_b = (frame_a + 1) % num_frames
        blend = frame_f - int(frame_f)

        # Read from wavetable with linear interpolation
        idx_f = phase * frame_size
        idx_a = int(idx_f) % frame_size
        idx_b = (idx_a + 1) % frame_size
        frac = idx_f - int(idx_f)

        # Bilinear interpolation
        sample_aa = table[frame_a, idx_a]
        sample_ab = table[frame_a, idx_b]
        sample_ba = table[frame_b, idx_a]
        sample_bb = table[frame_b, idx_b]

        sample_a = sample_aa * (1 - frac) + sample_ab * frac
        sample_b = sample_ba * (1 - frac) + sample_bb * frac
        output[i] = sample_a * (1 - blend) + sample_b * blend

        phase += phase_inc
        if phase >= 1.0:
            phase -= 1.0

    return output


def string_ensemble(freq: float, duration: float = 3.0,
                    voices: int = 5, detune_cents: float = 8.0) -> np.ndarray:
    """
    Lush string ensemble with unison detuning.

    Multiple voices slightly detuned create the characteristic
    ensemble "shimmer".
    """
    table = create_wavetable()
    output = np.zeros(int(SAMPLE_RATE * duration))

    # Detune spread
    detune_spread = np.linspace(-detune_cents, detune_cents, voices)

    for i, cents in enumerate(detune_spread):
        detune_ratio = 2 ** (cents / 1200)
        voice_freq = freq * detune_ratio

        # Slight position variation per voice
        pos_offset = i * 0.05
        voice = wavetable_oscillator(
            voice_freq, duration, table,
            pos_start=0.1 + pos_offset,
            pos_end=0.5 + pos_offset,
            pos_speed=0.8
        )
        output[:len(voice)] += voice / voices

    # Slow attack, long release
    t = np.linspace(0, duration, len(output))
    attack = 1 - np.exp(-t * 2)  # ~500ms attack
    release_start = duration - 0.5
    release = np.where(t > release_start,
                       np.exp(-(t - release_start) * 4), 1.0)
    env = attack * release

    output *= env

    # Gentle low-pass for warmth
    b, a = butter(2, 3000 / (SAMPLE_RATE / 2), btype='low')
    output = lfilter(b, a, output)

    return output / (np.max(np.abs(output)) + 1e-10)


def synth_pad(freq: float, duration: float = 4.0,
              brightness: float = 0.5,
              movement: float = 0.5) -> np.ndarray:
    """
    Evolving synth pad with modulation.

    Args:
        brightness: 0-1, how far into wavetable to go
        movement: 0-1, how much the timbre evolves
    """
    table = create_wavetable()
    output = np.zeros(int(SAMPLE_RATE * duration))

    # 7 detuned voices for maximum width
    detune_cents = [-12, -7, -3, 0, 3, 7, 12]

    for cents in detune_cents:
        detune_ratio = 2 ** (cents / 1200)
        voice = wavetable_oscillator(
            freq * detune_ratio, duration, table,
            pos_start=brightness * 0.3,
            pos_end=brightness * 0.3 + movement * 0.4,
            pos_speed=0.7
        )
        output[:len(voice)] += voice / 7

    # Very slow attack for pad character
    t = np.linspace(0, duration, len(output))
    attack = 1 - np.exp(-t * 0.8)  # ~1.25s attack
    decay = np.exp(-t * 0.2)  # Slow decay
    env = attack * decay

    output *= env

    # Add subtle chorus-like effect via pitch modulation
    # (already achieved through detuning, but could add LFO here)

    # Low-pass based on brightness
    cutoff = 1000 + brightness * 3000
    b, a = butter(2, cutoff / (SAMPLE_RATE / 2), btype='low')
    output = lfilter(b, a, output)

    return output / (np.max(np.abs(output)) + 1e-10)


def glass_pad(freq: float, duration: float = 4.0) -> np.ndarray:
    """
    Crystalline glass-like pad.

    High harmonics with slow attack, ethereal quality.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Additive synthesis with high harmonics
    output = np.zeros_like(t)
    harmonics = [1, 2, 3, 4, 5, 7, 9, 11, 13]
    amps = [1.0, 0.5, 0.3, 0.4, 0.2, 0.15, 0.1, 0.08, 0.05]

    for harm, amp in zip(harmonics, amps):
        # Each harmonic has slightly different envelope
        harm_env = (1 - np.exp(-t * (1 + harm * 0.1))) * np.exp(-t * (0.1 + harm * 0.02))
        output += np.sin(2 * np.pi * freq * harm * t) * amp * harm_env

    # Detuned layer for width
    for cents in [-5, 5]:
        ratio = 2 ** (cents / 1200)
        layer = np.sin(2 * np.pi * freq * ratio * t) * 0.3
        output += layer

    # Overall envelope
    env = (1 - np.exp(-t * 0.5)) * np.exp(-t * 0.15)
    output *= env

    return output / (np.max(np.abs(output)) + 1e-10)


def main():
    output_dir = Path("assets/audio/instruments")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate at common chord frequencies
    notes = {
        'C3': 130.81,
        'E3': 164.81,
        'G3': 196.0,
        'C4': 261.63,
        'E4': 329.63,
        'G4': 392.0,
    }

    for name, freq in notes.items():
        note = name.lower()

        # String ensemble
        audio = string_ensemble(freq, 4.0)
        sf.write(output_dir / f"strings_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Warm pad
        audio = synth_pad(freq, 5.0, brightness=0.3, movement=0.4)
        sf.write(output_dir / f"pad_warm_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Bright pad
        audio = synth_pad(freq, 5.0, brightness=0.7, movement=0.6)
        sf.write(output_dir / f"pad_bright_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

        # Glass pad
        audio = glass_pad(freq, 5.0)
        sf.write(output_dir / f"pad_glass_{note}.wav",
                 audio, SAMPLE_RATE, subtype='PCM_16')

    print(f"Generated strings/pad samples in {output_dir}")


if __name__ == "__main__":
    main()
