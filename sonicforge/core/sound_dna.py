from __future__ import annotations

import random

from sonicforge.core.models import PatchGenome


OSCILLATORS = {
    "drums": ("noise", "pulse", "sine"),
    "bass": ("sine", "triangle", "square"),
    "pad": ("saw", "triangle", "noise"),
    "melody": ("square", "triangle", "saw"),
    "voice": ("triangle", "sine", "saw"),
}


def create_patch(role: str, emotion: dict[str, float], seed: int) -> PatchGenome:
    rng = random.Random(seed)
    energy = emotion["energy"]
    tension = emotion["tension"]
    palette = OSCILLATORS.get(role, OSCILLATORS["melody"])
    oscillator = palette[0 if energy < 45 else 1 if energy < 70 else 2]
    cutoff = 1800 + energy * 40 + tension * 10 + rng.randint(-200, 200)
    resonance = round(0.2 + tension / 200 + rng.random() * 0.2, 2)
    attack = round(max(0.01, 0.18 - energy / 600), 3)
    release = round(0.12 + (100 - energy) / 220 + rng.random() * 0.2, 3)
    color = "#%02x%02x%02x" % (
        80 + int(energy * 1.1) % 160,
        80 + int((100 - tension) * 1.2) % 160,
        100 + int(emotion["valence"] * 0.9) % 140,
    )
    return PatchGenome(
        oscillator=oscillator,
        cutoff=float(cutoff),
        resonance=resonance,
        attack=attack,
        release=release,
        color=color,
    )


def mutate_patch(patch: PatchGenome, intensity: float, seed: int) -> PatchGenome:
    rng = random.Random(seed)
    drift = max(0.05, intensity / 100)
    oscillator = patch.oscillator
    if rng.random() < 0.3 * drift:
        pool = ["sine", "triangle", "square", "saw", "noise", "pulse"]
        oscillator = rng.choice(pool)
    return PatchGenome(
        oscillator=oscillator,
        cutoff=max(200.0, patch.cutoff * (0.8 + rng.random() * 0.4 * drift)),
        resonance=min(0.95, max(0.1, patch.resonance + rng.uniform(-0.2, 0.2) * drift)),
        attack=max(0.005, patch.attack + rng.uniform(-0.05, 0.05) * drift),
        release=max(0.02, patch.release + rng.uniform(-0.12, 0.12) * drift),
        color=patch.color,
    )

