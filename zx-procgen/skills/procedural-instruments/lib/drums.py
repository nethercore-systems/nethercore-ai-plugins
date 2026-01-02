"""
Drum Synthesis Primitives

Low-level building blocks for synthesizing drum sounds. These are PRIMITIVES,
not complete instruments. The LLM should compose these to create actual drums.

For example implementations, see: references/drum-examples.py
"""

import numpy as np
from scipy.signal import butter, lfilter
from typing import Tuple

SAMPLE_RATE = 22050


# =============================================================================
# EXCITATION SOURCES
# =============================================================================

def noise_burst(
    duration: float,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate a burst of white noise for drum transients.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Noise burst signal
    """
    num_samples = int(sample_rate * duration)
    return np.random.randn(num_samples)


def pitched_body(
    duration: float,
    start_freq: float,
    end_freq: float,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate a pitched sine body with frequency envelope (pitch drop).

    Common in kicks, toms, and some snares.

    Args:
        duration: Duration in seconds
        start_freq: Starting frequency in Hz
        end_freq: Ending frequency in Hz
        sample_rate: Sample rate

    Returns:
        Pitched body signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Exponential frequency envelope
    freq = end_freq + (start_freq - end_freq) * np.exp(-t * 30)

    # Integrate frequency to get phase
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    return np.sin(phase)


def metallic_partials(
    duration: float,
    base_freq: float,
    num_partials: int = 6,
    inharmonicity: float = 1.414,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate inharmonic partials for metallic sounds (cymbals, bells).

    Args:
        duration: Duration in seconds
        base_freq: Base frequency in Hz
        num_partials: Number of partials to generate
        inharmonicity: Ratio between partials (1.414 = sqrt(2) for cymbals)
        sample_rate: Sample rate

    Returns:
        Metallic partials signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)
    output = np.zeros(num_samples)

    for i in range(num_partials):
        freq = base_freq * (inharmonicity ** i)
        if freq < sample_rate / 2:  # Nyquist check
            amp = 1.0 / (i + 1)  # Decreasing amplitude
            output += np.sin(2 * np.pi * freq * t) * amp

    return output


# =============================================================================
# ENVELOPES
# =============================================================================

def percussive_envelope(
    t: np.ndarray,
    attack: float = 0.001,
    decay: float = 0.1
) -> np.ndarray:
    """
    Generate a percussive envelope (fast attack, exponential decay).

    Args:
        t: Time array in seconds
        attack: Attack time in seconds
        decay: Decay time constant in seconds

    Returns:
        Envelope array (0-1)
    """
    attack_env = 1 - np.exp(-t / attack)
    decay_env = np.exp(-t / decay)
    return attack_env * decay_env


def two_stage_decay(
    t: np.ndarray,
    fast_decay: float = 0.05,
    slow_decay: float = 0.3,
    crossover: float = 0.5
) -> np.ndarray:
    """
    Two-stage decay envelope (fast initial, slow tail).

    Useful for snares, toms with sustain.

    Args:
        t: Time array in seconds
        fast_decay: Initial fast decay constant
        slow_decay: Secondary slow decay constant
        crossover: Mix point between stages (0-1)

    Returns:
        Envelope array
    """
    fast = np.exp(-t / fast_decay)
    slow = np.exp(-t / slow_decay)
    return fast * crossover + slow * (1 - crossover)


# =============================================================================
# FILTERS (drum-specific)
# =============================================================================

def drum_lowpass(
    signal: np.ndarray,
    cutoff: float,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply lowpass filter optimized for drum sounds.

    Args:
        signal: Input signal
        cutoff: Cutoff frequency in Hz
        sample_rate: Sample rate

    Returns:
        Filtered signal
    """
    nyquist = sample_rate / 2
    normalized = min(cutoff / nyquist, 0.99)
    b, a = butter(2, normalized, btype='low')
    return lfilter(b, a, signal)


def drum_bandpass(
    signal: np.ndarray,
    low_cutoff: float,
    high_cutoff: float,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply bandpass filter for isolating drum frequency ranges.

    Args:
        signal: Input signal
        low_cutoff: Low cutoff frequency in Hz
        high_cutoff: High cutoff frequency in Hz
        sample_rate: Sample rate

    Returns:
        Filtered signal
    """
    nyquist = sample_rate / 2
    low = max(0.01, min(low_cutoff / nyquist, 0.99))
    high = max(0.01, min(high_cutoff / nyquist, 0.99))
    if low >= high:
        return signal
    b, a = butter(2, [low, high], btype='band')
    return lfilter(b, a, signal)


def drum_highpass(
    signal: np.ndarray,
    cutoff: float,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply highpass filter for bright drum transients.

    Args:
        signal: Input signal
        cutoff: Cutoff frequency in Hz
        sample_rate: Sample rate

    Returns:
        Filtered signal
    """
    nyquist = sample_rate / 2
    normalized = max(0.01, min(cutoff / nyquist, 0.99))
    b, a = butter(2, normalized, btype='high')
    return lfilter(b, a, signal)


# =============================================================================
# UTILITIES
# =============================================================================

def normalize_drum(signal: np.ndarray, peak: float = 0.9) -> np.ndarray:
    """
    Normalize drum signal to specified peak.

    Args:
        signal: Input signal
        peak: Target peak level (0-1)

    Returns:
        Normalized signal
    """
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        return signal / max_val * peak
    return signal


def layer_sounds(*signals: np.ndarray, normalize_output: bool = True) -> np.ndarray:
    """
    Layer multiple drum components together.

    Args:
        *signals: Variable number of signals to layer
        normalize_output: Whether to normalize the result

    Returns:
        Layered signal
    """
    if not signals:
        return np.array([])

    # Pad to same length
    max_len = max(len(s) for s in signals)
    padded = [np.pad(s, (0, max_len - len(s))) for s in signals]

    output = sum(padded)

    if normalize_output:
        return normalize_drum(output)
    return output
