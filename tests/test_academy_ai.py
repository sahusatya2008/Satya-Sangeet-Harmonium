from __future__ import annotations

import unittest
from unittest.mock import patch

from sonicforge.core.academy_ai import coach_academy_user, extract_public_query
from sonicforge.core.academy_tts import humanize_speech_text, speech_profile_for


SECTIONS = [
    {
        "id": "training-path",
        "title": "Training Path",
        "eyebrow": "1. Training Path",
        "chunks": [
            "Follow the order of orientation, air stability, scale discipline, expression, accompaniment, and performance readiness.",
            "Orientation comes first because it builds visual familiarity with the keyboard and note labels.",
        ],
        "aliases": ["training path", "orientation path"],
        "targets": [
            {"alias": "orientation", "label": "Orientation", "chunkIndex": 1},
        ],
    },
    {
        "id": "posture-bellows",
        "title": "Posture And Bellows",
        "eyebrow": "3. Posture And Bellows",
        "chunks": [
            "Bellows pressure is the real musical engine. If the air is unstable, the performance sounds amateur even when the notes are correct.",
            "Pump before the tone collapses and make small controlled refills rather than dramatic pushes.",
        ],
        "aliases": ["posture and bellows", "bellows", "bellows pressure"],
        "targets": [
            {"alias": "bellows pressure", "label": "Bellows Pressure", "chunkIndex": 0},
        ],
    },
    {
        "id": "fingering",
        "title": "Fingering System",
        "eyebrow": "4. Fingering System",
        "chunks": [
            "Use the same fingering for the same pattern until it becomes automatic.",
            "Use the thumb as a stable pivot, not a frantic rescue finger.",
        ],
        "aliases": ["fingering", "fingering system"],
        "targets": [
            {"alias": "thumb use", "label": "Thumb Use", "chunkIndex": 1},
        ],
    },
]


class AcademyAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.provider_patcher = patch("sonicforge.core.academy_ai.resolve_llm_provider", return_value=None)
        self.provider_patcher.start()

    def tearDown(self) -> None:
        self.provider_patcher.stop()

    def test_extract_public_query_handles_conversational_about_phrase(self) -> None:
        self.assertEqual(
            extract_public_query("i was wondering if you could tell me something about gravity"),
            "gravity",
        )

    def test_positive_consent_starts_training(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "yes please, start the training",
                "sections": SECTIONS,
                "state": {"awaiting_consent": True, "paused": True},
            }
        )
        self.assertEqual(decision["action"], "start")
        self.assertTrue(decision["should_continue"])
        self.assertEqual(decision["section_index"], 0)

    def test_natural_pause_phrase_is_understood(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "could you stop here for a moment",
                "sections": SECTIONS,
                "state": {"paused": False, "current_section_index": 1, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "pause")

    def test_listen_interrupt_is_understood(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "listen",
                "sections": SECTIONS,
                "state": {"paused": False, "current_section_index": 1, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "wait")
        self.assertIn("listening", decision["reply"].lower())

    def test_explain_request_jumps_to_target_lesson(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "can you explain fingering in detail",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "jump")
        self.assertEqual(decision["section_index"], 2)
        self.assertTrue(decision["should_continue"])

    def test_question_returns_contextual_answer(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "what is bellows pressure and why does it matter",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 1, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertIn("Bellows Pressure", decision["reply"])
        self.assertEqual(decision["section_index"], 1)

    def test_voice_style_request_adjusts_reply_profile(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "please speak more calmly and smoothly",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["voice_style"], "calm")
        self.assertIn("calmly", decision["reply"])

    def test_basic_identity_question_is_answered(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "who are you",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertIn("voice coach", decision["reply"].lower())

    def test_name_question_is_answered_naturally(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "what's your name",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertIn("satya sangeet voice coach", decision["reply"].lower())

    def test_personal_discussion_gets_friend_like_reply(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "can we talk like friends because i feel confused and stuck",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertIn("talk", decision["reply"].lower())
        self.assertIn("friend", decision["reply"].lower())

    def test_general_music_question_uses_broader_knowledge(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "what is a raga",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertIn("melodic framework", decision["reply"].lower())

    def test_what_is_music_does_not_fall_into_manual_chunks(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "what is music",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertIn("organizing sound", decision["reply"].lower())

    def test_background_music_request_sets_ambience_mode(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "please keep soft classical music in the background",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )
        self.assertEqual(decision["action"], "answer")
        self.assertEqual(decision["ambience_mode"], "soft")

    def test_big_model_answer_is_used_for_outside_manual_questions(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value=None):
            with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value="Photosynthesis is how plants convert light into chemical energy."):
                decision = coach_academy_user(
                    {
                        "utterance": "what is photosynthesis",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("plants convert light", decision["reply"].lower())

    def test_natural_question_wording_still_gets_a_reliable_help_answer(self) -> None:
        decision = coach_academy_user(
            {
                "utterance": "what do you do for me here",
                "sections": SECTIONS,
                "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
            }
        )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("answer lesson questions", decision["reply"].lower())

    def test_llama_cpp_provider_is_used_for_open_domain_answers(self) -> None:
        with patch(
            "sonicforge.core.academy_ai.resolve_llm_provider",
            return_value={
                "kind": "llama-cpp",
                "endpoint": "http://127.0.0.1:8012/v1",
                "model": "Qwen/Test",
                "api_key": "",
            },
        ):
            with patch(
                "sonicforge.core.academy_ai.fetch_json",
                return_value={
                    "choices": [
                        {
                            "message": {
                                "content": "Gravity is the force that attracts masses toward each other."
                            }
                        }
                    ]
                },
            ):
                decision = coach_academy_user(
                    {
                        "utterance": "tell me about gravity",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("gravity", decision["reply"].lower())

    def test_public_knowledge_fallback_is_used_when_big_model_is_unavailable(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value=None):
            with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Photosynthesis is the process by which plants make food from light."):
                decision = coach_academy_user(
                    {
                        "utterance": "what is photosynthesis",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("plants make food", decision["reply"].lower())

    def test_factual_open_question_prefers_grounded_public_answer_before_model_guess(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Music is the art of organizing sound intentionally through rhythm, melody, harmony, and expression."):
            with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value="A drone is a sustained note often used under melodies."):
                decision = coach_academy_user(
                    {
                        "utterance": "what is music",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("organizing sound", decision["reply"].lower())
        self.assertNotIn("drone", decision["reply"].lower())

    def test_tell_me_about_phrase_is_treated_as_information_request(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value=None):
            with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Gravity is the force by which masses attract one another."):
                decision = coach_academy_user(
                    {
                        "utterance": "tell me about gravity",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("gravity", decision["reply"].lower())

    def test_off_topic_model_answer_is_rejected_for_open_domain_question(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Gravity is the force that attracts masses toward one another."):
            with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value="In this academy, the drone stabilizes pitch while the bellows support tone."):
                decision = coach_academy_user(
                    {
                        "utterance": "what is gravity",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("attracts masses", decision["reply"].lower())
        self.assertNotIn("academy", decision["reply"].lower())

    def test_broad_natural_outside_question_without_direct_prefix_uses_open_domain_lookup(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value=None):
            with patch(
                "sonicforge.core.academy_ai.lookup_public_knowledge",
                return_value="Gravity is the force by which masses attract one another.",
            ):
                decision = coach_academy_user(
                    {
                        "utterance": "i was wondering if you could tell me something about gravity",
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("gravity", decision["reply"].lower())

    def test_follow_up_question_uses_recent_history_topic(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value=None):
            with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Gravity works because mass curves spacetime in modern physics."):
                decision = coach_academy_user(
                    {
                        "utterance": "how does it work",
                        "sections": SECTIONS,
                        "history": [
                            {"role": "user", "text": "tell me about gravity"},
                            {"role": "assistant", "text": "Gravity is the force by which masses attract one another."},
                        ],
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("gravity", decision["reply"].lower())

    def test_better_transcript_alternative_can_be_selected(self) -> None:
        with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value=None):
            with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Gravity is the force by which masses attract one another."):
                decision = coach_academy_user(
                    {
                        "utterance": "tell me about cavity",
                        "alternatives": ["tell me about gravity", "tell me about cavity"],
                        "sections": SECTIONS,
                        "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                    }
                )

        self.assertEqual(decision["action"], "answer")
        self.assertIn("gravity", decision["reply"].lower())

    def test_hindi_language_request_is_translated_and_localized(self) -> None:
        def fake_translate(text: str, target_language: str, source_language: str = "auto") -> str | None:
            mapping = {
                ("आप कौन हैं", "en"): "who are you",
                (
                    "I am the Satya Sangeet voice coach inside the SNSAI harmonium academy. I guide your training, answer harmonium and music questions, and help you move through lessons in a calm conversational way.",
                    "hi",
                ): "मैं सत्यम् संगीत हारमोनियम अकादमी की वॉइस कोच हूँ। मैं आपके प्रशिक्षण का मार्गदर्शन करती हूँ और आपके प्रश्नों का उत्तर देती हूँ।",
            }
            return mapping.get((text, target_language), text)

        with patch("sonicforge.core.academy_ai.translate_text", side_effect=fake_translate):
            decision = coach_academy_user(
                {
                    "utterance": "आप कौन हैं",
                    "language": "hi-IN",
                    "sections": SECTIONS,
                    "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                }
            )

        self.assertEqual(decision["action"], "answer")
        self.assertEqual(decision["reply_language"], "hi")
        self.assertIn("वॉइस कोच", decision["reply"])

    def test_hindi_outside_information_question_is_answered(self) -> None:
        def fake_translate(text: str, target_language: str, source_language: str = "auto") -> str | None:
            mapping = {
                ("गुरुत्वाकर्षण क्या है", "en"): "what is gravity",
                (
                    "Gravity is the force by which masses attract one another.",
                    "hi",
                ): "प्रशिक्षण पुस्तिका के बाहर, यह संक्षिप्त उत्तर है। गुरुत्वाकर्षण वह बल है जिससे द्रव्यमान एक दूसरे को आकर्षित करते हैं।",
            }
            return mapping.get((text, target_language), text)

        with patch("sonicforge.core.academy_ai.translate_text", side_effect=fake_translate):
            with patch("sonicforge.core.academy_ai.lookup_big_model_answer", return_value=None):
                with patch("sonicforge.core.academy_ai.lookup_public_knowledge", return_value="Gravity is the force by which masses attract one another."):
                    decision = coach_academy_user(
                        {
                            "utterance": "गुरुत्वाकर्षण क्या है",
                            "language": "hi-IN",
                            "sections": SECTIONS,
                            "state": {"paused": True, "current_section_index": 0, "current_chunk_index": 0},
                        }
                    )

        self.assertEqual(decision["action"], "answer")
        self.assertEqual(decision["reply_language"], "hi")
        self.assertIn("गुरुत्वाकर्षण", decision["reply"])

    def test_tts_profile_prefers_hindi_voice_for_hindi_requests(self) -> None:
        profile = speech_profile_for("hi-IN", "calm")
        self.assertEqual(profile.language, "hi")
        self.assertEqual(profile.voice, "Lekha")
        self.assertEqual(profile.neural_voice, "hi-IN-SwaraNeural")

    def test_tts_profile_prefers_indian_neural_voice_for_english_requests(self) -> None:
        profile = speech_profile_for("en-IN", "sweet")
        self.assertEqual(profile.language, "en")
        self.assertEqual(profile.neural_voice, "en-IN-NeerjaExpressiveNeural")

    def test_tts_text_is_humanized_for_spoken_acronyms(self) -> None:
        spoken = humanize_speech_text("I am the SNSAI AI coach", "en-IN")
        self.assertIn("S N S A I", spoken)
        self.assertIn("A I", spoken)


if __name__ == "__main__":
    unittest.main()
