# components/UI/DuskApp/handlers.py
from PIL import Image
from components.LOGIC.logging_setup import log, log_error
from components.LOGIC.image_processing import process_image
from tkinter import messagebox

class DuskAppHandlersMixin:
    def _on_files_added(self, files):
        n = len(files)
        self._status.config(
            text=f"added {n} file{'s' if n != 1 else ''} to queue")

    def _on_file_selected(self, path):
        try:
            self._current_img = Image.open(path)
            self._current_path = path
            self._status.config(text=f"viewing  {path.name}")
            log(f"Selected: {path}")
            self._update_preview()
        except Exception as exc:
            log_error(f"Cannot open: {path}", exc)
            self._status.config(
                text=f"error opening {path.name} — see logs")
            messagebox.showerror("DUSK — Open Error",
                f"Could not open image:\n{path.name}\n\n"
                f"{type(exc).__name__}: {exc}")

    def _schedule_preview(self):
        if self._preview_after:
            self.after_cancel(self._preview_after)
        self._preview_after = self.after(200, self._update_preview)

    def _update_preview(self):
        if self._current_img is None:
            return
        try:
            out = process_image(self._current_img.copy(),
                                self._settings.get_settings())
            self._preview.show(
                self._current_img, out,
                self._current_path.name if self._current_path else "")
        except Exception as exc:
            log_error("Preview render error", exc)
            self._status.config(text="preview error — see logs")