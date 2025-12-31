"""
Audio Synthesis Library for ZX Procedural Generation

This library provides reusable synthesis primitives for generating
instruments, sounds, and tracker music for Nethercore ZX games.

Modules:
    synthesis   - Core primitives: ADSR, FM, Karplus-Strong, vibrato
    waveforms   - Basic oscillators: sine, square, saw, triangle, noise
    drums       - Drum synthesis: kick, snare, hat, toms
    effects     - Audio effects: reverb, distortion, filters
    xm_writer   - XM tracker file generation
    it_writer   - IT tracker file generation

Usage:
    from lib.synthesis import karplus_strong, fm_operator, adsr_envelope
    from lib.waveforms import sine_wave, saw_wave
    from lib.drums import kick_808, snare_layered
    from lib.effects import simple_reverb, normalize
    from lib.xm_writer import XmModule, write_xm
"""

from .synthesis import (
    adsr_envelope,
    multi_envelope,
    fm_operator,
    karplus_strong,
    attack_transient,
    apply_vibrato,
)

from .waveforms import (
    sine_wave,
    square_wave,
    saw_wave,
    triangle_wave,
    white_noise,
    pink_noise,
    brown_noise,
    normalize,
    to_8bit_pcm,
    to_16bit_pcm,
)

from .effects import (
    simple_reverb,
    lowpass_filter,
    highpass_filter,
    apply_distortion,
    filter_sweep,
)

# Default sample rate for ZX
SAMPLE_RATE = 22050

__all__ = [
    # synthesis
    "adsr_envelope",
    "multi_envelope",
    "fm_operator",
    "karplus_strong",
    "attack_transient",
    "apply_vibrato",
    # waveforms
    "sine_wave",
    "square_wave",
    "saw_wave",
    "triangle_wave",
    "white_noise",
    "pink_noise",
    "brown_noise",
    "normalize",
    "to_8bit_pcm",
    "to_16bit_pcm",
    # effects
    "simple_reverb",
    "lowpass_filter",
    "highpass_filter",
    "apply_distortion",
    "filter_sweep",
    # constants
    "SAMPLE_RATE",
]
