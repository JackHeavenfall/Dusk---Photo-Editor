# components/constants.py
# Colors, fonts, and global constants.

# ── Palette ────────────────────────────────────────────────────────────────
BG        = "#1a1714"
BG2       = "#221f1b"
BG3       = "#2e2923"
SURFACE   = "#332e27"
SURFACE2  = "#3d372f"
BORDER    = "#4a4238"
TEXT      = "#e8ddd0"
TEXT_DIM  = "#8a7d6e"
TEXT_MUTED= "#5a5048"
ACCENT    = "#c4a882"
ACCENT2   = "#e8c49a"
DANGER    = "#c47a5a"
SUCCESS   = "#7a9a78"
ACTIVE_BG = "#3a3228"

LOG_COLORS = {
    "DEBUG":    "#5a7a8a",
    "INFO":     TEXT_DIM,
    "WARNING":  "#c4a040",
    "ERROR":    DANGER,
    "CRITICAL": "#ff6a4a",
}

# ── Fonts ─────────────────────────────────────────────────────────────────
FONT_TITLE  = ("Georgia", 22, "bold")
FONT_LABEL  = ("Georgia", 9, "italic")
FONT_BODY   = ("Courier", 9)
FONT_BUTTON = ("Courier", 9, "bold")
FONT_SMALL  = ("Courier", 8)
FONT_BIG    = ("Georgia", 13)
FONT_MONO   = ("Courier New", 8)

# ── Image support ─────────────────────────────────────────────────────────
SUPPORTED  = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
THUMB_W, THUMB_H = 54, 40