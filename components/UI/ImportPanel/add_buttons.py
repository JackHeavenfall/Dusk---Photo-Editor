# add_buttons.py - Large import buttons and browse actions
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from components.constants import BG, BG2, SURFACE, SURFACE2, ACCENT, TEXT, TEXT_MUTED, FONT_BUTTON, FONT_SMALL
from components.LOGIC.zip_utils import extract_zip

def extend_add_buttons(cls):
    def _make_big_btn(self, parent, icon, label, sub, command):
        outer = tk.Frame(parent, bg=SURFACE, cursor="hand2")
        inner = tk.Frame(outer, bg=SURFACE)
        inner.pack(fill="x", padx=10, pady=8)
        badge = tk.Label(inner, text=icon, font=("Courier", 7, "bold"),
                         bg=ACCENT, fg=BG, padx=4, pady=2)
        badge.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="w")
        tk.Label(inner, text=label, font=FONT_BUTTON,
                 bg=SURFACE, fg=TEXT, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(inner, text=sub, font=FONT_SMALL,
                 bg=SURFACE, fg=TEXT_MUTED, anchor="w").grid(row=1, column=1, sticky="w")
        for w in [outer, inner, badge] + list(inner.winfo_children()):
            w.bind("<Enter>", lambda e, w=w: w.config(bg=SURFACE2) if w != badge else None)
            w.bind("<Leave>", lambda e, w=w: w.config(bg=SURFACE if w != badge else ACCENT))
            w.bind("<Button-1>", lambda e: command())
        return outer

    def _browse_files(self):
        from components.constants import SUPPORTED
        exts = " ".join(f"*{e}" for e in sorted(SUPPORTED))
        paths = filedialog.askopenfilenames(
            title="Select images or zip archives",
            filetypes=[("Images & Archives", exts + " *.zip"),
                       ("JPEG Images", "*.jpg *.jpeg"),
                       ("PNG Images", "*.png"),
                       ("ZIP Archives", "*.zip"),
                       ("All Files", "*.*")]
        )
        if paths:
            self._handle_paths([Path(p) for p in paths])

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Select a folder of images")
        if folder:
            self._handle_paths([Path(folder)])

    def _browse_zip(self):
        path = filedialog.askopenfilename(
            title="Select a zip archive",
            filetypes=[("Zip Archives", "*.zip"), ("All Files", "*.*")]
        )
        if path:
            self._handle_paths([Path(path)])

    cls._make_big_btn = _make_big_btn
    cls._browse_files = _browse_files
    cls._browse_folder = _browse_folder
    cls._browse_zip = _browse_zip