# Replication Guide for AI Agents

This guide explains how to recreate the DUSK project **from scratch using only the documentation** in this `docs/` folder. It assumes you have read all other `.md` files (Architecture, Component Registry, Constants, Logging System, Image Pipeline, Import Panel, Preview Panel, Settings Panel, Log Viewer, Export Dialog, DuskApp, Installation). The goal is to produce a working application with identical behaviour and structure.

## Overview of the Replication Process

1. **Understand the architecture** – self‑registering components, data flow, threading model.
2. **Set up the directory tree** – exactly as described in `Architecture.md`.
3. **Implement the central registry** – a simple dictionary with `register()` and `get_component()`.
4. **Implement the logging system** – file handlers, queue handler, three exception hooks.
5. **Implement the constants** – colours, fonts, supported extensions, thumbnail size.
6. **Implement the logic modules** – `default_settings`, `image_processing`, `zip_utils`.
7. **Implement each UI component** – following the file splits described in their respective docs.
8. **Implement the main application (`DuskApp`)** – using mixins, assembling all panels.
9. **Write `main.py`** – initialisation sequence, registry retrieval, event loop.
10. **Apply the known fixes** (from the debugging session) – see below.

## Step 1 – Create the Directory Structure

Create the following folders and empty files (the exact names matter):

```
project/
├── main.py
├── components/
│   ├── __init__.py
│   ├── registry.py
│   ├── constants.py
│   ├── LOGIC/
│   │   ├── __init__.py
│   │   ├── logging_setup.py
│   │   ├── image_processing.py
│   │   ├── default_settings.py
│   │   └── zip_utils.py
│   ├── UI/
│   │   ├── __init__.py
│   │   ├── DuskButton.py
│   │   ├── DuskSlider.py
│   │   ├── PreviewPanel/
│   │   │   ├── __init__.py
│   │   │   ├── core.py
│   │   │   └── redraw.py
│   │   ├── SettingsPanel/
│   │   │   ├── __init__.py
│   │   │   ├── core.py
│   │   │   ├── build.py
│   │   │   └── preset_reset.py
│   │   ├── LogViewer/
│   │   │   ├── __init__.py
│   │   │   ├── core.py
│   │   │   └── actions.py
│   │   ├── ExportDialog/
│   │   │   ├── __init__.py
│   │   │   ├── core.py
│   │   │   └── worker.py
│   │   ├── ImportPanel/
│   │   │   ├── __init__.py
│   │   │   ├── core.py
│   │   │   ├── add_buttons.py
│   │   │   ├── drop_target.py
│   │   │   ├── queue_management.py
│   │   │   ├── card_rendering.py
│   │   │   └── thumb_loading.py
│   │   └── DuskApp/
│   │       ├── __init__.py
│   │       ├── core.py
│   │       ├── build.py
│   │       ├── handlers.py
│   │       ├── export.py
│   │       └── status.py
│   └── operations/
│       ├── __init__.py
│       └── drag_drop.py   (can be empty)
```

## Step 2 – Implement the Registry

File: `components/registry.py` – a minimal dictionary with three functions:

```python
_registry = {}

def register(module_name, cls_or_func):
    _registry[module_name] = cls_or_func

def get_component(module_name):
    if module_name not in _registry:
        raise ImportError(f"Component '{module_name}' not registered")
    return _registry[module_name]

def get_registry():
    return _registry.copy()
```

## Step 3 – Implement Logging System

File: `components/LOGIC/logging_setup.py`

Follow `Logging System.md`. Key points:

- Determine `_SCRIPT_DIR` as the parent of the `components` folder (use `Path(__file__).resolve().parent.parent`).
- Create `LOG_PATH` and `ERR_PATH` next to `main.py`.
- Set up two file handlers (`delay=False`).
- Create a `_QueueHandler` that puts records into a `queue.Queue`.
- Define `log()` and `log_error()`.
- Install `sys.excepthook` and `threading.excepthook`.
- Register `atexit` flush.
- Provide `init_logging()` that writes a startup banner.

**Important:** The queue variable (`_gui_log_queue`) must be accessible from `LogViewer` – either export it or keep it as a module‑level variable.

## Step 4 – Implement Constants

File: `components/constants.py`

Exactly as in `Constants and Theme.md`. No code logic, just variables.

## Step 5 – Implement Logic Modules

- **`default_settings.py`** – function returning the dictionary.
- **`image_processing.py`** – implement the 7‑step pipeline using PIL and NumPy. Use the exact order and formulas described in `Image Processing Pipeline.md`.
- **`zip_utils.py`** – function `extract_zip(zip_path, tmp_dir)` that extracts and returns a list of image paths (using `SUPPORTED` from constants). Use `tempfile.gettempdir()` for the base temporary folder.

## Step 6 – Implement UI Components (Theory)

Each UI component must:

- Be a class inheriting from `tk.Frame` (or `tk.Toplevel` for `ExportDialog`).
- Register itself at the end of its `__init__.py` (or main `.py` file) using `register(__name__, ClassName)`.
- Use direct imports for dependencies inside the same package (e.g., `from ..DuskButton import DuskButton`). Only use `get_component()` for cross‑package dependencies when absolutely necessary (avoid it inside UI components – import directly).

### 6.1 DuskButton and DuskSlider

Simple widgets – see their descriptions. `DuskButton` has four variants: normal, accent, danger, ghost. `DuskSlider` is a frame containing a label, a value display, and a `tk.Scale`.

### 6.2 ImportPanel

Split into six files as per `Import Panel.md`. The constructor (`core.py`) creates the basic layout and calls methods from the other files (which are monkey‑patched into the class). Use the `extend_*` pattern shown in the original code: each helper file defines a function that adds methods to the class.

**Critical:** The background thumbnail loading must be in a daemon thread. Use `PIL.Image.thumbnail()` and centre the image on a dark square.

### 6.3 PreviewPanel

Two files: `core.py` and `redraw.py`. Implement `show()`, `_redraw()`, `_place()`. The guard in `_redraw()` must return early if `self._src_raw is None`.

**Fix:** In `core.py`, initialise `self._mode = tk.StringVar(value="split")` **before** calling `self._build()`.

### 6.4 SettingsPanel

Three files: `core.py`, `build.py`, `preset_reset.py`. Use `DuskSlider` for each parameter. The `_build` method creates a scrollable canvas with sections and presets.

**Fix:** In `core.py`, import `DuskSlider` from `components.UI.DuskSlider` (not from `DuskButton`).

### 6.5 LogViewer

Two files: `core.py` and `actions.py`. The `_poll` method reads from `_gui_log_queue` every 500 ms. The `_reload` method reads the log files from disk.

### 6.6 ExportDialog

Two files: `core.py` and `worker.py`. The worker runs in a daemon thread and uses `self.after(0, ...)` for all Tkinter updates.

### 6.7 DuskApp

Six files as listed in `DuskApp – Main Window.md`. Use multiple inheritance to combine mixins. The `_build` method creates the top bar, the notebook, and places the editor and log frames.

**Important:** In `build.py`, use **direct imports** for all UI components (`from components.UI.ImportPanel import ImportPanel`, etc.), not `get_component()`. This avoids circular imports.

## Step 7 – Write `main.py`

```python
import sys
from components.LOGIC.logging_setup import init_logging, log_error, _flush_logs
init_logging()

import components   # triggers all registrations

from components.registry import get_component
DuskApp = get_component("components.UI.DuskApp")

def main():
    try:
        app = DuskApp()
        app.mainloop()
    except Exception as e:
        log_error("Fatal error in main loop", e)
        _flush_logs()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Step 8 – Apply the Known Fixes (Essential)

The documentation does not include these because they emerged during debugging. Apply them manually:

1. **PreviewPanel** – in `core.py`, move `self._mode` initialisation above `self._build()`.
2. **PreviewPanel.redraw** – add guard:
   ```python
   if self._src_raw is None or self._out_raw is None:
       return
   ```
3. **SettingsPanel.core** – change import to `from components.UI.DuskSlider import DuskSlider`.
4. **DuskApp.build** – replace any `get_component()` calls with direct imports.
5. **components/UI/__init__.py** – must import all sub‑packages:
   ```python
   from . import DuskButton, DuskSlider, PreviewPanel, SettingsPanel, LogViewer, ExportDialog, ImportPanel, DuskApp
   ```
6. **Every component’s `__init__.py`** – must call `register(__name__, ClassName)` at the end.

## Step 9 – Test Incrementally

- Run `python main.py` – no errors, window appears.
- Add an image via “Browse Files” – thumbnail appears.
- Click thumbnail – preview shows the image.
- Adjust a slider – preview updates after 200 ms.
- Switch preview modes – before, split, after.
- Export a single image – output folder created, file saved.
- Test drag‑and‑drop (if `tkdnd` available).
- Test ZIP import.
- Check log files and in‑app log viewer.

## Step 10 – Packaging (Optional)

Follow `Installation and Running.md` for PyInstaller.

## Verification Criteria

A successful replication must satisfy:

- No `ImportError` or `AttributeError` on startup.
- All sliders work and affect the preview.
- The queue can hold multiple images, thumbnails load asynchronously.
- Export processes all images with current settings.
- Logs are written to disk and visible in the Log Viewer.
- The application closes cleanly (no zombie threads).

## Final Notes

- Do **not** hardcode absolute paths. Use `Path(__file__).resolve().parent` and `tempfile.gettempdir()`.
- All background threads must be daemons (`daemon=True`).
- Every Tkinter update from a non‑main thread must use `widget.after(0, callback)`.
- Keep every Python file under 1 KB. If a file grows larger, split it further.
- The registry is **only** for locating components, not for importing internal helpers. Use normal Python imports for intra‑package dependencies.

With this guide and the other `.md` files, an AI agent can reconstruct the entire DUSK photo editor without seeing the original source code.