const RecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition || null;
const MediaRecorderCtor = window.MediaRecorder || null;
const synth = window.speechSynthesis || null;
const ASSISTANT_API = `${window.location.origin || "http://127.0.0.1:8000"}/api/academy-assistant`;
const TTS_API = `${window.location.origin || "http://127.0.0.1:8000"}/api/academy-tts`;
const STT_API = `${window.location.origin || "http://127.0.0.1:8000"}/api/academy-transcribe`;
const LLM_STATUS_API = `${window.location.origin || "http://127.0.0.1:8000"}/api/academy-llm-status`;

const dom = {
  indicator: document.getElementById("academy-voice-indicator"),
  status: document.getElementById("academy-voice-status"),
  current: document.getElementById("academy-voice-current"),
  heard: document.getElementById("academy-voice-heard"),
  reply: document.getElementById("academy-voice-reply"),
  llmStatus: document.getElementById("academy-llm-status"),
  llmDetail: document.getElementById("academy-llm-detail"),
  llmRefresh: document.getElementById("academy-llm-refresh"),
  enable: document.getElementById("academy-voice-enable"),
  stop: document.getElementById("academy-voice-stop"),
  resume: document.getElementById("academy-voice-continue"),
  restart: document.getElementById("academy-voice-restart"),
  voiceLanguage: document.getElementById("academy-voice-language"),
  ambienceToggle: document.getElementById("academy-ambience-toggle"),
  ambienceVolume: document.getElementById("academy-ambience-volume"),
  ambienceStatus: document.getElementById("academy-ambience-status"),
  chatLog: document.getElementById("academy-chat-log"),
  chatForm: document.getElementById("academy-chat-form"),
  chatInput: document.getElementById("academy-chat-input"),
  chatSend: document.getElementById("academy-chat-send"),
  navLinks: Array.from(document.querySelectorAll(".academy-nav a")),
  sections: Array.from(document.querySelectorAll(".academy-main > .academy-section")),
};

const coachState = {
  enabled: false,
  listening: false,
  speaking: false,
  paused: true,
  awaitingConsent: false,
  recognition: null,
  sections: [],
  currentSectionIndex: 0,
  currentChunkIndex: 0,
  activeSectionIndex: -1,
  speechToken: 0,
  utteranceText: "",
  utteranceStartedAt: 0,
  heardText: "",
  requestToken: 0,
  shouldRestartRecognition: true,
  recognitionRestartTimer: 0,
  recognitionLang: "en-IN",
  replyLanguage: "en-IN",
  voiceStyle: "",
  speechRate: 0.89,
  speechPitch: 0.99,
  chunkPauseMs: 360,
  audioContext: null,
  ambienceEnabled: false,
  ambienceUserVolume: 0.28,
  ambienceMaster: null,
  ambiencePlucks: [],
  ambienceVoices: [],
  ambienceLoopTimer: 0,
  audioPlayer: null,
  activeSpeechUrl: "",
  activeSpeechAbortController: null,
  activeAssistantAbortController: null,
  speechCache: new Map(),
  micStream: null,
  micSource: null,
  micAnalyser: null,
  micLevelBuffer: null,
  micMonitorFrame: 0,
  micSpeechCandidateAt: 0,
  micSpeechLastDetectedAt: 0,
  micRecordingStartedAt: 0,
  mediaRecorder: null,
  mediaChunks: [],
  transcriptionInFlight: false,
  activeTranscriptionAbortController: null,
  serverMicEnabled: false,
  messages: [],
};

function normalizeText(text) {
  return text
    .toLowerCase()
    .replace(/[`'"()[\]{}.,!?/:;\\-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function sentenceChunks(text) {
  const cleaned = text.replace(/\s+/g, " ").replace(/`/g, "").trim();
  if (!cleaned) {
    return [];
  }

  return cleaned
    .split(/(?<=[.!?])\s+/)
    .flatMap((sentence) => {
      const trimmed = sentence.trim();
      if (!trimmed) {
        return [];
      }
      if (trimmed.length <= 320) {
        return [trimmed];
      }
      return trimmed
        .split(/[;:]\s+/)
        .map((part) => part.trim())
        .filter(Boolean);
    });
}

function pushChunks(chunks, text) {
  sentenceChunks(text).forEach((chunk) => chunks.push(chunk));
}

function buildAcademySections() {
  return dom.sections.map((section, index) => {
    const title = section.querySelector(".academy-section__header h2")?.textContent.trim() || `Section ${index + 1}`;
    const eyebrow = section.querySelector(".academy-eyebrow")?.textContent.trim() || `Section ${index + 1}`;
    const chunks = [];
    const aliases = new Set([
      normalizeText(title),
      normalizeText(section.id.replace(/-/g, " ")),
      normalizeText(eyebrow),
      normalizeText(`section ${index + 1}`),
    ]);
    const targets = [];

    pushChunks(chunks, `${eyebrow}. ${title}.`);
    targets.push({ alias: normalizeText(title), label: title, chunkIndex: 0 });

    section
      .querySelectorAll(".academy-path-card, .academy-card, .academy-routine-card, .academy-drill")
      .forEach((card) => {
        const heading = card.querySelector("h3")?.textContent.trim() || "";
        const parts = Array.from(card.querySelectorAll("p, li"))
          .map((node) => node.textContent.trim())
          .filter(Boolean);
        const composed = [heading, ...parts].filter(Boolean).join(". ");
        if (!composed) {
          return;
        }
        const chunkIndex = chunks.length;
        pushChunks(chunks, composed);
        if (heading) {
          const alias = normalizeText(heading);
          aliases.add(alias);
          targets.push({ alias, label: heading, chunkIndex });
        }
      });

    section.querySelectorAll(".academy-callout").forEach((callout) => {
      const strong = callout.querySelector("strong")?.textContent.trim() || "";
      const span = callout.querySelector("span")?.textContent.trim() || "";
      const composed = [strong, span].filter(Boolean).join(". ");
      if (!composed) {
        return;
      }
      pushChunks(chunks, composed);
      if (strong) {
        const alias = normalizeText(strong);
        aliases.add(alias);
        targets.push({ alias, label: strong, chunkIndex: Math.max(0, chunks.length - 1) });
      }
    });

    const headers = Array.from(section.querySelectorAll("thead th")).map((cell) => cell.textContent.trim());
    section.querySelectorAll("tbody tr").forEach((row) => {
      const cells = Array.from(row.querySelectorAll("td")).map((cell) => cell.textContent.trim());
      if (!cells.length) {
        return;
      }
      const rowText = cells
        .map((cell, cellIndex) => `${headers[cellIndex] || `Column ${cellIndex + 1}`}. ${cell}`)
        .join(". ");
      pushChunks(chunks, rowText);
    });

    section.querySelectorAll(".academy-timeline__item").forEach((item) => {
      const strong = item.querySelector("strong")?.textContent.trim() || "";
      const text = item.querySelector("p")?.textContent.trim() || "";
      pushChunks(chunks, [strong, text].filter(Boolean).join(". "));
    });

    section.querySelectorAll(".academy-check").forEach((item) => {
      const text = item.textContent.trim();
      if (!text) {
        return;
      }
      const chunkIndex = chunks.length;
      pushChunks(chunks, text);
      const alias = normalizeText(text);
      aliases.add(alias);
      targets.push({ alias, label: text, chunkIndex });
    });

    return {
      id: section.id,
      index,
      title,
      eyebrow,
      chunks,
      aliases: Array.from(aliases),
      targets,
      element: section,
    };
  });
}

function englishReplyLocale() {
  const selected = coachState.recognitionLang || dom.voiceLanguage?.value || "en-IN";
  return (selected || "").toLowerCase().startsWith("en") ? selected : "en-IN";
}

function effectiveReplyLocale(replyLanguage = coachState.replyLanguage) {
  const normalized = (replyLanguage || "").toLowerCase();
  if (normalized.startsWith("hi")) {
    return "hi-IN";
  }
  if (normalized.startsWith("en")) {
    return replyLanguage.includes("-") ? replyLanguage : englishReplyLocale();
  }
  return englishReplyLocale();
}

function pickVoice(preferredLanguage = effectiveReplyLocale()) {
  if (!synth) {
    return null;
  }
  const voices = synth.getVoices();
  if (!voices.length) {
    return null;
  }

  const wantsHindi = /^hi/i.test(preferredLanguage);
  const preferredNames = wantsHindi
    ? [/lekha/i, /google hindi/i, /hindi/i]
    : [
        /flo/i,
        /veena/i,
        /samantha/i,
        /serena/i,
        /ava/i,
        /allison/i,
        /karen/i,
        /jenny/i,
        /sonia/i,
        /victoria/i,
        /rishi/i,
        /aria/i,
        /daniel/i,
        /google uk english/i,
        /google us english/i,
      ];

  const scored = voices.map((voice) => {
    let score = 0;
    if (wantsHindi) {
      if (/^hi/i.test(voice.lang)) {
        score += 18;
      }
    } else if (/^en-(IN|GB|US)/i.test(voice.lang)) {
      score += 8;
    } else if (/^en/i.test(voice.lang)) {
      score += 4;
    }
    preferredNames.forEach((pattern, index) => {
      if (pattern.test(voice.name)) {
        score += 24 - index;
      }
    });
    if (/female|woman|samantha|veena|victoria|karen|jenny|aria|sonia|serena|flo|lekha/i.test(voice.name)) {
      score += 5;
    }
    if (/premium|enhanced|natural/i.test(voice.name)) {
      score += 6;
    }
    if (voice.localService) {
      score += 3;
    }
    return { voice, score };
  });

  scored.sort((left, right) => right.score - left.score);
  return scored[0]?.voice || voices[0];
}

function setStatus(message) {
  dom.status.textContent = message;
}

function setCurrentLesson(message) {
  dom.current.textContent = message;
}

function setHeard(message) {
  dom.heard.textContent = message;
}

function setReply(message) {
  if (dom.reply) {
    dom.reply.textContent = message;
  }
}

function setLLMStatus(title, detail = "") {
  if (dom.llmStatus) {
    dom.llmStatus.textContent = title;
  }
  if (dom.llmDetail) {
    dom.llmDetail.textContent = detail;
  }
}

function setAmbienceStatus(message) {
  if (dom.ambienceStatus) {
    dom.ambienceStatus.textContent = message;
  }
}

function addChatMessage(role, text) {
  if (!dom.chatLog || !text) {
    return;
  }

  const article = document.createElement("article");
  article.className = `academy-chat__message academy-chat__message--${role}`;

  const speaker = document.createElement("span");
  speaker.className = "academy-chat__speaker";
  speaker.textContent = role === "user" ? "You" : "Assistant";

  const body = document.createElement("p");
  body.textContent = text;

  article.appendChild(speaker);
  article.appendChild(body);
  dom.chatLog.appendChild(article);
  dom.chatLog.scrollTop = dom.chatLog.scrollHeight;

  coachState.messages.push({ role, text });
  if (coachState.messages.length > 40) {
    coachState.messages.shift();
    const firstDynamic = dom.chatLog.querySelector(".academy-chat__message");
    if (firstDynamic && dom.chatLog.children.length > 24) {
      dom.chatLog.removeChild(firstDynamic);
    }
  }
}

function updateIndicator() {
  dom.indicator.classList.toggle("is-live", coachState.listening);
  dom.indicator.classList.toggle("is-speaking", coachState.speaking);

  if (coachState.speaking) {
    dom.indicator.textContent = "Speaking";
    return;
  }
  if (coachState.listening) {
    dom.indicator.textContent = "Mic Live";
    return;
  }
  if (coachState.enabled) {
    dom.indicator.textContent = "Ready";
    return;
  }
  dom.indicator.textContent = "Mic Off";
}

function supportsServerMicrophone() {
  return Boolean(navigator.mediaDevices?.getUserMedia && MediaRecorderCtor);
}

function recorderMimeType() {
  if (!MediaRecorderCtor?.isTypeSupported) {
    return "audio/webm";
  }
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/mp4",
  ];
  return candidates.find((candidate) => MediaRecorderCtor.isTypeSupported(candidate)) || "";
}

function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const chunkSize = 0x8000;
  for (let index = 0; index < bytes.length; index += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(index, index + chunkSize));
  }
  return window.btoa(binary);
}

async function blobToBase64(blob) {
  const buffer = await blob.arrayBuffer();
  return arrayBufferToBase64(buffer);
}

async function requestServerTranscription(blob) {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 10000);
  coachState.activeTranscriptionAbortController = controller;
  const audioBase64 = await blobToBase64(blob);
  try {
    const response = await fetch(STT_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        audio_base64: audioBase64,
        mime_type: blob.type || recorderMimeType() || "audio/webm",
        language: coachState.recognitionLang,
      }),
    });

    if (!response.ok) {
      throw new Error(`Transcription request failed with status ${response.status}`);
    }

    return response.json();
  } finally {
    window.clearTimeout(timeout);
    coachState.activeTranscriptionAbortController = null;
  }
}

function createReedWave(context) {
  const real = new Float32Array([0, 1, 0.48, 0.22, 0.13, 0.08, 0.05]);
  const imag = new Float32Array(real.length);
  return context.createPeriodicWave(real, imag, { disableNormalization: false });
}

function ensureAmbienceEngine() {
  if (coachState.audioContext) {
    return coachState.audioContext;
  }

  const AudioContextCtor = window.AudioContext || window.webkitAudioContext || null;
  if (!AudioContextCtor) {
    setAmbienceStatus("This browser does not support the classical ambience engine.");
    return null;
  }

  const context = new AudioContextCtor();
  const master = context.createGain();
  const toneFilter = context.createBiquadFilter();
  const lowShelf = context.createBiquadFilter();
  const compressor = context.createDynamicsCompressor();

  master.gain.value = 0.0001;
  toneFilter.type = "lowpass";
  toneFilter.frequency.value = 2100;
  toneFilter.Q.value = 0.4;
  lowShelf.type = "lowshelf";
  lowShelf.frequency.value = 210;
  lowShelf.gain.value = 2.2;
  compressor.threshold.value = -28;
  compressor.knee.value = 16;
  compressor.ratio.value = 2.4;
  compressor.attack.value = 0.012;
  compressor.release.value = 0.34;

  master.connect(toneFilter);
  toneFilter.connect(lowShelf);
  lowShelf.connect(compressor);
  compressor.connect(context.destination);

  const wave = createReedWave(context);
  const droneFrequencies = [146.83, 220.0, 293.66];
  const droneVoices = [];

  droneFrequencies.forEach((frequency, index) => {
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    const filter = context.createBiquadFilter();

    oscillator.setPeriodicWave(wave);
    oscillator.frequency.value = frequency;
    oscillator.detune.value = index === 1 ? -3.2 : index === 2 ? 3.8 : 0;

    filter.type = "bandpass";
    filter.frequency.value = index === 0 ? 310 : index === 1 ? 520 : 760;
    filter.Q.value = 0.6;

    gain.gain.value = index === 1 ? 0.06 : 0.045;

    oscillator.connect(filter);
    filter.connect(gain);
    gain.connect(master);
    oscillator.start();

    droneVoices.push({ oscillator, gain, filter });
  });

  coachState.audioContext = context;
  coachState.ambienceMaster = master;
  coachState.ambienceVoices = droneVoices;
  return context;
}

function createPluckFrequencyCycle() {
  return [146.83, 293.66, 220.0, 293.66];
}

function triggerTanpuraPluck(time, frequency, accent = 1) {
  const context = coachState.audioContext;
  const master = coachState.ambienceMaster;
  if (!context || !master) {
    return;
  }

  const wave = createReedWave(context);
  const oscillator = context.createOscillator();
  const shimmer = context.createOscillator();
  const gain = context.createGain();
  const filter = context.createBiquadFilter();

  oscillator.setPeriodicWave(wave);
  oscillator.frequency.setValueAtTime(frequency, time);
  shimmer.type = "triangle";
  shimmer.frequency.setValueAtTime(frequency * 2, time);
  shimmer.detune.setValueAtTime(5, time);

  filter.type = "lowpass";
  filter.frequency.setValueAtTime(1850, time);
  filter.Q.value = 0.35;

  gain.gain.setValueAtTime(0.0001, time);
  gain.gain.linearRampToValueAtTime(0.04 * accent, time + 0.03);
  gain.gain.exponentialRampToValueAtTime(0.0012, time + 2.9);

  oscillator.connect(filter);
  shimmer.connect(filter);
  filter.connect(gain);
  gain.connect(master);

  oscillator.start(time);
  shimmer.start(time);
  oscillator.stop(time + 3.2);
  shimmer.stop(time + 3.2);
}

function scheduleAmbienceLoop() {
  const context = coachState.audioContext;
  if (!context || !coachState.ambienceEnabled) {
    return;
  }

  window.clearTimeout(coachState.ambienceLoopTimer);
  const startTime = context.currentTime + 0.06;
  const cycle = createPluckFrequencyCycle();

  cycle.forEach((frequency, index) => {
    triggerTanpuraPluck(startTime + (index * 1.28), frequency, index === 0 ? 1.15 : 1);
  });

  coachState.ambienceLoopTimer = window.setTimeout(scheduleAmbienceLoop, 5050);
}

function updateAmbienceLevel() {
  const context = coachState.audioContext;
  const master = coachState.ambienceMaster;
  if (!context || !master) {
    return;
  }

  const baseLevel = coachState.ambienceEnabled ? Math.max(0.0001, coachState.ambienceUserVolume) : 0.0001;
  const speakingLevel = coachState.speaking ? baseLevel * 0.24 : baseLevel;
  master.gain.cancelScheduledValues(context.currentTime);
  master.gain.linearRampToValueAtTime(speakingLevel, context.currentTime + 0.22);
}

function setAmbienceEnabled(enabled) {
  const context = ensureAmbienceEngine();
  if (!context) {
    return;
  }

  coachState.ambienceEnabled = enabled;
  if (dom.ambienceToggle) {
    dom.ambienceToggle.textContent = enabled ? "Stop Ambience" : "Start Ambience";
  }

  if (context.state === "suspended") {
    context.resume().catch(() => {});
  }

  if (enabled) {
    scheduleAmbienceLoop();
    setAmbienceStatus("Soft classical ambience is active and will duck beneath the coach voice.");
  } else {
    window.clearTimeout(coachState.ambienceLoopTimer);
    setAmbienceStatus("Background classical ambience is off. You can turn it on manually or ask the coach to play soft classical music.");
  }

  updateAmbienceLevel();
}

function applyAmbienceMode(mode) {
  if (!mode) {
    return;
  }
  if (mode === "off") {
    setAmbienceEnabled(false);
    return;
  }
  if (mode === "soft") {
    coachState.ambienceUserVolume = 0.18;
    if (dom.ambienceVolume) {
      dom.ambienceVolume.value = String(Math.round(coachState.ambienceUserVolume * 100));
    }
    setAmbienceEnabled(true);
    setAmbienceStatus("Classical ambience is active at a very soft level under the voice.");
    return;
  }
  setAmbienceEnabled(true);
}

function stopMicrophoneMonitor() {
  if (coachState.micMonitorFrame) {
    window.cancelAnimationFrame(coachState.micMonitorFrame);
    coachState.micMonitorFrame = 0;
  }
}

function stopMediaRecorderCapture() {
  if (coachState.mediaRecorder && coachState.mediaRecorder.state !== "inactive") {
    coachState.mediaRecorder.stop();
  }
}

function cancelActiveTranscription() {
  if (coachState.activeTranscriptionAbortController) {
    coachState.activeTranscriptionAbortController.abort();
    coachState.activeTranscriptionAbortController = null;
  }
}

function microphoneRms() {
  if (!coachState.micAnalyser || !coachState.micLevelBuffer) {
    return 0;
  }

  coachState.micAnalyser.getFloatTimeDomainData(coachState.micLevelBuffer);
  let sum = 0;
  for (let index = 0; index < coachState.micLevelBuffer.length; index += 1) {
    const sample = coachState.micLevelBuffer[index];
    sum += sample * sample;
  }
  return Math.sqrt(sum / coachState.micLevelBuffer.length);
}

async function submitRecordedUtterance(blob) {
  if (!blob || blob.size < 4096) {
    return;
  }

  coachState.transcriptionInFlight = true;
  setStatus("Listening deeply and converting your speech into a clean transcript.");

  try {
    const payload = await requestServerTranscription(blob);
    const transcript = (payload.text || "").trim();
    const confidence = Number(payload.confidence || 0);
    const alternatives = Array.isArray(payload.alternatives) ? payload.alternatives : [];
    if (!transcript || likelyEcho(transcript)) {
      return;
    }
    if (confidence < 0.46 && !alternatives.length) {
      setStatus("I heard something, but not clearly enough to trust it.");
      setReply("Please say that once more in one clear sentence, or type it below so I can answer properly.");
      return;
    }
    if (coachState.speaking) {
      pauseCoachState();
      setStatus("I heard you and I am listening now.");
      setCurrentLesson("Listening to you");
    }
    setHeard(transcript);
    await handleCommand(transcript, alternatives);
  } catch (error) {
    if (error?.name === "AbortError") {
      if (coachState.enabled) {
        setStatus("Deep listening was interrupted, so the coach is ready to listen again.");
      }
      return;
    }
    coachState.serverMicEnabled = false;
    stopMicrophoneMonitor();
    setStatus("Deep listening transcription was unavailable for that phrase. The assistant is keeping the browser microphone path ready as backup.");
    if (RecognitionCtor && coachState.enabled && !coachState.speaking) {
      if (!coachState.recognition) {
        coachState.recognition = configureRecognition();
      }
      startRecognition();
    }
  } finally {
    coachState.transcriptionInFlight = false;
    if (RecognitionCtor && coachState.enabled && !coachState.speaking) {
      queueRecognitionRestart(120);
    }
  }
}

function beginServerSpeechCapture() {
  if (!coachState.micStream || coachState.mediaRecorder || coachState.transcriptionInFlight) {
    return;
  }

  const mimeType = recorderMimeType();
  coachState.mediaChunks = [];
  coachState.mediaRecorder = mimeType
    ? new MediaRecorderCtor(coachState.micStream, { mimeType })
    : new MediaRecorderCtor(coachState.micStream);
  coachState.micRecordingStartedAt = performance.now();

  coachState.mediaRecorder.ondataavailable = (event) => {
    if (event.data?.size) {
      coachState.mediaChunks.push(event.data);
    }
  };

  coachState.mediaRecorder.onstop = async () => {
    const chunks = coachState.mediaChunks.slice();
    const type = coachState.mediaRecorder?.mimeType || mimeType || "audio/webm";
    coachState.mediaRecorder = null;
    coachState.mediaChunks = [];

    if (!chunks.length || !coachState.enabled) {
      return;
    }
    const blob = new Blob(chunks, { type });
    await submitRecordedUtterance(blob);
  };

  coachState.mediaRecorder.start(180);
  coachState.micSpeechLastDetectedAt = performance.now();
}

function monitorServerMicrophone() {
  if (!coachState.enabled || !coachState.serverMicEnabled) {
    stopMicrophoneMonitor();
    return;
  }

  if (coachState.recognition && !coachState.speaking && !coachState.mediaRecorder && !coachState.transcriptionInFlight) {
    if (coachState.mediaRecorder && coachState.mediaRecorder.state !== "inactive") {
      stopMediaRecorderCapture();
    }
    coachState.micSpeechCandidateAt = 0;
    coachState.micMonitorFrame = window.requestAnimationFrame(monitorServerMicrophone);
    return;
  }

  const rms = microphoneRms();
  const now = performance.now();
  const speakingNow = coachState.speaking;
  const startThreshold = speakingNow ? 0.042 : 0.018;
  const stopSilenceMs = speakingNow ? 320 : 560;
  const activationMs = speakingNow ? 95 : 80;
  const maxCaptureMs = speakingNow ? 1800 : 2800;

  if (!coachState.transcriptionInFlight && rms > startThreshold) {
    if (!coachState.micSpeechCandidateAt) {
      coachState.micSpeechCandidateAt = now;
    }
    coachState.micSpeechLastDetectedAt = now;
    if (!coachState.mediaRecorder && now - coachState.micSpeechCandidateAt >= activationMs) {
      beginServerSpeechCapture();
      if (speakingNow) {
        coachState.paused = true;
        coachState.awaitingConsent = false;
        coachState.speechToken += 1;
        coachState.speaking = false;
        abortActiveAssistantRequest();
        stopServerSpeech();
        if (synth) {
          synth.cancel();
        }
        setStatus("I heard you. Listening now.");
        setCurrentLesson("Listening to you");
        updateIndicator();
        updateAmbienceLevel();
      }
    }
  } else {
    coachState.micSpeechCandidateAt = 0;
  }

  if (
    coachState.mediaRecorder &&
    coachState.mediaRecorder.state !== "inactive" &&
    now - coachState.micSpeechLastDetectedAt >= stopSilenceMs
  ) {
    stopMediaRecorderCapture();
  }
  if (
    coachState.mediaRecorder &&
    coachState.mediaRecorder.state !== "inactive" &&
    now - coachState.micRecordingStartedAt >= maxCaptureMs
  ) {
    stopMediaRecorderCapture();
  }

  coachState.listening = coachState.enabled && (coachState.serverMicEnabled || !coachState.speaking);
  updateIndicator();
  coachState.micMonitorFrame = window.requestAnimationFrame(monitorServerMicrophone);
}

async function ensureServerMicrophonePipeline() {
  if (!supportsServerMicrophone()) {
    return false;
  }

  if (!coachState.micStream) {
    coachState.micStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        channelCount: 1,
      },
    });
  }

  const context = ensureAmbienceEngine();
  if (!context) {
    return false;
  }

  if (context.state === "suspended") {
    await context.resume().catch(() => {});
  }

  if (!coachState.micSource) {
    coachState.micSource = context.createMediaStreamSource(coachState.micStream);
    coachState.micAnalyser = context.createAnalyser();
    coachState.micAnalyser.fftSize = 2048;
    coachState.micAnalyser.smoothingTimeConstant = 0.18;
    coachState.micLevelBuffer = new Float32Array(coachState.micAnalyser.fftSize);
    coachState.micSource.connect(coachState.micAnalyser);
  }

  coachState.serverMicEnabled = true;
  stopMicrophoneMonitor();
  monitorServerMicrophone();
  return true;
}

function focusSection(index, shouldScroll = false) {
  coachState.activeSectionIndex = index;
  dom.sections.forEach((section, sectionIndex) => {
    section.classList.toggle("is-current", sectionIndex === index);
  });
  dom.navLinks.forEach((link) => {
    link.classList.toggle("is-current", link.getAttribute("href") === `#${coachState.sections[index]?.id || ""}`);
  });

  const section = coachState.sections[index];
  if (shouldScroll && section?.element) {
    section.element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function likelyEcho(command) {
  const normalized = normalizeText(command);
  if (!normalized || normalized.split(" ").length <= 3) {
    return false;
  }
  const currentUtterance = coachState.utteranceText;
  if (!currentUtterance) {
    return false;
  }
  const spoken = normalizeText(currentUtterance);
  if (!spoken) {
    return false;
  }
  const words = normalized.split(" ");
  const overlap = words.filter((word) => spoken.includes(word)).length / Math.max(words.length, 1);
  const recent = Date.now() - coachState.utteranceStartedAt < 4500;
  return recent && overlap > 0.65;
}

function stopRecognitionForSpeech() {
  if (!coachState.recognition) {
    return;
  }
  coachState.shouldRestartRecognition = false;
  window.clearTimeout(coachState.recognitionRestartTimer);
  if (coachState.listening) {
    try {
      coachState.recognition.stop();
    } catch (error) {
      // Ignore stop races from the Web Speech API.
    }
  }
}

function queueRecognitionRestart(delayMs = 420) {
  if (!coachState.enabled || !coachState.recognition) {
    return;
  }
  coachState.shouldRestartRecognition = true;
  window.clearTimeout(coachState.recognitionRestartTimer);
  coachState.recognitionRestartTimer = window.setTimeout(() => {
    if (!coachState.speaking && coachState.enabled) {
      startRecognition();
    }
  }, delayMs);
}

function applyVoiceStyle(style) {
  if (style === "sweet") {
    coachState.speechRate = 0.87;
    coachState.speechPitch = 1.0;
    coachState.chunkPauseMs = 520;
    return;
  }
  if (style === "calm") {
    coachState.speechRate = 0.85;
    coachState.speechPitch = 0.98;
    coachState.chunkPauseMs = 500;
    return;
  }
  if (style === "clear") {
    coachState.speechRate = 0.84;
    coachState.speechPitch = 0.99;
    coachState.chunkPauseMs = 540;
    return;
  }
  if (style === "brisk") {
    coachState.speechRate = 0.95;
    coachState.speechPitch = 1.0;
    coachState.chunkPauseMs = 260;
    return;
  }
  coachState.speechRate = 0.88;
  coachState.speechPitch = 0.99;
  coachState.chunkPauseMs = 480;
}

function clearSpeechObjectUrl() {
  if (coachState.activeSpeechUrl) {
    URL.revokeObjectURL(coachState.activeSpeechUrl);
    coachState.activeSpeechUrl = "";
  }
}

function resetAudioPlaybackOnly() {
  if (coachState.audioPlayer) {
    coachState.audioPlayer.pause();
    coachState.audioPlayer.removeAttribute("src");
    coachState.audioPlayer.load();
  }
  clearSpeechObjectUrl();
}

function stopServerSpeech() {
  if (coachState.activeSpeechAbortController) {
    coachState.activeSpeechAbortController.abort();
    coachState.activeSpeechAbortController = null;
  }
  resetAudioPlaybackOnly();
}

async function requestSpeechAudio(text, replyLanguage, voiceStyle) {
  const cacheKey = `${replyLanguage}|${voiceStyle || "default"}|${text}`;
  if (coachState.speechCache.has(cacheKey)) {
    return coachState.speechCache.get(cacheKey);
  }

  const controller = new AbortController();
  coachState.activeSpeechAbortController = controller;
  const response = await fetch(TTS_API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    signal: controller.signal,
    body: JSON.stringify({
      text,
      language: replyLanguage,
      voice_style: voiceStyle || "",
    }),
  });

  if (!response.ok) {
    throw new Error(`Speech request failed with status ${response.status}`);
  }

  const blob = await response.blob();
  coachState.speechCache.set(cacheKey, blob);
  if (coachState.speechCache.size > 32) {
    const firstKey = coachState.speechCache.keys().next().value;
    coachState.speechCache.delete(firstKey);
  }
  return blob;
}

function playSpeechBlob(blob, token, onfinish) {
  return new Promise((resolve) => {
    if (!(blob instanceof Blob) || token !== coachState.speechToken) {
      resolve(false);
      return;
    }

    if (!coachState.audioPlayer) {
      coachState.audioPlayer = new Audio();
      coachState.audioPlayer.preload = "auto";
    }

    resetAudioPlaybackOnly();
    const audio = coachState.audioPlayer;
    const objectUrl = URL.createObjectURL(blob);
    coachState.activeSpeechUrl = objectUrl;

    const finish = (played) => {
      audio.onended = null;
      audio.onerror = null;
      coachState.activeSpeechAbortController = null;
      clearSpeechObjectUrl();
      resolve(played);
    };

    audio.onended = () => {
      if (token === coachState.speechToken) {
        onfinish();
      }
      finish(true);
    };
    audio.onerror = () => finish(false);
    audio.src = objectUrl;

    audio.play()
      .then(() => {})
      .catch(() => finish(false));
  });
}

async function playSpeechChunks(text, token, onfinish) {
  const chunks = sentenceChunks(text);
  if (!chunks.length) {
    return false;
  }

  const replyLanguage = effectiveReplyLocale();
  const voiceStyle = coachState.voiceStyle || "";
  let currentIndex = 0;
  let currentBlobPromise = requestSpeechAudio(chunks[0], replyLanguage, voiceStyle);

  while (currentIndex < chunks.length) {
    if (token !== coachState.speechToken) {
      return true;
    }

    const remainingText = chunks.slice(currentIndex).join(" ");
    let blob = null;
    try {
      blob = await currentBlobPromise;
    } catch (error) {
      if (token !== coachState.speechToken) {
        return true;
      }
      speakWithBrowserVoice(remainingText, token, onfinish);
      return true;
    }

    if (!(blob instanceof Blob)) {
      speakWithBrowserVoice(remainingText, token, onfinish);
      return true;
    }

    const nextIndex = currentIndex + 1;
    const nextBlobPromise = nextIndex < chunks.length
      ? requestSpeechAudio(chunks[nextIndex], replyLanguage, voiceStyle)
      : null;

    const isLastChunk = nextIndex >= chunks.length;
    const played = await playSpeechBlob(blob, token, isLastChunk ? onfinish : () => {});
    if (!played) {
      if (token !== coachState.speechToken) {
        return true;
      }
      speakWithBrowserVoice(remainingText, token, onfinish);
      return true;
    }

    currentIndex = nextIndex;
    currentBlobPromise = nextBlobPromise;
  }

  return true;
}

function speakWithBrowserVoice(text, token, onfinish) {
  if (!synth || !text) {
    onfinish();
    return;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  const locale = effectiveReplyLocale();
  const voice = pickVoice(locale);
  if (voice) {
    utterance.voice = voice;
    utterance.lang = voice.lang;
  } else {
    utterance.lang = locale;
  }
  utterance.rate = coachState.speechRate;
  utterance.pitch = coachState.speechPitch;
  utterance.volume = 0.98;

  utterance.onend = () => {
    if (token === coachState.speechToken) {
      onfinish();
    }
  };

  utterance.onerror = () => {
    if (token === coachState.speechToken) {
      onfinish();
    }
  };

  synth.cancel();
  synth.speak(utterance);
}

function speak(text, onend = null) {
  if (!text) {
    if (onend) {
      onend();
    }
    return;
  }

  coachState.speechToken += 1;
  const token = coachState.speechToken;
  coachState.speaking = true;
  coachState.utteranceText = text;
  coachState.utteranceStartedAt = Date.now();
  stopRecognitionForSpeech();
  updateIndicator();
  updateAmbienceLevel();

  const finish = () => {
    if (token !== coachState.speechToken) {
      return;
    }
    coachState.activeSpeechAbortController = null;
    coachState.speaking = false;
    updateIndicator();
    updateAmbienceLevel();
    queueRecognitionRestart();
    if (onend) {
      onend();
    }
  };

  void (async () => {
    try {
      const played = await playSpeechChunks(text, token, finish);
      if (played) {
        return;
      }
    } catch (error) {
      // Fall back to browser speech synthesis below.
    }

    if (token !== coachState.speechToken) {
      return;
    }
    speakWithBrowserVoice(text, token, finish);
  })();
}

function pauseCoachState() {
  coachState.paused = true;
  coachState.awaitingConsent = false;
  coachState.speechToken += 1;
  coachState.speaking = false;
  abortActiveAssistantRequest();
  cancelActiveTranscription();
  stopServerSpeech();
  if (synth) {
    synth.cancel();
  }
  updateIndicator();
  updateAmbienceLevel();
}

function respondLocally(text, onend = null) {
  setReply(text);
  addChatMessage("assistant", text);
  speak(text, onend);
}

function stopExplanation(spokenReply = true) {
  pauseCoachState();
  setStatus("Voice coach paused. Say continue whenever you want to resume from the same lesson point.");
  if (spokenReply) {
    respondLocally("Stopping here. Say continue whenever you want, and I will resume from the same part.");
  } else {
    queueRecognitionRestart(180);
  }
}

function explanationFinished() {
  coachState.paused = true;
  coachState.awaitingConsent = false;
  setStatus("Full academy explanation completed. Say from beginning, continue, or name any lesson title to hear it again.");
  setCurrentLesson("Training complete");
  respondLocally("We have completed the full training guide. Say from beginning, continue, or explain any lesson title if you want another pass.");
}

function speakCurrentChunk() {
  if (coachState.paused) {
    return;
  }

  const section = coachState.sections[coachState.currentSectionIndex];
  if (!section) {
    explanationFinished();
    return;
  }

  if (coachState.currentChunkIndex >= section.chunks.length) {
    coachState.currentSectionIndex += 1;
    coachState.currentChunkIndex = 0;
    speakCurrentChunk();
    return;
  }

  focusSection(coachState.currentSectionIndex, coachState.activeSectionIndex !== coachState.currentSectionIndex);
  setCurrentLesson(`${section.title} · Part ${coachState.currentChunkIndex + 1} of ${section.chunks.length}`);
  setStatus(`Explaining ${section.title}. You can ask questions naturally, say stop, continue, repeat that, or jump to another lesson.`);

  const chunk = section.chunks[coachState.currentChunkIndex];
  speak(chunk, () => {
    if (coachState.paused) {
      return;
    }
    coachState.currentChunkIndex += 1;
    window.setTimeout(() => speakCurrentChunk(), coachState.chunkPauseMs);
  });
}

function startExplanationFrom(sectionIndex, chunkIndex = 0, intro = "") {
  coachState.currentSectionIndex = Math.max(0, Math.min(sectionIndex, coachState.sections.length - 1));
  coachState.currentChunkIndex = Math.max(0, chunkIndex);
  coachState.awaitingConsent = false;
  coachState.paused = false;
  focusSection(coachState.currentSectionIndex, true);

  if (intro) {
    speak(intro, () => {
      if (!coachState.paused) {
        speakCurrentChunk();
      }
    });
    return;
  }

  speakCurrentChunk();
}

function resumeExplanation() {
  if (!coachState.enabled) {
    enableVoiceCoach();
    return;
  }

  if (!coachState.paused && coachState.speaking) {
    setStatus("Voice coach is already explaining. Say stop if you want it to pause.");
    return;
  }

  const section = coachState.sections[coachState.currentSectionIndex];
  const intro = section
    ? `Continuing from ${section.title}.`
    : "Continuing the training from where we paused.";
  coachState.paused = false;
  coachState.awaitingConsent = false;
  speak(intro, () => {
    if (!coachState.paused) {
      speakCurrentChunk();
    }
  });
}

function restartFromBeginning() {
  startExplanationFrom(0, 0, "Starting again from the beginning of the training.");
}

function findTarget(command) {
  let bestMatch = null;

  coachState.sections.forEach((section, index) => {
    const sectionNumberAlias = `section ${index + 1}`;
    if (command.includes(sectionNumberAlias)) {
      bestMatch = { sectionIndex: index, chunkIndex: 0, label: section.title, score: 10000 };
    }

    section.targets.forEach((target) => {
      const alias = target.alias;
      if (!alias) {
        return;
      }
      let score = 0;
      if (command.includes(alias)) {
        score = alias.length;
      } else {
        const words = alias.split(" ").filter(Boolean);
        if (words.length > 1 && words.every((word) => command.includes(word))) {
          score = words.join(" ").length - 2;
        }
      }
      if (!score) {
        return;
      }
      if (!bestMatch || score > bestMatch.score) {
        bestMatch = { sectionIndex: index, chunkIndex: target.chunkIndex, label: target.label, score };
      }
    });

    section.aliases.forEach((alias) => {
      if (!alias) {
        return;
      }
      let score = 0;
      if (command.includes(alias)) {
        score = alias.length;
      } else {
        const words = alias.split(" ").filter(Boolean);
        if (words.length > 1 && words.every((word) => command.includes(word))) {
          score = words.join(" ").length - 3;
        }
      }
      if (!score) {
        return;
      }
      if (!bestMatch || score > bestMatch.score) {
        bestMatch = { sectionIndex: index, chunkIndex: 0, label: section.title, score };
      }
    });
  });

  return bestMatch;
}

function fallbackHandleCommand(rawText) {
  const transcript = rawText.trim();
  if (!transcript) {
    return;
  }

  setHeard(transcript);
  const command = normalizeText(transcript);
  if (!command || likelyEcho(command)) {
    return;
  }

  if (command === "listen" || command === "listen to me" || command === "hear me out") {
    pauseCoachState();
    setStatus("I am listening now. Go ahead.");
    respondLocally("I am listening now. Go ahead.");
    return;
  }

  if (command.includes("stop") || command.includes("pause")) {
    stopExplanation();
    return;
  }

  if (
    command.includes("from beginning") ||
    command.includes("from start") ||
    command.includes("from starting") ||
    command.includes("start from beginning") ||
    command.includes("restart")
  ) {
    restartFromBeginning();
    return;
  }

  if (command.includes("continue") || command.includes("resume")) {
    resumeExplanation();
    return;
  }

  if (command.includes("background music") || command.includes("classical music")) {
    if (command.includes("off") || command.includes("stop")) {
      applyAmbienceMode("off");
      respondLocally("I have turned the background music off.");
      return;
    }
    applyAmbienceMode(command.includes("soft") || command.includes("low") ? "soft" : "on");
    respondLocally("I have started the calm classical ambience beneath the lesson.");
    return;
  }

  const target = findTarget(command);
  if (target && (command.includes("explain") || command.includes("go to") || command.includes("start from") || command.includes("teach") || command.includes("from") || command.includes("section"))) {
    startExplanationFrom(
      target.sectionIndex,
      target.chunkIndex,
      `Let's go to ${target.label}. I will start explaining from there.`
    );
    return;
  }

  if (coachState.awaitingConsent) {
    if (command.includes("yes") || command.includes("yeah") || command.includes("start") || command.includes("okay")) {
      startExplanationFrom(0, 0, "Beautiful. Let's begin with the training path.");
      return;
    }
    if (command.includes("no") || command.includes("not now") || command.includes("later")) {
      coachState.awaitingConsent = false;
      coachState.paused = true;
      setStatus("Voice coach is waiting. Say continue or name a lesson title whenever you want to begin.");
      respondLocally("No problem. I will stay ready. Say continue whenever you want me to begin, or name any lesson title.");
      return;
    }
  }

  if ((command.includes("yes") || command.includes("start")) && coachState.paused) {
    resumeExplanation();
    return;
  }

  setStatus("I did not get a reliable live understanding of that question yet.");
  respondLocally(
    "I want to answer that properly, but I did not get a reliable understanding just now. Please say it again in one clear sentence, or type it below and I will answer directly."
  );
}

function assistantStatePayload() {
  return {
    enabled: coachState.enabled,
    paused: coachState.paused,
    awaiting_consent: coachState.awaitingConsent,
    current_section_index: coachState.currentSectionIndex,
    current_chunk_index: coachState.currentChunkIndex,
    reply_language: coachState.replyLanguage,
  };
}

function assistantSectionsPayload() {
  return coachState.sections.map((section) => ({
    id: section.id,
    title: section.title,
    eyebrow: section.eyebrow,
    chunks: section.chunks,
    aliases: section.aliases,
    targets: section.targets.map((target) => ({
      alias: target.alias,
      label: target.label,
      chunkIndex: target.chunkIndex,
    })),
  }));
}

function assistantHistoryPayload() {
  return coachState.messages.slice(-12).map((message) => ({
    role: message.role,
    text: message.text,
  }));
}

function abortActiveAssistantRequest() {
  if (coachState.activeAssistantAbortController) {
    coachState.activeAssistantAbortController.abort();
    coachState.activeAssistantAbortController = null;
  }
}

async function requestAssistantDecision(utterance, alternatives = []) {
  for (let attempt = 0; attempt < 2; attempt += 1) {
    const controller = new AbortController();
    coachState.activeAssistantAbortController = controller;
    const timeout = window.setTimeout(() => controller.abort(), attempt === 0 ? 12000 : 18000);
    try {
      const response = await fetch(ASSISTANT_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: controller.signal,
        body: JSON.stringify({
          utterance,
          alternatives,
          language: coachState.recognitionLang,
          state: assistantStatePayload(),
          sections: assistantSectionsPayload(),
          history: assistantHistoryPayload(),
        }),
      });

      if (!response.ok) {
        if (attempt === 0 && (response.status === 503 || response.status === 504)) {
          await new Promise((resolve) => window.setTimeout(resolve, 450));
          continue;
        }
        throw new Error(`Assistant request failed with status ${response.status}`);
      }

      return response.json();
    } catch (error) {
      if (attempt === 0 && (error?.name === "AbortError" || /failed to fetch/i.test(String(error?.message || error)))) {
        await new Promise((resolve) => window.setTimeout(resolve, 350));
        continue;
      }
      throw error;
    } finally {
      if (coachState.activeAssistantAbortController === controller) {
        coachState.activeAssistantAbortController = null;
      }
      window.clearTimeout(timeout);
    }
  }

  throw new Error("Assistant request did not complete.");
}

async function refreshLLMStatus() {
  setLLMStatus(
    "Checking language model availability",
    "The academy is checking whether a real local or configured language model is active."
  );
  try {
    const response = await fetch(LLM_STATUS_API, { headers: { Accept: "application/json" } });
    if (!response.ok) {
      throw new Error(`LLM status failed with ${response.status}`);
    }
    const payload = await response.json();
    const providerName = payload.provider && payload.provider !== "none" ? String(payload.provider) : "fallback intelligence";
    const title = payload.available
      ? `Real LLM Active · ${providerName} · ${payload.model || "academy model"}`
      : `Real LLM Not Active · ${providerName}`;
    const detail = payload.command_hint
      ? `${payload.detail} Suggested setup: ${payload.command_hint}`
      : (payload.detail || "No language model status details were returned.");
    setLLMStatus(title, detail);
  } catch (error) {
    setLLMStatus(
      "Language model status unavailable",
      "The academy could not read the LLM status right now, but the assistant can still use its fallback path."
    );
  }
}

function applyAssistantDecision(decision) {
  applyVoiceStyle(decision.voice_style || "");
  coachState.voiceStyle = decision.voice_style || "";
  coachState.replyLanguage = (decision.reply_language || "").toLowerCase().startsWith("hi")
    ? "hi-IN"
    : effectiveReplyLocale("en-IN");
  applyAmbienceMode(decision.ambience_mode || "");
  setReply(decision.reply || "The assistant is ready.");
  addChatMessage("assistant", decision.reply || "The assistant is ready.");

  if (typeof decision.section_index === "number") {
    focusSection(decision.section_index, true);
  }

  if (decision.focus_label) {
    setCurrentLesson(decision.focus_label);
  }

  switch (decision.action) {
    case "pause":
      stopExplanation(false);
      speak(decision.reply);
      return;
    case "wait":
      pauseCoachState();
      setStatus("Voice coach is waiting. Say continue or ask for any lesson when you are ready.");
      speak(decision.reply);
      return;
    case "restart":
    case "start":
    case "jump":
      if (decision.should_continue) {
        startExplanationFrom(decision.section_index ?? 0, decision.chunk_index ?? 0, decision.reply);
      } else {
        coachState.currentSectionIndex = decision.section_index ?? coachState.currentSectionIndex;
        coachState.currentChunkIndex = decision.chunk_index ?? coachState.currentChunkIndex;
        coachState.paused = true;
        coachState.awaitingConsent = false;
        speak(decision.reply);
      }
      return;
    case "resume":
      coachState.currentSectionIndex = decision.section_index ?? coachState.currentSectionIndex;
      coachState.currentChunkIndex = decision.chunk_index ?? coachState.currentChunkIndex;
      coachState.paused = false;
      coachState.awaitingConsent = false;
      speak(decision.reply, () => {
        if (decision.should_continue && !coachState.paused) {
          speakCurrentChunk();
        }
      });
      return;
    case "repeat":
      coachState.currentSectionIndex = decision.section_index ?? coachState.currentSectionIndex;
      coachState.currentChunkIndex = decision.chunk_index ?? coachState.currentChunkIndex;
      coachState.paused = false;
      speak(decision.reply, () => {
        if (!coachState.paused) {
          speakCurrentChunk();
        }
      });
      return;
    case "answer":
    default:
      setStatus("Voice coach understood your question and is responding.");
      speak(decision.reply, () => {
        if (decision.should_continue) {
          coachState.currentSectionIndex = decision.section_index ?? coachState.currentSectionIndex;
          coachState.currentChunkIndex = decision.chunk_index ?? coachState.currentChunkIndex;
          coachState.paused = false;
          speakCurrentChunk();
        } else {
          coachState.paused = true;
        }
      });
  }
}

async function submitAssistantQuery(rawText, source = "voice", alternatives = []) {
  const transcript = rawText.trim();
  if (!transcript) {
    return;
  }

  if (source === "voice") {
    setHeard(transcript);
  }
  const command = normalizeText(transcript);
  if (!command || likelyEcho(command)) {
    return;
  }
  addChatMessage("user", transcript);

  const requestToken = coachState.requestToken + 1;
  coachState.requestToken = requestToken;
  abortActiveAssistantRequest();
  setStatus("Understanding your request and preparing the right response.");
  setReply("Thinking about your request and preparing an answer.");

  try {
    const decision = await requestAssistantDecision(transcript, alternatives);
    if (requestToken !== coachState.requestToken) {
      return;
    }
    applyAssistantDecision(decision);
  } catch (error) {
    setStatus("The advanced language assistant had trouble with that turn. I am falling back only for simple controls so I do not give you a wrong answer.");
    setReply("The live assistant request did not finish cleanly, so I will only use the safe control fallback for this turn.");
    fallbackHandleCommand(transcript);
  }
}

async function handleCommand(rawText, alternatives = []) {
  return submitAssistantQuery(rawText, "voice", alternatives);
}

function startRecognition() {
  if (!coachState.enabled || !coachState.recognition || coachState.speaking) {
    return;
  }

  try {
    coachState.recognition.start();
  } catch (error) {
    if (!/start/i.test(String(error.message || error))) {
      setStatus("Voice coach could not start microphone listening. Please allow microphone access and try again.");
    }
  }
}

function configureRecognition() {
  if (!RecognitionCtor) {
    return null;
  }

  const recognition = new RecognitionCtor();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = coachState.recognitionLang;
  recognition.maxAlternatives = 3;

  recognition.onstart = () => {
    coachState.listening = true;
    updateIndicator();
    if (!coachState.awaitingConsent && coachState.paused) {
      setStatus("Microphone is live. Ask naturally for any lesson, say continue, stop, repeat that, or jump anywhere.");
    }
  };

  recognition.onend = () => {
    coachState.listening = false;
    updateIndicator();
    if (coachState.enabled && coachState.shouldRestartRecognition && !coachState.speaking) {
      window.setTimeout(startRecognition, 260);
    }
  };

  recognition.onerror = (event) => {
    coachState.listening = false;
    updateIndicator();
    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      coachState.enabled = false;
      setStatus("Microphone permission was denied. Please allow microphone access and enable the voice coach again.");
      return;
    }
    if (event.error === "no-speech" || event.error === "aborted") {
      return;
    }
    setStatus(`Voice coach microphone issue: ${event.error}. It will keep trying to listen.`);
  };

  recognition.onresult = (event) => {
    let heardFinal = "";
    let heardInterim = "";
    let heardAlternatives = [];

    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const result = event.results[index];
      const transcript = result[0]?.transcript?.trim() || "";
      if (!transcript) {
        continue;
      }
      if (result.isFinal) {
        heardFinal += `${transcript} `;
        heardAlternatives = [];
        for (let altIndex = 0; altIndex < Math.min(result.length, 3); altIndex += 1) {
          const alternative = result[altIndex]?.transcript?.trim() || "";
          if (alternative) {
            heardAlternatives.push(alternative);
          }
        }
      } else {
        heardInterim += `${transcript} `;
      }
    }

    if (heardInterim.trim()) {
      setHeard(`Listening: ${heardInterim.trim()}`);
    }

    if (heardFinal.trim()) {
      handleCommand(heardFinal.trim(), heardAlternatives);
    }
  };

  return recognition;
}

function enableVoiceCoach() {
  coachState.enabled = true;
  coachState.paused = true;
  coachState.awaitingConsent = true;
  coachState.shouldRestartRecognition = true;
  coachState.replyLanguage = effectiveReplyLocale(coachState.recognitionLang);
  coachState.voiceStyle = "calm";
  applyVoiceStyle("calm");
  ensureAmbienceEngine();
  dom.enable.textContent = "Voice Coach Active";
  setCurrentLesson("Awaiting your answer");
  setStatus("Voice coach enabled. It is preparing the strongest listening mode available.");
  setHeard("Microphone active. Waiting for your answer.");

  const greeting = coachState.replyLanguage.toLowerCase().startsWith("hi")
    ? "नमस्ते। मैं आपकी सत्यम् संगीत वॉइस कोच हूँ। क्या मैं प्रशिक्षण समझाना शुरू करूँ? आप हाँ कह सकते हैं, या फिंगरिंग, बेलोज़, संगत, अभ्यास दिनचर्या, या किसी भी सामान्य जानकारी के बारे में पूछ सकते हैं।"
    : "Hello. I am your Satya Sangeet voice coach. Should I start explaining how to go with the training? You can say yes to begin, or ask for any lesson such as fingering, bellows, accompaniment, professional routine, or any outside question you want to know.";

  void (async () => {
    try {
      const serverMicReady = await ensureServerMicrophonePipeline();
      if (RecognitionCtor) {
        if (!coachState.recognition) {
          coachState.recognition = configureRecognition();
        }
        startRecognition();
        if (serverMicReady) {
          setStatus("Hybrid listening mode is active. Fast browser speech handles normal listening, and deep listening stays ready to catch interruptions while I am speaking.");
        } else {
          setStatus("Fast browser microphone mode is active. The assistant chat remains available for full written answers.");
        }
      } else if (serverMicReady) {
        setStatus("Deep listening mode is active. The coach is listening through the local speech model.");
      } else {
        setStatus("Live microphone recognition is unavailable here. You can still use the typed assistant below for full answers.");
        setReply("Live microphone recognition is unavailable in this browser, but the assistant chat is fully active.");
      }
    } catch (error) {
      coachState.serverMicEnabled = false;
      if (RecognitionCtor) {
        if (!coachState.recognition) {
          coachState.recognition = configureRecognition();
        }
        startRecognition();
        setStatus("Deep listening mode could not start, so the assistant switched to the browser microphone path.");
      } else {
        setStatus("Microphone setup could not start here. The typed assistant below is still fully active.");
        setReply("Microphone setup is unavailable right now, but the assistant chat is ready.");
      }
    }
    respondLocally(greeting);
  })();
}

function initializeAcademyCoach() {
  coachState.sections = buildAcademySections();
  coachState.recognitionLang = dom.voiceLanguage?.value || coachState.recognitionLang;
  coachState.replyLanguage = effectiveReplyLocale(coachState.recognitionLang);
  focusSection(0, false);
  setCurrentLesson(coachState.sections[0]?.title || "Training Path");
  setReply("The assistant is ready. You can speak or type any lesson, music, or outside-information question.");
  setLLMStatus(
    "Checking language model availability",
    "The academy is checking whether a real local or configured language model is active."
  );
  coachState.messages = [
    {
      role: "assistant",
      text: "Hello. Ask me anything here if the microphone is unclear or if you want a written answer on screen.",
    },
  ];
  updateIndicator();
  setAmbienceStatus("Background classical ambience is off. You can turn it on manually or ask the coach to play soft classical music.");

  dom.enable.addEventListener("click", enableVoiceCoach);
  dom.stop.addEventListener("click", () => stopExplanation(false));
  dom.resume.addEventListener("click", resumeExplanation);
  dom.restart.addEventListener("click", restartFromBeginning);
  dom.llmRefresh?.addEventListener("click", () => {
    void refreshLLMStatus();
  });
  dom.voiceLanguage?.addEventListener("change", (event) => {
    coachState.recognitionLang = event.target.value;
    coachState.replyLanguage = effectiveReplyLocale(event.target.value);
    if (coachState.recognition) {
      coachState.recognition.lang = coachState.recognitionLang;
      if (coachState.enabled && !coachState.serverMicEnabled) {
        stopRecognitionForSpeech();
        queueRecognitionRestart(120);
      }
    }
    setStatus(`Microphone language set to ${event.target.options[event.target.selectedIndex]?.text || coachState.recognitionLang}.`);
  });
  dom.ambienceToggle?.addEventListener("click", () => setAmbienceEnabled(!coachState.ambienceEnabled));
  dom.ambienceVolume?.addEventListener("input", (event) => {
    coachState.ambienceUserVolume = Number(event.target.value) / 100;
    updateAmbienceLevel();
    if (coachState.ambienceEnabled) {
      setAmbienceStatus(`Classical ambience volume is set to ${Math.round(coachState.ambienceUserVolume * 100)} percent and will duck under the coach voice.`);
    }
  });

  dom.chatForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = dom.chatInput?.value?.trim() || "";
    if (!text) {
      return;
    }
    dom.chatInput.value = "";
    await submitAssistantQuery(text, "typed");
  });

  if (!supportsServerMicrophone() && !RecognitionCtor) {
    setStatus("Live microphone coaching needs either server transcription or browser speech recognition. The typed assistant below is still available.");
    setHeard("Speech recognition is not available in this browser.");
  } else if (!synth) {
    setStatus("Speech playback is not available in this browser. The assistant will still answer on screen and through the chat panel.");
    setReply("Speech playback is unavailable, so answers will stay visible on screen.");
  }

  if (synth) {
    if (typeof synth.onvoiceschanged !== "undefined") {
      synth.onvoiceschanged = () => pickVoice(effectiveReplyLocale());
    }
    pickVoice(effectiveReplyLocale());
  }

  void refreshLLMStatus();
}

initializeAcademyCoach();
