# Jump SFX Specification
# Usage: python sound_parser.py sfx jump.spec.py jump.wav

SOUND = {
    "sound": {
        "name": "jump",
        "category": "action",
        "duration": 0.2,
        "sample_rate": 22050,

        "layers": [
            # Rising pitch sweep - main jump sound
            {
                "name": "sweep",
                "type": "sine",
                "freq": 150,
                "freq_end": 400,
                "duration": 0.12,
                "amplitude": 0.8,
                "envelope": {
                    "attack": 0.005,
                    "decay": 0.08,
                    "sustain": 0.3,
                    "release": 0.03
                }
            },
            # Harmonic layer - adds character
            {
                "name": "harmonic",
                "type": "sine",
                "freq": 300,
                "freq_end": 800,
                "duration": 0.1,
                "amplitude": 0.3,
                "envelope": {
                    "attack": 0.005,
                    "decay": 0.06,
                    "sustain": 0,
                    "release": 0.03
                }
            },
            # Soft thump - feet leaving ground
            {
                "name": "thump",
                "type": "noise_burst",
                "color": "brown",
                "duration": 0.03,
                "amplitude": 0.25,
                "filter": {"type": "lowpass", "cutoff": 400}
            }
        ],

        "envelope": {
            "attack": 0.002,
            "decay": 0.12,
            "sustain": 0,
            "release": 0.06
        },

        "normalize": True,
        "peak_db": -6.0
    }
}
