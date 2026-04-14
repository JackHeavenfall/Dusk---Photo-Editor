# Constants and Theme

All visual constants are defined in `components/constants.py`. This file is imported by almost every UI component.

## Colour Palette

| Variable      | Hex       | Usage                        |
|---------------|-----------|------------------------------|
| `BG`          | `#1a1714` | Main window background       |
| `BG2`         | `#221f1b` | Side panels, sliders         |
| `BG3`         | `#2e2923` | Hover states, drop zone      |
| `SURFACE`     | `#332e27` | Buttons, import cards        |
| `SURFACE2`    | `#3d372f` | Slider troughs, borders      |
| `BORDER`      | `#4a4238` | Separator lines              |
| `TEXT`        | `#e8ddd0` | Main text                    |
| `TEXT_DIM`    | `#8a7d6e` | Secondary labels             |
| `TEXT_MUTED`  | `#5a5048` | Disabled / very dim          |
| `ACCENT`      | `#c4a882` | Slider active, highlights    |
| `ACCENT2`     | `#e8c49a` | Titles, selected text        |
| `DANGER`      | `#c47a5a` | Clear / remove buttons       |
| `SUCCESS`     | `#7a9a78` | (Reserved)                   |
| `ACTIVE_BG`   | `#3a3228` | Selected queue card          |

## Fonts

- `FONT_TITLE`   = `("Georgia", 22, "bold")`
- `FONT_LABEL`   = `("Georgia", 9, "italic")`
- `FONT_BODY`    = `("Courier", 9)`
- `FONT_BUTTON`  = `("Courier", 9, "bold")`
- `FONT_SMALL`   = `("Courier", 8)`
- `FONT_BIG`     = `("Georgia", 13)`
- `FONT_MONO`    = `("Courier New", 8)`

## Image Support

- `SUPPORTED` = `{".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}`
- Thumbnail size: `THUMB_W = 54`, `THUMB_H = 40`

## Log Colours

```python
LOG_COLORS = {
    "DEBUG":    "#5a7a8a",
    "INFO":     TEXT_DIM,
    "WARNING":  "#c4a040",
    "ERROR":    DANGER,
    "CRITICAL": "#ff6a4a",
}