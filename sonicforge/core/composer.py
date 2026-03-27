from __future__ import annotations

import random
from uuid import uuid4

from sonicforge.core.models import NoteEvent, ProjectState, Section, Track
from sonicforge.core.sound_dna import create_patch


KEYS = ["C", "D", "E", "F", "G", "A", "Bb"]
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}
PROGRESSIONS = {
    "major": [
        [1, 5, 6, 4],
        [1, 4, 6, 5],
        [6, 4, 1, 5],
        [1, 3, 4, 5],
    ],
    "minor": [
        [1, 6, 3, 7],
        [1, 4, 6, 5],
        [6, 7, 1, 4],
        [1, 7, 6, 7],
    ],
}


def _section_layout(bars: int) -> list[Section]:
    if bars <= 8:
        return [
            Section("Intro", 1, 2, 0.45),
            Section("Verse", 3, 2, 0.6),
            Section("Chorus", 5, bars - 4, 0.85),
        ]
    if bars <= 12:
        return [
            Section("Intro", 1, 2, 0.35),
            Section("Verse", 3, 4, 0.55),
            Section("Chorus", 7, 4, 0.85),
            Section("Bridge", 11, bars - 10, 0.7),
        ]
    return [
        Section("Intro", 1, 2, 0.3),
        Section("Verse", 3, 4, 0.55),
        Section("Pre-Chorus", 7, 2, 0.68),
        Section("Chorus", 9, 4, 0.9),
        Section("Bridge", 13, max(2, bars - 12), 0.75),
    ]


def _degree_to_pitch(root_midi: int, mode: str, degree: int, octave: int = 0) -> int:
    scale = SCALES[mode]
    index = (degree - 1) % len(scale)
    return root_midi + scale[index] + octave * 12


def _chord_tones(root_midi: int, mode: str, degree: int) -> tuple[int, int, int]:
    third_degree = 3 if mode == "major" else 3
    fifth_degree = 5
    return (
        _degree_to_pitch(root_midi, mode, degree),
        _degree_to_pitch(root_midi, mode, degree + third_degree - 1),
        _degree_to_pitch(root_midi, mode, degree + fifth_degree - 1),
    )


def _bar_progression(rng: random.Random, mode: str, bars: int) -> list[int]:
    base = rng.choice(PROGRESSIONS[mode])
    progression: list[int] = []
    while len(progression) < bars:
        progression.extend(base)
    return progression[:bars]


def _build_pad_track(root_midi: int, mode: str, bars: int, progression: list[int], patch_seed: int) -> Track:
    notes: list[NoteEvent] = []
    for bar in range(bars):
        start = bar * 4
        for tone in _chord_tones(root_midi, mode, progression[bar]):
            notes.append(NoteEvent(pitch=tone + 12, start=start, duration=4.0, velocity=72))
    return Track(
        name="Pad",
        instrument="pad",
        color="#6dd3ce",
        volume=0.62,
        pan=0.12,
        notes=notes,
        patch=create_patch("pad", {"valence": 60, "energy": 48, "tension": 42}, patch_seed),
    )


def _build_bass_track(root_midi: int, mode: str, bars: int, progression: list[int], energy: float, patch_seed: int) -> Track:
    notes: list[NoteEvent] = []
    active_pattern = [0.0, 1.5, 2.0, 3.0] if energy > 60 else [0.0, 2.0]
    for bar in range(bars):
        degree = progression[bar]
        root_note = _degree_to_pitch(root_midi - 12, mode, degree)
        fifth_note = _degree_to_pitch(root_midi - 12, mode, degree + 4)
        for start in active_pattern:
            pitch = root_note if start in (0.0, 2.0) else fifth_note
            notes.append(NoteEvent(pitch=pitch, start=bar * 4 + start, duration=0.9, velocity=92))
    return Track(
        name="Bass",
        instrument="bass",
        color="#f4a261",
        volume=0.78,
        pan=-0.05,
        notes=notes,
        patch=create_patch("bass", {"valence": 45, "energy": energy, "tension": 50}, patch_seed),
    )


def _build_drum_track(bars: int, energy: float, tension: float, patch_seed: int) -> Track:
    notes: list[NoteEvent] = []
    hat_step = 0.5 if energy > 55 else 1.0
    for bar in range(bars):
        base = bar * 4
        for beat in (0.0, 2.0):
            notes.append(NoteEvent(pitch=36, start=base + beat, duration=0.25, velocity=120))
        for beat in (1.0, 3.0):
            notes.append(NoteEvent(pitch=38, start=base + beat, duration=0.25, velocity=110))
        hat = 0.0
        while hat < 4.0:
            velocity = 85 if hat % 1.0 == 0 else 62
            notes.append(NoteEvent(pitch=42, start=base + hat, duration=0.15, velocity=velocity))
            hat += hat_step
        if tension > 70 and bar % 4 == 3:
            notes.append(NoteEvent(pitch=46, start=base + 3.5, duration=0.25, velocity=105))
    return Track(
        name="Drums",
        instrument="drums",
        color="#e76f51",
        volume=0.86,
        pan=0.0,
        notes=notes,
        patch=create_patch("drums", {"valence": 50, "energy": energy, "tension": tension}, patch_seed),
    )


def _build_melody_track(
    rng: random.Random,
    root_midi: int,
    mode: str,
    bars: int,
    progression: list[int],
    energy: float,
    tension: float,
    patch_seed: int,
) -> Track:
    notes: list[NoteEvent] = []
    motif_offsets = [0, 2, 4, 2] if tension < 55 else [0, 4, 2, 6]
    density = 4 if energy > 68 else 3 if energy > 45 else 2
    for bar in range(bars):
        degree = progression[bar]
        chord = _chord_tones(root_midi + 12, mode, degree)
        choices = list(chord) + [
            _degree_to_pitch(root_midi + 12, mode, degree + 1),
            _degree_to_pitch(root_midi + 12, mode, degree + 5),
        ]
        for slot in range(density):
            start = bar * 4 + slot * (4 / density)
            motif = motif_offsets[(bar + slot) % len(motif_offsets)]
            choice = choices[(motif + rng.randint(0, len(choices) - 1)) % len(choices)]
            duration = 0.75 if density >= 4 else 1.0
            notes.append(
                NoteEvent(
                    pitch=choice,
                    start=round(start, 3),
                    duration=duration,
                    velocity=90 + rng.randint(-12, 10),
                )
            )
        if bar % 4 == 3:
            notes[-1].duration = 1.5
    return Track(
        name="Melody",
        instrument="melody",
        color="#7b9acc",
        volume=0.72,
        pan=0.08,
        notes=notes,
        patch=create_patch("melody", {"valence": 65, "energy": energy, "tension": tension}, patch_seed),
    )


def compose_project(
    name: str,
    genre: str,
    tempo: int,
    bars: int,
    emotion: dict[str, float],
    seed: int | None = None,
) -> ProjectState:
    rng = random.Random(seed if seed is not None else int(tempo + bars + emotion["energy"] * 3))
    mode = "major" if emotion["valence"] >= 50 else "minor"
    key = rng.choice(KEYS)
    key_offset = {
        "C": 60,
        "D": 62,
        "E": 64,
        "F": 65,
        "G": 67,
        "A": 69,
        "Bb": 70,
    }[key]
    progression = _bar_progression(rng, mode, bars)
    sections = _section_layout(bars)
    tracks = [
        _build_drum_track(bars, emotion["energy"], emotion["tension"], rng.randint(1, 9999)),
        _build_bass_track(key_offset, mode, bars, progression, emotion["energy"], rng.randint(1, 9999)),
        _build_pad_track(key_offset, mode, bars, progression, rng.randint(1, 9999)),
        _build_melody_track(
            rng,
            key_offset,
            mode,
            bars,
            progression,
            emotion["energy"],
            emotion["tension"],
            rng.randint(1, 9999),
        ),
    ]
    project = ProjectState(
        project_id=str(uuid4()),
        name=name,
        genre=genre,
        tempo=tempo,
        bars=bars,
        key=key,
        mode=mode,
        emotion=emotion,
        tracks=tracks,
        sections=sections,
    )
    project.events.append(
        {
            "type": "compose",
            "payload": {
                "genre": genre,
                "tempo": tempo,
                "bars": bars,
                "emotion": emotion,
            },
        }
    )
    return project
