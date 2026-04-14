# DUSK Photo Editor – Overview

**Tagline:** "tired yet handsome"

DUSK is a desktop GUI photo editor specialised in portrait and mood adjustments. It provides a dark, elegant interface, real‑time preview, batch processing, and advanced image manipulation.

## Core Features

- **Queue‑based import** – add images via file picker, folder scan, drag‑and‑drop, or ZIP archives.
- **Non‑destructive editing** – crop, smooth, brightness, contrast, saturation, sharpness, vignette, grain, tone (warm/cool).
- **Split / before / after preview** – see changes instantly.
- **Presets** – dusk, noir, golden, raw.
- **Batch export** – process entire queue, choose format (JPEG, PNG, WebP), quality, and optional ZIP archive.
- **Integrated logging** – all events and errors written to disk, plus an in‑app log viewer.
- **Crash resilience** – catches and logs unhandled exceptions from main thread, worker threads, and Tkinter callbacks.

## Technology Stack

- Python 3.10+
- Tkinter – GUI framework
- Pillow (PIL) – image loading, processing, thumbnails
- NumPy – fast pixel‑level operations (vignette, grain, tone)
- tkdnd (optional) – native drag‑and‑drop

## Design Philosophy

- **Modular** – every component is isolated into small files (<1 KB).
- **Self‑registering** – components are discovered automatically, no manual import chains.
- **Thread‑safe** – background tasks never touch Tkinter directly; they use `.after()` callbacks.
- **Portable** – runs on Windows, macOS, Linux with the same codebase.