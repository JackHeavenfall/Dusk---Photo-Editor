# thumb_loading.py - Background thumbnail loading
from PIL import Image, ImageTk
from components.constants import THUMB_W, THUMB_H
from components.LOGIC.logging_setup import log

def extend_thumb_loading(cls):
    def _load_thumbs(self, start_idx, paths):
        for offset, path in enumerate(paths):
            real_idx = start_idx + offset
            try:
                img = Image.open(path)
                img.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)
                bg_color = (30, 28, 25)
                canvas = Image.new("RGB", (THUMB_W, THUMB_H), bg_color)
                ox = (THUMB_W - img.width) // 2
                oy = (THUMB_H - img.height) // 2
                canvas.paste(img.convert("RGB"), (ox, oy))
                tkimg = ImageTk.PhotoImage(canvas)
                if real_idx < len(self._thumbs):
                    self._thumbs[real_idx] = tkimg
                    self.after(0, self._rebuild_cards)
            except Exception as exc:
                import logging
                log(f"Thumb load failed for {path.name}: {exc}", logging.DEBUG)

    cls._load_thumbs = _load_thumbs