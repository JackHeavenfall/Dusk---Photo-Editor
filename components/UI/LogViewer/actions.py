# actions.py
import zipfile
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from components.LOGIC.logging_setup import LOG_PATH, ERR_PATH, log, log_error

def _reload(self):
    def _read(path, widget):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        if path.exists():
            try:
                for line in path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True):
                    widget.insert("end", line, self._tag_for(line))
                widget.see("end")
            except Exception as exc:
                widget.insert("end", f"[read error: {exc}]\n", "ERROR")
        else:
            widget.insert("end", "(no log file yet)\n", "DEBUG")
        widget.config(state="disabled")

    _read(LOG_PATH, self._app_text)
    _read(ERR_PATH, self._err_text)
    self._info.config(text=f"refreshed {datetime.now().strftime('%H:%M:%S')}")

def _tag_for(self, line):
    for lvl in ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"):
        if lvl in line:
            return lvl
    return "INFO"

def _clear_view(self):
    for w in (self._app_text, self._err_text):
        w.config(state="normal")
        w.delete("1.0", "end")
        w.config(state="disabled")
    self._info.config(text="view cleared (disk files unchanged)")

def _export_logs(self):
    if not LOG_PATH.exists() and not ERR_PATH.exists():
        messagebox.showinfo("DUSK", "No log files yet.")
        return
    dest = filedialog.asksaveasfilename(
        title="Save log archive", defaultextension=".zip",
        filetypes=[("Zip archive", "*.zip")],
        initialfile=f"dusk_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
    )
    if not dest:
        return
    try:
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in (LOG_PATH, ERR_PATH):
                if p.exists():
                    zf.write(p, p.name)
        log(f"Logs exported: {dest}")
        self._info.config(text=f"exported -> {Path(dest).name}")
        messagebox.showinfo("DUSK", f"Logs saved:\n{dest}")
    except Exception as exc:
        log_error("Log export failed", exc)
        messagebox.showerror("DUSK", f"Export failed:\n{exc}")