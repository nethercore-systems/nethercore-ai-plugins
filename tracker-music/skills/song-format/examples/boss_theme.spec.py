# Boss Battle Theme - Example Song Spec
# Dark, aggressive battle music with chromatic bass and stabs

SONG = {
    "song": {
        "name": "boss_theme",
        "title": "Dark Lord Battle",
        "format": "xm",
        "bpm": 155,
        "speed": 4,
        "channels": 6,

        "channel_names": {
            0: "kick",
            1: "snare",
            2: "hihat",
            3: "bass",
            4: "lead",
            5: "pad"
        },

        # Inline instrument definitions for self-contained example
        "instruments": [
            # Kick - punchy FM
            {
                "name": "kick",
                "synthesis": {"type": "fm", "index": 12.0, "index_decay": 20.0},
                "envelope": {"attack": 0.001, "decay": 0.15, "sustain": 0, "release": 0.05},
                "base_note": "C2",
                "output": {"duration": 0.3}
            },
            # Snare - noise + body
            {
                "name": "snare",
                "synthesis": {"type": "fm", "index": 8.0, "index_decay": 15.0},
                "envelope": {"attack": 0.001, "decay": 0.12, "sustain": 0, "release": 0.05},
                "base_note": "D3",
                "output": {"duration": 0.25}
            },
            # Hi-hat - metallic
            {
                "name": "hihat",
                "synthesis": {"type": "fm", "index": 4.0, "index_decay": 30.0},
                "envelope": {"attack": 0.001, "decay": 0.05, "sustain": 0, "release": 0.02},
                "base_note": "F#5",
                "output": {"duration": 0.1}
            },
            # Bass - aggressive saw
            {
                "name": "bass",
                "synthesis": {
                    "type": "subtractive",
                    "oscillators": [
                        {"waveform": "saw", "detune": 0},
                        {"waveform": "saw", "detune": 7}
                    ],
                    "filter": {"type": "lowpass", "cutoff": 800}
                },
                "envelope": {"attack": 0.005, "decay": 0.2, "sustain": 0.6, "release": 0.1},
                "base_note": "C1",
                "output": {"duration": 1.0}
            },
            # Lead - aggressive detuned saw with character
            {
                "name": "lead",
                "synthesis": {
                    "type": "subtractive",
                    "oscillators": [
                        {"waveform": "saw", "detune": 0},
                        {"waveform": "saw", "detune": -8},
                        {"waveform": "square", "detune": 5, "duty": 0.3}
                    ],
                    "filter": {"type": "lowpass", "cutoff": 3500}
                },
                "envelope": {"attack": 0.015, "decay": 0.2, "sustain": 0.65, "release": 0.15},
                "base_note": "C4",
                "output": {"duration": 1.2}
            },
            # Pad - dark atmosphere
            {
                "name": "pad",
                "synthesis": {"type": "karplus_strong", "damping": 0.999, "brightness": 0.3},
                "envelope": {"attack": 0.5, "decay": 0.3, "sustain": 0.5, "release": 1.0},
                "base_note": "D2",
                "output": {"duration": 3.0}
            }
        ],

        "patterns": {
            # Sparse intro - builds tension
            "intro": {
                "rows": 64,
                "notes": {
                    0: [  # Kick - sparse, building
                        {"row": 0, "note": "C-3", "inst": 0, "vol": 40},
                        {"row": 32, "note": "C-3", "inst": 0, "vol": 56}
                    ],
                    5: [  # Pad - ominous swell
                        {"row": 0, "note": "D-2", "inst": 5, "vol": 20}
                    ]
                }
            },

            # Main pattern - aggressive 4-on-floor
            "main": {
                "rows": 64,
                "notes": {
                    0: [  # Kick - driving beat
                        {"row": 0, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 8, "note": "C-3", "inst": 0, "vol": 48},
                        {"row": 16, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 24, "note": "C-3", "inst": 0, "vol": 48},
                        {"row": 32, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 40, "note": "C-3", "inst": 0, "vol": 48},
                        {"row": 48, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 56, "note": "C-3", "inst": 0, "vol": 48}
                    ],
                    1: [  # Snare - backbeat
                        {"row": 8, "note": "D-3", "inst": 1, "vol": 64},
                        {"row": 24, "note": "D-3", "inst": 1, "vol": 56},
                        {"row": 40, "note": "D-3", "inst": 1, "vol": 64},
                        {"row": 56, "note": "D-3", "inst": 1, "vol": 56}
                    ],
                    2: [  # Hi-hat - 8th notes
                        {"row": 0, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 4, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 8, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 12, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 16, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 20, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 24, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 28, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 32, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 36, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 40, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 44, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 48, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 52, "note": "F#4", "inst": 2, "vol": 24},
                        {"row": 56, "note": "F#4", "inst": 2, "vol": 32},
                        {"row": 60, "note": "F#4", "inst": 2, "vol": 24}
                    ],
                    3: [  # Bass - chromatic menace in D minor
                        {"row": 0, "note": "D-1", "inst": 3, "vol": 64},
                        {"row": 12, "note": "D-1", "inst": 3, "vol": 48},
                        {"row": 16, "note": "D#1", "inst": 3, "vol": 64},
                        {"row": 28, "note": "D#1", "inst": 3, "vol": 48},
                        {"row": 32, "note": "E-1", "inst": 3, "vol": 64},
                        {"row": 44, "note": "E-1", "inst": 3, "vol": 48},
                        {"row": 48, "note": "D-1", "inst": 3, "vol": 64}
                    ],
                    4: [  # Lead - menacing riff
                        {"row": 0, "note": "D-4", "inst": 4, "vol": 58},
                        {"row": 8, "note": "F-4", "inst": 4, "vol": 60},
                        {"row": 14, "note": "E-4", "inst": 4, "vol": 56},
                        {"row": 16, "note": "D-4", "inst": 4, "vol": 62},
                        {"row": 24, "note": "C-4", "inst": 4, "vol": 58},
                        {"row": 32, "note": "A-4", "inst": 4, "vol": 64},
                        {"row": 36, "note": "G-4", "inst": 4, "vol": 58},
                        {"row": 40, "note": "F-4", "inst": 4, "vol": 60},
                        {"row": 44, "note": "E-4", "inst": 4, "vol": 56},
                        {"row": 48, "note": "D-4", "inst": 4, "vol": 64},
                        {"row": 56, "note": "C#4", "inst": 4, "vol": 60}
                    ],
                    5: [  # Pad - dark atmosphere
                        {"row": 0, "note": "D-2", "inst": 5, "vol": 32}
                    ]
                }
            },

            # Breakdown - sparse tension builder
            "breakdown": {
                "rows": 64,
                "notes": {
                    0: [  # Sparse kicks
                        {"row": 0, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 48, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 52, "note": "C-3", "inst": 0, "vol": 56},
                        {"row": 56, "note": "C-3", "inst": 0, "vol": 48},
                        {"row": 60, "note": "C-3", "inst": 0, "vol": 40}
                    ],
                    5: [  # Pad - tension build
                        {"row": 0, "note": "D-2", "inst": 5, "vol": 32},
                        {"row": 32, "note": "D#2", "inst": 5, "vol": 48}
                    ]
                }
            }
        },

        "arrangement": [
            {"pattern": "intro"},
            {"pattern": "main", "repeat": 2},
            {"pattern": "breakdown"},
            {"pattern": "main", "repeat": 2}
        ],

        "restart_position": 1,  # Skip intro on loop

        "automation": [
            {
                "type": "volume_fade",
                "pattern": "intro",
                "channel": 5,
                "start_row": 0,
                "end_row": 48,
                "start_vol": 0,
                "end_vol": 48
            }
        ]
    }
}
