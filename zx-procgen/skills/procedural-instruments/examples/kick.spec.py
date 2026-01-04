# Kick Drum Instrument Specification
# Usage: python sound_parser.py instrument kick.spec.py kick.wav

INSTRUMENT = {
    "instrument": {
        "name": "kick",
        "category": "drums",
        "base_note": "C2",
        "sample_rate": 22050,

        # Kicks use a specialized synthesis approach
        # The parser will handle this as a pitched_body + noise layer
        "synthesis": {
            "type": "fm",
            "algorithm": "simple",
            "index": 8.0,
            "index_decay": 25.0,
            "operators": [
                {"ratio": 1.0, "level": 1.0}
            ]
        },

        "envelope": {
            "attack": 0.001,
            "decay": 0.15,
            "sustain": 0,
            "release": 0.1
        },

        "pitch_envelope": {
            "attack": 0.0,
            "amount": 24,       # 2 octaves pitch drop
            "decay": 0.03
        },

        "output": {
            "duration": 0.3,
            "bit_depth": 16,
            "loop": False
        }
    }
}
