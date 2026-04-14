# components/UI/DuskApp/core.py
import tkinter as tk
import traceback
from components.constants import BG, FONT_TITLE, TEXT_MUTED, ACCENT2
from components.LOGIC.logging_setup import err_log, _flush_logs, log
from tkinter import messagebox

class DuskAppCore(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DUSK - portrait editor")
        self.geometry("1320x840")
        self.minsize(1000, 660)
        self.configure(bg=BG)

        self._current_img = None
        self._current_path = None
        self._preview_after = None

        # Tkinter callback exception hook
        self.report_callback_exception = self._on_tk_error

        # Build UI (defined in build mixin)
        self._build()

        log("DUSK started — UI ready")

    def _on_tk_error(self, exc_type, exc_val, exc_tb):
        text = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
        err_log.critical("TK CALLBACK EXCEPTION\n" + text)
        _flush_logs()
        try:
            messagebox.showerror(
                "DUSK — Error",
                f"An error occurred: {exc_val}\n\n"
                f"Full details saved to:\n{err_log.handlers[0].baseFilename}"
            )
        except Exception:
            pass

    def destroy(self):
        log("DUSK exiting cleanly")
        _flush_logs()
        super().destroy()