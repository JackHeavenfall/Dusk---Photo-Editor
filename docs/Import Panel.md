# Import Panel

The `ImportPanel` (in `components/UI/ImportPanel/`) is the left‑side queue manager. It is split into six files, each <1 KB.

## File Responsibilities

| File | Responsibility |
|------|----------------|
| `core.py` | Constructor, basic layout, references to other parts. |
| `add_buttons.py` | Three large import buttons (files, folder, zip) and their browse actions. |
| `drop_target.py` | Drag‑and‑drop zone, integration with `tkdnd` (if available). |
| `queue_management.py` | Adding/removing items, handling paths, ZIP extraction, duplicate detection. |
| `card_rendering.py` | Drawing the thumbnail cards, selection, scrolling. |
| `thumb_loading.py` | Background thread that generates thumbnails. |

## Queue Data Structures

- `self._items`: list of `Path` objects (image files).
- `self._thumbs`: parallel list of `ImageTk.PhotoImage` or `None` (not yet loaded).
- `self._selected_idx`: index of currently selected card, or -1.

## Supported File Sources

- **Single files** – any image with extension in `SUPPORTED`.
- **Folder** – recursively scanned for images (all subfolders).
- **ZIP archive** – extracted to a temporary directory (`tempfile.gettempdir()/dusk_zip`), then scanned for images.

## Drag‑and‑Drop Behaviour

- Uses `tkdnd` if the Tk package is available. On Windows, it usually is; on macOS/Linux, the user may need to install it.
- If `tkdnd` is not present, the drop zone still works as a click‑to‑browse button.
- Dropped files can be images, folders, or ZIPs – handled the same way as manual browsing.

## Thumbnail Loading

- Thumbnails are generated in a **daemon thread** so the UI remains responsive.
- Each thumbnail is centred on a dark grey square (RGB 30,28,25).
- When a thumbnail is ready, it triggers a card rebuild on the main thread via `.after(0, self._rebuild_cards)`.

## Public Methods

- `get_all()` → returns a copy of `self._items`.
- `clear_queue()` → empties the queue and rebuilds the card list.

## Callbacks

- `on_select(path)` – called when the user clicks a card.
- `on_files_added(paths)` – called after new files are successfully added.