const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const SARGAM_LABELS = ["Sa", "r", "Re", "g", "Ga", "Ma", "Ma+", "Pa", "d", "Dha", "n", "Ni"];
const BLACK_PITCHES = new Set([1, 3, 6, 8, 10]);

const KEYBOARD_BINDINGS = [
  { code: "KeyZ", label: "Z" },
  { code: "KeyS", label: "S" },
  { code: "KeyX", label: "X" },
  { code: "KeyD", label: "D" },
  { code: "KeyC", label: "C" },
  { code: "KeyV", label: "V" },
  { code: "KeyG", label: "G" },
  { code: "KeyB", label: "B" },
  { code: "KeyH", label: "H" },
  { code: "KeyN", label: "N" },
  { code: "KeyJ", label: "J" },
  { code: "KeyM", label: "M" },
  { code: "KeyQ", label: "Q" },
  { code: "Digit2", label: "2" },
  { code: "KeyW", label: "W" },
  { code: "Digit3", label: "3" },
  { code: "KeyE", label: "E" },
  { code: "KeyR", label: "R" },
  { code: "Digit5", label: "5" },
  { code: "KeyT", label: "T" },
  { code: "Digit6", label: "6" },
  { code: "KeyY", label: "Y" },
  { code: "Digit7", label: "7" },
  { code: "KeyU", label: "U" },
  { code: "KeyI", label: "I" },
];

const PRESETS = {
  classical: {
    label: "Classical Concert",
    masterVolume: 76,
    bellowsPressure: 74,
    brightness: 58,
    attack: 18,
    release: 240,
    reverb: 18,
    droneVolume: 58,
    stops: { bass: true, male: true, female: false },
    coupler: false,
    autoBellows: true,
    aiIntent: "alap",
  },
  bhajan: {
    label: "Bhajan Bed",
    masterVolume: 82,
    bellowsPressure: 80,
    brightness: 46,
    attack: 28,
    release: 420,
    reverb: 26,
    droneVolume: 68,
    stops: { bass: true, male: true, female: false },
    coupler: false,
    autoBellows: true,
    aiIntent: "bhajan",
  },
  film: {
    label: "Film Glow",
    masterVolume: 74,
    bellowsPressure: 70,
    brightness: 64,
    attack: 42,
    release: 520,
    reverb: 34,
    droneVolume: 62,
    stops: { bass: true, male: true, female: true },
    coupler: true,
    autoBellows: true,
    aiIntent: "film",
  },
  bright: {
    label: "Bright Lead",
    masterVolume: 78,
    bellowsPressure: 76,
    brightness: 78,
    attack: 10,
    release: 150,
    reverb: 12,
    droneVolume: 50,
    stops: { bass: false, male: true, female: true },
    coupler: true,
    autoBellows: true,
    aiIntent: "taan",
  },
};

const AI_INTENTS = {
  alap: {
    label: "Classical Alap",
    anchorOffset: 0,
    baseDuration: 620,
    template: [0, 2, 4, 5, 7, 5, 4, 2, 0, 2, 4, 7, 9, 7, 5, 4],
    alternate: [0, 2, 3, 5, 7, 5, 3, 2, 0, 2, 5, 7, 5, 3, 2, 0],
    graceDirection: -1,
  },
  bhajan: {
    label: "Bhajan Lead",
    anchorOffset: 0,
    baseDuration: 500,
    template: [0, 4, 5, 7, 5, 4, 2, 0, 4, 5, 7, 9, 7, 5, 4, 2],
    alternate: [0, 2, 4, 5, 7, 5, 4, 2, 0, 2, 4, 7, 5, 4, 2, 0],
    graceDirection: 1,
  },
  film: {
    label: "Film Melody",
    anchorOffset: 5,
    baseDuration: 420,
    template: [0, 2, 7, 5, 4, 7, 9, 7, 5, 4, 2, 0, 7, 5, 4, 2],
    alternate: [0, 4, 7, 9, 7, 5, 4, 2, 0, 2, 7, 9, 7, 5, 4, 2],
    graceDirection: -1,
  },
  taan: {
    label: "Fast Taan",
    anchorOffset: 0,
    baseDuration: 230,
    template: [0, 2, 4, 5, 7, 9, 11, 12, 11, 9, 7, 5, 4, 2, 0, 2],
    alternate: [0, 2, 4, 7, 9, 12, 9, 7, 5, 4, 2, 0, 2, 4, 7, 5],
    graceDirection: 1,
  },
};

const HARMONIUM_SAMPLE_ANCHORS = [
  {
    note: "C3",
    midi: 48,
    url: "/harmonium_c3.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523878/",
  },
  {
    note: "F3",
    midi: 53,
    url: "/harmonium_f3.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523882/",
  },
  {
    note: "G3",
    midi: 55,
    url: "/harmonium_g3.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523888/",
  },
  {
    note: "C4",
    midi: 60,
    url: "/harmonium_c4.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523877/",
  },
  {
    note: "F4",
    midi: 65,
    url: "/harmonium_f4.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523885/",
  },
  {
    note: "A4",
    midi: 69,
    url: "/harmonium_a4.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523857/",
  },
  {
    note: "C5",
    midi: 72,
    url: "/harmonium_c5.mp3",
    sourcePage: "https://freesound.org/people/cabled_mess/sounds/523876/",
  },
];

const dom = {
  saRoot: document.getElementById("sa-root"),
  baseOctave: document.getElementById("base-octave"),
  displayMode: document.getElementById("display-mode"),
  masterVolume: document.getElementById("master-volume"),
  bellowsPressure: document.getElementById("bellows-pressure"),
  brightness: document.getElementById("brightness"),
  attack: document.getElementById("attack"),
  release: document.getElementById("release"),
  reverbMix: document.getElementById("reverb-mix"),
  droneVolume: document.getElementById("drone-volume"),
  aiIntent: document.getElementById("ai-intent"),
  aiLength: document.getElementById("ai-length"),
  aiOrnament: document.getElementById("ai-ornament"),
  aiPrecision: document.getElementById("ai-precision"),
  aiGenerate: document.getElementById("ai-generate"),
  aiPreview: document.getElementById("ai-preview"),
  aiSummary: document.getElementById("ai-summary"),
  aiPhraseTrack: document.getElementById("ai-phrase-track"),
  keybed: document.getElementById("harmonium-keybed"),
  sampleEngineStatus: document.getElementById("sample-engine-status"),
  bellowsVisual: document.getElementById("bellows-visual"),
  bellowsLive: document.getElementById("bellows-live"),
  tonicLive: document.getElementById("tonic-live"),
  registerLive: document.getElementById("register-live"),
  noteReadout: document.getElementById("note-readout"),
  shortcutReadout: document.getElementById("shortcut-readout"),
  frequencyReadout: document.getElementById("frequency-readout"),
  droneReadout: document.getElementById("drone-readout"),
  pressedCount: document.getElementById("pressed-count"),
  mappingSummary: document.getElementById("mapping-summary"),
  activeStack: document.getElementById("active-stack"),
  panicButton: document.getElementById("panic-button"),
  pumpBellows: document.getElementById("pump-bellows"),
  droneLabels: {
    sa: document.getElementById("drone-sa-label"),
    pa: document.getElementById("drone-pa-label"),
    ni: document.getElementById("drone-ni-label"),
  },
  volumeValue: document.getElementById("volume-value"),
  bellowsTargetValue: document.getElementById("bellows-target-value"),
  brightnessValue: document.getElementById("brightness-value"),
  attackValue: document.getElementById("attack-value"),
  releaseValue: document.getElementById("release-value"),
  reverbValue: document.getElementById("reverb-value"),
  droneVolumeValue: document.getElementById("drone-volume-value"),
  aiLengthValue: document.getElementById("ai-length-value"),
  aiOrnamentValue: document.getElementById("ai-ornament-value"),
  aiPrecisionValue: document.getElementById("ai-precision-value"),
  presetButtons: Array.from(document.querySelectorAll(".preset-button")),
  stopButtons: Array.from(document.querySelectorAll("[data-stop]")),
  modeButtons: Array.from(document.querySelectorAll("[data-mode]")),
  droneButtons: Array.from(document.querySelectorAll("[data-drone]")),
};

const state = {
  rootSemitone: Number(dom.saRoot.value),
  baseOctave: Number(dom.baseOctave.value),
  displayMode: dom.displayMode.value,
  masterVolume: Number(dom.masterVolume.value),
  bellowsTarget: Number(dom.bellowsPressure.value),
  currentBellows: Number(dom.bellowsPressure.value),
  brightness: Number(dom.brightness.value),
  attackMs: Number(dom.attack.value),
  releaseMs: Number(dom.release.value),
  reverbMix: Number(dom.reverbMix.value),
  droneVolume: Number(dom.droneVolume.value),
  aiIntent: dom.aiIntent.value,
  aiLength: Number(dom.aiLength.value),
  aiOrnament: Number(dom.aiOrnament.value),
  aiPrecision: Number(dom.aiPrecision.value),
  autoBellows: true,
  coupler: false,
  stops: { bass: true, male: true, female: false },
  drones: { sa: false, pa: false, ni: false },
  lastEvent: null,
  keyLayout: [],
  pressedNotes: new Set(),
  currentPreset: "classical",
  aiPhrase: [],
  aiPreviewTimers: [],
  pressedKeyCodes: new Set(),
};

let audioContext = null;
let masterBus = null;
let cabinetDrive = null;
let cabinetTone = null;
let dryGain = null;
let verbSend = null;
let verbPreDelay = null;
let verbGain = null;
let convolver = null;
let verbTone = null;
let noiseGain = null;
let compressor = null;
let masterOutput = null;
let periodicWaves = {};
let attackNoiseBuffer = null;
let activeVoices = new Map();
let animationHandle = 0;
const sampleLibrary = {
  status: "idle",
  buffers: new Map(),
  loadingPromise: null,
  error: null,
};

function midiToFrequency(midi) {
  return 440 * 2 ** ((midi - 69) / 12);
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function formatNoteName(midi) {
  const pitchClass = midi % 12;
  const octave = Math.floor(midi / 12) - 1;
  return `${NOTE_NAMES[pitchClass]}${octave}`;
}

function relativeSargam(pitchClass) {
  const relative = (pitchClass - state.rootSemitone + 12) % 12;
  return SARGAM_LABELS[relative];
}

function noteDescriptorForMidi(midi, fallbackLabel = "--") {
  const visible = state.keyLayout.find((item) => item.midi === midi) || null;
  return {
    midi,
    pitchClass: midi % 12,
    noteName: formatNoteName(midi),
    frequency: midiToFrequency(midi),
    sargam: relativeSargam(midi % 12),
    binding: { label: visible?.binding.label || fallbackLabel },
    button: visible?.button || null,
  };
}

function registerSummary() {
  const enabled = [];
  if (state.stops.bass) {
    enabled.push("Bass");
  }
  if (state.stops.male) {
    enabled.push("Male");
  }
  if (state.stops.female) {
    enabled.push("Female");
  }
  if (!enabled.length) {
    enabled.push("Male");
  }
  if (state.coupler) {
    enabled.push("Coupler");
  }
  return enabled.join(" + ");
}

function anyPrimaryStopEnabled() {
  return state.stops.bass || state.stops.male || state.stops.female;
}

function createNoiseBuffer(context, seconds) {
  const buffer = context.createBuffer(1, Math.floor(context.sampleRate * seconds), context.sampleRate);
  const channel = buffer.getChannelData(0);
  for (let i = 0; i < channel.length; i += 1) {
    channel[i] = Math.random() * 2 - 1;
  }
  return buffer;
}

function createImpulseResponse(context, seconds, decay) {
  const buffer = context.createBuffer(2, Math.floor(context.sampleRate * seconds), context.sampleRate);
  for (let channelIndex = 0; channelIndex < buffer.numberOfChannels; channelIndex += 1) {
    const channel = buffer.getChannelData(channelIndex);
    for (let i = 0; i < channel.length; i += 1) {
      const envelope = (1 - i / channel.length) ** decay;
      channel[i] = (Math.random() * 2 - 1) * envelope;
    }
  }
  return buffer;
}

function createBlessedImpulseResponse(context, seconds, decay) {
  const buffer = context.createBuffer(2, Math.floor(context.sampleRate * seconds), context.sampleRate);
  const taps = [
    { time: 0.013, gain: 0.72 },
    { time: 0.021, gain: 0.48 },
    { time: 0.034, gain: 0.34 },
    { time: 0.048, gain: 0.22 },
  ];

  for (let channelIndex = 0; channelIndex < buffer.numberOfChannels; channelIndex += 1) {
    const channel = buffer.getChannelData(channelIndex);
    for (let i = 0; i < channel.length; i += 1) {
      const time = i / context.sampleRate;
      const tail = (1 - i / channel.length) ** decay;
      const shimmer = Math.sin(time * (channelIndex === 0 ? 37 : 41)) * 0.16;
      const warmth = Math.sin(time * 9.5) * 0.08;
      channel[i] = ((Math.random() * 2 - 1) * 0.22 + shimmer + warmth) * tail;
    }

    taps.forEach((tap, tapIndex) => {
      const tapIndexSamples = Math.min(channel.length - 1, Math.floor(tap.time * context.sampleRate));
      channel[tapIndexSamples] += tap.gain * (channelIndex === 0 ? 1 : 0.92 - tapIndex * 0.08);
    });
  }

  return buffer;
}

function createWaveShaperCurve(amount) {
  const samples = 44100;
  const curve = new Float32Array(samples);
  for (let i = 0; i < samples; i += 1) {
    const x = (i * 2) / samples - 1;
    curve[i] = ((Math.PI + amount) * x) / (Math.PI + amount * Math.abs(x));
  }
  return curve;
}

function createPeriodicWave(context, amplitudes) {
  const real = new Float32Array(amplitudes.length + 1);
  const imag = new Float32Array(amplitudes.length + 1);
  for (let i = 0; i < amplitudes.length; i += 1) {
    imag[i + 1] = amplitudes[i];
  }
  return context.createPeriodicWave(real, imag, { disableNormalization: false });
}

function updateSampleEngineStatus() {
  if (!dom.sampleEngineStatus) {
    return;
  }
  if (sampleLibrary.status === "ready") {
    dom.sampleEngineStatus.textContent = "Real sampled harmonium";
    return;
  }
  if (sampleLibrary.status === "loading") {
    dom.sampleEngineStatus.textContent = "Loading samples";
    return;
  }
  if (sampleLibrary.status === "error") {
    dom.sampleEngineStatus.textContent = "Fallback reed engine";
    return;
  }
  dom.sampleEngineStatus.textContent = "Preparing engine";
}

function findNearestZeroCrossing(channelData, centerIndex, radius) {
  let bestIndex = clamp(centerIndex, 1, channelData.length - 2);
  let bestScore = Number.POSITIVE_INFINITY;

  for (let offset = -radius; offset <= radius; offset += 1) {
    const index = clamp(centerIndex + offset, 1, channelData.length - 2);
    const current = channelData[index];
    const next = channelData[index + 1];
    const crossesZero =
      (current <= 0 && next >= 0) || (current >= 0 && next <= 0);
    const score = Math.abs(current) + Math.abs(next) + (crossesZero ? 0 : 0.25);
    if (score < bestScore) {
      bestScore = score;
      bestIndex = index;
    }
  }

  return bestIndex;
}

function sampleLoopPoints(buffer) {
  const channelData = buffer.getChannelData(0);
  const minGapSec = 0.42;
  const baseStartSec = clamp(buffer.duration * 0.34, 0.32, Math.max(0.32, buffer.duration - 1.2));
  const baseEndSec = clamp(buffer.duration - 0.16, baseStartSec + minGapSec, buffer.duration - 0.04);
  const searchRadius = Math.max(48, Math.floor(buffer.sampleRate * 0.018));

  let startIndex = findNearestZeroCrossing(
    channelData,
    Math.floor(baseStartSec * buffer.sampleRate),
    searchRadius
  );
  let endIndex = findNearestZeroCrossing(
    channelData,
    Math.floor(baseEndSec * buffer.sampleRate),
    searchRadius
  );

  if ((endIndex - startIndex) / buffer.sampleRate < minGapSec) {
    startIndex = Math.floor(baseStartSec * buffer.sampleRate);
    endIndex = Math.floor(baseEndSec * buffer.sampleRate);
  }

  const loopStart = startIndex / buffer.sampleRate;
  const loopEnd = endIndex / buffer.sampleRate;
  return { loopStart, loopEnd };
}

function sampleAttackStart(buffer) {
  const channelData = buffer.getChannelData(0);
  const threshold = 0.01;
  const previewWindow = Math.min(channelData.length, Math.floor(buffer.sampleRate * 0.28));

  for (let index = 0; index < previewWindow; index += 1) {
    if (Math.abs(channelData[index]) >= threshold) {
      return Math.max(0, index / buffer.sampleRate - 0.01);
    }
  }

  return 0;
}

function sampleTrimGain(buffer) {
  const channelData = buffer.getChannelData(0);
  const startIndex = Math.floor(sampleAttackStart(buffer) * buffer.sampleRate);
  const endIndex = Math.min(channelData.length, startIndex + Math.floor(buffer.sampleRate * 0.55));
  let peak = 0;

  for (let index = startIndex; index < endIndex; index += 1) {
    peak = Math.max(peak, Math.abs(channelData[index]));
  }

  if (!peak) {
    return 1;
  }

  return clamp(0.84 / peak, 0.75, 1.22);
}

async function ensureSampleLibraryReady() {
  if (!audioContext) {
    return false;
  }
  if (sampleLibrary.status === "ready") {
    return true;
  }
  if (sampleLibrary.status === "error") {
    return false;
  }
  if (sampleLibrary.loadingPromise) {
    return sampleLibrary.loadingPromise;
  }

  sampleLibrary.status = "loading";
  updateSampleEngineStatus();

  sampleLibrary.loadingPromise = Promise.all(
    HARMONIUM_SAMPLE_ANCHORS.map(async (anchor) => {
      const response = await fetch(anchor.url);
      if (!response.ok) {
        throw new Error(`sample fetch failed for ${anchor.note}`);
      }
      const bytes = await response.arrayBuffer();
      const buffer = await audioContext.decodeAudioData(bytes.slice(0));
      const { loopStart, loopEnd } = sampleLoopPoints(buffer);
      sampleLibrary.buffers.set(anchor.note, {
        ...anchor,
        buffer,
        loopStart,
        loopEnd,
        startOffset: sampleAttackStart(buffer),
        trimGain: sampleTrimGain(buffer),
      });
    })
  )
    .then(() => {
      sampleLibrary.status = "ready";
      sampleLibrary.error = null;
      updateSampleEngineStatus();
      return true;
    })
    .catch((error) => {
      sampleLibrary.status = "error";
      sampleLibrary.error = error;
      updateSampleEngineStatus();
      return false;
    });

  return sampleLibrary.loadingPromise;
}

function chooseNearestSample(targetMidi, maxStretchSemitones = Number.POSITIVE_INFINITY) {
  let winner = null;
  sampleLibrary.buffers.forEach((anchor) => {
    if (!winner || Math.abs(anchor.midi - targetMidi) < Math.abs(winner.midi - targetMidi)) {
      winner = anchor;
    }
  });
  if (!winner) {
    return null;
  }
  return Math.abs(winner.midi - targetMidi) <= maxStretchSemitones ? winner : null;
}

function resolveRegisterTarget(targetMidi, preferredOffset, maxStretchSemitones, fallbackToBase = true) {
  const preferredMidi = targetMidi + preferredOffset;
  if (chooseNearestSample(preferredMidi, maxStretchSemitones)) {
    return preferredMidi;
  }
  if (fallbackToBase && chooseNearestSample(targetMidi, maxStretchSemitones)) {
    return targetMidi;
  }
  return null;
}

function createSamplePart(targetMidi, mixNode, options = {}) {
  if (targetMidi == null) {
    return null;
  }

  const {
    detuneCents = 0,
    filterType = null,
    filterFrequency = 1200,
    filterQ = 0.7,
    loop = true,
    maxStretchSemitones = Number.POSITIVE_INFINITY,
    outputTrim = 1,
  } = options;
  const anchor = chooseNearestSample(targetMidi, maxStretchSemitones);
  if (!anchor) {
    return null;
  }

  const source = audioContext.createBufferSource();
  const trim = audioContext.createGain();
  const gain = audioContext.createGain();
  const playbackRate = 2 ** ((targetMidi - anchor.midi) / 12);

  source.buffer = anchor.buffer;
  source.playbackRate.value = playbackRate;
  source.detune.value = detuneCents;
  if (loop) {
    source.loop = true;
    source.loopStart = anchor.loopStart;
    source.loopEnd = anchor.loopEnd;
  }

  trim.gain.value = anchor.trimGain * outputTrim;
  gain.gain.value = 0;

  if (filterType) {
    const filter = audioContext.createBiquadFilter();
    filter.type = filterType;
    filter.frequency.value = filterFrequency;
    filter.Q.value = filterQ;
    source.connect(filter);
    filter.connect(trim);
    trim.connect(gain);
    gain.connect(mixNode);
    return { source, gain, trim, filter, anchor };
  }

  source.connect(trim);
  trim.connect(gain);
  gain.connect(mixNode);
  return { source, gain, trim, anchor };
}

async function ensureAudioEngine() {
  if (!audioContext) {
    const AudioCtor = window.AudioContext || window.webkitAudioContext;
    audioContext = new AudioCtor();

    masterBus = audioContext.createGain();
    cabinetDrive = audioContext.createWaveShaper();
    cabinetTone = audioContext.createBiquadFilter();
    dryGain = audioContext.createGain();
    verbSend = audioContext.createGain();
    verbPreDelay = audioContext.createDelay(0.4);
    convolver = audioContext.createConvolver();
    verbTone = audioContext.createBiquadFilter();
    verbGain = audioContext.createGain();
    noiseGain = audioContext.createGain();
    compressor = audioContext.createDynamicsCompressor();
    masterOutput = audioContext.createGain();

    cabinetDrive.curve = createWaveShaperCurve(2.2);
    cabinetDrive.oversample = "2x";

    cabinetTone.type = "lowpass";
    cabinetTone.frequency.value = 3500;
    cabinetTone.Q.value = 0.42;

    verbPreDelay.delayTime.value = 0.022;
    convolver.buffer = createBlessedImpulseResponse(audioContext, 1.9, 5.1);
    verbTone.type = "lowpass";
    verbTone.frequency.value = 3100;
    verbTone.Q.value = 0.15;
    verbSend.gain.value = 0.028;
    verbGain.gain.value = 0.09;
    dryGain.gain.value = 0.96;

    compressor.threshold.value = -16;
    compressor.knee.value = 10;
    compressor.ratio.value = 1.8;
    compressor.attack.value = 0.008;
    compressor.release.value = 0.12;

    masterOutput.gain.value = 0.58;

    periodicWaves = {
      bass: createPeriodicWave(audioContext, [1.0, 0.46, 0.18, 0.08, 0.03]),
      male: createPeriodicWave(audioContext, [1.0, 0.78, 0.34, 0.19, 0.11, 0.07, 0.04]),
      female: createPeriodicWave(audioContext, [1.0, 0.62, 0.36, 0.22, 0.15, 0.1, 0.06]),
    };
    attackNoiseBuffer = createNoiseBuffer(audioContext, 0.09);

    const constantNoise = audioContext.createBufferSource();
    const noiseFilter = audioContext.createBiquadFilter();
    constantNoise.buffer = createNoiseBuffer(audioContext, 2.0);
    constantNoise.loop = true;
    noiseFilter.type = "bandpass";
    noiseFilter.frequency.value = 1350;
    noiseFilter.Q.value = 0.65;
    noiseGain.gain.value = 0;

    masterBus.connect(cabinetDrive);
    cabinetDrive.connect(cabinetTone);
    cabinetTone.connect(dryGain);
    cabinetTone.connect(verbSend);
    dryGain.connect(compressor);
    verbSend.connect(verbPreDelay);
    verbPreDelay.connect(convolver);
    convolver.connect(verbTone);
    verbTone.connect(verbGain);
    verbGain.connect(compressor);
    constantNoise.connect(noiseFilter);
    noiseFilter.connect(noiseGain);
    noiseGain.connect(compressor);
    compressor.connect(masterOutput);
    masterOutput.connect(audioContext.destination);
    constantNoise.start();
  }

  if (audioContext.state === "suspended") {
    await audioContext.resume();
  }

  updateSampleEngineStatus();
  void ensureSampleLibraryReady();
}

function createOscillatorPart(context, frequency, waveName, detuneCents = 0) {
  const oscillator = context.createOscillator();
  oscillator.frequency.value = frequency;
  oscillator.detune.value = detuneCents;
  if (periodicWaves[waveName]) {
    oscillator.setPeriodicWave(periodicWaves[waveName]);
  } else {
    oscillator.type = "sawtooth";
  }
  const gain = context.createGain();
  gain.gain.value = 0;
  oscillator.connect(gain);
  return { oscillator, gain };
}

function applyPitchBloom(part, settledDetune) {
  const now = audioContext.currentTime;
  part.oscillator.detune.cancelScheduledValues(now);
  part.oscillator.detune.setValueAtTime(settledDetune - 2.6, now);
  part.oscillator.detune.linearRampToValueAtTime(settledDetune, now + 0.055);
}

function startAttackNoise(mixNode, note) {
  const source = audioContext.createBufferSource();
  const filter = audioContext.createBiquadFilter();
  const gain = audioContext.createGain();
  const now = audioContext.currentTime;

  source.buffer = attackNoiseBuffer;
  filter.type = "bandpass";
  filter.frequency.value = clamp(note.frequency * 4.8, 650, 2400);
  filter.Q.value = 0.9;
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(0.016 + state.brightness / 5200, now + 0.014);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.06);

  source.connect(filter);
  filter.connect(gain);
  gain.connect(mixNode);
  source.start(now);
  source.stop(now + 0.1);
}

function currentPressureFactor() {
  return 0.16 + (state.currentBellows / 100) * 0.84;
}

function voiceBaseLevel(voice) {
  return voice.drone ? 0.2 : 0.32;
}

function refreshVoiceMix(voice) {
  const now = audioContext.currentTime;
  const fallbackMale = anyPrimaryStopEnabled() ? 0 : 1;
  const scale = voice.drone ? 0.78 : 1;

  const targets =
    voice.mode === "sample"
      ? {
          bass: state.stops.bass ? 0.06 * scale : 0,
          male: (state.stops.male ? 0.22 : 0) + fallbackMale * 0.2 * scale,
          maleBeat: 0,
          maleShimmer: 0,
          female: state.stops.female ? 0.035 * scale : 0,
          coupler: state.coupler && !voice.drone ? 0.04 : 0,
        }
      : {
          bass: state.stops.bass ? 0.13 * scale : 0,
          male: (state.stops.male ? 0.17 : 0) + fallbackMale * 0.18 * scale,
          maleBeat: (state.stops.male ? 0.13 : 0) + fallbackMale * 0.15 * scale,
          maleShimmer: (state.stops.male ? 0.05 : 0) + fallbackMale * 0.04 * scale,
          female: state.stops.female ? 0.06 * scale : 0,
          coupler: state.coupler && !voice.drone ? 0.075 : 0,
        };

  ["bass", "male", "maleBeat", "maleShimmer", "female", "coupler"].forEach((partName) => {
    if (voice.parts[partName]) {
      voice.parts[partName].gain.gain.setTargetAtTime(targets[partName], now, 0.02);
    }
  });
}

function refreshVoiceTone(voice) {
  const now = audioContext.currentTime;
  if (voice.mode === "sample") {
    const lowpass = 2600 + state.brightness * 7;
    const highpass = 34 + state.brightness * 0.06;
    const primaryFormant = clamp(voice.note.frequency * 1.05, 360, 680);

    voice.bodyLowpass.frequency.setTargetAtTime(voice.drone ? lowpass * 0.94 : lowpass, now, 0.03);
    voice.bodyLowpass.Q.setTargetAtTime(0.18 + state.brightness / 280, now, 0.03);
    voice.bodyHighpass.frequency.setTargetAtTime(highpass, now, 0.03);
    voice.formantA.frequency.setTargetAtTime(primaryFormant, now, 0.03);
    voice.formantAGain.gain.setTargetAtTime(0.028 + state.brightness / 1800, now, 0.03);
    voice.formantB.frequency.setTargetAtTime(clamp(primaryFormant * 1.85, 720, 1250), now, 0.03);
    voice.formantBGain.gain.setTargetAtTime(0.014 + state.brightness / 3000, now, 0.03);
    voice.airFormant.frequency.setTargetAtTime(clamp(primaryFormant * 2.7, 1250, 1900), now, 0.03);
    voice.airGain.gain.setTargetAtTime(0.002 + state.brightness / 9000, now, 0.03);
  } else {
    const lowpass = 1680 + state.brightness * 18;
    const highpass = 70 + state.brightness * 0.35;
    const primaryFormant = clamp(voice.note.frequency * 1.45, 520, 980);

    voice.bodyLowpass.frequency.setTargetAtTime(voice.drone ? lowpass * 0.88 : lowpass, now, 0.03);
    voice.bodyLowpass.Q.setTargetAtTime(0.44 + state.brightness / 120, now, 0.03);
    voice.bodyHighpass.frequency.setTargetAtTime(highpass, now, 0.03);
    voice.formantA.frequency.setTargetAtTime(primaryFormant, now, 0.03);
    voice.formantAGain.gain.setTargetAtTime(0.22 + state.brightness / 300, now, 0.03);
    voice.formantB.frequency.setTargetAtTime(clamp(primaryFormant * 2.1, 980, 1720), now, 0.03);
    voice.formantBGain.gain.setTargetAtTime(0.14 + state.brightness / 420, now, 0.03);
    voice.airFormant.frequency.setTargetAtTime(clamp(primaryFormant * 3.25, 1700, 2750), now, 0.03);
    voice.airGain.gain.setTargetAtTime(0.045 + state.brightness / 900, now, 0.03);
  }
  refreshVoiceMix(voice);
}

function refreshVoicePressure(voice) {
  const now = audioContext.currentTime;
  const pressure = (state.masterVolume / 100) * currentPressureFactor() * voiceBaseLevel(voice);
  const droneTrim = voice.drone ? Math.max(0.12, state.droneVolume / 100) : 1;
  voice.pressureGain.gain.setTargetAtTime(pressure * droneTrim, now, 0.02);
}

function refreshAllVoices() {
  if (!audioContext) {
    return;
  }

  activeVoices.forEach((voice) => {
    refreshVoiceTone(voice);
    refreshVoicePressure(voice);
  });

  const now = audioContext.currentTime;
  const wet = state.reverbMix / 100;
  if (sampleLibrary.status === "ready") {
    cabinetTone.frequency.setTargetAtTime(3300 + state.brightness * 4.4, now, 0.04);
    cabinetTone.Q.setTargetAtTime(0.34 + wet * 0.18, now, 0.04);
    dryGain.gain.setTargetAtTime(0.98 - wet * 0.14, now, 0.04);
    verbSend.gain.setTargetAtTime(0.004 + wet * 0.12, now, 0.04);
    verbPreDelay.delayTime.setTargetAtTime(0.012 + wet * 0.022, now, 0.04);
    verbTone.frequency.setTargetAtTime(2200 + state.brightness * 11 + wet * 900, now, 0.04);
    verbGain.gain.setTargetAtTime(0.025 + wet * 0.28, now, 0.04);
  } else {
    cabinetTone.frequency.setTargetAtTime(2100 + state.brightness * 16, now, 0.04);
    cabinetTone.Q.setTargetAtTime(0.42 + wet * 0.22, now, 0.04);
    dryGain.gain.setTargetAtTime(0.95 - wet * 0.18, now, 0.04);
    verbSend.gain.setTargetAtTime(0.018 + wet * 0.16 + state.releaseMs / 22000, now, 0.04);
    verbPreDelay.delayTime.setTargetAtTime(0.016 + wet * 0.024, now, 0.04);
    verbTone.frequency.setTargetAtTime(1900 + state.brightness * 9 + wet * 700, now, 0.04);
    verbGain.gain.setTargetAtTime(0.05 + wet * 0.34 + state.releaseMs / 32000, now, 0.04);
  }
  masterOutput.gain.setTargetAtTime(0.45 + state.masterVolume / 210, now, 0.04);
  updateNoiseFloor();
}

function updateNoiseFloor() {
  if (!audioContext || !noiseGain) {
    return;
  }
  if (sampleLibrary.status === "ready") {
    noiseGain.gain.setTargetAtTime(0, audioContext.currentTime, 0.04);
    return;
  }
  const activeCount = state.pressedNotes.size + Object.values(state.drones).filter(Boolean).length;
  const target = activeCount ? 0.002 + (state.currentBellows / 100) * 0.01 : 0;
  noiseGain.gain.setTargetAtTime(target, audioContext.currentTime, 0.06);
}

function clearAiTargets() {
  state.keyLayout.forEach((note) => {
    note.button.classList.remove("is-ai-target", "ai-playing");
  });
}

function buildKeyLayout() {
  const startMidi = (state.baseOctave + 1) * 12;
  let whiteIndex = 0;

  state.keyLayout = KEYBOARD_BINDINGS.map((binding, index) => {
    const midi = startMidi + index;
    const pitchClass = midi % 12;
    const isBlack = BLACK_PITCHES.has(pitchClass);
    const note = {
      index,
      midi,
      pitchClass,
      isBlack,
      noteName: formatNoteName(midi),
      frequency: midiToFrequency(midi),
      sargam: relativeSargam(pitchClass),
      binding,
      whiteIndex: isBlack ? null : whiteIndex,
      blackCenter: isBlack ? whiteIndex - 0.32 : null,
      button: null,
    };
    if (!isBlack) {
      whiteIndex += 1;
    }
    return note;
  });

  const whiteCount = whiteIndex;
  dom.keybed.innerHTML = "";

  state.keyLayout.forEach((note) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `harmonium-key ${note.isBlack ? "black" : "white"}`;
    button.dataset.midi = String(note.midi);
    button.dataset.code = note.binding.code;

    if (note.isBlack) {
      button.style.left = `${(note.blackCenter / whiteCount) * 100}%`;
    } else {
      button.style.left = `${(note.whiteIndex / whiteCount) * 100}%`;
      button.style.width = `${100 / whiteCount}%`;
    }

    button.innerHTML = `
      <span class="key-surface"></span>
      <span class="key-front-face"></span>
      <span class="key-depth-shadow"></span>
      <span class="key-label">
        <span class="label-note">${note.noteName}</span>
        <span class="label-sargam">${note.sargam}</span>
        <span class="label-shortcut">${note.binding.label}</span>
      </span>
    `;

    button.addEventListener("pointerdown", async (event) => {
      event.preventDefault();
      await startNote(note, "pointer");
    });
    button.addEventListener("pointerenter", async (event) => {
      if (event.buttons === 1) {
        await startNote(note, "pointer");
      }
    });
    button.addEventListener("pointerup", () => stopNote(note.midi));
    button.addEventListener("pointerleave", () => stopNote(note.midi));
    button.addEventListener("pointercancel", () => stopNote(note.midi));
    button.addEventListener("contextmenu", (event) => event.preventDefault());

    note.button = button;
    dom.keybed.appendChild(button);
  });

  updateKeyLabels();
}

function updateKeyLabels() {
  dom.keybed.classList.remove("mode-all", "mode-notes", "mode-sargam", "mode-minimal");
  dom.keybed.classList.add(`mode-${state.displayMode}`);

  state.keyLayout.forEach((note) => {
    note.noteName = formatNoteName(note.midi);
    note.sargam = relativeSargam(note.pitchClass);
    note.button.querySelector(".label-note").textContent = note.noteName;
    note.button.querySelector(".label-sargam").textContent = note.sargam;
    note.button.querySelector(".label-shortcut").textContent = note.binding.label;

    const relation = (note.pitchClass - state.rootSemitone + 12) % 12;
    note.button.classList.toggle("is-tonic", relation === 0);
    note.button.classList.toggle("is-dominant", relation === 7);
  });

  updateDroneLabels();
  renderAiPhrase();
}

function updateSliderReadouts() {
  dom.volumeValue.textContent = `${state.masterVolume}%`;
  dom.bellowsTargetValue.textContent = `${state.bellowsTarget}%`;
  dom.brightnessValue.textContent = `${state.brightness}%`;
  dom.attackValue.textContent = `${state.attackMs} ms`;
  dom.releaseValue.textContent = `${state.releaseMs} ms`;
  dom.reverbValue.textContent = `${state.reverbMix}%`;
  dom.droneVolumeValue.textContent = `${state.droneVolume}%`;
  dom.aiLengthValue.textContent = `${state.aiLength} notes`;
  dom.aiOrnamentValue.textContent = `${state.aiOrnament}%`;
  dom.aiPrecisionValue.textContent = `${state.aiPrecision}%`;
}

function syncButtons() {
  dom.stopButtons.forEach((button) => {
    button.classList.toggle("active", Boolean(state.stops[button.dataset.stop]));
  });
  dom.modeButtons.forEach((button) => {
    const mode = button.dataset.mode;
    const enabled = mode === "auto-bellows" ? state.autoBellows : state.coupler;
    button.classList.toggle("active", enabled);
  });
  dom.droneButtons.forEach((button) => {
    button.classList.toggle("active", Boolean(state.drones[button.dataset.drone]));
  });
  dom.presetButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.preset === state.currentPreset);
  });
}

function updateStatusReadout() {
  dom.bellowsLive.textContent = `${Math.round(state.currentBellows)}%`;
  dom.tonicLive.textContent = `Sa = ${NOTE_NAMES[state.rootSemitone]}`;
  dom.registerLive.textContent = registerSummary();
  dom.reverbLive.textContent = state.reverbMix > 0 ? `Bloom ${state.reverbMix}%` : "Dry";
  dom.droneReadout.textContent =
    Object.entries(state.drones)
      .filter(([, enabled]) => enabled)
      .map(([name]) => name.toUpperCase())
      .join(" + ") || "Off";
  dom.pressedCount.textContent = `${state.pressedNotes.size} active`;
}

function droneMidi(name) {
  const anchor = (state.baseOctave + 2) * 12 + state.rootSemitone;
  if (name === "sa") {
    return anchor;
  }
  if (name === "pa") {
    let candidate = Math.floor(anchor / 12) * 12 + ((state.rootSemitone + 7) % 12);
    while (candidate < anchor) {
      candidate += 12;
    }
    return candidate;
  }
  let candidate = Math.floor(anchor / 12) * 12 + ((state.rootSemitone + 11) % 12);
  while (candidate < anchor) {
    candidate += 12;
  }
  return candidate;
}

function updateDroneLabels() {
  ["sa", "pa", "ni"].forEach((name) => {
    dom.droneLabels[name].textContent = formatNoteName(droneMidi(name));
  });
}

function updateNoteReadout(note, source) {
  if (!note) {
    dom.noteReadout.innerHTML = `
      <div class="readout-main">
        <strong>Sa Root Ready</strong>
        <span>Play any key or preview an SNS AI phrase to inspect pitch, Sargam function, and keyboard mapping.</span>
      </div>
    `;
    dom.shortcutReadout.textContent = "Z to I";
    dom.frequencyReadout.textContent = "Idle";
    return;
  }

  dom.noteReadout.innerHTML = `
    <div class="readout-main">
      <strong>${note.noteName} · ${note.sargam}</strong>
      <span>${source} · keyboard ${note.binding.label} · ${registerSummary()}</span>
    </div>
  `;
  dom.shortcutReadout.textContent = note.binding.label;
  dom.frequencyReadout.textContent = `${note.frequency.toFixed(2)} Hz`;
}

function renderMappingSummary() {
  const lower = state.keyLayout.slice(0, 8).map((note) => `${note.binding.label}:${note.noteName}`).join(" ");
  const middle = state.keyLayout.slice(8, 17).map((note) => `${note.binding.label}:${note.noteName}`).join(" ");
  const upper = state.keyLayout.slice(17).map((note) => `${note.binding.label}:${note.noteName}`).join(" ");

  dom.mappingSummary.innerHTML = `
    <div class="mapping-card">
      <strong>Lower Reach</strong>
      <span>${lower}</span>
    </div>
    <div class="mapping-card">
      <strong>Middle Reach</strong>
      <span>${middle}</span>
    </div>
    <div class="mapping-card">
      <strong>Upper Reach</strong>
      <span>${upper}</span>
    </div>
  `;
}

function renderActiveStack() {
  const chips = [];
  state.pressedNotes.forEach((midi) => {
    const note = state.keyLayout.find((item) => item.midi === midi);
    if (note) {
      chips.push(`
        <div class="active-chip">
          <strong>${note.noteName}</strong>
          <span>${note.sargam} · key ${note.binding.label}</span>
        </div>
      `);
    }
  });

  Object.entries(state.drones)
    .filter(([, enabled]) => enabled)
    .forEach(([name]) => {
      chips.push(`
        <div class="active-chip">
          <strong>${name.toUpperCase()} Drone</strong>
          <span>${formatNoteName(droneMidi(name))}</span>
        </div>
      `);
    });

  dom.activeStack.innerHTML = chips.length
    ? chips.join("")
    : "<p class='empty-copy'>No notes are currently pressed.</p>";
}

function createVoiceSignalChain() {
  const mix = audioContext.createGain();
  const bodyLowpass = audioContext.createBiquadFilter();
  const bodyHighpass = audioContext.createBiquadFilter();
  const outputBlend = audioContext.createGain();
  const formantA = audioContext.createBiquadFilter();
  const formantAGain = audioContext.createGain();
  const formantB = audioContext.createBiquadFilter();
  const formantBGain = audioContext.createGain();
  const airFormant = audioContext.createBiquadFilter();
  const airGain = audioContext.createGain();
  const envelope = audioContext.createGain();
  const pressureGain = audioContext.createGain();

  bodyLowpass.type = "lowpass";
  bodyHighpass.type = "highpass";
  formantA.type = "bandpass";
  formantB.type = "bandpass";
  airFormant.type = "bandpass";
  formantA.Q.value = 1.1;
  formantB.Q.value = 1.5;
  airFormant.Q.value = 1.9;
  formantAGain.gain.value = 0;
  formantBGain.gain.value = 0;
  airGain.gain.value = 0;
  envelope.gain.value = 0.0001;
  pressureGain.gain.value = 0;

  mix.connect(bodyLowpass);
  bodyLowpass.connect(bodyHighpass);
  bodyHighpass.connect(outputBlend);
  mix.connect(formantA);
  formantA.connect(formantAGain);
  formantAGain.connect(outputBlend);
  mix.connect(formantB);
  formantB.connect(formantBGain);
  formantBGain.connect(outputBlend);
  mix.connect(airFormant);
  airFormant.connect(airGain);
  airGain.connect(outputBlend);
  outputBlend.connect(envelope);
  envelope.connect(pressureGain);
  pressureGain.connect(masterBus);

  return {
    mix,
    bodyLowpass,
    bodyHighpass,
    formantA,
    formantAGain,
    formantB,
    formantBGain,
    airFormant,
    airGain,
    envelope,
    pressureGain,
  };
}

function finalizeVoiceStart(voice, note, source, trackPressed, drone) {
  const now = audioContext.currentTime;
  activeVoices.set(voice.id, voice);
  refreshVoiceTone(voice);
  refreshVoicePressure(voice);

  voice.envelope.gain.cancelScheduledValues(now);
  voice.envelope.gain.setValueAtTime(0.0001, now);
  voice.envelope.gain.exponentialRampToValueAtTime(voiceBaseLevel(voice), now + state.attackMs / 1000);

  if (trackPressed) {
    state.pressedNotes.add(note.midi);
    if (note.button) {
      note.button.classList.add("active");
    }
  }

  state.lastEvent = { note, source: drone ? `${source} drone` : source };
  updateStatusReadout();
  updateNoteReadout(note, drone ? `${source} drone` : source);
  renderActiveStack();
  updateNoiseFloor();
  return voice;
}

function startSampleVoice(id, note, source, options = {}) {
  const { drone = false, trackPressed = true } = options;
  const now = audioContext.currentTime;
  const nodes = createVoiceSignalChain();
  const sustainLoop = drone;
  const maxStretch = 4.5;
  const bassTargetMidi = resolveRegisterTarget(note.midi, -12, maxStretch);
  const femaleTargetMidi = resolveRegisterTarget(note.midi, 12, maxStretch);
  const couplerTargetMidi = resolveRegisterTarget(note.midi, 12, 3.5);

  const parts = {
    bass: createSamplePart(bassTargetMidi, nodes.mix, {
      detuneCents: -1.4,
      filterType: "lowpass",
      filterFrequency: 540,
      filterQ: 0.44,
      loop: sustainLoop,
      maxStretchSemitones: maxStretch,
      outputTrim: 0.62,
    }),
    male: createSamplePart(note.midi, nodes.mix, {
      detuneCents: 0,
      loop: sustainLoop,
      maxStretchSemitones: maxStretch,
      outputTrim: 1,
    }),
    female: createSamplePart(femaleTargetMidi, nodes.mix, {
      detuneCents: 0.8,
      filterType: "highpass",
      filterFrequency: 760,
      filterQ: 0.48,
      loop: sustainLoop,
      maxStretchSemitones: maxStretch,
      outputTrim: 0.54,
    }),
    coupler: createSamplePart(couplerTargetMidi, nodes.mix, {
      detuneCents: -0.2,
      filterType: "highpass",
      filterFrequency: 680,
      filterQ: 0.42,
      loop: sustainLoop,
      maxStretchSemitones: 3.5,
      outputTrim: couplerTargetMidi === note.midi ? 0.42 : 0.5,
    }),
  };

  Object.values(parts).forEach((part) => {
    if (part) {
      const startOffset = part.anchor.startOffset || 0;
      if (part.source.loop) {
        part.source.start(now, Math.min(startOffset, part.anchor.loopStart));
      } else {
        part.source.start(now, startOffset);
      }
    }
  });

  const voice = {
    id,
    note,
    source,
    drone,
    trackPressed,
    mode: "sample",
    parts,
    ...nodes,
  };

  return finalizeVoiceStart(voice, note, source, trackPressed, drone);
}

function startSynthVoice(id, note, source, options = {}) {
  const { drone = false, trackPressed = true } = options;
  const now = audioContext.currentTime;
  const nodes = createVoiceSignalChain();

  const parts = {
    bass: createOscillatorPart(audioContext, note.frequency / 2, "bass", -6),
    male: createOscillatorPart(audioContext, note.frequency, "male", -4),
    maleBeat: createOscillatorPart(audioContext, note.frequency, "male", 3.5),
    maleShimmer: createOscillatorPart(audioContext, note.frequency, "female", 8),
    female: createOscillatorPart(audioContext, note.frequency * 2, "female", 1.5),
    coupler: createOscillatorPart(audioContext, note.frequency * 2, "female", -3),
  };

  const pitchBloomTargets = {
    bass: -6,
    male: -4,
    maleBeat: 3.5,
    maleShimmer: 8,
    female: 1.5,
    coupler: -3,
  };

  Object.entries(parts).forEach(([name, part]) => {
    part.gain.connect(nodes.mix);
    applyPitchBloom(part, pitchBloomTargets[name]);
    part.oscillator.start(now);
  });

  if (!drone) {
    startAttackNoise(nodes.mix, note);
  }

  const voice = {
    id,
    note,
    source,
    drone,
    trackPressed,
    mode: "synth",
    parts,
    ...nodes,
  };

  return finalizeVoiceStart(voice, note, source, trackPressed, drone);
}

async function startVoice(id, note, source, options = {}) {
  await ensureAudioEngine();
  if (activeVoices.has(id)) {
    return activeVoices.get(id);
  }

  const sampleReady = await ensureSampleLibraryReady();
  if (sampleReady) {
    return startSampleVoice(id, note, source, options);
  }
  return startSynthVoice(id, note, source, options);
}

async function startNote(note, source) {
  await startVoice(`key:${note.midi}`, note, source, { drone: false, trackPressed: true });
}

function releaseVoice(id, releaseMs = null) {
  if (!audioContext || !activeVoices.has(id)) {
    return;
  }

  const voice = activeVoices.get(id);
  const now = audioContext.currentTime;
  const fadeMs = releaseMs ?? state.releaseMs;

  voice.envelope.gain.cancelScheduledValues(now);
  voice.envelope.gain.setValueAtTime(Math.max(0.0001, voice.envelope.gain.value || 0.08), now);
  voice.envelope.gain.exponentialRampToValueAtTime(0.0001, now + fadeMs / 1000);

  window.setTimeout(() => {
    Object.values(voice.parts).forEach((part) => {
      try {
        if (voice.mode === "sample") {
          part.source.stop();
        } else {
          part.oscillator.stop();
        }
      } catch (error) {
        return null;
      }
      return null;
    });
  }, fadeMs + 90);

  activeVoices.delete(id);
  if (voice.trackPressed) {
    state.pressedNotes.delete(voice.note.midi);
    if (voice.note.button) {
      voice.note.button.classList.remove("active");
    }
  }

  updateStatusReadout();
  renderActiveStack();
  updateNoiseFloor();
}

function stopNote(midi) {
  releaseVoice(`key:${midi}`);
}

function cancelAiPreview() {
  state.aiPreviewTimers.forEach((timer) => window.clearTimeout(timer));
  state.aiPreviewTimers = [];
  Array.from(activeVoices.keys())
    .filter((id) => id.startsWith("ai:"))
    .forEach((id) => releaseVoice(id, 80));
  dom.aiPhraseTrack.querySelectorAll(".ai-phrase-chip").forEach((chip) => chip.classList.remove("active"));
  state.keyLayout.forEach((note) => note.button.classList.remove("ai-playing"));
}

function releaseAllVoices() {
  Array.from(activeVoices.keys()).forEach((id) => releaseVoice(id, 140));
  state.pressedNotes.clear();
  state.keyLayout.forEach((note) => note.button.classList.remove("active"));
  updateNoiseFloor();
}

function panicStop() {
  cancelAiPreview();
  releaseAllVoices();
  state.pressedKeyCodes.clear();
  state.drones = { sa: false, pa: false, ni: false };
  state.lastEvent = null;
  updateStatusReadout();
  syncButtons();
  updateNoteReadout(null, "Ready");
  renderActiveStack();
}

async function syncDroneVoices() {
  for (const name of ["sa", "pa", "ni"]) {
    const id = `drone:${name}`;
    if (!state.drones[name]) {
      releaseVoice(id, 120);
      continue;
    }
    const note = noteDescriptorForMidi(droneMidi(name), name.toUpperCase());
    if (activeVoices.has(id)) {
      const voice = activeVoices.get(id);
      voice.note = note;
      refreshVoiceTone(voice);
      refreshVoicePressure(voice);
      continue;
    }
    await startVoice(id, note, name.toUpperCase(), { drone: true, trackPressed: false });
  }
  renderActiveStack();
}

function pumpBellows() {
  state.currentBellows = Math.min(100, state.currentBellows + 14);
  refreshAllVoices();
  updateBellowsVisual();
}

function updateBellowsVisual() {
  const scale = 0.64 + state.currentBellows / 280;
  dom.bellowsVisual.style.setProperty("--pleat-scale", scale.toFixed(3));
  dom.bellowsLive.textContent = `${Math.round(state.currentBellows)}%`;
}

function applyDisplayState() {
  updateSliderReadouts();
  syncButtons();
  updateStatusReadout();
  updateNoteReadout(state.lastEvent?.note || null, state.lastEvent?.source || "Ready");
  renderMappingSummary();
  renderActiveStack();
  renderAiPhrase();
}

function readAiControls() {
  state.aiIntent = dom.aiIntent.value;
  state.aiLength = Number(dom.aiLength.value);
  state.aiOrnament = Number(dom.aiOrnament.value);
  state.aiPrecision = Number(dom.aiPrecision.value);
}

function phraseProfile() {
  return AI_INTENTS[state.aiIntent] || AI_INTENTS.alap;
}

function generateAiPhrase() {
  cancelAiPreview();
  readAiControls();

  const profile = phraseProfile();
  const visibleMin = state.keyLayout[0].midi;
  const visibleMax = state.keyLayout[state.keyLayout.length - 1].midi;
  const anchor = clamp((state.baseOctave + 2) * 12 + state.rootSemitone + profile.anchorOffset, visibleMin + 2, visibleMax - 2);
  const instability = Math.round((100 - state.aiPrecision) / 16);
  const phrase = [];

  for (let i = 0; i < state.aiLength; i += 1) {
    const template = profile.template[i % profile.template.length];
    const alternate = profile.alternate[i % profile.alternate.length];
    const useAlternate = instability > 0 && i % 3 === 1;
    const semitoneOffset = useAlternate ? alternate : template;
    const mainMidi = clamp(anchor + semitoneOffset, visibleMin, visibleMax);
    const mainDescriptor = noteDescriptorForMidi(mainMidi);
    const durationMs = clamp(profile.baseDuration - (i % 2) * 40, 150, 800);

    if (state.aiOrnament > 22 && i % 2 === 0) {
      const graceShift = profile.graceDirection;
      const graceMidi = clamp(mainMidi + graceShift, visibleMin, visibleMax);
      if (graceMidi !== mainMidi) {
        const graceDescriptor = noteDescriptorForMidi(graceMidi);
        phrase.push({
          id: `orn-${i}`,
          midi: graceMidi,
          noteName: graceDescriptor.noteName,
          sargam: graceDescriptor.sargam,
          bindingLabel: graceDescriptor.binding.label,
          durationMs: clamp(80 + state.aiOrnament, 90, 180),
          ornament: true,
        });
      }
    }

    phrase.push({
      id: `main-${i}`,
      midi: mainMidi,
      noteName: mainDescriptor.noteName,
      sargam: mainDescriptor.sargam,
      bindingLabel: mainDescriptor.binding.label,
      durationMs,
      ornament: false,
    });
  }

  state.aiPhrase = phrase;
  dom.aiSummary.textContent = `SNS AI prepared a ${profile.label.toLowerCase()} phrase in ${NOTE_NAMES[state.rootSemitone]} with ${state.aiLength} target notes, ${state.aiPrecision}% precision, and ${state.aiOrnament}% ornament depth.`;
  renderAiPhrase();
}

function renderAiPhrase() {
  clearAiTargets();

  if (!state.aiPhrase.length) {
    dom.aiPhraseTrack.innerHTML = "<p class='empty-copy'>No AI phrase has been generated yet.</p>";
    return;
  }

  const uniqueTargets = new Set(state.aiPhrase.filter((entry) => !entry.ornament).map((entry) => entry.midi));
  state.keyLayout.forEach((note) => {
    note.button.classList.toggle("is-ai-target", uniqueTargets.has(note.midi));
  });

  dom.aiPhraseTrack.innerHTML = state.aiPhrase
    .map(
      (entry, index) => `
        <button class="ai-phrase-chip" type="button" data-ai-index="${index}">
          <strong>${entry.noteName}</strong>
          <span>${entry.ornament ? "ornament" : `${entry.sargam} · key ${entry.bindingLabel}`}</span>
        </button>
      `
    )
    .join("");

  dom.aiPhraseTrack.querySelectorAll(".ai-phrase-chip").forEach((button) => {
    button.addEventListener("click", async () => {
      const entry = state.aiPhrase[Number(button.dataset.aiIndex)];
      if (!entry) {
        return;
      }
      cancelAiPreview();
      await playAiEntry(entry, Number(button.dataset.aiIndex));
    });
  });
}

async function playAiEntry(entry, index) {
  const note = noteDescriptorForMidi(entry.midi, "AI");
  const id = `ai:${Date.now()}:${index}`;
  const chip = dom.aiPhraseTrack.querySelector(`[data-ai-index="${index}"]`);

  if (note.button) {
    note.button.classList.add("ai-playing");
  }
  chip?.classList.add("active");
  await startVoice(id, note, "SNS AI", { drone: false, trackPressed: false });

  const timer = window.setTimeout(() => {
    if (note.button) {
      note.button.classList.remove("ai-playing");
    }
    chip?.classList.remove("active");
    releaseVoice(id, clamp(entry.durationMs * 0.7, 90, 320));
  }, entry.durationMs);
  state.aiPreviewTimers.push(timer);
}

function previewAiPhrase() {
  if (!state.aiPhrase.length) {
    generateAiPhrase();
  }
  cancelAiPreview();

  let offset = 0;
  state.aiPhrase.forEach((entry, index) => {
    const timer = window.setTimeout(() => {
      playAiEntry(entry, index);
    }, offset);
    state.aiPreviewTimers.push(timer);
    offset += Math.max(90, entry.durationMs * 0.82);
  });
}

function applyPreset(name) {
  const preset = PRESETS[name];
  if (!preset) {
    return;
  }

  cancelAiPreview();
  state.currentPreset = name;
  dom.masterVolume.value = String(preset.masterVolume);
  dom.bellowsPressure.value = String(preset.bellowsPressure);
  dom.brightness.value = String(preset.brightness);
  dom.attack.value = String(preset.attack);
  dom.release.value = String(preset.release);
  dom.reverbMix.value = String(preset.reverb);
  dom.droneVolume.value = String(preset.droneVolume);
  dom.aiIntent.value = preset.aiIntent;

  state.masterVolume = preset.masterVolume;
  state.bellowsTarget = preset.bellowsPressure;
  state.currentBellows = Math.max(state.currentBellows, preset.bellowsPressure);
  state.brightness = preset.brightness;
  state.attackMs = preset.attack;
  state.releaseMs = preset.release;
  state.reverbMix = preset.reverb;
  state.droneVolume = preset.droneVolume;
  state.autoBellows = preset.autoBellows;
  state.coupler = preset.coupler;
  state.stops = { ...preset.stops };
  state.aiIntent = preset.aiIntent;

  refreshAllVoices();
  generateAiPhrase();
  applyDisplayState();
  updateBellowsVisual();
}

async function setRootAndLayout() {
  cancelAiPreview();
  releaseAllVoices();
  state.lastEvent = null;
  state.rootSemitone = Number(dom.saRoot.value);
  state.baseOctave = Number(dom.baseOctave.value);
  state.displayMode = dom.displayMode.value;
  buildKeyLayout();
  generateAiPhrase();
  await syncDroneVoices();
  applyDisplayState();
}

function updateContinuousState() {
  state.masterVolume = Number(dom.masterVolume.value);
  state.bellowsTarget = Number(dom.bellowsPressure.value);
  state.brightness = Number(dom.brightness.value);
  state.attackMs = Number(dom.attack.value);
  state.releaseMs = Number(dom.release.value);
  state.reverbMix = Number(dom.reverbMix.value);
  state.droneVolume = Number(dom.droneVolume.value);
  refreshAllVoices();
  applyDisplayState();
  updateBellowsVisual();
}

function bindControls() {
  dom.saRoot.addEventListener("change", setRootAndLayout);
  dom.baseOctave.addEventListener("change", setRootAndLayout);
  dom.displayMode.addEventListener("change", () => {
    state.displayMode = dom.displayMode.value;
    updateKeyLabels();
    applyDisplayState();
  });

  [dom.masterVolume, dom.bellowsPressure, dom.brightness, dom.attack, dom.release, dom.reverbMix, dom.droneVolume].forEach(
    (input) => input.addEventListener("input", updateContinuousState)
  );

  [dom.aiLength, dom.aiOrnament, dom.aiPrecision].forEach((input) => {
    input.addEventListener("input", () => {
      readAiControls();
      updateSliderReadouts();
      generateAiPhrase();
    });
  });
  dom.aiIntent.addEventListener("change", () => {
    readAiControls();
    generateAiPhrase();
    applyDisplayState();
  });

  dom.aiGenerate.addEventListener("click", () => {
    generateAiPhrase();
    applyDisplayState();
  });
  dom.aiPreview.addEventListener("click", previewAiPhrase);

  dom.presetButtons.forEach((button) => {
    button.addEventListener("click", () => applyPreset(button.dataset.preset));
  });

  dom.stopButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.stops[button.dataset.stop] = !state.stops[button.dataset.stop];
      refreshAllVoices();
      applyDisplayState();
    });
  });

  dom.modeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.mode === "auto-bellows") {
        state.autoBellows = !state.autoBellows;
      } else {
        state.coupler = !state.coupler;
      }
      refreshAllVoices();
      applyDisplayState();
    });
  });

  dom.droneButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      state.drones[button.dataset.drone] = !state.drones[button.dataset.drone];
      await syncDroneVoices();
      applyDisplayState();
    });
  });

  dom.pumpBellows.addEventListener("click", pumpBellows);
  dom.panicButton.addEventListener("click", panicStop);

  document.addEventListener("keydown", async (event) => {
    if (event.code === "Backspace") {
      event.preventDefault();
      panicStop();
      return;
    }
    if (event.code === "Space") {
      event.preventDefault();
      if (!state.autoBellows) {
        pumpBellows();
      }
      return;
    }
    if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) {
      return;
    }

    const note = state.keyLayout.find((item) => item.binding.code === event.code);
    if (!note) {
      return;
    }
    if (event.repeat || state.pressedKeyCodes.has(event.code)) {
      return;
    }
    event.preventDefault();
    state.pressedKeyCodes.add(event.code);
    await startNote(note, "keyboard");
  });

  document.addEventListener("keyup", (event) => {
    const note = state.keyLayout.find((item) => item.binding.code === event.code);
    if (!note) {
      return;
    }
    state.pressedKeyCodes.delete(event.code);
    stopNote(note.midi);
  });

  window.addEventListener("blur", panicStop);
}

function animationTick() {
  if (state.autoBellows) {
    const target = state.bellowsTarget + Math.sin(Date.now() / 360) * 3.2;
    state.currentBellows += (target - state.currentBellows) * 0.07;
  } else {
    state.currentBellows = Math.max(0, state.currentBellows - 0.1);
    if (state.currentBellows > state.bellowsTarget) {
      state.currentBellows -= 0.04;
    }
  }

  state.currentBellows = clamp(state.currentBellows, 0, 100);
  refreshAllVoices();
  updateBellowsVisual();
  updateStatusReadout();
  animationHandle = window.requestAnimationFrame(animationTick);
}

function initialize() {
  updateSampleEngineStatus();
  bindControls();
  buildKeyLayout();
  applyPreset(state.currentPreset);
  generateAiPhrase();
  applyDisplayState();
  updateBellowsVisual();
  void ensureAudioEngine().catch(() => null);
  animationHandle = window.requestAnimationFrame(animationTick);
}

initialize();
