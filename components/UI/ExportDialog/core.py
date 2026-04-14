# core.py
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from components.constants import BG, SURFACE, BORDER, ACCENT, ACCENT2, TEXT, TEXT_DIM, FONT_BIG, FONT_LABEL, FONT_BODY, FONT_SMALL

from components.UI.DuskButton import DuskButton

from components.registry import register
import threading

class ExportDialog(tk.Toplevel):
    def __init__(self, parent, files, settings):
        super().__init__(parent)
        self.title("export — dusk")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._files = files
        self._settings = settings
        self._out_dir = tk.StringVar(value=str(Path.home() / "Pictures" / "dusk_output"))
        self._fmt = tk.StringVar(value="jpg")
        self._quality = tk.IntVar(value=92)
        self._do_zip = tk.BooleanVar(value=len(files) > 1)
        self._zip_name = tk.StringVar(value="dusk_export")
        self._running = False
        self._build()

    def _build(self):
        tk.Label(self, text="export", font=FONT_BIG, fg=ACCENT2, bg=BG).pack(pady=(16,4))
        tk.Label(self, text=f"{len(self._files)} image(s) to process", font=FONT_LABEL, fg=TEXT_DIM, bg=BG).pack()

        body = tk.Frame(self, bg=BG)
        body.pack(padx=24, pady=12, fill="x")

        def row(label, fn):
            f = tk.Frame(body, bg=BG)
            f.pack(fill="x", pady=4)
            tk.Label(f, text=label, font=FONT_LABEL, fg=TEXT_DIM, bg=BG, width=14, anchor="w").pack(side="left")
            fn(f)

        def dir_row(p):
            tk.Entry(p, textvariable=self._out_dir, font=FONT_BODY, bg=SURFACE, fg=TEXT,
                     insertbackground=ACCENT, bd=0, relief="flat", highlightthickness=1,
                     highlightcolor=ACCENT, highlightbackground=BORDER
                     ).pack(side="left", fill="x", expand=True, ipady=4, padx=(0,4))
            DuskButton(p, "browse", command=self._browse_dir).pack(side="right")

        def fmt_row(p):
            for f in ["jpg", "png", "webp"]:
                tk.Radiobutton(p, text=f, variable=self._fmt, value=f, font=FONT_BODY, fg=TEXT_DIM, bg=BG,
                               selectcolor=BG, activebackground=BG, activeforeground=ACCENT, indicatoron=False,
                               padx=8, pady=2, relief="flat", bd=0, highlightthickness=0).pack(side="left", padx=2)

        row("output folder", dir_row)
        row("format", fmt_row)

        qs = tk.Frame(body, bg=BG)
        qs.pack(fill="x", pady=4)
        tk.Label(qs, text="jpeg quality", font=FONT_LABEL, fg=TEXT_DIM, bg=BG, width=14, anchor="w").pack(side="left")
        tk.Scale(qs, variable=self._quality, from_=60, to=100, orient="horizontal", bg=BG, troughcolor=SURFACE,
                 activebackground=ACCENT, fg=TEXT, highlightthickness=0, bd=0, sliderrelief="flat",
                 sliderlength=14, showvalue=True, font=FONT_SMALL).pack(side="left", fill="x", expand=True)

        zf = tk.Frame(body, bg=BG)
        zf.pack(fill="x", pady=4)
        tk.Checkbutton(zf, text="zip output", variable=self._do_zip, font=FONT_LABEL, fg=TEXT_DIM, bg=BG,
                       selectcolor=BG, activebackground=BG, activeforeground=ACCENT).pack(side="left")
        tk.Entry(zf, textvariable=self._zip_name, font=FONT_BODY, bg=SURFACE, fg=TEXT,
                 insertbackground=ACCENT, bd=0, relief="flat", width=18, highlightthickness=1,
                 highlightcolor=ACCENT, highlightbackground=BORDER).pack(side="left", padx=8, ipady=3)

        self._prog = ttk.Progressbar(self, mode="determinate", maximum=max(1, len(self._files)))
        self._prog_lbl = tk.Label(self, text="", font=FONT_SMALL, fg=TEXT_DIM, bg=BG)

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=16)
        DuskButton(btn_row, "cancel", command=self._cancel).pack(side="left", padx=8)
        self._export_btn = DuskButton(btn_row, "export", command=self._start, variant="accent")
        self._export_btn.pack(side="left", padx=8)

    def _browse_dir(self):
        from tkinter import filedialog
        d = filedialog.askdirectory(title="Choose export folder")
        if d:
            self._out_dir.set(d)

    def _cancel(self):
        self._running = False
        self.destroy()

    def _start(self):
        if self._running:
            return
        self._running = True
        self._prog.pack(fill="x", padx=24, pady=2)
        self._prog_lbl.pack()
        self._export_btn.config(text="exporting...")
        threading.Thread(target=self._worker, daemon=True).start()

    # _worker in separate file

from .worker import _worker
ExportDialog._worker = _worker

register(__name__, ExportDialog)