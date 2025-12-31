"""
Basic Waveform Generators

Provides fundamental oscillator waveforms for synthesis:
- Sine, square, sawtooth, triangle
- White, pink, and brown noise
- 8-bit and 16-bit output formats for tracker modules
"""

import numpy as np
import struct
from typing import Literal

SAMPLE_RATE = 22050


# =============================================================================
# OSCILLATORS
# =============================================================================

def sine_wave(
    freq: float,
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    phase: float = 0.0
) -> np.ndarray:
    """
    Generate pure sine wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate
        phase: Initial phase in radians

    Returns:
        Sine wave signal (-1 to 1)
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * freq * t + phase)


def square_wave(
    freq: float,
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    duty: float = 0.5
) -> np.ndarray:
    """
    Generate square/pulse wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate
        duty: Duty cycle (0-1), 0.5 = pure square

    Returns:
        Square wave signal (-1 to 1)
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    phase = (freq * t) % 1.0
    return np.where(phase < duty, 1.0, -1.0).astype(np.float32)


def saw_wave(
    freq: float,
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    antialiased: bool = True
) -> np.ndarray:
    """
    Generate sawtooth wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate
        antialiased: Use additive synthesis to reduce aliasing

    Returns:
        Sawtooth wave signal (-1 to 1)
    """
    t = np.linspace(0, duration, int(sample_rate * duration))

    if antialiased:
        # Band-limited sawtooth via additive synthesis
        output = np.zeros_like(t)
        num_harmonics = min(20, int(sample_rate / 2 / freq))

        for h in range(1, num_harmonics + 1):
            output += np.sin(2 * np.pi * freq * h * t) * (1.0 / h)

        return (output * 2 / np.pi).astype(np.float32)
    else:
        # Simple sawtooth (may alias at high frequencies)
        phase = (freq * t) % 1.0
        return (2 * phase - 1).astype(np.float32)


def triangle_wave(
    freq: float,
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate triangle wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Triangle wave signal (-1 to 1)
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    phase = (freq * t) % 1.0
    # Triangle: ramp up to 0.5, ramp down from 0.5 to 1
    return (4 * np.abs(phase - 0.5) - 1).astype(np.float32)


# =============================================================================
# NOISE GENERATORS
# =============================================================================

def white_noise(
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate white noise (flat frequency spectrum).

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        White noise signal (-1 to 1)
    """
    num_samples = int(sample_rate * duration)
    return np.random.randn(num_samples).astype(np.float32)


def pink_noise(
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate pink noise (1/f spectrum, equal power per octave).

    Useful for natural-sounding textures and drum transients.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Pink noise signal (normalized to approximately -1 to 1)
    """
    num_samples = int(sample_rate * duration)
    white = np.random.randn(num_samples)

    # Apply 1/sqrt(f) filter in frequency domain
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(num_samples)
    freqs[0] = 1  # Avoid division by zero
    fft = fft / np.sqrt(freqs)

    pink = np.fft.irfft(fft, num_samples)
    return (pink / (np.max(np.abs(pink)) + 1e-10)).astype(np.float32)


def brown_noise(
    duration: float = 1.0,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Generate brown/red noise (1/f^2 spectrum, random walk).

    Deep, rumbling character. Good for explosions and thunder.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Brown noise signal (normalized to approximately -1 to 1)
    """
    num_samples = int(sample_rate * duration)
    white = np.random.randn(num_samples)
    brown = np.cumsum(white)
    brown -= np.mean(brown)
    return (brown / (np.max(np.abs(brown)) + 1e-10)).astype(np.float32)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def normalize(signal: np.ndarray, peak: float = 0.9) -> np.ndarray:
    """
    Normalize signal to specified peak level.

    Args:
        signal: Input audio signal
        peak: Target peak level (0-1)

    Returns:
        Normalized signal
    """
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        return signal / max_val * peak
    return signal


def mix_signals(*signals: np.ndarray, normalize_output: bool = True) -> np.ndarray:
    """
    Mix multiple signals together.

    Args:
        *signals: Variable number of audio signals (same length)
        normalize_output: Whether to normalize the result

    Returns:
        Mixed signal
    """
    if not signals:
        return np.array([])

    # Ensure all same length
    min_len = min(len(s) for s in signals)
    mixed = sum(s[:min_len] for s in signals) / len(signals)

    if normalize_output:
        return normalize(mixed)
    return mixed


# =============================================================================
# TRACKER-COMPATIBLE OUTPUT
# =============================================================================

def to_8bit_pcm(signal: np.ndarray) -> bytes:
    """
    Convert float signal to 8-bit signed PCM for XM/IT trackers.

    Args:
        signal: Audio signal (should be normalized to -1 to 1)

    Returns:
        8-bit signed PCM data as bytes
    """
    # Normalize if needed
    max_val = np.max(np.abs(signal))
    if max_val > 1.0:
        signal = signal / max_val

    # Convert to 8-bit signed (-128 to 127)
    samples = np.clip(signal * 127, -128, 127).astype(np.int8)
    return samples.tobytes()


def to_16bit_pcm(signal: np.ndarray) -> bytes:
    """
    Convert float signal to 16-bit signed PCM for XM/IT trackers.

    Args:
        signal: Audio signal (should be normalized to -1 to 1)

    Returns:
        16-bit signed little-endian PCM data as bytes
    """
    # Normalize if needed
    max_val = np.max(np.abs(signal))
    if max_val > 1.0:
        signal = signal / max_val

    # Convert to 16-bit signed (-32768 to 32767)
    samples = np.clip(signal * 32767, -32768, 32767).astype(np.int16)
    return samples.tobytes()


def generate_looping_sample(
    generator_func,
    freq: float = 440.0,
    duration: float = 0.5,
    sample_rate: int = SAMPLE_RATE,
    bits: Literal[8, 16] = 16
) -> tuple[bytes, int]:
    """
    Generate a looping sample suitable for tracker instruments.

    Args:
        generator_func: Function that takes (freq, duration, sample_rate) and returns audio
        freq: Sample frequency in Hz
        duration: Sample duration in seconds
        sample_rate: Sample rate
        bits: Output bit depth (8 or 16)

    Returns:
        Tuple of (sample_data, loop_length)

    Example:
        data, loop_len = generate_looping_sample(
            lambda f, d, sr: sine_wave(f, d, sr),
            freq=440.0,
            duration=0.5
        )
    """
    signal = generator_func(freq, duration, sample_rate)

    if bits == 8:
        data = to_8bit_pcm(signal)
        loop_length = len(signal)
    else:
        data = to_16bit_pcm(signal)
        loop_length = len(signal)  # In samples, not bytes

    return data, loop_length
