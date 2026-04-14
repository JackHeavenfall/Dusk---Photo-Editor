# core.py
import tkinter as tk
from components.constants import BG, ACCENT, TEXT_MUTED, FONT_LABEL, FONT_SMALL
from components.registry import register

class PreviewPanel(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG, **kw)
        self._refs = []
        self._src_raw = None
        self._out_raw = None
        self._mode = tk.StringVar(value="split")
        self._build()

    def _build(self):
        toggle = tk.Frame(self, bg=BG)
        toggle.pack(pady=(8, 4))
        for val, lbl in [("before", "before"), ("split", "split"), ("after", "after")]:
            tk.Radiobutton(
                toggle, text=lbl, variable=self._mode, value=val,
                font=FONT_LABEL, fg=TEXT_MUTED, bg=BG, selectcolor=BG,
                activebackground=BG, activeforeground=ACCENT,
                command=self._redraw, indicatoron=False,
                padx=8, pady=2, relief="flat", bd=0, highlightthickness=0,
            ).pack(side="left", padx=2)

        self._canvas = tk.Canvas(self, bg=BG, bd=0, highlightthickness=0)
        self._canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self._canvas.bind("<Configure>", lambda e: self._redraw())

        self._lbl = tk.Label(self, text="no image loaded",
                             font=FONT_LABEL, fg=TEXT_MUTED, bg=BG)
        self._lbl.pack(pady=4)

    def show(self, src, out, name=""):
        self._src_raw = src
        self._out_raw = out
        self._lbl.config(text=name)
        self._redraw()

from .redraw import _redraw, _place
PreviewPanel._redraw = _redraw
PreviewPanel._place = _place

register(__name__, PreviewPanel)