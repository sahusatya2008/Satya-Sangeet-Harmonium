from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class NoteEvent:
    pitch: int
    start: float
    duration: float
    velocity: int
    lane: str = ""


@dataclass
class PatchGenome:
    oscillator: str
    cutoff: float
    resonance: float
    attack: float
    release: float
    color: str


@dataclass
class Track:
    name: str
    instrument: str
    color: str
    volume: float
    pan: float
    notes: list[NoteEvent] = field(default_factory=list)
    patch: PatchGenome | None = None


@dataclass
class Section:
    name: str
    start_bar: int
    bars: int
    energy: float


@dataclass
class Suggestion:
    suggestion_id: str
    title: str
    description: str
    action_type: str
    confidence: float


@dataclass
class MixReport:
    headroom_db: float
    stereo_width: float
    low_end_focus: float
    recommendations: list[str] = field(default_factory=list)


@dataclass
class PhonemeFrame:
    symbol: str
    start_beat: float
    duration_beats: float
    note_pitch: int


@dataclass
class VoicePlan:
    lyrics: str
    phonemes: list[PhonemeFrame] = field(default_factory=list)
    breaths: list[float] = field(default_factory=list)


@dataclass
class ProjectState:
    project_id: str
    name: str
    genre: str
    tempo: int
    bars: int
    key: str
    mode: str
    emotion: dict[str, float]
    tracks: list[Track] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    suggestions: list[Suggestion] = field(default_factory=list)
    mix_report: MixReport | None = None
    voice_plan: VoicePlan | None = None
    events: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def note_from_dict(data: dict[str, Any]) -> NoteEvent:
    return NoteEvent(**data)


def patch_from_dict(data: dict[str, Any] | None) -> PatchGenome | None:
    if data is None:
        return None
    return PatchGenome(**data)


def track_from_dict(data: dict[str, Any]) -> Track:
    return Track(
        name=data["name"],
        instrument=data["instrument"],
        color=data["color"],
        volume=data["volume"],
        pan=data["pan"],
        notes=[note_from_dict(note) for note in data.get("notes", [])],
        patch=patch_from_dict(data.get("patch")),
    )


def section_from_dict(data: dict[str, Any]) -> Section:
    return Section(**data)


def suggestion_from_dict(data: dict[str, Any]) -> Suggestion:
    return Suggestion(**data)


def mix_report_from_dict(data: dict[str, Any] | None) -> MixReport | None:
    if data is None:
        return None
    return MixReport(**data)


def phoneme_from_dict(data: dict[str, Any]) -> PhonemeFrame:
    return PhonemeFrame(**data)


def voice_plan_from_dict(data: dict[str, Any] | None) -> VoicePlan | None:
    if data is None:
        return None
    return VoicePlan(
        lyrics=data["lyrics"],
        phonemes=[phoneme_from_dict(item) for item in data.get("phonemes", [])],
        breaths=list(data.get("breaths", [])),
    )


def project_from_dict(data: dict[str, Any]) -> ProjectState:
    return ProjectState(
        project_id=data["project_id"],
        name=data["name"],
        genre=data["genre"],
        tempo=data["tempo"],
        bars=data["bars"],
        key=data["key"],
        mode=data["mode"],
        emotion=dict(data.get("emotion", {})),
        tracks=[track_from_dict(track) for track in data.get("tracks", [])],
        sections=[section_from_dict(section) for section in data.get("sections", [])],
        suggestions=[suggestion_from_dict(item) for item in data.get("suggestions", [])],
        mix_report=mix_report_from_dict(data.get("mix_report")),
        voice_plan=voice_plan_from_dict(data.get("voice_plan")),
        events=list(data.get("events", [])),
    )
