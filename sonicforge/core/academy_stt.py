from __future__ import annotations

import base64
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any


STT_MODEL_CACHE: dict[tuple[str, str, str], Any] = {}
DOMAIN_INITIAL_PROMPT = (
    "This is a harmonium academy conversation. Common terms include harmonium, bellows, sargam, raga, tala, alankar, alap, taan, accompaniment, fingering, posture, and practice."
)
SPEECH_PREP_FILTER = "highpass=f=120,lowpass=f=7600,volume=1.8"
TRANSCRIPT_TERM_REPLACEMENTS = (
    (r"\bhamonium\b", "harmonium"),
    (r"\bharmoniom\b", "harmonium"),
    (r"\bbelows\b", "bellows"),
    (r"\bsargum\b", "sargam"),
    (r"\bralga\b", "raga"),
    (r"\btaal\b", "tala"),
)


def normalize_stt_language(language_code: str) -> str | None:
    normalized = str(language_code).strip().lower()
    if normalized.startswith("hi"):
        return "hi"
    if normalized.startswith("en"):
        return "en"
    return None


def stt_model_name_for(language_code: str) -> str:
    normalized_language = normalize_stt_language(language_code) or ""
    if normalized_language == "en":
        return (
            os.getenv("SATYA_ACADEMY_STT_MODEL_EN", "").strip()
            or os.getenv("SATYA_ACADEMY_STT_MODEL", "").strip()
            or "base.en"
        )
    if normalized_language == "hi":
        return (
            os.getenv("SATYA_ACADEMY_STT_MODEL_HI", "").strip()
            or os.getenv("SATYA_ACADEMY_STT_MODEL", "").strip()
            or "base"
        )
    return os.getenv("SATYA_ACADEMY_STT_MODEL", "base").strip() or "base"


def whisper_model_class() -> Any:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:  # pragma: no cover - depends on optional runtime dependency
        raise RuntimeError(
            "The deep listening model is not installed yet. Run the launcher again so it can install faster-whisper."
        ) from exc
    return WhisperModel


def get_whisper_model(language_code: str = "") -> Any:
    model_name = stt_model_name_for(language_code)
    device = os.getenv("SATYA_ACADEMY_STT_DEVICE", "cpu").strip() or "cpu"
    compute_type = os.getenv("SATYA_ACADEMY_STT_COMPUTE", "int8").strip() or "int8"
    cache_key = (model_name, device, compute_type)
    if cache_key in STT_MODEL_CACHE:
        return STT_MODEL_CACHE[cache_key]

    WhisperModel = whisper_model_class()
    download_root = Path(os.getenv("SATYA_ACADEMY_STT_CACHE", str(Path.home() / ".cache" / "satya_sangeet_whisper")))
    download_root.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(
        model_name,
        device=device,
        compute_type=compute_type,
        download_root=str(download_root),
    )
    STT_MODEL_CACHE[cache_key] = model
    return model


def prepare_stt_model() -> None:
    get_whisper_model()


def audio_extension_for_mime(mime_type: str) -> str:
    mime = str(mime_type or "").lower()
    if "ogg" in mime:
        return ".ogg"
    if "mp4" in mime or "m4a" in mime:
        return ".m4a"
    if "wav" in mime or "wave" in mime:
        return ".wav"
    return ".webm"


def ensure_ffmpeg_available() -> str:
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg is required for deep listening transcription but is not installed.")
    return ffmpeg_path


def normalize_transcript_text(text: str) -> str:
    normalized = " ".join(str(text).strip().split())
    for pattern, replacement in TRANSCRIPT_TERM_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized.strip()


def confidence_for_segments(segments: list[Any], language_probability: float) -> float:
    if not segments:
        return 0.0
    avg_logprob = 0.0
    count = 0
    for segment in segments:
        avg_logprob += float(getattr(segment, "avg_logprob", -2.0) or -2.0)
        count += 1
    avg_logprob /= max(count, 1)
    acoustic_confidence = max(0.0, min(1.0, (avg_logprob + 2.2) / 2.2))
    return round((acoustic_confidence * 0.6) + (max(0.0, min(1.0, language_probability)) * 0.4), 4)


def run_single_transcription(model: Any, wav_path: Path, language: str | None) -> dict[str, Any]:
    segments_iter, info = model.transcribe(
        str(wav_path),
        beam_size=5,
        best_of=5,
        patience=0.8,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 160, "speech_pad_ms": 120},
        condition_on_previous_text=False,
        compression_ratio_threshold=2.4,
        no_speech_threshold=0.35,
        temperature=0.0,
        initial_prompt=DOMAIN_INITIAL_PROMPT,
        language=language,
    )
    segments = [segment for segment in segments_iter if getattr(segment, "text", "").strip()]
    transcript = normalize_transcript_text(" ".join(segment.text.strip() for segment in segments))
    detected_language = getattr(info, "language", language or "") or ""
    language_probability = float(getattr(info, "language_probability", 0.0) or 0.0)
    return {
        "text": transcript,
        "language": detected_language,
        "language_probability": language_probability,
        "confidence": confidence_for_segments(segments, language_probability),
    }


def transcribe_audio_base64(audio_base64: str, mime_type: str = "audio/webm", language_code: str = "") -> dict[str, Any]:
    cleaned = str(audio_base64).strip()
    if not cleaned:
        raise ValueError("Audio payload is empty.")

    ensure_ffmpeg_available()
    audio_bytes = base64.b64decode(cleaned)
    if len(audio_bytes) < 4096:
        raise ValueError("Audio payload is too small to transcribe.")

    with tempfile.TemporaryDirectory(prefix="satya_sangeet_stt_") as temp_dir:
        temp_path = Path(temp_dir)
        source_path = temp_path / f"input{audio_extension_for_mime(mime_type)}"
        wav_path = temp_path / "speech.wav"
        source_path.write_bytes(audio_bytes)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source_path),
                "-af",
                SPEECH_PREP_FILTER,
                "-ac",
                "1",
                "-ar",
                "16000",
                "-acodec",
                "pcm_s16le",
                str(wav_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        preferred_language = normalize_stt_language(language_code)
        model = get_whisper_model(preferred_language or "")
        candidates: list[dict[str, Any]] = []

        primary = run_single_transcription(model, wav_path, preferred_language)
        if primary["text"]:
            candidates.append(primary)

        should_probe_auto = not primary["text"] or primary["confidence"] < 0.58
        if should_probe_auto:
            auto_candidate = run_single_transcription(model, wav_path, None)
            if auto_candidate["text"]:
                candidates.append(auto_candidate)

        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for candidate in candidates:
            normalized = candidate["text"].lower()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            deduped.append(candidate)

        if not deduped:
            return {
                "text": "",
                "language": preferred_language or "",
                "language_probability": 0.0,
                "confidence": 0.0,
                "alternatives": [],
            }

        deduped.sort(
            key=lambda candidate: (
                candidate["confidence"],
                len(candidate["text"]),
                candidate["language"] == preferred_language,
            ),
            reverse=True,
        )
        best = deduped[0]
        alternatives = [candidate["text"] for candidate in deduped[1:3]]
        return {
            "text": best["text"],
            "language": best["language"] or preferred_language or "",
            "language_probability": best["language_probability"],
            "confidence": best["confidence"],
            "alternatives": alternatives,
        }
