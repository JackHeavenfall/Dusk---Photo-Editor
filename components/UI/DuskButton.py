# DuskButton.py
import tkinter as tk
from components.constants import BG, BG3, SURFACE2, BORDER, TEXT, TEXT_DIM, ACCENT, ACCENT2, DANGER, FONT_BUTTON
from components.registry import register

class DuskButton(tk.Label):
    def __init__(self, parent, text, command=None, variant="normal", **kw):
        c = {
            "normal": (SURFACE2, BORDER,  TEXT),
            "accent": (ACCENT,   ACCENT2, BG),
            "danger": (SURFACE2, DANGER,  DANGER),
            "ghost":  (BG3,      SURFACE2, TEXT_DIM),
        }
        bi, bh, fg = c.get(variant, c["normal"])
        super().__init__(parent, text=text, font=FONT_BUTTON, fg=fg,
                         bg=bi, padx=12, pady=6, cursor="hand2", **kw)
        self._bi, self._bh, self._fg, self._v = bi, bh, fg, variant
        self._cmd = command
        self.bind("<Enter>",    lambda e: self.config(
                                    bg=self._bh,
                                    fg=BG if self._v == "accent" else self._bh))
        self.bind("<Leave>",    lambda e: self.config(bg=self._bi, fg=self._fg))
        self.bind("<Button-1>", lambda e: self._cmd() if self._cmd else None)

register(__name__, DuskButton)