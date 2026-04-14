# core.py
import tkinter as tk
from tkinter import ttk
import queue
import threading
from datetime import datetime

from components.constants import BG, BG2, SURFACE2, ACCENT2, TEXT_DIM, TEXT_MUTED, BORDER, LOG_COLORS, FONT_BIG, FONT_BUTTON, FONT_SMALL, FONT_MONO

from components.LOGIC.logging_setup import _gui_log_queue, LOG_PATH, ERR_PATH

from components.UI.DuskButton import DuskButton

from components.registry import register


class LogViewer(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG, **kw)
        self._build()
        self._poll()

    def _build(self):
        # header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(hdr, text="logs", font=FONT_BIG, fg=ACCENT2, bg=BG).pack(side="left")
        DuskButton(hdr, "export logs", command=self._export_logs, variant="accent").pack(side="right", padx=4)
        DuskButton(hdr, "clear view", command=self._clear_view).pack(side="right", padx=4)
        DuskButton(hdr, "refresh", command=self._reload).pack(side="right", padx=4)
        tk.Label(hdr, text=f"next to dusk.pyw  —  {LOG_PATH.parent}", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG).pack(side="left", padx=12)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        style = ttk.Style()
        style.configure("Log.TNotebook", background=BG, borderwidth=0, tabmargins=0)
        style.configure("Log.TNotebook.Tab", background=BG2, foreground=TEXT_DIM, font=FONT_BUTTON, padding=[14,5], borderwidth=0)
        style.map("Log.TNotebook.Tab", background=[("selected", SURFACE2)], foreground=[("selected", ACCENT2)])

        nb = ttk.Notebook(self, style="Log.TNotebook")
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        self._app_text = self._tab(nb, "app log")
        self._err_text = self._tab(nb, "error log")

        for w in (self._app_text, self._err_text):
            for level, color in LOG_COLORS.items():
                w.tag_config(level, foreground=color)

        self._info = tk.Label(self, text="", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG, anchor="w")
        self._info.pack(fill="x", padx=12, pady=(0, 6))
        self._reload()

    def _tab(self, nb, title):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text=title)
        sb = tk.Scrollbar(f, bg=BG2, troughcolor=BG, bd=0, relief="flat")
        sb.pack(side="right", fill="y")
        t = tk.Text(f, bg=BG2, fg=TEXT_DIM, font=FONT_MONO, bd=0, relief="flat", wrap="word",
                    highlightthickness=0, yscrollcommand=sb.set, state="disabled", selectbackground=SURFACE2)
        t.pack(fill="both", expand=True)
        sb.config(command=t.yview)
        return t

    def _poll(self):
        try:
            while True:
                r = _gui_log_queue.get_nowait()
                line = f"{r.asctime}  {r.levelname:<8}  {r.getMessage()}\n"
                lvl = r.levelname
                self._append(self._app_text, line, lvl)
                if lvl in ("WARNING", "ERROR", "CRITICAL"):
                    self._append(self._err_text, line, lvl)
        except queue.Empty:
            pass
        self.after(500, self._poll)

    def _append(self, w, text, tag=""):
        w.config(state="normal")
        w.insert("end", text, tag or ())
        w.see("end")
        w.config(state="disabled")

    # _reload, _tag_for, _clear_view, _export_logs in separate files

from .actions import _reload, _tag_for, _clear_view, _export_logs
LogViewer._reload = _reload
LogViewer._tag_for = _tag_for
LogViewer._clear_view = _clear_view
LogViewer._export_logs = _export_logs

register(__name__, LogViewer)