# Coin Collect SFX Specification
# Run: python .studio/generate.py --only sounds

SOUND = {
    "sound": {
        "name": "coin",
        "category": "action",
        "duration": 0.3,
        "sample_rate": 22050,

        "layers": [
            # Initial ping - high metallic
            {
                "name": "ping",
                "type": "sine",
                "freq": 1200,
                "duration": 0.15,
                "amplitude": 0.7,
                "envelope": {
                    "attack": 0.001,
                    "decay": 0.1,
                    "sustain": 0,
                    "release": 0.05
                }
            },
            # Second harmonic - octave up
            {
                "name": "harmonic1",
                "type": "sine",
                "freq": 2400,
                "duration": 0.12,
                "amplitude": 0.4,
                "delay": 0.02,
                "envelope": {
                    "attack": 0.001,
                    "decay": 0.08,
                    "sustain": 0,
                    "release": 0.03
                }
            },
            # Third tone - fifth up
            {
                "name": "harmonic2",
                "type": "sine",
                "freq": 1800,
                "duration": 0.1,
                "amplitude": 0.3,
                "delay": 0.04,
                "envelope": {
                    "attack": 0.001,
                    "decay": 0.06,
                    "sustain": 0,
                    "release": 0.03
                }
            },
            # Subtle metallic shimmer
            {
                "name": "shimmer",
                "type": "metallic",
                "base_freq": 3000,
                "num_partials": 4,
                "inharmonicity": 1.2,
                "duration": 0.08,
                "amplitude": 0.15
            }
        ],

        "envelope": {
            "attack": 0.001,
            "decay": 0.2,
            "sustain": 0,
            "release": 0.1
        },

        "normalize": True,
        "peak_db": -6.0
    }
}
