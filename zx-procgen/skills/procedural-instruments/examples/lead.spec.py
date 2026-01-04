# Lead Synth Instrument Specification
# Usage: python sound_parser.py instrument lead.spec.py lead.wav

INSTRUMENT = {
    "instrument": {
        "name": "lead",
        "category": "lead",
        "base_note": "C4",
        "sample_rate": 22050,

        "synthesis": {
            "type": "subtractive",
            "oscillators": [
                {"waveform": "saw", "detune": 0},
                {"waveform": "saw", "detune": 7},    # 7 cents sharp
                {"waveform": "saw", "detune": -7}   # 7 cents flat
            ],
            "filter": {
                "type": "lowpass",
                "cutoff": 3000,
                "q": 1.5
            }
        },

        "envelope": {
            "attack": 0.02,
            "decay": 0.15,
            "sustain": 0.7,
            "release": 0.2
        },

        "output": {
            "duration": 1.0,
            "bit_depth": 16,
            "loop": True,
            "loop_start": 0.1,
            "loop_end": 0.9
        }
    }
}
