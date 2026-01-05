# Menu Theme - Example Song Spec
# Gentle, ambient menu music with arpeggios

SONG = {
    "song": {
        "name": "menu_theme",
        "title": "Main Menu",
        "format": "it",  # Using IT for NNA polyphony
        "bpm": 110,
        "speed": 6,
        "channels": 4,

        "channel_names": {
            0: "piano",
            1: "pad",
            2: "bass",
            3: "perc"
        },

        "instruments": [
            # Piano - FM with soft attack
            {
                "name": "piano",
                "synthesis": {
                    "type": "fm",
                    "index": 3.0,
                    "index_decay": 4.0
                },
                "envelope": {
                    "attack": 0.01,
                    "decay": 0.8,
                    "sustain": 0.2,
                    "release": 0.5
                },
                "base_note": "C4",
                "output": {"duration": 2.0}
            },
            # Pad - warm strings
            {
                "name": "pad",
                "synthesis": {
                    "type": "additive",
                    "partials": [
                        [1.0, 1.0],
                        [2.0, 0.5],
                        [3.0, 0.25],
                        [4.0, 0.125]
                    ]
                },
                "envelope": {
                    "attack": 0.8,
                    "decay": 0.3,
                    "sustain": 0.6,
                    "release": 1.5
                },
                "base_note": "C3",
                "output": {"duration": 4.0}
            },
            # Bass - soft pluck
            {
                "name": "bass",
                "synthesis": {
                    "type": "karplus_strong",
                    "damping": 0.998,
                    "brightness": 0.4
                },
                "envelope": {
                    "attack": 0.01,
                    "decay": 0.5,
                    "sustain": 0.3,
                    "release": 0.3
                },
                "base_note": "C2",
                "output": {"duration": 1.5}
            },
            # Light percussion - soft click
            {
                "name": "perc",
                "synthesis": {
                    "type": "fm",
                    "index": 2.0,
                    "index_decay": 40.0
                },
                "envelope": {
                    "attack": 0.001,
                    "decay": 0.08,
                    "sustain": 0,
                    "release": 0.02
                },
                "base_note": "C5",
                "output": {"duration": 0.15}
            }
        ],

        "patterns": {
            # Ambient intro - just pad
            "ambient": {
                "rows": 64,
                "notes": {
                    1: [  # Pad - C major chord spread
                        {"row": 0, "note": "C-3", "inst": 1, "vol": 40}
                    ],
                    0: [  # Piano - gentle arpeggios
                        {"row": 0, "note": "C-4", "inst": 0, "vol": 48},
                        {"row": 8, "note": "E-4", "inst": 0, "vol": 40},
                        {"row": 16, "note": "G-4", "inst": 0, "vol": 44},
                        {"row": 24, "note": "C-5", "inst": 0, "vol": 40},
                        {"row": 32, "note": "G-4", "inst": 0, "vol": 44},
                        {"row": 40, "note": "E-4", "inst": 0, "vol": 40},
                        {"row": 48, "note": "C-4", "inst": 0, "vol": 48}
                    ]
                }
            },

            # Main melody pattern
            "melody": {
                "rows": 64,
                "notes": {
                    0: [  # Piano - melody line
                        {"row": 0, "note": "G-4", "inst": 0, "vol": 56},
                        {"row": 8, "note": "A-4", "inst": 0, "vol": 52},
                        {"row": 16, "note": "B-4", "inst": 0, "vol": 56},
                        {"row": 24, "note": "C-5", "inst": 0, "vol": 60},
                        {"row": 32, "note": "B-4", "inst": 0, "vol": 56},
                        {"row": 40, "note": "A-4", "inst": 0, "vol": 52},
                        {"row": 48, "note": "G-4", "inst": 0, "vol": 56}
                    ],
                    1: [  # Pad - sustained
                        {"row": 0, "note": "C-3", "inst": 1, "vol": 40}
                    ],
                    2: [  # Bass - root notes
                        {"row": 0, "note": "C-2", "inst": 2, "vol": 48},
                        {"row": 32, "note": "G-1", "inst": 2, "vol": 44}
                    ],
                    3: [  # Light percussion
                        {"row": 0, "note": "C-5", "inst": 3, "vol": 24},
                        {"row": 16, "note": "C-5", "inst": 3, "vol": 20},
                        {"row": 32, "note": "C-5", "inst": 3, "vol": 24},
                        {"row": 48, "note": "C-5", "inst": 3, "vol": 20}
                    ]
                }
            },

            # Variation - Am chord
            "variation": {
                "rows": 64,
                "notes": {
                    0: [  # Piano - Am arpeggio
                        {"row": 0, "note": "A-3", "inst": 0, "vol": 52},
                        {"row": 8, "note": "C-4", "inst": 0, "vol": 44},
                        {"row": 16, "note": "E-4", "inst": 0, "vol": 48},
                        {"row": 24, "note": "A-4", "inst": 0, "vol": 44},
                        {"row": 32, "note": "E-4", "inst": 0, "vol": 48},
                        {"row": 40, "note": "C-4", "inst": 0, "vol": 44},
                        {"row": 48, "note": "A-3", "inst": 0, "vol": 52}
                    ],
                    1: [  # Pad - Am
                        {"row": 0, "note": "A-2", "inst": 1, "vol": 36}
                    ],
                    2: [  # Bass
                        {"row": 0, "note": "A-1", "inst": 2, "vol": 44},
                        {"row": 32, "note": "E-1", "inst": 2, "vol": 40}
                    ]
                }
            }
        },

        "arrangement": [
            {"pattern": "ambient", "repeat": 2},
            {"pattern": "melody"},
            {"pattern": "variation"},
            {"pattern": "melody"},
            {"pattern": "ambient"}
        ],

        "restart_position": 0,  # Full loop

        "automation": [
            {
                "type": "volume_fade",
                "pattern": "ambient",
                "channel": 1,
                "start_row": 0,
                "end_row": 32,
                "start_vol": 0,
                "end_vol": 40
            }
        ],

        "it_options": {
            "stereo": True,
            "global_volume": 100,
            "mix_volume": 40
        }
    }
}
