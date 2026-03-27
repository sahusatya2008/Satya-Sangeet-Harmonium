let currentProject = null;
let audioContext = null;
let apiBase = null;

const byId = (id) => document.getElementById(id);

const fields = {
  name: byId("name"),
  genre: byId("genre"),
  tempo: byId("tempo"),
  bars: byId("bars"),
  valence: byId("valence"),
  energy: byId("energy"),
  tension: byId("tension"),
  lyrics: byId("lyrics"),
};

["tempo", "valence", "energy", "tension"].forEach((key) => {
  fields[key].addEventListener("input", () => {
    byId(`${key}-value`).textContent = fields[key].value;
  });
});

byId("generate").addEventListener("click", generateProject);
byId("mix").addEventListener("click", autoMix);
byId("play").addEventListener("click", playProject);
byId("download").addEventListener("click", downloadWav);

initializeApiConnection();

async function generateProject() {
  try {
    setStatus("Generating arrangement...");
    currentProject = await requestJson("/api/compose", {
      name: fields.name.value,
      genre: fields.genre.value,
      tempo: Number(fields.tempo.value),
      bars: Number(fields.bars.value),
      valence: Number(fields.valence.value),
      energy: Number(fields.energy.value),
      tension: Number(fields.tension.value),
      lyrics: fields.lyrics.value,
    });
    renderProject();
    setStatus(`Generated ${currentProject.name} in ${currentProject.key} ${currentProject.mode}.`);
  } catch (error) {
    setStatus(error.message);
  }
}

async function autoMix() {
  if (!currentProject) {
    return setStatus("Generate a session first.");
  }
  try {
    setStatus("Applying auto mix...");
    currentProject = await requestJson("/api/auto-mix", { project: currentProject });
    renderProject();
    setStatus("Auto mix updated track balances.");
  } catch (error) {
    setStatus(error.message);
  }
}

async function applySuggestion(suggestionId) {
  if (!currentProject) {
    return setStatus("Generate a session first.");
  }
  try {
    setStatus(`Applying ${suggestionId}...`);
    currentProject = await requestJson("/api/apply-suggestion", {
      project: currentProject,
      suggestion_id: suggestionId,
    });
    renderProject();
    setStatus(`Applied ${suggestionId}.`);
  } catch (error) {
    setStatus(error.message);
  }
}

async function downloadWav() {
  if (!currentProject) {
    return setStatus("Generate a session first.");
  }
  try {
    setStatus("Rendering WAV...");
    await ensureApiBase();
    const response = await fetch(apiUrl("/api/export-wav"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project: currentProject }),
    });
    if (!response.ok) {
      throw new Error("WAV export failed.");
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${currentProject.name}.wav`;
    anchor.click();
    URL.revokeObjectURL(url);
    setStatus("WAV exported.");
  } catch (error) {
    setStatus(error.message);
  }
}

async function requestJson(url, body) {
  await ensureApiBase();
  let response;
  try {
    response = await fetch(apiUrl(url), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (error) {
    apiBase = null;
    throw new Error(
      "Cannot reach the SonicForge API. Start the system with `python3 run_sonicforge.py --mode web` and open the page from that server."
    );
  }

  let payload = {};
  try {
    payload = await response.json();
  } catch (error) {
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}.`);
    }
  }

  if (!response.ok) {
    throw new Error(payload.error || `Request failed with status ${response.status}.`);
  }
  return payload;
}

function apiUrl(path) {
  if (!apiBase) {
    return path;
  }
  return new URL(path, `${apiBase}/`).toString();
}

async function initializeApiConnection() {
  try {
    await ensureApiBase();
    setStatus(`Connected to SonicForge API at ${apiBase}`);
  } catch (error) {
    setStatus(error.message);
  }
}

async function ensureApiBase() {
  if (apiBase) {
    return apiBase;
  }
  const candidates = candidateApiBases();
  for (const candidate of candidates) {
    try {
      const response = await fetch(new URL("/api/health", `${candidate}/`).toString(), {
        method: "GET",
        mode: "cors",
      });
      if (response.ok) {
        apiBase = candidate.replace(/\/$/, "");
        return apiBase;
      }
    } catch (error) {
      continue;
    }
  }
  throw new Error(
    "SonicForge API is not reachable. Run `python3 run_sonicforge.py --mode web` first, then reload this page."
  );
}

function candidateApiBases() {
  const search = new URLSearchParams(window.location.search);
  const explicit = search.get("api");
  const candidates = [];
  if (explicit) {
    candidates.push(explicit);
  }
  if (window.location.protocol === "http:" || window.location.protocol === "https:") {
    candidates.push(window.location.origin);
  }
  candidates.push("http://127.0.0.1:8000");
  candidates.push("http://localhost:8000");
  candidates.push("http://127.0.0.1:8001");
  candidates.push("http://localhost:8001");
  return [...new Set(candidates)];
}

function renderProject() {
  renderMetrics();
  renderTimeline();
  renderSuggestions();
  renderDetailFeed();
  byId("transport").textContent = `${currentProject.tempo} BPM · ${currentProject.bars} bars · ${currentProject.key} ${currentProject.mode}`;
}

function renderMetrics() {
  const metrics = byId("metrics");
  if (!currentProject) {
    metrics.innerHTML = "";
    return;
  }
  const report = currentProject.mix_report || { headroom_db: 0, stereo_width: 0, low_end_focus: 0 };
  metrics.innerHTML = [
    metric("Headroom", `${report.headroom_db.toFixed(2)} dB`),
    metric("Stereo Width", report.stereo_width.toFixed(2)),
    metric("Low-End Focus", report.low_end_focus.toFixed(2)),
    metric("Tracks", `${currentProject.tracks.length}`),
  ].join("");
}

function metric(label, value) {
  return `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`;
}

function renderTimeline() {
  const timeline = byId("timeline");
  timeline.innerHTML = "";
  if (!currentProject) {
    return;
  }
  const totalBeats = Math.max(4, currentProject.bars * 4);
  currentProject.tracks.forEach((track) => {
    const row = document.createElement("div");
    row.className = "track-row";
    const label = document.createElement("div");
    label.className = "track-label";
    label.innerHTML = `<strong>${track.name}</strong><br />${track.instrument} · vol ${track.volume.toFixed(2)} · pan ${track.pan.toFixed(2)}`;
    const lane = document.createElement("div");
    lane.className = "track-lane";
    track.notes.forEach((note) => {
      const block = document.createElement("div");
      block.className = "note-block";
      block.style.left = `${(note.start / totalBeats) * 100}%`;
      block.style.width = `${Math.max(0.8, (note.duration / totalBeats) * 100)}%`;
      block.style.background = track.patch?.color || track.color;
      lane.appendChild(block);
    });
    row.append(label, lane);
    timeline.appendChild(row);
  });
}

function renderSuggestions() {
  const suggestions = byId("suggestions");
  suggestions.innerHTML = "";
  if (!currentProject || !currentProject.suggestions.length) {
    suggestions.innerHTML = "<p class='tagline'>No suggestions available for this state.</p>";
    return;
  }
  currentProject.suggestions.forEach((suggestion) => {
    const card = document.createElement("div");
    card.className = "suggestion";
    card.innerHTML = `
      <h4>${suggestion.title}</h4>
      <p>${suggestion.description}</p>
      <p class="tagline">Confidence ${Math.round(suggestion.confidence * 100)}%</p>
      <button>Apply Suggestion</button>
    `;
    card.querySelector("button").addEventListener("click", () => applySuggestion(suggestion.suggestion_id));
    suggestions.appendChild(card);
  });
}

function renderDetailFeed() {
  const target = byId("detail-feed");
  if (!currentProject) {
    target.textContent = "No detail feed loaded.";
    return;
  }

  const blocks = [
    `Project: ${currentProject.name}`,
    `Key: ${currentProject.key} ${currentProject.mode}`,
    "",
    "Sections:",
  ];

  currentProject.sections.forEach((section) => {
    blocks.push(`- ${section.name}: bar ${section.start_bar}, ${section.bars} bars, energy ${section.energy.toFixed(2)}`);
  });

  if (currentProject.voice_plan && currentProject.voice_plan.phonemes.length) {
    blocks.push("");
    blocks.push(`Lyrics: ${currentProject.voice_plan.lyrics}`);
    blocks.push("");
    currentProject.voice_plan.phonemes.slice(0, 18).forEach((frame) => {
      blocks.push(
        `${frame.symbol.padEnd(3)} beat ${frame.start_beat.toFixed(2).padStart(5)} · dur ${frame.duration_beats.toFixed(2)} · pitch ${frame.note_pitch}`
      );
    });
    blocks.push("");
    blocks.push(
      `Breaths: ${(currentProject.voice_plan.breaths || []).map((value) => value.toFixed(2)).join(", ") || "none"}`
    );
  } else {
    blocks.push("");
    blocks.push("No lyric phrase supplied for voice planning.");
  }

  if (currentProject.mix_report) {
    blocks.push("");
    blocks.push("Mix notes:");
    currentProject.mix_report.recommendations.forEach((item) => blocks.push(`- ${item}`));
  }

  target.textContent = blocks.join("\n");
}

function setStatus(message) {
  byId("status").textContent = message;
}

async function playProject() {
  if (!currentProject) {
    return setStatus("Generate a session first.");
  }
  if (!audioContext) {
    const AudioCtor = window.AudioContext || window.webkitAudioContext;
    audioContext = new AudioCtor();
  }
  const startTime = audioContext.currentTime + 0.08;
  currentProject.tracks.forEach((track) => {
    track.notes.forEach((note) => scheduleNote(track, note, startTime));
  });
  setStatus("Playing browser preview...");
}

function scheduleNote(track, note, startTime) {
  const begin = startTime + (note.start * 60) / currentProject.tempo;
  const duration = Math.max(0.06, (note.duration * 60) / currentProject.tempo);
  if (track.instrument === "drums") {
    scheduleDrum(track, note, begin, duration);
    return;
  }

  const oscillator = audioContext.createOscillator();
  oscillator.type = mapOscillator(track.patch?.oscillator || track.instrument);
  oscillator.frequency.value = midiToFrequency(note.pitch);

  const gain = audioContext.createGain();
  gain.gain.setValueAtTime(0.0001, begin);
  gain.gain.linearRampToValueAtTime((track.volume * note.velocity) / 180, begin + 0.03);
  gain.gain.exponentialRampToValueAtTime(0.0001, begin + duration, 0.04);

  const panner = audioContext.createStereoPanner();
  panner.pan.value = track.pan;

  oscillator.connect(gain).connect(panner).connect(audioContext.destination);
  oscillator.start(begin);
  oscillator.stop(begin + duration + 0.05);
}

function scheduleDrum(track, note, begin, duration) {
  const gain = audioContext.createGain();
  const panner = audioContext.createStereoPanner();
  panner.pan.value = track.pan;
  gain.connect(panner).connect(audioContext.destination);

  if (note.pitch === 36) {
    const osc = audioContext.createOscillator();
    osc.type = "sine";
    osc.frequency.setValueAtTime(120, begin);
    osc.frequency.exponentialRampToValueAtTime(45, begin + 0.12);
    gain.gain.setValueAtTime(0.0001, begin);
    gain.gain.exponentialRampToValueAtTime(0.8 * track.volume, begin + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, begin + 0.18);
    osc.connect(gain);
    osc.start(begin);
    osc.stop(begin + 0.2);
    return;
  }

  const bufferSize = Math.max(1, Math.floor(audioContext.sampleRate * duration));
  const noiseBuffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i += 1) {
    data[i] = (Math.random() * 2 - 1) * Math.exp((-6 * i) / bufferSize);
  }
  const source = audioContext.createBufferSource();
  source.buffer = noiseBuffer;
  gain.gain.setValueAtTime(0.65 * track.volume, begin);
  gain.gain.exponentialRampToValueAtTime(0.0001, begin + duration);
  source.connect(gain);
  source.start(begin);
  source.stop(begin + duration + 0.02);
}

function mapOscillator(oscillator) {
  if (oscillator === "pulse" || oscillator === "square") return "square";
  if (oscillator === "saw") return "sawtooth";
  return oscillator === "noise" ? "triangle" : oscillator;
}

function midiToFrequency(note) {
  return 440 * 2 ** ((note - 69) / 12);
}
