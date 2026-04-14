# core.py - Constructor and basic layout
import tkinter as tk
from components.constants import BG2, BORDER, BG3, TEXT_MUTED, FONT_LABEL

from components.UI.DuskButton import DuskButton



class ImportPanel(tk.Frame):
    def __init__(self, parent, on_select, on_files_added, **kw):
        super().__init__(parent, bg=BG2, **kw)
        self._on_select = on_select
        self._on_files_added = on_files_added
        self._items = []          # list[Path]
        self._thumbs = []         # list[ImageTk | None]
        self._selected_idx = -1
        self._build()

    def _build(self):
        # Section 1: large add-buttons
        add_frame = tk.Frame(self, bg=BG2)
        add_frame.pack(fill="x", padx=10, pady=(10, 6))
        tk.Label(add_frame, text="ADD IMAGES", font=("Courier", 7, "bold"),
                 fg=TEXT_MUTED, bg=BG2).pack(anchor="w", pady=(0, 6))

        # Buttons will be created by methods from add_buttons.py
        self._make_big_btn(add_frame, "IMAGE", "Browse Files",
                           "jpg  png  webp  bmp  tiff",
                           self._browse_files).pack(fill="x", pady=2)
        self._make_big_btn(add_frame, "FOLDER", "Browse Folder",
                           "imports all images inside",
                           self._browse_folder).pack(fill="x", pady=2)
        self._make_big_btn(add_frame, "ZIP", "Open Archive  .zip",
                           "auto-extracts then imports",
                           self._browse_zip).pack(fill="x", pady=2)

        # Section 2: drop target (will be built by drop_target)
        self._build_drop_zone()

        # Section 3: queue header
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=8)
        q_hdr = tk.Frame(self, bg=BG2)
        q_hdr.pack(fill="x", padx=10, pady=(8, 2))
        tk.Label(q_hdr, text="QUEUE", font=("Courier", 7, "bold"),
                 fg=TEXT_MUTED, bg=BG2).pack(side="left")
        self._count_lbl = tk.Label(q_hdr, text="0 files",
                                   font=("Courier", 8), fg=TEXT_MUTED, bg=BG2)
        self._count_lbl.pack(side="right")

        # Section 4: scrollable card list (built by card_rendering)
        self._build_card_area()

        # Section 5: controls
        ctrl = tk.Frame(self, bg=BG2)
        ctrl.pack(fill="x", padx=8, pady=(2, 8))
        DuskButton(ctrl, "remove selected", command=self._remove_selected,
                   variant="ghost").pack(side="left", padx=2)
        DuskButton(ctrl, "clear all", command=self.clear_queue,
                   variant="danger").pack(side="right", padx=2)