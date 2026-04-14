# build.py
import tkinter as tk
from components.constants import BG2, BORDER, TEXT_MUTED
from components.LOGIC.default_settings import default_settings

from components.registry import get_component
DuskSlider = get_component("components.UI.DuskSlider")
DuskButton = get_component("components.UI.DuskButton")

def _build(self):
    d = default_settings()
    canvas = tk.Canvas(self, bg=BG2, bd=0, highlightthickness=0)
    sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)

    inner = tk.Frame(canvas, bg=BG2)
    wid = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _resize(e=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(wid, width=canvas.winfo_width())
    inner.bind("<Configure>", _resize)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(wid, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

    def section(t):
        tk.Frame(inner, bg=BG2, height=4).pack()
        f = tk.Frame(inner, bg=BG2)
        f.pack(fill="x", padx=8, pady=(8, 0))
        tk.Label(f, text=t.upper(), font=("Courier", 7, "bold"), fg=TEXT_MUTED, bg=BG2).pack(anchor="w")
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=8, pady=2)

    def sl(k, lbl, lo, hi):
        DuskSlider(inner, lbl, self._var(k, d[k]), lo, hi,
                   command=self._on_change).pack(fill="x", pady=1)

    section("crop (%)")
    sl("crop_top", "top trim", 0, 40)
    sl("crop_bottom", "bottom trim", 0, 40)
    sl("crop_left", "left trim", 0, 40)
    sl("crop_right", "right trim", 0, 40)
    section("skin")
    sl("smooth", "softness", 0, 100)
    sl("smooth_radius", "blur radius", 1, 8)
    section("exposure")
    sl("brightness", "brightness", 50, 150)
    sl("contrast", "contrast", 50, 150)
    sl("saturation", "saturation", 0, 150)
    sl("sharpness", "sharpness", 0, 200)
    section("mood")
    sl("vignette", "vignette", 0, 100)
    sl("grain", "grain", 0, 80)
    sl("tone", "warm / cool", -100, 100)

    section("presets")
    pr = tk.Frame(inner, bg=BG2)
    pr.pack(fill="x", padx=8, pady=8)
    presets = {
        "dusk":   dict(brightness=105, contrast=110, saturation=90, vignette=70, grain=12, tone=10),
        "noir":   dict(brightness=95,  contrast=130, saturation=20, vignette=90, grain=25, tone=-5),
        "golden": dict(brightness=112, contrast=105, saturation=110, vignette=50, grain=5,  tone=30),
        "raw":    dict(brightness=100, contrast=100, saturation=100, vignette=0,  grain=0,  tone=0),
    }
    for name, vals in presets.items():
        DuskButton(pr, name, command=lambda v=vals, n=name: self._preset(v, n)).pack(side="left", padx=2)

    tk.Frame(inner, bg=BG2, height=8).pack()
    DuskButton(inner, "reset all", command=self._reset, variant="danger").pack(anchor="e", padx=12)
    tk.Frame(inner, bg=BG2, height=12).pack()