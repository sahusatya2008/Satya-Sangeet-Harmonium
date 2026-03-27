from __future__ import annotations

import asyncio
from dataclasses import dataclass
import importlib.util
from pathlib import Path
import re
import subprocess
import tempfile


AVAILABLE_VOICES_CACHE: set[str] | None = None


@dataclass(frozen=True)
class AcademySpeechProfile:
    voice: str
    rate: int
    language: str
    neural_voice: str
    neural_rate: str
    neural_pitch: str
    neural_volume: str


@dataclass(frozen=True)
class AcademySpeechRender:
    audio_bytes: bytes
    voice_name: str
    content_type: str
    provider: str


def normalize_tts_language(language_code: str) -> str:
    return "hi" if str(language_code).lower().startswith("hi") else "en"


def available_system_voices() -> set[str]:
    global AVAILABLE_VOICES_CACHE
    if AVAILABLE_VOICES_CACHE is not None:
        return AVAILABLE_VOICES_CACHE

    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        AVAILABLE_VOICES_CACHE = set()
        return AVAILABLE_VOICES_CACHE

    voices: set[str] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        voice_name = line.split("  ", 1)[0].strip()
        if voice_name:
            voices.add(voice_name)

    AVAILABLE_VOICES_CACHE = voices
    return voices


def pick_supported_voice(candidates: list[str], fallback: str) -> str:
    available = available_system_voices()
    if not available:
        return fallback
    for candidate in candidates:
        if candidate in available:
            return candidate
    return fallback if fallback in available else sorted(available)[0]


def speech_profile_for(language_code: str, voice_style: str = "") -> AcademySpeechProfile:
    language = normalize_tts_language(language_code)
    normalized_style = voice_style.strip().lower()

    if language == "hi":
        voice = pick_supported_voice(["Lekha"], "Lekha")
        rate = 156
        neural_voice = "hi-IN-SwaraNeural"
        neural_rate = "-2%"
        neural_pitch = "+0Hz"
        neural_volume = "+2%"
        if normalized_style == "clear":
            rate = 154
            neural_voice = "hi-IN-SwaraNeural"
            neural_rate = "-1%"
        elif normalized_style == "brisk":
            rate = 165
            neural_voice = "hi-IN-MadhurNeural"
            neural_rate = "+2%"
            neural_volume = "+1%"
        elif normalized_style in {"sweet", "calm"}:
            rate = 154
            neural_voice = "hi-IN-SwaraNeural"
            neural_rate = "-3%"
        return AcademySpeechProfile(
            voice=voice,
            rate=rate,
            language="hi",
            neural_voice=neural_voice,
            neural_rate=neural_rate,
            neural_pitch=neural_pitch,
            neural_volume=neural_volume,
        )

    if normalized_style == "clear":
        voice = pick_supported_voice(["Flo (English (UK))", "Rishi", "Daniel"], "Flo (English (UK))")
        rate = 154
        neural_voice = "en-IN-NeerjaNeural"
        neural_rate = "-1%"
        neural_pitch = "+0Hz"
        neural_volume = "+1%"
    elif normalized_style == "brisk":
        voice = pick_supported_voice(["Rishi", "Eddy (English (UK))", "Daniel"], "Rishi")
        rate = 168
        neural_voice = "en-IN-PrabhatNeural"
        neural_rate = "+2%"
        neural_pitch = "+0Hz"
        neural_volume = "+0%"
    elif normalized_style == "sweet":
        voice = pick_supported_voice(["Flo (English (UK))", "Karen", "Samantha"], "Flo (English (UK))")
        rate = 154
        neural_voice = "en-IN-NeerjaExpressiveNeural"
        neural_rate = "-3%"
        neural_pitch = "+0Hz"
        neural_volume = "+2%"
    else:
        voice = pick_supported_voice(["Flo (English (UK))", "Rishi", "Daniel"], "Flo (English (UK))")
        rate = 154
        neural_voice = "en-IN-NeerjaExpressiveNeural"
        neural_rate = "-2%"
        neural_pitch = "+0Hz"
        neural_volume = "+1%"

    return AcademySpeechProfile(
        voice=voice,
        rate=rate,
        language="en",
        neural_voice=neural_voice,
        neural_rate=neural_rate,
        neural_pitch=neural_pitch,
        neural_volume=neural_volume,
    )


def humanize_speech_text(text: str, language_code: str) -> str:
    language = normalize_tts_language(language_code)
    cleaned = " ".join(text.strip().split())
    cleaned = cleaned.replace("`", "")
    cleaned = re.sub(r"\s*[:;]\s*", ". ", cleaned)
    cleaned = re.sub(r"\s*[–—-]\s*", ", ", cleaned)
    cleaned = re.sub(r"\.\.+", ".", cleaned)
    cleaned = re.sub(r"([,.!?])(?=[^\s])", r"\1 ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if language == "hi":
        replacements = {
            "SNSAI": "एस एन एस ए आई",
            "AI": "ए आई",
            "TTS": "टी टी एस",
            "STT": "एस टी टी",
        }
    else:
        replacements = {
            "SNSAI": "S N S A I",
            "AI": "A I",
            "TTS": "T T S",
            "STT": "S T T",
        }

    for source, target in replacements.items():
        cleaned = re.sub(rf"\b{re.escape(source)}\b", target, cleaned)

    cleaned = re.sub(r"\s+,", ",", cleaned)
    cleaned = re.sub(r"\s+\.", ".", cleaned)
    if cleaned and cleaned[-1] not in ".!?।":
        cleaned += "."
    return cleaned


def edge_tts_available() -> bool:
    return importlib.util.find_spec("edge_tts") is not None


def synthesize_with_edge_tts(text: str, profile: AcademySpeechProfile) -> AcademySpeechRender | None:
    if not edge_tts_available():
        return None

    try:
        import edge_tts
    except ImportError:
        return None

    with tempfile.TemporaryDirectory(prefix="satya_sangeet_edge_tts_") as temp_dir:
        temp_path = Path(temp_dir)
        mp3_path = temp_path / "speech.mp3"

        async def render() -> None:
            communicate = edge_tts.Communicate(
                text,
                profile.neural_voice,
                rate=profile.neural_rate,
                volume=profile.neural_volume,
                pitch=profile.neural_pitch,
                boundary="SentenceBoundary",
            )
            await communicate.save(str(mp3_path))

        try:
            asyncio.run(render())
        except Exception:
            return None

        if not mp3_path.exists():
            return None

        return AcademySpeechRender(
            audio_bytes=mp3_path.read_bytes(),
            voice_name=profile.neural_voice,
            content_type="audio/mpeg",
            provider="edge-tts",
        )


def synthesize_with_system_voice(text: str, profile: AcademySpeechProfile) -> AcademySpeechRender:
    cleaned = " ".join(text.strip().split())
    with tempfile.TemporaryDirectory(prefix="satya_sangeet_tts_") as temp_dir:
        temp_path = Path(temp_dir)
        aiff_path = temp_path / "speech.aiff"
        wav_path = temp_path / "speech.wav"

        subprocess.run(
            ["say", "-v", profile.voice, "-r", str(profile.rate), "-o", str(aiff_path), cleaned],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["afconvert", "-f", "WAVE", "-d", "LEI16", str(aiff_path), str(wav_path)],
            check=True,
            capture_output=True,
            text=True,
        )

        return AcademySpeechRender(
            audio_bytes=wav_path.read_bytes(),
            voice_name=profile.voice,
            content_type="audio/wav",
            provider="macos-say",
        )


def synthesize_academy_speech(text: str, language_code: str = "en-IN", voice_style: str = "") -> AcademySpeechRender:
    cleaned = humanize_speech_text(text, language_code)
    if not cleaned:
        raise ValueError("Speech text is empty.")
    if len(cleaned) > 1800:
        raise ValueError("Speech text is too long.")

    profile = speech_profile_for(language_code, voice_style)
    neural_render = synthesize_with_edge_tts(cleaned, profile)
    if neural_render is not None:
        return neural_render
    return synthesize_with_system_voice(cleaned, profile)
