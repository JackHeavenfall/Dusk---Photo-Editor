# Architecture

DUSK follows a modular, self‑registering component architecture. All major UI elements and logic modules are isolated into small files (<1 KB each) and automatically discovered through a central registry.

## High‑Level Data Flow

1. **User adds images** → `ImportPanel` → queue (list of `Path` objects).
2. **User selects an image** → `DuskApp._on_file_selected` → loads PIL `Image` → stores in `self._current_img`.
3. **User adjusts a slider** → `SettingsPanel` triggers `on_change` → `DuskApp._schedule_preview` (debounced 200 ms) → `_update_preview` → calls `process_image()` → sends result to `PreviewPanel.show()`.
4. **User clicks "export all"** → `ExportDialog` opens, runs background thread to process all queued images with current settings.
5. **Logging** – every component uses `log()` and `log_error()`; messages go to both disk files and the in‑app `LogViewer`.

## Component Categories

- **Logic modules** (`components/LOGIC/`) – no GUI, pure functions.
- **UI components** (`components/UI/`) – each is a Tkinter widget class that registers itself.
- **Registry** – maps module names (e.g., `"components.UI.DuskButton"`) to class objects.

## Initialization Sequence (main.py)

1. `init_logging()` – sets up file handlers, queue handler, exception hooks.
2. `import components` – triggers all `register()` calls in UI and LOGIC submodules.
3. `get_component("components.UI.DuskApp")` – retrieves the main application class.
4. Instantiate `DuskApp`, which builds all sub‑panels.
5. `app.mainloop()` starts the Tkinter event loop.

## Why Self‑Registration?

- Eliminates manual import chains.
- Allows easy addition of new components without editing existing files.
- Keeps each file under 1 KB (fragmentation enforced).
- The registry acts as a central service locator.

## Threading

- Thumbnail loading runs in a daemon thread.
- Export runs in a daemon thread.
- Log polling (from queue to GUI) runs via `after()` calls on the main thread.
- All Tkinter updates are scheduled with `.after()` to avoid cross‑thread issues.