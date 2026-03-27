from __future__ import annotations

from sonicforge.core.models import MixReport, ProjectState


TARGETS = {
    "drums": {"volume": 0.88, "pan": 0.0},
    "bass": {"volume": 0.8, "pan": -0.04},
    "pad": {"volume": 0.6, "pan": 0.2},
    "melody": {"volume": 0.78, "pan": 0.08},
    "voice": {"volume": 0.84, "pan": 0.0},
}


def analyze_mix(project: ProjectState) -> MixReport:
    stereo_width = round(
        sum(abs(track.pan) for track in project.tracks) / max(1, len(project.tracks)),
        3,
    )
    low_end_notes = sum(
        1 for track in project.tracks for note in track.notes if note.pitch <= 48
    )
    total_notes = sum(len(track.notes) for track in project.tracks) or 1
    low_end_focus = round(low_end_notes / total_notes, 3)
    average_level = sum(track.volume for track in project.tracks) / max(1, len(project.tracks))
    headroom_db = round(8.5 - average_level * 6.0, 2)
    recommendations: list[str] = []
    if stereo_width < 0.12:
        recommendations.append("Increase pad or texture panning to open the stereo field.")
    if low_end_focus > 0.26:
        recommendations.append("Reduce bass note density or tighten drum sustain to clear low-end mud.")
    if headroom_db < 3.0:
        recommendations.append("Pull bus levels down before export to preserve mastering headroom.")
    if not recommendations:
        recommendations.append("Mix sits in a healthy range for a sketch and is ready for export.")
    return MixReport(
        headroom_db=headroom_db,
        stereo_width=stereo_width,
        low_end_focus=low_end_focus,
        recommendations=recommendations,
    )


def apply_auto_mix(project: ProjectState) -> ProjectState:
    for track in project.tracks:
        target = TARGETS.get(track.instrument)
        if target:
            track.volume = target["volume"]
            track.pan = target["pan"]
    project.mix_report = analyze_mix(project)
    project.events.append({"type": "auto_mix", "payload": project.mix_report.recommendations})
    return project
