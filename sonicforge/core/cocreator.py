from __future__ import annotations

from sonicforge.core.models import NoteEvent, ProjectState, Suggestion


def generate_suggestions(project: ProjectState) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    emotion = project.emotion
    drums = _find_track(project, "drums")
    bass = _find_track(project, "bass")
    pad = _find_track(project, "pad")
    melody = _find_track(project, "melody")

    if pad and abs(pad.pan) < 0.18:
        suggestions.append(
            Suggestion(
                suggestion_id="widen_pad",
                title="Widen the pad bed",
                description="Push the pad wider to frame the melody and create a bigger chorus image.",
                action_type="mix",
                confidence=0.83,
            )
        )
    if melody and len(melody.notes) < project.bars * 3:
        suggestions.append(
            Suggestion(
                suggestion_id="response_phrase",
                title="Add a response phrase",
                description="Answer the main melody in the second half to make the hook feel finished.",
                action_type="arrangement",
                confidence=0.76,
            )
        )
    if drums and emotion["energy"] > 60:
        suggestions.append(
            Suggestion(
                suggestion_id="open_hat_lift",
                title="Lift the final section",
                description="Add open hats and a denser hat lane in the last section to create lift.",
                action_type="rhythm",
                confidence=0.81,
            )
        )
    if bass and emotion["tension"] > 58:
        suggestions.append(
            Suggestion(
                suggestion_id="bass_octave_drive",
                title="Drive the bass harder",
                description="Layer octave jumps in the last section to add forward motion and pressure.",
                action_type="arrangement",
                confidence=0.74,
            )
        )

    return suggestions[:3]


def apply_suggestion(project: ProjectState, suggestion_id: str) -> ProjectState:
    if suggestion_id == "widen_pad":
        pad = _find_track(project, "pad")
        if pad:
            pad.pan = 0.35
    elif suggestion_id == "response_phrase":
        melody = _find_track(project, "melody")
        if melody:
            _append_response_phrase(project, melody)
    elif suggestion_id == "open_hat_lift":
        drums = _find_track(project, "drums")
        if drums:
            _add_hat_lift(project, drums)
    elif suggestion_id == "bass_octave_drive":
        bass = _find_track(project, "bass")
        if bass:
            _drive_bass(project, bass)
    project.events.append({"type": "apply_suggestion", "payload": {"id": suggestion_id}})
    return project


def _find_track(project: ProjectState, instrument: str):
    for track in project.tracks:
        if track.instrument == instrument:
            return track
    return None


def _append_response_phrase(project: ProjectState, melody_track) -> None:
    start_bar = max(0, project.bars - 4)
    phrase = [
        NoteEvent(pitch=72, start=start_bar * 4 + 1.0, duration=0.75, velocity=92),
        NoteEvent(pitch=74, start=start_bar * 4 + 2.0, duration=0.75, velocity=90),
        NoteEvent(pitch=76, start=start_bar * 4 + 3.0, duration=1.0, velocity=94),
    ]
    melody_track.notes.extend(phrase)


def _add_hat_lift(project: ProjectState, drums_track) -> None:
    start_bar = max(0, project.bars - 4)
    for bar in range(start_bar, project.bars):
        base = bar * 4
        for beat in (0.5, 1.5, 2.5, 3.5):
            drums_track.notes.append(
                NoteEvent(pitch=46, start=base + beat, duration=0.12, velocity=108, lane="lift")
            )


def _drive_bass(project: ProjectState, bass_track) -> None:
    driven: list[NoteEvent] = []
    for note in bass_track.notes:
        if note.start >= (project.bars - 4) * 4:
            driven.append(
                NoteEvent(
                    pitch=note.pitch + 12,
                    start=note.start + 0.5,
                    duration=max(0.35, note.duration - 0.2),
                    velocity=max(72, note.velocity - 8),
                    lane="drive",
                )
            )
    bass_track.notes.extend(driven)
