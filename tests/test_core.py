from __future__ import annotations

import unittest

from sonicforge.core.session import (
    apply_mix,
    apply_project_suggestion,
    create_project,
    render_project_audio,
)


class SonicForgeCoreTests(unittest.TestCase):
    def test_create_project_builds_four_primary_tracks(self) -> None:
        project = create_project("Test", "cinematic-electronic", 118, 8, 60, 70, 48)
        self.assertEqual(len(project.tracks), 4)
        self.assertIsNotNone(project.mix_report)
        self.assertGreater(len(project.suggestions), 0)

    def test_voice_plan_is_created_when_lyrics_are_supplied(self) -> None:
        project = create_project(
            "Vocal Test",
            "alt-pop",
            120,
            8,
            72,
            64,
            40,
            lyrics="we fold the light into tomorrow",
        )
        self.assertIsNotNone(project.voice_plan)
        self.assertGreater(len(project.voice_plan.phonemes), 0)

    def test_apply_suggestion_mutates_project(self) -> None:
        project = create_project("Suggest", "alt-pop", 116, 8, 58, 66, 62)
        pad_before = next(track for track in project.tracks if track.instrument == "pad").pan
        project = apply_project_suggestion(project, "widen_pad")
        pad_after = next(track for track in project.tracks if track.instrument == "pad").pan
        self.assertNotEqual(pad_before, pad_after)

    def test_auto_mix_updates_mix_report(self) -> None:
        project = create_project("Mix", "alt-pop", 110, 8, 48, 55, 44)
        before = project.mix_report.headroom_db
        project = apply_mix(project)
        self.assertNotEqual(before, project.mix_report.headroom_db)

    def test_audio_renderer_outputs_wav_bytes(self) -> None:
        project = create_project("Render", "alt-pop", 110, 8, 48, 55, 44)
        wav_bytes = render_project_audio(project)
        self.assertTrue(wav_bytes.startswith(b"RIFF"))


if __name__ == "__main__":
    unittest.main()
