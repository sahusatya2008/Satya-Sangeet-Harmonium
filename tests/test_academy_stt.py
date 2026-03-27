from __future__ import annotations

import unittest

from sonicforge.core.academy_stt import (
    audio_extension_for_mime,
    confidence_for_segments,
    normalize_stt_language,
    normalize_transcript_text,
    stt_model_name_for,
)


class _FakeSegment:
    def __init__(self, avg_logprob: float) -> None:
        self.avg_logprob = avg_logprob


class AcademySpeechToTextTests(unittest.TestCase):
    def test_language_normalization(self) -> None:
        self.assertEqual(normalize_stt_language("hi-IN"), "hi")
        self.assertEqual(normalize_stt_language("en-US"), "en")
        self.assertIsNone(normalize_stt_language("fr-FR"))

    def test_mime_extension_selection(self) -> None:
        self.assertEqual(audio_extension_for_mime("audio/webm;codecs=opus"), ".webm")
        self.assertEqual(audio_extension_for_mime("audio/mp4"), ".m4a")
        self.assertEqual(audio_extension_for_mime("audio/wav"), ".wav")

    def test_transcript_normalization_repairs_common_music_terms(self) -> None:
        self.assertEqual(
            normalize_transcript_text("hamonium belows and sargum"),
            "harmonium bellows and sargam",
        )

    def test_language_specific_model_selection_prefers_english_model(self) -> None:
        self.assertEqual(stt_model_name_for("en-IN"), "base.en")
        self.assertEqual(stt_model_name_for("hi-IN"), "base")

    def test_segment_confidence_stays_in_expected_range(self) -> None:
        confidence = confidence_for_segments([_FakeSegment(-0.4), _FakeSegment(-0.6)], 0.92)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        self.assertGreater(confidence, 0.6)


if __name__ == "__main__":
    unittest.main()
