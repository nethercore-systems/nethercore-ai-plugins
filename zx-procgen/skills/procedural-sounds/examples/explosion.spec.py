# Explosion SFX Specification
# Usage: python sound_parser.py sfx explosion.spec.py explosion.wav

SOUND = {
    "sound": {
        "name": "explosion",
        "category": "impact",
        "duration": 0.8,
        "sample_rate": 22050,

        "layers": [
            # Initial blast - white noise burst
            {
                "name": "blast",
                "type": "noise_burst",
                "color": "white",
                "duration": 0.15,
                "amplitude": 1.0,
                "envelope": {
                    "attack": 0.001,
                    "decay": 0.1,
                    "sustain": 0.2,
                    "release": 0.04
                },
                "filter": {"type": "bandpass", "cutoff_low": 200, "cutoff_high": 4000}
            },
            # Low-end thump - pitched body
            {
                "name": "thump",
                "type": "pitched_body",
                "start_freq": 150,
                "end_freq": 30,
                "duration": 0.3,
                "amplitude": 0.9,
                "filter": {"type": "lowpass", "cutoff": 200}
            },
            # Rumble tail - brown noise
            {
                "name": "rumble",
                "type": "noise_burst",
                "color": "brown",
                "duration": 0.6,
                "amplitude": 0.4,
                "delay": 0.1,
                "filter": {"type": "lowpass", "cutoff": 300}
            },
            # High sizzle - debris
            {
                "name": "sizzle",
                "type": "noise_burst",
                "color": "pink",
                "duration": 0.5,
                "amplitude": 0.25,
                "delay": 0.05,
                "filter": {"type": "highpass", "cutoff": 2000}
            }
        ],

        "envelope": {
            "attack": 0.001,
            "decay": 0.4,
            "sustain": 0.1,
            "release": 0.3
        },

        "normalize": True,
        "peak_db": -1.0
    }
}
