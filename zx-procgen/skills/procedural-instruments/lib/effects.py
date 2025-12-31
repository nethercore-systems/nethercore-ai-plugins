"""
Audio Effects

Provides common audio processing effects:
- Filters (lowpass, highpass, bandpass, filter sweeps)
- Distortion and saturation
- Reverb and delay
- Normalization and dynamics
"""

import numpy as np
from scipy.signal import butter, lfilter, filtfilt
from typing import Literal

SAMPLE_RATE = 22050


# =============================================================================
# FILTERS
# =============================================================================

def lowpass_filter(
    signal: np.ndarray,
    cutoff: float,
    order: int = 2,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply lowpass filter to signal.

    Args:
        signal: Input audio signal
        cutoff: Cutoff frequency in Hz
        order: Filter order (higher = steeper rolloff)
        sample_rate: Sample rate

    Returns:
        Filtered signal
    """
    nyquist = sample_rate / 2
    normalized_cutoff = min(cutoff / nyquist, 0.99)
    b, a = butter(order, normalized_cutoff, btype='low')
    return lfilter(b, a, signal)


def highpass_filter(
    signal: np.ndarray,
    cutoff: float,
    order: int = 2,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply highpass filter to signal.

    Args:
        signal: Input audio signal
        cutoff: Cutoff frequency in Hz
        order: Filter order
        sample_rate: Sample rate

    Returns:
        Filtered signal
    """
    nyquist = sample_rate / 2
    normalized_cutoff = max(0.01, min(cutoff / nyquist, 0.99))
    b, a = butter(order, normalized_cutoff, btype='high')
    return lfilter(b, a, signal)


def bandpass_filter(
    signal: np.ndarray,
    low_cutoff: float,
    high_cutoff: float,
    order: int = 2,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply bandpass filter to signal.

    Args:
        signal: Input audio signal
        low_cutoff: Low cutoff frequency in Hz
        high_cutoff: High cutoff frequency in Hz
        order: Filter order
        sample_rate: Sample rate

    Returns:
        Filtered signal
    """
    nyquist = sample_rate / 2
    low = max(0.01, min(low_cutoff / nyquist, 0.99))
    high = max(0.01, min(high_cutoff / nyquist, 0.99))
    if low >= high:
        return signal
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)


def filter_sweep(
    signal: np.ndarray,
    start_cutoff: float,
    end_cutoff: float,
    filter_type: Literal['low', 'high'] = 'low',
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply time-varying filter sweep.

    Useful for filter envelope effects (e.g., synth bass, wah).

    Args:
        signal: Input audio signal
        start_cutoff: Starting cutoff frequency in Hz
        end_cutoff: Ending cutoff frequency in Hz
        filter_type: 'low' for lowpass, 'high' for highpass
        sample_rate: Sample rate

    Returns:
        Filtered signal with sweep applied
    """
    num_samples = len(signal)
    output = np.zeros(num_samples, dtype=np.float32)
    chunk_size = 256

    for i in range(0, num_samples, chunk_size):
        end = min(i + chunk_size, num_samples)
        progress = i / num_samples

        # Interpolate cutoff
        cutoff = start_cutoff * (1 - progress) + end_cutoff * progress

        nyquist = sample_rate / 2
        norm_cutoff = max(0.01, min(cutoff / nyquist, 0.99))

        b, a = butter(2, norm_cutoff, btype=filter_type)
        output[i:end] = lfilter(b, a, signal[i:end])

    return output


# =============================================================================
# DISTORTION
# =============================================================================

def apply_distortion(
    signal: np.ndarray,
    drive: float = 0.5,
    mix: float = 1.0
) -> np.ndarray:
    """
    Apply soft-clipping distortion.

    Uses tanh waveshaping for warm, analog-style distortion.

    Args:
        signal: Input audio signal
        drive: Distortion amount (0-1, can go higher for extreme)
        mix: Wet/dry mix (0 = dry, 1 = fully distorted)

    Returns:
        Distorted signal
    """
    # Apply gain based on drive
    gain = 1 + drive * 10
    driven = signal * gain

    # Soft clip with tanh
    distorted = np.tanh(driven)

    # Mix with dry signal
    output = signal * (1 - mix) + distorted * mix

    return output


def apply_bitcrush(
    signal: np.ndarray,
    bits: int = 8,
    sample_reduce: int = 1
) -> np.ndarray:
    """
    Apply bit crushing effect.

    Reduces bit depth and optionally sample rate for lo-fi sound.

    Args:
        signal: Input audio signal
        bits: Target bit depth (1-16)
        sample_reduce: Sample rate reduction factor

    Returns:
        Bit-crushed signal
    """
    # Bit depth reduction
    levels = 2 ** bits
    crushed = np.round(signal * (levels / 2)) / (levels / 2)

    # Sample rate reduction
    if sample_reduce > 1:
        crushed = np.repeat(crushed[::sample_reduce], sample_reduce)[:len(signal)]

    return crushed


def apply_saturation(
    signal: np.ndarray,
    amount: float = 0.3
) -> np.ndarray:
    """
    Apply subtle saturation/warmth.

    Gentler than distortion, adds harmonics without obvious clipping.

    Args:
        signal: Input audio signal
        amount: Saturation amount (0-1)

    Returns:
        Saturated signal
    """
    # Soft saturation curve
    x = signal * (1 + amount * 2)
    saturated = x / (1 + np.abs(x) * amount)

    return saturated


# =============================================================================
# REVERB AND DELAY
# =============================================================================

def simple_reverb(
    signal: np.ndarray,
    room_size: float = 0.5,
    damping: float = 0.5,
    mix: float = 0.3,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Simple comb filter reverb.

    Args:
        signal: Input audio signal
        room_size: Room size (0-1, larger = longer reverb)
        damping: High frequency damping (0-1)
        mix: Wet/dry mix
        sample_rate: Sample rate

    Returns:
        Signal with reverb applied
    """
    # Comb filter delays (in seconds, scaled by room size)
    base_delays = [0.029, 0.037, 0.041, 0.043]
    delays = [int(d * room_size * 2 * sample_rate) for d in base_delays]

    # Ensure we have enough output buffer
    max_delay = max(delays)
    output_len = len(signal) + max_delay
    output = np.zeros(output_len, dtype=np.float32)

    feedback = room_size * 0.8

    for delay in delays:
        comb = np.zeros(output_len, dtype=np.float32)
        comb[:len(signal)] = signal

        for i in range(delay, len(signal)):
            # Feedback with damping (simple lowpass)
            if i > 0:
                damped = comb[i - delay] * (1 - damping) + comb[i - delay - 1] * damping if i > delay else comb[i - delay]
            else:
                damped = comb[i - delay]
            comb[i] += damped * feedback

        output += comb

    # Normalize comb sum
    output = output[:len(signal)] / len(delays)

    # Mix with dry
    return signal * (1 - mix) + output * mix


def delay(
    signal: np.ndarray,
    delay_time: float = 0.3,
    feedback: float = 0.4,
    mix: float = 0.3,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Simple delay effect.

    Args:
        signal: Input audio signal
        delay_time: Delay time in seconds
        feedback: Feedback amount (0-1, >1 for runaway)
        mix: Wet/dry mix
        sample_rate: Sample rate

    Returns:
        Signal with delay applied
    """
    delay_samples = int(delay_time * sample_rate)

    # Create output buffer with room for delay
    output_len = len(signal) + delay_samples * 4  # Room for feedback
    output = np.zeros(output_len, dtype=np.float32)
    output[:len(signal)] = signal

    # Apply feedback delay
    for i in range(delay_samples, output_len):
        output[i] += output[i - delay_samples] * feedback

    # Trim to original length
    output = output[:len(signal)]

    # Extract wet signal (everything after first delay)
    wet = np.zeros_like(signal)
    wet[delay_samples:] = output[delay_samples:] - signal[delay_samples:]

    return signal * (1 - mix) + (signal + wet) * mix


# =============================================================================
# DYNAMICS
# =============================================================================

def normalize(
    signal: np.ndarray,
    peak: float = 0.9
) -> np.ndarray:
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


def fade_in(
    signal: np.ndarray,
    duration: float = 0.01,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply fade-in to signal.

    Args:
        signal: Input audio signal
        duration: Fade duration in seconds
        sample_rate: Sample rate

    Returns:
        Signal with fade-in applied
    """
    fade_samples = int(duration * sample_rate)
    fade_samples = min(fade_samples, len(signal))

    output = signal.copy()
    fade = np.linspace(0, 1, fade_samples)
    output[:fade_samples] *= fade

    return output


def fade_out(
    signal: np.ndarray,
    duration: float = 0.01,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply fade-out to signal.

    Args:
        signal: Input audio signal
        duration: Fade duration in seconds
        sample_rate: Sample rate

    Returns:
        Signal with fade-out applied
    """
    fade_samples = int(duration * sample_rate)
    fade_samples = min(fade_samples, len(signal))

    output = signal.copy()
    fade = np.linspace(1, 0, fade_samples)
    output[-fade_samples:] *= fade

    return output


def remove_dc_offset(signal: np.ndarray) -> np.ndarray:
    """
    Remove DC offset from signal.

    Args:
        signal: Input audio signal

    Returns:
        Signal with DC offset removed
    """
    return signal - np.mean(signal)


def apply_compression(
    signal: np.ndarray,
    threshold: float = 0.5,
    ratio: float = 4.0,
    attack: float = 0.01,
    release: float = 0.1,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Apply simple compression.

    Args:
        signal: Input audio signal
        threshold: Compression threshold (0-1)
        ratio: Compression ratio (e.g., 4 = 4:1)
        attack: Attack time in seconds
        release: Release time in seconds
        sample_rate: Sample rate

    Returns:
        Compressed signal
    """
    # Calculate envelope
    abs_signal = np.abs(signal)

    # Smooth envelope with attack/release
    attack_coef = np.exp(-1 / (attack * sample_rate))
    release_coef = np.exp(-1 / (release * sample_rate))

    envelope = np.zeros_like(signal)
    for i in range(1, len(signal)):
        if abs_signal[i] > envelope[i-1]:
            envelope[i] = attack_coef * envelope[i-1] + (1 - attack_coef) * abs_signal[i]
        else:
            envelope[i] = release_coef * envelope[i-1] + (1 - release_coef) * abs_signal[i]

    # Calculate gain reduction
    gain = np.ones_like(signal)
    above_threshold = envelope > threshold
    if np.any(above_threshold):
        # How much above threshold (in linear scale)
        excess = envelope[above_threshold] / threshold
        # Apply ratio
        gain[above_threshold] = threshold / envelope[above_threshold] * (excess ** (1/ratio))

    return signal * gain
