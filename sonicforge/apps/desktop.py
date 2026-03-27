from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from sonicforge.core.audio_preview import write_project_wav
from sonicforge.core.models import ProjectState
from sonicforge.core.session import apply_mix, apply_project_suggestion, create_project


class SonicForgeDesktop(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SNSAI SonicForge X MVP")
        self.geometry("1320x860")
        self.configure(bg="#0b1020")
        self.current_project: ProjectState | None = None
        self.suggestion_ids: list[str] = []
        self._build_style()
        self._build_layout()

    def _build_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Panel.TFrame", background="#10182b")
        style.configure("Card.TLabelframe", background="#10182b", foreground="#f5f8ff")
        style.configure("Card.TLabelframe.Label", background="#10182b", foreground="#f5f8ff")
        style.configure("Action.TButton", font=("Helvetica", 12, "bold"))

    def _build_layout(self) -> None:
        shell = ttk.Frame(self, padding=18, style="Panel.TFrame")
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=0)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        controls = ttk.LabelFrame(shell, text="Forge Controls", padding=16, style="Card.TLabelframe")
        controls.grid(row=0, column=0, sticky="nsw", padx=(0, 18))
        controls.columnconfigure(0, weight=1)
        output = ttk.Frame(shell, style="Panel.TFrame")
        output.grid(row=0, column=1, sticky="nsew")
        output.columnconfigure(0, weight=1)
        output.rowconfigure(0, weight=1)
        output.rowconfigure(1, weight=1)

        self.name_var = tk.StringVar(value="Neon Frontier")
        self.genre_var = tk.StringVar(value="cinematic-electronic")
        self.tempo_var = tk.IntVar(value=118)
        self.bars_var = tk.IntVar(value=8)
        self.valence_var = tk.DoubleVar(value=62)
        self.energy_var = tk.DoubleVar(value=68)
        self.tension_var = tk.DoubleVar(value=48)

        row = 0
        for label, variable in (
            ("Project", self.name_var),
            ("Genre", self.genre_var),
        ):
            ttk.Label(controls, text=label).grid(row=row, column=0, sticky="w", pady=(0, 6))
            ttk.Entry(controls, textvariable=variable, width=28).grid(row=row + 1, column=0, sticky="ew", pady=(0, 12))
            row += 2

        ttk.Label(controls, text="Tempo").grid(row=row, column=0, sticky="w")
        ttk.Scale(controls, from_=80, to=150, variable=self.tempo_var, orient="horizontal").grid(row=row + 1, column=0, sticky="ew")
        row += 2
        ttk.Label(controls, text="Bars").grid(row=row, column=0, sticky="w", pady=(8, 0))
        ttk.Spinbox(controls, from_=8, to=16, textvariable=self.bars_var, width=10).grid(row=row + 1, column=0, sticky="w")
        row += 2

        row = self._build_slider(controls, "Valence", self.valence_var, row)
        row = self._build_slider(controls, "Energy", self.energy_var, row)
        row = self._build_slider(controls, "Tension", self.tension_var, row)

        ttk.Label(controls, text="Lyrics").grid(row=row, column=0, sticky="w", pady=(8, 4))
        self.lyrics_input = tk.Text(controls, width=28, height=6, bg="#0d1324", fg="#f5f8ff", insertbackground="#f5f8ff")
        self.lyrics_input.insert("1.0", "we burn the night into a silver line")
        self.lyrics_input.grid(row=row + 1, column=0, sticky="ew")
        row += 2

        ttk.Button(controls, text="Generate Session", command=self.generate_project, style="Action.TButton").grid(row=row + 1, column=0, sticky="ew", pady=(8, 6))
        ttk.Button(controls, text="Auto Mix", command=self.auto_mix).grid(row=row + 2, column=0, sticky="ew", pady=6)
        ttk.Button(controls, text="Apply Selected Suggestion", command=self.apply_selected_suggestion).grid(row=row + 3, column=0, sticky="ew", pady=6)
        ttk.Button(controls, text="Export WAV", command=self.export_wav).grid(row=row + 4, column=0, sticky="ew", pady=6)

        summary_card = ttk.LabelFrame(output, text="Session Output", padding=14, style="Card.TLabelframe")
        summary_card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        summary_card.columnconfigure(0, weight=1)
        summary_card.rowconfigure(0, weight=1)
        self.summary_text = tk.Text(summary_card, wrap="word", bg="#0d1324", fg="#f5f8ff", insertbackground="#f5f8ff")
        self.summary_text.grid(row=0, column=0, sticky="nsew")

        lower = ttk.Frame(output, style="Panel.TFrame")
        lower.grid(row=1, column=0, sticky="nsew")
        lower.columnconfigure(0, weight=1)
        lower.columnconfigure(1, weight=1)
        lower.rowconfigure(0, weight=1)

        suggestion_card = ttk.LabelFrame(lower, text="Suggestions", padding=14, style="Card.TLabelframe")
        suggestion_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        suggestion_card.columnconfigure(0, weight=1)
        suggestion_card.rowconfigure(0, weight=1)
        self.suggestion_list = tk.Listbox(suggestion_card, bg="#0d1324", fg="#f5f8ff", selectbackground="#1c3b6b")
        self.suggestion_list.grid(row=0, column=0, sticky="nsew")

        voice_card = ttk.LabelFrame(lower, text="Voice Plan", padding=14, style="Card.TLabelframe")
        voice_card.grid(row=0, column=1, sticky="nsew")
        voice_card.columnconfigure(0, weight=1)
        voice_card.rowconfigure(0, weight=1)
        self.voice_text = tk.Text(voice_card, wrap="word", bg="#0d1324", fg="#f5f8ff", insertbackground="#f5f8ff")
        self.voice_text.grid(row=0, column=0, sticky="nsew")

    def _build_slider(self, parent: ttk.LabelFrame, label: str, variable: tk.DoubleVar, row: int) -> int:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(8, 0))
        ttk.Scale(parent, from_=0, to=100, variable=variable, orient="horizontal").grid(row=row + 1, column=0, sticky="ew")
        return row + 2

    def _build_combo(self, parent, label: str, variable: tk.StringVar, values: list[str], row: int, column: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w", pady=(2, 0))
        box = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly")
        box.grid(row=row + 1, column=column, sticky="ew", padx=(0, 6), pady=(0, 8))

    def _build_spin(self, parent, label: str, variable, minimum: int, maximum: int, row: int, column: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w", pady=(2, 0))
        ttk.Spinbox(parent, from_=minimum, to=maximum, textvariable=variable, width=10).grid(
            row=row + 1,
            column=column,
            sticky="ew",
            padx=(0, 6),
            pady=(0, 8),
        )

    def generate_project(self) -> None:
        self.current_project = create_project(
            name=self.name_var.get().strip() or "Untitled Forge Session",
            genre=self.genre_var.get().strip() or "cinematic-electronic",
            tempo=int(self.tempo_var.get()),
            bars=int(self.bars_var.get()),
            valence=float(self.valence_var.get()),
            energy=float(self.energy_var.get()),
            tension=float(self.tension_var.get()),
            lyrics=self.lyrics_input.get("1.0", "end").strip(),
        )
        self._refresh_view()

    def auto_mix(self) -> None:
        if not self.current_project:
            return messagebox.showinfo("SonicForge", "Generate a session before running Auto Mix.")
        self.current_project = apply_mix(self.current_project)
        self._refresh_view()

    def apply_selected_suggestion(self) -> None:
        if not self.current_project:
            return messagebox.showinfo("SonicForge", "Generate a session before applying a suggestion.")
        selection = self.suggestion_list.curselection()
        if not selection:
            return messagebox.showinfo("SonicForge", "Select a suggestion first.")
        suggestion_id = self.suggestion_ids[selection[0]]
        self.current_project = apply_project_suggestion(self.current_project, suggestion_id)
        self._refresh_view()

    def export_wav(self) -> None:
        if not self.current_project:
            return messagebox.showinfo("SonicForge", "Generate a session before exporting.")
        path = filedialog.asksaveasfilename(
            title="Export WAV",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            initialfile=f"{self.current_project.name}.wav",
        )
        if not path:
            return None
        write_project_wav(self.current_project, path)
        messagebox.showinfo("SonicForge", f"Exported {path}")

    def _refresh_view(self) -> None:
        project = self.current_project
        if project is None:
            return None
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", self._project_summary(project))

        self.suggestion_ids = [item.suggestion_id for item in project.suggestions]
        self.suggestion_list.delete(0, "end")
        for suggestion in project.suggestions:
            self.suggestion_list.insert(
                "end",
                f"{suggestion.title} ({int(suggestion.confidence * 100)}%)",
            )

        self.voice_text.delete("1.0", "end")
        if project.voice_plan and project.voice_plan.phonemes:
            lines = [f"Lyrics: {project.voice_plan.lyrics}", "", "Phoneme timeline:"]
            for frame in project.voice_plan.phonemes[:20]:
                lines.append(
                    f"{frame.symbol}  beat {frame.start_beat:.2f}  dur {frame.duration_beats:.2f}  pitch {frame.note_pitch}"
                )
            if project.voice_plan.breaths:
                lines.append("")
                lines.append("Breaths: " + ", ".join(f"{beat:.2f}" for beat in project.voice_plan.breaths))
            self.voice_text.insert("1.0", "\n".join(lines))
        else:
            self.voice_text.insert("1.0", "No lyric phrase supplied for voice planning.")

    def _project_summary(self, project: ProjectState) -> str:
        lines = [
            f"Project: {project.name}",
            f"Genre: {project.genre}",
            f"Tempo: {project.tempo} BPM",
            f"Form: {project.bars} bars in {project.key} {project.mode}",
            f"Emotion: valence {project.emotion['valence']:.0f}, energy {project.emotion['energy']:.0f}, tension {project.emotion['tension']:.0f}",
            "",
            "Sections:",
        ]
        for section in project.sections:
            lines.append(f"- {section.name}: bar {section.start_bar} for {section.bars} bars, energy {section.energy:.2f}")
        lines.append("")
        lines.append("Tracks:")
        for track in project.tracks:
            lines.append(
                f"- {track.name}: {len(track.notes)} notes, vol {track.volume:.2f}, pan {track.pan:.2f}, osc {track.patch.oscillator if track.patch else 'n/a'}"
            )
        if project.mix_report:
            lines.append("")
            lines.append(
                f"Mix report: headroom {project.mix_report.headroom_db:.2f} dB, width {project.mix_report.stereo_width:.2f}, low-end focus {project.mix_report.low_end_focus:.2f}"
            )
            lines.extend(f"- {item}" for item in project.mix_report.recommendations)
        return "\n".join(lines)


def main() -> None:
    app = SonicForgeDesktop()
    app.mainloop()


if __name__ == "__main__":
    main()
