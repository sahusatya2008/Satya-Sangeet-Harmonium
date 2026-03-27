from __future__ import annotations

from sonicforge.core.models import PhonemeFrame, Track, VoicePlan


PHONEME_MAP = {
    "a": "AH",
    "b": "B",
    "c": "K",
    "d": "D",
    "e": "EH",
    "f": "F",
    "g": "G",
    "h": "HH",
    "i": "IH",
    "j": "JH",
    "k": "K",
    "l": "L",
    "m": "M",
    "n": "N",
    "o": "OW",
    "p": "P",
    "q": "K",
    "r": "R",
    "s": "S",
    "t": "T",
    "u": "UH",
    "v": "V",
    "w": "W",
    "x": "KS",
    "y": "Y",
    "z": "Z",
}


def _word_to_phonemes(word: str) -> list[str]:
    phonemes: list[str] = []
    for character in word.lower():
        token = PHONEME_MAP.get(character)
        if token:
            phonemes.append(token)
    return phonemes or ["AH"]


def generate_vocal_plan(lyrics: str, melody_track: Track | None, bars: int) -> VoicePlan:
    cleaned = " ".join(lyrics.split())
    if not cleaned:
        return VoicePlan(lyrics="")

    words = cleaned.split()
    phrase_notes = melody_track.notes if melody_track else []
    default_pitch = 64
    beat_cursor = 0.0
    phoneme_frames: list[PhonemeFrame] = []
    breaths: list[float] = []

    note_index = 0
    for index, word in enumerate(words):
        phonemes = _word_to_phonemes(word)
        word_duration = max(0.75, bars * 4 / max(1, len(words)))
        frame_duration = word_duration / len(phonemes)
        note_pitch = (
            phrase_notes[min(note_index, len(phrase_notes) - 1)].pitch
            if phrase_notes
            else default_pitch
        )
        for phoneme in phonemes:
            phoneme_frames.append(
                PhonemeFrame(
                    symbol=phoneme,
                    start_beat=round(beat_cursor, 3),
                    duration_beats=round(frame_duration, 3),
                    note_pitch=note_pitch,
                )
            )
            beat_cursor += frame_duration
            note_index += 1

        if (index + 1) % 4 == 0 and beat_cursor < bars * 4:
            breaths.append(round(beat_cursor, 3))
            beat_cursor += 0.25

    return VoicePlan(lyrics=cleaned, phonemes=phoneme_frames, breaths=breaths)
