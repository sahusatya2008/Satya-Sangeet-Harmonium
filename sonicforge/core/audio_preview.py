from __future__ import annotations

import math
import struct
import wave
from array import array
from pathlib import Path
from random import Random

from sonicforge.core.models import NoteEvent, ProjectState


SAMPLE_RATE = 44_100


def render_project_bytes(project: ProjectState, sample_rate: int = SAMPLE_RATE) -> bytes:
    total_seconds = max(4.0, project.bars * 4 * 60 / project.tempo)
    total_samples = int(total_seconds * sample_rate)
    left = array("f", [0.0]) * total_samples
    right = array("f", [0.0]) * total_samples

    for track in project.tracks:
        for note in track.notes:
            _render_note(left, right, track.instrument, track.volume, track.pan, note, project.tempo, sample_rate)

    pcm = bytearray()
    for i in range(total_samples):
        l = max(-1.0, min(1.0, left[i]))
        r = max(-1.0, min(1.0, right[i]))
        pcm.extend(struct.pack("<hh", int(l * 32767), int(r * 32767)))

    return _wrap_wav_bytes(bytes(pcm), sample_rate)


def write_project_wav(project: ProjectState, path: str | Path, sample_rate: int = SAMPLE_RATE) -> Path:
    output = Path(path)
    wav_bytes = render_project_bytes(project, sample_rate)
    output.write_bytes(wav_bytes)
    return output


def _wrap_wav_bytes(pcm: bytes, sample_rate: int) -> bytes:
    output = bytearray()
    with wave.open(_ByteWriter(output), "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm)
    return bytes(output)


class _ByteWriter:
    def __init__(self, store: bytearray) -> None:
        self.store = store

    def write(self, data: bytes) -> int:
        self.store.extend(data)
        return len(data)

    def tell(self) -> int:
        return len(self.store)

    def seek(self, offset: int, whence: int = 0) -> int:
        if whence == 0 and offset == len(self.store):
            return offset
        raise OSError("ByteWriter only supports append-style writes.")

    def flush(self) -> None:
        return None


def _render_note(
    left: array,
    right: array,
    instrument: str,
    volume: float,
    pan: float,
    note: NoteEvent,
    tempo: int,
    sample_rate: int,
) -> None:
    start_index = int(note.start * 60 / tempo * sample_rate)
    duration_seconds = max(0.05, note.duration * 60 / tempo)
    note_samples = max(1, int(duration_seconds * sample_rate))
    peak = volume * (note.velocity / 127)
    left_gain = peak * (1 - max(0.0, pan))
    right_gain = peak * (1 + min(0.0, pan))
    frequency = 440.0 * (2 ** ((note.pitch - 69) / 12))
    rng = Random(note.pitch * 100_000 + int(note.start * 1000))

    for offset in range(note_samples):
        sample_index = start_index + offset
        if sample_index >= len(left):
            break
        time_sec = offset / sample_rate
        env = _envelope(time_sec, duration_seconds)
        value = _instrument_sample(instrument, frequency, time_sec, duration_seconds, rng)
        left[sample_index] += value * env * left_gain * 0.35
        right[sample_index] += value * env * right_gain * 0.35


def _envelope(time_sec: float, duration_seconds: float) -> float:
    attack = min(0.03, duration_seconds * 0.2)
    release = min(0.18, duration_seconds * 0.4)
    if time_sec < attack:
        return time_sec / max(attack, 1e-4)
    if time_sec > duration_seconds - release:
        return max(0.0, (duration_seconds - time_sec) / max(release, 1e-4))
    return 1.0


def _instrument_sample(
    instrument: str,
    frequency: float,
    time_sec: float,
    duration_seconds: float,
    rng: Random,
) -> float:
    phase = 2 * math.pi * frequency * time_sec
    if instrument == "bass":
        return math.sin(phase) * 0.8 + math.sin(phase * 2) * 0.2
    if instrument == "pad":
        return math.sin(phase) * 0.5 + math.sin(phase * 2) * 0.25 + math.sin(phase * 3) * 0.1
    if instrument == "melody":
        square = 1.0 if math.sin(phase) >= 0 else -1.0
        return square * 0.55 + math.sin(phase) * 0.25
    if instrument == "drums":
        return _drum_sample(frequency, time_sec, duration_seconds, rng)
    return math.sin(phase)


def _drum_sample(frequency: float, time_sec: float, duration_seconds: float, rng: Random) -> float:
    if frequency < 80:
        sweep = frequency * (1.8 - time_sec * 6)
        return math.sin(2 * math.pi * max(25, sweep) * time_sec) * math.exp(-12 * time_sec)
    noise = (rng.random() * 2 - 1) * math.exp(-18 * time_sec)
    body = math.sin(2 * math.pi * 180 * time_sec) * math.exp(-16 * time_sec)
    if duration_seconds < 0.18:
        return noise * 0.75
    return noise * 0.65 + body * 0.35
