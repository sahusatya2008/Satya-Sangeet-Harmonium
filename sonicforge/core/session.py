from __future__ import annotations

from sonicforge.core.audio_preview import render_project_bytes
from sonicforge.core.cocreator import apply_suggestion, generate_suggestions
from sonicforge.core.composer import compose_project
from sonicforge.core.mixmaster import analyze_mix, apply_auto_mix
from sonicforge.core.models import ProjectState
from sonicforge.core.voice import generate_vocal_plan


def create_project(
    name: str,
    genre: str,
    tempo: int,
    bars: int,
    valence: float,
    energy: float,
    tension: float,
    lyrics: str = "",
    seed: int | None = None,
) -> ProjectState:
    emotion = {
        "valence": float(valence),
        "energy": float(energy),
        "tension": float(tension),
    }
    project = compose_project(name, genre, tempo, bars, emotion, seed)
    melody = next((track for track in project.tracks if track.instrument == "melody"), None)
    if lyrics.strip():
        project.voice_plan = generate_vocal_plan(lyrics, melody, bars)
    project.mix_report = analyze_mix(project)
    project.suggestions = generate_suggestions(project)
    return project


def refresh_project(project: ProjectState) -> ProjectState:
    project.mix_report = analyze_mix(project)
    project.suggestions = generate_suggestions(project)
    return project


def apply_mix(project: ProjectState) -> ProjectState:
    return refresh_project(apply_auto_mix(project))


def apply_project_suggestion(project: ProjectState, suggestion_id: str) -> ProjectState:
    project = apply_suggestion(project, suggestion_id)
    return refresh_project(project)


def render_project_audio(project: ProjectState) -> bytes:
    return render_project_bytes(project)
