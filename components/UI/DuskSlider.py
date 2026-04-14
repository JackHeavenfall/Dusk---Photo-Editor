# DuskSlider.py
import tkinter as tk
from components.constants import BG2, TEXT_DIM, ACCENT, SURFACE2, TEXT, FONT_LABEL, FONT_SMALL
from components.registry import register

class DuskSlider(tk.Frame):
    def __init__(self, parent, label, var, from_, to, command=None, bg=None, **kw):
        _bg = bg or BG2
        super().__init__(parent, bg=_bg, **kw)
        row = tk.Frame(self, bg=_bg)
        row.pack(fill="x", padx=8, pady=(6, 0))
        tk.Label(row, text=label, font=FONT_LABEL, fg=TEXT_DIM, bg=_bg, anchor="w").pack(side="left")
        lbl = tk.Label(row, text=str(int(var.get())), font=FONT_SMALL,
                       fg=ACCENT, bg=_bg, width=4, anchor="e")
        lbl.pack(side="right")

        def _cmd(v):
            lbl.config(text=str(int(float(v))))
            if command:
                command()

        tk.Scale(self, variable=var, from_=from_, to=to, orient="horizontal",
                 showvalue=False, bg=_bg, troughcolor=SURFACE2, activebackground=ACCENT,
                 fg=TEXT, highlightthickness=0, bd=0, sliderrelief="flat",
                 sliderlength=14, command=_cmd
                 ).pack(fill="x", padx=8, pady=(0, 4))

register(__name__, DuskSlider)