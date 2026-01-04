# Bass Instrument Specification
# Usage: python sound_parser.py instrument bass.spec.py bass.wav

INSTRUMENT = {
    "instrument": {
        "name": "bass",
        "category": "bass",
        "base_note": "C2",
        "sample_rate": 22050,

        "synthesis": {
            "type": "karplus_strong",
            "damping": 0.994,
            "brightness": 0.5
        },

        "envelope": {
            "attack": 0.01,
            "decay": 0.4,
            "sustain": 0.3,
            "release": 0.3
        },

        "output": {
            "duration": 1.5,
            "bit_depth": 16,
            "loop": True,
            "loop_start": 0.1,
            "loop_end": 1.4
        }
    }
}
