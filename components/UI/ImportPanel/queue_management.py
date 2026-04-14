# queue_management.py - Queue operations and path handling
import threading
import tempfile
from pathlib import Path
from tkinter import messagebox
from components.constants import SUPPORTED
from components.LOGIC.zip_utils import extract_zip
from components.LOGIC.logging_setup import log, log_error

def extend_queue_management(cls):
    def _handle_paths(self, paths):
        found, skipped = [], 0
        for p in paths:
            try:
                if p.is_dir():
                    imgs = [f for f in p.rglob("*") if f.suffix.lower() in SUPPORTED]
                    found.extend(imgs)
                elif p.suffix.lower() == ".zip":
                    # Use system temp folder instead of APP_DIR
                    tmp_root = Path(tempfile.gettempdir()) / "dusk_zip"
                    tmp = tmp_root / p.stem
                    found.extend(extract_zip(p, tmp))
                elif p.suffix.lower() in SUPPORTED:
                    found.append(p)
                else:
                    skipped += 1
            except Exception as exc:
                log_error(f"Error handling path: {p}", exc)
        if not found:
            if skipped:
                messagebox.showwarning("DUSK — Nothing Added",
                    f"Supported extensions: {', '.join(sorted(SUPPORTED))}")
            else:
                messagebox.showinfo("DUSK — Empty", "No images found.")
            return
        self._add_to_queue(found)

    def _add_to_queue(self, paths):
        existing = set(self._items)
        new_paths = [p for p in paths if p not in existing]
        if not new_paths:
            messagebox.showinfo("DUSK — Already Queued", "All images already in queue.")
            return
        start_idx = len(self._items)
        for p in new_paths:
            self._items.append(p)
            self._thumbs.append(None)
        self._rebuild_cards()
        self._update_count()
        self._on_files_added(new_paths)
        if self._selected_idx == -1:
            self._select(start_idx)
        threading.Thread(target=self._load_thumbs,
                         args=(start_idx, list(new_paths)), daemon=True).start()

    def _remove_selected(self):
        if not (0 <= self._selected_idx < len(self._items)):
            return
        self._items.pop(self._selected_idx)
        self._thumbs.pop(self._selected_idx)
        if self._items:
            new_idx = min(self._selected_idx, len(self._items)-1)
            self._selected_idx = -1
            self._rebuild_cards()
            self._update_count()
            self._select(new_idx)
        else:
            self._selected_idx = -1
            self._rebuild_cards()
            self._update_count()

    def clear_queue(self):
        self._items.clear()
        self._thumbs.clear()
        self._selected_idx = -1
        self._rebuild_cards()
        self._update_count()

    def get_all(self):
        return list(self._items)

    def _update_count(self):
        n = len(self._items)
        self._count_lbl.config(text=f"{n} file{'s' if n != 1 else ''}")

    cls._handle_paths = _handle_paths
    cls._add_to_queue = _add_to_queue
    cls._remove_selected = _remove_selected
    cls.clear_queue = clear_queue
    cls.get_all = get_all
    cls._update_count = _update_count