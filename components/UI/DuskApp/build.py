# components/UI/DuskApp/build.py
import tkinter as tk
from tkinter import ttk
from components.constants import BG, BORDER, BG2, BG3, TEXT_MUTED, ACCENT2, FONT_TITLE, FONT_SMALL

from components.UI.ImportPanel import ImportPanel
from components.UI.PreviewPanel import PreviewPanel
from components.UI.SettingsPanel import SettingsPanel
from components.UI.LogViewer import LogViewer
from components.UI.DuskButton import DuskButton


class DuskAppBuildMixin:
    def _build(self):
        # Top bar
        topbar = tk.Frame(self, bg=BG, height=50)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="DUSK", font=FONT_TITLE,
                 fg=ACCENT2, bg=BG).pack(side="left", padx=20)
        tk.Label(topbar, text="tired yet handsome",
                 font=("Georgia", 9, "italic"),
                 fg=TEXT_MUTED, bg=BG).pack(side="left", padx=4)
        DuskButton(topbar, "export all",
                   command=self._export_all, variant="accent"
                   ).pack(side="right", padx=12, pady=8)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # Notebook (editor + logs)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Root.TNotebook",
                        background=BG, borderwidth=0, tabmargins=[0, 4, 0, 0])
        style.configure("Root.TNotebook.Tab",
                        background=BG2, foreground=TEXT_MUTED,
                        font=("Courier", 9, "bold"), padding=[18, 6],
                        borderwidth=0)
        style.map("Root.TNotebook.Tab",
                  background=[("selected", BG3)],
                  foreground=[("selected", ACCENT2)])

        nb = ttk.Notebook(self, style="Root.TNotebook")
        nb.pack(fill="both", expand=True)

        editor_frame = tk.Frame(nb, bg=BG)
        nb.add(editor_frame, text="  editor  ")
        self._build_editor(editor_frame)

        log_frame = tk.Frame(nb, bg=BG)
        nb.add(log_frame, text="  logs  ")
        LogViewer(log_frame).pack(fill="both", expand=True)

        # Status bar
        self._status = tk.Label(
            self,
            text="ready  —  use the buttons on the left to add images",
            font=FONT_SMALL, fg=TEXT_MUTED, bg=BG, anchor="w", padx=12)
        self._status.pack(fill="x", side="bottom", pady=2)

    def _build_editor(self, parent):
        pane = tk.PanedWindow(parent, orient="horizontal", bg=BG, bd=0,
                              sashwidth=4, sashrelief="flat", handlesize=0)
        pane.pack(fill="both", expand=True)

        left = tk.Frame(pane, bg=BG2, width=290)
        pane.add(left, minsize=250)
        self._import = ImportPanel(left,
                                   on_select=self._on_file_selected,
                                   on_files_added=self._on_files_added)
        self._import.pack(fill="both", expand=True)

        centre = tk.Frame(pane, bg=BG, width=580)
        pane.add(centre, minsize=300)
        self._preview = PreviewPanel(centre)
        self._preview.pack(fill="both", expand=True)

        right = tk.Frame(pane, bg=BG2, width=250)
        pane.add(right, minsize=200)
        tk.Label(right, text="adjustments", font=("Georgia", 9, "italic"),
                 fg=TEXT_MUTED, bg=BG2).pack(pady=(10, 0))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=8, pady=4)
        self._settings = SettingsPanel(right, on_change=self._schedule_preview)
        self._settings.pack(fill="both", expand=True)