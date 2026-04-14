# Preview Panel

The `PreviewPanel` (in `components/UI/PreviewPanel/`) shows the before/after/split view of the current image.

## Files

- `core.py` – class definition, `__init__`, `_build`, `show()`.
- `redraw.py` – `_redraw()` and `_place()` (split into separate file to stay under 1 KB).

## State

- `self._src_raw` – original PIL `Image`.
- `self._out_raw` – processed PIL `Image`.
- `self._mode` – `tk.StringVar` with values `"before"`, `"split"`, `"after"`.
- `self._refs` – list of `ImageTk.PhotoImage` references to prevent garbage collection.

## Methods

- `show(src, out, name="")` – stores the two images, updates label, calls `_redraw()`.
- `_redraw()` – called on resize and mode change. It calculates canvas dimensions, splits the area if needed, and calls `_place()` to draw each side.
- `_place(img, x, y, w, h, fw=None)` – resizes the image to fit the given rectangle (maintaining aspect ratio), creates a `PhotoImage`, and draws it on the canvas.

## Important Guard

`_redraw()` returns immediately if `self._src_raw` is `None` (no image loaded) to avoid `AttributeError`.

## Interaction with DuskApp

- After slider changes, `DuskApp._update_preview()` calls `process_image()` and then `PreviewPanel.show()`.
- The canvas resizing event also triggers `_redraw()`.