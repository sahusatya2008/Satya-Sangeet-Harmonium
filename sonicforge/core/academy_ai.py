from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import json
import os
import re
import shutil
from typing import Any
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


STOP_WORDS = {
    "a",
    "about",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "do",
    "for",
    "from",
    "go",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "please",
    "should",
    "so",
    "start",
    "teach",
    "tell",
    "that",
    "the",
    "this",
    "to",
    "we",
    "what",
    "where",
    "why",
    "with",
    "you",
}

POSITIVE_PATTERNS = (
    "yes",
    "yes please",
    "sure",
    "okay",
    "ok",
    "all right",
    "alright",
    "please begin",
    "please start",
    "start explaining",
    "begin the training",
    "go ahead",
)

NEGATIVE_PATTERNS = (
    "no",
    "not now",
    "later",
    "maybe later",
    "wait for now",
)

PAUSE_PATTERNS = (
    "stop",
    "pause",
    "hold on",
    "wait a moment",
    "wait for a moment",
    "be quiet",
    "enough for now",
    "stop here",
)

LISTEN_PATTERNS = (
    "listen",
    "listen to me",
    "hear me out",
    "let me speak",
    "just listen",
    "one second",
    "one moment",
    "wait listen",
)

RESUME_PATTERNS = (
    "continue",
    "resume",
    "go on",
    "carry on",
    "keep going",
    "proceed",
)

RESTART_PATTERNS = (
    "from beginning",
    "from start",
    "restart",
    "start again",
    "begin again",
)

LOCATION_PATTERNS = (
    "where were we",
    "where are we",
    "which lesson",
    "current lesson",
    "what section",
    "what are we on",
)

REPEAT_PATTERNS = (
    "repeat that",
    "say that again",
    "repeat please",
    "repeat the last part",
)

VOICE_CALM_PATTERNS = (
    "speak slowly",
    "talk slowly",
    "speak more slowly",
    "more calmly",
    "be calm",
    "speak calmly",
    "softly",
    "smoothly",
    "gentle",
)

VOICE_CLEAR_PATTERNS = (
    "more clear",
    "more clearly",
    "clear voice",
    "clearer",
    "pronounce",
    "properly",
)

VOICE_BRISK_PATTERNS = (
    "speak faster",
    "talk faster",
    "speed up",
    "faster please",
)

VOICE_SWEET_PATTERNS = (
    "cute voice",
    "sweet voice",
    "soft voice",
    "gentle voice",
    "feminine voice",
)

AMBIENCE_ON_PATTERNS = (
    "background music",
    "classical music",
    "music in the background",
    "play music",
    "turn on music",
    "start music",
    "start background music",
)

AMBIENCE_OFF_PATTERNS = (
    "stop music",
    "turn off music",
    "music off",
    "stop background music",
    "turn off background music",
)

AMBIENCE_SOFT_PATTERNS = (
    "lower the music",
    "music softer",
    "soft background music",
    "soft classical music",
    "keep the music low",
    "reduce the music",
)

EXPLAIN_VERBS = (
    "explain",
    "teach",
    "show",
    "go to",
    "move to",
    "take me to",
    "start from",
    "open",
    "cover",
)

QUESTION_OPENERS = (
    "what",
    "why",
    "how",
    "when",
    "which",
    "can you",
    "could you",
    "would you",
    "do i",
    "should i",
)

INFO_REQUEST_PREFIXES = (
    "tell me about ",
    "explain ",
    "define ",
    "what's ",
    "whats ",
    "who is ",
    "where is ",
    "when is ",
    "why does ",
    "how can i ",
    "can you explain ",
    "please explain ",
    "can you tell me about ",
    "give me information about ",
    "i want to know about ",
    "i want information about ",
    "help me understand ",
    "meaning of ",
    "describe ",
)

OPEN_DOMAIN_HINTS = (
    "i was wondering",
    "i am wondering",
    "i m wondering",
    "do you know",
    "have you heard of",
    "can i ask",
    "let me ask",
    "i want to ask",
    "could you tell me",
    "could you explain",
    "can you tell me",
    "help me understand",
    "i want to understand",
    "i am curious about",
    "i m curious about",
    "curious about",
    "tell me something about",
    "give me some information about",
    "i need information about",
)

PERSONAL_DISCUSSION_PATTERNS = (
    "can we talk",
    "talk to me",
    "talk like a friend",
    "speak like a friend",
    "be my friend",
    "i need advice",
    "help me decide",
    "personal question",
    "i need help",
    "i feel ",
    "i am feeling ",
    "i m feeling ",
    "i am confused",
    "i m confused",
    "i am worried",
    "i m worried",
    "i am stressed",
    "i m stressed",
    "i am upset",
    "i m upset",
    "i am sad",
    "i m sad",
    "i am frustrated",
    "i m frustrated",
    "i feel stuck",
    "i am stuck",
    "i m stuck",
)

FOLLOW_UP_PATTERNS = (
    "tell me more",
    "explain more",
    "more about that",
    "more about it",
    "what about that",
    "what about it",
    "and why",
    "and how",
    "why is that",
    "how does it work",
    "how does that work",
)

FOLLOW_UP_PRONOUNS = {"it", "that", "this", "those", "these", "they", "them"}

TERM_REPLACEMENTS = (
    (r"\bbellows\b", "bellows"),
    (r"\bbelows\b", "bellows"),
    (r"\bbellowss\b", "bellows"),
    (r"\bsargum\b", "sargam"),
    (r"\bsargamm\b", "sargam"),
    (r"\bralga\b", "raga"),
    (r"\bragga\b", "raga"),
    (r"\bragaa\b", "raga"),
    (r"\btaal\b", "tala"),
    (r"\ballankar\b", "alankar"),
    (r"\balankaar\b", "alankar"),
    (r"\btaanh\b", "taan"),
    (r"\bhamonium\b", "harmonium"),
    (r"\bharmoniom\b", "harmonium"),
)

GENERAL_CONVERSATION_ENTRIES = (
    {
        "aliases": ("who are you", "what are you", "tell me about yourself"),
        "reply": (
            "I am the Satya Sangeet voice coach inside the SNSAI harmonium academy. "
            "I guide your training, answer harmonium and music questions, and help you move through lessons in a calm conversational way."
        ),
    },
    {
        "aliases": ("how are you", "how are you doing", "are you okay"),
        "reply": (
            "I am doing well and I am fully focused on helping you practice calmly, clearly, and with good musical understanding."
        ),
    },
    {
        "aliases": ("what is your name", "what's your name", "whats your name"),
        "reply": (
            "My name here is the Satya Sangeet voice coach. I am the academy assistant designed to guide your harmonium learning and answer your questions calmly."
        ),
    },
    {
        "aliases": ("what do you do", "what can you do", "how can you help me"),
        "reply": (
            "I can explain the harmonium training path, answer lesson questions, pause and resume teaching, jump to any topic, repeat parts slowly, "
            "guide your practice flow, and answer a wide range of basic music and general conversation questions."
        ),
    },
    {
        "aliases": ("are you listening", "can you hear me", "did you hear me"),
        "reply": (
            "Yes. I am here and ready to listen, answer questions, and guide the next step of your training. If the microphone is unclear, you can also type to me below."
        ),
    },
    {
        "aliases": ("who made you", "who created you", "who built you"),
        "reply": (
            "I am the academy assistant for Satya Sangeet Harmonium by SNSAI, built for this learning experience and presented inside the developer's harmonium environment."
        ),
    },
    {
        "aliases": ("thank you", "thanks", "thank you so much"),
        "reply": "You are always welcome. I am happy to stay with you and keep the practice flow calm and clear.",
    },
    {
        "aliases": ("hello", "hi", "good morning", "good evening", "good afternoon"),
        "reply": "Hello. I am here with you. Whenever you are ready, ask me anything or let me guide the next part of your training.",
    },
)

GENERAL_KNOWLEDGE_ENTRIES = (
    {
        "aliases": ("what is music", "define music", "tell me about music"),
        "reply": (
            "Music is the art of organizing sound through elements like rhythm, melody, harmony, tone, texture, and expression so that it communicates feeling, structure, or meaning."
        ),
    },
    {
        "aliases": ("what is harmonium", "what is a harmonium", "tell me about harmonium"),
        "reply": (
            "A harmonium is a free reed keyboard instrument that creates sound when air from the bellows passes through tuned metal reeds. "
            "In Indian music it is widely used for accompaniment, teaching, devotional singing, and melodic guidance."
        ),
    },
    {
        "aliases": ("what is raga", "what is a raga", "define raga"),
        "reply": (
            "A raga is a melodic framework in Indian classical music. It is not just a scale. "
            "It includes characteristic note movement, important resting tones, emotional color, and typical phrase shapes."
        ),
    },
    {
        "aliases": ("what is tala", "what is a tala", "define tala"),
        "reply": (
            "A tala is a rhythmic cycle in Indian music. It organizes beats into a repeating pattern, often with strong and light points that shape phrasing and improvisation."
        ),
    },
    {
        "aliases": ("what is sargam", "define sargam", "what does sargam mean"),
        "reply": (
            "Sargam is the note naming system using Sa, Re, Ga, Ma, Pa, Dha, and Ni. "
            "It is the Indian equivalent of syllables like Do, Re, Mi, and it is used for teaching, practice, and melodic articulation."
        ),
    },
    {
        "aliases": ("what is bellows pressure", "define bellows pressure"),
        "reply": (
            "Bellows pressure is the steadiness and strength of the air you push through the harmonium reeds. It matters because uneven air makes the tone wobble, weaken, or sound untrained even when the notes are correct."
        ),
    },
    {
        "aliases": ("what is melody", "define melody"),
        "reply": (
            "Melody is a sequence of musical notes heard as one connected line or tune. It is usually the part of the music people remember and sing back."
        ),
    },
    {
        "aliases": ("what is harmony", "define harmony"),
        "reply": (
            "Harmony is the way different notes sound together at the same time to support, color, or deepen a melody."
        ),
    },
    {
        "aliases": ("what is rhythm", "define rhythm"),
        "reply": (
            "Rhythm is the pattern of timing in music. It controls the placement of beats, accents, motion, and groove."
        ),
    },
    {
        "aliases": ("what is alankar", "what is an alankar", "define alankar"),
        "reply": (
            "An alankar is a patterned melodic exercise. It trains note accuracy, fingering, speed control, and phrase stability across a tonic or scale."
        ),
    },
    {
        "aliases": ("what is alap", "what is an alap", "define alap"),
        "reply": (
            "An alap is a slow and exploratory introduction to a raga. It focuses on mood, note relationships, and phrase identity rather than rhythmic speed."
        ),
    },
    {
        "aliases": ("what is taan", "what is a taan", "define taan"),
        "reply": (
            "A taan is a fast melodic run or phrase, usually used to show agility, tonal control, and raga command while still landing musically."
        ),
    },
    {
        "aliases": ("what is drone", "what is a drone in music", "why use a drone"),
        "reply": (
            "A drone is a sustained tonal reference, often centered on Sa and Pa. It stabilizes pitch perception, supports intonation, and keeps the melodic space grounded."
        ),
    },
)

LLM_PROVIDER_CACHE: dict[str, Any] = {"resolved": False, "provider": None}
TRANSLATION_CACHE: dict[tuple[str, str, str], str] = {}
PUBLIC_KNOWLEDGE_CACHE: dict[str, str] = {}
VALID_MODEL_ACTIONS = {"answer", "pause", "resume", "restart", "repeat", "jump", "wait", "start"}
VALID_VOICE_STYLES = {"", "sweet", "calm", "clear", "brisk"}
VALID_AMBIENCE_MODES = {"", "on", "off", "soft"}
FACTUAL_INFO_PREFIXES = (
    "what is ",
    "what are ",
    "who is ",
    "who are ",
    "where is ",
    "when is ",
    "why is ",
    "why are ",
    "define ",
    "meaning of ",
    "tell me about ",
    "tell me something about ",
    "can you tell me about ",
    "could you tell me about ",
    "give me information about ",
    "give me some information about ",
    "i want to know about ",
    "help me understand ",
    "describe ",
)
OPEN_DOMAIN_ACADEMY_BIAS_TERMS = {
    "academy",
    "lesson",
    "training",
    "harmonium",
    "bellows",
    "fingering",
    "sargam",
    "raga",
    "tala",
    "alankar",
    "alap",
    "taan",
    "drone",
    "keyboard",
    "practice",
}
PREFERRED_OLLAMA_MODELS = (
    "qwen2.5:3b",
    "qwen2.5:1.5b",
    "qwen2.5:0.5b",
    "gemma3:4b",
    "gemma3:1b",
)
DEFAULT_LLAMA_CPP_ENDPOINT = os.getenv("SATYA_ACADEMY_LLAMA_CPP_ENDPOINT", "http://127.0.0.1:8012/v1").strip() or "http://127.0.0.1:8012/v1"


@dataclass
class AcademyTarget:
    alias: str
    label: str
    chunk_index: int


@dataclass
class AcademySection:
    id: str
    title: str
    eyebrow: str
    chunks: list[str]
    aliases: list[str]
    targets: list[AcademyTarget]


@dataclass
class AcademyCoachState:
    enabled: bool = False
    paused: bool = True
    awaiting_consent: bool = False
    current_section_index: int = 0
    current_chunk_index: int = 0


@dataclass
class ConversationTurn:
    role: str
    text: str


@dataclass
class AcademyDecision:
    action: str
    reply: str
    section_index: int | None = None
    chunk_index: int | None = None
    should_continue: bool = False
    focus_label: str = ""
    voice_style: str = ""
    ambience_mode: str = ""
    reply_language: str = "en"

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "reply": self.reply,
            "section_index": self.section_index,
            "chunk_index": self.chunk_index,
            "should_continue": self.should_continue,
            "focus_label": self.focus_label,
            "voice_style": self.voice_style,
            "ambience_mode": self.ambience_mode,
            "reply_language": self.reply_language,
        }


@dataclass
class AcademyLLMStatus:
    available: bool
    provider: str
    model: str
    endpoint: str
    detail: str
    command_hint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "provider": self.provider,
            "model": self.model,
            "endpoint": self.endpoint,
            "detail": self.detail,
            "command_hint": self.command_hint,
        }


def normalize_text(text: str) -> str:
    normalized = text.lower()
    for pattern, replacement in TERM_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", normalized)).strip()


def tokenize(text: str) -> list[str]:
    tokens = []
    for token in normalize_text(text).split():
        if token in STOP_WORDS:
            continue
        if token.endswith("ing") and len(token) > 5:
            token = token[:-3]
        elif token.endswith("ed") and len(token) > 4:
            token = token[:-2]
        elif token.endswith("s") and len(token) > 4:
            token = token[:-1]
        tokens.append(token)
    return tokens


def raw_words(text: str) -> list[str]:
    return [word for word in normalize_text(text).split() if word]


def phrase_present(command: str, patterns: tuple[str, ...]) -> bool:
    for pattern in patterns:
        normalized_pattern = normalize_text(pattern)
        if not normalized_pattern:
            continue
        if re.search(rf"(?:^|\s){re.escape(normalized_pattern)}(?:$|\s)", command):
            return True
    return False


def utterance_is_question(command: str) -> bool:
    return any(command.startswith(opener) for opener in QUESTION_OPENERS) or "?" in command


def looks_like_information_request(command: str) -> bool:
    if utterance_is_question(command):
        return True
    return any(command.startswith(prefix) for prefix in INFO_REQUEST_PREFIXES)


def looks_like_factual_information_request(command: str) -> bool:
    if has_explicit_control_intent(command) or has_navigation_intent(command):
        return False
    if looks_like_personal_discussion(command):
        return False
    if any(command.startswith(prefix) for prefix in FACTUAL_INFO_PREFIXES):
        return True
    if utterance_is_question(command):
        return not any(
            command.startswith(prefix)
            for prefix in (
                "should i",
                "can i",
                "how can i",
                "could you help",
                "can you help",
            )
        )
    return False


def content_words(command: str) -> list[str]:
    return [word for word in raw_words(command) if word not in STOP_WORDS]


def looks_like_open_domain_query(command: str) -> bool:
    if looks_like_information_request(command) or looks_like_follow_up(command):
        return True
    if any(hint in command for hint in OPEN_DOMAIN_HINTS):
        return True
    if " about " in f" {command} " and len(content_words(command)) >= 3:
        return True
    return len(content_words(command)) >= 6 and not looks_like_personal_discussion(command)


def looks_like_follow_up(command: str) -> bool:
    if any(pattern in command for pattern in FOLLOW_UP_PATTERNS):
        return True
    words = raw_words(command)
    if len(words) <= 5 and any(word in FOLLOW_UP_PRONOUNS for word in words):
        return True
    return command.startswith("and ")


def looks_like_personal_discussion(command: str) -> bool:
    if any(command.startswith(pattern) or pattern in command for pattern in PERSONAL_DISCUSSION_PATTERNS):
        return True

    words = set(raw_words(command))
    emotional_hints = {
        "feel",
        "feeling",
        "friend",
        "talk",
        "personal",
        "advice",
        "decide",
        "confused",
        "worried",
        "stressed",
        "upset",
        "sad",
        "frustrated",
        "lonely",
        "problem",
        "issue",
        "stuck",
        "help",
    }
    return len(words) >= 4 and bool(words & emotional_hints)


def has_navigation_intent(command: str) -> bool:
    return phrase_present(
        command,
        EXPLAIN_VERBS
        + (
            "lesson",
            "topic",
            "section",
            "training path",
            "jump to",
            "move to",
            "take me to",
        ),
    )


def has_explicit_control_intent(command: str) -> bool:
    return phrase_present(
        command,
        PAUSE_PATTERNS + LISTEN_PATTERNS + RESUME_PATTERNS + RESTART_PATTERNS + LOCATION_PATTERNS + REPEAT_PATTERNS,
    )


def is_listen_interrupt(command: str) -> bool:
    return phrase_present(command, LISTEN_PATTERNS) and len(raw_words(command)) <= 4 and not utterance_is_question(command)


def section_from_payload(data: dict[str, Any]) -> AcademySection:
    return AcademySection(
        id=str(data.get("id", "")),
        title=str(data.get("title", "")),
        eyebrow=str(data.get("eyebrow", "")),
        chunks=[str(item) for item in data.get("chunks", [])],
        aliases=[str(item) for item in data.get("aliases", [])],
        targets=[
            AcademyTarget(
                alias=str(target.get("alias", "")),
                label=str(target.get("label", "")),
                chunk_index=int(target.get("chunkIndex", 0)),
            )
            for target in data.get("targets", [])
        ],
    )


def state_from_payload(data: dict[str, Any]) -> AcademyCoachState:
    return AcademyCoachState(
        enabled=bool(data.get("enabled", False)),
        paused=bool(data.get("paused", True)),
        awaiting_consent=bool(data.get("awaiting_consent", False)),
        current_section_index=int(data.get("current_section_index", 0)),
        current_chunk_index=int(data.get("current_chunk_index", 0)),
    )


def history_from_payload(items: list[dict[str, Any]] | None) -> list[ConversationTurn]:
    history: list[ConversationTurn] = []
    for item in items or []:
        role = str(item.get("role", "")).strip().lower()
        text = str(item.get("text", "")).strip()
        if role not in {"user", "assistant"} or not text:
            continue
        history.append(ConversationTurn(role=role, text=text))
    return history[-12:]


def score_phrase_match(command: str, command_tokens: list[str], phrase: str) -> float:
    normalized_phrase = normalize_text(phrase)
    if not normalized_phrase:
        return 0.0
    if re.search(rf"(?:^|\s){re.escape(normalized_phrase)}(?:$|\s)", command):
        return 8.0 + min(len(normalized_phrase) / 18.0, 3.0)

    phrase_tokens = tokenize(normalized_phrase)
    if not phrase_tokens:
        return 0.0

    overlap = len(set(command_tokens) & set(phrase_tokens))
    if not overlap:
        ratio = SequenceMatcher(None, command, normalized_phrase).ratio()
        return ratio * 1.3

    coverage = overlap / len(set(phrase_tokens))
    density = overlap / max(len(set(command_tokens)), 1)
    ratio = SequenceMatcher(None, command, normalized_phrase).ratio()
    contiguous_bonus = 1.5 if all(token in command_tokens for token in phrase_tokens) else 0.0
    return (coverage * 5.0) + (density * 2.2) + (ratio * 1.8) + contiguous_bonus


def find_target(command: str, sections: list[AcademySection]) -> dict[str, Any] | None:
    command_tokens = tokenize(command)
    best: dict[str, Any] | None = None

    for section_index, section in enumerate(sections):
        candidates = [
            {"label": section.title, "phrase": section.title, "chunk_index": 0, "priority": 0.2},
            {"label": section.eyebrow, "phrase": section.eyebrow, "chunk_index": 0, "priority": 0.1},
            {"label": section.title, "phrase": section.id.replace("-", " "), "chunk_index": 0, "priority": 0.1},
            {"label": section.title, "phrase": f"section {section_index + 1}", "chunk_index": 0, "priority": 0.05},
        ]
        candidates.extend(
            {"label": section.title, "phrase": alias, "chunk_index": 0, "priority": 0.25}
            for alias in section.aliases
        )
        candidates.extend(
            {"label": target.label, "phrase": target.alias, "chunk_index": target.chunk_index, "priority": 0.7}
            for target in section.targets
        )

        for candidate in candidates:
            score = score_phrase_match(command, command_tokens, candidate["phrase"]) + candidate["priority"]
            if score < 3.1:
                continue
            if best is None or score > best["score"]:
                best = {
                    "section_index": section_index,
                    "chunk_index": candidate["chunk_index"],
                    "label": candidate["label"],
                    "score": score,
                }

    return best


def summarize_sentences(text: str, max_sentences: int = 2) -> str:
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.replace("..", "."))
        if sentence.strip()
    ]
    if not sentences:
        return text.strip()
    return " ".join(sentences[:max_sentences]).strip()


def score_chunk_match(command: str, chunk: str) -> float:
    query_tokens = set(tokenize(command))
    chunk_tokens = set(tokenize(chunk))
    if not chunk_tokens:
        return 0.0
    overlap = len(query_tokens & chunk_tokens)
    jaccard = overlap / len(chunk_tokens | query_tokens) if query_tokens else 0.0
    phrase_bonus = 2.0 if normalize_text(chunk)[:80] and normalize_text(chunk)[:80] in command else 0.0
    ratio = SequenceMatcher(None, normalize_text(command), normalize_text(chunk[:240])).ratio()
    return (overlap * 1.6) + (jaccard * 6.0) + (ratio * 2.4) + phrase_bonus


def top_chunk_matches(command: str, sections: list[AcademySection], target: dict[str, Any] | None) -> list[tuple[float, int, int, str]]:
    matches: list[tuple[float, int, int, str]] = []
    preferred_section = target["section_index"] if target else None

    for section_index, section in enumerate(sections):
        for chunk_index, chunk in enumerate(section.chunks):
            score = score_chunk_match(command, chunk)
            if preferred_section is not None and section_index == preferred_section:
                score += 1.4
            if target and preferred_section == section_index and chunk_index == target["chunk_index"]:
                score += 2.2
            if score <= 1.6:
                continue
            matches.append((score, section_index, chunk_index, chunk))

    matches.sort(key=lambda item: item[0], reverse=True)
    return matches[:4]


def build_answer(command: str, sections: list[AcademySection], target: dict[str, Any] | None, state: AcademyCoachState) -> AcademyDecision | None:
    matches = top_chunk_matches(command, sections, target)
    if not matches:
        return None

    lead_score, lead_section_index, lead_chunk_index, lead_chunk = matches[0]
    if target is None and lead_score < 4.6:
        return None
    section = sections[lead_section_index]
    combined = " ".join(summarize_sentences(chunk, 2) for _, _, _, chunk in matches[:2])
    answer = summarize_sentences(combined, 3)
    prefix = answer_prefix(command, section.title, target["label"] if target else "")
    reply = f"{prefix} {answer}".strip()

    should_continue = False
    if phrase_present(command, RESUME_PATTERNS) or "then continue" in command or "and continue" in command:
        should_continue = True

    return AcademyDecision(
        action="answer",
        reply=reply,
        section_index=lead_section_index,
        chunk_index=lead_chunk_index,
        should_continue=should_continue,
        focus_label=target["label"] if target else section.title,
    )


def answer_prefix(command: str, section_title: str, focus_label: str) -> str:
    if "how" in command:
        return f"Here is the practical way to approach {focus_label or section_title}."
    if "why" in command:
        return f"The reason {focus_label or section_title} matters is this."
    if "what" in command:
        return f"{focus_label or section_title} means this."
    if "should" in command or "can you" in command or "could you" in command:
        return f"Yes. For {focus_label or section_title}, focus on this."
    return f"Let me explain {focus_label or section_title} clearly."


def current_section_summary(sections: list[AcademySection], state: AcademyCoachState) -> str:
    if not sections:
        return "the academy introduction"

    section_index = max(0, min(state.current_section_index, len(sections) - 1))
    section = sections[section_index]
    part_count = max(len(section.chunks), 1)
    part_index = max(0, min(state.current_chunk_index + 1, part_count))
    return f"{section.title}, part {part_index} of {part_count}"


def voice_style_for(command: str) -> str:
    if phrase_present(command, VOICE_SWEET_PATTERNS):
        return "sweet"
    if phrase_present(command, VOICE_CALM_PATTERNS):
        return "calm"
    if phrase_present(command, VOICE_CLEAR_PATTERNS):
        return "clear"
    if phrase_present(command, VOICE_BRISK_PATTERNS):
        return "brisk"
    return ""


def ambience_mode_for(command: str) -> str:
    if phrase_present(command, AMBIENCE_OFF_PATTERNS):
        return "off"
    if phrase_present(command, AMBIENCE_SOFT_PATTERNS):
        return "soft"
    if phrase_present(command, AMBIENCE_ON_PATTERNS):
        return "on"
    return ""


def score_alias_entry(command: str, aliases: tuple[str, ...]) -> float:
    command_tokens = tokenize(command)
    best_score = 0.0
    for alias in aliases:
        best_score = max(best_score, score_phrase_match(command, command_tokens, alias))
    return best_score


def max_knowledge_score(command: str) -> float:
    return max((score_alias_entry(command, entry["aliases"]) for entry in GENERAL_KNOWLEDGE_ENTRIES), default=0.0)


def max_conversation_score(command: str) -> float:
    scores: list[float] = []
    for entry in GENERAL_CONVERSATION_ENTRIES:
        aliases = tuple(
            alias
            for alias in entry["aliases"]
            if not (alias == "tell me about yourself" and "yourself" not in command)
        )
        if aliases:
            scores.append(score_alias_entry(command, aliases))
    return max(scores, default=0.0)


def manual_vocabulary(sections: list[AcademySection]) -> set[str]:
    vocabulary: set[str] = set()
    for section in sections:
        for phrase in [section.title, section.eyebrow, *section.aliases]:
            vocabulary.update(tokenize(phrase))
        for target in section.targets:
            vocabulary.update(tokenize(target.alias))
            vocabulary.update(tokenize(target.label))
    return vocabulary


def should_use_manual_answer(
    command: str,
    sections: list[AcademySection],
    target: dict[str, Any] | None,
) -> bool:
    if not sections:
        return False
    if target is not None and float(target.get("score", 0.0)) >= 3.8:
        return True
    if not looks_like_information_request(command):
        return target is not None

    query = extract_public_query(command)
    query_tokens = [token for token in tokenize(query) if token]
    if not query_tokens:
        return target is not None

    vocabulary = manual_vocabulary(sections)
    overlap = len(set(query_tokens) & vocabulary)
    return overlap >= max(1, len(set(query_tokens)) // 2 + len(set(query_tokens)) % 2)


def score_command_candidate(command: str, sections: list[AcademySection]) -> float:
    score = float(len(tokenize(command))) * 0.15
    if looks_like_information_request(command):
        score += 2.8
    if looks_like_follow_up(command):
        score += 1.4
    if looks_like_personal_discussion(command):
        score += 2.2
    if phrase_present(command, PAUSE_PATTERNS + LISTEN_PATTERNS + RESUME_PATTERNS + RESTART_PATTERNS + LOCATION_PATTERNS + REPEAT_PATTERNS):
        score += 4.2

    target = find_target(command, sections)
    if target:
        score += float(target["score"]) + 1.6

    score += max_knowledge_score(command)
    score += max_conversation_score(command)
    return score


def choose_best_utterance(
    utterance: str,
    alternatives: list[str],
    sections: list[AcademySection],
) -> tuple[str, str]:
    candidates = [utterance, *alternatives]
    best_raw = utterance
    best_normalized = normalize_text(utterance)
    best_score = -1.0

    seen: set[str] = set()
    for raw in candidates:
        stripped = str(raw).strip()
        if not stripped:
            continue
        normalized = normalize_text(stripped)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        score = score_command_candidate(normalized, sections)
        if score > best_score:
            best_raw = stripped
            best_normalized = normalized
            best_score = score

    return best_raw, best_normalized


def extract_recent_topic(history: list[ConversationTurn]) -> str:
    for turn in reversed(history):
        if turn.role != "user":
            continue
        candidate = extract_public_query(turn.text)
        words = [
            word
            for word in raw_words(candidate)
            if word not in STOP_WORDS and word not in FOLLOW_UP_PRONOUNS
        ]
        if words:
            return " ".join(words[:6])
    return ""


def resolve_command_with_history(command: str, history: list[ConversationTurn]) -> str:
    if not history:
        return command

    if not looks_like_follow_up(command):
        return command

    topic = extract_recent_topic(history)
    if not topic:
        return command

    if "why" in command:
        return f"why is {topic} important"
    if "how" in command:
        return f"how does {topic} work"
    if "more" in command or "explain" in command:
        return f"tell me more about {topic}"
    if "what about" in command:
        return f"what about {topic}"
    return f"{command} {topic}"


def general_conversation_reply(command: str) -> AcademyDecision | None:
    best_entry: dict[str, Any] | None = None
    best_score = 0.0
    for entry in GENERAL_CONVERSATION_ENTRIES:
        aliases = tuple(
            alias
            for alias in entry["aliases"]
            if not (alias == "tell me about yourself" and "yourself" not in command)
        )
        if not aliases:
            continue
        score = score_alias_entry(command, aliases)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry and best_score >= 4.3:
        return AcademyDecision(action="answer", reply=best_entry["reply"])
    return None


def personal_discussion_reply(command: str) -> AcademyDecision | None:
    if phrase_present(command, ("can we talk", "talk to me", "talk like a friend", "speak like a friend", "be my friend")):
        return AcademyDecision(
            action="answer",
            reply=(
                "Of course. We can talk in a natural, friendly way. Tell me what is on your mind, and I will answer as clearly, warmly, and honestly as I can."
            ),
        )

    if phrase_present(command, ("i need advice", "help me decide", "what should i do")):
        return AcademyDecision(
            action="answer",
            reply=(
                "Yes. Tell me the situation, the options you are considering, and what matters most to you. I will help you think it through like a calm friend."
            ),
        )

    if looks_like_personal_discussion(command):
        return AcademyDecision(
            action="answer",
            reply=(
                "I hear you. We can slow down and talk it through together. Tell me what feels confusing, heavy, or important right now, and I will respond step by step."
            ),
        )
    return None


def should_try_big_model_first(command: str, target: dict[str, Any] | None) -> bool:
    if has_explicit_control_intent(command):
        return False
    if target is not None and has_navigation_intent(command):
        return False
    if target is not None and float(target.get("score", 0.0)) >= 6.4:
        return False
    words = raw_words(command)
    return (
        utterance_is_question(command)
        or looks_like_open_domain_query(command)
        or looks_like_follow_up(command)
        or looks_like_personal_discussion(command)
        or len(words) >= 5
    )


def should_try_model_decision(command: str, target: dict[str, Any] | None) -> bool:
    if looks_like_information_request(command):
        return False
    if looks_like_open_domain_query(command):
        return False
    if looks_like_personal_discussion(command):
        return False
    if utterance_is_question(command):
        return False
    if max_conversation_score(command) >= 4.3 or max_knowledge_score(command) >= 4.0:
        return False
    return has_navigation_intent(command) or (target is not None and len(raw_words(command)) >= 3)


def general_knowledge_reply(command: str) -> AcademyDecision | None:
    best_entry: dict[str, Any] | None = None
    best_score = 0.0
    for entry in GENERAL_KNOWLEDGE_ENTRIES:
        score = score_alias_entry(command, entry["aliases"])
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry and best_score >= 4.0:
        return AcademyDecision(action="answer", reply=best_entry["reply"])
    return None


def clean_generated_answer(text: str) -> str:
    cleaned = summarize_sentences(str(text or "").strip(), 4)
    cleaned = re.sub(r"\s+\d+\.\s*$", "", cleaned).strip()
    cleaned = re.sub(r"\s*[:;,]\s*$", ".", cleaned).strip()
    return cleaned


def stabilize_generated_answer(command: str, answer: str) -> str:
    lowered_command = normalize_text(command)
    lowered_answer = normalize_text(answer)

    if score_alias_entry(lowered_command, GENERAL_CONVERSATION_ENTRIES[2]["aliases"]) >= 4.3:
        if "satya" not in lowered_answer or "voice coach" not in lowered_answer:
            return GENERAL_CONVERSATION_ENTRIES[2]["reply"]

    if score_alias_entry(lowered_command, GENERAL_CONVERSATION_ENTRIES[0]["aliases"]) >= 4.3:
        if "voice coach" not in lowered_answer:
            return GENERAL_CONVERSATION_ENTRIES[0]["reply"]

    if score_alias_entry(lowered_command, GENERAL_CONVERSATION_ENTRIES[3]["aliases"]) >= 4.3:
        help_terms = {"harmonium", "lesson", "training", "question", "practice", "guide"}
        if not (help_terms & set(tokenize(lowered_answer))):
            return GENERAL_CONVERSATION_ENTRIES[3]["reply"]

    return answer


def fetch_json(
    url: str,
    timeout: float = 1.8,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
) -> Any:
    request_headers = {"User-Agent": "SatyaSangeetAcademy/1.0"}
    if headers:
        request_headers.update(headers)

    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")

    request = Request(url, data=body, headers=request_headers, method=method)
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_reply_language(language_code: str) -> str:
    return "hi" if str(language_code).lower().startswith("hi") else "en"


def translate_text(text: str, target_language: str, source_language: str = "auto") -> str | None:
    cleaned = text.strip()
    if not cleaned or target_language == source_language:
        return cleaned

    cache_key = (cleaned, source_language, target_language)
    if cache_key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[cache_key]

    try:
        url = (
            "https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl={quote(source_language)}&tl={quote(target_language)}&dt=t&q={quote(cleaned)}"
        )
        request = Request(url, headers={"User-Agent": "SatyaSangeetAcademy/1.0"})
        with urlopen(request, timeout=2.6) as response:
            payload = json.loads(response.read().decode("utf-8"))

        segments = payload[0] if isinstance(payload, list) and payload else []
        translated = "".join(str(item[0]) for item in segments if isinstance(item, list) and item)
        translated = translated.strip()
        if translated:
            TRANSLATION_CACHE[cache_key] = translated
            return translated
    except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
        return None

    return None


def contains_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text))


def translate_history(history: list[ConversationTurn], target_language: str) -> list[ConversationTurn]:
    translated: list[ConversationTurn] = []
    for turn in history:
        translated.append(
            ConversationTurn(
                role=turn.role,
                text=translate_text(turn.text, target_language, "auto") or turn.text,
            )
        )
    return translated


def localize_decision(
    decision: AcademyDecision,
    reply_language: str,
    default_voice_style: str = "",
    default_ambience_mode: str = "",
) -> dict[str, Any]:
    if default_voice_style and not decision.voice_style:
        decision.voice_style = default_voice_style
    if default_ambience_mode and not decision.ambience_mode:
        decision.ambience_mode = default_ambience_mode

    decision.reply_language = "en"
    if reply_language == "hi" and decision.reply:
        translated = translate_text(decision.reply, "hi", "en")
        if translated:
            decision.reply = translated
            decision.reply_language = "hi"

    return decision.to_dict()


def preferred_ollama_model() -> str:
    for value in (
        os.getenv("SATYA_ACADEMY_LLM_MODEL", "").strip(),
        os.getenv("SONICFORGE_LLM_MODEL", "").strip(),
    ):
        if value:
            return value
    return PREFERRED_OLLAMA_MODELS[0]


def fetch_ollama_model_names() -> list[str]:
    payload = fetch_json("http://127.0.0.1:11434/api/tags", timeout=0.55)
    models = payload.get("models", []) if isinstance(payload, dict) else []
    names: list[str] = []
    for model in models:
        name = str(model.get("name", "")).strip()
        if name:
            names.append(name)
    return names


def fetch_llama_cpp_gateway_status() -> dict[str, Any] | None:
    try:
        payload = fetch_json(DEFAULT_LLAMA_CPP_ENDPOINT, timeout=0.55)
    except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def resolve_llm_provider(force_refresh: bool = False) -> dict[str, Any] | None:
    if force_refresh:
        LLM_PROVIDER_CACHE["resolved"] = False
        LLM_PROVIDER_CACHE["provider"] = None

    if LLM_PROVIDER_CACHE["resolved"] and LLM_PROVIDER_CACHE["provider"] is not None:
        return LLM_PROVIDER_CACHE["provider"]

    provider: dict[str, Any] | None = None
    endpoint = os.getenv("SONICFORGE_LLM_ENDPOINT", "").strip()
    model = os.getenv("SONICFORGE_LLM_MODEL", "").strip()
    api_key = os.getenv("SONICFORGE_LLM_API_KEY", "").strip()

    if endpoint and model:
        provider = {
            "kind": "openai-compatible",
            "endpoint": endpoint.rstrip("/"),
            "model": model,
            "api_key": api_key,
        }
    else:
        llama_status = fetch_llama_cpp_gateway_status()
        if llama_status and bool(llama_status.get("ready")):
            provider = {
                "kind": "llama-cpp",
                "endpoint": DEFAULT_LLAMA_CPP_ENDPOINT,
                "model": str(llama_status.get("model", preferred_ollama_model())),
                "api_key": "",
            }

    if provider is None and not (endpoint and model):
        try:
            lmstudio = fetch_json("http://127.0.0.1:1234/v1/models", timeout=0.45)
            models = lmstudio.get("data", []) if isinstance(lmstudio, dict) else []
            if models:
                provider = {
                    "kind": "openai-compatible",
                    "endpoint": "http://127.0.0.1:1234/v1",
                    "model": str(models[0].get("id", "")),
                    "api_key": "",
                }
        except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
            provider = None

        if provider is None:
            try:
                models = fetch_ollama_model_names()
                if models:
                    selected_model = preferred_ollama_model()
                    if selected_model not in models:
                        for candidate in PREFERRED_OLLAMA_MODELS:
                            if candidate in models:
                                selected_model = candidate
                                break
                        else:
                            selected_model = models[0]
                    provider = {
                        "kind": "ollama",
                        "endpoint": "http://127.0.0.1:11434",
                        "model": selected_model,
                        "api_key": "",
                    }
            except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
                provider = None

    LLM_PROVIDER_CACHE["resolved"] = True
    LLM_PROVIDER_CACHE["provider"] = provider
    return provider


def academy_llm_status() -> dict[str, Any]:
    provider = resolve_llm_provider(force_refresh=True)
    if provider:
        detail = (
            f"The academy is using a real language model through {provider['kind']} with model {provider['model']}."
        )
        command_hint = ""
        if provider["kind"] == "llama-cpp":
            detail = f"The academy is using the local llama.cpp brain with model {provider['model']}."
        if provider["kind"] == "ollama":
            detail = f"The academy is using the local Ollama brain with model {provider['model']}."
        return AcademyLLMStatus(
            available=True,
            provider=str(provider["kind"]),
            model=str(provider["model"]),
            endpoint=str(provider["endpoint"]),
            detail=detail,
            command_hint=command_hint,
        ).to_dict()

    llama_status = fetch_llama_cpp_gateway_status()
    if llama_status:
        return AcademyLLMStatus(
            available=bool(llama_status.get("ready")),
            provider="llama-cpp",
            model=str(llama_status.get("model", "Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M")),
            endpoint=str(llama_status.get("endpoint", DEFAULT_LLAMA_CPP_ENDPOINT)),
            detail=str(llama_status.get("detail", "The local academy model gateway is active.")),
            command_hint="" if bool(llama_status.get("ready")) else "python3 run_sonicforge.py --setup-llm",
        ).to_dict()

    endpoint = os.getenv("SONICFORGE_LLM_ENDPOINT", "").strip()
    model = os.getenv("SONICFORGE_LLM_MODEL", "").strip()
    if endpoint and model:
        return AcademyLLMStatus(
            available=False,
            provider="openai-compatible",
            model=model,
            endpoint=endpoint,
            detail="A custom LLM endpoint is configured, but it is not responding yet.",
        ).to_dict()

    if shutil.which("llama-server"):
        return AcademyLLMStatus(
            available=False,
            provider="llama-cpp",
            model="Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M",
            endpoint=DEFAULT_LLAMA_CPP_ENDPOINT,
            detail="llama.cpp is installed, but the local academy model server is not running yet.",
            command_hint="python3 run_sonicforge.py --setup-llm",
        ).to_dict()

    if shutil.which("ollama"):
        try:
            models = fetch_ollama_model_names()
        except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
            return AcademyLLMStatus(
                available=False,
                provider="ollama",
                model=preferred_ollama_model(),
                endpoint="http://127.0.0.1:11434",
                detail="Ollama is installed, but its local model service is not running yet.",
                command_hint="ollama serve",
            ).to_dict()

        if not models:
            return AcademyLLMStatus(
                available=False,
                provider="ollama",
                model=preferred_ollama_model(),
                endpoint="http://127.0.0.1:11434",
                detail="Ollama is available, but no local model has been pulled yet for the academy assistant.",
                command_hint="ollama pull qwen2.5:3b",
            ).to_dict()

        return AcademyLLMStatus(
            available=False,
            provider="ollama",
            model=models[0],
            endpoint="http://127.0.0.1:11434",
            detail="A local model exists in Ollama, but the academy has not activated it yet. Restart the app after setup.",
            command_hint="python3 run_sonicforge.py --mode web",
        ).to_dict()

    return AcademyLLMStatus(
        available=False,
        provider="none",
        model=preferred_ollama_model(),
        endpoint="",
        detail="No real local LLM runtime is active yet. The academy is still using its fallback intelligence stack.",
        command_hint="brew install llama.cpp && python3 run_sonicforge.py --setup-llm",
    ).to_dict()


def build_section_catalog(sections: list[AcademySection]) -> str:
    catalog: list[str] = []
    for section in sections[:12]:
        aliases = ", ".join(alias for alias in section.aliases[:4] if alias) or "none"
        catalog.append(f"{section.title} [aliases: {aliases}]")
    return " | ".join(catalog)


def build_manual_context(command: str, sections: list[AcademySection], target: dict[str, Any] | None) -> str:
    if not sections or not should_use_manual_answer(command, sections, target):
        return ""

    snippets: list[str] = []
    seen: set[tuple[int, int]] = set()
    for _, section_index, chunk_index, chunk in top_chunk_matches(command, sections, target)[:3]:
        key = (section_index, chunk_index)
        if key in seen:
            continue
        seen.add(key)
        section_title = sections[section_index].title or f"Section {section_index + 1}"
        snippets.append(f"{section_title}: {summarize_sentences(chunk, 2)}")

    return " | ".join(snippets)


def build_llm_messages(
    utterance: str,
    sections: list[AcademySection],
    state: AcademyCoachState,
    history: list[ConversationTurn],
    response_mode: str = "answer",
) -> list[dict[str, str]]:
    normalized_utterance = normalize_text(utterance)
    lesson_context = current_section_summary(sections, state)
    section_catalog = build_section_catalog(sections)
    target = find_target(normalized_utterance, sections) if sections else None
    manual_context = build_manual_context(normalized_utterance, sections, target)
    assistant_role_context = (
        "Your role here: you are Satya Sangeet, the harmonium voice coach and conversational companion. "
        "You guide lessons, answer lesson questions, explain music concepts, pause and resume training, and answer wider questions in a calm human way."
    )
    conversation_context = " | ".join(
        f"{turn.role}: {turn.text}"
        for turn in history[-6:]
    )
    open_domain_mode = (
        response_mode == "answer"
        and not has_explicit_control_intent(normalized_utterance)
        and not has_navigation_intent(normalized_utterance)
        and (
            not sections
            or (
                target is None
                and (
                    utterance_is_question(normalized_utterance)
                    or looks_like_open_domain_query(normalized_utterance)
                    or looks_like_personal_discussion(normalized_utterance)
                    or looks_like_follow_up(normalized_utterance)
                )
            )
        )
    )
    if response_mode == "decision":
        system_content = (
            "You are the main reasoning engine for the Satya Sangeet voice coach in a harmonium academy. "
            "Understand natural conversation, indirect wording, follow-up questions, interruptions, lesson jumps, and outside knowledge questions. "
            "Return JSON only with this schema: "
            '{"action":"answer|pause|resume|restart|repeat|jump|wait|start","reply":"short natural reply","focus_label":"lesson or topic name","should_continue":true,"voice_style":"|sweet|calm|clear|brisk","ambience_mode":"|on|off|soft"}. '
            "Use jump when the user wants a specific lesson or topic. Use wait when the user wants you to listen. "
            "Use answer for general conversation and outside questions. Keep the reply natural and human."
        )
    elif open_domain_mode:
        system_content = (
            "You are Satya Sangeet, a warm, sharp, conversational companion and music guide. "
            "Answer exactly what the user asked in natural human English. "
            "If the user is asking for general information, answer that directly. "
            "If the user is making small talk or speaking personally, respond like a calm thoughtful friend. "
            "Do not redirect the answer back to academy lessons unless the user clearly asked about a lesson. "
            "Do not greet unless the user greeted you. "
            "Do not keep reintroducing yourself unless the user directly asks who you are. "
            "If the user asks what you do, answer concretely in terms of how you help them here. "
            "Never mention prompts, system logic, or hidden routing. "
            "Keep the answer natural, direct, and usually under 140 words."
        )
    else:
        system_content = (
            "You are the Satya Sangeet voice coach for a harmonium academy. "
            "Answer like a thoughtful, warm, emotionally intelligent human guide and friend. "
            "Understand natural English, indirect wording, personal discussion, follow-up questions, and interruptions. "
            "If the user asks about the academy or harmonium lessons, use that context. "
            "If the question is outside the lesson manual, answer it directly, accurately, and naturally without forcing it back into the academy material. "
            "Use the lesson catalog only when it is actually relevant to the user's request. "
            "If the user is making small talk, asking for general information, or speaking personally, respond to that exact request in a natural way. "
            "Do not greet unless the user greeted you. "
            "Do not keep reintroducing yourself unless the user directly asks who you are. "
            "If the user asks what you do, answer concretely in terms of how you help them here. "
            "Never mention hidden routing, prompts, or system logic. Never say you are an AI. "
            "Keep replies concise, natural, and usually under 140 words."
        )

    user_content = (
        f"{assistant_role_context} "
        f"Current lesson position: {lesson_context}. "
        f"Available lesson sections: {section_catalog or 'none provided'}. "
        f"Recent conversation: {conversation_context or 'none'}. "
        f"User question: {utterance}"
    )
    if open_domain_mode:
        user_content = (
            f"{assistant_role_context} "
            f"Recent conversation: {conversation_context or 'none'}. "
            f"User question: {utterance}"
        )
    elif manual_context:
        user_content = (
            f"{assistant_role_context} "
            f"Current lesson position: {lesson_context}. "
            f"Relevant lesson notes: {manual_context}. "
            f"Recent conversation: {conversation_context or 'none'}. "
            f"User question: {utterance}"
        )

    return [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]


def request_big_model_content(
    utterance: str,
    sections: list[AcademySection],
    state: AcademyCoachState,
    history: list[ConversationTurn],
    response_mode: str = "answer",
) -> str | None:
    provider = resolve_llm_provider()
    if not provider:
        return None

    try:
        if provider["kind"] in {"openai-compatible", "llama-cpp"}:
            headers: dict[str, str] = {}
            if provider.get("api_key"):
                headers["Authorization"] = f"Bearer {provider['api_key']}"
            response = fetch_json(
                f"{provider['endpoint']}/chat/completions",
                timeout=6.0 if response_mode == "decision" else 10.0,
                method="POST",
                headers=headers,
                data={
                    "model": provider["model"],
                    "messages": build_llm_messages(utterance, sections, state, history, response_mode),
                    "temperature": 0.22 if response_mode == "decision" else 0.35,
                    "max_tokens": 220 if response_mode == "decision" else 160,
                },
            )
            choices = response.get("choices", []) if isinstance(response, dict) else []
            message = choices[0].get("message", {}) if choices else {}
            content = message.get("content", "")
            if isinstance(content, str) and content.strip():
                return content.strip()

        if provider["kind"] == "ollama":
            response = fetch_json(
                f"{provider['endpoint']}/api/chat",
                timeout=6.0 if response_mode == "decision" else 10.0,
                method="POST",
                data={
                    "model": provider["model"],
                    "messages": build_llm_messages(utterance, sections, state, history, response_mode),
                    "stream": False,
                    "format": "json" if response_mode == "decision" else "",
                    "options": {"temperature": 0.22 if response_mode == "decision" else 0.35, "num_predict": 220 if response_mode == "decision" else 160},
                },
            )
            message = response.get("message", {}) if isinstance(response, dict) else {}
            content = str(message.get("content", "")).strip() if isinstance(message, dict) else ""
            if content:
                return content
    except (TimeoutError, URLError, json.JSONDecodeError, ValueError, KeyError):
        return None

    return None


def extract_json_object(text: str) -> dict[str, Any] | None:
    cleaned = str(text or "").strip()
    if not cleaned:
        return None
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE | re.DOTALL).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    snippet = cleaned[start : end + 1]
    try:
        payload = json.loads(snippet)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def coerce_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1", "continue"}:
            return True
        if normalized in {"false", "no", "0"}:
            return False
    return default


def resolve_focus_target(focus_label: str, sections: list[AcademySection]) -> dict[str, Any] | None:
    label = normalize_text(focus_label)
    if not label:
        return None
    return find_target(f"explain {label}", sections) or find_target(label, sections)


def decision_from_llm_content(
    content: str,
    sections: list[AcademySection],
    state: AcademyCoachState,
) -> AcademyDecision | None:
    payload = extract_json_object(content)
    if not payload:
        cleaned = summarize_sentences(content.strip(), 4)
        return AcademyDecision(action="answer", reply=cleaned) if cleaned else None

    action = normalize_text(str(payload.get("action", "answer"))) or "answer"
    if action not in VALID_MODEL_ACTIONS:
        action = "answer"

    reply = str(payload.get("reply", "")).strip()
    if not reply and action == "answer":
        return None

    focus_label = str(payload.get("focus_label", "") or payload.get("section_alias", "")).strip()
    target = resolve_focus_target(focus_label, sections) if focus_label else None
    should_continue = coerce_bool(payload.get("should_continue"), action in {"start", "resume", "restart", "repeat", "jump"})
    voice_style = normalize_text(str(payload.get("voice_style", "")))
    ambience_mode = normalize_text(str(payload.get("ambience_mode", "")))

    if voice_style not in VALID_VOICE_STYLES:
        voice_style = ""
    if ambience_mode not in VALID_AMBIENCE_MODES:
        ambience_mode = ""

    if action == "pause":
        return AcademyDecision(action="pause", reply=reply or "Of course. I am pausing here.", voice_style=voice_style, ambience_mode=ambience_mode)
    if action == "wait":
        return AcademyDecision(action="wait", reply=reply or "I am listening now. Go ahead.", voice_style=voice_style, ambience_mode=ambience_mode)
    if action == "resume":
        return AcademyDecision(
            action="resume",
            reply=reply or "Certainly. I will continue from where we paused.",
            section_index=state.current_section_index,
            chunk_index=state.current_chunk_index,
            should_continue=True,
            voice_style=voice_style,
            ambience_mode=ambience_mode,
        )
    if action == "repeat":
        return AcademyDecision(
            action="repeat",
            reply=reply or "I will repeat that part carefully.",
            section_index=state.current_section_index,
            chunk_index=state.current_chunk_index,
            should_continue=True,
            voice_style=voice_style,
            ambience_mode=ambience_mode,
        )
    if action == "restart":
        return AcademyDecision(
            action="restart",
            reply=reply or "Certainly. I will begin again from the start.",
            section_index=0,
            chunk_index=0,
            should_continue=True,
            focus_label="Training Path",
            voice_style=voice_style,
            ambience_mode=ambience_mode,
        )
    if action in {"start", "jump"}:
        if target:
            return AcademyDecision(
                action="jump" if action == "jump" else "start",
                reply=reply or f"I will take you to {target['label']} now.",
                section_index=target["section_index"],
                chunk_index=target["chunk_index"],
                should_continue=should_continue,
                focus_label=target["label"],
                voice_style=voice_style,
                ambience_mode=ambience_mode,
            )
        if action == "start":
            return AcademyDecision(
                action="start",
                reply=reply or "Certainly. I will begin the training now.",
                section_index=0,
                chunk_index=0,
                should_continue=True,
                focus_label="Training Path",
                voice_style=voice_style,
                ambience_mode=ambience_mode,
            )
        return None

    return AcademyDecision(
        action="answer",
        reply=reply or summarize_sentences(content.strip(), 4),
        section_index=target["section_index"] if target else None,
        chunk_index=target["chunk_index"] if target else None,
        focus_label=target["label"] if target else focus_label,
        should_continue=should_continue if target else False,
        voice_style=voice_style,
        ambience_mode=ambience_mode,
    )


def lookup_big_model_decision(
    utterance: str,
    sections: list[AcademySection],
    state: AcademyCoachState,
    history: list[ConversationTurn],
) -> AcademyDecision | None:
    content = request_big_model_content(utterance, sections, state, history, response_mode="decision")
    if not content:
        return None
    return decision_from_llm_content(content, sections, state)


def lookup_big_model_answer(
    utterance: str,
    sections: list[AcademySection],
    state: AcademyCoachState,
    history: list[ConversationTurn],
) -> str | None:
    content = request_big_model_content(utterance, sections, state, history, response_mode="answer")
    if not content:
        return None
    return clean_generated_answer(content)


def extract_public_query(command: str) -> str:
    query = normalize_text(command)
    for prefix in (
        "i was wondering if you could tell me something about ",
        "i am wondering if you could tell me something about ",
        "i was wondering if you could tell me about ",
        "i am wondering if you could tell me about ",
        "could you tell me something about ",
        "can you tell me something about ",
        "tell me something about ",
        "could you tell me about ",
        "can you tell me about ",
        "i want to know about ",
        "i want information about ",
        "give me some information about ",
        "what is ",
        "what are ",
        "who is ",
        "who are ",
        "why is ",
        "why are ",
        "tell me about ",
        "explain ",
        "define ",
        "how does ",
        "how do ",
    ):
        if query.startswith(prefix):
            query = query[len(prefix):].strip()
            break

    about_match = re.search(r"\b(?:about|regarding|on)\s+([a-z0-9\s]+)$", query)
    if about_match:
        query = about_match.group(1).strip()

    query = re.sub(r"^(please|actually|really|just)\s+", "", query).strip()
    query = re.sub(r"\b(work|works|important|mean|means)\b$", "", query).strip()
    return query


def lookup_duckduckgo_answer(command: str) -> str | None:
    query = extract_public_query(command)
    if len(raw_words(query)) < 1:
        return None

    try:
        data = fetch_json(
            f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&no_redirect=1&skip_disambig=1",
            timeout=1.8,
        )
        for key in ("AbstractText", "Answer", "Definition"):
            text = str(data.get(key, "")).strip() if isinstance(data, dict) else ""
            if text:
                return summarize_sentences(text, 2)

        related_topics = data.get("RelatedTopics", []) if isinstance(data, dict) else []
        for topic in related_topics[:5]:
            if isinstance(topic, dict) and topic.get("Text"):
                return summarize_sentences(str(topic["Text"]), 2)
            if isinstance(topic, dict):
                nested = topic.get("Topics", [])
                for item in nested[:3]:
                    if isinstance(item, dict) and item.get("Text"):
                        return summarize_sentences(str(item["Text"]), 2)
    except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
        return None

    return None


def lookup_dictionary_answer(command: str) -> str | None:
    query = extract_public_query(command)
    words = raw_words(query)
    if len(words) != 1:
        return None

    try:
        entries = fetch_json(f"https://api.dictionaryapi.dev/api/v2/entries/en/{quote(words[0])}", timeout=1.8)
        if isinstance(entries, list) and entries:
            meanings = entries[0].get("meanings", [])
            if meanings:
                definitions = meanings[0].get("definitions", [])
                if definitions:
                    definition = str(definitions[0].get("definition", "")).strip()
                    if definition:
                        return f"{words[0].capitalize()} means this. {summarize_sentences(definition, 2)}"
    except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
        return None

    return None


def lookup_wikipedia_summary(command: str) -> str | None:
    query = extract_public_query(command)
    if len(raw_words(query)) < 1:
        return None

    try:
        search_data = fetch_json(
            "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=1"
            f"&namespace=0&search={quote(query)}",
            timeout=1.6,
        )
        titles = search_data[1] if isinstance(search_data, list) and len(search_data) > 1 else []
        if not titles:
            return None

        title = str(titles[0]).strip()
        if not title:
            return None

        summary_data = fetch_json(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}",
            timeout=1.8,
        )
        extract = str(summary_data.get("extract", "")).strip() if isinstance(summary_data, dict) else ""
        if not extract:
            return None
        return summarize_sentences(extract, 2)
    except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
        return None


def lookup_public_knowledge(command: str) -> str | None:
    cache_key = normalize_text(command)
    if cache_key in PUBLIC_KNOWLEDGE_CACHE:
        return PUBLIC_KNOWLEDGE_CACHE[cache_key]

    for lookup in (lookup_wikipedia_summary, lookup_duckduckgo_answer, lookup_dictionary_answer):
        answer = lookup(command)
        if answer:
            PUBLIC_KNOWLEDGE_CACHE[cache_key] = answer
            return answer

    return None


def public_knowledge_decision(command: str, answer: str, voice_style: str) -> AcademyDecision:
    normalized_command = normalize_text(command)
    if normalized_command.startswith(("tell me about ", "tell me something about ", "describe ")):
        reply = f"Here is a clear way to understand it. {answer.strip()}"
    elif normalized_command.startswith(("can you explain ", "please explain ", "help me understand ")):
        reply = f"Certainly. {answer.strip()}"
    else:
        reply = answer.strip()
    return AcademyDecision(
        action="answer",
        reply=reply,
        voice_style=voice_style,
    )


def answer_looks_off_topic(
    command: str,
    answer: str,
    sections: list[AcademySection],
    target: dict[str, Any] | None,
) -> bool:
    if not answer or target is not None or should_use_manual_answer(command, sections, target):
        return False
    if not looks_like_factual_information_request(command) and not looks_like_open_domain_query(command):
        return False

    query_words = set(content_words(extract_public_query(command)))
    answer_words = set(tokenize(answer))
    if not answer_words:
        return True

    direct_overlap = len(query_words & answer_words)
    unexpected_bias = (answer_words & OPEN_DOMAIN_ACADEMY_BIAS_TERMS) - query_words
    if direct_overlap == 0 and len(unexpected_bias) >= 1:
        return True
    if direct_overlap <= 1 and len(unexpected_bias) >= 2:
        return True

    if query_words and not (query_words & answer_words):
        lowered = normalize_text(answer)
        if any(term in lowered for term in ("academy", "lesson", "training path", "voice coach")):
            return True
    return False


def grounded_open_domain_decision(command: str, voice_style: str) -> AcademyDecision | None:
    if not (looks_like_factual_information_request(command) or looks_like_open_domain_query(command)):
        return None
    public_answer = lookup_public_knowledge(command)
    if not public_answer:
        return None
    return public_knowledge_decision(command, public_answer, voice_style)


def decide_control_action(
    command: str,
    sections: list[AcademySection],
    state: AcademyCoachState,
    target: dict[str, Any] | None,
) -> AcademyDecision | None:
    voice_style = voice_style_for(command)
    ambience_mode = ambience_mode_for(command)

    if is_listen_interrupt(command):
        return AcademyDecision(
            action="wait",
            reply="I am listening now. Go ahead, and I will focus on what you want to say.",
            voice_style=voice_style,
            ambience_mode=ambience_mode,
        )

    if ambience_mode:
        if ambience_mode == "off":
            return AcademyDecision(
                action="answer",
                reply="Certainly. I am turning the background music off so the voice stays fully clear.",
                voice_style=voice_style,
                ambience_mode=ambience_mode,
            )
        if ambience_mode == "soft":
            return AcademyDecision(
                action="answer",
                reply="Certainly. I will keep the classical background very soft and gentle under the voice.",
                voice_style=voice_style,
                ambience_mode=ambience_mode,
            )
        return AcademyDecision(
            action="answer",
            reply="Certainly. I will keep a calm classical background beneath the lesson and lower it whenever I speak.",
            voice_style=voice_style,
            ambience_mode=ambience_mode,
        )

    if voice_style and target is None and not looks_like_information_request(command):
        return AcademyDecision(
            action="answer",
            reply=voice_style_reply(voice_style),
            voice_style=voice_style,
            ambience_mode=ambience_mode,
        )

    if phrase_present(command, PAUSE_PATTERNS):
        return AcademyDecision(
            action="pause",
            reply="Of course. I am stopping here. Say continue whenever you want me to resume from the same point.",
            voice_style=voice_style,
        )

    if phrase_present(command, RESTART_PATTERNS):
        return AcademyDecision(
            action="restart",
            reply="Certainly. I will return to the beginning and start the training again in a calm step by step way.",
            section_index=0,
            chunk_index=0,
            should_continue=True,
            focus_label="Training Path",
            voice_style=voice_style,
        )

    if phrase_present(command, REPEAT_PATTERNS):
        return AcademyDecision(
            action="repeat",
            reply="I will repeat the same part slowly.",
            section_index=state.current_section_index,
            chunk_index=state.current_chunk_index,
            should_continue=True,
            voice_style=voice_style,
        )

    if phrase_present(command, LOCATION_PATTERNS):
        return AcademyDecision(
            action="answer",
            reply=(
                f"We are currently at {current_section_summary(sections, state)}. "
                "You can say continue, repeat that, or ask me to jump to another lesson."
            ),
            voice_style=voice_style,
        )

    if state.awaiting_consent:
        if phrase_present(command, NEGATIVE_PATTERNS):
            return AcademyDecision(
                action="wait",
                reply="No problem. I will stay ready. Say continue whenever you want to begin, or name any lesson that you want me to explain.",
                voice_style=voice_style,
            )
        if phrase_present(command, POSITIVE_PATTERNS):
            if target and (target["section_index"] != 0 or target["chunk_index"] != 0):
                return AcademyDecision(
                    action="jump",
                    reply=f"Beautiful. I will begin with {target['label']} and guide you from there.",
                    section_index=target["section_index"],
                    chunk_index=target["chunk_index"],
                    should_continue=True,
                    focus_label=target["label"],
                    voice_style=voice_style,
                )
            return AcademyDecision(
                action="start",
                reply="Beautiful. Let us begin with the training path, and I will guide you step by step.",
                section_index=0,
                chunk_index=0,
                should_continue=True,
                focus_label="Training Path",
                voice_style=voice_style,
            )

    if phrase_present(command, RESUME_PATTERNS):
        if target:
            return AcademyDecision(
                action="jump",
                reply=f"Certainly. I will move to {target['label']} and continue from there.",
                section_index=target["section_index"],
                chunk_index=target["chunk_index"],
                should_continue=True,
                focus_label=target["label"],
                voice_style=voice_style,
            )
        return AcademyDecision(
            action="resume",
            reply="Certainly. I will continue from the exact point where we paused.",
            section_index=state.current_section_index,
            chunk_index=state.current_chunk_index,
            should_continue=True,
            voice_style=voice_style,
        )

    if phrase_present(command, POSITIVE_PATTERNS) and state.paused:
        return AcademyDecision(
            action="resume",
            reply="Certainly. I will continue from where we left off.",
            section_index=state.current_section_index,
            chunk_index=state.current_chunk_index,
            should_continue=True,
            voice_style=voice_style,
        )

    if target and (phrase_present(command, EXPLAIN_VERBS) or ("continue" in command and "with" in command)):
        return AcademyDecision(
            action="jump",
            reply=f"Absolutely. I will take you to {target['label']} and explain it carefully.",
            section_index=target["section_index"],
            chunk_index=target["chunk_index"],
            should_continue=True,
            focus_label=target["label"],
            voice_style=voice_style,
        )

    return None


def coach_academy_user(payload: dict[str, Any]) -> dict[str, Any]:
    utterance = str(payload.get("utterance", "")).strip()
    sections = [section_from_payload(item) for item in payload.get("sections", [])]
    state = state_from_payload(payload.get("state", {}))
    history = history_from_payload(payload.get("history"))
    alternatives = [str(item).strip() for item in payload.get("alternatives", []) if str(item).strip()]
    requested_language = str(payload.get("language", "")).strip()
    reply_language = normalize_reply_language(
        requested_language or ("hi" if contains_devanagari(utterance) else "en")
    )

    should_translate_to_english = reply_language == "hi" or contains_devanagari(utterance) or any(
        contains_devanagari(item) for item in alternatives
    )
    if should_translate_to_english:
        utterance = translate_text(utterance, "en", "auto") or utterance
        alternatives = [translate_text(item, "en", "auto") or item for item in alternatives]
        history = translate_history(history, "en")

    utterance, command = choose_best_utterance(utterance, alternatives, sections)
    command = resolve_command_with_history(command, history)
    voice_style = voice_style_for(command)
    ambience_mode = ambience_mode_for(command)
    open_domain_query = looks_like_open_domain_query(command)
    tried_big_model = False

    if not utterance:
        return localize_decision(
            AcademyDecision(
            action="answer",
            reply="I am listening. Tell me what you want to learn, or say continue to resume the training.",
            voice_style=voice_style,
            ),
            reply_language,
            voice_style,
            ambience_mode,
        )

    target = find_target(command, sections)
    control_decision = decide_control_action(command, sections, state, target)
    if control_decision:
        return localize_decision(control_decision, reply_language, voice_style, ambience_mode)

    if target and ("go to" in command or "take me" in command or "move to" in command or "open" in command):
        return localize_decision(
            AcademyDecision(
                action="jump",
                reply=f"Certainly. I am taking you to {target['label']} now.",
                section_index=target["section_index"],
                chunk_index=target["chunk_index"],
                should_continue=False,
                focus_label=target["label"],
                voice_style=voice_style,
            ),
            reply_language,
            voice_style,
            ambience_mode,
        )

    manual_answer_allowed = (looks_like_information_request(command) or target) and should_use_manual_answer(command, sections, target)

    if should_try_big_model_first(command, target):
        big_model_answer = lookup_big_model_answer(utterance, sections, state, history)
        tried_big_model = True
        if big_model_answer and not answer_looks_off_topic(command, big_model_answer, sections, target):
            big_model_answer = stabilize_generated_answer(command, big_model_answer)
            return localize_decision(
                AcademyDecision(
                    action="answer",
                    reply=big_model_answer,
                    voice_style=voice_style,
                ),
                reply_language,
                voice_style,
                ambience_mode,
            )

    if should_try_model_decision(command, target):
        model_decision = lookup_big_model_decision(utterance, sections, state, history)
        if model_decision:
            return localize_decision(model_decision, reply_language, voice_style, ambience_mode)

    if manual_answer_allowed:
        decision = build_answer(command, sections, target, state)
        if decision:
            return localize_decision(decision, reply_language, voice_style, ambience_mode)

    companion_decision = personal_discussion_reply(command)
    if companion_decision:
        return localize_decision(companion_decision, reply_language, voice_style, ambience_mode)

    conversation_decision = general_conversation_reply(command)
    if conversation_decision:
        return localize_decision(conversation_decision, reply_language, voice_style, ambience_mode)

    knowledge_decision = general_knowledge_reply(command)
    if knowledge_decision:
        return localize_decision(knowledge_decision, reply_language, voice_style, ambience_mode)

    if looks_like_information_request(command) or target:
        if not tried_big_model:
            big_model_answer = lookup_big_model_answer(utterance, sections, state, history)
            tried_big_model = True
            if big_model_answer and not answer_looks_off_topic(command, big_model_answer, sections, target):
                big_model_answer = stabilize_generated_answer(command, big_model_answer)
                return localize_decision(
                    AcademyDecision(
                        action="answer",
                        reply=big_model_answer,
                        voice_style=voice_style,
                    ),
                    reply_language,
                    voice_style,
                    ambience_mode,
                )

        grounded_open_domain = grounded_open_domain_decision(command, voice_style)
        if grounded_open_domain:
            return localize_decision(
                grounded_open_domain,
                reply_language,
                voice_style,
                ambience_mode,
            )

    if open_domain_query and not target:
        if not tried_big_model:
            big_model_answer = lookup_big_model_answer(utterance, sections, state, history)
            tried_big_model = True
            if big_model_answer and not answer_looks_off_topic(command, big_model_answer, sections, target):
                big_model_answer = stabilize_generated_answer(command, big_model_answer)
                return localize_decision(
                    AcademyDecision(
                        action="answer",
                        reply=big_model_answer,
                        voice_style=voice_style,
                    ),
                    reply_language,
                    voice_style,
                    ambience_mode,
                )

        grounded_open_domain = grounded_open_domain_decision(command, voice_style)
        if grounded_open_domain:
            return localize_decision(
                grounded_open_domain,
                reply_language,
                voice_style,
                ambience_mode,
            )

    if voice_style:
        return localize_decision(
            AcademyDecision(
                action="answer",
                reply=voice_style_reply(voice_style),
                voice_style=voice_style,
                ambience_mode=ambience_mode,
            ),
            reply_language,
            voice_style,
            ambience_mode,
        )

    return localize_decision(
        AcademyDecision(
            action="answer",
            reply=(
                "I am with you. Ask me in your own words about the training, music, general information, or anything you want to talk through, and I will answer as clearly and naturally as I can."
            ),
        ),
        reply_language,
        voice_style,
        ambience_mode,
    )


def voice_style_reply(voice_style: str) -> str:
    if voice_style == "sweet":
        return "Certainly. I will speak in a softer, sweeter, and calmer voice from now on."
    if voice_style == "calm":
        return "Of course. I will speak more calmly, more smoothly, and at a slower pace from now on."
    if voice_style == "clear":
        return "Certainly. I will speak more clearly and separate the important words more carefully."
    if voice_style == "brisk":
        return "Certainly. I will keep the guidance a little more direct and a little faster."
    return "I will adjust my speaking style."
