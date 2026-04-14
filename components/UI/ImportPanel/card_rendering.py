# card_rendering.py - Card display and selection
import tkinter as tk
from components.constants import (BG, BG2, BG3, SURFACE,
        SURFACE2, BORDER, TEXT, TEXT_DIM,
        TEXT_MUTED, ACCENT, ACCENT2, DANGER,
        SUCCESS, ACTIVE_BG, THUMB_W, THUMB_H, FONT_BODY, FONT_SMALL)

def extend_card_rendering(cls):
    def _build_card_area(self):
        scroll_outer = tk.Frame(self, bg=BG2)
        scroll_outer.pack(fill="both", expand=True, padx=4, pady=(0,2))
        self._vsb = tk.Scrollbar(scroll_outer, orient="vertical", bg=BG2, troughcolor=BG, bd=0)
        self._vsb.pack(side="right", fill="y")
        self._card_canvas = tk.Canvas(scroll_outer, bg=BG2, bd=0, highlightthickness=0)
        self._card_canvas.pack(side="left", fill="both", expand=True)
        self._card_canvas.configure(yscrollcommand=self._vsb.set)
        self._vsb.config(command=self._card_canvas.yview)
        self._card_canvas.bind("<MouseWheel>", lambda e: self._card_canvas.yview_scroll(-1*(e.delta//120), "units"))
        self._cards = tk.Frame(self._card_canvas, bg=BG2)
        self._cards_id = self._card_canvas.create_window((0,0), window=self._cards, anchor="nw")
        self._cards.bind("<Configure>", self._sync_scroll)
        self._card_canvas.bind("<Configure>", lambda e: self._card_canvas.itemconfig(self._cards_id, width=e.width))

    def _rebuild_cards(self):
        for w in self._cards.winfo_children():
            w.destroy()
        if not self._items:
            tk.Label(self._cards, text="no images in queue",
                     font=("Georgia", 9, "italic"), fg=TEXT_MUTED, bg=BG2, pady=16).pack()
            return
        for i, path in enumerate(self._items):
            self._make_card(i, path)

    def _make_card(self, idx, path):
        is_sel = (idx == self._selected_idx)
        card_bg = ACTIVE_BG if is_sel else BG2
        border_c = ACCENT if is_sel else BORDER
        card = tk.Frame(self._cards, bg=border_c, cursor="hand2")
        card.pack(fill="x", padx=4, pady=2)
        inner = tk.Frame(card, bg=card_bg)
        inner.pack(fill="x", padx=1, pady=1)
        thumb_lbl = tk.Label(inner, bg=BG3, width=THUMB_W, height=THUMB_H, bd=0)
        thumb_lbl.grid(row=0, column=0, rowspan=2, padx=(5,8), pady=5, sticky="ns")
        if self._thumbs[idx] is not None:
            thumb_lbl.config(image=self._thumbs[idx])
        name = path.name
        display = (name[:20]+"...") if len(name)>22 else name
        tk.Label(inner, text=display, font=FONT_BODY, fg=ACCENT2 if is_sel else TEXT,
                 bg=card_bg, anchor="w").grid(row=0, column=1, sticky="ew", pady=(5,0), padx=(0,4))
        pstr = str(path.parent)
        if len(pstr) > 26: pstr = "..." + pstr[-24:]
        tk.Label(inner, text=pstr, font=FONT_SMALL,
                 fg=TEXT_DIM if is_sel else TEXT_MUTED, bg=card_bg, anchor="w"
                 ).grid(row=1, column=1, sticky="ew", pady=(0,5), padx=(0,4))
        inner.columnconfigure(1, weight=1)
        def _click(e, i=idx): self._select(i)
        for w in [card, inner, thumb_lbl] + list(inner.winfo_children()):
            w.bind("<Button-1>", _click)

    def _select(self, idx):
        self._selected_idx = idx
        self._rebuild_cards()
        if 0 <= idx < len(self._items):
            self._on_select(self._items[idx])
            self.after(30, self._scroll_to, idx)

    def _scroll_to(self, idx):
        if len(self._items) > 1:
            self._card_canvas.yview_moveto(idx / len(self._items))

    def _sync_scroll(self, event=None):
        self._card_canvas.configure(scrollregion=self._card_canvas.bbox("all"))

    cls._build_card_area = _build_card_area
    cls._rebuild_cards = _rebuild_cards
    cls._make_card = _make_card
    cls._select = _select
    cls._scroll_to = _scroll_to
    cls._sync_scroll = _sync_scroll