# 🎵 SonicForge X - Technical Architecture Document

**Developer:** Satya Narayan Sahu  
**Version:** 1.0.0 (Phase 1 MVP)  
**Date:** March 27, 2026  
**Document Type:** Technical Architecture Specification  
**Classification:** Open Source - MIT License  

---

## 📋 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Core Module Architecture](#4-core-module-architecture)
5. [Algorithm Deep Dive](#5-algorithm-deep-dive)
6. [Data Structures & Models](#6-data-structures--models)
7. [API Gateway & Endpoints](#7-api-gateway--endpoints)
8. [Web Frontend Architecture](#8-web-frontend-architecture)
9. [Desktop Application Architecture](#9-desktop-application-architecture)
10. [AI & Machine Learning Components](#10-ai--machine-learning-components)
11. [Audio Processing Pipeline](#11-audio-processing-pipeline)
12. [Communication Protocols](#12-communication-protocols)
13. [State Management](#13-state-management)
14. [Testing Strategy](#14-testing-strategy)
15. [Deployment Architecture](#15-deployment-architecture)
16. [Performance Optimization](#16-performance-optimization)
17. [Security Considerations](#17-security-considerations)
18. [Future Roadmap](#18-future-roadmap)
19. [Glossary](#19-glossary)
20. [References](#20-references)

---

## 1. Executive Summary

SonicForge X is an innovative AI-powered music composition and production system that combines cutting-edge artificial intelligence with traditional music theory. The system provides:

- **Emotion-Driven Composition**: AI generates music based on emotional parameters
- **Harmonium Academy**: Interactive voice coach with conversational AI
- **Real-Time Mixing**: Automatic mixing and mastering with suggestions
- **Multi-Platform Support**: Desktop (Tkinter) and Web (HTTP) interfaces
- **No-Dependency Core**: Pure Python implementation for maximum compatibility

### Key Achievements (Phase 1 MVP):
✅ Session model and event logging  
✅ Emotion-driven composition engine  
✅ 3D harmonium with sampled playback  
✅ Voice coach with natural conversation  
✅ AI suggestion engine for arrangements  
✅ Lightweight mix analysis and auto-mix  
✅ WAV rendering for offline export  

---

## 2. System Overview

### 2.1 System Purpose
SonicForge X aims to democratize music production by providing AI-assisted composition tools that understand emotional context and musical theory.

### 2.2 Target Users
1. **Music Producers**: Professional and amateur composers
2. **Students**: Learning music theory and composition
3. **Educators**: Teaching harmonium and Indian classical music
4. **AI Enthusiasts**: Exploring creative AI applications

### 2.3 Core Features Matrix

| Feature | Desktop | Web | Status |
|---------|---------|-----|--------|
| Music Composition | ✅ | ✅ | MVP |
| AI Suggestions | ✅ | ✅ | MVP |
| Mix Analysis | ✅ | ✅ | MVP |
| WAV Export | ✅ | ✅ | MVP |
| Harmonium 3D | ❌ | ✅ | MVP |
| Voice Coach | ❌ | ✅ | MVP |
| Real-time Playback | ❌ | ✅ | MVP |

---

## 3. High-Level Architecture

### 3.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SONICFORGE X ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   DESKTOP APP   │     │   WEB CLIENT    │     │   MOBILE APP    │
│   (Tkinter)     │     │   (Browser)     │     │   (Future)      │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            API GATEWAY                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ /api/compose│  │ /api/mix    │  │ /api/export │  │ /api/voice  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CORE ENGINE                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Composer   │  │  MixMaster  │  │ Cocreator   │  │ SoundDNA    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Session    │  │  Models     │  │  Voice      │  │ AcademyAI   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATA & STORAGE                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Session   │  │   WAV Files │  │   Samples   │  │   Logs      │      │
│  │   State     │  │   Cache     │  │   Library   │  │   Events    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Interaction Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     REQUEST-RESPONSE FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

User Input                    Processing                     Output
    │                             │                             │
    ▼                             ▼                             ▼
┌─────────┐                 ┌─────────────┐               ┌─────────┐
│ Command │────────────────▶│   Parser    │               │ Response│
└─────────┘                 └──────┬──────┘               └─────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │   Router    │
                            └──────┬──────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
           ▼                       ▼                       ▼
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   Compose   │         │     Mix     │         │   Export    │
    │   Engine    │         │   Engine    │         │   Engine    │
    └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
           │                       │                       │
           ▼                       ▼                       ▼
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │  AI Model   │         │  Analyzer   │         │  Renderer   │
    └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │   Session   │
                            │   State     │
                            └─────────────┘
```

### 3.3 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Backend | Python | 3.8+ | Core logic |
| Desktop UI | Tkinter | Built-in | Native interface |
| Web Server | http.server | Built-in | HTTP serving |
| Web Frontend | JavaScript | ES6+ | Browser client |
| Speech-to-Text | faster-whisper | Latest | Voice input |
| Text-to-Speech | edge-tts | Latest | Voice output |
| Audio Processing | wave, struct | Built-in | WAV generation |
| Testing | unittest | Built-in | Unit tests |

---

## 4. Core Module Architecture

### 4.1 Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MODULE DEPENDENCY GRAPH                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   server.py     │◀───────┐
└────────┬────────┘        │
         │                 │
         ▼                 │
┌─────────────────┐        │
│   llm_gateway   │        │
└────────┬────────┘        │
         │                 │
         ▼                 │
┌─────────────────┐        │
│   desktop.py    │◀───────┤
└────────┬────────┘        │
         │                 │
         ▼                 │
┌─────────────────────────────────────────────────────────────────┐
│                         CORE MODULES                             │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   composer.py   │  mixmaster.py   │  cocreator.py   │ voice.py  │
└────────┬────────┴────────┬────────┴────────┬────────┴─────┬─────┘
         │                 │                 │              │
         ▼                 ▼                 ▼              ▼
┌─────────────────┬─────────────────┬─────────────────┬───────────┤
│   models.py     │   session.py    │  sound_dna.py   │ academy_* │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

### 4.2 Core Modules Detailed Breakdown

#### 4.2.1 composer.py - Music Composition Engine

**Purpose**: Generates musical compositions based on emotional parameters and music theory rules.

**Key Classes**:
```python
class Composer:
    """Main composition engine with emotion-driven generation"""
    
    def __init__(self, session: Session):
        self.session = session
        self.chord_progressions = self._load_progressions()
        self.scale_patterns = self._load_scales()
    
    def compose(self, emotion: str, tempo: int, key: str) -> CompositionResult:
        """Generate a composition based on parameters"""
        pass
    
    def _apply_music_theory(self, notes: List[Note]) -> List[Note]:
        """Apply voice leading and harmony rules"""
        pass
```

**Algorithm**: Emotion-to-Music Mapping
```
Input: emotion, tempo, key
Output: CompositionResult

1. Map emotion to musical parameters:
   - happy → major key, fast tempo, ascending patterns
   - sad → minor key, slow tempo, descending patterns
   - energetic → fast tempo, complex rhythms
   - calm → slow tempo, simple harmonies

2. Generate chord progression:
   - Select progression template based on emotion
   - Apply key signature transformations
   - Add variations and substitutions

3. Generate melody:
   - Use scale patterns from key
   - Apply rhythm patterns from tempo
   - Add melodic ornaments

4. Apply voice leading:
   - Resolve dissonances
   - Maintain smooth voice motion
   - Add bass line

5. Return composition with metadata
```

#### 4.2.2 mixmaster.py - Audio Mixing Engine

**Purpose**: Analyzes and optimizes audio mixes with suggestions for improvement.

**Key Classes**:
```python
class MixMaster:
    """Audio mixing and mastering engine"""
    
    def analyze_mix(self, tracks: List[Track]) -> MixAnalysis:
        """Analyze mix for issues"""
        pass
    
    def auto_mix(self, tracks: List[Track]) -> List[Track]:
        """Apply automatic mixing"""
        pass
    
    def generate_suggestions(self, analysis: MixAnalysis) -> List[Suggestion]:
        """Generate improvement suggestions"""
        pass
```

**Algorithm**: Mix Analysis Pipeline
```
Input: List[Track]
Output: MixAnalysis

1. Frequency Analysis:
   - Compute FFT for each track
   - Identify frequency conflicts
   - Detect masking issues

2. Dynamic Range Analysis:
   - Calculate RMS levels
   - Measure peak levels
   - Compute dynamic range

3. Stereo Analysis:
   - Measure stereo width
   - Check mono compatibility
   - Detect phase issues

4. Generate Metrics:
   - Headroom: peak_level - 0dB
   - Low-end focus: energy below 200Hz
   - Stereo width: correlation coefficient

5. Return analysis with issues and suggestions
```

#### 4.2.3 cocreator.py - AI Suggestion Engine

**Purpose**: Generates creative suggestions for music arrangement and production.

**Key Classes**:
```python
class Cocreator:
    """AI-powered creative suggestion engine"""
    
    def analyze_composition(self, composition: Composition) -> Analysis:
        """Analyze composition for improvement areas"""
        pass
    
    def generate_suggestions(self, analysis: Analysis) -> List[Suggestion]:
        """Generate creative suggestions"""
        pass
```

#### 4.2.4 sound_dna.py - Sound Design Engine

**Purpose**: Generates unique sound timbres and textures.

**Key Classes**:
```python
class SoundDNA:
    """Sound design and timbre generation"""
    
    def generate_dna(self, parameters: Dict) -> SoundProfile:
        """Generate sound DNA profile"""
        pass
    
    def synthesize(self, profile: SoundProfile) -> AudioBuffer:
        """Synthesize audio from profile"""
        pass
```

#### 4.2.5 voice.py - Voice Processing

**Purpose**: Handles voice input/output with speech recognition and synthesis.

**Key Classes**:
```python
class Voice:
    """Voice processing and synthesis"""
    
    def recognize_speech(self, audio: AudioBuffer) -> str:
        """Convert speech to text"""
        pass
    
    def synthesize_speech(self, text: str) -> AudioBuffer:
        """Convert text to speech"""
        pass
```

#### 4.2.6 session.py - Session Management

**Purpose**: Manages application state and event logging.

**Key Classes**:
```python
class Session:
    """Application session state manager"""
    
    def __init__(self):
        self.state = {}
        self.event_log = []
    
    def log_event(self, event_type: str, data: Dict):
        """Log an event"""
        pass
    
    def get_state(self, key: str) -> Any:
        """Get state value"""
        pass
    
    def set_state(self, key: str, value: Any):
        """Set state value"""
        pass
```

#### 4.2.7 models.py - Data Models

**Purpose**: Defines data structures for the application.

**Key Dataclasses**:
```python
@dataclass
class Note:
    pitch: int          # MIDI note number (0-127)
    velocity: int       # Note velocity (0-127)
    start_time: float   # Start time in beats
    duration: float     # Duration in beats
    channel: int        # MIDI channel (0-15)

@dataclass
class Track:
    name: str
    instrument: str
    notes: List[Note]
    volume: float       # 0.0 to 1.0
    pan: float          # -1.0 (left) to 1.0 (right)
    effects: List[str]

@dataclass
class Composition:
    title: str
    key: str
    tempo: int
    time_signature: Tuple[int, int]
    tracks: List[Track]
    metadata: Dict

@dataclass
class Suggestion:
    id: str
    type: str           # 'arrangement', 'mix', 'sound_design'
    description: str
    parameters: Dict
    impact: float       # 0.0 to 1.0
```

#### 4.2.8 academy_ai.py - Harmonium Academy AI

**Purpose**: Provides conversational AI coaching for harmonium learning.

**Key Classes**:
```python
@dataclass
class AcademySection:
    id: str
    title: str
    chunks: List[str]
    aliases: List[str]

@dataclass
class AcademyCoachState:
    enabled: bool
    paused: bool
    current_section_index: int
    current_chunk_index: int

class AcademyAI:
    """Conversational AI for harmonium academy"""
    
    def process_utterance(self, text: str, state: AcademyCoachState) -> AcademyDecision:
        """Process user utterance and generate response"""
        pass
```

#### 4.2.9 academy_stt.py & academy_tts.py - Speech Processing

**Purpose**: Speech-to-text and text-to-speech for academy voice coach.

**Key Functions**:
```python
# academy_stt.py
def transcribe_audio(audio_data: bytes) -> str:
    """Transcribe audio to text using faster-whisper"""
    pass

# academy_tts.py
def synthesize_speech(text: str, voice: str) -> bytes:
    """Synthesize speech using edge-tts"""
    pass
```

---

## 5. Algorithm Deep Dive

### 5.1 Emotion-to-Music Mapping Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   EMOTION-TO-MUSIC MAPPING ALGORITHM                        │
└─────────────────────────────────────────────────────────────────────────────┘

Input Parameters:
  - emotion: str (happy, sad, energetic, calm, mysterious, romantic)
  - tempo: int (BPM)
  - key: str (C, D, E, F, G, A, B + major/minor)

Algorithm:

1. EMOTION PARAMETER EXTRACTION:
   ┌─────────────────────────────────────────────────────────────┐
   │ emotion_params = {                                          │
   │     'happy': {'mode': 'major', 'tempo_range': [100, 140],  │
   │              'intensity': 0.8, 'complexity': 0.6},          │
   │     'sad': {'mode': 'minor', 'tempo_range': [60, 80],      │
   │            'intensity': 0.4, 'complexity': 0.3},            │
   │     'energetic': {'mode': 'major', 'tempo_range': [120, 160],│
   │                  'intensity': 1.0, 'complexity': 0.8},      │
   │     'calm': {'mode': 'major', 'tempo_range': [60, 90],     │
   │             'intensity': 0.3, 'complexity': 0.2},           │
   │     'mysterious': {'mode': 'minor', 'tempo_range': [70, 100],│
   │                   'intensity': 0.6, 'complexity': 0.7},     │
   │     'romantic': {'mode': 'minor', 'tempo_range': [70, 100], │
   │                 'intensity': 0.5, 'complexity': 0.5}        │
   │ }                                                           │
   └─────────────────────────────────────────────────────────────┘

2. SCALE SELECTION:
   ┌─────────────────────────────────────────────────────────────┐
   │ IF mode == 'major':                                         │
   │   scale = major_scale_patterns[key]                         │
   │   chords = major_chord_progressions                         │
   │ ELSE:                                                       │
   │   scale = minor_scale_patterns[key]                         │
   │   chords = minor_chord_progressions                         │
   └─────────────────────────────────────────────────────────────┘

3. CHORD PROGRESSION GENERATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ progression = random.choice(chords)                         │
   │ # Example: I-V-vi-IV for happy, i-iv-v-i for sad           │
   │                                                             │
   │ FOR each chord in progression:                              │
   │   notes = chord_to_notes(chord, key)                        │
   │   voicing = apply_voice_leading(notes, previous_notes)      │
   │   rhythm = generate_rhythm(tempo, intensity)                │
   └─────────────────────────────────────────────────────────────┘

4. MELODY GENERATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ melody_notes = []                                           │
   │ current_note = scale[0]  # Start on root                    │
   │                                                             │
   │ FOR i in range(num_measures * beats_per_measure):           │
   │   # Apply melodic contour based on emotion                  │
   │   IF emotion == 'happy':                                    │
   │     direction = weighted_choice([↑, →, ↓], [0.5, 0.3, 0.2])│
   │   ELSE IF emotion == 'sad':                                 │
   │     direction = weighted_choice([↓, →, ↑], [0.5, 0.3, 0.2])│
   │                                                             │
   │   next_note = move_in_scale(current_note, direction, scale) │
   │   duration = random.choice([0.25, 0.5, 1.0])  # in beats   │
   │                                                             │
   │   melody_notes.append(Note(next_note, velocity, i, duration))│
   │   current_note = next_note                                  │
   └─────────────────────────────────────────────────────────────┘

5. BASS LINE GENERATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ bass_notes = []                                             │
   │                                                             │
   │ FOR each chord in progression:                              │
   │   root = chord_root(chord)                                  │
   │   bass_note = root - 24  # Two octaves lower                │
   │   rhythm = bass_rhythm_pattern(tempo)                       │
   │                                                             │
   │   FOR beat in rhythm:                                       │
   │     bass_notes.append(Note(bass_note, 100, beat, 0.5))     │
   └─────────────────────────────────────────────────────────────┘

6. ARRANGEMENT ASSEMBLY:
   ┌─────────────────────────────────────────────────────────────┐
   │ composition = Composition(                                  │
   │     title=f"{emotion.title()} in {key}",                    │
   │     key=key,                                                │
   │     tempo=tempo,                                            │
   │     time_signature=(4, 4),                                  │
   │     tracks=[                                                 │
   │         Track("Melody", "piano", melody_notes, 0.8, 0.0),   │
   │         Track("Chords", "piano", chord_notes, 0.6, -0.3),   │
   │         Track("Bass", "bass", bass_notes, 0.7, 0.0)         │
   │     ]                                                        │
   │ )                                                           │
   │                                                             │
   │ RETURN composition                                          │
   └─────────────────────────────────────────────────────────────┘

Output: Composition object with tracks, metadata, and parameters
```

### 5.2 Voice Leading Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      VOICE LEADING ALGORITHM                                │
└─────────────────────────────────────────────────────────────────────────────┘

Purpose: Ensure smooth transitions between chords by minimizing voice movement.

Input: current_voices (List[int]), next_chord (List[int])
Output: next_voices (List[int])

Algorithm:

1. INITIALIZATION:
   next_voices = []
   available_notes = sorted(next_chord * 2)  # Duplicate for octave options

2. FOR each voice in current_voices:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Find closest note in next chord                           │
   │ min_distance = infinity                                     │
   │ best_note = None                                            │
   │                                                             │
   │ FOR note in available_notes:                                │
   │   distance = abs(voice - note)                              │
   │   IF distance < min_distance:                               │
   │     min_distance = distance                                 │
   │     best_note = note                                        │
   │                                                             │
   │ # Prefer movement by step (semitone or tone)                │
   │ IF min_distance <= 2:                                       │
   │   next_voices.append(best_note)                             │
   │   available_notes.remove(best_note)                         │
   │ ELSE:                                                       │
   │   # Find note within octave range                           │
   │   candidates = [n for n in available_notes                  │
   │                 if abs(n - voice) <= 12]                    │
   │   IF candidates:                                            │
   │     best = min(candidates, key=lambda n: abs(n - voice))    │
   │     next_voices.append(best)                                │
   │     available_notes.remove(best)                            │
   └─────────────────────────────────────────────────────────────┘

3. RULES APPLIED:
   - Parallel fifths/octaves avoided
   - Voice crossing avoided
   - Tendency tones resolved
   - Common tones retained when possible

4. RETURN next_voices
```

### 5.3 Mix Analysis Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MIX ANALYSIS ALGORITHM                                 │
└─────────────────────────────────────────────────────────────────────────────┘

Input: tracks (List[Track])
Output: MixAnalysis

Algorithm:

1. FREQUENCY ANALYSIS:
   ┌─────────────────────────────────────────────────────────────┐
   │ frequency_bins = {                                          │
   │     'sub': (20, 60),        # Sub-bass                     │
   │     'bass': (60, 250),      # Bass                         │
   │     'low_mid': (250, 500),  # Low-mids                     │
   │     'mid': (500, 2000),     # Mids                         │
   │     'high_mid': (2000, 4000), # High-mids                  │
   │     'high': (4000, 20000)   # Highs                        │
   │ }                                                           │
   │                                                             │
   │ FOR each track in tracks:                                   │
   │   fft_result = FFT(track.audio_data)                        │
   │   FOR band, (low, high) in frequency_bins.items():          │
   │     band_energy = sum(fft_result[low:high])                 │
   │     track.energy[band] = band_energy                        │
   │                                                             │
   │ # Detect frequency conflicts                                │
   │ FOR band in frequency_bins:                                 │
   │   tracks_in_band = [t for t in tracks if t.energy[band] > 0.1]│
   │   IF len(tracks_in_band) > 2:                               │
   │     issues.append(FrequencyConflict(band, tracks_in_band))  │
   └─────────────────────────────────────────────────────────────┘

2. DYNAMIC RANGE ANALYSIS:
   ┌─────────────────────────────────────────────────────────────┐
   │ FOR each track in tracks:                                   │
   │   rms = sqrt(mean(audio_data ** 2))                         │
   │   peak = max(abs(audio_data))                               │
   │   dynamic_range = 20 * log10(peak / rms)  # in dB          │
   │                                                             │
   │   IF dynamic_range < 6:                                     │
   │     issues.append(OverCompression(track))                   │
   │   IF dynamic_range > 20:                                    │
   │     issues.append(UnderCompression(track))                  │
   │                                                             │
   │ # Calculate headroom                                        │
   │ master_peak = max(t.peak for t in tracks)                   │
   │ headroom = 0 - master_peak  # dB until clipping             │
   │                                                             │
   │ IF headroom < 3:                                            │
   │     issues.append(LowHeadroom(headroom))                    │
   └─────────────────────────────────────────────────────────────┘

3. STEREO ANALYSIS:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Calculate stereo width                                    │
   │ mid = (left + right) / 2                                    │
   │ side = (left - right) / 2                                   │
   │ stereo_width = energy(side) / energy(mid)                   │
   │                                                             │
   │ # Check mono compatibility                                  │
   │ mono_sum = left + right                                     │
   │ IF abs(energy(mono_sum) - energy(mid)) > 0.1:               │
   │     issues.append(PhaseIssue(track))                        │
   │                                                             │
   │ # Calculate correlation                                     │
   │ correlation = correlate(left, right)                        │
   │ IF correlation < 0.5:                                       │
   │     issues.append(MonoIncompatible(track))                  │
   └─────────────────────────────────────────────────────────────┘

4. GENERATE METRICS:
   ┌─────────────────────────────────────────────────────────────┐
   │ metrics = {                                                 │
   │     'headroom': headroom,                                   │
   │     'stereo_width': stereo_width,                           │
   │     'low_end_focus': sum(t.energy['bass'] for t in tracks), │
   │     'dynamic_range': mean([t.dynamic_range for t in tracks]),│
   │     'frequency_balance': calculate_balance(tracks),         │
   │     'loudness': calculate_lufs(tracks)                      │
   │ }                                                           │
   └─────────────────────────────────────────────────────────────┘

5. RETURN MixAnalysis(metrics, issues, suggestions)
```

### 5.4 Academy AI Conversation Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   ACADEMY AI CONVERSATION ALGORITHM                         │
└─────────────────────────────────────────────────────────────────────────────┘

Input: user_text (str), state (AcademyCoachState)
Output: AcademyDecision

Algorithm:

1. TEXT NORMALIZATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ normalized = user_text.lower()                              │
   │ # Apply term replacements                                   │
   │ replacements = {                                            │
   │     'what is': 'what',                                      │
   │     'tell me about': 'explain',                             │
   │     'how do i': 'how to',                                   │
   │     'can you': 'please'                                     │
   │ }                                                           │
   │ for old, new in replacements.items():                       │
   │     normalized = normalized.replace(old, new)               │
   │                                                             │
   │ # Remove punctuation                                        │
   │ normalized = ''.join(c for c in normalized if c.isalnum() or c == ' ')│
   └─────────────────────────────────────────────────────────────┘

2. TOKENIZATION & STEMming:
   ┌─────────────────────────────────────────────────────────────┐
   │ tokens = normalized.split()                                 │
   │ # Remove stop words                                         │
   │ stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were'}│
   │ tokens = [t for t in tokens if t not in stop_words]         │
   │                                                             │
   │ # Simple stemming                                           │
   │ stemmed = [stem(t) for t in tokens]                         │
   │ # Example: 'playing' → 'play', 'notes' → 'note'            │
   └─────────────────────────────────────────────────────────────┘

3. INTENT CLASSIFICATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Pattern matching for intents                              │
   │ patterns = {                                                │
   │     'greeting': ['hello', 'hi', 'hey', 'namaste'],          │
   │     'farewell': ['bye', 'goodbye', 'see you', 'thank you'], │
   │     'control': ['pause', 'resume', 'stop', 'start'],        │
   │     'navigate': ['go to', 'jump to', 'next', 'previous'],   │
   │     'question': ['what', 'how', 'why', 'when', 'where'],    │
   │     'repeat': ['repeat', 'again', 'once more']              │
   │ }                                                           │
   │                                                             │
   │ FOR intent, keywords in patterns.items():                   │
   │   IF any(keyword in normalized for keyword in keywords):    │
   │     detected_intent = intent                                │
   │     BREAK                                                   │
   └─────────────────────────────────────────────────────────────┘

4. COMMAND PROCESSING:
   ┌─────────────────────────────────────────────────────────────┐
   │ IF detected_intent == 'control':                            │
   │   IF 'pause' in normalized:                                 │
   │     state.paused = True                                     │
   │     RETURN AcademyDecision(action='pause',                  │
   │            reply='Okay, I will pause. Say resume to continue.')│
   │   ELIF 'resume' in normalized:                              │
   │     state.paused = False                                    │
   │     RETURN AcademyDecision(action='resume',                 │
   │            reply='Resuming lesson. Where were we?')          │
   │                                                             │
   │ IF detected_intent == 'navigate':                           │
   │   target = find_target(normalized, sections)                │
   │   IF target:                                                │
   │     state.current_section_index = target.section_index      │
   │     state.current_chunk_index = target.chunk_index          │
   │     RETURN AcademyDecision(action='navigate',               │
   │            section_index=target.section_index,              │
   │            chunk_index=target.chunk_index,                  │
   │            reply=f'Going to {target.label}')                 │
   └─────────────────────────────────────────────────────────────┘

5. KNOWLEDGE RETRIEVAL:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Search sections for matching content                      │
   │ best_match = None                                           │
   │ best_score = 0                                              │
   │                                                             │
   │ FOR section in sections:                                    │
   │   FOR chunk in section.chunks:                              │
   │     score = phrase_similarity(normalized, chunk)            │
   │     IF score > best_score:                                  │
   │       best_score = score                                    │
   │       best_match = (section, chunk)                         │
   │                                                             │
   │ IF best_score > 0.3:                                        │
   │   section, chunk = best_match                               │
   │   RETURN AcademyDecision(                                   │
   │     action='answer',                                        │
   │     reply=chunk,                                            │
   │     section_index=sections.index(section),                  │
   │     chunk_index=section.chunks.index(chunk)                 │
   │   )                                                         │
   └─────────────────────────────────────────────────────────────┘

6. FALLBACK RESPONSE:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Generate contextual fallback                              │
   │ current_section = sections[state.current_section_index]     │
   │ fallbacks = [                                               │
   │     f"I'm not sure about that. Would you like to know about {current_section.title}?",│
   │     "That's an interesting question. Let me think about it.",│
   │     "I'm still learning about that. Can you ask something else?"│
   │ ]                                                           │
   │                                                             │
   │ RETURN AcademyDecision(                                     │
   │   action='fallback',                                        │
   │   reply=random.choice(fallbacks),                           │
   │   should_continue=True                                      │
   │ )                                                           │
   └─────────────────────────────────────────────────────────────┘

7. RETURN decision
```

### 5.5 WAV Generation Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      WAV GENERATION ALGORITHM                               │
└─────────────────────────────────────────────────────────────────────────────┘

Input: composition (Composition), sample_rate (int, default 44100)
Output: bytes (WAV file data)

Algorithm:

1. INITIALIZATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Calculate total duration                                  │
   │ max_time = 0                                                │
   │ FOR track in composition.tracks:                            │
   │   FOR note in track.notes:                                  │
   │     end_time = note.start_time + note.duration              │
   │     IF end_time > max_time:                                 │
   │       max_time = end_time                                   │
   │                                                             │
   │ total_samples = int(max_time * sample_rate)                 │
   │ audio_buffer = zeros(total_samples)                         │
   └─────────────────────────────────────────────────────────────┘

2. NOTE SYNTHESIS:
   ┌─────────────────────────────────────────────────────────────┐
   │ FOR each track in composition.tracks:                       │
   │   FOR each note in track.notes:                             │
   │     # Calculate note parameters                             │
   │     frequency = 440 * 2^((note.pitch - 69) / 12)  # A4=440Hz│
   │     start_sample = int(note.start_time * sample_rate)       │
   │     duration_samples = int(note.duration * sample_rate)     │
   │                                                             │
   │     # Generate waveform based on instrument                 │
   │     IF track.instrument == 'piano':                         │
   │       waveform = generate_piano_waveform(                   │
   │         frequency, duration_samples, note.velocity          │
   │       )                                                     │
   │     ELIF track.instrument == 'bass':                        │
   │       waveform = generate_bass_waveform(                    │
   │         frequency, duration_samples, note.velocity          │
   │       )                                                     │
   │                                                             │
   │     # Apply envelope (ADSR)                                 │
   │     envelope = generate_adsr_envelope(                      │
   │       attack=0.01, decay=0.1, sustain=0.7, release=0.2,    │
   │       duration=duration_samples                             │
   │     )                                                       │
   │     waveform = waveform * envelope                          │
   │                                                             │
   │     # Apply track volume and pan                            │
   │     waveform = waveform * track.volume                      │
   │     # Pan: -1.0 (left) to 1.0 (right)                       │
   │     left_gain = (1 - track.pan) / 2                         │
   │     right_gain = (1 + track.pan) / 2                        │
   │                                                             │
   │     # Mix into buffer                                       │
   │     audio_buffer[start_sample:start_sample+duration_samples] += waveform│
   └─────────────────────────────────────────────────────────────┘

3. WAVEFORM GENERATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ def generate_piano_waveform(frequency, samples, velocity):  │
   │   t = arange(samples) / sample_rate                         │
   │                                                             │
   │   # Fundamental                                             │
   │   fundamental = sin(2 * pi * frequency * t)                 │
   │                                                             │
   │   # Add harmonics (piano has rich harmonic content)         │
   │   harmonic2 = 0.5 * sin(2 * pi * 2 * frequency * t)        │
   │   harmonic3 = 0.25 * sin(2 * pi * 3 * frequency * t)       │
   │   harmonic4 = 0.125 * sin(2 * pi * 4 * frequency * t)      │
   │                                                             │
   │   # Combine harmonics                                       │
   │   waveform = fundamental + harmonic2 + harmonic3 + harmonic4│
   │                                                             │
   │   # Apply velocity                                          │
   │   waveform = waveform * (velocity / 127.0)                  │
   │                                                             │
   │   return waveform                                           │
   └─────────────────────────────────────────────────────────────┘

4. ENVELOPE GENERATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ def generate_adsr_envelope(attack, decay, sustain, release, │
   │                           duration):                        │
   │   envelope = zeros(duration)                                │
   │                                                             │
   │   # Attack phase                                            │
   │   attack_samples = int(attack * sample_rate)                │
   │   envelope[0:attack_samples] = linspace(0, 1, attack_samples)│
   │                                                             │
   │   # Decay phase                                             │
   │   decay_samples = int(decay * sample_rate)                  │
   │   decay_start = attack_samples                              │
   │   decay_end = decay_start + decay_samples                   │
   │   envelope[decay_start:decay_end] = linspace(1, sustain,    │
   │                                             decay_samples)  │
   │                                                             │
   │   # Sustain phase                                           │
   │   sustain_start = decay_end                                 │
   │   sustain_end = duration - int(release * sample_rate)       │
   │   envelope[sustain_start:sustain_end] = sustain             │
   │                                                             │
   │   # Release phase                                           │
   │   release_samples = sustain_end - sustain_start             │
   │   envelope[sustain_end:] = linspace(sustain, 0,             │
   │                                     release_samples)        │
   │                                                             │
   │   return envelope                                           │
   └─────────────────────────────────────────────────────────────┘

5. NORMALIZATION:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Normalize to prevent clipping                             │
   │ max_amplitude = max(abs(audio_buffer))                      │
   │ IF max_amplitude > 1.0:                                     │
   │   audio_buffer = audio_buffer / max_amplitude * 0.9  # Leave headroom│
   └─────────────────────────────────────────────────────────────┘

6. WAV ENCODING:
   ┌─────────────────────────────────────────────────────────────┐
   │ # Create WAV file structure                                 │
   │ wav_file = BytesIO()                                        │
   │                                                             │
   │ # Write WAV header                                          │
   │ write_wav_header(wav_file, sample_rate, total_samples)      │
   │                                                             │
   │ # Write audio data                                          │
   │ FOR sample in audio_buffer:                                 │
   │   # Convert to 16-bit integer                               │
   │   int_sample = int(sample * 32767)                          │
   │   wav_file.write(struct.pack('<h', int_sample))             │
   │                                                             │
   │ RETURN wav_file.getvalue()                                  │
   └─────────────────────────────────────────────────────────────┘

Output: WAV file bytes ready for playback or export
```

---

## 6. Data Structures & Models

### 6.1 Core Data Models

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum

class Emotion(Enum):
    """Musical emotions for composition"""
    HAPPY = "happy"
    SAD = "sad"
    ENERGETIC = "energetic"
    CALM = "calm"
    MYSTERIOUS = "mysterious"
    ROMANTIC = "romantic"

class Instrument(Enum):
    """Available instruments"""
    PIANO = "piano"
    BASS = "bass"
    DRUMS = "drums"
    GUITAR = "guitar"
    SYNTH = "synth"
    HARMONIUM = "harmonium"

@dataclass
class Note:
    """Musical note representation"""
    pitch: int          # MIDI note number (0-127)
    velocity: int       # Note velocity/loudness (0-127)
    start_time: float   # Start time in beats
    duration: float     # Duration in beats
    channel: int = 0    # MIDI channel (0-15)
    
    @property
    def frequency(self) -> float:
        """Calculate frequency from MIDI pitch"""
        return 440.0 * (2.0 ** ((self.pitch - 69) / 12.0))
    
    @property
    def note_name(self) -> str:
        """Get note name (C, D, E, etc.)"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return notes[self.pitch % 12]

@dataclass
class Track:
    """Audio track representation"""
    name: str
    instrument: str
    notes: List[Note]
    volume: float = 0.8       # 0.0 to 1.0
    pan: float = 0.0          # -1.0 (left) to 1.0 (right)
    muted: bool = False
    solo: bool = False
    effects: List[str] = None
    
    def __post_init__(self):
        if self.effects is None:
            self.effects = []
    
    @property
    def total_duration(self) -> float:
        """Calculate total track duration in beats"""
        if not self.notes:
            return 0.0
        return max(n.start_time + n.duration for n in self.notes)

@dataclass
class Composition:
    """Complete music composition"""
    title: str
    key: str                    # e.g., "C", "Am", "F#"
    tempo: int                  # BPM
    time_signature: Tuple[int, int]  # e.g., (4, 4)
    tracks: List[Track]
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def duration_seconds(self) -> float:
        """Calculate total duration in seconds"""
        max_beats = max(t.total_duration for t in self.tracks) if self.tracks else 0
        return (max_beats / self.tempo) * 60

@dataclass
class MixAnalysis:
    """Mix analysis results"""
    metrics: Dict[str, float]
    issues: List[str]
    suggestions: List[str]
    timestamp: float = 0.0

@dataclass
class Suggestion:
    """AI-generated suggestion"""
    id: str
    type: str                   # 'arrangement', 'mix', 'sound_design'
    description: str
    parameters: Dict
    impact: float = 0.5         # 0.0 to 1.0
    applied: bool = False

@dataclass
class SessionState:
    """Application session state"""
    current_composition: Optional[Composition] = None
    history: List[Dict] = None
    preferences: Dict = None
    last_action: str = ""
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
        if self.preferences is None:
            self.preferences = {}

@dataclass
class AcademySection:
    """Academy lesson section"""
    id: str
    title: str
    eyebrow: str = ""           # Subtitle
    chunks: List[str] = None    # Lesson content chunks
    aliases: List[str] = None   # Alternative names
    
    def __post_init__(self):
        if self.chunks is None:
            self.chunks = []
        if self.aliases is None:
            self.aliases = []

@dataclass
class AcademyCoachState:
    """Academy voice coach state"""
    enabled: bool = False
    paused: bool = False
    awaiting_consent: bool = False
    current_section_index: int = 0
    current_chunk_index: int = 0
    conversation_history: List[Dict] = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []

@dataclass
class AcademyDecision:
    """Academy AI decision output"""
    action: str                 # 'answer', 'navigate', 'pause', 'resume', 'fallback'
    reply: str                  # Response text
    section_index: int = 0
    chunk_index: int = 0
    should_continue: bool = True
    focus_label: str = ""
    voice_style: str = "friendly"
    ambience_mode: str = "default"
    reply_language: str = "en"
```

### 6.2 Enumerations

```python
class SuggestionType(Enum):
    """Types of AI suggestions"""
    ARRANGEMENT = "arrangement"
    MIX = "mix"
    SOUND_DESIGN = "sound_design"
    HARMONY = "harmony"
    RHYTHM = "rhythm"

class AcademyAction(Enum):
    """Academy coach actions"""
    ANSWER = "answer"
    NAVIGATE = "navigate"
    PAUSE = "pause"
    RESUME = "resume"
    REPEAT = "repeat"
    FALLBACK = "fallback"
    CONSENT = "consent"
```

### 6.3 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW DIAGRAM                                   │
└─────────────────────────────────────────────────────────────────────────────┘

User Input                    Processing                      Output
    │                              │                              │
    ▼                              ▼                              ▼
┌─────────┐                  ┌───────────┐                  ┌─────────┐
│ Emotion │─────────────────▶│ Composer  │─────────────────▶│Composition│
│ Params  │                  │           │                  │ Object  │
└─────────┘                  └───────────┘                  └─────────┘
    │                              │                              │
    ▼                              ▼                              ▼
┌─────────┐                  ┌───────────┐                  ┌─────────┐
│ Track   │─────────────────▶│ MixMaster │─────────────────▶│MixAnalysis│
│ Data    │                  │           │                  │         │
└─────────┘                  └───────────┘                  └─────────┘
    │                              │                              │
    ▼                              ▼                              ▼
┌─────────┐                  ┌───────────┐                  ┌─────────┐
│ Session │─────────────────▶│ Cocreator │─────────────────▶│Suggestions│
│ State   │                  │           │                  │         │
└─────────┘                  └───────────┘                  └─────────┘
    │                              │                              │
    ▼                              ▼                              ▼
┌─────────┐                  ┌───────────┐                  ┌─────────┐
│ Voice   │─────────────────▶│ AcademyAI │─────────────────▶│AcademyDecision│
│ Input   │                  │           │                  │         │
└─────────┘                  └───────────┘                  └─────────┘
```

---

## 7. API Gateway & Endpoints

### 7.1 HTTP Server Implementation

```python
# sonicforge/apps/server.py

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class SonicForgeHandler(BaseHTTPRequestHandler):
    """HTTP request handler for SonicForge API"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == '/':
            self.serve_file('web/index.html', 'text/html')
        elif path == '/api/status':
            self.send_json_response({'status': 'running', 'version': '1.0.0'})
        elif path.startswith('/api/'):
            self.handle_api_get(path)
        else:
            self.serve_static_file(path)
    
    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')
            return
        
        if path == '/api/compose':
            self.handle_compose(data)
        elif path == '/api/auto-mix':
            self.handle_auto_mix(data)
        elif path == '/api/export-wav':
            self.handle_export_wav(data)
        elif path == '/api/apply-suggestion':
            self.handle_apply_suggestion(data)
        elif path == '/api/academy/chat':
            self.handle_academy_chat(data)
        else:
            self.send_error(404, 'Not Found')
```

### 7.2 API Endpoints Specification

#### 7.2.1 Composition Endpoint
```
POST /api/compose
Content-Type: application/json

Request Body:
{
  "emotion": "happy",           // Required: happy, sad, energetic, calm, mysterious, romantic
  "tempo": 120,                 // Required: 40-200 BPM
  "key": "C",                   // Required: C, D, E, F, G, A, B (+ #/b)
  "time_signature": [4, 4],     // Optional: [beats, note_value]
  "tracks": 3,                  // Optional: number of tracks
  "duration": 32                // Optional: duration in bars
}

Response:
{
  "success": true,
  "composition": {
    "title": "Happy in C",
    "key": "C",
    "tempo": 120,
    "time_signature": [4, 4],
    "tracks": [
      {
        "name": "Melody",
        "instrument": "piano",
        "notes": [
          {"pitch": 60, "velocity": 100, "start_time": 0.0, "duration": 1.0},
          ...
        ],
        "volume": 0.8,
        "pan": 0.0
      },
      ...
    ],
    "duration_seconds": 12.0
  },
  "metrics": {
    "total_notes": 45,
    "tracks_count": 3,
    "complexity_score": 0.65
  }
}
```

#### 7.2.2 Auto-Mix Endpoint
```
POST /api/auto-mix
Content-Type: application/json

Request Body:
{
  "tracks": [                   // Required: array of tracks
    {
      "name": "Melody",
      "instrument": "piano",
      "notes": [...],
      "volume": 0.8,
      "pan": 0.0
    },
    ...
  ],
  "target_loudness": -14        // Optional: target LUFS
}

Response:
{
  "success": true,
  "analysis": {
    "metrics": {
      "headroom": 6.2,
      "stereo_width": 0.75,
      "low_end_focus": 0.45,
      "dynamic_range": 12.5,
      "loudness": -18.2
    },
    "issues": [
      "Low headroom on track 'Bass'",
      "Frequency conflict in 200-400Hz range"
    ],
    "suggestions": [
      "Reduce bass volume by 3dB",
      "Apply high-pass filter to melody above 150Hz"
    ]
  },
  "mixed_tracks": [...],        // Optimized tracks
  "applied_changes": [
    {"track": "Bass", "parameter": "volume", "from": 0.9, "to": 0.63},
    ...
  ]
}
```

#### 7.2.3 Export WAV Endpoint
```
POST /api/export-wav
Content-Type: application/json

Request Body:
{
  "composition": { ... },       // Required: composition object
  "sample_rate": 44100,         // Optional: 22050, 44100, 48000
  "bit_depth": 16,              // Optional: 16, 24, 32
  "normalize": true             // Optional: normalize audio
}

Response:
Content-Type: audio/wav
Content-Disposition: attachment; filename="composition.wav"

[WAV binary data]
```

#### 7.2.4 Apply Suggestion Endpoint
```
POST /api/apply-suggestion
Content-Type: application/json

Request Body:
{
  "suggestion_id": "sug_001",   // Required: suggestion ID
  "composition": { ... },       // Required: current composition
  "parameters": {}              // Optional: override parameters
}

Response:
{
  "success": true,
  "modified_composition": { ... },
  "changes_applied": [
    {"type": "arrangement", "description": "Added harmony track"},
    ...
  ]
}
```

#### 7.2.5 Academy Chat Endpoint
```
POST /api/academy/chat
Content-Type: application/json

Request Body:
{
  "text": "What is a sargam?",  // Required: user message
  "language": "en",             // Optional: en, hi
  "state": {                    // Optional: current coach state
    "enabled": true,
    "paused": false,
    "current_section_index": 0,
    "current_chunk_index": 0
  }
}

Response:
{
  "success": true,
  "decision": {
    "action": "answer",
    "reply": "Sargam is the Indian solfège system...",
    "section_index": 0,
    "chunk_index": 2,
    "should_continue": true,
    "voice_style": "friendly",
    "ambience_mode": "default"
  },
  "updated_state": { ... },
  "audio_url": "/api/academy/audio/reply_001.wav"  // Optional TTS audio
}
```

### 7.3 API Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API REQUEST FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Client                    Server                     Core Engine
  │                          │                            │
  │  POST /api/compose       │                            │
  │  {emotion, tempo, key}   │                            │
  │─────────────────────────▶│                            │
  │                          │                            │
  │                          │  Parse request             │
  │                          │  Validate parameters       │
  │                          │───────────────────────────▶│
  │                          │                            │
  │                          │                            │  Generate composition
  │                          │                            │  Apply music theory
  │                          │                            │  Return Composition
  │                          │◀───────────────────────────│
  │                          │                            │
  │                          │  Format response           │
  │                          │  Calculate metrics         │
  │  200 OK                  │                            │
  │  {composition, metrics}  │                            │
  │◀─────────────────────────│                            │
  │                          │                            │
```

---

## 8. Web Frontend Architecture

### 8.1 JavaScript Module Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      WEB FRONTEND ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         index.html                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Header    │  │   Main      │  │   Footer    │            │
│  │   Nav       │  │   Content   │  │             │            │
│  └─────────────┘  └──────┬──────┘  └─────────────┘            │
│                          │                                      │
│  ┌───────────────────────┼───────────────────────┐            │
│  │                       │                       │            │
│  ▼                       ▼                       ▼            │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│ │  Composer   │  │   Mixer     │  │  Harmonium  │            │
│ │  Panel      │  │   Panel     │  │   Panel     │            │
│ └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│        │                │                │                      │
│        ▼                ▼                ▼                      │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│ │   app.js    │  │  mixer.js   │  │harmonium.js │            │
│ │             │  │             │  │             │            │
│ └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Core JavaScript Functions

#### 8.2.1 API Communication Module (app.js)

```javascript
// sonicforge/web/app.js

class SonicForgeAPI {
    constructor() {
        this.baseUrl = this.discoverApiBase();
        this.sessionId = this.generateSessionId();
    }
    
    /**
     * Discover API base URL from candidate endpoints
     * @returns {string} API base URL
     */
    discoverApiBase() {
        const candidates = [
            'http://127.0.0.1:8000',
            'http://localhost:8000',
            window.location.origin
        ];
        
        for (const base of candidates) {
            try {
                fetch(`${base}/api/status`)
                    .then(response => {
                        if (response.ok) return base;
                    });
            } catch (e) {
                continue;
            }
        }
        return candidates[0];
    }
    
    /**
     * Make API request with error handling
     * @param {string} endpoint - API endpoint
     * @param {object} body - Request body
     * @returns {Promise<object>} Response data
     */
    async request(endpoint, body = {}) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-ID': this.sessionId
                },
                body: JSON.stringify(body)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    /**
     * Generate new composition
     * @param {object} params - Composition parameters
     * @returns {Promise<object>} Composition data
     */
    async compose(params) {
        return this.request('/api/compose', params);
    }
    
    /**
     * Apply automatic mixing
     * @param {object} data - Mix data
     * @returns {Promise<object>} Mix analysis
     */
    async autoMix(data) {
        return this.request('/api/auto-mix', data);
    }
    
    /**
     * Export composition to WAV
     * @param {object} composition - Composition to export
     * @returns {Promise<Blob>} WAV file blob
     */
    async exportWav(composition) {
        const response = await fetch(`${this.baseUrl}/api/export-wav`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ composition })
        });
        return response.blob();
    }
    
    /**
     * Send academy chat message
     * @param {string} text - User message
     * @param {object} state - Current coach state
     * @returns {Promise<object>} AI response
     */
    async academyChat(text, state) {
        return this.request('/api/academy/chat', { text, state });
    }
}

// Initialize API client
const api = new SonicForgeAPI();

// UI Event Handlers
async function generateProject() {
    const emotion = document.getElementById('emotion').value;
    const tempo = parseInt(document.getElementById('tempo').value);
    const key = document.getElementById('key').value;
    
    showLoading();
    
    try {
        const result = await api.compose({ emotion, tempo, key });
        renderProject(result.composition);
        renderMetrics(result.metrics);
        showSuccess('Composition generated!');
    } catch (error) {
        showError('Failed to generate composition');
    } finally {
        hideLoading();
    }
}

async function autoMix() {
    if (!currentProject) {
        showError('Generate a composition first');
        return;
    }
    
    showLoading();
    
    try {
        const result = await api.autoMix({ tracks: currentProject.tracks });
        renderMixAnalysis(result.analysis);
        currentProject.tracks = result.mixed_tracks;
        renderProject(currentProject);
        showSuccess('Mix optimized!');
    } catch (error) {
        showError('Failed to mix');
    } finally {
        hideLoading();
    }
}

async function downloadWav() {
    if (!currentProject) {
        showError('Generate a composition first');
        return;
    }
    
    showLoading();
    
    try {
        const blob = await api.exportWav(currentProject);
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentProject.title.replace(/\s+/g, '_')}.wav`;
        a.click();
        URL.revokeObjectURL(url);
        showSuccess('WAV exported!');
    } catch (error) {
        showError('Failed to export WAV');
    } finally {
        hideLoading();
    }
}

// UI Rendering Functions
function renderProject(composition) {
    const container = document.getElementById('project-container');
    container.innerHTML = '';
    
    // Render title
    const title = document.createElement('h2');
    title.textContent = composition.title;
    container.appendChild(title);
    
    // Render tracks
    composition.tracks.forEach(track => {
        const trackElement = createTrackElement(track);
        container.appendChild(trackElement);
    });
    
    // Store current project
    currentProject = composition;
}

function renderMetrics(metrics) {
    const container = document.getElementById('metrics-container');
    container.innerHTML = `
        <div class="metric">
            <span class="metric-label">Total Notes:</span>
            <span class="metric-value">${metrics.total_notes}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Tracks:</span>
            <span class="metric-value">${metrics.tracks_count}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Complexity:</span>
            <span class="metric-value">${(metrics.complexity_score * 100).toFixed(1)}%</span>
        </div>
    `;
}

function createTrackElement(track) {
    const div = document.createElement('div');
    div.className = 'track';
    div.innerHTML = `
        <div class="track-header">
            <span class="track-name">${track.name}</span>
            <span class="track-instrument">${track.instrument}</span>
        </div>
        <div class="track-notes">
            ${track.notes.map(note => `
                <div class="note" style="left: ${note.start_time * 50}px; width: ${note.duration * 50}px;">
                    ${note.pitch}
                </div>
            `).join('')}
        </div>
        <div class="track-controls">
            <input type="range" min="0" max="100" value="${track.volume * 100}" 
                   onchange="updateTrackVolume('${track.name}', this.value)">
            <input type="range" min="-100" max="100" value="${track.pan * 100}"
                   onchange="updateTrackPan('${track.name}', this.value)">
        </div>
    `;
    return div;
}

// State management
let currentProject = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('SonicForge Web Client initialized');
    api.discoverApiBase().then(base => {
        console.log('API Base:', base);
    });
});
```

#### 8.2.2 Harmonium Interface (harmonium.js)

```javascript
// sonicforge/web/harmonium.js

class HarmoniumPlayer {
    constructor() {
        this.audioContext = null;
        this.samples = {};
        this.currentNotes = [];
        this.dronePlaying = false;
        this.droneOscillators = [];
    }
    
    /**
     * Initialize audio context and load samples
     */
    async init() {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        await this.loadSamples();
    }
    
    /**
     * Load harmonium samples
     */
    async loadSamples() {
        const sampleFiles = {
            'C3': 'harmonium_c3.mp3',
            'F3': 'harmonium_f3.mp3',
            'G3': 'harmonium_g3.mp3',
            'C4': 'harmonium_c4.mp3',
            'F4': 'harmonium_f4.mp3',
            'A4': 'harmonium_a4.mp3',
            'C5': 'harmonium_c5.mp3'
        };
        
        for (const [note, file] of Object.entries(sampleFiles)) {
            try {
                const response = await fetch(file);
                const arrayBuffer = await response.arrayBuffer();
                const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
                this.samples[note] = audioBuffer;
            } catch (error) {
                console.error(`Failed to load sample ${note}:`, error);
            }
        }
    }
    
    /**
     * Play a harmonium note
     * @param {string} note - Note name (e.g., 'C4')
     * @param {number} duration - Duration in seconds
     */
    playNote(note, duration = 1.0) {
        if (!this.samples[note]) {
            console.warn(`Sample not found: ${note}`);
            return;
        }
        
        const source = this.audioContext.createBufferSource();
        source.buffer = this.samples[note];
        
        // Create gain node for envelope
        const gainNode = this.audioContext.createGain();
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(1, this.audioContext.currentTime + 0.05);
        gainNode.gain.setValueAtTime(1, this.audioContext.currentTime + duration - 0.1);
        gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + duration);
        
        // Connect nodes
        source.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        // Play
        source.start();
        source.stop(this.audioContext.currentTime + duration);
        
        this.currentNotes.push({ source, gainNode, note });
    }
    
    /**
     * Start drone (continuous note)
     * @param {string} note - Drone note
     */
    startDrone(note = 'C3') {
        if (this.dronePlaying) return;
        
        const frequency = this.noteToFrequency(note);
        
        // Create oscillators for rich harmonium drone sound
        const oscillators = [];
        const harmonics = [1, 2, 3, 4, 5];
        const volumes = [0.5, 0.3, 0.15, 0.1, 0.05];
        
        harmonics.forEach((harmonic, i) => {
            const osc = this.audioContext.createOscillator();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(frequency * harmonic, this.audioContext.currentTime);
            
            const gain = this.audioContext.createGain();
            gain.gain.setValueAtTime(0, this.audioContext.currentTime);
            gain.gain.linearRampToValueAtTime(volumes[i], this.audioContext.currentTime + 0.5);
            
            osc.connect(gain);
            gain.connect(this.audioContext.destination);
            osc.start();
            
            oscillators.push({ osc, gain });
        });
        
        this.droneOscillators = oscillators;
        this.dronePlaying = true;
    }
    
    /**
     * Stop drone
     */
    stopDrone() {
        this.droneOscillators.forEach(({ osc, gain }) => {
            gain.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 0.5);
            setTimeout(() => osc.stop(), 500);
        });
        this.droneOscillators = [];
        this.dronePlaying = false;
    }
    
    /**
     * Convert note name to frequency
     * @param {string} note - Note name (e.g., 'C4')
     * @returns {number} Frequency in Hz
     */
    noteToFrequency(note) {
        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const octave = parseInt(note.slice(-1));
        const noteName = note.slice(0, -1);
        const semitone = notes.indexOf(noteName);
        
        // A4 = 440Hz
        const a4 = 440;
        const a4_semitone = 9; // A is the 9th semitone (0-indexed)
        const a4_octave = 4;
        
        const semitonesFromA4 = (octave - a4_octave) * 12 + (semitone - a4_semitone);
        return a4 * Math.pow(2, semitonesFromA4 / 12);
    }
    
    /**
     * Play sargam sequence
     * @param {Array<string>} sargam - Array of note names
     * @param {number} tempo - Tempo in BPM
     */
    async playSargam(sargam, tempo = 120) {
        const beatDuration = 60 / tempo;
        
        for (const note of sargam) {
            this.playNote(note, beatDuration);
            await this.sleep(beatDuration * 1000);
        }
    }
    
    /**
     * Sleep utility
     * @param {number} ms - Milliseconds to sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize harmonium player
const harmonium = new HarmoniumPlayer();

// UI Event Handlers
document.addEventListener('DOMContentLoaded', async () => {
    await harmonium.init();
    console.log('Harmonium initialized');
    
    // Set up keyboard events for playing notes
    document.addEventListener('keydown', (e) => {
        const noteMap = {
            'a': 'C4', 's': 'D4', 'd': 'E4', 'f': 'F4',
            'g': 'G4', 'h': 'A4', 'j': 'B4', 'k': 'C5'
        };
        
        if (noteMap[e.key]) {
            harmonium.playNote(noteMap[e.key]);
        }
        
        if (e.key === ' ') {
            e.preventDefault();
            if (harmonium.dronePlaying) {
                harmonium.stopDrone();
            } else {
                harmonium.startDrone('C3');
            }
        }
    });
});

// Academy voice coach integration
class AcademyCoach {
    constructor() {
        this.state = {
            enabled: false,
            paused: false,
            current_section_index: 0,
            current_chunk_index: 0
        };
        this.conversationHistory = [];
    }
    
    /**
     * Send message to academy AI
     * @param {string} text - User message
     * @returns {Promise<object>} AI response
     */
    async sendMessage(text) {
        try {
            const response = await api.academyChat(text, this.state);
            
            if (response.success) {
                this.state = response.updated_state;
                this.conversationHistory.push({
                    role: 'user',
                    text: text
                });
                this.conversationHistory.push({
                    role: 'assistant',
                    text: response.decision.reply
                });
                
                return response.decision;
            }
        } catch (error) {
            console.error('Academy chat error:', error);
            return {
                action: 'error',
                reply: 'Sorry, I had trouble understanding. Please try again.'
            };
        }
    }
    
    /**
     * Start voice recognition
     */
    startVoiceInput() {
        if (!('webkitSpeechRecognition' in window)) {
            alert('Speech recognition not supported');
            return;
        }
        
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = async (event) => {
            const text = event.results[0][0].transcript;
            const response = await this.sendMessage(text);
            this.displayResponse(response);
        };
        
        recognition.start();
    }
    
    /**
     * Display AI response
     * @param {object} response - AI response object
     */
    displayResponse(response) {
        const chatContainer = document.getElementById('academy-chat');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant';
        messageDiv.innerHTML = `
            <div class="message-content">${response.reply}</div>
            <div class="message-action">${response.action}</div>
        `;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

const academyCoach = new AcademyCoach();
```

### 8.3 CSS Architecture

```css
/* sonicforge/web/styles.css */

:root {
    /* Color Palette */
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;
    --secondary-color: #10b981;
    --accent-color: #f59e0b;
    --danger-color: #ef4444;
    --warning-color: #f59e0b;
    --success-color: #10b981;
    
    /* Background Colors */
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --bg-card: #1e293b;
    
    /* Text Colors */
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Border Radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 1rem;
    --radius-full: 9999px;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
    --transition-slow: 500ms ease;
}

/* Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
}

/* Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-lg);
}

.grid {
    display: grid;
    gap: var(--spacing-lg);
}

.grid-2 {
    grid-template-columns: repeat(2, 1fr);
}

.grid-3 {
    grid-template-columns: repeat(3, 1fr);
}

/* Cards */
.card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-md);
    transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-sm) var(--spacing-lg);
    border: none;
    border-radius: var(--radius-md);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
}

.btn-secondary {
    background: var(--bg-tertiary);
    color: var(--text-primary);
}

.btn-secondary:hover {
    background: var(--bg-secondary);
}

/* Forms */
.form-group {
    margin-bottom: var(--spacing-md);
}

.form-label {
    display: block;
    margin-bottom: var(--spacing-xs);
    font-weight: 500;
    color: var(--text-secondary);
}

.form-input {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--bg-tertiary);
    border-radius: var(--radius-md);
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 1rem;
    transition: border-color var(--transition-fast);
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-color);
}

/* Track Display */
.track {
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
}

.track-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);
}

.track-name {
    font-weight: 600;
}

.track-instrument {
    color: var(--text-muted);
    font-size: 0.875rem;
}

.track-notes {
    position: relative;
    height: 40px;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    overflow: hidden;
}

.note {
    position: absolute;
    height: 100%;
    background: var(--primary-color);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    color: white;
}

/* Metrics */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-md);
}

.metric {
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    text-align: center;
}

.metric-label {
    display: block;
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: var(--spacing-xs);
}

.metric-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
}

/* Harmonium */
.harmonium {
    display: flex;
    gap: var(--spacing-xs);
    padding: var(--spacing-lg);
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
}

.harmonium-key {
    width: 60px;
    height: 200px;
    background: white;
    border-radius: 0 0 var(--radius-md) var(--radius-md);
    cursor: pointer;
    transition: background var(--transition-fast);
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding-bottom: var(--spacing-sm);
    font-weight: 600;
    color: var(--bg-primary);
}

.harmonium-key:hover {
    background: var(--primary-light);
    color: white;
}

.harmonium-key.black {
    width: 40px;
    height: 120px;
    background: var(--bg-primary);
    color: white;
    margin: 0 -20px;
    z-index: 1;
}

/* Loading & Alerts */
.loading {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 3px solid var(--bg-tertiary);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.alert {
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
}

.alert-success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid var(--success-color);
    color: var(--success-color);
}

.alert-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid var(--danger-color);
    color: var(--danger-color);
}

/* Responsive */
@media (max-width: 768px) {
    .grid-2, .grid-3 {
        grid-template-columns: 1fr;
    }
    
    .harmonium {
        flex-wrap: wrap;
        justify-content: center;
    }
}
```

---

## 9. Desktop Application Architecture

### 9.1 Tkinter GUI Structure

```python
# sonicforge/apps/desktop.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from typing import Optional

class SonicForgeDesktop(tk.Tk):
    """Main desktop application window"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("SonicForge X - AI Music Studio")
        self.geometry("1320x860")
        self.configure(bg="#0b1020")
        
        # State
        self.session = Session()
        self.composer = Composer(self.session)
        self.mixmaster = MixMaster()
        self.cocreator = Cocreator()
        self.current_composition: Optional[Composition] = None
        
        # Build UI
        self._build_style()
        self._build_layout()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _build_style(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#0b1020')
        style.configure('TLabel', background='#0b1020', foreground='#f1f5f9')
        style.configure('TButton', background='#6366f1', foreground='white')
        style.configure('TEntry', fieldbackground='#1e293b', foreground='#f1f5f9')
        style.configure('TCombobox', fieldbackground='#1e293b', foreground='#f1f5f9')
        
        # Custom styles
        style.configure('Header.TLabel', font=('Inter', 24, 'bold'))
        style.configure('Subheader.TLabel', font=('Inter', 16))
        style.configure('Metric.TLabel', font=('Inter', 12))
    
    def _build_layout(self):
        """Build complete UI layout"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="🎵 SonicForge X", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Control Panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self._build_control_panel(control_frame)
        
        # Content Area (PanedWindow)
        content_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel - Composition
        left_frame = ttk.Frame(content_frame)
        content_frame.add(left_frame, weight=2)
        self._build_composition_panel(left_frame)
        
        # Right Panel - Analysis & Suggestions
        right_frame = ttk.Frame(content_frame)
        content_frame.add(right_frame, weight=1)
        self._build_analysis_panel(right_frame)
        
        # Status Bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
    
    def _build_control_panel(self, parent):
        """Build composition control panel"""
        # Emotion selection
        ttk.Label(parent, text="Emotion:").grid(row=0, column=0, padx=5)
        self.emotion_var = tk.StringVar(value="happy")
        emotions = ["happy", "sad", "energetic", "calm", "mysterious", "romantic"]
        emotion_combo = ttk.Combobox(parent, textvariable=self.emotion_var, values=emotions, state='readonly')
        emotion_combo.grid(row=0, column=1, padx=5)
        
        # Tempo
        ttk.Label(parent, text="Tempo:").grid(row=0, column=2, padx=5)
        self.tempo_var = tk.IntVar(value=120)
        tempo_scale = ttk.Scale(parent, from_=40, to=200, variable=self.tempo_var, orient=tk.HORIZONTAL)
        tempo_scale.grid(row=0, column=3, padx=5)
        self.tempo_label = ttk.Label(parent, text="120 BPM")
        self.tempo_label.grid(row=0, column=4, padx=5)
        
        # Key
        ttk.Label(parent, text="Key:").grid(row=0, column=5, padx=5)
        self.key_var = tk.StringVar(value="C")
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        key_combo = ttk.Combobox(parent, textvariable=self.key_var, values=keys, state='readonly', width=5)
        key_combo.grid(row=0, column=6, padx=5)
        
        # Buttons
        ttk.Button(parent, text="Generate", command=self.generate_project).grid(row=0, column=7, padx=10)
        ttk.Button(parent, text="Auto Mix", command=self.auto_mix).grid(row=0, column=8, padx=5)
        ttk.Button(parent, text="Export WAV", command=self.export_wav).grid(row=0, column=9, padx=5)
        
        # Bind tempo slider
        tempo_scale.configure(command=self._update_tempo_label)
    
    def _build_composition_panel(self, parent):
        """Build composition display panel"""
        # Track list
        ttk.Label(parent, text="Tracks", style='Subheader.TLabel').pack(anchor=tk.W)
        
        # Canvas for track visualization
        self.tracks_canvas = tk.Canvas(parent, bg="#1e293b", height=400)
        self.tracks_canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tracks_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tracks_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Track details frame
        self.tracks_frame = ttk.Frame(self.tracks_canvas)
        self.tracks_canvas.create_window((0, 0), window=self.tracks_frame, anchor=tk.NW)
    
    def _build_analysis_panel(self, parent):
        """Build analysis and suggestions panel"""
        # Metrics
        ttk.Label(parent, text="Mix Analysis", style='Subheader.TLabel').pack(anchor=tk.W)
        
        metrics_frame = ttk.Frame(parent)
        metrics_frame.pack(fill=tk.X, pady=10)
        
        self.metrics_labels = {}
        metrics = ["Headroom", "Stereo Width", "Low-End Focus", "Dynamic Range"]
        for i, metric in enumerate(metrics):
            ttk.Label(metrics_frame, text=f"{metric}:").grid(row=i, column=0, sticky=tk.W, padx=5)
            self.metrics_labels[metric] = ttk.Label(metrics_frame, text="--")
            self.metrics_labels[metric].grid(row=i, column=1, sticky=tk.W, padx=5)
        
        # Suggestions
        ttk.Label(parent, text="AI Suggestions", style='Subheader.TLabel').pack(anchor=tk.W, pady=(20, 0))
        
        self.suggestions_listbox = tk.Listbox(parent, bg="#1e293b", fg="#f1f5f9", height=10)
        self.suggestions_listbox.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Button(parent, text="Apply Selected", command=self.apply_selected_suggestion).pack(anchor=tk.E)
    
    def _update_tempo_label(self, value):
        """Update tempo label when slider changes"""
        self.tempo_label.configure(text=f"{int(float(value))} BPM")
    
    def generate_project(self):
        """Generate new composition"""
        def generate():
            self.status_label.configure(text="Generating composition...")
            
            # Get parameters
            emotion = self.emotion_var.get()
            tempo = self.tempo_var.get()
            key = self.key_var.get()
            
            # Generate composition
            self.current_composition = self.composer.compose(emotion, tempo, key)
            
            # Update UI
            self.after(0, self._refresh_view)
            self.status_label.configure(text="Composition generated!")
        
        # Run in background thread
        threading.Thread(target=generate, daemon=True).start()
    
    def auto_mix(self):
        """Apply automatic mixing"""
        if not self.current_composition:
            messagebox.showwarning("Warning", "Generate a composition first!")
            return
        
        def mix():
            self.status_label.configure(text="Mixing...")
            
            # Analyze and mix
            analysis = self.mixmaster.analyze_mix(self.current_composition.tracks)
            self.current_composition.tracks = self.mixmaster.auto_mix(self.current_composition.tracks)
            suggestions = self.cocreator.generate_suggestions(analysis)
            
            # Update UI
            self.after(0, lambda: self._update_analysis(analysis, suggestions))
            self.status_label.configure(text="Mix complete!")
        
        threading.Thread(target=mix, daemon=True).start()
    
    def export_wav(self):
        """Export composition to WAV"""
        if not self.current_composition:
            messagebox.showwarning("Warning", "Generate a composition first!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if filepath:
            def export():
                self.status_label.configure(text="Exporting WAV...")
                
                # Generate WAV
                from sonicforge.core.audio_preview import generate_wav
                wav_data = generate_wav(self.current_composition)
                
                # Write file
                with open(filepath, 'wb') as f:
                    f.write(wav_data)
                
                self.status_label.configure(text=f"Exported to {filepath}")
            
            threading.Thread(target=export, daemon=True).start()
    
    def apply_selected_suggestion(self):
        """Apply selected AI suggestion"""
        selection = self.suggestions_listbox.curselection()
        if not selection:
            return
        
        # Apply suggestion logic
        suggestion_index = selection[0]
        # Implementation depends on suggestion structure
    
    def _refresh_view(self):
        """Refresh all UI elements"""
        if not self.current_composition:
            return
        
        # Clear tracks frame
        for widget in self.tracks_frame.winfo_children():
            widget.destroy()
        
        # Render each track
        for i, track in enumerate(self.current_composition.tracks):
            track_frame = ttk.Frame(self.tracks_frame)
            track_frame.pack(fill=tk.X, pady=5)
            
            # Track info
            ttk.Label(track_frame, text=track.name, width=15).pack(side=tk.LEFT)
            ttk.Label(track_frame, text=track.instrument, width=10).pack(side=tk.LEFT)
            
            # Volume slider
            vol_var = tk.DoubleVar(value=track.volume * 100)
            vol_scale = ttk.Scale(track_frame, from_=0, to=100, variable=vol_var, orient=tk.HORIZONTAL, length=100)
            vol_scale.pack(side=tk.LEFT, padx=10)
            
            # Pan slider
            pan_var = tk.DoubleVar(value=track.pan * 100)
            pan_scale = ttk.Scale(track_frame, from_=-100, to=100, variable=pan_var, orient=tk.HORIZONTAL, length=100)
            pan_scale.pack(side=tk.LEFT, padx=10)
        
        # Update canvas scroll region
        self.tracks_frame.update_idletasks()
        self.tracks_canvas.configure(scrollregion=self.tracks_canvas.bbox(tk.ALL))
    
    def _update_analysis(self, analysis, suggestions):
        """Update analysis panel with new data"""
        # Update metrics
        metrics = analysis.metrics
        self.metrics_labels["Headroom"].configure(text=f"{metrics.get('headroom', 0):.1f} dB")
        self.metrics_labels["Stereo Width"].configure(text=f"{metrics.get('stereo_width', 0):.2f}")
        self.metrics_labels["Low-End Focus"].configure(text=f"{metrics.get('low_end_focus', 0):.2f}")
        self.metrics_labels["Dynamic Range"].configure(text=f"{metrics.get('dynamic_range', 0):.1f} dB")
        
        # Update suggestions
        self.suggestions_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.suggestions_listbox.insert(tk.END, suggestion.description)
    
    def _start_background_tasks(self):
        """Start background processing tasks"""
        # Could start periodic updates, audio preview, etc.
        pass

def main():
    """Main entry point for desktop application"""
    app = SonicForgeDesktop()
    app.mainloop()

if __name__ == "__main__":
    main()
```

### 9.2 Desktop Application Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DESKTOP APPLICATION FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Application Startup                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│               Initialize Components                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Session   │  │   Composer  │  │  MixMaster  │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Build UI Components                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Controls   │  │   Tracks    │  │  Analysis   │            │
│  │   Panel     │  │   Display   │  │   Panel     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Event Loop Running                             │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Generate  │         │   Auto Mix  │         │   Export    │
│   Button    │         │   Button    │         │   Button    │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ Background  │         │ Background  │         │ Background  │
│   Thread    │         │   Thread    │         │   Thread    │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Composer   │         │  MixMaster  │         │  WAV Gen    │
│  .compose() │         │  .analyze() │         │  .render()  │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ Update UI   │         │ Update UI   │         │ Save File   │
│ (mainloop)  │         │ (mainloop)  │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## 10. AI & Machine Learning Components

### 10.1 Speech-to-Text Integration

```python
# sonicforge/core/academy_stt.py

from faster_whisper import WhisperModel
import numpy as np
from typing import Optional
import io
import wave

class SpeechToText:
    """Speech-to-text using faster-whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize STT model
        
        Args:
            model_size: Model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.supported_languages = ['en', 'hi', 'es', 'fr', 'de', 'ja', 'zh']
    
    def transcribe_audio(self, audio_data: bytes, language: str = "en") -> str:
        """
        Transcribe audio data to text
        
        Args:
            audio_data: WAV audio bytes
            language: Language code
            
        Returns:
            Transcribed text
        """
        try:
            # Convert bytes to numpy array
            audio_np = self._bytes_to_numpy(audio_data)
            
            # Transcribe
            segments, info = self.model.transcribe(
                audio_np,
                language=language,
                beam_size=5,
                vad_filter=True
            )
            
            # Combine segments
            text = " ".join([segment.text for segment in segments])
            return text.strip()
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
    
    def _bytes_to_numpy(self, audio_data: bytes) -> np.ndarray:
        """Convert WAV bytes to numpy array"""
        with io.BytesIO(audio_data) as wav_io:
            with wave.open(wav_io, 'rb') as wav_file:
                # Get audio parameters
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                
                # Read audio data
                audio_bytes = wav_file.readframes(n_frames)
                
                # Convert to numpy array
                if sample_width == 2:  # 16-bit
                    dtype = np.int16
                elif sample_width == 4:  # 32-bit
                    dtype = np.int32
                else:
                    dtype = np.int8
                
                audio_np = np.frombuffer(audio_bytes, dtype=dtype)
                
                # Convert to float32 and normalize
                audio_np = audio_np.astype(np.float32) / np.iinfo(dtype).max
                
                # Convert stereo to mono if needed
                if n_channels == 2:
                    audio_np = audio_np.reshape(-1, 2).mean(axis=1)
                
                return audio_np
    
    def transcribe_file(self, filepath: str, language: str = "en") -> str:
        """
        Transcribe audio file
        
        Args:
            filepath: Path to audio file
            language: Language code
            
        Returns:
            Transcribed text
        """
        with open(filepath, 'rb') as f:
            audio_data = f.read()
        return self.transcribe_audio(audio_data, language)
    
    def detect_language(self, audio_data: bytes) -> str:
        """
        Detect language of audio
        
        Args:
            audio_data: WAV audio bytes
            
        Returns:
            Detected language code
        """
        audio_np = self._bytes_to_numpy(audio_data)
        
        # Use first 30 seconds for detection
        audio_sample = audio_np[:30 * 16000]  # Assuming 16kHz
        
        _, info = self.model.transcribe(audio_sample, beam_size=5)
        return info.language
```

### 10.2 Text-to-Speech Integration

```python
# sonicforge/core/academy_tts.py

import edge_tts
import asyncio
from typing import Optional
import io

class TextToSpeech:
    """Text-to-speech using edge-tts"""
    
    def __init__(self):
        """Initialize TTS engine"""
        self.voices = {
            'en': {
                'male': 'en-US-GuyNeural',
                'female': 'en-US-JennyNeural'
            },
            'hi': {
                'male': 'hi-IN-MadhurNeural',
                'female': 'hi-IN-SwaraNeural'
            }
        }
        self.default_voice = 'en-US-JennyNeural'
    
    async def synthesize_speech(self, text: str, voice: Optional[str] = None,
                                 rate: str = "+0%", pitch: str = "+0Hz") -> bytes:
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            voice: Voice name
            rate: Speech rate adjustment
            pitch: Pitch adjustment
            
        Returns:
            Audio bytes (MP3 format)
        """
        if voice is None:
            voice = self.default_voice
        
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
    
    def synthesize_speech_sync(self, text: str, voice: Optional[str] = None) -> bytes:
        """Synchronous wrapper for synthesize_speech"""
        return asyncio.run(self.synthesize_speech(text, voice))
    
    def get_voice_for_language(self, language: str, gender: str = "female") -> str:
        """
        Get voice name for language and gender
        
        Args:
            language: Language code
            gender: 'male' or 'female'
            
        Returns:
            Voice name
        """
        lang_voices = self.voices.get(language, self.voices['en'])
        return lang_voices.get(gender, lang_voices['female'])
    
    async def save_to_file(self, text: str, filepath: str, voice: Optional[str] = None):
        """
        Synthesize and save to file
        
        Args:
            text: Text to synthesize
            filepath: Output file path
            voice: Voice name
        """
        if voice is None:
            voice = self.default_voice
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
    
    def list_available_voices(self) -> dict:
        """Get list of available voices"""
        return self.voices
```

### 10.3 AI Decision Making

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AI DECISION MAKING FLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

User Input                    AI Processing                     Output
    │                              │                              │
    ▼                              ▼                              ▼
┌─────────┐                  ┌───────────┐                  ┌─────────┐
│ Voice   │─────────────────▶│    STT    │─────────────────▶│  Text   │
│ Audio   │                  │ (Whisper) │                  │         │
└─────────┘                  └───────────┘                  └─────────┘
                                                               │
                                                               ▼
                                                         ┌───────────┐
                                                         │ NLP       │
                                                         │ Processing│
                                                         └─────┬─────┘
                                                               │
         ┌─────────────────────────────────────────────────────┼─────────────────────┐
         │                                                     │                     │
         ▼                                                     ▼                     ▼
┌─────────────────┐                                ┌─────────────────┐      ┌─────────────────┐
│ Intent          │                                │ Context         │      │ Knowledge       │
│ Classification  │                                │ Analysis        │      │ Retrieval       │
└────────┬────────┘                                └────────┬────────┘      └────────┬────────┘
         │                                                  │                      │
         ▼                                                  ▼                      ▼
┌─────────────────┐                                ┌─────────────────┐      ┌─────────────────┐
│ Action          │                                │ State           │      │ Content         │
│ Selection       │                                │ Management      │      │ Generation      │
└────────┬────────┘                                └────────┬────────┘      └────────┬────────┘
         │                                                  │                      │
         └───────────────────────────────────────────────────┼──────────────────────┘
                                                             │
                                                             ▼
                                                      ┌───────────┐
                                                      │ Decision  │
                                                      │ Builder   │
                                                      └─────┬─────┘
                                                            │
                                                            ▼
                                                      ┌───────────┐
                                                      │   TTS     │
                                                      │ (edge-tts)│
                                                      └─────┬─────┘
                                                            │
                                                            ▼
                                                      ┌─────────┐
                                                      │ Voice   │
                                                      │ Output  │
                                                      └─────────┘
```

---

## 11. Audio Processing Pipeline

### 11.1 WAV Generation Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      WAV GENERATION PIPELINE                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐
│ Composition │
│   Object    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Track Processing                             │
├─────────────────────────────────────────────────────────────────┤
│  FOR each track:                                                │
│    ┌─────────────┐                                             │
│    │   Notes     │                                             │
│    │   List      │                                             │
│    └──────┬──────┘                                             │
│           │                                                     │
│           ▼                                                     │
│    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│    │  Frequency  │────▶│  Waveform   │────▶│  Envelope   │    │
│    │ Calculation │     │ Generation  │     │ Application │    │
│    └─────────────┘     └─────────────┘     └─────────────┘    │
│           │                                                     │
│           ▼                                                     │
│    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│    │   Volume    │────▶│     Pan     │────▶│   Effects   │    │
│    │  Scaling    │     │   Stereo    │     │   Chain     │    │
│    └─────────────┘     └─────────────┘     └─────────────┘    │
│           │                                                     │
│           ▼                                                     │
│    ┌─────────────┐                                             │
│    │   Track     │                                             │
│    │   Buffer    │                                             │
│    └─────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Master Processing                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Track     │────▶│  Summing    │────▶│  Normalization│     │
│  │   Mixing    │     │   Bus       │     │              │     │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                               │                                │
│                               ▼                                │
│                        ┌─────────────┐                        │
│                        │   Master    │                        │
│                        │   Buffer    │                        │
│                        └─────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WAV Encoding                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Header    │────▶│  PCM Data   │────▶│   File      │      │
│  │   Writing   │     │  Encoding   │     │   Output    │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  WAV File   │
│   Bytes     │
└─────────────┘
```

### 11.2 Audio Effects Chain

```python
# sonicforge/core/audio_effects.py

import numpy as np
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class AudioEffect:
    """Audio effect parameters"""
    name: str
    parameters: Dict[str, float]
    enabled: bool = True

class EffectsChain:
    """Audio effects processing chain"""
    
    def __init__(self):
        self.effects: List[AudioEffect] = []
    
    def add_effect(self, effect: AudioEffect):
        """Add effect to chain"""
        self.effects.append(effect)
    
    def process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Process audio through effects chain"""
        output = audio.copy()
        
        for effect in self.effects:
            if not effect.enabled:
                continue
            
            if effect.name == "reverb":
                output = self._apply_reverb(output, effect.parameters, sample_rate)
            elif effect.name == "delay":
                output = self._apply_delay(output, effect.parameters, sample_rate)
            elif effect.name == "eq":
                output = self._apply_eq(output, effect.parameters, sample_rate)
            elif effect.name == "compressor":
                output = self._apply_compressor(output, effect.parameters, sample_rate)
            elif effect.name == "distortion":
                output = self._apply_distortion(output, effect.parameters)
        
        return output
    
    def _apply_reverb(self, audio: np.ndarray, params: Dict, sample_rate: int) -> np.ndarray:
        """Apply reverb effect"""
        # Simple convolution reverb
        decay = params.get("decay", 0.5)
        wet = params.get("wet", 0.3)
        
        # Create impulse response
        ir_length = int(sample_rate * decay)
        impulse = np.random.randn(ir_length) * np.exp(-np.linspace(0, 5, ir_length))
        
        # Convolve
        output = np.convolve(audio, impulse, mode='full')[:len(audio)]
        
        # Mix dry and wet
        return audio * (1 - wet) + output * wet
    
    def _apply_delay(self, audio: np.ndarray, params: Dict, sample_rate: int) -> np.ndarray:
        """Apply delay effect"""
        delay_time = params.get("delay_time", 0.3)  # seconds
        feedback = params.get("feedback", 0.4)
        wet = params.get("wet", 0.5)
        
        delay_samples = int(delay_time * sample_rate)
        output = audio.copy()
        
        # Add delayed copies
        for i in range(1, 4):  # 3 echoes
            delayed = np.zeros_like(audio)
            offset = delay_samples * i
            if offset < len(audio):
                delayed[offset:] = audio[:len(audio) - offset] * (feedback ** i)
                output += delayed * wet
        
        return output
    
    def _apply_eq(self, audio: np.ndarray, params: Dict, sample_rate: int) -> np.ndarray:
        """Apply equalizer"""
        # Simple 3-band EQ using FFT
        low_gain = params.get("low", 1.0)
        mid_gain = params.get("mid", 1.0)
        high_gain = params.get("high", 1.0)
        
        # FFT
        fft = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), 1/sample_rate)
        
        # Apply gains
        low_mask = freqs < 300
        mid_mask = (freqs >= 300) & (freqs < 3000)
        high_mask = freqs >= 3000
        
        fft[low_mask] *= low_gain
        fft[mid_mask] *= mid_gain
        fft[high_mask] *= high_gain
        
        # Inverse FFT
        return np.fft.irfft(fft, n=len(audio))
    
    def _apply_compressor(self, audio: np.ndarray, params: Dict, sample_rate: int) -> np.ndarray:
        """Apply dynamic range compression"""
        threshold = params.get("threshold", -20)  # dB
        ratio = params.get("ratio", 4.0)
        attack = params.get("attack", 0.01)  # seconds
        release = params.get("release", 0.1)  # seconds
        
        # Convert to dB
        audio_db = 20 * np.log10(np.abs(audio) + 1e-10)
        
        # Calculate gain reduction
        gain_reduction = np.zeros_like(audio_db)
        above_threshold = audio_db > threshold
        gain_reduction[above_threshold] = (audio_db[above_threshold] - threshold) * (1 - 1/ratio)
        
        # Apply attack/release smoothing
        attack_samples = int(attack * sample_rate)
        release_samples = int(release * sample_rate)
        
        # Simple smoothing (in practice, use proper envelope follower)
        smoothed = np.convolve(gain_reduction, np.ones(attack_samples)/attack_samples, mode='same')
        
        # Apply gain reduction
        gain = 10 ** (-smoothed / 20)
        return audio * gain
    
    def _apply_distortion(self, audio: np.ndarray, params: Dict) -> np.ndarray:
        """Apply distortion effect"""
        drive = params.get("drive", 2.0)
        mix = params.get("mix", 0.5)
        
        # Soft clipping
        distorted = np.tanh(audio * drive)
        
        # Mix
        return audio * (1 - mix) + distorted * mix
```

---

## 12. Communication Protocols

### 12.1 Internal Message Passing

```python
# sonicforge/core/message_bus.py

from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import threading
import queue

class MessageType(Enum):
    """Message types for internal communication"""
    COMPOSITION_REQUEST = "composition_request"
    COMPOSITION_COMPLETE = "composition_complete"
    MIX_REQUEST = "mix_request"
    MIX_COMPLETE = "mix_complete"
    EXPORT_REQUEST = "export_request"
    EXPORT_COMPLETE = "export_complete"
    STATE_UPDATE = "state_update"
    ERROR = "error"

@dataclass
class Message:
    """Internal message structure"""
    type: MessageType
    data: Dict[str, Any]
    source: str
    timestamp: float

class MessageBus:
    """Internal message bus for component communication"""
    
    def __init__(self):
        self.subscribers: Dict[MessageType, List[Callable]] = {}
        self.message_queue = queue.Queue()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start message processing thread"""
        self.running = True
        self.thread = threading.Thread(target=self._process_messages, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop message processing"""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def subscribe(self, message_type: MessageType, callback: Callable):
        """
        Subscribe to message type
        
        Args:
            message_type: Type of message to subscribe to
            callback: Function to call when message is received
        """
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        self.subscribers[message_type].append(callback)
    
    def publish(self, message: Message):
        """
        Publish message to bus
        
        Args:
            message: Message to publish
        """
        self.message_queue.put(message)
    
    def _process_messages(self):
        """Process messages from queue"""
        while self.running:
            try:
                message = self.message_queue.get(timeout=0.1)
                self._dispatch_message(message)
            except queue.Empty:
                continue
    
    def _dispatch_message(self, message: Message):
        """
        Dispatch message to subscribers
        
        Args:
            message: Message to dispatch
        """
        if message.type in self.subscribers:
            for callback in self.subscribers[message.type]:
                try:
                    callback(message)
                except Exception as e:
                    print(f"Error in message handler: {e}")

# Global message bus instance
message_bus = MessageBus()
```

### 12.2 WebSocket Communication (Future)

```python
# sonicforge/apps/websocket_server.py (Future Implementation)

import asyncio
import websockets
import json
from typing import Set

class WebSocketServer:
    """WebSocket server for real-time communication"""
    
    def __init__(self, host: str = "localhost", port: int = 8001):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
    
    async def handler(self, websocket, path):
        """Handle WebSocket connection"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        finally:
            self.clients.remove(websocket)
    
    async def process_message(self, websocket, message: str):
        """Process incoming message"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "compose":
                # Handle composition request
                response = await self.handle_compose(data)
                await websocket.send(json.dumps(response))
            
            elif message_type == "mix":
                # Handle mix request
                response = await self.handle_mix(data)
                await websocket.send(json.dumps(response))
            
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"error": "Invalid JSON"}))
    
    async def broadcast(self, message: dict):
        """Broadcast message to all clients"""
        if self.clients:
            message_str = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_str) for client in self.clients]
            )
    
    async def start(self):
        """Start WebSocket server"""
        server = await websockets.serve(self.handler, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        await server.wait_closed()
```

---

## 13. State Management

### 13.1 Session State Architecture

```python
# sonicforge/core/session.py

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time
import json
from pathlib import Path

@dataclass
class SessionState:
    """Application session state"""
    session_id: str
    created_at: float
    last_updated: float
    current_composition: Optional[Dict] = None
    history: List[Dict] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    undo_stack: List[Dict] = field(default_factory=list)
    redo_stack: List[Dict] = field(default_factory=list)

class Session:
    """Session manager for state persistence"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.state = SessionState(
            session_id=session_id or self._generate_session_id(),
            created_at=time.time(),
            last_updated=time.time()
        )
        self.state_file = Path(f".sonicforge/session_{self.state.session_id}.json")
        self.state_file.parent.mkdir(exist_ok=True)
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def save_state(self):
        """Save current state to file"""
        self.state.last_updated = time.time()
        
        state_dict = {
            "session_id": self.state.session_id,
            "created_at": self.state.created_at,
            "last_updated": self.state.last_updated,
            "current_composition": self.state.current_composition,
            "history": self.state.history,
            "preferences": self.state.preferences
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state_dict, f, indent=2)
    
    def load_state(self) -> bool:
        """Load state from file"""
        if not self.state_file.exists():
            return False
        
        try:
            with open(self.state_file, 'r') as f:
                state_dict = json.load(f)
            
            self.state.session_id = state_dict["session_id"]
            self.state.created_at = state_dict["created_at"]
            self.state.last_updated = state_dict["last_updated"]
            self.state.current_composition = state_dict.get("current_composition")
            self.state.history = state_dict.get("history", [])
            self.state.preferences = state_dict.get("preferences", {})
            
            return True
        except Exception as e:
            print(f"Error loading state: {e}")
            return False
    
    def push_undo(self, state_snapshot: Dict):
        """Push state to undo stack"""
        self.state.undo_stack.append(state_snapshot)
        self.state.redo_stack.clear()  # Clear redo stack on new action
        
        # Limit undo stack size
        if len(self.state.undo_stack) > 50:
            self.state.undo_stack.pop(0)
    
    def undo(self) -> Optional[Dict]:
        """Undo last action"""
        if not self.state.undo_stack:
            return None
        
        # Save current state to redo stack
        current_snapshot = self._create_snapshot()
        self.state.redo_stack.append(current_snapshot)
        
        # Restore previous state
        return self.state.undo_stack.pop()
    
    def redo(self) -> Optional[Dict]:
        """Redo last undone action"""
        if not self.state.redo_stack:
            return None
        
        # Save current state to undo stack
        current_snapshot = self._create_snapshot()
        self.state.undo_stack.append(current_snapshot)
        
        # Restore redo state
        return self.state.redo_stack.pop()
    
    def _create_snapshot(self) -> Dict:
        """Create state snapshot for undo/redo"""
        return {
            "timestamp": time.time(),
            "composition": self.state.current_composition,
            "preferences": self.state.preferences.copy()
        }
    
    def log_event(self, event_type: str, data: Dict):
        """Log event to history"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        }
        self.state.history.append(event)
        
        # Limit history size
        if len(self.state.history) > 1000:
            self.state.history.pop(0)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get preference value"""
        return self.state.preferences.get(key, default)
    
    def set_preference(self, key: str, value: Any):
        """Set preference value"""
        self.state.preferences[key] = value
        self.save_state()
    
    def clear_history(self):
        """Clear event history"""
        self.state.history.clear()
        self.save_state()
```

### 13.2 State Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STATE FLOW DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   User Action   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     State Manager                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Current   │────▶│    Undo     │────▶│    Redo     │      │
│  │   State     │     │   Stack     │     │   Stack     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Event     │────▶│   History   │────▶│  Preferences│      │
│  │   Logger    │     │   Log       │     │   Store     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Persistence Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Session   │────▶│    State    │────▶│   Backup    │      │
│  │   File      │     │   JSON      │     │   Files     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 14. Testing Strategy

### 14.1 Test Structure

```
tests/
├── __init__.py
├── test_core.py          # Core module tests
├── test_academy_ai.py    # Academy AI tests
├── test_academy_stt.py   # STT tests
└── test_composer.py      # Composer tests
```

### 14.2 Unit Test Examples

```python
# tests/test_composer.py

import unittest
from sonicforge.core.composer import Composer
from sonicforge.core.session import Session
from sonicforge.core.models import Composition, Note, Track

class TestComposer(unittest.TestCase):
    """Test cases for Composer module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.session = Session()
        self.composer = Composer(self.session)
    
    def test_compose_happy_emotion(self):
        """Test composition with happy emotion"""
        composition = self.composer.compose("happy", 120, "C")
        
        self.assertIsInstance(composition, Composition)
        self.assertEqual(composition.key, "C")
        self.assertEqual(composition.tempo, 120)
        self.assertGreater(len(composition.tracks), 0)
    
    def test_compose_sad_emotion(self):
        """Test composition with sad emotion"""
        composition = self.composer.compose("sad", 70, "Am")
        
        self.assertIsInstance(composition, Composition)
        self.assertEqual(composition.key, "Am")
        self.assertEqual(composition.tempo, 70)
    
    def test_note_properties(self):
        """Test Note dataclass properties"""
        note = Note(pitch=60, velocity=100, start_time=0.0, duration=1.0)
        
        self.assertEqual(note.pitch, 60)
        self.assertEqual(note.note_name, "C")
        self.assertAlmostEqual(note.frequency, 261.63, places=2)
    
    def test_track_duration(self):
        """Test Track duration calculation"""
        notes = [
            Note(pitch=60, velocity=100, start_time=0.0, duration=1.0),
            Note(pitch=64, velocity=100, start_time=1.0, duration=2.0),
            Note(pitch=67, velocity=100, start_time=3.0, duration=1.0)
        ]
        
        track = Track(name="Test", instrument="piano", notes=notes)
        self.assertEqual(track.total_duration, 4.0)
    
    def test_composition_duration(self):
        """Test Composition duration calculation"""
        composition = self.composer.compose("happy", 120, "C")
        duration = composition.duration_seconds
        
        self.assertGreater(duration, 0)
        self.assertIsInstance(duration, float)

class TestMixMaster(unittest.TestCase):
    """Test cases for MixMaster module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mixmaster = MixMaster()
    
    def test_analyze_mix(self):
        """Test mix analysis"""
        # Create test tracks
        tracks = [
            Track(name="Melody", instrument="piano", notes=[], volume=0.8),
            Track(name="Bass", instrument="bass", notes=[], volume=0.9)
        ]
        
        analysis = self.mixmaster.analyze_mix(tracks)
        
        self.assertIsNotNone(analysis)
        self.assertIn("headroom", analysis.metrics)
        self.assertIn("stereo_width", analysis.metrics)

class TestAcademyAI(unittest.TestCase):
    """Test cases for Academy AI module"""
    
    def setUp(self):
        """Set up test fixtures"""
        from sonicforge.core.academy_ai import AcademyAI
        self.ai = AcademyAI()
    
    def test_greeting(self):
        """Test greeting response"""
        state = AcademyCoachState()
        decision = self.ai.process_utterance("hello", state)
        
        self.assertEqual(decision.action, "answer")
        self.assertIn("hello", decision.reply.lower())
    
    def test_pause_command(self):
        """Test pause command"""
        state = AcademyCoachState()
        decision = self.ai.process_utterance("pause", state)
        
        self.assertEqual(decision.action, "pause")
        self.assertTrue(state.paused)

if __name__ == "__main__":
    unittest.main()
```

### 14.3 Test Execution

```bash
# Run all tests
python3 -m unittest discover -s tests

# Run specific test file
python3 -m unittest tests.test_composer

# Run with verbose output
python3 -m unittest discover -s tests -v

# Run specific test case
python3 -m unittest tests.test_composer.TestComposer.test_compose_happy_emotion
```

---

## 15. Deployment Architecture

### 15.1 Local Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LOCAL DEPLOYMENT ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     User's Machine                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Python Runtime                         │   │
│  │                 (Python 3.8+)                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────┼────────────────────────┐           │
│  │                        │                        │           │
│  ▼                        ▼                        ▼           │
│ ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  Desktop    │     │    Web      │     │   Tests     │       │
│  │  (Tkinter)  │     │  (HTTP)     │     │ (unittest)  │       │
│  └──────┬──────┘     └──────┬──────┘     └─────────────┘       │
│         │                   │                                   │
│         │                   │                                   │
│         ▼                   ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Core Engine                           │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │   │
│  │  │Composer │ │MixMaster│ │Cocreator│ │ SoundDNA│      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Storage                                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Session   │  │   WAV Files │  │   Samples   │     │   │
│  │  │   State     │  │   Cache     │  │   Library   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 15.2 Master Run Script

```python
# run_sonicforge.py

#!/usr/bin/env python3
"""
SonicForge X Master Launcher
Automatically selects Python, manages virtual environment, and starts applications.
"""

import os
import sys
import subprocess
import argparse
import signal
import time
from pathlib import Path

class SonicForgeLauncher:
    """Master launcher for SonicForge X"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / ".venv"
        self.processes = []
        
    def find_python(self) -> str:
        """Find suitable Python interpreter"""
        candidates = [
            "python3.11",
            "python3.10",
            "python3.9",
            "python3.8",
            "python3",
            "python"
        ]
        
        for candidate in candidates:
            try:
                result = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    if "Python 3" in version:
                        return candidate
            except FileNotFoundError:
                continue
        
        raise RuntimeError("No suitable Python 3 interpreter found")
    
    def setup_virtualenv(self, python: str):
        """Set up virtual environment"""
        if not self.venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run([python, "-m", "venv", str(self.venv_path)], check=True)
        
        # Get venv Python path
        if sys.platform == "win32":
            venv_python = self.venv_path / "Scripts" / "python.exe"
        else:
            venv_python = self.venv_path / "bin" / "python"
        
        return str(venv_python)
    
    def install_dependencies(self, python: str):
        """Install dependencies"""
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            print("Installing dependencies...")
            subprocess.run(
                [python, "-m", "pip", "install", "-r", str(requirements_file)],
                check=True
            )
    
    def run_tests(self, python: str) -> bool:
        """Run test suite"""
        print("Running tests...")
        result = subprocess.run(
            [python, "-m", "unittest", "discover", "-s", "tests"],
            cwd=str(self.project_root)
        )
        return result.returncode == 0
    
    def kill_existing_processes(self):
        """Kill existing SonicForge processes"""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["pkill", "-f", "sonicforge"], capture_output=True)
            elif sys.platform == "linux":
                subprocess.run(["pkill", "-f", "sonicforge"], capture_output=True)
            time.sleep(1)
        except Exception:
            pass
    
    def start_web_server(self, python: str):
        """Start web server"""
        print("Starting web server...")
        process = subprocess.Popen(
            [python, "-m", "sonicforge.apps.server"],
            cwd=str(self.project_root)
        )
        self.processes.append(process)
        print(f"Web server started (PID: {process.pid})")
        print("Open http://127.0.0.1:8000 in your browser")
    
    def start_desktop_app(self, python: str):
        """Start desktop application"""
        print("Starting desktop app...")
        process = subprocess.Popen(
            [python, "-m", "sonicforge.apps.desktop"],
            cwd=str(self.project_root)
        )
        self.processes.append(process)
        print(f"Desktop app started (PID: {process.pid})")
    
    def cleanup(self):
        """Clean up processes on exit"""
        print("\nShutting down...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("Goodbye!")
    
    def run(self, mode: str = "web", skip_tests: bool = False):
        """Main run method"""
        try:
            # Set up signal handler
            signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
            
            # Find Python
            python = self.find_python()
            print(f"Using Python: {python}")
            
            # Set up virtual environment
            venv_python = self.setup_virtualenv(python)
            
            # Install dependencies
            self.install_dependencies(venv_python)
            
            # Run tests
            if not skip_tests:
                if not self.run_tests(venv_python):
                    print("Tests failed! Aborting.")
                    return
            
            # Kill existing processes
            self.kill_existing_processes()
            
            # Start applications
            if mode in ["web", "both"]:
                self.start_web_server(venv_python)
            
            if mode in ["desktop", "both"]:
                self.start_desktop_app(venv_python)
            
            # Wait for processes
            print("\nSonicForge X is running. Press Ctrl+C to stop.")
            for process in self.processes:
                process.wait()
                
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="SonicForge X Launcher")
    parser.add_argument(
        "--mode",
        choices=["web", "desktop", "both"],
        default="web",
        help="Application mode to start"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip test suite"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check environment, don't start"
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Only clean up processes"
    )
    
    args = parser.parse_args()
    launcher = SonicForgeLauncher()
    
    if args.clean_only:
        launcher.kill_existing_processes()
        return
    
    if args.check_only:
        python = launcher.find_python()
        print(f"Python: {python}")
        print("Environment OK")
        return
    
    launcher.run(mode=args.mode, skip_tests=args.skip_tests)

if __name__ == "__main__":
    main()
```

---

## 16. Performance Optimization

### 16.1 Optimization Strategies

| Strategy | Implementation | Impact |
|----------|----------------|--------|
| **Caching** | Cache composed results, WAV files | High |
| **Lazy Loading** | Load samples on demand | Medium |
| **Batch Processing** | Process notes in batches | Medium |
| **Memory Pooling** | Reuse audio buffers | Medium |
| **Async Processing** | Non-blocking I/O operations | High |
| **Code Profiling** | Identify bottlenecks | - |

### 16.2 Caching Implementation

```python
# sonicforge/core/cache.py

import hashlib
import pickle
from pathlib import Path
from typing import Any, Optional
from functools import wraps
import time

class Cache:
    """Simple file-based cache"""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        data = pickle.dumps((args, kwargs))
        return hashlib.md5(data).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        cache_file = self.cache_dir / f"{key}.pkl"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
            
            # Check expiration
            if data.get('expires_at', 0) < time.time():
                cache_file.unlink()
                return None
            
            return data['value']
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache"""
        cache_file = self.cache_dir / f"{key}.pkl"
        
        data = {
            'value': value,
            'expires_at': time.time() + ttl
        }
        
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)
    
    def delete(self, key: str):
        """Delete value from cache"""
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            cache_file.unlink()
    
    def clear(self):
        """Clear all cache"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()

def cached(ttl: int = 3600):
    """Decorator for caching function results"""
    cache = Cache()
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}_{cache._generate_key(*args, **kwargs)}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Usage example
@cached(ttl=1800)
def compose(emotion: str, tempo: int, key: str) -> dict:
    """Cached composition function"""
    # Expensive composition logic
    pass
```

---

## 17. Security Considerations

### 17.1 Security Measures

| Area | Measure | Implementation |
|------|---------|----------------|
| **Input Validation** | Validate all user inputs | Pydantic, type hints |
| **File Access** | Restrict file operations | Path validation |
| **Network** | Local-only server | Bind to 127.0.0.1 |
| **Dependencies** | Minimal dependencies | Built-in modules |
| **Error Handling** | No sensitive info in errors | Generic messages |

### 17.2 Input Validation

```python
# sonicforge/core/validators.py

from typing import Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Validation result"""
    valid: bool
    errors: list
    warnings: list

class CompositionValidator:
    """Validate composition parameters"""
    
    VALID_EMOTIONS = ["happy", "sad", "energetic", "calm", "mysterious", "romantic"]
    VALID_KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
                  "Am", "A#m", "Bm", "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m"]
    TEMPO_RANGE = (40, 200)
    
    @classmethod
    def validate_composition_params(cls, emotion: str, tempo: int, key: str) -> ValidationResult:
        """
        Validate composition parameters
        
        Args:
            emotion: Emotion type
            tempo: Tempo in BPM
            key: Musical key
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        # Validate emotion
        if emotion not in cls.VALID_EMOTIONS:
            errors.append(f"Invalid emotion: {emotion}. Must be one of {cls.VALID_EMOTIONS}")
        
        # Validate tempo
        if not isinstance(tempo, int):
            errors.append(f"Tempo must be an integer, got {type(tempo)}")
        elif tempo < cls.TEMPO_RANGE[0] or tempo > cls.TEMPO_RANGE[1]:
            errors.append(f"Tempo must be between {cls.TEMPO_RANGE[0]} and {cls.TEMPO_RANGE[1]}")
        
        # Validate key
        if key not in cls.VALID_KEYS:
            errors.append(f"Invalid key: {key}. Must be one of {cls.VALID_KEYS}")
        
        # Warnings
        if tempo < 60:
            warnings.append("Very slow tempo may result in sparse composition")
        elif tempo > 160:
            warnings.append("Very fast tempo may result in dense composition")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
```

---

## 18. Future Roadmap

### 18.1 Phase 2 Features

| Feature | Description | Priority |
|---------|-------------|----------|
| **Native Audio Engine** | C++ low-latency audio | High |
| **Neural Inference** | Real ML model serving | High |
| **Voice Synthesis** | Waveform generation | Medium |
| **Advanced Mixing** | Autonomous mastering | Medium |
| **Sensor Integration** | EEG, gesture control | Low |
| **Cloud Sync** | Collaboration features | Low |
| **Mobile App** | iOS/Android support | Medium |

### 18.2 Architecture Evolution

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FUTURE ARCHITECTURE                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 1 (Current)                    Phase 2 (Future)
┌─────────────────┐                  ┌─────────────────┐
│   Python Core   │                  │   C++ Engine    │
│   (Pure Python) │                  │   (Native)      │
└────────┬────────┘                  └────────┬────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────┐                  ┌─────────────────┐
│   Simple WAV    │                  │   Real-time     │
│   Generation    │                  │   Audio         │
└────────┬────────┘                  └────────┬────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────┐                  ┌─────────────────┐
│   Rule-based    │                  │   Neural        │
│   AI            │                  │   Networks      │
└────────┬────────┘                  └────────┬────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────┐                  ┌─────────────────┐
│   Local Only    │                  │   Cloud + Local │
│                 │                  │   Hybrid        │
└─────────────────┘                  └─────────────────┘
```

---

## 19. Glossary

| Term | Definition |
|------|------------|
| **ADSR** | Attack, Decay, Sustain, Release - envelope parameters for sound shaping |
| **BPM** | Beats Per Minute - tempo measurement |
| **FFT** | Fast Fourier Transform - frequency analysis algorithm |
| **LUFS** | Loudness Units Full Scale - loudness measurement standard |
| **MIDI** | Musical Instrument Digital Interface - protocol for musical data |
| **PCM** | Pulse Code Modulation - digital audio representation |
| **RMS** | Root Mean Square - average signal level measurement |
| **Sargam** | Indian solfège system (Sa, Re, Ga, Ma, Pa, Dha, Ni) |
| **STT** | Speech-to-Text - voice recognition technology |
| **TTS** | Text-to-Speech - voice synthesis technology |
| **WAV** | Waveform Audio File Format - uncompressed audio format |

---

## 20. References

1. **Python Documentation**: https://docs.python.org/3/
2. **Tkinter Documentation**: https://docs.python.org/3/library/tkinter.html
3. **faster-whisper**: https://github.com/SYSTRAN/faster-whisper
4. **edge-tts**: https://github.com/rany2/edge-tts
5. **Music Theory**: https://www.musictheory.net/
6. **Digital Signal Processing**: https://dspguide.com/
7. **Audio Engineering**: https://www.aes.org/

---

## 📝 Document Information

**Document Title:** SonicForge X - Technical Architecture Document  
**Version:** 1.0.0  
**Author:** Satya Narayan Sahu  
**Date:** March 27, 2026  
**Status:** Final  
**Classification:** Open Source - MIT License  

---

## 🎵 About the Developer

**Satya Narayan Sahu** is a passionate software developer and music enthusiast who created SonicForge X to democratize music production through AI. This project represents the intersection of technology and art, making professional music composition accessible to everyone.

---

*"Music is the universal language of mankind."* - Henry Wadsworth Longfellow

---

**© 2026 Satya Narayan Sahu. All rights reserved.**