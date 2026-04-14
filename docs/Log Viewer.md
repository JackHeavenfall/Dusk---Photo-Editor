# Log Viewer

The `LogViewer` (in `components/UI/LogViewer/`) displays live and historical logs inside the application.

## Files

- `core.py` – `__init__`, `_build`, `_tab`, `_poll`, `_append`.
- `actions.py` – `_reload`, `_tag_for`, `_clear_view`, `_export_logs`.

## How It Works

- **Live log feed** – polls `_gui_log_queue` (the same queue used by the `_QueueHandler` in `logging_setup.py`). New records are appended to the "app log" tab; errors also go to the "error log" tab.
- **File reload** – reads `dusk.log` and `dusk_errors.log` directly from disk. This shows the complete history, including messages logged before the LogViewer was created.
- **Colour coding** – uses `LOG_COLORS` dict from `constants.py` to tag different log levels.

## UI Controls

- **Refresh** – reloads from disk files.
- **Clear view** – clears the text widgets (does not delete disk logs).
- **Export logs** – saves both log files as a ZIP archive.

## Tagging

Each line in the text widget is tagged with the log level (e.g., "ERROR"). The tag configuration sets the foreground colour.

## Polling Interval

`self.after(500, self._poll)` – runs every 500 ms.