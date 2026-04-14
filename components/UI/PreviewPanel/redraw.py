# redraw.py
import tkinter as tk
from PIL import Image, ImageTk
from components.constants import ACCENT, FONT_SMALL, TEXT_MUTED

def _redraw(self):
    c = self._canvas
    cw, ch = c.winfo_width(), c.winfo_height()
    if cw < 10 or ch < 10:
        return
    if self._src_raw is None or self._out_raw is None:
        return

    c.delete("all")
    self._refs = []
    mode = self._mode.get()
    if mode == "before":
        self._place(self._src_raw, 0, 0, cw, ch)
    elif mode == "after":
        self._place(self._out_raw, 0, 0, cw, ch)
    else:
        half = cw // 2
        self._place(self._src_raw, 0,    0, half, ch, fw=half)
        self._place(self._out_raw, half, 0, half, ch, fw=half)
        c.create_line(half, 0, half, ch, fill=ACCENT, width=1, dash=(4, 4))
        c.create_text(half // 2,        14, text="before", font=FONT_SMALL, fill=TEXT_MUTED)
        c.create_text(half + half // 2, 14, text="after",  font=FONT_SMALL, fill=TEXT_MUTED)

def _place(self, img, x, y, w, h, fw=None):
    fw = fw or w
    copy = img.copy()
    copy.thumbnail((fw, h), Image.LANCZOS)
    iw, ih = copy.size
    tkimg = ImageTk.PhotoImage(copy)
    self._refs.append(tkimg)
    self._canvas.create_image(x + (fw - iw) // 2, y + (h - ih) // 2,
                              anchor="nw", image=tkimg)