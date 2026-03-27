# Satya Sangeet Harmonium - My First AI Music Project

Hey there! Welcome to my project documentation. My name is **Satya Narayan Sahu**, and I'm a student who loves both coding and music. This is my project called **Satya Sangeet
Harmonium** - basically, it's an AI system that can compose music, mix tracks, and even teach you how to play harmonium!

I built this entire thing from scratch using Python, and honestly, it was quite an adventure. Let me tell you everything about it!

---

## What Is Satya Sangeet Harmonium?

So, Satya Sangeet Harmonium is basically an **AI-powered music production system**. Think of it like having a super smart music assistant that can:

1. **Compose music** based on emotions (like happy, sad, energetic, etc.)
2. **Mix and master** your tracks automatically
3. **Teach you harmonium** with a voice coach that actually talks to you
4. **Export your music** as WAV files that you can play anywhere

The cool part? I made the entire core system using only Python's built-in libraries - no fancy external packages needed! This means you can run it on any computer with Python installed.

---

## How I Built This (The Architecture)

Let me break down how the whole system works:

### The Big Picture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOU (The User)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────────────┐
│              Choose Your Interface                         │
│  ┌─────────────────┐           ┌─────────────────┐         │
│  │  Desktop App    │           │   Web Browser   │         │
│  │  (Tkinter GUI)  │           │   (HTTP App)    │         │
│  └────────┬────────┘           └────────┬────────┘         │
└───────────┼─────────────────────────────┼──────────────────┘
            │                             │
            └──────────────┬──────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway                              │
│         (Handles all your requests)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 CORE ENGINE                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │  Harmonium  │ │Harmonium AI │ │  AcademyAI  │            │
│  │ ( Play it ) │ │(A testing)  │ │ (Teaches)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### The Modules (Parts of the System)

I divided the whole project into different modules, each doing a specific job:

#### 1. **Core Engine** (`sonicforge/core/`)
This is the brain of the system. It contains:

- **composer.py** - The music composition engine. It takes your emotion input and creates music using music theory rules. It understands things like chord progressions, scales, and melody generation.

- **mixmaster.py** - The audio mixing engine. It analyzes your tracks, finds problems (like frequency conflicts or low headroom), and automatically fixes them. It can also give you suggestions on how to improve your mix.

- **cocreator.py** - The AI suggestion engine. After you compose something, it analyzes it and suggests improvements or variations.

- **sound_dna.py** - The sound design engine. It generates unique sound timbres and textures.

- **voice.py** - Handles voice input/output. It uses speech recognition and text-to-speech for the academy coach.

- **session.py** - Manages your session state. It keeps track of what you've done, supports undo/redo, and saves your preferences.

- **models.py** - Defines all the data structures like Note, Track, Composition, etc.

- **academy_ai.py** - The conversational AI for the harmonium academy. It can answer questions, navigate lessons, and have natural conversations.

- **academy_stt.py** - Speech-to-text using faster-whisper library.

- **academy_tts.py** - Text-to-speech using edge-tts library.

#### 2. **Applications** (`sonicforge/apps/`)
These are the different ways you can use the system:

- **desktop.py** - A native desktop application built with Tkinter. It has a nice dark theme UI where you can compose, mix, and export music.

- **server.py** - A web server that serves the web interface and handles API requests.

- **llm_gateway.py** - A gateway for connecting to large language models (for future features).

#### 3. **Web Interface** (`sonicforge/web/`)
The browser-based interface:

- **index.html** - The main page where you compose and mix music
- **harmonium.html** - The 3D harmonium simulator page
- **app.js** - JavaScript code that talks to the backend
- **harmonium.js** - Code for the harmonium simulator
- **styles.css** - The styling (dark theme, modern look)

---

## How The AI Works

### The Composition Algorithm

When you tell the system "compose happy music in C major at 120 BPM", here's what happens:

1. **Emotion Mapping**: The system maps "happy" to musical parameters:
   - Major key mode
   - Fast tempo (100-140 BPM)
   - High intensity (0.8)
   - Medium complexity (0.6)

2. **Scale Selection**: For C major, it selects the C major scale notes: C, D, E, F, G, A, B

3. **Chord Progression**: It picks a chord progression that sounds happy, like I-V-vi-IV (C-G-Am-F)

4. **Melody Generation**: It creates a melody by:
   - Starting on the root note (C)
   - Moving up and down the scale
   - Using weighted random choices (more likely to go up for happy music)
   - Varying note durations

5. **Bass Line**: It generates a bass line that follows the chord roots

6. **Voice Leading**: It ensures smooth transitions between chords (no awkward jumps)

7. **Assembly**: It puts everything together into a Composition object with tracks

### The Mix Analysis Algorithm

The MixMaster analyzes your tracks by:

1. **Frequency Analysis**: Uses FFT (Fast Fourier Transform) to see what frequencies are present in each track
2. **Dynamic Range**: Measures how loud and quiet parts are
3. **Stereo Width**: Checks how wide the stereo image is
4. **Headroom**: Makes sure nothing is clipping (going over 0dB)

It then generates metrics like:
- Headroom (how much space before clipping)
- Stereo Width (how wide the sound is)
- Low-End Focus (how much bass energy)
- Dynamic Range (difference between loud and quiet parts)

### The Academy AI

The voice coach uses a pattern-matching algorithm:

1. **Text Normalization**: Converts your text to lowercase, removes punctuation
2. **Tokenization**: Breaks your sentence into words
3. **Intent Classification**: Matches patterns like:
   - "hello", "hi", "namaste" → greeting
   - "pause", "stop" → control command
   - "what is", "how to" → question
4. **Knowledge Retrieval**: Searches the lesson content for relevant answers
5. **Response Generation**: Creates a natural-sounding response

---

## Technical Stuff (For The Nerds)

### Data Structures

I designed these data structures to represent musical concepts:

```python
@dataclass
class Note:
    """Represents a single musical note"""
    pitch: int          # MIDI note number (0-127)
    velocity: int       # How hard the note is played (0-127)
    start_time: float   # When the note starts (in beats)
    duration: float     # How long the note lasts (in beats)
    channel: int        # MIDI channel (0-15)
    
    @property
    def frequency(self) -> float:
        """Converts MIDI pitch to frequency in Hz"""
        return 440.0 * (2.0 ** ((self.pitch - 69) / 12.0))

@dataclass
class Track:
    """Represents an audio track"""
    name: str
    instrument: str
    notes: List[Note]
    volume: float = 0.8
    pan: float = 0.0
    effects: List[str] = None

@dataclass
class Composition:
    """Represents a complete musical composition"""
    title: str
    key: str
    tempo: int
    time_signature: Tuple[int, int]
    tracks: List[Track]
    metadata: Dict = None
```

### WAV Generation

To generate WAV files, I implemented this algorithm:

1. Calculate total duration from all tracks
2. Create an audio buffer (array of samples)
3. For each note in each track:
   - Calculate frequency from MIDI pitch
   - Generate waveform (sine waves with harmonics)
   - Apply ADSR envelope (Attack, Decay, Sustain, Release)
   - Apply volume and pan settings
   - Mix into the buffer
4. Normalize the audio (prevent clipping)
5. Encode as WAV file with proper headers

### Speech Recognition

For voice input, I use **faster-whisper** (a fast version of OpenAI's Whisper model):

1. Record audio from microphone
2. Convert to 16kHz mono audio
3. Run through Whisper model
4. Get text transcription
5. Send to Academy AI for processing

### Text-to-Speech

For voice output, I use **edge-tts** (Microsoft's TTS service):

1. Get text response from Academy AI
2. Send to edge-tts API
3. Receive MP3 audio
4. Play through browser audio

---

## How to Run This

### Option 1: Web App (Easiest)

```bash
# Open terminal and run:
python3 -m sonicforge.apps.server

# Then open your browser and go to:
# http://127.0.0.1:8000
```

### Option 2: Desktop App

```bash
# Open terminal and run:
python3 -m sonicforge.apps.desktop

# A window will pop up with the desktop interface
```

### Option 3: Master Launcher (Recommended)

```bash
# This handles everything automatically:
python3 run_sonicforge.py --mode both

# Or just web:
python3 run_sonicforge.py --mode web

# Or just desktop:
python3 run_sonicforge.py --mode desktop
```

### Running Tests

```bash
# Run all tests:
python3 -m unittest discover -s tests

# Run specific test:
python3 -m unittest tests.test_composer
```

---

## Project Structure

Here's how I organized all the files:

```
SonicForge/
├── sonicforge/              # Main package
│   ├── core/               # Core engine modules
│   │   ├── composer.py     # Music composition
│   │   ├── mixmaster.py    # Audio mixing
│   │   ├── cocreator.py    # AI suggestions
│   │   ├── sound_dna.py    # Sound design
│   │   ├── voice.py        # Voice processing
│   │   ├── session.py      # Session management
│   │   ├── models.py       # Data structures
│   │   ├── academy_ai.py   # Academy AI coach
│   │   ├── academy_stt.py  # Speech-to-text
│   │   └── academy_tts.py  # Text-to-speech
│   │
│   ├── apps/               # Application interfaces
│   │   ├── desktop.py      # Tkinter desktop app
│   │   ├── server.py       # Web server
│   │   └── llm_gateway.py  # LLM integration
│   │
│   └── web/                # Web interface
│       ├── index.html      # Main page
│       ├── harmonium.html  # Harmonium page
│       ├── app.js          # Main JavaScript
│       ├── harmonium.js    # Harmonium code
│       ├── styles.css      # Styling
│       └── *.mp3           # Harmonium samples
│
├── tests/                  # Unit tests
│   ├── test_composer.py
│   ├── test_academy_ai.py
│   └── test_core.py
│
├── Architecture/           # Documentation
│   └── document.md         # Technical architecture doc
│
├── run_sonicforge.py       # Master launcher
├── requirements.txt        # Dependencies (minimal!)
└── README.md              # This file!
```

---

## What Makes This Special

### 1. Zero External Dependencies (Almost!)

The core engine uses only Python built-in libraries:
- `wave` - For WAV file generation
- `struct` - For binary data packing
- `math` - For mathematical calculations
- `random` - For randomization
- `json` - For data serialization
- `tkinter` - For desktop GUI (built-in)
- `http.server` - For web server (built-in)

The only external packages are:
- `faster-whisper` - For speech recognition
- `edge-tts` - For text-to-speech

### 2. Emotion-Driven Composition

Most music software just lets you pick a key and tempo. Mine actually understands emotions and maps them to musical characteristics!

### 3. Real-Time Mixing Analysis

The MixMaster doesn't just mix - it analyzes your tracks and tells you what's wrong and how to fix it.

### 4. Conversational AI Coach

The harmonium academy has a voice coach that can have natural conversations, answer questions, and guide you through lessons.

### 5. Multiple Interfaces

You can use it as:
- A desktop application (native feel)
- A web application (accessible from anywhere)
- Both at the same time!

---

## Future Plans (Phase 2)

I have big plans for the future:

1. **Native Audio Engine**: Replace Python's wave module with a C++ engine for lower latency
2. **Real Neural Networks**: Use actual ML models instead of rule-based algorithms
3. **Voice Synthesis**: Generate actual singing voices
4. **Advanced Mixing**: AI that can master tracks professionally
5. **Sensor Integration**: Use EEG brain sensors or gesture controllers
6. **Cloud Collaboration**: Work on music with friends in real-time
7. **Mobile Apps**: iOS and Android versions

---

## Testing

I wrote unit tests to make sure everything works:

```python
# Example test from tests/test_composer.py
def test_compose_happy_emotion(self):
    """Test composition with happy emotion"""
    composition = self.composer.compose("happy", 120, "C")
    
    self.assertIsInstance(composition, Composition)
    self.assertEqual(composition.key, "C")
    self.assertEqual(composition.tempo, 120)
    self.assertGreater(len(composition.tracks), 0)
```

Run tests with:
```bash
python3 -m unittest discover -s tests -v
```

---

## 🐛 Known Limitations

Let me be honest about what this can't do (yet):

1. **Simple WAV Generation**: The audio quality is basic (sine waves, not realistic instruments)
2. **Rule-Based AI**: Not using real machine learning yet
3. **Limited Instruments**: Only piano and bass sounds
4. **No Real-Time Preview**: Can't hear the music while composing
5. **Basic Mixing**: The mixing algorithms are simple

But hey, it's a Phase 1 MVP! The foundation is solid for future improvements.

---

## What I Learned

Building this project taught me:

1. **Music Theory**: How chords, scales, and progressions work
2. **Digital Audio**: How sound is represented digitally (PCM, WAV format)
3. **Signal Processing**: FFT, frequency analysis, filtering
4. **AI/NLP**: Pattern matching, intent classification, conversation management
5. **Web Development**: HTTP servers, REST APIs, JavaScript
6. **Desktop GUI**: Tkinter, event-driven programming
7. **Software Architecture**: How to organize a large project
8. **Testing**: Writing unit tests, test-driven development

---

## Technical Deep Dive

Want to know more? Check out the **Architecture Document** at:
`Architecture/document.md`

It has:
- Detailed algorithm explanations
- Code examples
- Data structure definitions
- Flowcharts and diagrams
- API specifications
- And much more!

---

## Contributing

This is my personal project, but if you want to suggest improvements or report bugs, feel free to reach out!

**Contact**: Satya Narayan Sahu

---

## COPYRIGHT NOTICE

**© 2026 Satya Narayan Sahu. All Rights Reserved.**

This is my original work. Please respect my intellectual property:

### What You CAN Do:
- ✅ Study the code for learning
- ✅ Use it for school projects (with credit)
- ✅ Reference it in academic work

### What You CANNOT Do:
- ❌ Use it commercially
- ❌ Share the code with others
- ❌ Copy parts of the code
- ❌ Earn money using this software
- ❌ Reverse engineer it
- ❌ Remove my name from it

**Legal Warning**: Unauthorized use, copying, or distribution is a violation of copyright law and may result in legal action.

For licensing inquiries, contact: **Satya Narayan Sahu**

---

## Project Stats

- **Total Lines of Code**: ~5,000+
- **Programming Languages**: Python, JavaScript, HTML, CSS
- **Development Time**: Several months
- **External Dependencies**: Only 2 (faster-whisper, edge-tts)
- **Test Coverage**: Core modules tested
- **Platforms**: Windows, macOS, Linux

---

## Conclusion

SonicForge X is my passion project that combines my love for music and coding. It's not perfect, but it's a solid foundation for an AI-powered music production system.

The best part? I built the entire core engine using only Python's built-in libraries - no fancy frameworks or external packages needed for the main functionality!

If you're a student like me interested in AI, music, or software development, I hope this project inspires you to build something cool too!

**Remember**: This is proprietary software owned by me. Please respect the copyright notice above.

---

*"Music is the universal language of mankind."* - Henry Wadsworth Longfellow

---

**Made with ❤️ by Satya Narayan Sahu**
**© 2026 All Rights Reserved**
