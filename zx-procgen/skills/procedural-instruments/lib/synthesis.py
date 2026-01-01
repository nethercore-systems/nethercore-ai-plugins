"""
Core Synthesis Primitives

Low-level building blocks for audio synthesis. These are PRIMITIVES,
not complete instruments. The LLM should compose these to create actual instruments.

Provides:
- ADSR and multi-stage envelopes
- FM (Frequency Modulation) operators
- Karplus-Strong physical modeling
- Vibrato and pitch modulation
- Attack transients

For example implementations, see: examples/*.py
"""

import numpy as np
from scipy.signal import butter, lfilter
from typing import List, Tuple

SAMPLE_RATE = 22050


# =============================================================================
# ENVELOPES
# =============================================================================

def adsr_envelope(
    t: np.ndarray,
    attack: float = 0.01,
    decay: float = 0.1,
    sustain: float = 0.7,
    release: float = 0.2,
    sustain_time: float = 0.0
) -> np.ndarray:
    """
    Generate ADSR (Attack-Decay-Sustain-Release) envelope.

    Args:
        t: Time array in seconds
        attack: Attack time in seconds
        decay: Decay time in seconds
        sustain: Sustain level (0-1)
        release: Release time in seconds
        sustain_time: Time to hold sustain (0 = until end)

    Returns:
        Envelope array (0-1)
    """
    env = np.zeros_like(t)
    duration = t[-1]

    # Calculate phase boundaries
    attack_end = attack
    decay_end = attack_end + decay

    if sustain_time > 0:
        sustain_end = decay_end + sustain_time
        release_start = sustain_end
    else:
        # Sustain fills remaining time minus release
        release_start = max(decay_end, duration - release)

    for i, time in enumerate(t):
        if time < attack_end:
            # Attack phase: ramp up
            env[i] = time / attack if attack > 0 else 1.0
        elif time < decay_end:
            # Decay phase: exponential decay to sustain
            decay_progress = (time - attack_end) / decay if decay > 0 else 1.0
            env[i] = 1.0 - (1.0 - sustain) * decay_progress
        elif time < release_start:
            # Sustain phase
            env[i] = sustain
        else:
            # Release phase: decay to zero
            release_progress = (time - release_start) / release if release > 0 else 1.0
            env[i] = sustain * (1.0 - min(1.0, release_progress))

    return env


def multi_envelope(
    t: np.ndarray,
    segments: List[Tuple[float, float, str]]
) -> np.ndarray:
    """
    Generate multi-stage envelope with arbitrary segments.

    Real instruments don't follow simple ADSR - use this for complex envelopes.

    Args:
        t: Time array in seconds
        segments: List of (duration, target_level, curve_type) tuples
                  curve_type: 'linear', 'exp', 'log'

    Returns:
        Envelope array

    Example:
        # Piano-like: quick attack, complex decay
        segments = [
            (0.01, 1.0, 'linear'),   # Attack
            (0.05, 0.8, 'exp'),      # Initial decay
            (0.2, 0.6, 'exp'),       # Secondary decay
            (1.0, 0.0, 'exp'),       # Long tail
        ]
    """
    env = np.zeros_like(t)
    current_time = 0.0
    current_level = 0.0

    for duration, target, curve in segments:
        mask = (t >= current_time) & (t < current_time + duration)
        local_t = (t[mask] - current_time) / duration if duration > 0 else np.ones_like(t[mask])
        local_t = np.clip(local_t, 0, 1)

        if curve == 'exp':
            # Exponential curve (fast start, slow end)
            env[mask] = current_level + (target - current_level) * (1 - np.exp(-5 * local_t))
        elif curve == 'log':
            # Logarithmic curve (slow start, fast end)
            env[mask] = current_level + (target - current_level) * (np.log(1 + 9 * local_t) / np.log(10))
        else:  # linear
            env[mask] = current_level + (target - current_level) * local_t

        current_time += duration
        current_level = target

    # Fill remaining time with final level
    env[t >= current_time] = current_level

    return env


# =============================================================================
# FM SYNTHESIS
# =============================================================================

def fm_operator(
    freq: float,
    t: np.ndarray,
    index: np.ndarray | float = 0.0,
    modulator: np.ndarray | None = None
) -> np.ndarray:
    """
    Single FM operator with optional modulation input.

    Args:
        freq: Carrier frequency in Hz
        t: Time array in seconds
        index: Modulation index (depth). Can be array for time-varying modulation.
        modulator: Modulator signal (optional)

    Returns:
        Carrier signal with FM applied

    Example:
        # DX7-style Rhodes piano
        t = np.linspace(0, 1.0, 22050)
        mod = np.sin(2 * np.pi * freq * t)  # 1:1 ratio modulator
        index = 5.0 * np.exp(-t * 8)        # Decaying modulation index
        carrier = fm_operator(freq, t, index, mod)
    """
    phase = 2 * np.pi * freq * t
    if modulator is not None:
        phase = phase + index * modulator
    return np.sin(phase)


# =============================================================================
# KARPLUS-STRONG (Physical Modeling)
# =============================================================================

def karplus_strong(
    freq: float,
    duration: float = 1.0,
    damping: float = 0.996,
    brightness: float = 0.7,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Karplus-Strong algorithm for plucked string synthesis.

    Physical modeling approach: feedback delay line with lowpass averaging.

    Args:
        freq: Note frequency in Hz
        duration: Duration in seconds
        damping: Decay rate (0.99-0.999, higher = longer sustain)
        brightness: Initial pluck brightness (0-1)
        sample_rate: Sample rate

    Returns:
        Plucked string audio signal

    Example:
        # Acoustic guitar
        audio = karplus_strong(440.0, 2.0, damping=0.996, brightness=0.75)

        # Nylon guitar (warmer)
        audio = karplus_strong(440.0, 2.0, damping=0.994, brightness=0.45)

        # Bass guitar
        audio = karplus_strong(110.0, 2.0, damping=0.998, brightness=0.6)
    """
    num_samples = int(sample_rate * duration)
    delay_length = max(2, int(sample_rate / freq))

    # Initialize with filtered noise (the "pluck" excitation)
    noise = np.random.randn(delay_length)

    # Filter initial noise based on brightness
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


# =============================================================================
# MODULATION
# =============================================================================

def apply_vibrato(
    signal: np.ndarray,
    t: np.ndarray,
    rate: float = 5.0,
    depth: float = 0.02,
    delay: float = 0.2
) -> np.ndarray:
    """
    Apply vibrato (pitch modulation) to a signal.

    Note: This applies amplitude-based vibrato simulation. For true pitch
    vibrato on synthesized signals, modulate the frequency during synthesis.

    Args:
        signal: Input audio signal
        t: Time array in seconds
        rate: Vibrato rate in Hz (typically 4-7 Hz)
        depth: Vibrato depth (0-0.1 typical)
        delay: Delay before vibrato starts (seconds)

    Returns:
        Signal with vibrato applied
    """
    vibrato_env = np.clip((t - delay) / 0.1, 0, 1)
    vibrato = np.sin(2 * np.pi * rate * t) * depth * vibrato_env

    # Apply as amplitude modulation (approximation)
    return signal * (1 + vibrato)


def attack_transient(
    t: np.ndarray,
    attack_duration: float = 0.02,
    noise_amount: float = 0.3
) -> np.ndarray:
    """
    Generate attack transient noise for realistic instrument attacks.

    Real instruments have complex transients at note onset.

    Args:
        t: Time array in seconds
        attack_duration: Duration of transient in seconds
        noise_amount: Amount of noise (0-1)

    Returns:
        Attack transient signal to add to main signal
    """
    noise = np.random.randn(len(t)) * noise_amount
    attack_env = np.exp(-t / attack_duration * 10)
    return noise * attack_env
