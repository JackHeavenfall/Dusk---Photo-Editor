# Export Dialog

The `ExportDialog` (in `components/UI/ExportDialog/`) handles batch export of the queue.

## Files

- `core.py` – dialog layout, `__init__`, `_build`, `_browse_dir`, `_cancel`, `_start`.
- `worker.py` – `_worker()` (background processing).

## User Options

- **Output folder** – user‑selectable, defaults to `~/Pictures/dusk_output`.
- **Format** – JPEG, PNG, WebP.
- **JPEG quality** – slider 60–100 (ignored for PNG/WebP).
- **Zip output** – if checked, all exported images are packed into a ZIP archive.
- **ZIP name** – base name for the archive.

## Export Process

1. User clicks "export" → `_start()` sets `_running = True`, shows progress bar, starts `_worker` thread.
2. Worker creates output folder, iterates over `self._files`:
   - Load image with PIL.
   - Apply `process_image()` using the current settings.
   - Save with appropriate format.
   - Update progress bar via `self.after()`.
3. If cancelled (`_running = False`), stops early.
4. After all images, if ZIP requested, creates a ZIP file containing all exported images.
5. Shows completion message, changes button text to "done ✓".

## Thread Safety

- All Tkinter calls (progress updates, label changes) are wrapped in `self.after(0, lambda: ...)`.
- The dialog disables the export button while running to prevent multiple threads.