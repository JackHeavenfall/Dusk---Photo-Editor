# components/LOGIC/logging_setup.py
import logging
import sys
import threading
import queue as Queue
import atexit
import traceback
from datetime import datetime  # <-- ADDED
from pathlib import Path

# Determine script directory
try:
    _SCRIPT_DIR = Path(__file__).resolve().parent.parent.parent
except NameError:
    _SCRIPT_DIR = Path.cwd()

LOG_PATH = _SCRIPT_DIR / "dusk.log"
ERR_PATH = _SCRIPT_DIR / "dusk_errors.log"

_FMT = "%(asctime)s  %(levelname)-8s  %(message)s"
_DATE = "%Y-%m-%d %H:%M:%S"
_formatter = logging.Formatter(_FMT, datefmt=_DATE)

app_log = logging.getLogger("dusk.app")
err_log = logging.getLogger("dusk.error")
app_log.setLevel(logging.DEBUG)
err_log.setLevel(logging.WARNING)

_app_fh = logging.FileHandler(LOG_PATH, encoding="utf-8", delay=False)
_err_fh = logging.FileHandler(ERR_PATH, encoding="utf-8", delay=False)
_app_fh.setFormatter(_formatter)
_err_fh.setFormatter(_formatter)
app_log.addHandler(_app_fh)
err_log.addHandler(_err_fh)

_gui_log_queue = Queue.Queue()

class _QueueHandler(logging.Handler):
    def emit(self, record):
        try:
            self.format(record)
            _gui_log_queue.put_nowait(record)
        except Exception:
            pass

_qh = _QueueHandler()
_qh.setFormatter(_formatter)
app_log.addHandler(_qh)
err_log.addHandler(_qh)

def log(msg, level=logging.INFO):
    app_log.log(level, msg)

def log_error(msg, exc=None):
    if exc:
        tb = traceback.format_exc()
        full = f"{msg} | {type(exc).__name__}: {exc}\n{tb}"
    else:
        full = msg
    err_log.error(full)
    app_log.error(full)

def _flush_logs():
    for h in list(app_log.handlers) + list(err_log.handlers):
        try:
            h.flush()
            h.close()
        except Exception:
            pass

atexit.register(_flush_logs)

def _excepthook(exc_type, exc_val, exc_tb):
    text = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
    err_log.critical("UNHANDLED EXCEPTION (main thread)\n" + text)
    _flush_logs()
    try:
        from tkinter import messagebox
        messagebox.showerror(
            "DUSK — Crashed",
            f"{exc_type.__name__}: {exc_val}\n\nFull crash details saved to:\n{ERR_PATH}")
    except Exception:
        pass

def _thread_excepthook(args):
    text = "".join(traceback.format_exception(
        args.exc_type, args.exc_value, args.exc_traceback))
    name = getattr(args.thread, "name", "unknown")
    err_log.critical(f"UNHANDLED EXCEPTION (thread: {name})\n" + text)
    _flush_logs()

sys.excepthook = _excepthook
threading.excepthook = _thread_excepthook

def init_logging():
    """Call this at the very start of main.py to set up logging."""
    app_log.info("=" * 60)
    app_log.info(f"DUSK logging initialized")
    app_log.info(f"Logs: {LOG_PATH}")
    app_log.info(f"Errors: {ERR_PATH}")
    app_log.info("=" * 60)

APP_DIR = _SCRIPT_DIR