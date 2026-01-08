# Pad Instrument Specification
# Run: python .studio/generate.py --only instruments

INSTRUMENT = {
    "instrument": {
        "name": "pad",
        "category": "pad",
        "base_note": "C3",
        "sample_rate": 22050,

        "synthesis": {
            "type": "additive",
            "partials": [
                (1.0, 1.0),     # Fundamental
                (2.0, 0.5),     # Octave
                (3.0, 0.25),    # Fifth
                (4.0, 0.15),    # 2nd octave
                (5.0, 0.1),     # Major 3rd
                (6.0, 0.08)     # 5th + octave
            ]
        },

        "envelope": {
            "attack": 0.3,
            "decay": 0.2,
            "sustain": 0.8,
            "release": 0.5
        },

        "output": {
            "duration": 2.0,
            "bit_depth": 16,
            "loop": True,
            "loop_start": 0.4,
            "loop_end": 1.8
        }
    }
}
