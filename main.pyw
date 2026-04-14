# main.py
# Entry point for DUSK photo editor.
# Sets up crash logging, then launches the application.

import sys
import traceback
import threading
import tkinter as tk
from tkinter import messagebox

# Import the logging setup first (must happen before any other code)
from components.LOGIC.logging_setup import init_logging, log_error, _flush_logs

init_logging()  # creates log files and hooks

# Import the registry to trigger auto‑registration of all components
import components  # noqa: F401

# Import the main application class (built from mixins)
from components.registry import get_component
DuskApp = get_component("components.UI.DuskApp")

def main():
    try:
        app = DuskApp()
        app.mainloop()
    except Exception as e:
        log_error("Fatal error in main loop", e)
        _flush_logs()
        messagebox.showerror(
            "DUSK — Fatal Error",
            f"{type(e).__name__}: {e}\n\nSee log files for details."
        )
        sys.exit(1)

if __name__ == "__main__":
    main()