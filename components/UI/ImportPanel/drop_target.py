# drop_target.py - Drag-and-drop support
import tkinter as tk
from pathlib import Path
from components.constants import BG3, SURFACE2, TEXT_MUTED, FONT_LABEL, BORDER

def extend_drop_target(cls):
    def _build_drop_zone(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=8, pady=(4, 0))
        self._drop_frame = tk.Frame(self, bg=BG3, cursor="hand2")
        self._drop_frame.pack(fill="x", padx=8, pady=6)
        self._drop_arrow = tk.Label(self._drop_frame, text="v", font=("Courier", 14, "bold"),
                                    fg=TEXT_MUTED, bg=BG3, pady=4)
        self._drop_arrow.pack()
        self._drop_lbl = tk.Label(self._drop_frame, text="click here to browse files",
                                  font=FONT_LABEL, fg=TEXT_MUTED, bg=BG3, pady=4)
        self._drop_lbl.pack()
        for w in (self._drop_frame, self._drop_arrow, self._drop_lbl):
            w.bind("<Button-1>", lambda e: self._browse_files())
            w.bind("<Enter>", lambda e: self._drop_hl(True))
            w.bind("<Leave>", lambda e: self._drop_hl(False))
        self._try_dnd()

    def _try_dnd(self):
        try:
            self.tk.call("package", "require", "tkdnd")
            for widget in (self, self._drop_frame):
                widget.drop_target_register("DND_Files")
                widget.dnd_bind("<<Drop>>", self._on_dnd_drop)
                widget.dnd_bind("<<DragEnter>>", lambda e: self._drop_hl(True))
                widget.dnd_bind("<<DragLeave>>", lambda e: self._drop_hl(False))
            self._drop_lbl.config(text="drag & drop files here — or click to browse")
        except Exception:
            self._drop_lbl.config(text="click here to browse files")

    def _on_dnd_drop(self, event):
        self._drop_hl(False)
        try:
            paths = [Path(p) for p in self.tk.splitlist(event.data)]
            self._handle_paths(paths)
        except Exception as exc:
            from components.LOGIC.logging_setup import log_error
            log_error("DnD handler error", exc)

    def _drop_hl(self, on):
        col = SURFACE2 if on else BG3
        self._drop_frame.config(bg=col)
        self._drop_arrow.config(bg=col)
        self._drop_lbl.config(bg=col)

    cls._build_drop_zone = _build_drop_zone
    cls._try_dnd = _try_dnd
    cls._on_dnd_drop = _on_dnd_drop
    cls._drop_hl = _drop_hl