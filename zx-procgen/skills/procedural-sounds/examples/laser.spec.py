# Laser Shot SFX Specification
# Usage: python sound_parser.py sfx laser.spec.py laser.wav

SOUND = {
    "sound": {
        "name": "laser",
        "category": "projectile",
        "duration": 0.25,
        "sample_rate": 22050,

        "layers": [
            # Sharp attack transient
            {
                "name": "transient",
                "type": "noise_burst",
                "color": "white",
                "duration": 0.02,
                "amplitude": 0.3,
                "filter": {"type": "highpass", "cutoff": 4000}
            },
            # Main body - FM sweep
            {
                "name": "body",
                "type": "fm_synth",
                "carrier_freq": 600,
                "mod_ratio": 1.5,
                "mod_index": 6.0,
                "index_decay": 12.0,
                "amplitude": 1.0
            },
            # Sub-bass punch
            {
                "name": "sub",
                "type": "sine",
                "freq": 120,
                "freq_end": 60,
                "duration": 0.1,
                "amplitude": 0.4,
                "envelope": {
                    "attack": 0.001,
                    "decay": 0.08,
                    "sustain": 0,
                    "release": 0.02
                }
            }
        ],

        "envelope": {
            "attack": 0.002,
            "decay": 0.15,
            "sustain": 0,
            "release": 0.08
        },

        "master_filter": {"type": "lowpass", "cutoff": 8000},
        "normalize": True,
        "peak_db": -3.0
    }
}
