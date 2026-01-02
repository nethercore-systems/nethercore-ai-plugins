"""
Drum Synthesis Examples

EXAMPLE IMPLEMENTATIONS - NOT A LIBRARY!

These are reference implementations showing how to synthesize common drum sounds.
Do NOT import this file directly. Instead, study these examples and compose your
own drums using primitives from lib/drums.py, lib/synthesis.py, and lib/waveforms.py.

Examples included:
- Kicks (808, acoustic, punchy)
- Snares (808, acoustic, layered)
- Hi-hats (closed, open)
- Toms, cymbals, percussion
"""

import numpy as np
from scipy.signal import butter, lfilter
from typing import Literal

SAMPLE_RATE = 22050


# =============================================================================
# KICK DRUMS
# =============================================================================

def kick_808(
    duration: float = 0.5,
    pitch: float = 60.0,
    pitch_drop: float = 50.0,
    decay: float = 0.3,
    click: float = 0.3,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    TR-808 style kick drum.

    Sine wave with pitch envelope drop and optional click.

    Args:
        duration: Duration in seconds
        pitch: Starting pitch in Hz
        pitch_drop: Amount to drop pitch (Hz)
        decay: Amplitude decay rate
        click: Click transient amount (0-1)
        sample_rate: Sample rate

    Returns:
        Kick drum audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Pitch envelope: rapid drop from pitch to (pitch - pitch_drop)
    freq = pitch - pitch_drop * (1 - np.exp(-t * 30))

    # Integrate frequency to get phase
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    body = np.sin(phase)

    # Amplitude envelope
    amp_env = np.exp(-t / decay)

    # Click transient
    click_env = np.exp(-t * 100)
    click_sig = np.sin(phase * 2) * click_env * click

    output = (body + click_sig) * amp_env
    return output / (np.max(np.abs(output)) + 1e-10)


def kick_acoustic(
    duration: float = 0.4,
    pitch: float = 80.0,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Acoustic-style kick drum.

    More attack transient, less sustained sub.

    Args:
        duration: Duration in seconds
        pitch: Fundamental pitch in Hz
        sample_rate: Sample rate

    Returns:
        Kick drum audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Body: pitch drop
    freq = pitch * np.exp(-t * 20) + 40
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    body = np.sin(phase)

    # Beater transient (noise burst)
    beater = np.random.randn(num_samples) * 0.5
    beater_env = np.exp(-t * 80)
    beater *= beater_env

    # Lowpass the beater
    b, a = butter(2, 2000 / (sample_rate / 2), btype='low')
    beater = lfilter(b, a, beater)

    # Combine
    amp_env = np.exp(-t * 8)
    output = (body * 0.8 + beater * 0.4) * amp_env

    return output / (np.max(np.abs(output)) + 1e-10)


def kick_punchy(
    duration: float = 0.3,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Punchy electronic kick for dance/EDM.

    Short, tight, with emphasized attack.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Kick drum audio signal
    """
    return kick_808(
        duration=duration,
        pitch=70,
        pitch_drop=55,
        decay=0.15,
        click=0.5,
        sample_rate=sample_rate
    )


# =============================================================================
# SNARE DRUMS
# =============================================================================

def snare_808(
    duration: float = 0.3,
    tone_pitch: float = 180.0,
    noise_mix: float = 0.6,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    TR-808 style snare drum.

    Pitched body with noise layer.

    Args:
        duration: Duration in seconds
        tone_pitch: Body tone pitch in Hz
        noise_mix: Noise layer mix (0-1)
        sample_rate: Sample rate

    Returns:
        Snare drum audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Body tone with pitch drop
    freq = tone_pitch * np.exp(-t * 15)
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    body = np.sin(phase)

    # Noise layer (snares)
    noise = np.random.randn(num_samples)
    # Bandpass the noise
    b, a = butter(2, [1000 / (sample_rate / 2), 8000 / (sample_rate / 2)], btype='band')
    noise = lfilter(b, a, noise)

    # Envelopes
    body_env = np.exp(-t * 20)
    noise_env = np.exp(-t * 15)

    output = body * body_env * (1 - noise_mix) + noise * noise_env * noise_mix
    return output / (np.max(np.abs(output)) + 1e-10)


def snare_acoustic(
    duration: float = 0.35,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Acoustic-style snare drum.

    Multi-layer: body tone, head transient, snare wires.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Snare drum audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Body tone (two modes)
    freq1 = 200 * np.exp(-t * 10)
    freq2 = 340 * np.exp(-t * 12)
    body1 = np.sin(np.cumsum(2 * np.pi * freq1 / sample_rate))
    body2 = np.sin(np.cumsum(2 * np.pi * freq2 / sample_rate))

    # Snare wires (filtered noise)
    wires = np.random.randn(num_samples)
    b, a = butter(2, [2000 / (sample_rate / 2), 9000 / (sample_rate / 2)], btype='band')
    wires = lfilter(b, a, wires)

    # Stick attack (short noise burst)
    stick = np.random.randn(num_samples) * np.exp(-t * 150)

    # Envelopes
    body_env = np.exp(-t * 15)
    wire_env = np.exp(-t * 12)

    output = (
        body1 * body_env * 0.4 +
        body2 * body_env * 0.3 +
        wires * wire_env * 0.4 +
        stick * 0.2
    )

    return output / (np.max(np.abs(output)) + 1e-10)


def snare_layered(
    duration: float = 0.3,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Layered snare combining 808 and acoustic elements.

    Good general-purpose snare.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Snare drum audio signal
    """
    s808 = snare_808(duration, sample_rate=sample_rate)
    acoustic = snare_acoustic(duration, sample_rate=sample_rate)

    # Trim to same length
    min_len = min(len(s808), len(acoustic))
    output = s808[:min_len] * 0.5 + acoustic[:min_len] * 0.5

    return output / (np.max(np.abs(output)) + 1e-10)


# =============================================================================
# HI-HATS
# =============================================================================

def hihat_closed(
    duration: float = 0.08,
    brightness: float = 0.7,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Closed hi-hat.

    Filtered noise with fast decay.

    Args:
        duration: Duration in seconds
        brightness: High frequency content (0-1)
        sample_rate: Sample rate

    Returns:
        Hi-hat audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Noise source
    noise = np.random.randn(num_samples)

    # Highpass filter based on brightness
    cutoff = 4000 + brightness * 6000
    b, a = butter(2, min(cutoff / (sample_rate / 2), 0.99), btype='high')
    filtered = lfilter(b, a, noise)

    # Fast decay envelope
    env = np.exp(-t * 60)

    output = filtered * env
    return output / (np.max(np.abs(output)) + 1e-10)


def hihat_open(
    duration: float = 0.4,
    brightness: float = 0.7,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Open hi-hat.

    Longer decay than closed.

    Args:
        duration: Duration in seconds
        brightness: High frequency content (0-1)
        sample_rate: Sample rate

    Returns:
        Hi-hat audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Noise source
    noise = np.random.randn(num_samples)

    # Highpass filter
    cutoff = 3500 + brightness * 5000
    b, a = butter(2, min(cutoff / (sample_rate / 2), 0.99), btype='high')
    filtered = lfilter(b, a, noise)

    # Add some metallic resonance
    resonance = np.sin(2 * np.pi * 6000 * t) * 0.1
    resonance += np.sin(2 * np.pi * 8500 * t) * 0.08

    # Slower decay envelope
    env = np.exp(-t * 8)

    output = (filtered + resonance) * env
    return output / (np.max(np.abs(output)) + 1e-10)


# =============================================================================
# TOMS AND PERCUSSION
# =============================================================================

def tom(
    duration: float = 0.4,
    pitch: float = 120.0,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Tom drum.

    Pitched body with attack transient.

    Args:
        duration: Duration in seconds
        pitch: Fundamental pitch in Hz (low tom ~80, mid ~120, high ~180)
        sample_rate: Sample rate

    Returns:
        Tom drum audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Body with pitch drop
    freq = pitch * (1 + 0.3 * np.exp(-t * 20))
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    body = np.sin(phase)

    # Attack transient
    attack = np.random.randn(num_samples) * np.exp(-t * 100)
    b, a = butter(2, 1000 / (sample_rate / 2), btype='low')
    attack = lfilter(b, a, attack)

    # Envelope
    env = np.exp(-t * 6)

    output = (body * 0.8 + attack * 0.3) * env
    return output / (np.max(np.abs(output)) + 1e-10)


def crash(
    duration: float = 1.5,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Crash cymbal.

    Noise-based with metallic resonances.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Crash cymbal audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Noise base
    noise = np.random.randn(num_samples)
    b, a = butter(2, 3000 / (sample_rate / 2), btype='high')
    filtered = lfilter(b, a, noise)

    # Metallic resonances
    res = np.zeros(num_samples)
    for freq in [4200, 5800, 7300, 9100]:
        res += np.sin(2 * np.pi * freq * t) * 0.1

    # Envelope: fast attack, slow decay
    env = np.exp(-t * 3)
    attack = 1 - np.exp(-t * 100)

    output = (filtered * 0.7 + res * 0.3) * env * attack
    return output / (np.max(np.abs(output)) + 1e-10)


def ride(
    duration: float = 1.0,
    bell: bool = False,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Ride cymbal.

    Args:
        duration: Duration in seconds
        bell: If True, emphasize bell sound
        sample_rate: Sample rate

    Returns:
        Ride cymbal audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Noise component
    noise = np.random.randn(num_samples)
    b, a = butter(2, 4000 / (sample_rate / 2), btype='high')
    filtered = lfilter(b, a, noise)

    # Bell resonances (more prominent if bell=True)
    bell_mix = 0.4 if bell else 0.15
    res = np.zeros(num_samples)
    for freq in [3500, 5200, 7800]:
        res += np.sin(2 * np.pi * freq * t)

    # Envelope
    env = np.exp(-t * 4)
    attack = 1 - np.exp(-t * 200)

    output = (filtered * (1 - bell_mix) + res * bell_mix / 3) * env * attack
    return output / (np.max(np.abs(output)) + 1e-10)


def clap(
    duration: float = 0.25,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Hand clap.

    Multiple noise bursts with reverb-like tail.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Clap audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Multiple short noise bursts (simulating multiple hands)
    output = np.zeros(num_samples)
    for delay in [0.0, 0.01, 0.02, 0.025]:
        burst = np.random.randn(num_samples)
        t_shifted = np.maximum(0, t - delay)
        env = np.exp(-t_shifted * 40) * (t >= delay)
        output += burst * env

    # Bandpass filter
    b, a = butter(2, [800 / (sample_rate / 2), 6000 / (sample_rate / 2)], btype='band')
    output = lfilter(b, a, output)

    # Overall envelope
    env = np.exp(-t * 10)
    output *= env

    return output / (np.max(np.abs(output)) + 1e-10)


def rimshot(
    duration: float = 0.1,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Rimshot/sidestick.

    Short, bright click.

    Args:
        duration: Duration in seconds
        sample_rate: Sample rate

    Returns:
        Rimshot audio signal
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # High-pitched click
    freq = 800 * np.exp(-t * 30)
    tone = np.sin(np.cumsum(2 * np.pi * freq / sample_rate))

    # Noise transient
    noise = np.random.randn(num_samples)
    b, a = butter(2, [1000 / (sample_rate / 2), 8000 / (sample_rate / 2)], btype='band')
    noise = lfilter(b, a, noise)

    # Very fast envelope
    env = np.exp(-t * 60)

    output = (tone * 0.5 + noise * 0.5) * env
    return output / (np.max(np.abs(output)) + 1e-10)
