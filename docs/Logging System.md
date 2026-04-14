# Logging System

All logging is centralised in `components/LOGIC/logging_setup.py`. It is initialised **before anything else** to capture startup errors.

## Log Files

- `dusk.log` – all messages (INFO, DEBUG, WARNING, ERROR, CRITICAL).
- `dusk_errors.log` – only WARNING, ERROR, CRITICAL.

Both files are created next to `main.py` (the script directory). They are opened immediately (`delay=False`) so even a crash at import time is recorded.

## Dual Output

- **Disk files** – persistent record, rotated by the user (no automatic rotation).
- **In‑app log viewer** – messages are also sent to a `queue.Queue`; the `LogViewer` polls this queue every 500 ms and displays new messages in real time.

## Exception Hooks (Three Surfaces)

1. **`sys.excepthook`** – catches unhandled exceptions on the main thread.
2. **`threading.excepthook`** – catches unhandled exceptions in worker threads.
3. **Tkinter callback override** – `DuskApp.report_callback_exception` logs errors from button commands, slider callbacks, etc.

All hooks write the full traceback to `dusk_errors.log` and (if possible) show a message box to the user.

## AtExit Flush

`atexit.register(_flush_logs)` ensures all handlers are flushed and closed when the interpreter exits, even on crashes.

## Public Functions

```python
def log(msg, level=logging.INFO):
    """Write a message to dusk.log (and to the GUI queue)."""

def log_error(msg, exc=None):
    """Write an error message plus optional exception traceback to both logs."""

```

### Usage Example
```python
from components.LOGIC.logging_setup import log, log_error

log("Export started")
try:
    risky_operation()
except Exception as e:
    log_error("Export failed", e)

```

### Important Notes
- The logging system is not configurable at runtime – it uses fixed paths and formats.
- The GUI log viewer does not slow down the application because the queue is non‑blocking.
- If the disk is full or unwritable, logging fails silently (only a console error, which is invisible when using pythonw).