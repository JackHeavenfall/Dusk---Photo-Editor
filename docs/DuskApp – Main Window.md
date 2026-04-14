# DuskApp – Main Window

The main application class is defined in `components/UI/DuskApp/` using multiple inheritance mixins.

## Files

- `core.py` – `DuskAppCore` (inherits `tk.Tk`), sets up window geometry, exception hook, attributes.
- `build.py` – `DuskAppBuildMixin` – builds top bar, notebook, editor and log frames.
- `handlers.py` – `DuskAppHandlersMixin` – callbacks from import panel and settings.
- `export.py` – `DuskAppExportMixin` – `_export_all()`.
- `status.py` – `DuskAppStatusMixin` – optional status helper.
- `__init__.py` – assembles final `DuskApp` class and registers it.

## Attributes

- `self._current_img` – PIL `Image` of the selected image.
- `self._current_path` – `Path` of the selected image.
- `self._preview_after` – ID of pending preview update (for debouncing).
- `self._import` – `ImportPanel` instance.
- `self._preview` – `PreviewPanel` instance.
- `self._settings` – `SettingsPanel` instance.
- `self._status` – `tk.Label` at bottom for messages.

## Key Methods

- `_on_file_selected(path)` – opens image, stores it, updates preview.
- `_schedule_preview()` – cancels previous pending update, schedules new one after 200 ms.
- `_update_preview()` – calls `process_image()` with current settings, sends result to `PreviewPanel`.
- `_export_all()` – opens `ExportDialog` with current queue and settings.

## Tkinter Callback Exception Handling

`self.report_callback_exception = self._on_tk_error` captures errors from button commands, tracebacks them, and logs them to `dusk_errors.log`.